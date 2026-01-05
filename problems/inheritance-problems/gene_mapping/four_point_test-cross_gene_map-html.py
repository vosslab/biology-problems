#!/usr/bin/env python3

import os
import re
import sys
import copy
import numpy
import random

import bptools
import genemaplib as ptcl

debug = True

def get_possible_y_values():
	# Initialize an empty list to store possible y values
	possible_y_values = []

	# Loop through possible x values
	for x in range(7, 41):  # x is from 15 to 35
		# Loop through possible y values (positive integers greater than zero)
		for y in range(2, x):  # I'm limiting y up to 1000 for the example
			# Check if xy/50 is an integer
			if (x * y) % 50 == 0:
				# Calculate z
				z = x + y + (x * y) // 50  # using // for integer division

				# Check if z > x and z < 46
				if z <= 47:
					# Append to possible_y_values if all conditions are met
					possible_y_values.append((x, y, z))

	# Print out the possible (x, y) pairs
	possible_y_values.sort()
	print(f'found {len(possible_y_values)} solutions!!')
	print(f'possible_y_values={possible_y_values}')
	return possible_y_values

def getDistances():
	possible_solutions = [
		(10, 5, 16), (15, 10, 28),
		(20, 5, 27), (20, 10, 34),
		(20, 15, 41), (25, 2, 28),
		(25, 4, 31), (25, 6, 34),
		(25, 8, 37), (25, 10, 40),
		(25, 12, 43), (25, 14, 46),
		(30, 5, 38), (30, 10, 46)
	]
	solution = random.choice(possible_solutions)
	if debug is True: print(f"distances={solution}")
	return list(solution)

def getDistancesOriginal():
	if debug is True: print("determine gene distances")
	a = numpy.random.poisson(lam=12, size=7)
	a.sort()
	distances = [a[0], a[-1]]
	random.shuffle(distances)
	distance3 = distances[0] + distances[1] - (distances[0] * distances[1])/50.
	distances.append(distance3)
	if debug is True: print(distances)
	return distances

def generateProgenyData(types, type_counts, basetype):
	if debug is True: print("\n\ngenerate progeny data")
	typemap = {}
	for t in types:
		n = ptcl.invert_genotype(t, basetype)
		#rand = random.gauss(0.5, 0.01)
		try:
			count = type_counts[t]
		except KeyError:
			count = type_counts[n]
		tcount = 0
		ncount = 0
		for i in range(count):
			if random.random() > 0.5:
				tcount += 1
			else:
				ncount += 1
		sys.stderr.write(".")
		#typemap[t] = int(rand * count)
		#typemap[n] = count - typemap[t]
		typemap[t] = tcount
		typemap[n] = ncount
	sys.stderr.write("\n")
	return typemap

def generateTypeCounts(parental, doublecross, basetype):
	type_counts = {}
	if debug is True: print("determine double type")
	doubletype = ptcl.flip_gene_by_letter(parental, geneorder[1], basetype)
	doublecount = int(round(doublecross*progeny_size/100.))
	if debug is True: print("  ", doubletype, ptcl.invert_genotype(doubletype, basetype), doublecount)
	type_counts[doubletype] = doublecount

	if debug is True: print("determine first flip")
	firsttype = ptcl.flip_gene_by_letter(parental, geneorder[0], basetype)
	firstcount = int(round(distances[0]*progeny_size/100.)) - doublecount
	if debug is True: print("  ", firsttype, ptcl.invert_genotype(firsttype, basetype), firstcount)
	type_counts[firsttype] = firstcount

	if debug is True: print("determine second flip")
	secondtype = ptcl.flip_gene_by_letter(parental, geneorder[2], basetype)
	secondcount = int(round(distances[1]*progeny_size/100.)) - doublecount
	if debug is True: print("  ", secondtype, ptcl.invert_genotype(secondtype, basetype), secondcount)
	type_counts[secondtype] = secondcount

	if debug is True: print("determine parental type count")
	parentcount = progeny_size - doublecount - firstcount - secondcount
	if debug is True: print("  ", parental, ptcl.invert_genotype(parental, basetype), parentcount)
	type_counts[parental] = parentcount

	return type_counts

def makeQuestion(basetype, geneorder, distances, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s - %d - %s"
		%(geneorder[0], distances[0], geneorder[1], distances[1], geneorder[2]))
	print(answerString)
	if debug is True: print("------------")

	if debug is True: print("determine double crossovers")
	doublecross = distances[0]*distances[1]/100.
	if debug is True: print("doublecross", doublecross*10, 'per 1000')

	if debug is True: print("determine parental type")
	types = ['+++', '++'+basetype[2], '+'+basetype[1]+'+', '+'+basetype[1]+basetype[2]]
	parental = random.choice(types)
	if debug is True: print("  ", parental, ptcl.invert_genotype(parental, basetype))
	type_counts = generateTypeCounts(parental, doublecross, basetype)
	typemap = generateProgenyData(types, type_counts, basetype)
	return typemap

def questionText(basetype):
	question_string = '<h6>Three-Point Test-Cross: Gene Mapping</h6>'
	question_string += '<p>A test-cross with a heterozygote fruit fly for three genes is conducted. '
	question_string += 'The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<p>Using the table above, determine the order of the genes and the distances between them. '
	question_string += 'Once calculated, fill in the following four blanks: </p><p> <ul>'
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[1].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[2].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[1].upper(),basetype[2].upper())
	question_string += '<li>From this the correct order of the genes is [geneorder] (gene order).</li></ul></p>'
	question_string += '<p><i>Hint 1:</i> ALL gene distances will be whole numbers, '
	question_string += 'do NOT enter a decimal; if you have a decimal your calculations are wrong.</p>'
	question_string += '<p><i>Hint 2:</i> enter your answer in the blank using only letters or numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</p>'
	return question_string

def getVariables(basetype):
	variable_list = []
	if basetype[0] < basetype[1]:
		variable = '{0}{1}'.format(basetype[0].upper(),basetype[1].upper())
	else:
		variable = '{0}{1}'.format(basetype[1].upper(),basetype[0].upper())
	variable_list.append(variable)
	if basetype[1] < basetype[2]:
		variable = '{0}{1}'.format(basetype[1].upper(),basetype[2].upper())
	else:
		variable = '{0}{1}'.format(basetype[2].upper(),basetype[1].upper())
	variable_list.append(variable)
	if basetype[0] < basetype[2]:
		variable = '{0}{1}'.format(basetype[0].upper(),basetype[2].upper())
	else:
		variable = '{0}{1}'.format(basetype[2].upper(),basetype[0].upper())
	variable_list.append(variable)
	variable = 'geneorder'
	variable_list.append(variable)
	return variable_list

#=====================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub(r"<table.+</table>", '[]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub(r"</p>\s*<p>", '\n', pretty_question)
	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_FIB_PLUS_Question(N, question, variable_list, geneorder, distances):
	crc16 = bptools.getCrc16_FromString(question)

	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	bb_question = f'FIB_PLUS\t<p>{crc16}</p> {question}'
	pretty_question = makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	variable_to_distance = {}
	for i in range(len(variable_list)-1):
		variable_to_distance[variable_list[i]] = distances[i]
	variable_list.sort()
	for i in range(len(variable_list)-1):
		variable = variable_list[i]
		bb_question += '\t{0}\t{1}\t'.format(variable, variable_to_distance[variable])
	bb_question += '\tgeneorder\t{0}\t{1}'.format(geneorder, geneorder[::-1])
	bb_question += '\n'
	return bb_question

#=====================
#=====================
if __name__ == "__main__":
	lowercase = "abcdefghijklmnpqrsuvwxyz"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 1
	j = -1
	N = 0
	for i in range(duplicates):
		N += 1
		j += 1
		if j + 2 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+4]
		geneorder = ptcl.get_random_gene_order(basetype)
		distances = getDistances()
		progeny_size = ptcl.get_general_progeny_size(distances)
		typemap = makeQuestion(basetype, geneorder, distances, progeny_size)
		ascii_table = ptcl.make_progeny_ascii_table(typemap, progeny_size)
		ptcl.gene_map_solver(typemap, progeny_size)
		print(ascii_table)
		html_table = ptcl.make_progeny_html_table(typemap, progeny_size)
		#print(html_table)
		question_string = questionText(basetype)
		variable_list = getVariables(geneorder)
		complete_question = html_table + question_string
		final_question = formatBB_FIB_PLUS_Question(N, complete_question, variable_list, geneorder, distances)
		#print(final_question)
		f.write(final_question)
	f.close()
#THE END
