#!/usr/bin/env python3

import os
import sys
import random
import argparse
from itertools import combinations


import bptools
import genemaplib as gml
#import tetradlib

debug = True

def tetradSetToString(tetradSet):
	return '\t'.join(tetradSet)

def invertType(genotype, basetype):
	return gml.invert_genotype(genotype, basetype)

def flipGene(genotype, gene, basetype):
	return gml.flip_gene_by_letter(genotype, gene, basetype)

def set_gene_order(gene_letters_str):
	return gml.get_random_gene_order(gene_letters_str)

#=====================
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

#=====================
def makeProgenyAsciiTable(progeny_tetrads_count_dict, progeny_size):
	alltypes = sorted(progeny_tetrads_count_dict.keys())
	table = ''
	for type in alltypes:
		table += ("{0}\t".format(type))
		table += ("{0:d}\t".format(progeny_tetrads_count_dict[type]))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table

#=====================
def construct_progeny_counts(gene_letters_str, gene_order_str, distances, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s - %d - %s"
		%(gene_order_str[0], distances[0], gene_order_str[1], distances[1], gene_order_str[2]))
	print(answerString)
	if debug is True: print("------------")

	if debug is True: print("determine double crossovers")
	doublecross = distances[0]*distances[1]/100.
	if debug is True: print("doublecross", doublecross*10, 'per 1000')

	if debug is True: print("determine parental type")
	types = ['++'+gene_letters_str[2], '+'+gene_letters_str[1]+'+', '+'+gene_letters_str[1]+gene_letters_str[2]]
	parental = random.choice(types)

	progeny_tetrads_count_dict = generateTypeCounts(parental, gene_order_str, distances, progeny_size, gene_letters_str)
	return progeny_tetrads_count_dict

#=====================
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
	#r01 = d01/totalcross
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

#=====================
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

#=====================
def questionText(gene_letters_str):
	question_string = '<h6>Unordered Tetrad Three Gene Mapping</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among three genes. '
	question_string += '<p>Using the table, determine the order of the genes and the distances between them. '
	question_string += 'Once calculated, fill in the following four blanks: </p><ul>'
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(gene_letters_str[0].upper(),gene_letters_str[1].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(gene_letters_str[0].upper(),gene_letters_str[2].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(gene_letters_str[1].upper(),gene_letters_str[2].upper())
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

#=====================
def create_pair_variable(gene1, gene2):
	"""Helper function to create a variable name from two genes in alphabetical order."""
	return f"{min(gene1, gene2).upper()}{max(gene1, gene2).upper()}"

#=====================
def make_answer_map(gene_order_str, distances):
	"""
	Creates a mapping of variable names to their associated distances and gene order.

	For a given gene order and a list of distances, this function generates a dictionary where:
	- Each pairwise combination of genes (in alphabetical order) is mapped to a distance.
	- The full gene order is mapped to both its original and reversed versions.

	Args:
		gene_order_str (str): A string of gene letters, e.g., 'abc'.
		distances (list): A list of distances between each pair of genes, e.g., [5, 10, 15].

	Returns:
		dict: A dictionary with variable names as keys and distance or gene order as values.

	Example:
		>>> make_answer_map('abc', [5, 10, 15])
		{
			'AB': [5],
			'BC': [10],
			'AC': [15],
			'geneorder': ['abc', 'cba']
		}
	"""
	# Initialize answer map with pairwise gene combinations
	answer_map = {
		create_pair_variable(gene_order_str[0], gene_order_str[1]): [distances[0]],
		create_pair_variable(gene_order_str[1], gene_order_str[2]): [distances[1]],
		create_pair_variable(gene_order_str[0], gene_order_str[2]): [distances[2]],
	}
	# Add the full gene order and its reverse as a separate entry
	answer_map['geneorder'] = [gene_order_str, gene_order_str[::-1]]
	return answer_map


#=====================
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()
	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 1
	distance_triplet_list = gml.get_all_distance_triplets(msg=debug)
	for i in range(args.duplicates):
		gene_letters_str = gml.get_gene_letters(3)

		gene_order_str = set_gene_order(gene_letters_str)

		distances = sorted(random.choice(distance_triplet_list))
		while distances[1] > 26 and len(set(distances)) == 3:
			distances = sorted(random.choice(distance_triplet_list))
		if debug: print(f"distances = {distances}")

		progeny_size = gml.get_general_progeny_size(distances)

		progeny_tetrads_count_dict = construct_progeny_counts(gene_letters_str, gene_order_str, distances, progeny_size)
		if progeny_tetrads_count_dict is None:
			print("question failed")
			print(f"distances = {distances}")
			sys.exit(1)
			continue
		print(f"progeny_tetrads_count_dict = {progeny_tetrads_count_dict}")

		ascii_table = makeProgenyAsciiTable(progeny_tetrads_count_dict, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(progeny_tetrads_count_dict, progeny_size)
		#print(html_table)
		question_string = questionText(gene_letters_str)
		answer_map = make_answer_map(gene_order_str, distances)

		complete_question = html_table + question_string
		final_question = bptools.formatBB_FIB_PLUS_Question(N, complete_question, answer_map)
		if final_question is not None:
			N += 1
			f.write(final_question)
		else:
			print("question failed")
	f.close()

if __name__ == "__main__":
	main()
