"""Shared scenarios, counts, and questions for independent-assortment crosses."""

import os
import re
import sys
import html
import json
import random
import argparse

inheritance_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if inheritance_root not in sys.path:
	sys.path.insert(0, inheritance_root)

import bptools
import genotypelib
import cross_table


#============================================
def validate_scenario(scenario: dict) -> None:
	"""Require two named, colored diploid parents with the same ordered loci."""
	# ASVS 2.2.1 and 2.2.3: validate JSON structure and related parental loci.
	if not isinstance(scenario, dict) or set(scenario) != {'parents'}:
		raise ValueError('Scenario must contain a parents list')
	parents = scenario['parents']
	if not isinstance(parents, list) or len(parents) != 2:
		raise ValueError('Scenario requires exactly two parents')
	loci = []
	names = []
	for parent in parents:
		if not isinstance(parent, dict) or set(parent) != {'name', 'name_color', 'genotype'}:
			raise ValueError('Each parent requires name, name_color (#RRGGBB), and genotype')
		name = parent['name']
		if not isinstance(name, str) or not name.strip():
			raise ValueError('Parent names must be nonempty strings')
		names.append(name)
		# ASVS 2.2.1: accept only a hex color before placing JSON data in inline CSS.
		color = parent['name_color']
		if not isinstance(color, str) or re.fullmatch(r'#[0-9a-fA-F]{6}', color) is None:
			raise ValueError('Parent name_color must be a six-digit hex color, such as #006400')
		genotype = parent['genotype']
		if not isinstance(genotype, list) or not 2 <= len(genotype) <= len(genotypelib.uppercase):
			raise ValueError('Genotype must be a list of 2-20 allele pairs')
		parent_loci = []
		for pair in genotype:
			if not isinstance(pair, str) or len(pair) != 2:
				raise ValueError('Each allele pair must be a two-letter string')
			if pair[0].upper() not in genotypelib.uppercase or pair[0].upper() != pair[1].upper():
				raise ValueError('Each allele pair must describe one supported locus')
			if pair != ''.join(sorted(pair)):
				raise ValueError('Write the dominant allele first in heterozygous pairs')
			parent_loci.append(pair[0].upper())
		if len(set(parent_loci)) != len(parent_loci):
			raise ValueError('Each locus must occur once per parent')
		loci.append(parent_loci)
	if loci[0] != loci[1]:
		raise ValueError('Parents must have the same loci in the same order')
	if names[0] == names[1]:
		raise ValueError('Parents need distinct names')


#============================================
def make_scenario(num_genes: int) -> dict:
	"""Draw a cross useful for all four count questions."""
	if not 2 <= num_genes <= len(genotypelib.uppercase):
		raise ValueError('Number of genes must be between 2 and 20')
	names = [html.unescape(name) for name in cross_table.choose_student_names(2)]
	# Choose colors once with the names so the saved scenario owns their identity.
	colors = bptools.default_color_wheel(num_colors=2)
	# Preserve useful gamete and phenotype counts without forcing the parents to match.
	for _ in range(1024):
		parents = []
		for name, color in zip(names, colors):
			genes = genotypelib.createGenotypeList(num_genes)
			parents.append({
				'name': name,
				'name_color': f'#{color}',
				'genotype': [''.join(pair) for pair in genes],
			})
		scenario = {'parents': parents}
		counts = count_outcomes(scenario)
		if min(counts['gametes']) >= 4 and counts['phenotypes'] >= 4:
			return scenario
	raise RuntimeError('Could not sample a suitable cross; try again')


#============================================
def load_scenario(path: str) -> dict:
	"""Load data only; never regenerate or repair a supplied scenario."""
	with open(path, encoding='utf-8') as handle:
		scenario = json.load(handle)
	validate_scenario(scenario)
	return scenario


#============================================
def save_scenario(path: str, scenario: dict) -> None:
	"""Save a new scenario, protecting an existing exam's parents from overwrite."""
	validate_scenario(scenario)
	with open(path, 'x', encoding='utf-8') as handle:
		json.dump(scenario, handle, indent=2)
		handle.write('\n')


#============================================
def count_outcomes(scenario: dict) -> dict:
	"""Compute all four answers from the same two parental genotypes."""
	first, second = [parent['genotype'] for parent in scenario['parents']]
	gametes = [2 ** sum(pair[0] != pair[1] for pair in genes) for genes in (first, second)]
	counts = {
		'gametes': gametes,
		'genotypes': genotypelib.countGenotypesForCross(first, second),
		'phenotypes': genotypelib.countPhenotypesForCross(first, second),
	}
	return counts


#============================================
def generate_choices(answer: int, num_genes: int, num_choices: int,
		question_type: str, hint: bool) -> tuple[list, str]:
	"""Vary per-locus multiplicities, retaining numeric order and exactly one key."""
	powers = {}
	if question_type == 'gametes':
		# Error: count too many or too few loci as heterozygous.
		for power in range(max(num_genes + 1, num_choices)):
			powers[2 ** power] = (power, 0)
	else:
		# Errors: confuse two versus three outcomes, or treat a fixed locus as variable.
		for power2 in range(num_genes + 1):
			for power3 in range(num_genes - power2 + 1):
				powers[2 ** power2 * 3 ** power3] = (power2, power3)
	if answer not in powers or not 2 <= num_choices <= len(powers):
		raise ValueError('Requested choice count cannot be supplied for this cross')
	wrong = random.sample([value for value in powers if value != answer], num_choices - 1)
	choices = []
	answer_text = ''
	for value in sorted(wrong + [answer]):
		power2, power3 = powers[value]
		text = '1' if value == 1 else genotypelib.format_choice_plus(power2, power3, hint)
		choices.append(text)
		if value == answer:
			answer_text = text
	return choices, answer_text


#============================================
def write_question(N: int, args: argparse.Namespace, scenario: dict | None = None) -> object:
	"""Render one target using fresh parents or an explicitly shared scenario."""
	if scenario is None:
		scenario = make_scenario(args.num_genes)
	validate_scenario(scenario)
	parents = scenario['parents']
	first, second = [parent['genotype'] for parent in parents]
	# ASVS 1.2.1: encode names as text before wrapping them in validated color markup.
	names = []
	for parent in parents:
		name = html.escape(parent['name']).encode('ascii', 'xmlcharrefreplace').decode('ascii')
		names.append(bptools.colorHTMLText(name, parent['name_color'][1:]))
	counts = count_outcomes(scenario)
	kind = args.question_type
	term = cross_table.color_count_term(kind)
	question = '<h3>Independent Assortment in a Hybrid Cross</h3>'
	question += '<p>Assume independent assortment and complete dominance at every gene.</p>'
	if kind == 'gametes':
		index = args.parent - 1
		genes = parents[index]['genotype']
		question += cross_table.work_table_instructions()
		question += cross_table.make_work_table(genes, [names[index]])
		question += f'<p>How many unique <strong>{term}</strong> can {names[index]} produce?</p>'
		if args.hint:
			question += '<p><i>Hint: A heterozygous locus contributes two possible alleles; '
			question += 'a homozygous locus contributes one. Multiply across loci.</i></p>'
		answer = counts['gametes'][index]
	else:
		question += cross_table.work_table_instructions(is_cross=True)
		question += cross_table.make_work_table(first, names, second, last_step=kind)
		question += f'<p>How many unique offspring <strong>{term}</strong> can '
		question += f'the cross between {names[0]} and {names[1]} produce?</p>'
		if args.hint and kind == 'genotypes':
			question += f'<p><i>Hint: Each locus contributes 1, 2, or 3 {term}. '
			question += 'Multiply the per-locus counts.</i></p>'
		if args.hint and kind == 'phenotypes':
			question += f'<p><i>Hint: Aa &times; Aa and Aa &times; aa produce two {term}. '
			question += 'Other crosses produce one. Multiply across loci.</i></p>'
		answer = counts[kind]
	choices, answer_text = generate_choices(answer, len(first), args.num_choices, kind, args.hint)
	item = bptools.formatBB_MC_Question(N, question, choices, answer_text)
	return item


#============================================
def parse_arguments(default_type: str | None = None, default_genes: int = 4) -> argparse.Namespace:
	"""One CLI for creating a scenario or choosing a question about it."""
	parser = bptools.make_arg_parser(description='Count outcomes from independent-assortment crosses.')
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_hint_args(parser)
	parser.add_argument('-n', '--num-genes', '--num_genes', dest='num_genes', type=int,
		default=default_genes, help='Number of genes for a new random scenario')
	question_group = parser.add_mutually_exclusive_group()
	question_group.add_argument('-g', '--gametes', dest='question_type',
		action='store_const', const='gametes', help='Count one parent\'s unique gametes')
	question_group.add_argument('-t', '--genotypes', dest='question_type',
		action='store_const', const='genotypes', help='Count unique offspring genotypes')
	question_group.add_argument('-p', '--phenotypes', dest='question_type',
		action='store_const', const='phenotypes', help='Count unique offspring phenotypes')
	parser.set_defaults(question_type=default_type)
	parser.add_argument('-P', '--parent', dest='parent', type=int, choices=(1, 2), default=None,
		help='Parent whose gametes are counted')
	files = parser.add_mutually_exclusive_group()
	files.add_argument('-y', '--scenario', dest='scenario', help='Read shared parental scenario JSON')
	files.add_argument('-s', '--save-scenario', dest='save_scenario',
		help='Create scenario JSON and exit; refuses to overwrite an existing file')
	args = parser.parse_args()
	if not 2 <= args.num_genes <= len(genotypelib.uppercase):
		parser.error('--num-genes must be between 2 and 20')
	if not 2 <= args.num_choices <= 6:
		parser.error('--num-choices must be between 2 and 6')
	if not args.save_scenario and args.question_type is None:
		parser.error('Choose --gametes, --genotypes, or --phenotypes unless saving a scenario')
	if args.parent is not None and args.question_type != 'gametes':
		parser.error('--parent applies only to --gametes')
	if args.save_scenario and args.question_type is not None and default_type is None:
		parser.error('--save-scenario creates data only; omit the question mode')
	if args.parent is None:
		args.parent = 1
	return args


#============================================
def main(default_type: str | None = None, default_genes: int = 4) -> None:
	"""Create a reusable scenario or emit questions using the common writer."""
	args = parse_arguments(default_type, default_genes)
	if args.save_scenario:
		save_scenario(args.save_scenario, make_scenario(args.num_genes))
		print(f'Saved parental scenario: {args.save_scenario}')
		return
	scenario = load_scenario(args.scenario) if args.scenario else None

	def writer(N: int, writer_args: argparse.Namespace) -> object:
		item = write_question(N, writer_args, scenario)
		return item

	hint_mode = 'with_hint' if args.hint else 'no_hint'
	num_genes = len(scenario['parents'][0]['genotype']) if scenario else args.num_genes
	parts = [args.question_type, hint_mode, f'{num_genes}_genes']
	if args.question_type == 'gametes':
		parts.append(f'parent_{args.parent}')
	outfile = bptools.make_outfile(*parts)
	bptools.collect_and_write_questions(writer, args, outfile)
