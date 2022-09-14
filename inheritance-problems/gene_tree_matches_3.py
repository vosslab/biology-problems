#!/usr/bin/env python3

import os
import random

import bptools
from classic_phylolib import phylolib

# make a gene tree with 3 leaves, ask students to find the similar one

def makeQuestion(N, sorted_genes):
	perms = phylolib.comb_safe_permutations(sorted_genes)
	index = N % len(sorted_genes)
	genes = perms.pop(index)
	print(genes)
	if random.random() < 0.5:
		answer = phylolib.comb_tree_3_leaves_html(genes)
		question = phylolib.comb_tree_3_leaves_alternate_html(genes)
	else:
		question = phylolib.comb_tree_3_leaves_html(genes)
		answer = phylolib.comb_tree_3_leaves_alternate_html(genes)

	wrongs = []
	for oth in perms:
		w1 = phylolib.comb_tree_3_leaves_html(oth)
		wrongs.append(w1)
		w2 = phylolib.comb_tree_3_leaves_alternate_html(oth)
		wrongs.append(w2)

	w3 = phylolib.balanced_tree_3_leaves_html(genes)
	wrongs.append(w3)
	w3 = phylolib.balanced_tree_3_leaves_html(genes[::-1])
	wrongs.append(w3)

	choices = wrongs
	choices.append(answer)
	random.shuffle(choices)

	question += '<p>Given the gene tree above, which one of the following represents the same gene tree?</p>'
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
		if j + 2 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+3]
		sorted_genes = list(basetype)
		N += 1
		complete_question = makeQuestion(N, sorted_genes)
		f.write(complete_question)
	f.close()
