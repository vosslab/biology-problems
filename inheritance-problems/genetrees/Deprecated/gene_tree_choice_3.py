#!/usr/bin/env python3

import os
import sys
import copy
import math
import random
import argparse

import bptools
from classic_phylolib import phylolib

# make a gene tree with 3 leaves, ask students to find the similar one

#======================================
#======================================
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

#======================================
#======================================
def makeDistances_Comb(ordered_genes):
	# A-1-B -2-C -3-D
	distance_dict = {}
	num_distances = math.comb(len(ordered_genes), 2)
	distances = makeRandDistanceList(num_distances)
	#print("distances=",distances)
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
	#makeTable_ascii(ordered_genes, distance_dict)
	return distance_dict

#======================================
#======================================
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

#======================================
#======================================
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

#======================================
#======================================
def make_question(N, gene_letters_str):
	#print(f"gene_letters_str = {gene_letters_str}")
	gene_letters_list = sorted(gene_letters_str)
	permutated_letters_list = phylolib.comb_safe_permutations(gene_letters_list)
	index = N % len(gene_letters_list)
	correct_order_genes = permutated_letters_list.pop(index)

	alt_answer1 = phylolib.comb_tree_3_leaves_html(correct_order_genes)
	alt_answer2 = phylolib.comb_tree_3_leaves_alternate_html(correct_order_genes)
	answer = random.choice([alt_answer1, alt_answer2])

	wrongs = []
	for other_tree in permutated_letters_list:
		w1 = phylolib.comb_tree_3_leaves_html(other_tree)
		wrongs.append(w1)
		w2 = phylolib.comb_tree_3_leaves_alternate_html(other_tree)
		wrongs.append(w2)

	w3 = phylolib.balanced_tree_3_leaves_html(correct_order_genes)
	wrongs.append(w3)

	choices = set(wrongs)
	choices.discard(alt_answer1)
	choices.discard(alt_answer2)
	choices = list(choices)
	choices.append(answer)
	random.shuffle(choices)

	distance_dict = makeDistances_Comb(correct_order_genes)
	distance_table = makeTable_html(correct_order_genes, distance_dict)

	# Add the descriptive question statement
	g1 = gene_letters_list[0]
	g2 = gene_letters_list[1]
	g3 = gene_letters_list[2]
	problem_statement = (
		"<p>The table above represents a distance matrix for the following genes: "
		f"{', '.join(f'<b>{gene.upper()}</b>' for gene in gene_letters_list)}. "
		"The values in the matrix correspond to the genetic distances "
		"between pairs of genes.</p> "
		"<p>For example, "
		f"{gene_text(g1, g2, distance_dict)}, while "
		f"{gene_text(g1, g3, distance_dict)}. "
		"Distances are symmetric, meaning that both "
		f"{gene_text(g2, g3, distance_dict)} and "
		f"{gene_text(g3, g2, distance_dict)}.</p>"
		"<h6>Using this distance matrix, determine the most appropriate gene tree that "
		"accurately reflects the relationships and distances between these genes.</h6>"
	)
	# Format and return the complete question
	full_question = distance_table + problem_statement
	complete_question = bptools.formatBB_MC_Question(N, full_question, choices, answer)
	return complete_question

#======================================
#======================================
def gene_text(gene1, gene2, distance_dict):
	gene_string = (
		f"the distance between gene <b>{gene1.upper()}</b> and "
		f"gene <b>{gene2.upper()}</b> is "
		f"<b>{distance_dict[(gene1, gene2)]}</b>"
	)
	return gene_string


#======================================
#======================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create', default=1
	)

	parser.add_argument(
		'-c', '--num_choices', type=int, default=5,
		help="Number of choices to create."
	)

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	# Parse arguments from the command line
	args = parse_arguments()

	# Define output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq' +
		'-' + script_name +
		'-questions.txt'
		)
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			gene_letters_str = bptools.generate_gene_letters(3, clear=True)
			complete_question = make_question(N, gene_letters_str)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	bptools.print_histogram()
	print(f"{N} questions were written to file {outfile}")

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
