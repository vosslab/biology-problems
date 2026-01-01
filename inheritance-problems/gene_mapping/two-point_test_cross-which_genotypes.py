#!/usr/bin/env python3

import os
import sys
import copy
import random
import argparse

import bptools
import genemapclass as gmc

debug = False

#====================================
#====================================
def get_question_text(question_type='parental'):
	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>Review the phenotype counts shown in the table. '
	question_string += 'Based on the traits expressed in the offspring, identify the possible '
	question_string += f'<strong>{question_type} genotype combinations</strong>. '
	if question_type == 'parental':
		question_string += 'These are the allele combinations that the parent fruit flies originally carried. '
	else:  # Assuming the alternative is 'recombinant'
		question_string += 'These allele combinations have occurred due to genetic crossover. '
	question_string += 'More than one combination will be correct. '
	question_string += 'Select all that apply.</p> '
	return question_string

#====================================
#====================================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# Create a mutually exclusive group for question types
	question_group = parser.add_mutually_exclusive_group(required=True)
	# Add question type argument with choices
	question_group.add_argument('-t', '--type', dest='question_type', type=str,
		choices=('parental', 'recombinant'), help='Set the question type: accept or reject')
	question_group.add_argument('-p', '--parental', dest='question_type', action='store_const',
		const='parental',)
	question_group.add_argument('-r', '--recombinant', dest='question_type', action='store_const',
		const='recombinant',)
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
		GMC = gmc.GeneMappingClass(2, N)
		GMC.setup_question()
		print(GMC.get_progeny_ascii_table())
		header = GMC.get_question_header()
		html_table = GMC.get_progeny_html_table()
		phenotype_info_text = GMC.get_phenotype_info()

		choices_list = sorted(GMC.genotype_counts.keys(), reverse=True)
		if args.question_type == 'parental':
			answers_list = list(GMC.parental_genotypes_tuple)
		elif args.question_type == 'recombinant':
			answers_list = [item for item in choices_list if item not in GMC.parental_genotypes_tuple]
		else:
			print('unknown question type', args.question_type)
			sys.exit(1)

		question_string = get_question_text(args.question_type)
		full_question = header + phenotype_info_text + html_table + question_string
		final_question = bptools.formatBB_MA_Question(N, full_question, choices_list, answers_list)

		f.write(final_question)
	f.close()
	bptools.print_histogram()

#THE END
