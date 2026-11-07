#!/usr/bin/env python3

import itertools
import math

import bptools
import gene_map_class_lib as gmc
import gene_map_solver_lib as solver


def get_answer_mapping(mapping):
	"""Use gene letters, independently of their positions on the chromosome."""
	order = mapping.gene_order_str
	answer_map = {'geneorder': list(dict.fromkeys(
		[order, order[::-1], order.upper(), order[::-1].upper()]))}
	for (i, j), value in mapping.distances_dict.items():
		pair = ''.join(sorted((order[i-1], order[j-1]))).upper()
		answers = [f'{value:.1f}']
		if value.is_integer():
			answers.append(str(int(value)))
		answer_map[pair] = answers
	return answer_map


def get_question_text(letters):
	text = '<h6>Question</h6><p>Using the two tables above, determine all six pairwise '
	text += 'recombination-based distances (cM) and the gene order.</p><ul>'
	for a, b in itertools.combinations(letters.upper(), 2):
		text += f'<li>Distance between {a} and {b}: [{a}{b}] cM</li>'
	text += '<li>Gene order: [geneorder]</li></ul>'
	text += '<p>Enter each distance to one decimal place, without units '
	text += '(for example, 12.0 or 26.2). Enter the gene order as four letters '
	text += 'without spaces or hyphens; either direction is accepted.</p>'
	return text


def write_question(N, args):
	mapping = gmc.GeneMappingClass(4, N)
	mapping.setup_question()
	# Recover the key from observed offspring, without the hidden phase or order.
	_, _, order = solver.gene_map_solver(mapping.genotype_counts)
	if order not in (mapping.gene_order_str, mapping.gene_order_str[::-1]):
		raise ValueError('Generated gene order disagrees with offspring counts')
	for (i, j), expected in mapping.distances_dict.items():
		pair = (mapping.gene_order_str[i-1], mapping.gene_order_str[j-1])
		observed = solver.get_gene_distance(pair, mapping.parental_genotypes_tuple,
			mapping.genotype_counts, mapping.gene_letters_str, mapping.progeny_count_int)
		if not math.isclose(observed, expected, abs_tol=1e-9):
			raise ValueError('Generated distance disagrees with offspring counts')
	question = mapping.get_question_header() + mapping.get_phenotype_info()
	question += mapping.get_progeny_html_table() + get_question_text(mapping.gene_letters_str)
	return bptools.formatBB_FIB_PLUS_Question(N, question, get_answer_mapping(mapping))


def parse_arguments():
	parser = bptools.make_arg_parser(description='Generate four-gene test-cross bonus questions.')
	parser.set_defaults(duplicates=1)
	return parser.parse_args()


def main():
	args = parse_arguments()
	bptools.collect_and_write_questions(write_question, args, bptools.make_outfile(),
		print_histogram_flag=False)


if __name__ == '__main__':
	main()
