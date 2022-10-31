#!/usr/bin/env python3

"""
This program creates all permutations of matching pairs

MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
"""

import os
import sys
import pprint
import random
import argparse
import itertools

import bptools

#=======================
#=======================

base_replacement_rule_dict = {
	' not ': ' <strong>NOT</strong> ', #BOLD BLACK
	' Not ': ' <strong>NOT</strong> ', #BOLD BLACK
	' NOT ': ' <strong>NOT</strong> ', #BOLD BLACK
	' false ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' False ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' FALSE ': ' <span style="color: #ba372a;"><strong>FALSE</strong></span> ', #BOLD RED
	' true ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	' True ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	' TRUE ': ' <span style="color: #169179;"><strong>TRUE</strong></span> ', #BOLD GREEN
	'  ': ' ',
}

#=======================
def applyReplacementRulesToQuestions(list_of_question_text, replacement_rule_dict):
	if replacement_rule_dict is None:
		print("no replacement rules found")
		replacement_rule_dict = base_replacement_rule_dict
	else:
		replacement_rule_dict = {**base_replacement_rule_dict, **replacement_rule_dict}
	new_list_of_question_text = []
	for question_text in list_of_question_text:
		for find_text,replace_text in replacement_rule_dict.items():
			question_text = question_text.replace(find_text,replace_text)
		new_list_of_question_text.append(question_text)
	return new_list_of_question_text

#=======================
def makeQuestions(yaml_data, num_choices=None):
	matching_pairs_dict = yaml_data['matching pairs']
	exclude_pairs_list = yaml_data.get('exclude pairs', [])

	list_of_complete_questions = []

	if num_choices is None:
		num_choices = yaml_data.get('items to match per question', 5)

	all_keys = list(matching_pairs_dict.keys())
	all_combs = list(itertools.combinations(all_keys, num_choices))
	print('Created {0} combinations from {1} items'.format(len(all_combs), len(all_keys)))
	#filter combinations
	if len(exclude_pairs_list) > 0:
		filter_combs = []
		for comb in all_combs:
			excluded_comb = False
			#print(comb)
			for a,b in exclude_pairs_list:
				if a in comb and b in comb:
					excluded_comb = True
			if excluded_comb is False:
				filter_combs.append(comb)
		print('Filtered down to {0} combinations from {1} items'.format(len(filter_combs), len(all_combs)))
		all_combs = filter_combs
	random.shuffle(all_combs)
	N = 0
	for comb in all_combs:
		choices_list = list(comb)
		random.shuffle(choices_list)
		answer = choices_list[0]
		answer_description = matching_pairs_dict[answer]
		if isinstance(answer_description, list):
			answer_description = random.choice(answer_description)
		random.shuffle(choices_list)
		question = ("<p>Which one of the following {0} correspond to the description <strong>'{1}'</strong>.</p>".format(
			yaml_data['key description'], answer_description))
		N += 1
		complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)

		list_of_complete_questions.append(complete_question)

	list_of_complete_questions = applyReplacementRulesToQuestions(list_of_complete_questions, yaml_data.get('replacement_rules'))
	return list_of_complete_questions

#=======================
def makeQuestions2(yaml_data, num_choices=None):
	matching_pairs_dict = yaml_data['matching pairs']
	exclude_pairs_list = yaml_data.get('exclude pairs', [])

	list_of_complete_questions = []

	if num_choices is None:
		num_choices = yaml_data.get('items to match per question', 5)
	### Get Keys and Key/Values Pairs
	all_keys = list(matching_pairs_dict.keys())
	key_value_pairs = []
	for key in all_keys:
		for value in matching_pairs_dict[key]:
			pair = (key, value)
			key_value_pairs.append(pair)
	### Generate Combiniations
	all_combs = list(itertools.combinations(all_keys, num_choices))
	print('Created {0} combinations from {1} items'.format(len(all_combs), len(all_keys)))
	#filter combinations
	if len(exclude_pairs_list) > 0:
		filter_combs = []
		for comb in all_combs:
			excluded_comb = False
			#print(comb)
			for a,b in exclude_pairs_list:
				if a in comb and b in comb:
					excluded_comb = True
			if excluded_comb is False:
				filter_combs.append(comb)
		print('Filtered down to {0} combinations from {1} items'.format(len(filter_combs), len(all_combs)))
		all_combs = filter_combs
	random.shuffle(all_combs)
	N = 0
	for pair in key_value_pairs:
		key, value = pair
		comb = random.choice(all_combs)
		count = 0
		while not key in comb:
			comb = random.choice(all_combs)
			count += 1
			if count > 20:
				print("something probably wrong, too many combinations searched")
				sys.exit(1)
		choices_list = list(comb)
		choices_list.sort()
		answer = key
		answer_description = value
		question = ("<p>Which one of the following {0} correspond to the description <strong>'{1}'</strong>.</p>".format(
			yaml_data['key description'], answer_description))
		N += 1
		complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)

		list_of_complete_questions.append(complete_question)

	list_of_complete_questions = applyReplacementRulesToQuestions(list_of_complete_questions, yaml_data.get('replacement_rules'))
	return list_of_complete_questions

#=======================
#=======================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='yaml input file to process')
	parser.add_argument('-x', '--max-questions', metavar='#', type=int, dest='max_questions',
		help='max number of questions', default=199)
	parser.add_argument('-d', '--duplicate-runs', metavar='#', type=int, dest='duplicate_runs',
		help='if more than one value is provided for each choice, run duplicates', default=1)
	parser.add_argument('-c', '--num-choices', metavar='#', type=int, dest='num_choices',
		help='how many choices to have for each question', default=None)
	args = parser.parse_args()

	if args.input_yaml_file is None or not os.path.isfile(args.input_yaml_file):
		print("Usage: {0} -y <input_yaml_file>".format(__file__))
		sys.exit(0)

	yaml_data = bptools.readYamlFile(args.input_yaml_file)
	pprint.pprint(yaml_data)

	list_of_complete_questions = []
	for i in range(args.duplicate_runs):
		list_of_complete_questions += makeQuestions2(yaml_data, args.num_choices)

	if len(list_of_complete_questions) > args.max_questions:
		print("Too many questions, trimming down to {0} questions".format(args.max_questions))
		random.shuffle(list_of_complete_questions)
		less_questions = list_of_complete_questions[:args.max_questions]
		less_questions.sort()
		list_of_complete_questions = less_questions

	outfile = 'bbq-MC-' + os.path.splitext(os.path.basename(args.input_yaml_file))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for bbformat_question in list_of_complete_questions:
		N += 1
		f.write(bbformat_question)
	f.close()
	print("Wrote {0} questions to file.".format(N))
	print('')
