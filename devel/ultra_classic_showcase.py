#!/usr/bin/env python3

"""
Generate a Blackboard Classic vs Blackboard Ultra HTML-sanitization showcase.

Runs ten biology-problems question generators spanning six question types (MC,
MA, MATCH, FIB, MULTI_FIB, NUM). Several emit inline HTML that Blackboard Classic
renders correctly but Blackboard Ultra's HTML sanitizer strips or flattens. Two
questions are produced from each generator, then grouped by question type and each
type converted to its own pair of packages with qti-package-maker's bbq_converter
tool: a QTI v2.1 package and a Blackboard pool export ZIP. Grouping by type gives
one Ultra bank per question type. All questions are also gathered into one combined
BBQ file (single Blackboard Classic upload) and one complete showcase package (one
QTI v2.1 + one Blackboard pool export holding every type).

The ten generators, their question type, and the feature each demonstrates:
   1. monohybrid_degrees_of_dominance      MC    color: text spans (inline style)
   2. classify_Haworth                     MC    table spacing / border-* (ring)
   3. dihybrid_cross_epistatic_metabolics  MA/MC background-color (Punnett key)
   4. deletion_mutant_random               MC    width/position bars (deletion map)
   5. yaml_match_to_bbq (degrees_of_dominance) MATCH  QTI drops matching on import
   6. overhang_sequence                    FIB   restriction overhang sequence
   7. three-point_test_cross-distances_plus MULTI_FIB  gene order + map distances
   8. protein_gel_migration                NUM   protein MW from migration
   9. kaleidoscope_ladder_unknown_band     NUM   ladder MW (percent tolerance)
  10. two-point_test_cross-distance        NUM   genetics map distance (cM)

Upload the BBQ file to Blackboard Classic and the packages to Blackboard Ultra,
then compare. HTML generators show the sanitization differences; the QTI v2.1
import drops the Matching question, while the Blackboard pool export ZIP, imported
through Ultra's Import Pool / Import from file door, carries every type in.
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
	{
		# Plain Fill-in-the-Blank: restriction-enzyme overhang sequence. Matches the
		# real Blackboard sample Ch02.4 Overhang_Sequence_FiB.
		'label': '6_fib_overhang_sequence',
		'script': 'problems/molecular_biology-problems/overhang_sequence.py',
		'extra_args': ['--fib'],
	},
	{
		# Multi-blank Fill-in-the-Blank (Plus): three-point test cross gene order and
		# distances. Matches the real Blackboard sample Ch05.3 Three-Point ... Plus.
		'label': '7_multifib_three_point_cross',
		'script': 'problems/inheritance-problems/gene_mapping/three-point_test_cross-distances_plus.py',
		'extra_args': [],
	},
	{
		# Numeric entry: protein molecular weight from gel migration. Matches the real
		# Blackboard sample Ch05 Gel Migration Calc Numeric.
		'label': '8_num_protein_gel_migration',
		'script': 'problems/biochemistry-problems/electrophoresis/protein_gel_migration.py',
		'extra_args': ['--num'],
	},
	{
		# Numeric entry: unknown band molecular weight from a Kaleidoscope ladder
		# (biochem electrophoresis). Percent-based tolerances exercise another shape.
		'label': '9_num_kaleidoscope_ladder',
		'script': 'problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band.py',
		'extra_args': ['--num'],
	},
	{
		# Numeric entry: map distance (cM) from a two-point test cross (genetics).
		# Genetics test crosses are a natural numeric-answer source.
		'label': '10_num_two_point_test_cross',
		'script': 'problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py',
		'extra_args': ['--num'],
	},
]

# Two questions from every generator.
QUESTIONS_PER_GENERATOR = 2

# Stable output directory name so repeated runs overwrite instead of piling up.
OUTPUT_DIRNAME = 'output_showcase'

# Combined BBQ filename must match bbq_converter's expected
# "bbq-(core_name)-questions.txt" pattern.
COMBINED_CORE_NAME = 'ultra_classic_showcase'

# Map each BBQ leading type token to a readable question-type name. The output is
# grouped by question type, and each type name becomes the Ultra bank name. ORDER is
# intentionally absent: it is out of scope and known to fail on Blackboard import.
TYPE_NAMES = {
	'MC': 'MC',
	'MA': 'MA',
	'MAT': 'MATCH',
	'NUM': 'NUM',
	'FIB': 'FIB',
	'FIB_PLUS': 'MULTI_FIB',
}

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
def write_named_bbq(text: str, core_name: str, output_dir: str) -> str:
	"""
	Write BBQ text to a uniquely-named file matching bbq_converter's expected
	"bbq-(core_name)-questions.txt" pattern, and return its path. The core name
	becomes the package/bank name inside Blackboard, so a unique core name per
	upload keeps the Ultra banks from colliding.
	"""
	bbq_path = os.path.join(output_dir, f"bbq-{core_name}-questions.txt")
	with open(bbq_path, 'w') as f:
		f.write(text)
	return bbq_path

#======================================
def convert_one(bbq_path: str, qti_maker_dir: str, output_dir: str, env: dict):
	"""
	Convert one BBQ file to both packages in a single bbq_converter call: QTI v2.1
	(drops Matching on Ultra import) and the Blackboard pool export ZIP (carries
	Matching into Ultra via Import Pool / Import from file).
	"""
	converter = os.path.join(qti_maker_dir, 'tools', 'bbq_converter.py')
	if not os.path.isfile(converter):
		raise FileNotFoundError(f"bbq_converter not found: {converter}")

	# "-2" selects the Blackboard QTI v2.1 engine; "-B" selects the Blackboard
	# pool export ZIP engine. The converter appends both into one output list, so a
	# single call emits both packages. "--allow-mixed" is required because some
	# per-generator sets mix question types (the epistasis set emits MA alongside MC).
	command = [sys.executable, converter, '-i', bbq_path, '-2', '-B', '--allow-mixed']
	print("    " + " ".join(command))
	# Run in the output dir so both package zips are written alongside the BBQ.
	subprocess.run(command, cwd=output_dir, env=env, check=True)

#======================================
def clean_prior_outputs(output_dir: str):
	"""Remove this script's prior top-level outputs so each run leaves a clean set."""
	patterns = ['bbq-*-questions.txt', 'qti21-*.zip', 'blackboard_export_zip-*.zip']
	for pattern in patterns:
		for path in glob.glob(os.path.join(output_dir, pattern)):
			os.remove(path)

#======================================
def main():
	repo_root = get_repo_root()
	repo_parent = os.path.dirname(repo_root)
	qti_maker_dir = os.path.join(repo_parent, 'qti-package-maker')
	if not os.path.isdir(qti_maker_dir):
		raise FileNotFoundError(
			f"qti-package-maker repo not found alongside this repo at: {qti_maker_dir}"
		)

	# Prepare output directory (stable name) and clear prior outputs each run.
	output_dir = os.path.join(repo_root, OUTPUT_DIRNAME)
	parts_dir = os.path.join(output_dir, 'parts')
	os.makedirs(parts_dir, exist_ok=True)
	clean_prior_outputs(output_dir)

	env = build_subprocess_env(repo_root, qti_maker_dir)

	# Run every generator, collect all BBQ lines, and group them by question type.
	# Each type (MC, MA, MATCH, ...) becomes its own uniquely-named pair of Ultra
	# packages, so the Ultra banks are grouped by question type rather than by
	# generator title. All lines are also gathered into one combined BBQ for a
	# single Blackboard Classic upload.
	combined_text = ''
	lines_by_type = {}
	for generator in GENERATORS:
		bbq_file = run_generator(generator, repo_root, parts_dir, env)
		text = read_bbq_text(bbq_file)
		combined_text += text
		for line in text.split('\n'):
			if not line.strip():
				continue
			# The BBQ leading tab field is the question-type token.
			type_token = line.split('\t', 1)[0]
			type_name = TYPE_NAMES[type_token]
			lines_by_type.setdefault(type_name, []).append(line)

	# Convert each question type to its own QTI v2.1 + Blackboard pool export pair,
	# in a stable type-name order. The type name is the Ultra bank name.
	for type_name in sorted(lines_by_type):
		type_text = '\n'.join(lines_by_type[type_name]) + '\n'
		per_bbq_path = write_named_bbq(type_text, type_name, output_dir)
		count = len(lines_by_type[type_name])
		print(f"\n=== Converting {count} {type_name} question(s) to QTI v2.1 + Blackboard pool export ===")
		convert_one(per_bbq_path, qti_maker_dir, output_dir, env)

	# Write the combined BBQ and convert it to the complete showcase package: one
	# QTI v2.1 package and one Blackboard pool export ZIP holding every question type
	# (the original showcase goal, alongside the per-type breakdown above).
	combined_bbq_path = write_named_bbq(combined_text, COMBINED_CORE_NAME, output_dir)
	question_lines = [line for line in combined_text.split('\n') if line.strip()]
	print(f"\nWrote {len(question_lines)} combined questions to {combined_bbq_path}")
	print("\n=== Converting COMPLETE showcase to QTI v2.1 + Blackboard pool export ===")
	convert_one(combined_bbq_path, qti_maker_dir, output_dir, env)

	print("\nDONE.")
	print(f"  Combined BBQ (single Blackboard Classic upload): {combined_bbq_path}")
	print(f"  Complete showcase package (all types): {COMBINED_CORE_NAME} QTI v2.1 + bb-export")
	print("  Per-type QTI v2.1 + Blackboard pool export ZIPs (one Ultra bank per")
	print(f"    question type: {', '.join(sorted(lines_by_type))}): see {output_dir}")

#======================================
if __name__ == '__main__':
	main()

## THE END
