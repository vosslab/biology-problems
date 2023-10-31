#!/usr/bin/env python3

import os
import re
import sys
import copy
import math
import numpy
import string
import random

import bptools
import pointtestcrosslib as ptcl

debug = False

def getDistances():
	#integers
	"""key_maps = {
		35:	[10, 20, 30, 40, ],
		30:	[ 5, 10, 15, 20, 25, 35,],
		25:	[ 2,  4,  6,  8, 12, 14, 16, 18, 22,],
		20:	[ 5, 10, 15, 25, 30, 35,],
		15:	[10, 20, 30, 40, ],
		10:	[ 5, 15, 20, 25, 30, 35,],
		5:	[10, 20, 30, 40, ],
	}"""
	#a = random.choice(list(key_maps.keys()))
	#b = random.choice(key_maps[a])
	a = random.randint(15,35)
	b = random.randint(2,a-2)
	if a == b:
		print("ERROR")
		sys.exit(1)
	if debug is True: print("determine gene distances")
	distances = [a, b]
	random.shuffle(distances)
	distance3 = int(distances[0] + distances[1] - (distances[0] * distances[1])/50)
	distances.append(distance3)
	if debug is True: print(distances)
	return distances

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

def getProgenySize(distances):
	if debug is True: print("determine progeny size")
	gcd1 = math.gcd(distances[0], 100)
	gcd2 = math.gcd(distances[1], 100)
	gcdfinal = math.gcd(gcd1, gcd2)
	if debug is True: print("Final GCD", gcdfinal)
	progenybase = 100/gcdfinal
	minprogeny =  900/progenybase
	maxprogeny = 6000/progenybase
	progs = numpy.arange(minprogeny, maxprogeny+1, 1, dtype=numpy.float64)*progenybase
	#print(progs)
	numpy.random.shuffle(progs)
	#print(progs)
	bases = progs * distances[0] * distances[1] / 1e4
	#print(bases)
	devs = (bases - numpy.around(bases, 0))**2
	#print(devs)
	argmin = numpy.argmin(devs)
	progeny_size = int(progs[argmin])
	if debug is True: print(("total progeny: %d\n"%(progeny_size)))
	return progeny_size

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
		phenotype_string = ptcl.get_phenotype_name(type)
		table += '<tr>'
		table += ' <td {0}>&nbsp;{1}{2}</span></td>'.format(td_extra.replace('center', 'left'), span, phenotype_string)
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, type[0])
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, type[1])
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, type[2])
		table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, typemap[type])
		table += '</tr>'
	table += '<tr>'
	table += '  <th colspan="4" {0}">{1}TOTAL =</span></th>'.format(td_extra.replace('center', 'right'), span)
	table += '  <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, progeny_size)
	table += '</tr>'
	table += '</table>'
	return table

def makeProgenyAsciiTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	table = ''
	for type in alltypes:
		phenotype_string = ptcl.get_phenotype_name(type)
		table += ("{0}\t".format(type[0]))
		table += ("{0}\t".format(type[1]))
		table += ("{0}\t".format(type[2]))
		table += ("{0:d}\t".format(typemap[type]))
		table += ("{0}\t".format(phenotype_string))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table

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
	question_string = '<h6>Three-Point Test-Cross Gene Mapping</h6>'
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
	pretty_question = re.sub('\<table.+\<\/table\>', '[]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
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
		basetype = lowercase[j:j+3]
		geneorder = ptcl.get_random_gene_order(basetype)
		distances = getDistances()
		print(distances)
		progeny_size = getProgenySize(distances)
		typemap = makeQuestion(basetype, geneorder, distances, progeny_size)
		ascii_table = makeProgenyAsciiTable(typemap, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(typemap, progeny_size)
		#print(html_table)
		question_string = questionText(basetype)
		variable_list = getVariables(geneorder)
		complete_question = html_table + question_string
		final_question = formatBB_FIB_PLUS_Question(N, complete_question, variable_list, geneorder, distances)
		#print(final_question)
		f.write(final_question)
	f.close()
#THE END
