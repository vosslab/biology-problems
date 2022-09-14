#!/usr/bin/env python3

import os
import re
import sys
import copy
import math
import numpy
import string
import random
import crcmod.predefined

debug = True

def tetradSetToString(tetradSet):
	mystr = ("%s\t%s\t%s\t%s\t"
		%(tetradSet[0],tetradSet[1],tetradSet[2],tetradSet[3],))
	return mystr

#====================================
def invertType(genotype, basetype):
	newtype = ''
	for i in range(2):
		if genotype[i] == '+':
			newtype += basetype[i]
		else:
			newtype += '+'
	return newtype

#====================================
def flipGene(genotype, gene, basetype):
	newlist = list(genotype)
	for i in range(2):
		if basetype[i] == gene:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'
	newtype = ""
	for i in newlist:
		newtype += i
	return newtype

#====================================
def getDistance():
	#integers
	return random.randint(2,45)

#====================================
def getProgenySize(distance):
	if debug is True: print("determine progeny size")
	gcdfinal = math.gcd(distance, 100)
	if debug is True: print("Final GCD", gcdfinal)
	progenybase = 100/gcdfinal
	minprogeny =  900/progenybase
	maxprogeny = 6000/progenybase
	progs = numpy.arange(minprogeny, maxprogeny+1, 1, dtype=numpy.float64)*progenybase
	#print(progs)
	numpy.random.shuffle(progs)
	#print(progs)
	bases = progs * distance * distance / 1e4
	#print(bases)
	devs = (bases - numpy.around(bases, 0))**2
	#print(devs)
	argmin = numpy.argmin(devs)
	progeny_size = int(progs[argmin])
	if debug is True: print(("total progeny: %d\n"%(progeny_size)))
	return progeny_size

#====================================
def lcm(a, b):
	return abs(a*b) // math.gcd(a, b)

#====================================
def lcm4(a, b, c, d):
	gcd1 = math.gcd(a, b)
	gcd2 = math.gcd(c, d)
	gcdfinal = math.gcd(gcd1, gcd2)
	return abs(a*b*c*d) // gcdfinal

#====================================
def makeProgenyHtmlTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'
	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 400px; height: 220px;">'
	table += '<tr>'
	table += '  <th {0}>Set #</th>'.format(td_extra)
	table += '  <th colspan="4" {0}>Tetrad Genotypes</th>'.format(td_extra)
	table += '  <th {0}>Progeny<br/>Count</th>'.format(td_extra)
	table += '</tr>'
	for i,type in enumerate(alltypes):
		interheader = '</span></td><td {0}>{1}'.format(td_extra, span)
		html_type = type.strip().replace('\t', interheader)
		table += '<tr>'
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, i+1)
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, html_type)
		table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, typemap[type])
		table += '</tr>'
	table += '<tr>'
	table += '  <th colspan="5" {0}">TOTAL =</th>'.format(td_extra.replace('center', 'right'))
	table += '  <td {0}>{1:d}</td>'.format(td_extra.replace('center', 'right'), progeny_size)
	table += '</tr>'
	table += '</table>'
	return table

#====================================
def makeProgenyAsciiTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	table = ''
	for type in alltypes:
		table += ("{0}\t".format(type))
		table += ("{0:d}\t".format(typemap[type]))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table

#====================================
def makeQuestion(basetype, distance, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s"
		%(basetype[0], distance, basetype[1]))
	print(answerString)
	if debug is True: print("------------")

	types = ['++', '+'+basetype[1], basetype[0]+'+', basetype[0]+basetype[1]]
	if debug is True: print("types=", types)

	if debug is True: print("determine parental type")
	parental = random.choice(types)
	if debug is True: print("parental=", parental, invertType(parental, basetype))

	tetradCount = generateTypeCounts(parental, basetype, progeny_size, distance)
	if debug is True: print("tetradCount=", tetradCount)

	return tetradCount

#====================================
def generateTypeCountsX2(parental_type, basetype, progeny_size, distance):
	type_counts = {}
	recombinant_type_1 = flipGene(parental_type, geneorder[0], basetype)
	if debug is True: print("recombinant type 1=", recombinant_type_1)
	recombinant_type_2 = invertType(recombinant_type_1, basetype)
	if debug is True: print("recombinant type 2=", recombinant_type_2)

	if debug is True: print("determine recombinant type counts")
	total_recombinant_count = int(round(distance*progeny_size/100.))
	recombinant_count_1 = 0
	recombinant_count_2 = 0
	for i in range(total_recombinant_count):
		if random.random() < 0.5:
			recombinant_count_1 += 1
		else:
			recombinant_count_2 += 1
	if recombinant_count_1 == recombinant_count_2:
		shift = random.randint(1,4)
		recombinant_count_1 += shift
		recombinant_count_2 -= shift
	
	type_counts[recombinant_type_1] = recombinant_count_1
	if debug is True: print("recombinant count_1=", recombinant_count_1)
	type_counts[recombinant_type_2] = recombinant_count_2
	if debug is True: print("recombinant count_2=", recombinant_count_2)

	if debug is True: print("determine parental type count")
	total_parent_count = progeny_size - total_recombinant_count
	if debug is True: print("  ", parental_type, invertType(parental_type, basetype), total_parent_count)
	parent_count_1 = 0
	parent_count_2 = 0
	for i in range(total_parent_count):
		if random.random() < 0.5:
			parent_count_1 += 1
		else:
			parent_count_2 += 1
	if parent_count_1 == parent_count_2:
		shift = random.randint(1,4)
		parent_count_1 += shift
		parent_count_2 -= shift
	
	type_counts[parental_type] = parent_count_1
	if debug is True: print("parental count_1=", parent_count_1)
	type_counts[invertType(parental_type, basetype)] = parent_count_2
	if debug is True: print("parental count_2=", parent_count_2)


	return type_counts

#====================================
def generateTypeCounts(parental, basetype, progeny_size, distance):
	
	#distance = (3*NPD + TT/2) / progeny_size * 100%
	#NPD = double cross // 4
	#double cross = 2 * progeny_size * distance/100
	nonparent_ditype_count = progeny_size * distance**2 // 40000 + 1
	tetra_type_count = 2 * (distance*progeny_size//100 - 3 * nonparent_ditype_count)
	parent_ditype_count = progeny_size - tetra_type_count - nonparent_ditype_count

	if parent_ditype_count <= 0 or tetra_type_count <= 0:
		return None
	if tetra_type_count > parent_ditype_count:
		return None

	print("[3*{0} + {1}/2 ]//{2} = {3}".format(
		nonparent_ditype_count, tetra_type_count, progeny_size, distance))

	# Create Four Genotypes
	tetradCount = {}
	parental_type_1 = parental
	parental_type_2 = invertType(parental, basetype)
	recombinant_type_1 = flipGene(parental, basetype[0], basetype)
	recombinant_type_2 = flipGene(parental, basetype[1], basetype)

	#parental ditype (PD)
	tetradSet = [parental_type_1, parental_type_1, parental_type_2, parental_type_2,]
	tetradSet.sort()
	if debug is True: print(" parental ", tetradSet)
	if debug is True: print(" parent_ditype_count ", parent_ditype_count)


	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = parent_ditype_count

	#tetra-type (TT)
	tetradSet = [parental_type_1, parental_type_2, recombinant_type_1, recombinant_type_2, ]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = tetra_type_count
	if debug is True: print(" tetra-type (TT) ", tetradSet)
	if debug is True: print(" tetra_type_count ", tetra_type_count)

	#non-parental ditype (NPD)
	tetradSet = [recombinant_type_1, recombinant_type_1, recombinant_type_2, recombinant_type_2,]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = nonparent_ditype_count
	if debug is True: print(" non-parental ditype (NPD) ", tetradSet)
	if debug is True: print(" nonparent_ditype_count ", nonparent_ditype_count)

	return tetradCount

#=======================
def questionText(basetype):
	question_string = '<h6>Unordered Tetrad Two Gene Distance</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among two genes. '
	question_string += '<p>Using the table above, determine the distance between the two genes.</p> '
	question_string += '<ul> <li><i>Hint 1:</i> The gene distance will be a whole number, '
	question_string += 'do NOT enter a decimal; if you have a decimal your calculations are likely wrong.</li>'
	question_string += '<li><i>Hint 2:</i> enter your answer in the blank using only numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</li></ul> '
	question_string += '<p>Dr. Voss guide to unordered tetrads:</p><ul>'
	question_string += '<li>Step 1: Find the Row for the Parental Ditype (PD).</li>'
	question_string += '<li>Step 2: Assign PD, NPD, TT for each row</li>'
	question_string += '<li>Step 3: Determine if the two genes are linked.</li>'
	question_string += '<ul><li>PD >> NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	question_string += '<li>Step 4: Determine the map distance between the two genes</li>'
	question_string += '<ul><li>D = &half; (TT + 6 NPD)/total = (3 NPD + &half;TT)/total</li></ul>'
	question_string += '</ul>'

	return question_string

#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=====================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table.+\<\/table\>', '[]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_NUM_Question(N, question, answer, tolerance):
	bb_question = ''

	number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'NUM\t<p>{0}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	bb_question += '\t{0:d}\t{1:.1f}'.format(answer, tolerance)
	print("ANSWER {0:d} +/- {1:.1f}".format(answer, tolerance))
	print("")
	return bb_question + '\n'

#=====================
#=====================
if __name__ == "__main__":
	lowercase = "abcdefghijklmnpqrsuvwxyz"

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 198
	j = -1
	N = 0
	for i in range(duplicates):
		N += 1
		j += 1
		if j + 1 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+2]
		geneorder = basetype
		distance = getDistance()
		print("distance=", distance)
		progeny_size = getProgenySize(distance)

		typemap = makeQuestion(basetype, distance, progeny_size)
		if typemap is None:
			continue

		ascii_table = makeProgenyAsciiTable(typemap, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(typemap, progeny_size)
		#print(html_table)
		question_string = questionText(basetype)
		complete_question = html_table + question_string

		#final_question = blackboardFormat(question_string, html_table, variable_list, geneorder, distances)
		final_question = formatBB_NUM_Question(N, complete_question, distance, 0.1)

		#print(final_question)

		f.write(final_question)
	f.close()
