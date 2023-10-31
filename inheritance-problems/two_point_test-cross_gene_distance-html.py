#!/usr/bin/env python3

import os
import random

import bptools
import pointtestcrosslib as ptcl

debug = False

#====================================
def questionText(basetype):
	question_string = '<h6>Two-Point Test-Cross: Gene Distance Mapping</h6>'
	question_string += '<p>A test-cross with a heterozygote fruit fly for two genes is conducted. '
	question_string += 'The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<p>Using the table above, determine the distance between the two genes.</p> '
	question_string += '<ul> <li><i>Hint 1:</i> The gene distance will be a whole number, '
	question_string += 'do NOT enter a decimal; if you have a decimal your calculations are likely wrong.</li>'
	question_string += '<li><i>Hint 2:</i> enter your answer in the blank using only numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</li></ul> '
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
	if debug is True: print("parental=", parental, ptcl.invert_genotype(parental, basetype))
	type_counts = ptcl.generate_type_counts(parental, basetype, progeny_size, distance, geneorder)
	if debug is True: print("type_counts=", type_counts)
	return type_counts

#====================================
#====================================
if __name__ == "__main__":
	lowercase = "abcdefghijklmnpqrsuvwxyz"

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 197
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
		typemap = makeQuestion(basetype, distance, progeny_size)
		ascii_table =  ptcl.make_progeny_ascii_table(typemap, progeny_size)
		print(ascii_table)
		html_table = ptcl.make_progeny_html_table(typemap, progeny_size)
		#print(html_table)
		question_string = questionText(basetype)
		#variable_list = getVariables(geneorder)
		final_question = bptools.formatBB_NUM_Question(N, html_table+question_string, distance, 0.1)
		#final_question = blackboardFormat(N, question_string, html_table, distance)
		#print(final_question)

		f.write(final_question)
	f.close()







#THE END
