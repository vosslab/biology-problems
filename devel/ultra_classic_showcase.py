#!/usr/bin/env python3

"""
Generate a Blackboard Classic vs Blackboard Ultra HTML-sanitization showcase.

Runs twelve biology-problems question generators spanning four question types (MC,
MA, MATCH, FIB). Each is a SHORT item chosen to isolate one HTML-sanitization
failure that Blackboard Classic renders correctly but Blackboard Ultra's sanitizer
strips or flattens. Brevity is deliberate: the audience is IT staff reviewing
failure modes, not students, so each item shows one issue with minimal reading. Two
questions are produced from each generator, then grouped by question type and each
type converted to its own pair of packages with qti-package-maker's bbq_converter
tool: a QTI v2.1 package and a Blackboard pool export ZIP. Grouping by type gives
one Ultra bank per question type. All questions are also gathered into one combined
BBQ file (single Blackboard Classic upload) and one complete showcase package (one
QTI v2.1 + one Blackboard pool export holding every type).

The twelve generators are ordered by sanitization-failure mode (worst first), to
match the companion email's structure for an IT reviewer: content destroyed (color,
script, or layout carries the data), then color-as-convenience, then a clean
control, then the structural type-drop. Type and failure class for each:
   1. deletion_mutant_random               MC    CRITICAL color=data: deletion-map bars vanish
   2. hla_genotype (3 markers)             MC    CRITICAL color=data: marker color marks parental chromosome
   3. pipet_size_mc                         MC    CRITICAL color=data: red digits encode place value
   4. metabolic_pathway_inhibitor          MC    CRITICAL color=identity: nodes recolored figure<->text
   5. which_amino_acid                      MC    CRITICAL script render: RDKit.js <canvas> structure blank
   6. linear_digest (length 8, 2 sites)     MA    CRITICAL spacing=data: ruler tick positions collapse
   7. classify_Haworth                      MA    CRITICAL width=data: ring structure scrambles
   8. monohybrid_genotype_statements        MC    SECONDARY color disambiguates similar AA/Aa/aa tokens
   9. photosynthetic_light_pigments         MC    SECONDARY text color: colored wavelength terms
  10. michaelis_menten_table-Km             MC    SECONDARY zebra readability: alternating row bgcolor
  11. overhang_sequence                     FIB   CONTROL: minimal HTML + monospace probe, renders fine
  12. yaml_match_to_bbq (column_chromatography) MATCH STRUCTURAL type-drop + reinforces colored-term identity

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
	# ---- CRITICAL: content destroyed (color, script, or layout carries the data) ----
	{
		# Color = data. Colored deletion bars across the gene grid are the map the
		# student reads to deduce gene order; Ultra strips the cell color and the
		# map vanishes into empty cells.
		'label': '01_color_data_deletion_map',
		'script': 'problems/inheritance-problems/deletion_mutants/deletion_mutant_random.py',
		'extra_args': ['--num-genes', '6'],
	},
	{
		# Color = data (inline text color). Each parent chromosome's HLA markers are
		# colored to mark which chromosome they came from; a valid offspring genotype
		# is one full maternal chromosome plus one full paternal chromosome. Ultra
		# strips the inline marker color, the markers become bare letters, and no
		# option can be verified -- the answer collapses to a guess. Short pure-text MC.
		'label': '02_color_data_hla_haplotype',
		'script': 'problems/dna_profiling-problems/hla_genotype.py',
		'extra_args': ['--num-markers', '3'],
	},
	{
		# Color = data, plus a small stacked layout. The pipette dial shows red digits
		# to mark decimal place value (the hint says so); Ultra strips the red and the
		# place value is unreadable. Small item that packs several failures into a tiny
		# footprint: inline color carries the number, and the dial spacing reads as a
		# mini layout. Short MC.
		'label': '03_color_data_pipette_digits',
		'script': 'problems/laboratory-problems/pipet_size_mc.py',
		'extra_args': [],
	},
	{
		# Color = identity. A metabolic-pathway figure colors each enzyme/metabolite
		# node, and the same colors recur inline in the prose and options to track
		# identity; Ultra strips the color and the figure<->text link breaks. Short MC.
		'label': '04_color_identity_pathway',
		'script': 'problems/biochemistry-problems/enzymes/metabolic_pathway_inhibitor.py',
		'extra_args': [],
	},
	{
		# Client-side JS render. moleculelib draws the amino-acid structure with
		# RDKit.js into a <canvas> via inline <script>; Ultra strips <script>/<canvas>,
		# so the structure the question asks about disappears entirely. Smaller RDKit
		# item (just the structure + plain-text choices). Scripting probe (confirm by
		# import).
		'label': '05_script_render_amino_acid',
		'script': 'problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/which_amino_acid.py',
		'extra_args': [],
	},
	{
		# Spacing = data. A short restriction-digest ruler positions cut sites by HTML
		# table-cell spacing along a number line; Ultra reflows the spacing and the
		# tick positions (hence fragment sizes) become unreadable. Short MA.
		'label': '06_spacing_data_digest_ruler',
		'script': 'problems/molecular_biology-problems/linear_digest.py',
		'extra_args': ['--length', '8', '--num-sites', '2'],
	},
	{
		# Width + whitespace = data. The Haworth ring is laid out with table
		# borders/spacing; Ultra reflows it and the sugar structure scrambles. MA
		# (select exactly five categorizations).
		'label': '07_width_data_haworth_ring',
		'script': 'problems/biochemistry-problems/carbs/classify_Haworth.py',
		'extra_args': ['--pyran'],
	},
	# ---- SECONDARY: color is a convenience (item still solvable from the text) ----
	{
		# Color-convenience (disambiguation). Genotypes are colored by zygosity so
		# similar-looking AA / Aa / aa tokens are quick to tell apart; Ultra flattens
		# them to black, slowing reading but leaving the item answerable. Short MC.
		'label': '08_color_disambiguate_genotypes',
		'script': 'problems/inheritance-problems/monohybrid_genotype_statements.py',
		'extra_args': [],
	},
	{
		# Color-convenience (terms). Every option is built from colored wavelength
		# terms (orange/green/blue/violet); Ultra strips the color, leaving the text
		# names. Short MC, maximally color-dependent.
		'label': '09_text_color_pigment_wavelengths',
		'script': 'problems/biochemistry-problems/photosynthetic_light_pigments.py',
		'extra_args': [],
	},
	{
		# Color-convenience (readability). A Michaelis-Menten [S]/V0 table uses
		# alternating-row background color (zebra striping) for scanning; Ultra strips
		# the striping, leaving the data intact but harder to read. Short MC.
		'label': '10_readability_zebra_michaelis',
		'script': 'problems/biochemistry-problems/enzymes/michaelis_menten_table-Km.py',
		'extra_args': [],
	},
	# ---- CONTROL: minimal HTML, expected to render correctly in both platforms ----
	{
		# Control. Plain Fill-in-the-Blank restriction-enzyme overhang sequence; uses
		# font-family:monospace, so it doubles as the monospace-alignment probe
		# (confirm by import). Matches the real sample Ch02.4 Overhang_Sequence_FiB.
		'label': '11_control_clean_fib_overhang',
		'script': 'problems/molecular_biology-problems/overhang_sequence.py',
		'extra_args': ['--fib'],
	},
	# ---- STRUCTURAL: not an HTML failure -- Ultra's QTI import drops the type ----
	{
		# Structural type-drop AND a color reinforce, in one item. Blackboard's QTI
		# v2.1 package import supports only Multiple Choice, Fill-in-the-Blank, Essay,
		# and True/False, so Matching (MAT) is dropped on import -- the whole question
		# vanishes. This set also colors each column-type name (IEX, AC, HIC, SEC) and
		# the recurring key terms, and those colors link the colored prompt to its
		# colored description (the same color=identity mechanism as item 03). Where the
		# pool export does carry it into Ultra, the stripped inline color reinforces the
		# color-identity failure. Double duty: type-drop plus colored-term identity.
		'label': '12_typedrop_color_matching',
		'script': 'problems/matching_sets/yaml_match_to_bbq.py',
		'input_file': 'problems/matching_sets/laboratory/column_chromatography.yml',
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
