#!/usr/bin/env python3

"""
Generate a Blackboard Classic vs Blackboard Ultra HTML-sanitization showcase.

Runs five biology-problems question generators, each of which emits inline HTML
that Blackboard Classic renders correctly but Blackboard Ultra's HTML sanitizer
strips or flattens. Two questions are produced from each generator, the ten
questions are concatenated into a single BBQ upload file, and that file is then
converted to QTI v2.1 with qti-package-maker's bbq_converter tool.

The five generators and the CSS feature each one depends on:
  1. monohybrid_degrees_of_dominance   color: text spans (inline style)
  2. classify_Haworth                  table spacing / border-* (ring drawing)
  3. dihybrid_cross_epistatic_metabolics background-color (Punnett answer key)
  4. deletion_mutant_random            width/position bars (deletion map)
  5. write_pedigree_match_random       background-color + border (symbol fill)

Upload the BBQ file to Blackboard Classic and the QTI v2.1 package to Blackboard
Ultra, then compare the rendered questions to see the sanitization differences.
"""

import os
import sys
import glob
import shutil
import subprocess

#======================================
# Each generator: a label, the script path relative to the repo root, and the
# extra CLI flags it needs beyond the shared "-x 2" question-count flag.
GENERATORS = [
	{
		'label': '1_inline_color_monohybrid',
		'script': 'problems/inheritance-problems/monohybrid_degrees_of_dominance.py',
		'extra_args': [],
	},
	{
		'label': '2_table_borders_haworth',
		'script': 'problems/biochemistry-problems/carbs/classify_Haworth.py',
		'extra_args': ['--pyran'],
	},
	{
		'label': '3_bgcolor_epistasis_cross',
		'script': 'problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_metabolics.py',
		'extra_args': [],
	},
	{
		'label': '4_position_bars_deletion',
		'script': 'problems/inheritance-problems/deletion_mutants/deletion_mutant_random.py',
		'extra_args': ['--num-genes', '6'],
	},
	{
		# A simple text matching question. Blackboard's QTI v2.1 package import
		# supports only Multiple Choice, Fill-in-the-Blank, Essay, and True/False,
		# so Matching (MAT) is dropped on import. This slot demonstrates that drop
		# directly with a minimal genetics matching set (no heavy HTML), proving the
		# loss is the QTI matching limitation, not pedigree-specific HTML.
		'label': '5_matching_dominance',
		'script': 'problems/matching_sets/yaml_match_to_bbq.py',
		'input_file': 'problems/matching_sets/inheritance/degrees_of_dominance.yml',
		'extra_args': [],
	},
]

# Two questions from every generator.
QUESTIONS_PER_GENERATOR = 2

# Stable output directory name so repeated runs overwrite instead of piling up.
OUTPUT_DIRNAME = 'output_showcase'

# Combined BBQ filename must match bbq_converter's expected
# "bbq-(core_name)-questions.txt" pattern.
COMBINED_CORE_NAME = 'ultra_classic_showcase'

#======================================
def get_repo_root() -> str:
	"""Return the repository top level using git, not derived from CWD."""
	result = subprocess.run(
		['git', 'rev-parse', '--show-toplevel'],
		capture_output=True, text=True, check=True,
	)
	repo_root = result.stdout.strip()
	return repo_root

#======================================
def build_subprocess_env(repo_root: str, qti_maker_dir: str) -> dict:
	"""Build an environment with repo root and qti-package-maker on PYTHONPATH."""
	env = dict(os.environ)
	# Each generator self-inserts its own local import dir, but bptools lives at
	# the repo root and bbq_converter needs qti-package-maker importable.
	path_parts = [repo_root, qti_maker_dir]
	existing = env.get('PYTHONPATH', '')
	if existing:
		path_parts.append(existing)
	env['PYTHONPATH'] = ':'.join(path_parts)
	# Quieter, no bytecode litter (scripts still work without these).
	env['PYTHONUNBUFFERED'] = '1'
	env['PYTHONDONTWRITEBYTECODE'] = '1'
	return env

#======================================
def run_generator(generator: dict, repo_root: str, parts_dir: str, env: dict) -> str:
	"""
	Run one generator in its own clean subdirectory and return the path to the
	single BBQ file it produced.
	"""
	work_dir = os.path.join(parts_dir, generator['label'])
	# Clean and recreate the per-generator work dir.
	if os.path.isdir(work_dir):
		shutil.rmtree(work_dir)
	os.makedirs(work_dir)

	script_abspath = os.path.join(repo_root, generator['script'])
	if not os.path.isfile(script_abspath):
		raise FileNotFoundError(f"Generator script not found: {script_abspath}")

	# Build the command: python3 <script> -x 2 <anti-cheat off> <extra args>.
	# The showcase is about HTML sanitization, not security, so disable both shared
	# bptools anti-cheat features: hidden decoy terms and the no-click div wrapper.
	# Their injected markup would otherwise pollute the HTML being compared.
	command = [
		sys.executable, script_abspath,
		'-x', str(QUESTIONS_PER_GENERATOR),
		'--no-hidden-terms',
		'--allow-click',
	]
	command += generator['extra_args']

	# Some generators read a YAML/data file via "-f". Resolve it to an absolute
	# path because the generator runs with cwd set to its per-generator work dir.
	if 'input_file' in generator:
		input_abspath = os.path.join(repo_root, generator['input_file'])
		if not os.path.isfile(input_abspath):
			raise FileNotFoundError(f"Generator input file not found: {input_abspath}")
		command += ['-f', input_abspath]

	print(f"\n=== Running {generator['label']} ===")
	print("    " + " ".join(command))
	# Run inside the work dir so the relative bbq output lands there. Python adds
	# the script's own directory to sys.path[0], so the local library imports
	# resolve regardless of this cwd.
	subprocess.run(command, cwd=work_dir, env=env, check=True)

	# Locate the produced BBQ file (exactly one expected).
	bbq_files = glob.glob(os.path.join(work_dir, 'bbq-*-questions.txt'))
	if len(bbq_files) != 1:
		raise RuntimeError(
			f"Expected exactly one BBQ file in {work_dir}, found {len(bbq_files)}: {bbq_files}"
		)
	return bbq_files[0]

#======================================
def read_bbq_text(bbq_file: str) -> str:
	"""Read a BBQ file and return its text, guaranteeing a trailing newline."""
	with open(bbq_file, 'r') as f:
		text = f.read()
	if len(text) > 0 and not text.endswith('\n'):
		text += '\n'
	return text

#======================================
def convert_to_qti(combined_bbq_path: str, qti_maker_dir: str, output_dir: str, env: dict):
	"""Convert the combined BBQ file to QTI v2.1 via bbq_converter."""
	converter = os.path.join(qti_maker_dir, 'tools', 'bbq_converter.py')
	if not os.path.isfile(converter):
		raise FileNotFoundError(f"bbq_converter not found: {converter}")

	# "-2" selects the Blackboard QTI v2.1 output engine. "--allow-mixed" is
	# required because the showcase deliberately mixes MC and MA question types.
	command = [sys.executable, converter, '-i', combined_bbq_path, '-2', '--allow-mixed']
	print("\n=== Converting combined BBQ to QTI v2.1 ===")
	print("    " + " ".join(command))
	# Run in the output dir so the QTI package zip is written alongside the BBQ.
	subprocess.run(command, cwd=output_dir, env=env, check=True)

#======================================
def main():
	repo_root = get_repo_root()
	repo_parent = os.path.dirname(repo_root)
	qti_maker_dir = os.path.join(repo_parent, 'qti-package-maker')
	if not os.path.isdir(qti_maker_dir):
		raise FileNotFoundError(
			f"qti-package-maker repo not found alongside this repo at: {qti_maker_dir}"
		)

	# Prepare output directory (stable name, overwritten each run).
	output_dir = os.path.join(repo_root, OUTPUT_DIRNAME)
	parts_dir = os.path.join(output_dir, 'parts')
	os.makedirs(parts_dir, exist_ok=True)

	env = build_subprocess_env(repo_root, qti_maker_dir)

	# Generate each set and gather the BBQ text in showcase order.
	combined_text = ''
	for generator in GENERATORS:
		bbq_file = run_generator(generator, repo_root, parts_dir, env)
		combined_text += read_bbq_text(bbq_file)

	# Write the single combined BBQ upload file.
	combined_name = f"bbq-{COMBINED_CORE_NAME}-questions.txt"
	combined_bbq_path = os.path.join(output_dir, combined_name)
	with open(combined_bbq_path, 'w') as f:
		f.write(combined_text)
	question_lines = [line for line in combined_text.split('\n') if line.strip()]
	print(f"\nWrote {len(question_lines)} questions to {combined_bbq_path}")

	# Convert the combined BBQ to QTI v2.1.
	convert_to_qti(combined_bbq_path, qti_maker_dir, output_dir, env)

	print("\nDONE.")
	print(f"  BBQ (Blackboard Classic upload): {combined_bbq_path}")
	print(f"  QTI v2.1 package (Blackboard Ultra import): see {output_dir}")

#======================================
if __name__ == '__main__':
	main()

## THE END
