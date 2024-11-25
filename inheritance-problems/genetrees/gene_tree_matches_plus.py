#!/usr/bin/env python3

import os
import sys
import copy
import time
import random
import argparse

#local
import bptools
import phylolib2

debug = False

### TODO
# get most dissimilar in find SAME for quesiton and answer
# get most dissimilar in find DIFFERENT for quesiton and wrong choices

#=======================
#=======================
def findDifferentQuestion(N, sorted_genes, num_leaves, num_choices):
	""" make a gene tree with N leaves, ask students to find the different one """
	num_nodes = num_leaves - 1
	ordered_genes = copy.copy(sorted_genes)
	random.shuffle(ordered_genes)
	genetree = phylolib2.GeneTree()

	### get all base codes
	all_base_tree_codes = genetree.get_all_gene_tree_codes_for_leaf_count(num_leaves)

	### 1a. pick one random base code
	random.shuffle(all_base_tree_codes)
	match_code = all_base_tree_codes.pop()
	match_profile = genetree.gene_tree_code_to_profile(match_code, num_nodes)
	print("match_code=", match_code, match_profile)
	question_tree_name = genetree.get_tree_name_from_code(match_code)
	print("Gene Tree Name: ", question_tree_name)

	### 1b. replace the gene letters
	replaced_match_code = genetree.replace_gene_letters(match_code, ordered_genes)
	replaced_match_code = genetree.sort_alpha_for_gene_tree(replaced_match_code, num_nodes)
	replaced_match_profile = genetree.gene_tree_code_to_profile(replaced_match_code, num_nodes)
	print("replaced_match_code=", replaced_match_code, replaced_match_profile)
	#replaced_match_code is just used for generation of the other choices


	### 2. now get the most similar to replaced_match_code but DIFFERENT gene tree from the list
	### 2a. groups the unused trees
	profile_groups = genetree.group_gene_trees_by_profile(all_base_tree_codes, num_nodes)
	print(profile_groups.keys())
	### 2b. remove the group of gene trees similar to match
	if profile_groups.get(match_profile) is not None:
		del profile_groups[match_profile]
	### 2c. get the most similar to match_code profile
	sorted_profile_group_keys = genetree.sort_profiles_by_closeness(profile_groups, match_profile)
	most_similar_different_code_list = profile_groups[sorted_profile_group_keys[0]]
	most_similar_different_code = random.choice(most_similar_different_code_list)
	most_similar_different_profile = sorted_profile_group_keys[0]
	print("most_similar_different_code=", most_similar_different_code, most_similar_different_profile)
	### 2d. replace the gene letters
	replaced_most_similar_different_code = genetree.replace_gene_letters(most_similar_different_code, ordered_genes)
	print("replaced_most_similar_different_code=", replaced_most_similar_different_code)
	### 2e. rotate the branches of the tree
	rotated_replaced_most_similar_different_code = genetree.get_random_code_permutation(replaced_most_similar_different_code)
	rotated_replaced_most_similar_different_code = genetree.sort_alpha_for_gene_tree(rotated_replaced_most_similar_different_code, num_nodes)
	rotated_replaced_most_similar_profile = genetree.gene_tree_code_to_profile(rotated_replaced_most_similar_different_code, num_nodes)
	print("rotated_replaced_most_similar_different_code=", rotated_replaced_most_similar_different_code, rotated_replaced_most_similar_profile)
	### 2f. make sure it's different from original gene tree
	if rotated_replaced_most_similar_profile == replaced_match_profile:
		print("ERROR: wrong and correct are the same")
		sys.exit(1)
	### 2g. make sure it's different from original gene tree
	rotated_replaced_most_similar_html_choice = genetree.get_html_from_code(rotated_replaced_most_similar_different_code)

	### 3. now get the all the matches to the replaced_match_code for other SAME choices
	### 3a. get all rotation permutations for replaced_match_code
	choice_codes_list = genetree.get_all_alpha_sorted_code_rotation_permutations(replaced_match_code)
	choice_codes_list.sort()
	if debug is True:
		print("choice_codes_list=", choice_codes_list)
	print("Created {0} rotation permutations for tree with {1} nodes".format(len(choice_codes_list), num_nodes))
	### 3b. pick the gene tree to use in the question
	random.shuffle(choice_codes_list)
	question_code = choice_codes_list.pop()
	question_code = genetree.sort_alpha_for_gene_tree(question_code, num_nodes)
	if question_code in choice_codes_list:
		choice_codes_list.remove(question_code)
	### 3c. produce the html for each choice
	html_choices_list = []
	selected_choice_codes = {}
	random.shuffle(choice_codes_list)
	for choice_code in choice_codes_list:
		## 3c1. make sure the choice is sorted
		sorted_choice_code = genetree.sort_alpha_for_gene_tree(choice_code, num_leaves-1)
		## 3c2. make sure we have not used this choice yet
		if selected_choice_codes.get(sorted_choice_code) is True:
			continue
		selected_choice_codes[sorted_choice_code] = True
		## 3c3. get the profile
		choice_profile = genetree.gene_tree_code_to_profile(sorted_choice_code, num_nodes)
		print("choice_code=", sorted_choice_code, choice_profile)
		## 3c4. make sure it's different from the rotated_replaced_most_similar_profile
		if choice_profile == rotated_replaced_most_similar_profile:
			print("ERROR: what how did we get here?")
			print(choice_profile,' == ',rotated_replaced_most_similar_profile)
			sys.exit(1)
		## 3c5. make sure it's the same as the original
		if choice_profile != replaced_match_profile:
			continue
		## 3c6. make the html
		html_choice = genetree.get_html_from_code(sorted_choice_code)
		html_choices_list.append(html_choice)
		## 3c7. stop when we have enough choices
		if len(html_choices_list) >= num_choices - 1:
			break
	### 3d. check to make sure we got enough choices
	if len(html_choices_list) != num_choices - 1:
		print("WARNING: requested choices were not fulfilled")
		time.sleep(1)
		### some graphs just don't have enough alternate choices
		return None
	### 3e. add the correct choice to the list
	html_choices_list.append(rotated_replaced_most_similar_html_choice)
	random.shuffle(html_choices_list)

	### 3f. debug if necessary
	if debug is True:
		f = open("temp.html", "w")
		for html_choice in html_choices_list:
			f.write(html_choice)
		f.close()

	### 4a. write the question text
	question = '<p>The tree below Dr. Voss affectionately calls: {0}</p>'.format(question_tree_name)
	question += genetree.get_html_from_code(question_code)
	question += '<p></p><h6>All but one of the gene trees below are the same as the gene tree above.</h6>'
	question += '<h6>Which one of the following represents a '
	question += '<span style="color: #ba372a;"><strong>DIFFERENT</strong></span> gene tree?</h6>'
	### 4b. format the question
	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, rotated_replaced_most_similar_html_choice)

	print("findDifferentQuestion() is complete for {0} leaves and {1} choices".format(num_leaves, num_choices))
	return complete

#=======================
#=======================
def findSameQuestion(N, sorted_genes, num_leaves, num_choices):
	""" make a gene tree with N leaves, ask students to find the same one among other wrong ones"""
	### 0. setup variables
	num_nodes = num_leaves - 1
	ordered_genes = copy.copy(sorted_genes)
	random.shuffle(ordered_genes)
	genetree = phylolib2.GeneTree()
	
	### 1. get all possible gene base codes
	all_diff_codes = genetree.get_all_gene_tree_codes_for_leaf_count(num_leaves)
	random.shuffle(all_diff_codes)

	### 2. select a gene tree, for matching
	raw_code = all_diff_codes.pop()
	raw_profile = genetree.gene_tree_code_to_profile(raw_code, num_nodes)
	print("raw_code=", raw_code, raw_profile)
	question_tree_name = genetree.get_tree_name_from_code(raw_code)

	### 3. rotation permute the raw code to get the answer gene tree
	answer_code = genetree.get_random_code_permutation(raw_code)
	answer_code = genetree.replace_gene_letters(answer_code, ordered_genes)
	answer_code = genetree.sort_alpha_for_gene_tree(answer_code, num_nodes)
	answer_profile = genetree.gene_tree_code_to_profile(answer_code, num_nodes)
	print("answer_code=", answer_code, answer_profile)

	### 4a. selected a different rotation permutation of the raw code for the question text
	question_code = answer_code
	while question_code == answer_code:
		question_code = genetree.get_random_code_permutation(raw_code)
		question_code = genetree.replace_gene_letters(question_code, ordered_genes)
		question_code = genetree.sort_alpha_for_gene_tree(question_code, num_leaves-1)
	question_profile = genetree.gene_tree_code_to_profile(question_code, num_nodes)
	print("question_code=", question_code, question_profile)
	### 4b. double check answer and question are same tree
	if answer_profile != question_profile:
		print("ERROR: answer and question have different profiles")
		sys.exit(1)

	### 5. take all the unused trees and create the incorrect choices
	### 5a. sort the unused trees into profile groups
	profile_groups = genetree.group_gene_trees_by_profile(all_diff_codes, num_nodes)
	#print("profile_groups.keys()=", profile_groups.keys())
	### 5b. double-check and remove if necessary the profile group of the answer
	if profile_groups.get(raw_profile) is not None:
		del profile_groups[raw_profile]
	### 5c. sort the remaining profile groups by how similar they are to the answer
	sorted_profile_group_keys = genetree.sort_profiles_by_closeness(profile_groups, raw_profile)

	html_choices_list = []
	print("best sorted profile keys=", sorted_profile_group_keys[:num_choices - 1])
	### 5d. convert each tree type into an incorrect choice
	for key in sorted_profile_group_keys:
		### 5d1. get the list of codes for this profile
		profile_code_list = profile_groups[key]
		### 5d2. randomly select one of the codes
		choice_code = random.choice(profile_code_list)
		### 5d3. replace the gene letters
		choice_code = genetree.replace_gene_letters(choice_code, ordered_genes)
		### 5d4. make sure the tree is alpha sorted
		choice_code = genetree.sort_alpha_for_gene_tree(choice_code, num_leaves-1)
		### 5d5. double-check that the profile does not match the answer
		choice_profile = genetree.gene_tree_code_to_profile(choice_code, num_nodes)
		if choice_profile == answer_profile or choice_profile == question_profile:
			continue
		print("choice_code=", choice_code, choice_profile)
		### 5d6. convert the gene tree to html
		html_choice = genetree.get_html_from_code(choice_code)
		### 5d7. add html to growing list
		html_choices_list.append(html_choice)
		### 5d8. stop when we have enough 
		if len(html_choices_list) >= num_choices - 1:
			break

	### 6a. check to make sure we got enough choices
	if len(html_choices_list) != num_choices - 1:
		print("WARNING: requested choices were not fulfilled")
		time.sleep(1)
		return None

	### 6b. add the correct choice to the list
	answer_html_choice = genetree.get_html_from_code(answer_code)
	html_choices_list.append(answer_html_choice)
	random.shuffle(html_choices_list)

	### 6c. debug if necessary
	if debug is True:
		f = open("temp.html", "w")
		for html_choice in html_choices_list:
			f.write(html_choice)
		f.close()

	### 7a. write question text
	question = '<p>The tree below is a {0} leaf gene tree, Dr. Voss affectionatly calls this tree "{1}"</p>'.format(num_leaves, question_tree_name)
	question += genetree.get_html_from_code(question_code)
	question += '<p></p><h6>Several gene trees are shown below, but only one is the same as the one above.</h6>'
	question += '<h6>Which one of the following represents or is equivalent to the '
	question += '<span style="color: #169179;"><strong>SAME</strong></span> gene tree?</h6>'
	### 7b. format the question
	complete = bptools.formatBB_MC_Question(N, question, html_choices_list, answer_html_choice)

	print("findSameQuestion() is complete for {0} leaves and {1} choices".format(num_leaves, num_choices))
	return complete

#===========================================
#===========================================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-l', '--leaves', '--num-leaves', type=int, dest='num_leaves',
		help='number of leaves in gene trees', default=9)
	parser.add_argument('-q', '--num-questions', type=int, dest='num_questions',
		help='number of questions to create', default=24)
	parser.add_argument('-s', '--style', type=str, dest='style', choices=['same', 'different',],
		help='matching questions style, find same or find different', required=True)
	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of choices to choose from in the question', default=5)
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 1
	errors = 0
	while N <= args.num_questions:
		if errors > N > 5:
			print("TOO MANY ERRORS, QUITTING")
			sys.exit(1)
		sorted_genes = bptools.generate_gene_letters(args.num_leaves)
		if args.style == 'same':
			complete_question = findSameQuestion(N, sorted_genes, args.num_leaves, args.num_choices)
		elif args.style == 'different':
			complete_question = findDifferentQuestion(N, sorted_genes, args.num_leaves, args.num_choices)
		else:
			print("ERROR")
			sys.exit(1)
		if complete_question is None:
			errors += 1
			continue

		f.write(complete_question)
		N += 1
	f.close()
	print("wrote {0} questions to the file {1}".format(N, outfile))
	bptools.print_histogram()
