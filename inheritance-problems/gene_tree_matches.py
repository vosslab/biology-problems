#!/usr/bin/env python

import os
import random
import argparse

#local
import bptools
import phylolib2



#=======================
#=======================
def makeDifferentQuestion(N, sorted_genes, num_leaves, num_choices):
	""" make a gene tree with N leaves, ask students to find the different one """
	genetree = phylolib2.GeneTree()
	match_code = genetree.get_random_gene_tree_code(num_leaves)

	not_code = match_code
	while match_code == not_code:
		not_code = genetree.get_random_gene_tree_code_for_leaf_count(num_leaves)
	answer_code = genetree.get_random_code_permutation(not_code)
	answer_html_choice = genetree.get_html_from_code(answer_code)
	#print("answer_code=", answer_code)

	all_codes_list = genetree.get_all_code_permutations(match_code)
	random.shuffle(all_codes_list)
	question_code = all_codes_list.pop()
	question_tree_name = genetree.get_tree_name_from_code(match_code)

	choice_codes_list = all_codes_list[:num_choices]
	random.shuffle(choice_codes_list)
	html_choices_list = []
	for choice_code in choice_codes_list:
		#print("choice_code=", choice_code)
		html_choice = genetree.get_html_from_code(choice_code)
		html_choices_list.append(html_choice)
	html_choices_list.append(answer_html_choice)
	random.shuffle(html_choices_list)

	#f = open("temp.html", "w")
	#for html_choice in html_choices_list:
	#	f.write(html_choice)
	#f.close()

	question = '<p>The tree below Dr. Voss affectionatly calls: {0}</p>'.format(question_tree_name)
	question += genetree.get_html_from_code(question_code)
	question += '<p>All but one of the gene trees below are the same as the gene tree above.</p>'
	question += '<p>Which one of the following represents a <strong>different</strong> gene tree?</p>'
	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, answer_html_choice)

	return complete

#=======================
#=======================
def makeSameQuestion(N, sorted_genes, num_leaves, num_choices):
	""" make a gene tree with N leaves, ask students to find the same one """
	genetree = phylolib2.GeneTree()
	all_diff_codes = genetree.get_all_gene_tree_code_for_leaf_count(num_leaves)
	random.shuffle(all_diff_codes)

	raw_code = all_diff_codes.pop()
	question_tree_name = genetree.get_tree_name_from_code(raw_code)
	answer_code = genetree.get_random_code_permutation(raw_code)
	question_code = answer_code
	while question_code == answer_code:
		question_code = genetree.get_random_code_permutation(raw_code)	
	answer_html_choice = genetree.get_html_from_code(answer_code)

	#print("answer_code=", answer_code)

	random.shuffle(all_diff_codes)
	choice_codes_list = all_diff_codes[:num_choices]
	random.shuffle(choice_codes_list)
	html_choices_list = []
	for choice_code in choice_codes_list:
		#print("choice_code=", choice_code)
		html_choice = genetree.get_html_from_code(choice_code)
		html_choices_list.append(html_choice)
	html_choices_list.append(answer_html_choice)
	random.shuffle(html_choices_list)

	f = open("temp.html", "w")
	for html_choice in html_choices_list:
		f.write(html_choice)
	f.close()

	question = '<p>The tree below Dr. Voss affectionatly calls: {0}</p>'.format(question_tree_name)
	question += genetree.get_html_from_code(question_code)
	question += '<p>All but one of the gene trees below are the same as the gene tree above.</p>'
	question += '<p>Which one of the following represents a <strong>different</strong> gene tree?</p>'
	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, answer_html_choice)

	return complete


#=======================
#=======================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-l', '--leaves', '--num-leaves', type=int, dest='num_leaves',
		help='number of leaves in gene trees', default=9)
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
		sorted_genes = bptools.getGeneLetters(3, i)
		print(sorted_genes)
		N += 1
		#complete_question = makeDifferentQuestion(N, sorted_genes, args.num_leaves, args.num_choices)
		complete_question = makeSameQuestion(N, sorted_genes, args.num_leaves, args.num_choices)

		f.write(complete_question)
	f.close()
	print("wrote {0} questions to the file {1}".format(N, outfile))
