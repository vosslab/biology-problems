#!/usr/bin/env python

import os
import sys
import copy
import math
import random

import bptools
import phylolib


# make a gene tree table with 4 leaves, ask students to choose correct one

total_choices = 6

#===========================================
def makeRandDistanceList(num_distances):
	distances = []
	while len(distances) < num_distances:
		r = random.randint(2, num_distances*4)
		r *= 2
		skip = False
		for d in distances:
			if abs(r - d) <= 4:
				skip = True
		if skip is False:
			distances.append(r)
	distances.sort()
	return distances

#===========================================
def assignDistanceTuple(gene1, gene2, distance, distance_dict, linked_genes):
	gene_tuple1  = (gene1, gene2)
	gene_tuple2  = (gene2, gene1)
	distance_dict[gene_tuple1] = distance
	distance_dict[gene_tuple2] = distance

	return

#===========================================
def getShifts(num_linked_genes):
	if num_linked_genes == 1:
		return [0,]
	if num_linked_genes == 2:
		c = random.randint(1,2)
		s = random.randint(1,3)
		if c == 1:
			return [-s,s]
		else:
			return [s,-s]
	if num_linked_genes == 3:
		c = random.randint(1,4)
		s = random.randint(1,3)
		if c == 1:
			return [-s,-s,s]
		elif c == 2:
			return [-s,s,0]
		elif c == 3:
			return [s,-s,0]
		elif c == 4:
			return [s,s,-s]

#===========================================
def makeDistances_Comb(ordered_genes):
	# A-1-B -2-C -3-D
	distance_dict = {}
	num_distances = math.comb(len(ordered_genes), 2)//2
	distances = makeRandDistanceList(num_distances)
	print("distances=",distances)
	distance_dict = {}
	for i,g1 in enumerate(ordered_genes):
		if i == 0:
			continue
		shifts = getShifts(i)
		print("i=",i,"shifts=",shifts)
		for j,g2 in enumerate(ordered_genes):
				if i <= j:
					continue
				# i > j OR j < i
				key1 = (ordered_genes[j], ordered_genes[i])
				key2 = key1[::-1]
				distance_dict[key1] = distances[i-1] + shifts[j]
				distance_dict[key2] = distances[i-1] + shifts[j]
	makeTable_ascii(ordered_genes, distance_dict)
	return distance_dict

#===========================================
def makeTable_ascii(ordered_genes, distance_dict):
	sorted_genes = list(copy.copy(ordered_genes))
	sorted_genes.sort()
	sys.stderr.write('\t')
	for gene in sorted_genes:
		sys.stderr.write('{0}\t'.format(gene))
	sys.stderr.write('\n')
	for gene1 in sorted_genes:
		sys.stderr.write('{0}\t'.format(gene1))
		for gene2 in sorted_genes:
			if gene1 == gene2:
				sys.stderr.write('x\t')
			else:
				gene_tuple  = (gene1, gene2)
				distance = distance_dict[gene_tuple]
				sys.stderr.write('{0:d}\t'.format(distance))
		sys.stderr.write('\n')
		
#===========================================
def makeTable_html(ordered_genes, distance_dict):
	sorted_genes = list(copy.copy(ordered_genes))
	sorted_genes.sort()
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'

	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 460px; height: 150px">'
	table += '<tr>'
	table += '  <td {0}>genes</td>'.format(td_extra)
	for g in sorted_genes:
		table += '  <th {0}>{1}{2}</span></th>'.format(td_extra, span, g)
	table += '</tr>'
	for g1 in sorted_genes:
		table += '<tr>'
		table += '  <th {0}>{1}{2}</span></th>'.format(td_extra, span, g1)
		for g2 in sorted_genes:
			if g1 == g2:
				table += ' <td {0} style="background-color: gray">&times;</td>'.format(td_extra)
			else:
				#gene_sum = ordered_genes.index(g1) + ordered_genes.index(g2)
				gene_tuple  = (g1, g2)
				distance = distance_dict[gene_tuple]
				#d = distances[gene_sum-1]
				table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra, span, distance)
		table += '</tr>'
	table += '</table>'
	return table

#===========================================
def makeQuestion(gene_list, version):
	sorted_genes = copy.copy(gene_list)
	sorted_genes.sort()
	
	perms = phylolib.comb_safe_permutations(sorted_genes)
	print(perms)

	index = version % len(sorted_genes)
	ordered_genes = perms.pop(index)
	opposite_genes = (ordered_genes[0], ordered_genes[1], ordered_genes[3], ordered_genes[2])
	perms.remove(opposite_genes)
	print('ordered_genes=',ordered_genes)

	distance_dict = makeDistances_Comb(ordered_genes)
	print("distance_dict=",distance_dict)

	answer = phylolib.random_comb_tree_4_leaves_html(ordered_genes)
	opposite = phylolib.random_comb_tree_4_leaves_html(opposite_genes)

	#1: comb_tree_4_leaves_html(values, distances)
	#row1 = "         ____ a"
	#row2 = "      __|      "
	#row3 = "     |  |____ b"
	#row4 = "   __|         "
	#row5 = "  |  |_______ c"
	#row6 = "__|            "
	#row7 = "  |__________ d"
	#2: comb_tree_4_leaves_alternate_html(values, distances)
	#row6 = "   ____________ d"
	#row6 = "  |              "
	#row1 = "__|        ____ a"
	#row2 = "  |   ____|      "
	#row3 = "  |  |    |____ b"
	#row4 = "  |__|           "
	#row5 = "     |_________ c"
	#3: balanced_tree_4_leaves_html(values, distances)
	#row1 = "           ____ a"
	#row2 = "      ____|     "
	#row3 = "     |    |____ b"
	#row4 = "   __|          "
	#row5 = "     |   ______ c"
	#row6 = "     |__|        "
	#row6 = "        |______ d"

	wrongs = []
	for oth in perms:
		wrong_tree = phylolib.random_tree_4_leaves_html(oth)
		wrongs.append(wrong_tree)

	random.shuffle(wrongs)
	choices = wrongs[:total_choices-1]
	choices.append(opposite)
	choices.append(answer)
	random.shuffle(choices)

	question = ''
	question += makeTable_html(ordered_genes, distance_dict)
	question += '<p></p><h6>Given the table above, '
	question += 'which one of the following gene trees best fit the distance matrix data?</h6>'

	complete = bptools.formatBB_MC_Question(version, question, choices, answer)
	return complete

#===========================================
#===========================================
if __name__ == "__main__":
	lowercase = "abcdefghjkmnpqrstuwxyz"

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 16
	j = -1
	N = 0
	for i in range(duplicates):
		j += 1
		if j + 3 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+4]
		gene_list = list(basetype)
		N += 1
		complete_question = makeQuestion(gene_list, N)
		f.write(complete_question)
	f.close()
	print("{0} questions were written to file {1}".format(N, outfile))
