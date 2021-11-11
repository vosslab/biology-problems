#!/usr/bin/env python

import os
import sys
import copy
import math
import random
import phylolib

# make a gene tree table with 4 leaves, ask students to choose correct one

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
		s = 0
		return [-s,s]
	if num_linked_genes == 3:
		s = 0
		return [-s,0,s]
	if num_linked_genes == 4:
		s1 = 2
		s2 = 4
		return [-s2,-s1,s1,s2]

#===========================================
def makeDistances_Comb(ordered_genes):
	distance_dict = {}
	num_distances = math.comb(len(ordered_genes), 2)
	distances = makeRandDistanceList(num_distances)
	print(distances)
	i = 0
	linked_genes = {}
	for gene in ordered_genes:
		linked_genes[gene] = [gene,]
	index = 1
	for gene1 in ordered_genes:
		for gene2 in ordered_genes:
			if gene1 <= gene2:
				continue
			distance = distances[i]
			num_linked_genes = len(linked_genes[gene1])
			shifts = getShifts(num_linked_genes)
			print(num_linked_genes, shifts)
			for j,gene3 in enumerate(linked_genes[gene1]):
				assignDistanceTuple(gene3, gene2, distance+shifts[j], distance_dict, linked_genes)
			linked_genes[gene1].append(gene2)
			linked_genes[gene2].append(gene1)
			i += 1
	makeTable_ascii(ordered_genes, distance_dict)
	print(distance_dict)
	print(linked_genes)
	return distance_dict

#===========================================
def makeTable_ascii(ordered_genes, distance_dict):
	sorted_genes = copy.copy(ordered_genes)
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
def makeTable(ordered_genes, distances):
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'

	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 460px; height: 150px">'
	table += '<tr>'
	table += '  <td {0}>genes</td>'.format(td_extra)
	for g in ordered_genes:
		table += '  <th {0}>{1}{2}</span></th>'.format(td_extra, span, g)
	table += '</tr>'
	for g1 in ordered_genes:
		table += '<tr>'
		table += '  <th {0}>{1}{2}</span></th>'.format(td_extra, span, g1)
		for g2 in ordered_genes:
			if g1 == g2:
				table += ' <td {0} style="background-color: gray">&times;</td>'.format(td_extra)
			else:
				gene_sum = genes.index(g1) + genes.index(g2)
				d = distances[gene_sum-1]
				table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra, span, d)
		table += '</tr>'
	table += '</table>'
	return table

#===========================================
def makeQuestion(gene_list, version):
	ordered_genes = copy.copy(gene_list)
	random.shuffle(ordered_genes)
	
	perms = phylolib.comb_safe_permutations(ordered_genes)
	index = version % len(ordered_genes)
	genes = perms.pop(index)
	distances = makeDistances_Comb(ordered_genes)
	#print(genes)
	#print(perms)
	#print(distances)
	if version // len(ordered_genes) == 0:
		answer = phylolib.comb_tree_4_leaves_html(genes)
	else:
		answer = phylolib.comb_tree_4_leaves_alternate_html(genes)

	wrongs = []
	for oth in perms:
		wrong_tree = phylolib.random_tree_4_leaves_html(oth)
		wrongs.append(wrong_tree)

	random.shuffle(wrongs)
	choices = wrongs[:4]
	choices.append(answer)
	random.shuffle(choices)

	question = ''
	question += makeTable(genes, distances)
	question += '<p></p><h6>Given the table above, '
	question += 'which one of the following gene trees best fit the distance matrix data?</h6>'
	complete = 'MC\t'
	complete += question
	for c in choices:
		complete += '\t'+c
		if c == answer:
			complete += "\tCorrect"
		else:
			complete += "\tIncorrect"
	complete += '\n'
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
