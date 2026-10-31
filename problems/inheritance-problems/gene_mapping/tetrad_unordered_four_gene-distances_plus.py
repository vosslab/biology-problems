#!/usr/bin/env python3
"""Four-gene bonus questions using 16 unordered tetrad patterns."""

import itertools
import math
import random

import bptools
import genemaplib as gml
import gene_map_solver_lib as solver
import phenotypes_for_yeast
import tetradlib
import tetrad_solver_lib as tusl

bptools.allow_no_click_div = False
PAIR_POSITIONS = ((0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3))


def construct_tetrads(letters, order, parent, counts):
	"""Convert a fly pool vector to 16 teaching patterns with the same distances."""
	genotypes = {}
	for mask in gml.FOUR_GENE_MASKS:
		genotype = parent
		for boundary, bit in enumerate(mask, 1):
			if bit == '1':
				genotype = gml.crossover_after_index(genotype, boundary, order)
		genotypes[mask] = genotype
	ditype_counts = dict(zip(gml.FOUR_GENE_MASKS, counts))
	# Baseline total is 6*N; TT + 6*NPD is 12 times each fly recombinant count.
	ditype_counts['000'] = 7 * counts[0] - sum(counts) - 2
	# Adding the eighth tetratype preserves both the total and all six numerators.
	ditype_counts['100'] -= 3
	ditype_counts['010'] -= 3
	ditype_counts['110'] += 2
	rows = {tetradlib.make_ditype_from_genotype_str(genotypes[mask], letters): count
		for mask, count in ditype_counts.items()}
	for mask, count in zip(gml.FOUR_GENE_MASKS[1:], counts[1:]):
		tetrad = tetradlib.make_tetratype_from_genotype_strings(parent, genotypes[mask], letters)
		rows[tetrad] = 6 * count
	tetrad = tetradlib.make_tetratype_from_genotype_strings(
		genotypes['100'], genotypes['010'], letters)
	rows[tetrad] = 6
	return rows


def get_answer_mapping(rows, letters):
	"""Recover answers from the displayed counts, independently of phase and order."""
	distances = {}
	answers = {}
	for i, j in itertools.combinations(range(4), 2):
		tt, npd, _, _ = tusl.get_pair_tetrad_counts(rows, (i, j))
		value = tusl.calculate_distance_from_counts(tt, npd, sum(rows.values()))
		pair = (letters[i], letters[j])
		distances[pair] = value
		answers[''.join(pair).upper()] = [f'{value:.1f}']
		if float(value).is_integer():
			answers[''.join(pair).upper()].append(str(int(value)))
	order = solver.get_gene_order(distances)
	answers['geneorder'] = [order, order[::-1]]
	return answers


def get_question_text(letters):
	text = '<h6>Question</h6><p>Determine all six pairwise distances and the gene order: '
	pairs = [f'{a}{b} = [{a}{b}] cM' for a, b in itertools.combinations(letters.upper(), 2)]
	text += ', '.join(pairs) + '; gene order: [geneorder].</p>'
	text += '<p>For each gene pair, classify the tetrads as PD, NPD, or TT. '
	text += 'Calculate distance (cM) = 100 &times; (TT/2 + 3 NPD) / total tetrads.</p>'
	text += '<p>Enter distances to one decimal place without units (for example, 12.0 or 26.2). '
	text += 'Enter the gene order as four letters without spaces or hyphens; '
	text += 'either direction is accepted.</p>'
	return text


def write_question(N, args):
	letters = gml.get_gene_letters(4)
	order = gml.get_random_gene_order(letters)
	parent = random.choice(gml.generate_genotypes(letters))
	pool = gml.get_four_gene_distance_pool()
	key = random.choice(tuple(pool))
	rows = construct_tetrads(letters, order, parent, random.choice(pool[key]))
	# Reduce to integral counts before varying sample size without changing distances.
	divisor = math.gcd(*rows.values())
	base = sum(rows.values()) // divisor
	scale = random.randint(1, 100000 // base)
	rows = {tetrad: count // divisor * scale for tetrad, count in rows.items()}
	answers = get_answer_mapping(rows, letters)
	for (i, j), expected in zip(PAIR_POSITIONS, key):
		pair = ''.join(sorted((order[i], order[j]))).upper()
		if answers[pair][0] != f'{expected / 10:.1f}':
			raise ValueError('Generated distance disagrees with tetrad counts')
	if order not in answers['geneorder']:
		raise ValueError('Generated gene order disagrees with tetrad counts')
	_, colors = bptools.light_and_dark_color_wheel(4)
	text = '<h5>Unordered Tetrad Four Gene Mapping: Bonus</h5>'
	text += '<p>A cross in the yeast <i>Saccharomyces cerevisiae</i> produces the '
	text += '16 unordered tetrad patterns below. Use their counts to map four linked genes.</p>'
	text += gml.get_phenotype_info(letters, phenotypes_for_yeast.phenotype_dict, colors)
	text += tetradlib.make_progeny_html_table(rows, sum(rows.values()), colors)
	text += get_question_text(letters)
	return bptools.formatBB_FIB_PLUS_Question(N, text, answers)


def main():
	parser = bptools.make_arg_parser(description='Generate four-gene unordered tetrad bonus questions.')
	parser.set_defaults(duplicates=1)
	args = parser.parse_args()
	bptools.collect_and_write_questions(write_question, args, bptools.make_outfile(),
		print_histogram_flag=False)


if __name__ == '__main__':
	main()
