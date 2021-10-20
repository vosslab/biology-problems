#!/usr/bin/env python

import sys
import random
import phylolib
import itertools

# make a gene tree with 4 leaves, ask students to find the similar one

def makeQuestion(sorted_genes, version):
	perms = phylolib.comb_safe_permutations(sorted_genes)
	index = version % len(sorted_genes)
	genes = perms.pop(index)
	print(genes)
	if version // len(sorted_genes) == 0:
		answer = phylolib.comb_tree_4_leaves_html(genes)
		question = phylolib.comb_tree_4_leaves_alternate_html(genes)
	else:
		question = phylolib.comb_tree_4_leaves_html(genes)
		answer = phylolib.comb_tree_4_leaves_alternate_html(genes)

	wrongs = []
	random.shuffle(perms)
	for i in range(4):
		oth = perms[i]
		a = random.randint(1,3)
		if a == 1:
			w = phylolib.comb_tree_4_leaves_html(oth)
		elif a == 2:
			w = phylolib.comb_tree_4_leaves_alternate_html(oth)
		else:
			w = phylolib.balanced_tree_4_leaves_html(oth)
		wrongs.append(w)

	choices = wrongs
	choices.append(answer)
	random.shuffle(choices)

	question += '<p>Given the gene tree above, which one of the following represents the same gene tree?</p>'
	complete = 'MC\t'
	complete += question
	for c in choices:
		complete += '\t'+c
		if c == answer:
			complete += "\tCorrect"
		else:
			complete += "\tIncorrect"
	complete += '\n'
	#print(complete)
	return complete


if __name__ == "__main__":
	lowercase = "abcdefghjkmnpqrstuwxyz"

	filename = "bbq-gene_tree_matches_4.txt"
	f = open(filename, "w")
	duplicates = 4
	j = -1
	for i in range(duplicates):
		j += 1
		if j + 3 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+4]
		sorted_genes = list(basetype)
		for version in range(24):
			complete_question = makeQuestion(sorted_genes, version)
			f.write(complete_question)
	f.close()
