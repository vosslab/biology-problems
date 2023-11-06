#!/usr/bin/env python3

import os
import random
import argparse

import bptools
import genemapclass as gmc

debug = False

#====================================
def get_question_text():
	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>With the progeny data from the table, '
	question_string += '<strong>calculate the genetic distance between the two genes,</strong> '
	question_string += 'expressing your answer in centimorgans (cM)</p> '
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
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	lowercase = "abcdefghijklmnpqrsuvwxyz"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	j = -1
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
		distance = list(GMC.distances_dict.values())[0]

		question_string = get_question_text()
		full_question = header+phenotype_info_text+html_table+question_string
		final_question = bptools.formatBB_NUM_Question(N, full_question, distance, 0.1, tol_message=False)

		f.write(final_question)
	f.close()







#THE END
