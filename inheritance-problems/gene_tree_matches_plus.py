#!/usr/bin/env python

import os
import copy
import random
import argparse

#local
import bptools
import phylolib2



#=======================
#=======================
def findDifferentQuestion(N, sorted_genes, num_leaves, num_choices):
	""" make a gene tree with N leaves, ask students to find the different one """
	num_nodes = num_leaves - 1
	ordered_genes = copy.copy(sorted_genes)
	random.shuffle(ordered_genes)
	#^^ this does not work for the substitution

	genetree = phylolib2.GeneTree()
	all_base_tree_codes = genetree.get_all_gene_tree_codes_for_leaf_count(num_leaves)
	random.shuffle(all_base_tree_codes)
	match_code = all_base_tree_codes.pop()
	match_profile = genetree.gene_tree_code_to_profile(match_code, num_nodes)
	print("match_code=", match_code, match_profile)

	replaced_match_code = genetree.replace_gene_letters(match_code, ordered_genes)
	replaced_match_profile = genetree.gene_tree_code_to_profile(replaced_match_code, num_nodes)
	print("replaced_match_code=", replaced_match_code, replaced_match_profile)

	profile_groups = genetree.group_gene_trees_by_profile(all_base_tree_codes, num_nodes)
	print(profile_groups.keys())
	if profile_groups.get(match_profile) is not None:
		del profile_groups[match_profile]	
	sorted_profile_group_keys = genetree.sort_profiles_by_closeness(profile_groups, match_profile)
	not_same_code = random.choice(profile_groups[sorted_profile_group_keys[0]])
	print("not_same_code=", not_same_code, sorted_profile_group_keys[0])
	replaced_not_same_code = genetree.replace_gene_letters(not_same_code, ordered_genes)
	print("replaced_not_same_code=", replaced_not_same_code)
	rotated_replaced_not_same_code = genetree.get_random_code_permutation(replaced_not_same_code)
	print("rotated_replaced_not_same_code=", rotated_replaced_not_same_code)
	not_same_html_choice = genetree.get_html_from_code(rotated_replaced_not_same_code)
	not_same_profile = genetree.gene_tree_code_to_profile(rotated_replaced_not_same_code, num_nodes)
	print("not_same_profile=", not_same_profile)

	all_codes_list = genetree.get_all_code_permutations(replaced_match_code)
	print(all_codes_list)
	random.shuffle(all_codes_list)
	question_code = all_codes_list.pop()
	question_tree_name = genetree.get_tree_name_from_code(match_code)

	choice_codes_list = all_codes_list[:num_choices-1]
	random.shuffle(choice_codes_list)
	html_choices_list = []
	for choice_code in choice_codes_list:
		choice_profile = genetree.gene_tree_code_to_profile(choice_code, num_nodes)
		if choice_profile == not_same_profile:
			continue
		if choice_profile != replaced_match_profile:
			continue
		print("choice_code=", choice_code, choice_profile)
		html_choice = genetree.get_html_from_code(choice_code)
		html_choices_list.append(html_choice)
		if len(html_choices_list) > num_choices - 1:
			break
	html_choices_list.append(not_same_html_choice)
	random.shuffle(html_choices_list)

	f = open("temp.html", "w")
	for html_choice in html_choices_list:
		f.write(html_choice)
	f.close()

	question = '<p>The tree below Dr. Voss affectionately calls: {0}</p>'.format(question_tree_name)
	question += genetree.get_html_from_code(question_code)
	question += '<p></p><h6>All but one of the gene trees below are the same as the gene tree above.</h6>'
	question += '<h6>Which one of the following represents a <strong>different</strong> gene tree?</h6>'
	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, not_same_html_choice)

	return complete

#=======================
#=======================
def findSameQuestion(N, sorted_genes, num_leaves, num_choices):
	""" make a gene tree with N leaves, ask students to find the same one """
	num_nodes = num_leaves - 1
	ordered_genes = copy.copy(sorted_genes)
	random.shuffle(ordered_genes)
	
	genetree = phylolib2.GeneTree()
	all_diff_codes = genetree.get_all_gene_tree_codes_for_leaf_count(num_leaves)
	random.shuffle(all_diff_codes)

	raw_code = all_diff_codes.pop()
	raw_profile = genetree.gene_tree_code_to_profile(raw_code, num_nodes)
	print("raw_code=", raw_code, raw_profile)
	question_tree_name = genetree.get_tree_name_from_code(raw_code)
	answer_code = genetree.get_random_code_permutation(raw_code)
	answer_code = genetree.replace_gene_letters(answer_code, ordered_genes)
	answer_profile = genetree.gene_tree_code_to_profile(answer_code, num_nodes)
	print("answer_code=", answer_code, answer_profile)
	question_code = answer_code
	while question_code == answer_code:
		question_code = genetree.get_random_code_permutation(raw_code)
		question_code = genetree.replace_gene_letters(question_code, ordered_genes)
	question_profile = genetree.gene_tree_code_to_profile(question_code, num_nodes)
	print("question_code=", question_code, question_profile)
	if answer_profile != question_profile:
		print("ERROR: answer and question have different profiles")

	profile_groups = genetree.group_gene_trees_by_profile(all_diff_codes, num_nodes)
	print(profile_groups.keys())
	if profile_groups.get(raw_profile) is not None:
		del profile_groups[raw_profile]	
	sorted_profile_group_keys = genetree.sort_profiles_by_closeness(profile_groups, raw_profile)

	html_choices_list = []
	print("sorted profiles=", sorted_profile_group_keys[:6])
	for key in sorted_profile_group_keys:
		profile_code_list = profile_groups[key]
		choice_code = random.choice(profile_code_list)
		choice_code = genetree.replace_gene_letters(choice_code, ordered_genes)
		choice_profile = genetree.gene_tree_code_to_profile(choice_code, num_nodes)
		if choice_profile == answer_profile or choice_profile == answer_profile:
			continue
		print("choice_code=", choice_code, choice_profile)
		html_choice = genetree.get_html_from_code(choice_code)
		html_choices_list.append(html_choice)
		if len(html_choices_list) >= num_choices - 1:
			break
	answer_html_choice = genetree.get_html_from_code(answer_code)
	html_choices_list.append(answer_html_choice)
	random.shuffle(html_choices_list)

	f = open("temp.html", "w")
	for html_choice in html_choices_list:
		f.write(html_choice)
	f.close()

	question = '<p>The tree below is a {0} leaf gene tree, Dr. Voss affectionatly calls this tree "{1}"</p>'.format(num_leaves, question_tree_name)
	question += genetree.get_html_from_code(question_code)
	question += '<p></p><h6>Several gene trees are shown below, but only one is the same as the one above.</h6>'
	question += '<h6>Which one of the following represents a <strong>same</strong> gene tree?</h6>'
	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, answer_html_choice)

	return complete


#===========================================
#===========================================
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
		sorted_genes = bptools.getGeneLetters(args.num_leaves, i)
		N += 1
		#complete_question = findSameQuestion(N, sorted_genes, args.num_leaves, args.num_choices)
		complete_question = findDifferentQuestion(N, sorted_genes, args.num_leaves, args.num_choices)

		f.write(complete_question)
	f.close()
	print("wrote {0} questions to the file {1}".format(N, outfile))
	bptools.print_histogram()
