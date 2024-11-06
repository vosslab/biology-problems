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
		question_string += '<ul> '
		question_string += '<li><i>Important Tip 1:</i> '
		question_string +=   'Your calculated distance between the genes should be a whole number. '
		question_string +=   'Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
		question_string +=   'Please provide your answer as a complete number without fractions or decimals.</li>'
		question_string += '<li><i>Important Tip 2:</i> '
		question_string +=   'Your answer should be written as a numerical value only, '
		question_string +=   'no spaces, commas, or units such as "cM" or "map units". '
		question_string +=   'For example, if the distance is fifty one centimorgans, simply write "51". </li> '
		question_string += '</ul> '
	return question_string

#=====================
#=====================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	question_group = parser.add_mutually_exclusive_group(required=True)
	# Add question type argument with choices
	question_group.add_argument('-t', '--type', dest='question_type', type=str,
		choices=('num', 'mc'), help='Set the question type: accept or reject')
	question_group.add_argument('-m', '--mc', dest='question_type', action='store_const',
		const='mc',)
	question_group.add_argument('-n', '--num', dest='question_type', action='store_const',
		const='num',)
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

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

		genes_list = list(GMC.gene_letters_str)
		gene_indices = list(range(1,4))
		random.shuffle(gene_indices)
		gene1_index = gene_indices.pop()
		gene2_index = gene_indices.pop()
		gene_index_tuple = tuple(sorted([gene1_index, gene2_index]))
		gene_pair = (genes_list[gene_index_tuple[0]-1], genes_list[gene_index_tuple[1]-1])

		answer_distance = GMC.distances_dict[gene_index_tuple]

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

#THE END
