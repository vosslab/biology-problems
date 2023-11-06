#!/usr/bin/env python3

import os
import copy
import random
import argparse

import bptools
import genemapclass as gmc

debug = False

#====================================
def questionText():
	question_string = ''
	question_string += '<p>The phenotype counts resulting from the cross are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>Using the data presented in the table to determine the configuration '
	question_string += 'of the alleles on the parental chromosomes. '
	question_string += 'Determine whether the alleles for the two genes are in a '
	question_string += '<strong><i>cis</i></strong> (on the same chromosome) or '
	question_string += '<strong><i>trans</i></strong> (on different chromosomes) configuration. '

	return question_string

#====================================
#====================================
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
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

		choices_list = ['cis', 'trans']
		#old_choices = ['ortho', 'para', 'meta', 'anti', 'syn', 'cyclo', 'iso', 'tert', 'endo', 'exo']
		extra_choices = ['both', 'neither', 'cannot be determined']
		choices_list += extra_choices[:3]
		if '++' in GMC.parental_genotypes_tuple:
			answer = 'cis'
		else:
			answer = 'trans'

		question_string = questionText()
		full_question = header+phenotype_info_text+html_table+question_string
		final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer)

		f.write(final_question)
	f.close()
	bptools.print_histogram()

#THE END
