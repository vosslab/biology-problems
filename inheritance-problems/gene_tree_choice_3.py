#!/usr/bin/env python3

import os
import sys
import copy
import math
import random

import bptools
from classic_phylolib import phylolib

# make a gene tree with 3 leaves, ask students to find the similar one

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
def makeDistances_Comb(ordered_genes):
	# A-1-B -2-C -3-D
	distance_dict = {}
	num_distances = math.comb(len(ordered_genes), 2)
	distances = makeRandDistanceList(num_distances)
	print("distances=",distances)
	distance_dict = {}
	for i,g1 in enumerate(ordered_genes):
		if i == 0:
			continue
		for j,g2 in enumerate(ordered_genes):
				if i <= j:
					continue
				# i > j OR j < i
				key1 = (ordered_genes[j], ordered_genes[i])
				key2 = key1[::-1]
				distance_dict[key1] = distances[i-1]
				distance_dict[key2] = distances[i-1]
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


def makeQuestion(sorted_genes, version):
	perms = phylolib.comb_safe_permutations(sorted_genes)
	index = version % len(sorted_genes)
	ordered_genes = perms.pop(index)

	alt_answer1 = phylolib.comb_tree_3_leaves_html(ordered_genes)
	alt_answer2 = phylolib.comb_tree_3_leaves_alternate_html(ordered_genes)
	answer = random.choice([alt_answer1, alt_answer2])

	wrongs = []
	#for oth in perms:		
	#	wrong_tree = phylolib.random_comb_tree_3_leaves_html(oth)
	#	wrongs.append(wrong_tree)
	for oth in perms:		
		w1 = phylolib.comb_tree_3_leaves_html(oth)
		wrongs.append(w1)
		w2 = phylolib.comb_tree_3_leaves_alternate_html(oth)
		wrongs.append(w2)

	w3 = phylolib.balanced_tree_3_leaves_html(ordered_genes)
	wrongs.append(w3)

	choices = set(wrongs)
	choices.discard(alt_answer1)
	choices.discard(alt_answer2)
	choices = list(choices)
	choices.append(answer)
	random.shuffle(choices)

	distance_dict = makeDistances_Comb(ordered_genes)
	question = ''
	question += makeTable_html(ordered_genes, distance_dict)
	question += '<p></p><h6>Given the table above, which one of the following gene trees best fit the distance matrix data?</h6>'

	complete = bptools.formatBB_MC_Question(version, question, choices, answer)
	return complete


if __name__ == "__main__":
	lowercase = "abcdefghjkmnpqrstuwxyz"

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 24
	j = -1
	N = 0
	for i in range(duplicates):
		j += 1
		if j + 2 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+3]
		g = list(basetype)
		N += 1
		complete_question = makeQuestion(g, N)
		f.write(complete_question)
	f.close()
	print("{0} questions were written to file {1}".format(N, outfile))
