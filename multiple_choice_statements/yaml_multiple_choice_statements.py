#!/usr/bin/env python

"""
This program creates all permutations of statements make a multiple choice question of the form:

- Which one of the following statements is TRUE/FALSE concerning/about/regarding ****
A.
B.
C.
"""

import os
import sys
import math
import yaml
import copy
import pprint
import random
import argparse
import itertools

global_connection_words = [ 'concerning', 'about', 'regarding', 'of', ]
base_replacement_rules = {
	' NOT ': ' <strong>NOT</strong> '
}


#=======================
def readYamlFile(yaml_file):
	yaml_pointer = open(yaml_file, 'r')
	data = yaml.safe_load(yaml_pointer)
	yaml_pointer.close()
	return data

#=======================
def checkIfConflict(statement1_id, statement2_id, conflict_rules):
	# is a list of statement_ids
	for conflict_rule in conflict_rules.values():
		#print(conflict_rule)
		#answer = conflict_rule.get(statement1_id, False)  and conflict_rule.get(statement2_id, False)
		#print(statement1_id, "+", statement2_id, "=", answer)
		if (conflict_rule.get(statement1_id, False) is True
			and conflict_rule.get(statement2_id, False) is True):
			#print(statement1_id, statement2_id, conflict_rule.get(statement1_id, False), conflict_rule.get(statement2_id, False))
			return True

	return False

#=======================
def filterOpposingStatements(main_statement_id, opposing_statement_tree, conflict_rules):
	# first remove statements that conflict with the main statement
	allowed_opposing_statement_tree = {}
	for statement_id, statement in opposing_statement_tree.items():
		if checkIfConflict(main_statement_id, statement_id, conflict_rules) is False:
			allowed_opposing_statement_tree[statement_id] = statement
	#pprint.pprint(allowed_opposing_statement_tree)
	#sys.exit(1)

	# second put conflicting opposing_statement into either/or switch lists
	opposing_statement_nested_list = []
	used_statements = {}
	for statement1_id, statement1 in allowed_opposing_statement_tree.items():
		if used_statements.get(statement1_id) is True:
			continue
		statement1_list = [statement1, ]
		for statement2_id, statement2 in allowed_opposing_statement_tree.items():
			if statement1_id == statement2_id:
				continue
			if used_statements.get(statement2_id) is True:
				continue
			if checkIfConflict(statement1_id, statement2_id, conflict_rules) is True:
				statement1_list.append(statement2)
				used_statements[statement2_id] = True
		opposing_statement_nested_list.append(statement1_list)
		used_statements[statement1_id] = True

	#pprint.pprint(opposing_statement_nested_list)
	return opposing_statement_nested_list

#=======================
def makeQuestionsFromStatement(main_statement, opposing_statement_nested_list, question_text):

	num_wrong_choices = min(4, len(opposing_statement_nested_list))
	possible_iterations = len(list(itertools.product(*opposing_statement_nested_list)))
	possible_duplicate = possible_iterations * math.comb(len(opposing_statement_nested_list), num_wrong_choices)
	num_duplicates = max(1, int(math.floor(math.log(possible_duplicate))))
	print("Using {0} of a total of {1} possible duplicates.".format(num_duplicates, possible_duplicate))

	if num_wrong_choices <= 2:
		print("WARNING: not enough choices for this question, skipping...")
		return []
	letters = "ABCDEFGH"

	question_list = []
	for j in range(num_duplicates):
		bbformat = copy.copy(question_text)
		print(question_text)
		random.shuffle(opposing_statement_nested_list)
		choices_nested_list = copy.copy(opposing_statement_nested_list[:num_wrong_choices])
		choices_nested_list.append([main_statement, ])
		random.shuffle(choices_nested_list)
		for i, choice_list in enumerate(choices_nested_list):
			random.shuffle(choice_list)
			choice = choice_list[0]
			bbformat += '\t{0}. {1}'.format(letters[i], choice)
			if choice == main_statement:
				prefix = 'x'
				bbformat += '\tCorrect'
			else:
				prefix = ' '
				bbformat += '\tIncorrect'
			print("- [{0}] {1}. {2}".format(prefix, letters[i], choice))
		print("")
		question_list.append(bbformat)

	return question_list

#=======================
def writeQuestion(yaml_data, question_type):
	if question_type is True and yaml_data.get('override_question_true', 'default') != 'default':
		return yaml_data['override_question_true']
	if question_type is False and yaml_data.get('override_question_false', 'default') != 'default':
		return yaml_data['override_question_false']

	topic  = yaml_data['topic']
	if yaml_data.get('connection_words', None) is not None:
		connection_word_list = yaml_data.get('connection_words')
	else:
		connection_word_list = global_connection_words

	if question_type is False:
		question_type_html = '<span style="color: #ba372a;"><strong>FALSE</strong></span> ' #BOLD RED
	elif question_type is True:
		question_type_html = '<span style="color: #169179;"><strong>TRUE</strong></span> ' #BOLD GREEN
	else:
		question_type_html = '<strong>{0}</strong> '.format(str(question_type).upper())

	question_text = ("Which one of the following statements is "
		+"{0} {1} {2}?".format(question_type_html, random.choice(connection_word_list), topic) )
	return question_text

#=======================
def applyReplacementRulesToQuestions(list_of_question_text, replacement_rule_dict):
	if replacement_rule_dict is None:
		print("no replacement rules found")
		return list_of_question_text
	new_list_of_question_text = []
	for question_text in list_of_question_text:
		for find_text,replace_text in replacement_rule_dict.items():
			question_text = question_text.replace(find_text,replace_text)
		new_list_of_question_text.append(question_text)
	return new_list_of_question_text

#=======================
def sortStatements(yaml_data, notrue=False, nofalse=False):
	true_statement_tree = yaml_data['true_statements']
	false_statement_tree = yaml_data['false_statements']
	conflict_rules = yaml_data['conflict_rules']

	list_of_complete_questions = []

	question_text = writeQuestion(yaml_data, True)
	print(question_text)
	if notrue is False and question_text is not None:
		for true_statement_id,true_statement in true_statement_tree.items():

			filtered_false_statement_nested_list = filterOpposingStatements(true_statement_id, false_statement_tree, conflict_rules)
			question_string_list = makeQuestionsFromStatement(true_statement, filtered_false_statement_nested_list, question_text)
			list_of_complete_questions.extend(question_string_list)
	else:
		print("Skipping all of the TRUE statement questions")

	question_text = writeQuestion(yaml_data, False)
	print(question_text)
	if nofalse is False and question_text is not None:
		for false_statement_id,false_statement in false_statement_tree.items():

			filtered_true_statement_nested_list = filterOpposingStatements(false_statement_id, true_statement_tree, conflict_rules)
			question_string_list = makeQuestionsFromStatement(false_statement, filtered_true_statement_nested_list, question_text)
			list_of_complete_questions.extend(question_string_list)
	else:
		print("Skipping all of the FALSE statement questions")
		
	list_of_complete_questions = applyReplacementRulesToQuestions(list_of_complete_questions, yaml_data.get('replacement_rules'))	
		
	return list_of_complete_questions

#=======================
#=======================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
							  help='yaml input file to process')
	parser.add_argument('--nofalse', '--no-false', action='store_true', dest='nofalse', default=False,
							  help='do not create the false form (which one is false) of the question')
	parser.add_argument('--notrue', '--no-true', action='store_true', dest='notrue', default=False,
							  help='do not create the true form (which one is true) of the question')
	parser.add_argument('-x', '--max-questions', metavar='<file>', type=int, dest='max_questions',
							  help='yaml input file to process', default=199)
	args = parser.parse_args()

	if args.input_yaml_file is None or not os.path.isfile(args.input_yaml_file):
		print("Usage: {0} -y <input_yaml_file>".format(__file__))
		sys.exit(0)

	yaml_data = readYamlFile(args.input_yaml_file)
	pprint.pprint(yaml_data)

	list_of_complete_questions = sortStatements(yaml_data, notrue=args.notrue, nofalse=args.nofalse)
	if len(list_of_complete_questions) > args.max_questions:
		print("Too many questions, trimming down to {0} questions".format(args.max_questions))
		random.shuffle(list_of_complete_questions)
		less_questions = list_of_complete_questions[:args.max_questions]
		less_questions.sort()
		list_of_complete_questions = less_questions

	outfile = 'bbq-' + os.path.splitext(os.path.basename(args.input_yaml_file))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for bbformat_question in list_of_complete_questions:
		N += 1
		number_str = "{0}. ".format(N)
		f.write('MC\t' + number_str + bbformat_question + '\n')
	f.close()
	print("Wrote {0} questions to file.".format(N))


