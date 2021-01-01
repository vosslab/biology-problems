#!/usr/bin/env python

import os
import sys
import copy
import math
import numpy
import string
import random

debug = False

def tetradSetToString(tetradSet):
	mystr = ("%s\t%s\t%s\t%s\t"
		%(tetradSet[0],tetradSet[1],tetradSet[2],tetradSet[3],))
	return mystr

def invertType(genotype, basetype):
	newtype = ''
	for i in range(3):
		if genotype[i] == '+':
			newtype += basetype[i]
		else:
			newtype += '+'
	return newtype

def flipGene(genotype, gene, basetype):
	newlist = list(genotype)
	for i in range(3):
		if basetype[i] == gene:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'
	newtype = ""
	for i in newlist:
		newtype += i
	return newtype

def getGeneOrder(basetype):
	basetype2 = basetype[0]+basetype[2]+basetype[1]
	basetype3 = basetype[1]+basetype[0]+basetype[2]

	#gene order
	if debug is True: print("selecting gene order")
	geneorder = random.choice([basetype, basetype2, basetype3])
	if debug is True: print(geneorder)
	return geneorder

def getDistancesThreePoint():
	#integers
	key_maps = {
		35:	[10, 20, 30, 40, ],
		30:	[ 5, 10, 15, 20, 25, 35,],
		25:	[ 2,  4,  6,  8, 12, 14, 16, 18, 22,],
		20:	[ 5, 10, 15, 25, 30, 35,],
		15:	[10, 20, 30, 40, ],
		10:	[ 5, 15, 20, 25, 30, 35,],
		5:	[10, 20, 30, 40, ],
	}
	a = random.choice(list(key_maps.keys()))
	b = random.choice(key_maps[a])
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

def getDistances():
	#return [7,15,19]
	#return [6,16,19]
	return getDistancesOriginal()

def getProgenySize(distances):
	#return 2*2*3*3*5*5*7*7*11
	#return getProgenySizeThreePoint(distances)
	#return getProgenySizeTetrads(distances)
	return getProgenySizeTetradThree(distances)

def getProgenySizeThreePoint(distances):
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

#600*dcount3/progeny_size is integer

def lcm(a, b):
	return abs(a*b) // math.gcd(a, b)

def lcm4(a, b, c, d):
	gcd1 = math.gcd(a, b)
	gcd2 = math.gcd(c, d)
	gcdfinal = math.gcd(gcd1, gcd2)
	return abs(a*b*c*d) // gcdfinal

def getProgenySizeTetradThree(distances):
	if debug is True: print("determine progeny size")
	dist_sum = distances[0] + distances[1]
	#return lcm4(10, distances[0], distances[1], dist_sum)
	gcd1 = math.gcd(distances[0], distances[1])
	gcd2 = math.gcd(dist_sum, 100)
	gcdfinal = math.gcd(gcd1, gcd2)
	if debug is True: print("Final GCD", gcdfinal)
	progenybase = 100 // gcdfinal
	minprogeny =  900 // progenybase
	maxprogeny = 6000 // progenybase
	progs = numpy.arange(minprogeny, maxprogeny+1, 1, dtype=numpy.uint16)*progenybase
	#print(progs)
	numpy.random.shuffle(progs)
	#print(progs)
	#print("")
	bases = progs * distances[0] * distances[1] / 1e4
	#print(bases)
	devs = (bases - numpy.around(bases, 0))**2
	devs = numpy.lcm(progs, 600)
	#print(devs)
	devs2 = devs // 600
	dev_lst = list(devs2)
	#print(devs2)
	doublecounts = distances[0] * distances[1] * progs // 10000 + 2
	doublecounts = numpy.where(doublecounts <= 4, 5, doublecounts)
	doublecounts // 2
	#print(doublecounts)
	for i,dev in enumerate(dev_lst):
		#print(dev, "<", doublecounts[i], "->", progs[i], )
		if dev < doublecounts[i]:
			progeny_size = int(progs[i])
			break
	#argmin = numpy.argmin(devs)
	#progeny_size = int(progs[argmin])
	if debug is True: print(("total progeny: %d\n"%(progeny_size)))
	return progeny_size


def getProgenySizeTetrads(distances):
	if debug is True: print("determine progeny size")
	gcd1 = math.gcd(distances[0], 100)
	gcd2 = math.gcd(distances[1], 100)
	gcdfinal = math.gcd(gcd1, gcd2)
	if debug is True: print("Final GCD", gcdfinal)
	progenybase = 100/gcdfinal
	progs = numpy.arange(2, 41, 1, dtype=numpy.float64)*progenybase
	numpy.random.shuffle(progs)
	bases = progs * distances[0] * distances[1] / 1e4
	devs = (bases - numpy.around(bases, 0))**2
	argmin = numpy.argmin(devs)
	progeny_size = int(progs[argmin])
	if debug is True: print(("total progeny: %d\n"%(progeny_size)))
	return progeny_size

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

	tetradCount = generateTypeCounts(parental, geneorder, distances, progeny_size, basetype)
	return tetradCount



def getDoubleCounts(distances, progeny_size):
	doublecross = distances[0]*distances[1]/100.
	doublecount = int(round(doublecross * progeny_size/100.))+2
	if doublecount <= 4:
		doublecount = 5
	if debug is True: print("doublecount", doublecount)

	# dcount3 controls the third distance
	# for progeny_size of 1000, each dcount3 = 0.6 distance
	maxdcount3 = int(2*doublecount // 3)
	for dcount3 in range(1, maxdcount3+1):
		distance3 = (distances[0] + distances[1]) - 6*dcount3/progeny_size*100
		distance3 = round(distance3,8) #must be whole number
		#print("dcount3", dcount3, "distance3", distance3)
		if distance3.is_integer():
			break
	#GIVE UP
	if dcount3 == maxdcount3:
		dcount3 = 0
	if debug is True: print("dcount3", dcount3)

	#simulate the other numbers
	#probably could be faster with Poisson random numbers, but this is more fun
	d00 = distances[0]*distances[0] #10^2
	d01 = 0 #distances[0]*distances[1] #10*20 #override for dcount3 set above
	d11 = distances[1]*distances[1] #20^2
	totalcross = float(d00 + d11 + d01)
	r00 = d00/totalcross
	r01 = d01/totalcross
	r11 = d11/totalcross
	dcount1 = 0
	dcount2 = 0
	#dcount3 = 0
	for i in range(doublecount-dcount3):
		r = random.random()
		if r < r00:
			dcount1 += 1
		elif r < r00 + r11:
			dcount2 += 1
		else:
			#dcount3 += 1
			print("DCOUNT3!!")
			pass
	#DEBUGGING ONLY--
	#dcount1 = int(round(r00*doublecount))
	#dcount2 = int(round(r01*doublecount))
	#dcount3 = int(round(r11*doublecount))
	if debug is True: print("DOUBLE COUNTS", dcount1, dcount2, dcount3, doublecount)
	return dcount1, dcount2, dcount3

def generateTypeCounts(parental, geneorder, distances, progeny_size, basetype):
	dcount1, dcount2, dcount3 = getDoubleCounts(distances, progeny_size)

	doublecount = dcount1 + dcount2 + dcount3
	firstcount = 2*(int(round(distances[0]*progeny_size/100.)) - 3*(dcount1 + dcount3))
	secondcount = 2*(int(round(distances[1]*progeny_size/100.)) - 3*(dcount2 + dcount3))
	parentcount = progeny_size - doublecount - firstcount - secondcount

	# dcount3 controls the third distance
	# for progeny_size of 1000, each dcount3 = 0.6 distance
	distance3 = 0.5*(firstcount + secondcount + 6*(doublecount - dcount3))
	distance3 = round(distance3/progeny_size*100, 4)
	print("DISTANCE 3: ", distance3)
	distances[2] = int(distance3)

	if not distance3.is_integer():
		return None
	if firstcount <= 0 or secondcount <= 0:
		print("two many double cross-overs")
		return None
	if firstcount >= parentcount:
		print("Tetratype larger than Parental Type")
		return None
	if secondcount >= parentcount:
		print("Tetratype larger than Parental Type")
		return None

	# Create Six Genotypes
	tetradCount = {}

	tetradSet = [parental, parental, invertType(parental, basetype), invertType(parental, basetype),]
	tetradSet.sort()
	if debug is True: print(" parental ", tetradSet)

	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = parentcount

	#first flip
	firsttype = flipGene(parental, geneorder[0], basetype)

	#usually TT
	tetradSet = [firsttype, invertType(firsttype, basetype), parental, invertType(parental, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = firstcount

	#usually NPD
	tetradSet = [firsttype, invertType(firsttype, basetype), firsttype, invertType(firsttype, basetype), ]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount1

	#second flip
	secondtype = flipGene(parental, geneorder[2], basetype)

	#usually TT
	tetradSet = [secondtype, invertType(secondtype, basetype), parental, invertType(parental, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = secondcount

	#usually NPD
	tetradSet = [secondtype, invertType(secondtype, basetype), secondtype, invertType(secondtype, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount2

	#both flips
	thirdtype = flipGene(flipGene(parental, geneorder[2], basetype), geneorder[0], basetype)

	#usually NPD
	tetradSet = [thirdtype, invertType(thirdtype, basetype), thirdtype, invertType(thirdtype, basetype),]
	tetradSet.sort()
	tetradName = tetradSetToString(tetradSet)
	tetradCount[tetradName] = dcount3

	return tetradCount

def getCode():
	source = string.ascii_uppercase + string.digits
	code = ''
	for i in range(5):
		code += random.choice(source)
	code += ' - '
	return code

def questionText(basetype):
	question_string = getCode()
	question_string += '<h6>Unordered Tetrad Gene Mapping</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among three genes. '
	question_string += '<p>Using the table, determine the order of the genes and the distances between them. '
	question_string += 'Once calculated, fill in the following four blanks: </p><ul>'
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[1].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[0].upper(),basetype[2].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(basetype[1].upper(),basetype[2].upper())
	question_string += '<li>From this the correct order of the genes is [geneorder] (gene order).</li></ul>'
	question_string += '<p><i>Hint 1:</i> ALL gene distances will be whole numbers, '
	question_string += ' do NOT enter a decimal; if you have a decimal your calculations are wrong.</p>'
	question_string += '<p><i>Hint 2:</i> enter your answer in the blank using only letters or numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</p>'
	question_string += '<ul>'
	question_string += '<li>Step 1: Find the Row for the Parental Type for all three genes.</li>'
	question_string += '<li>Step 2: Pick any two genes and assign PD, NPD, TT</li>'
	question_string += '<li>Step 3: Determine if the two genes are linked.</li>'
	question_string += '<ul><li>PD >> NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	question_string += '<li>Step 4: Determine the map distance between the two genes</li>'
	question_string += '<ul><li>D = &half; (TT + 6 NPD)/total = (3 NPD + &half;TT)/total</li></ul>'
	question_string += '<li>Step 5: Go to Step 2 and pick a new pair of genes until all pairs are complete.</li>'
	question_string += '</ul>'


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

def blackboardFormat(question_string, html_table, variable_list, geneorder, distances):
	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	blackboard = 'FIB_PLUS\t'
	blackboard += html_table
	blackboard += question_string
	variable_to_distance = {}
	for i in range(len(variable_list)-1):
		variable_to_distance[variable_list[i]] = distances[i]
	variable_list.sort()
	for i in range(len(variable_list)-1):
		variable = variable_list[i]
		blackboard += '\t{0}\t{1}\t'.format(variable, variable_to_distance[variable])
	blackboard += '\tgeneorder\t{0}\t{1}\n'.format(geneorder, geneorder[::-1])
	return blackboard


if __name__ == "__main__":
	lowercase = "abcdefghijklmnpqrsuvwxyz"

	filename = "bbq-unordered_tetrad.txt"
	f = open(filename, "w")
	duplicates = 98
	j = -1
	for i in range(duplicates):
		j += 1
		if j + 3 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+3]
		geneorder = getGeneOrder(basetype)
		distances = getDistances()
		print(distances)
		progeny_size = getProgenySize(distances)

		typemap = makeQuestion(basetype, geneorder, distances, progeny_size)
		if typemap is None:
			continue

		ascii_table = makeProgenyAsciiTable(typemap, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(typemap, progeny_size)
		#print(html_table)
		question_string = questionText(basetype)
		variable_list = getVariables(geneorder)

		final_question = blackboardFormat(question_string, html_table, variable_list, geneorder, distances)
		#print(final_question)

		f.write(final_question)
	f.close()
