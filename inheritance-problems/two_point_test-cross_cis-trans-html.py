#!/usr/bin/env python3

import os
import copy
import random
import argparse

import bptools
import pointtestcrosslib as ptcl

debug = False

#====================================
def questionText(basetype, type='parental'):
	question_string = '<h6>Two-Point Test-Cross Gene Mapping</h6>'
	question_string += '<p>A test-cross with a heterozygote fruit fly for two genes is conducted. '
	question_string += 'The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<p>Using the table above, determine whether the parental chromosomes are cis or trans</p>'
	return question_string

#====================================
def makeQuestion(basetype, distance, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s"
		%(basetype[0], distance, basetype[1]))
	print(answerString)
	if debug is True: print("------------")

	if debug is True: print("determine parental type")
	types = ['++', '+'+basetype[1], basetype[0]+'+', basetype[0]+basetype[1]]
	if debug is True: print("types=", types)
	parental = random.choice(types)
	both_parental_types = (parental, ptcl.invert_genotype(parental, basetype))
	recombinant_types = copy.copy(types)
	recombinant_types.remove(parental)
	recombinant_types.remove(ptcl.invert_genotype(parental, basetype))

	type_categories = {
		'parental':    (parental,   ptcl.invert_genotype(parental, basetype)),
		'recombinant': recombinant_types,
	}
	print('type_categories=',type_categories)

	if debug is True: print("parental=", both_parental_types)
	type_counts = ptcl.generate_type_counts(parental, basetype, progeny_size, distance, geneorder)
	if debug is True: print("type_counts=", type_counts)
	return type_counts, type_categories

#====================================
#====================================
if __name__ == "__main__":
	#parser = argparse.ArgumentParser()
	#parser.add_argument('-t', '--type', type=str, dest='question_type',
	#	help='type of question to ask, (parental, recombinant)', default=5)
	#args = parser.parse_args()

	#used for gene letters
	lowercase = "abcdefghijklmnpqrsuvwxyz"

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 49
	j = -1
	N = 0
	for i in range(duplicates):
		N += 1
		j += 1
		if j + 1 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+2]
		geneorder = basetype
		distance = ptcl.get_distance()
		print(basetype, distance)
		progeny_size = ptcl.get_progeny_size(distance)
		typemap, type_categories = makeQuestion(basetype, distance, progeny_size)
		choices_list = ['cis', 'trans']
		extra_choices = ['ortho', 'para', 'meta', 'anti', 'syn', 'cyclo', 'iso', 'tert', 'endo', 'exo']
		#choices_list.sort()
		random.shuffle(extra_choices)
		choices_list += extra_choices[:3]
		random.shuffle(choices_list)

		if '++' in type_categories['parental']:
			answer = 'cis'
		else:
			answer = 'trans'

		ascii_table = ptcl.make_progeny_ascii_table(typemap, progeny_size)
		print(ascii_table)
		html_table = ptcl.make_progeny_html_table(typemap, progeny_size)

		question_string = questionText(basetype)
		question = html_table+question_string
		final_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
		#final_question = blackboardFormat(N, question_string, html_table, distance)
		#print(final_question)

		f.write(final_question)
	f.close()
	bptools.print_histogram()






#THE END
