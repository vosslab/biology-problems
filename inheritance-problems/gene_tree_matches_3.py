#!/usr/bin/env python

import random
import phylolib

# make a gene tree with 3 leaves, ask students to find the similar one

def makeQuestion(sorted_genes, version):
	perms = phylolib.comb_safe_permutations(sorted_genes)
	index = version % len(sorted_genes)
	genes = perms.pop(index)
	print(genes)
	if version // len(sorted_genes) == 0:
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
	return complete


if __name__ == "__main__":
	lowercase = "abcdefghjkmnpqrstuwxyz"

	filename = "bbq-gene_tree_matches_3.txt"
	f = open(filename, "w")
	duplicates = 16
	j = -1
	for i in range(duplicates):
		j += 1
		if j + 3 == len(lowercase):
			j = 0
		basetype = lowercase[j:j+3]
		g = list(basetype)
		for version in range(6):
			complete_question = makeQuestion(g, version)
			f.write(complete_question)
	f.close()
