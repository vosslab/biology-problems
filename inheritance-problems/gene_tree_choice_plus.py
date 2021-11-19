#!/usr/bin/env python

import os
import sys
import copy
import math
import random
import argparse
import colorsys
import itertools

#local
import bptools
import phylolib2

# make a gene tree table with 4 leaves, ask students to choose correct one

#===========================================
def rgb_to_hex(rgb1):
	rgb256 = tuple([int(i*255) for i in rgb1])
	#print(rgb256)
	return '#%02x%02x%02x' % rgb256

#===========================================
def distance_to_html_color(distance, distance_list):
	min_dist = distance_list[0]
	max_dist = distance_list[-1]
	fraction_diff = (max_dist - distance)/float(max_dist - min_dist)
	angle = fraction_diff/3.0
	rgb1 = colorsys.hsv_to_rgb(angle, 0.25, 0.85)
	html_hex = rgb_to_hex(rgb1)
	#print(html_hex)
	return html_hex

#===========================================
def comb_safe_permutations(genes):
	complete_set = itertools.permutations(genes, len(genes))
	comb_safe_set = list(complete_set)
	for p in comb_safe_set:
		#swap first two elements
		q = list(p)
		q[0], q[1] = q[1], q[0]
		r = tuple(q)
		comb_safe_set.remove(r)
	#print(comb_safe_set)
	return comb_safe_set

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

#==================================
def get_gene_pair_node(code, gene1, gene2):
	## assumes existing genes are alphabetical, also assumes ordered genes lag
	index1 = code.find(gene1)
	index2 = code.find(gene2)
	min_index = min(index1, index2)
	max_index = max(index1, index2)
	substring = code[min_index+1:max_index]
	#print("substring=", gene1, substring, gene2)
	sublist = list(substring)
	max_node = -1
	for s in sublist:
		if s.isdigit():
			s_int = int(s)
			max_node = max(max_node, s_int)
	#print("max_node=", max_node)
	return max_node

#===========================================
def makeDistancePairs(ordered_genes, distance_list, answer_code):
	# A-1-B -2-C -3-D
	distance_dict = {}
	num_distances = math.comb(len(ordered_genes), 2)//2
	distance_dict = {}
	for i,gene1 in enumerate(ordered_genes):
		if i == 0:
			continue
		for j,gene2 in enumerate(ordered_genes):
			if i <= j:
				continue
			# i > j OR j < i
			max_node = get_gene_pair_node(answer_code, gene1, gene2)
			distance_index = max_node - 1
			#print(gene1, gene2, distance_index, "j=", j)
			distance_dict[(gene1, gene2)] = distance_list[distance_index]
			distance_dict[(gene2, gene1)] = distance_list[distance_index]
	#makeTable_ascii(ordered_genes, distance_dict)
	return distance_dict

#===========================================
def addDistancePairShifts(distance_dict, ordered_genes, answer_code):
	for i,gene1 in enumerate(ordered_genes):
		for j,gene2 in enumerate(ordered_genes):
			if i == j:
				continue
			for k,gene3 in enumerate(ordered_genes):
				if j == k or i == k:
					continue
				# i > j > k OR k < j < i
				max_node_1_2 = get_gene_pair_node(answer_code, gene1, gene2)
				max_node_2_3 = get_gene_pair_node(answer_code, gene2, gene3)
				max_node_1_3 = get_gene_pair_node(answer_code, gene1, gene3)

				if max_node_2_3 == max_node_1_3 and max_node_1_2 < max_node_1_3:
					# do something
					#print("genes (", gene1, gene2, ")", gene3)
					#print("max_node", max_node_1_2, max_node_2_3, max_node_1_3)
					#print("DO SOMETHING")
					shift = random.randint(-1, 1) * 2
					distance_dict[(gene1, gene3)] += shift
					distance_dict[(gene3, gene1)] += shift
					distance_dict[(gene2, gene3)] -= shift
					distance_dict[(gene3, gene2)] -= shift
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
def makeTable_html(ordered_genes, distance_dict, distance_list):
	sorted_genes = list(copy.copy(ordered_genes))
	sorted_genes.sort()
	td_extra = 'align="center" style="border: 1px solid black; background-color: xxxxxx;"'
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
				my_td_extra = td_extra.replace('xxxxxx', 'gray')
				table += ' <td {0}>&times;</td>'.format(my_td_extra)
			else:
				#gene_sum = ordered_genes.index(g1) + ordered_genes.index(g2)
				gene_tuple  = (g1, g2)
				distance = distance_dict[gene_tuple]
				hex_color = distance_to_html_color(distance, distance_list)
				my_td_extra = td_extra.replace('xxxxxx', hex_color)
				table += ' <td {0}>{1}{2:d}</span></td>'.format(my_td_extra, span, distance)
		table += '</tr>'
	table += '</table>'
	f = open('temp.html', 'w')
	f.write(table)
	f.write(''.join(ordered_genes))
	f.close()
	return table

#===========================================
def getGoodGenePermutation(gene_permutations, ordered_genes, replace_answer_code):
	one_index = replace_answer_code.find('1')
	first_letter = replace_answer_code[one_index-1]
	second_letter = replace_answer_code[one_index+1]
	first_letter_index_pair = (ordered_genes.index(first_letter),  ordered_genes.index(second_letter))
	random.shuffle(gene_permutations)
	for permuted_genes in gene_permutations:
		if permuted_genes.index(first_letter) not in first_letter_index_pair:
			continue
		if permuted_genes.index(second_letter) not in first_letter_index_pair:
			continue
		print("PERMUTE", permuted_genes, ordered_genes, first_letter, second_letter)
		return permuted_genes

#===========================================
def makeQuestion(N, sorted_genes, num_leaves, num_choices):
	genetree = phylolib2.GeneTree()
	distance_list = makeRandDistanceList(num_leaves-1)
	print("distance_list=",distance_list)

	gene_permutations = comb_safe_permutations(sorted_genes)
	#print(gene_permutations)
	random.shuffle(gene_permutations)
	ordered_genes = gene_permutations.pop()
	print('ordered_genes=',ordered_genes)

	all_diff_codes = genetree.get_all_gene_tree_code_for_leaf_count(num_leaves)
	random.shuffle(all_diff_codes)

	answer_code = all_diff_codes.pop()
	answer_code = genetree.get_random_code_permutation(answer_code)
	replace_answer_code = genetree.replace_gene_letters(answer_code, ordered_genes)

	answer_html_choice = genetree.get_html_from_code(replace_answer_code)
	print('replace_answer_code=',replace_answer_code)

	distance_dict = makeDistancePairs(ordered_genes, distance_list, replace_answer_code)
	#print("distance_dict=",distance_dict)
	makeTable_ascii(ordered_genes, distance_dict)
	addDistancePairShifts(distance_dict, ordered_genes, replace_answer_code)
	#print("distance_dict=",distance_dict)
	makeTable_ascii(ordered_genes, distance_dict)

	### MAKE WRONG ANSWERS
	html_choices_list = []
	num_wrong_tree_choices = num_choices//2
	num_permute_tree_choices = num_choices - num_wrong_tree_choices - 1

	wrong_tree_choice_codes_list = all_diff_codes[:num_wrong_tree_choices]
	random.shuffle(wrong_tree_choice_codes_list)
	for wrong_tree_choice_code in wrong_tree_choice_codes_list:
		#print("choice_code=", choice_code)
		wrong_tree_choice_code = genetree.get_random_code_permutation(wrong_tree_choice_code)
		wrong_tree_choice_code = genetree.replace_gene_letters(wrong_tree_choice_code, ordered_genes)
		html_choice = genetree.get_html_from_code(wrong_tree_choice_code)
		html_choices_list.append(html_choice)

	all_permute_codes = genetree.get_all_code_permutations(answer_code)
	all_permute_codes.remove(answer_code)
	wrong_permute_choice_codes_list = all_permute_codes[:num_permute_tree_choices]
	for wrong_permute_choice_code in wrong_permute_choice_codes_list:
		permuted_genes = getGoodGenePermutation(gene_permutations, ordered_genes, replace_answer_code)
		wrong_permute_choice_code = genetree.replace_gene_letters(wrong_permute_choice_code, permuted_genes)
		html_choice = genetree.get_html_from_code(wrong_permute_choice_code)
		html_choices_list.append(html_choice)
		if len(html_choices_list) >= num_choices - 1:
			break

	html_choices_list.append(answer_html_choice)
	random.shuffle(html_choices_list)

	question = ''
	question += makeTable_html(ordered_genes, distance_dict, distance_list)
	question += '<p></p><h6>Given the gene distance matrix table above, '
	question += 'which one of the following gene trees correctly fit the data?</h6>'

	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, answer_html_choice)
	return complete

#===========================================
#===========================================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-l', '--leaves', '--num-leaves', type=int, dest='num_leaves',
		help='number of leaves in gene trees', default=5)
	parser.add_argument('-d', '--duplicate-runs', type=int, dest='duplicate_runs',
		help='number of questions to create', default=24)
	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of choices to choose from in the question', default=5)
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicate_runs):
		sorted_genes = bptools.getGeneLetters(args.num_leaves, i)
		N += 1
		complete_question = makeQuestion(N, sorted_genes, args.num_leaves, args.num_choices)

		f.write(complete_question)
	f.close()
	print("wrote {0} questions to the file {1}".format(N, outfile))
	bptools.print_histogram()

