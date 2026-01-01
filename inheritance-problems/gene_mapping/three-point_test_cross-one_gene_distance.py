#!/usr/bin/env python3

import os
import sys
import random
import argparse

import bptools
import genemapclass as gmc

debug = False

#=====================
#=====================
def get_question_text(question_type='parental', gene_pair=None):
	gene_pair_text =   f'genes <b>{gene_pair[0].upper()}</b> and <b>{gene_pair[1].upper()}</b>'

	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>With the progeny data from the table, '
	question_string += 'and using only the genotypes that result from crossover events '
	question_string += f'between the two {gene_pair_text} during meiosis.</p> '
	question_string += f'<p><strong>calculate the genetic distance between the two {gene_pair_text},</strong> '
	question_string += 'expressing your answer in centimorgans (cM)</p> '
	if question_type == 'num':
		question_string += get_important_tips()
	return question_string


#===========================================================
#===========================================================
def get_important_tips():
	"""
	Returns the HTML formatted hints for solving the problem.

	Returns:
		str: HTML formatted string with hints.
	"""
	tips = '<h6>Important Answer Guidelines</h6>'
	tips += '<p><ul>'
	tips += '<li><i>Important Tip 1:</i> '
	tips += '  Your calculated distance between the pair of genes should be a whole number. '
	tips += '  Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
	tips += '  Please provide your answer as a complete number without fractions or decimals.</li>'
	tips += '<li><i>Important Tip 2:</i> '
	tips += '  Your answer should be written as a numerical value only, '
	tips += '  with no spaces, commas, or units such as "cM" or "map units". '
	tips += '  For example, if the distance is fifty one centimorgans, simply write "51".</li>'
	tips += '</ul></p>'
	return tips

#=====================
def parse_arguments():
	"""Parses command-line arguments for the script."""
	parser = argparse.ArgumentParser(description="Generate Neurospora genetics questions.")
	question_group = parser.add_mutually_exclusive_group(required=True)

	# Add question type argument with choices
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('num', 'mc'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)
	question_group.add_argument(
		'-n', '--num', dest='question_type', action='store_const', const='num',
		help='Set question type to numeric'
	)

	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do', default=1
	)

	args = parser.parse_args()

	return args

#=====================
#=====================
def main():
	args = parse_arguments()

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ f'-{args.question_type.upper()}'
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicates):
		N += 1
		# Gene Mapping Class
		GMC = gmc.GeneMappingClass(3, N)
		GMC.debug = True
		GMC.question_type = args.question_type
		GMC.setup_question()
		print(GMC.get_progeny_ascii_table())
		header = GMC.get_question_header()
		html_table = GMC.get_progeny_html_table()
		phenotype_info_text = GMC.get_phenotype_info()

		genes_list = list(GMC.gene_order_str)
		gene_indices = random.sample(list(range(1,4)), 2)
		gene_index_tuple = tuple(sorted(gene_indices))
		gene_pair = (genes_list[gene_index_tuple[0]-1], genes_list[gene_index_tuple[1]-1])

		answer_distance = GMC.distances_dict[gene_index_tuple]
		print(gene_pair, gene_index_tuple)

		assert gene_pair == (
			GMC.gene_order_str[gene_index_tuple[0]-1],
			GMC.gene_order_str[gene_index_tuple[1]-1]
		), "gene_pair does not match gene_order_str at gene_index_tuple"

		question_string = get_question_text(args.question_type, gene_pair)
		full_question = header + phenotype_info_text + html_table + question_string
		GMC.is_valid_html(full_question)
		if args.question_type == 'num':
			final_question = bptools.formatBB_NUM_Question(N, full_question, answer_distance, 0.1, tol_message=False)
		elif args.question_type == 'mc':
			choices_list, answer_text = GMC.make_choices(gene_pair)
			final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)

		f.write(final_question)
	f.close()
	bptools.print_histogram()

#===========================================================
#===========================================================
if __name__ == "__main__":
	main()
#THE END
