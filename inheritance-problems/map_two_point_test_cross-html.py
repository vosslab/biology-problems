#!/usr/bin/env python

import os
import sys
import math
import numpy
import string
import random

debug = True

#====================================
phenotype_dict = {
	'a': 'amber',
	'b': 'bald',
	'c': 'conehead',
	'd': 'dumpy',
	'e': 'eyeless',
	'f': 'forked',
	'g': 'garnet',
	'h': 'hook',
	'i': 'indy',
	'j': 'jagged',
	'k': 'kidney',
	'l': 'lyra',
	'm': 'marula',
	'n': 'notch',
	'o': 'okra',
	'p': 'prickly',
	'q': 'quick',
	'r': 'rosy',
	's': 'scute',
	't': 'taxi',
	'u': 'upturned',
	'v': 'vestigial',
	'w': 'white',
	'x': 'xray',
	'y': 'yellow',
	'z': 'zipper',
}

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
def getGeneOrder(basetype):
	basetype2 = basetype[0]+basetype[2]+basetype[1]
	basetype3 = basetype[1]+basetype[0]+basetype[2]

	#gene order
	if debug is True: print("selecting gene order")
	geneorder = random.choice([basetype, basetype2, basetype3])
	if debug is True: print(geneorder)
	return geneorder

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
def getPhenotype(genotype):
	if genotype == "++":
		return '<i>wildtype</i>'
	phenotype_list = []
	for allele in genotype:
		if allele == '+':
			continue
		phenotype = phenotype_dict.get(allele)
		phenotype_list.append(phenotype)
	#print(phenotype_list)
	phenotype_string = ', '.join(phenotype_list)
	return phenotype_string

#====================================
def makeProgenyHtmlTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'
	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 460px; height: 280px">'
	table += '<tr>'
	table += '  <th {0}>{1}Phenotype</span></th>'.format(td_extra, span)
	table += '  <th colspan="3" {0}>{1}Genotypes</span></th>'.format(td_extra, span)
	table += '  <th {0}>{1}Progeny<br/>Count</span></th>'.format(td_extra, span)
	table += '</tr>'
	for type in alltypes:
		phenotype_string = getPhenotype(type)
		table += '<tr>'
		table += ' <td {0}>&nbsp;{1}{2}</span></td>'.format(td_extra.replace('center', 'left'), span, phenotype_string)
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, type[0])
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, type[1])
		table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, typemap[type])
		table += '</tr>'
	table += '<tr>'
	table += '  <th colspan="4" {0}">{1}TOTAL =</span></th>'.format(td_extra.replace('center', 'right'), span)
	table += '  <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, progeny_size)
	table += '</tr>'
	table += '</table>'
	return table

#====================================
def makeProgenyAsciiTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	table = ''
	for genotype in alltypes:
		phenotype_string = getPhenotype(genotype)
		table += ("{0}\t".format(genotype[0]))
		table += ("{0}\t".format(genotype[1]))
		table += ("{0:d}\t".format(typemap[genotype]))
		table += ("{0}\t".format(phenotype_string))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table


#====================================
def getCode():
	source = string.ascii_uppercase + string.digits
	code = ''
	for i in range(5):
		code += random.choice(source)
	code += ' - '
	return code

#====================================
def questionText(basetype):
	question_string = getCode()
	question_string += '<h6>Two-Point Test-Cross Gene Mapping</h6>'
	question_string += '<p>A test-cross with a heterozygote fruit fly for two genes is conducted. '
	question_string += 'The resulting phenotypes are summarized in above table.</p> '
	question_string += '<p>Using the table, determine the distance between the two genes. '
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[1].upper())
	question_string += '<p><i>Hint 1:</i> The gene distance will be a whole number, '
	question_string += 'do NOT enter a decimal; if you have a decimal your calculations are likely wrong.</p>'
	question_string += '<p><i>Hint 2:</i> enter your answer in the blank using only numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</p>'
	return question_string

#====================================
def getVariables(basetype):
	variable_list = []
	if basetype[0] < basetype[1]:
		variable = '{0}{1}'.format(basetype[0].upper(),basetype[1].upper())
	else:
		variable = '{0}{1}'.format(basetype[1].upper(),basetype[0].upper())
	variable_list.append(variable)
	variable = 'geneorder'
	variable_list.append(variable)
	return variable_list

#====================================
def blackboardFormat(question_string, html_table, variable_list, distance):
	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	blackboard = 'FIB_PLUS\t'
	blackboard += html_table
	blackboard += question_string
	variable_to_distance = {}
	for i in range(len(variable_list)-1):
		variable_to_distance[variable_list[i]] = distance
	variable_list.sort()
	for i in range(len(variable_list)-1):
		variable = variable_list[i]
		blackboard += '\t{0}\t{1}\t'.format(variable, variable_to_distance[variable])
	return blackboard


#====================================
def generateTypeCounts(parental_type, basetype, progeny_size, distance):
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
	
	type_counts[parental_type] = parent_count_1
	if debug is True: print("parental count_1=", parent_count_1)
	type_counts[invertType(parental_type, basetype)] = parent_count_2
	if debug is True: print("parental count_2=", parent_count_2)


	return type_counts

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
	if debug is True: print("parental=", parental, invertType(parental, basetype))
	type_counts = generateTypeCounts(parental, basetype, progeny_size, distance)
	if debug is True: print("type_counts=", type_counts)
	return type_counts

#====================================
#====================================
if __name__ == "__main__":
	lowercase = "abcdefghijklmnpqrsuvwxyz"

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 3
	j = -1
	for i in range(duplicates):
		j += 1
		if j + 3 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+2]
		geneorder = basetype
		distance = getDistance()
		print(basetype, distance)
		progeny_size = getProgenySize(distance)
		typemap = makeQuestion(basetype, distance, progeny_size)
		ascii_table = makeProgenyAsciiTable(typemap, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(typemap, progeny_size)
		#print(html_table)
		question_string = questionText(basetype)
		variable_list = getVariables(geneorder)

		final_question = blackboardFormat(question_string, html_table, variable_list, distance)
		#print(final_question)

		f.write(final_question)
	f.close()







#THE END
