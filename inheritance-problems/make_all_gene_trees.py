#!/usr/bin/env python

import os
import sys
import copy
import math
import time
import random
import argparse
import colorsys
import itertools

#local
import bptools
import phylolib2

# make a gene tree table with 4 leaves, ask students to choose correct one

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
def all_permutations(genes):
	complete_set = itertools.permutations(genes, len(genes))
	complete_set = list(complete_set)
	return complete_set

#===========================================
def gene_tree_code_to_profile(code, num_nodes):
	code_dict = {}
	for i in range(num_nodes):
		node_num = i + 1
		node_index = code.find(str(node_num))
		if code[node_index-1].isalpha():
			code_dict[node_num] = code_dict.get(node_num, []) + [code[node_index-1],]
		if code[node_index+1].isalpha():
			code_dict[node_num] = code_dict.get(node_num, []) + [code[node_index+1],]
	#print(code, code_dict)
	profile = ""
	keys = list(code_dict.keys())
	keys.sort()
	for key in keys:
		profile += str(key)
		values = code_dict[key]
		values.sort()
		profile += ''.join(values)
	#print(code, profile)
	return profile

#===========================================
def group_gene_trees(gene_tree_codes, num_nodes):
	gene_tree_groups = {}
	for code in gene_tree_codes:
		profile = gene_tree_code_to_profile(code, num_nodes)
		gene_tree_groups[profile] = gene_tree_groups.get(profile, []) + [code,]
	print("Number of groups {0}".format(len(gene_tree_groups)))
	#import pprint
	#pprint.pprint(gene_tree_groups)
	return gene_tree_groups

#===========================================
def is_gene_tree_alpha_sorted(code, num_nodes):
	code_dict = {}
	for i in range(num_nodes):
		node_num = i + 1
		node_index = code.find(str(node_num))
		char1 = code[node_index-1]
		if not char1.isalpha():
			continue
		char2 = code[node_index+1]
		if not char2.isalpha():
			continue
		if char1 > char2:
			return False
	return True
		


#===========================================
def makeQuestion(N, sorted_genes, num_leaves):
	t0 = time.time()
	genetree = phylolib2.GeneTree()
	num_nodes = num_leaves - 1
	code_choice_list = genetree.make_all_gene_trees_for_leaf_count(num_leaves)

	code_choice_list.sort()
	print("code_choice_list: prelen=", prelen, "postlen=", postlen)

	gene_tree_profile_groups = genetree.group_gene_trees_by_profile(code_choice_list, num_nodes)

	### FILTER ANSWERS


	group_names = list(gene_tree_profile_groups.keys())
	group_names.sort()
	if len(group_names) < 15:
		print(group_names)
	"""
	f = open('temp.html', 'w')
	for i, profile in enumerate(group_names):
		codes = gene_tree_groups[profile]
		f.write('<h1>{0}. {1} &mdash; {2} trees</h1>'.format(i+1, profile, len(codes)))
		codes.sort()
		count = 0
		for code in codes:
			#gene_tree_code_to_profile(code_choice, num_leaves-1)
			html_choice = genetree.get_html_from_code(code)
			#html_choices_list.append(html_choice)
			f.write(html_choice+'<br/>')
			count += 1
			if count >= 5:
				break
	f.close()
	"""
	return ''

#===========================================
#===========================================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-l', '--leaves', '--num-leaves', type=int, dest='num_leaves',
		help='number of leaves in gene trees', default=5)
	parser.add_argument('-d', '--duplicate-runs', type=int, dest='duplicate_runs',
		help='number of questions to create', default=1)
	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of choices to choose from in the question', default=5)
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicate_runs):
		sorted_genes = bptools.getGeneLetters(args.num_leaves, 0)
		N += 1
		complete_question = makeQuestion(N, sorted_genes, args.num_leaves)

		f.write(complete_question)
	f.close()
	print("wrote {0} questions to the file {1}".format(N, outfile))
	bptools.print_histogram()

