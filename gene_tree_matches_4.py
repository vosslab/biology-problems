#!/usr/bin/env python

import random
import phylolib


# make a gene tree with 3 leaves, ask students to find the similar one

def makeQuestion(version):
	if version % 3 == 0:
		genes = [g[0],g[1],g[2]]
		others = [[g[0],g[2],g[1]], [g[1],g[2],g[0]],]
	elif version % 3 == 1:
		genes = [g[0],g[2],g[1]]
		others = [[g[0],g[1],g[2]], [g[1],g[2],g[0]],]
	elif version % 3 == 2:
		genes = [g[1],g[2],g[0]]
		others = [[g[0],g[1],g[2]], [g[0],g[2],g[1]],]
	if version // 3 == 0:
		answer = phylolib.comb_tree_3_leaves_html(genes)
		question = phylolib.comb_tree_3_leaves_type_2_html(genes)
	else:
		question = phylolib.comb_tree_3_leaves_html(genes)
		answer = phylolib.comb_tree_3_leaves_type_2_html(genes)

	wrongs = []
	for oth in others:
		w1 = phylolib.comb_tree_3_leaves_html(oth)
		wrongs.append(w1)
		w2 = phylolib.comb_tree_3_leaves_type_2_html(oth)
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
	lowercase = "abcdefghijklmnopqrstuvwxyz"

	filename = "bbq-which_gene_tree_matches_3.txt"
	f = open(filename, "w")
	duplicates = 16
	j = -1
	for i in range(duplicates):
		j += 1
		if j + 3 == 26:
			j = 0
		basetype = lowercase[j:j+3]
		g = list(basetype)
		for version in range(6):
			complete_question = makeQuestion(version)
			f.write(complete_question)
	f.close()
