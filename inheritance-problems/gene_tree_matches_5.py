#!/usr/bin/env python

import os
import sys
import random

import bptools
from classic_phylolib import phylolib


# make a gene tree with 4 leaves, ask students to find the similar one

def makeQuestion(N, sorted_genes):
	perms = phylolib.comb_safe_permutations(sorted_genes)
	index = N % len(sorted_genes)
	ordered_genes = perms.pop(index)
	opposite_genes = (ordered_genes[0], ordered_genes[1], ordered_genes[3], ordered_genes[2], ordered_genes[4])
	print("ordered_genes=", ordered_genes)

	question = phylolib.random_balanced_tree_5_leaves_type_1_html(ordered_genes)
	answer = question
	while answer == question:
		answer = phylolib.random_balanced_tree_5_leaves_type_1_html(ordered_genes)

	wrongs = []
	random.shuffle(perms)
	for i in range(6):
		#sys.stderr.write(".")
		other_permuation = perms[i]
		wrong_tree = phylolib.random_tree_5_leaves_html(other_permuation)
		wrongs.append(wrong_tree)
	opposite = phylolib.random_balanced_tree_5_leaves_type_1_html(opposite_genes)

	choices = wrongs
	choices.append(answer)
	choices.append(opposite)
	random.shuffle(choices)

	question += '<p>Given the gene tree above, which one of the following gene trees below represent the same gene tree relationships?</p>'

	complete = bptools.formatBB_MC_Question(N, question, choices, answer)
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
		if j + 4 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+5]
		sorted_genes = list(basetype)
		N += 1
		complete_question = makeQuestion(N, sorted_genes)
		f.write(complete_question)
	f.close()
