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

N = 0

#=======================
#=======================
#=======================
def permuteMatchingPairs(yaml_data, num_choices=None, max_questions=None):
	matching_pairs_dict = yaml_data['matching pairs']
	exclude_pairs_list = yaml_data.get('exclude pairs', [])

	list_of_complete_questions = []

	#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
	#"Match each of the following <keys> with their corresponding <values>"
	if yaml_data.get("question override") is None:
		question = ("<p>Match each of the following {0} with their corresponding {1}.</p>".format(
			yaml_data['keys description'], yaml_data['values description']))
	else:
		question = yaml_data.get("question override")
	question += '<p><i>Note:</i> Each choice will be used exactly once.</p>'
	question = bptools.applyReplacementRulesToText(question, yaml_data.get('replacement_rules'))
	print("")
	#print("question", question)
	global N

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
		print('Filtered {0} combinations from {1} items'.format(len(filter_combs), len(all_combs)))
		all_combs = filter_combs
	random.shuffle(all_combs)
	for comb in all_combs:
		answers_list = list(comb)
		random.shuffle(answers_list)
		matching_list = []
		for key in answers_list:
			if isinstance(key, list):
				key = random.choice(key)
			value = matching_pairs_dict[key]
			if isinstance(value, list):
				value = random.choice(value)
			matching_list.append(value)
		N += 1
		answers_list = bptools.applyReplacementRulesToList(answers_list, yaml_data.get('replacement_rules'))
		#answers_list = bptools.append_clear_font_space_to_list(answers_list)
		matching_list = bptools.applyReplacementRulesToList(matching_list, yaml_data.get('replacement_rules'))
		#matching_list = bptools.append_clear_font_space_to_list(matching_list)
		complete_question = bptools.formatBB_MAT_Question(N, question, answers_list, matching_list)
		list_of_complete_questions.append(complete_question)
		if len(list_of_complete_questions) > max_questions*10:
			break

	#list_of_complete_questions = bptools.applyReplacementRulesToList(list_of_complete_questions, yaml_data.get('replacement_rules'))
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
		list_of_complete_questions += permuteMatchingPairs(yaml_data, args.num_choices, args.max_questions)

	if len(list_of_complete_questions) > args.max_questions:
		print("Too many questions ({0}), trimming down to {1} questions".format(len(list_of_complete_questions), args.max_questions))
		random.shuffle(list_of_complete_questions)
		less_questions = list_of_complete_questions[:args.max_questions]
		less_questions.sort()
		list_of_complete_questions = less_questions

	outfile = 'bbq-MATCH-' + os.path.splitext(os.path.basename(args.input_yaml_file))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for bbformat_question in list_of_complete_questions:
		N += 1
		#crc16_value = bptools.getCrc16_FromString(bbformat_question)
		#MAT TAB question text TAB answer text TAB matching text TAB answer two text TAB matching two text
		#formatBB_MAT_Question(N, question, answers_list, matching_list)
		#output_format = "MAT\t<p>{0:03d}. {1}</p> {2}\n".format(N, crc16_value, bbformat_question)
		f.write(bbformat_question)
	f.close()
	print("Wrote {0} questions to file.".format(N))
	print('')
	#does not make sense for matching questions
	#bptools.print_histogram()
