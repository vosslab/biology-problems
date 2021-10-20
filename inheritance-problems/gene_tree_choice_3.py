#!/usr/bin/env python

import copy
import random
import phylolib

# make a gene tree with 3 leaves, ask students to find the similar one

def makeTable(genes):
	distances = []
	while len(distances) < len(genes)-1:
		r = random.randint(4,10)
		if not r in distances:
			distances.append(r)
	distances.sort()
	#distances[0] //= 2
	distances[1] *= 2
	distances.reverse()
	distances.append(distances[0] + 1)
	sorted_genes = list(copy.copy(genes))
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
				gene_sum = genes.index(g1) + genes.index(g2)
				d = distances[gene_sum-1]
				table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra, span, d)
		table += '</tr>'
	table += '</table>'
	return table


def makeQuestion(sorted_genes, version):
	perms = phylolib.comb_safe_permutations(sorted_genes)
	index = version % len(sorted_genes)
	genes = perms.pop(index)
	#print(genes)
	#print(perms)
	if version // len(sorted_genes) == 0:
		answer = phylolib.comb_tree_3_leaves_html(genes)
		#answer += phylolib.comb_tree_3_leaves_alternate_html(genes)
	else:
		answer = phylolib.comb_tree_3_leaves_alternate_html(genes)
		#answer += phylolib.comb_tree_3_leaves_html(genes)

	wrongs = []
	for oth in perms:
		if random.random() < 0.5:
			w1 = phylolib.comb_tree_3_leaves_html(oth)
			#w1 += phylolib.comb_tree_3_leaves_alternate_html(oth)
			wrongs.append(w1)
		else:
			w2 = phylolib.comb_tree_3_leaves_alternate_html(oth)
			#w2 += phylolib.comb_tree_3_leaves_html(oth)
			wrongs.append(w2)
	sorted_genes = list(copy.copy(genes))
	sorted_genes.sort()
	w3 = phylolib.balanced_tree_3_leaves_html(sorted_genes)
	wrongs.append(w3)

	choices = wrongs
	choices.append(answer)
	random.shuffle(choices)

	question = ''
	question += makeTable(genes)
	question += '<p></p><h6>Given the table above, which one of the following gene trees best fit the distance matrix data?</h6>'
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

	filename = "bbq-gene_tree_choice_3.txt"
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
