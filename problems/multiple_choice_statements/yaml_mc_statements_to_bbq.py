#!/usr/bin/env python3

"""
This program creates all permutations of statements make a multiple choice question of the form:

- Which one of the following statements is TRUE/FALSE concerning/about/regarding ****
A.
B.
C.
"""

import os
import sys
import copy
import math
import time
import pprint
import random
import argparse
import itertools
import bptools

answer_histogram = {}

global_connection_words = [ 'concerning', 'about', 'regarding', 'of', ]
lowercase = "abcdefghijklmnopqrstuvwxyz"
is_lowercase = {}
for c in list(lowercase):
	is_lowercase[c] = True

#=======================
def checkUnique(yaml_data):
	true_statement_dict = yaml_data['true_statements']
	#pprint.pprint(true_statement_dict)
	false_statement_dict = yaml_data['false_statements']
	statement_dict = {}
	for key, value in true_statement_dict.items():
		if statement_dict.get(value) is None:
			statement_dict[value] = key
		else:
			print("DUPLICATE STATEMENT")
			print(value)
			print(statement_dict.get(value))
			print(key)
			time.sleep(2)
			sys.exit(1)
	for key, value in false_statement_dict.items():
		if statement_dict.get(value) is None:
			statement_dict[value] = key
		else:
			print("DUPLICATE STATEMENT")
			print(value)
			print(statement_dict.get(value))
			print(key)
			time.sleep(2)
			sys.exit(1)
	print("PASS checkUnique")
	return

#=======================
def autoAddConflictRules(yaml_data):
	is_number = {}
	for n in range(0,10):
		is_number[str(n)] = True
	true_statement_tree = yaml_data['true_statements']
	false_statement_tree = yaml_data['false_statements']
	yaml_data['conflict_rules'] = {}
	statement_keys = list(true_statement_tree.keys())
	statement_keys += list(false_statement_tree.keys())
	rule_bases = set()
	for key in statement_keys:
		#print(key[:-1])
		if is_lowercase.get(key[-1]) is True and is_number.get(key[-2]):
			#fits pattern the truth[1a]
			base = key[:-1]
			base = base.replace('false', 'bool')
			base = base.replace('truth', 'bool')
			rule_bases.add(base)
		elif is_number.get(key[-1]):
			#fits pattern the truth[1a]
			base = key
			base = base.replace('false', 'bool')
			base = base.replace('truth', 'bool')
			rule_bases.add(base)
	#print("Rule Bases", rule_bases)
	for base in rule_bases:
		base1 = base.replace('bool', 'truth')
		base2 = base.replace('bool', 'false')
		#print(base, base1, base2)
		yaml_data['conflict_rules'][base] = {}
		for key in statement_keys:
			if key == base1 or key == base2:
				#print(key, "True")
				yaml_data['conflict_rules'][base][key] = True
			elif is_lowercase.get(key[-1]) and (key[:-1] == base1 or key[:-1] == base2):
				yaml_data['conflict_rules'][base][key] = True
	base_keys = list(yaml_data['conflict_rules'].keys())
	for base in base_keys:
		if len(yaml_data['conflict_rules'][base]) == 1:
			del yaml_data['conflict_rules'][base]
	print("Final Conflict Rules:")
	pprint.pprint(yaml_data['conflict_rules'])
	print("")
	#time.sleep(1)
	#sys.exit(1)
	return


#=======================
def checkIfConflict(statement1_id, statement2_id, conflict_rules):
	# is a list of statement_ids
	for conflict_rule in conflict_rules.values():
		#print(conflict_rule)
		#answer = conflict_rule.get(statement1_id, False) and conflict_rule.get(statement2_id, False)
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
def makeQuestionsFromStatement(main_statement, opposing_statement_nested_list, question_text, replacement_rules_dict):
	num_wrong_choices = min(4, len(opposing_statement_nested_list))
	possible_iterations = len(list(itertools.product(*opposing_statement_nested_list)))
	possible_duplicate = possible_iterations * math.comb(len(opposing_statement_nested_list), num_wrong_choices)
	num_duplicates = max(1, int(math.floor(math.log(possible_duplicate))))
	print("Using {0} of a total of {1} possible duplicates.".format(num_duplicates, possible_duplicate))

	if num_wrong_choices <= 2:
		print("WARNING: not enough choices for this question, skipping...")
		return []

	question_list = []
	for j in range(num_duplicates):
		#get all the possible wrong answers
		random.shuffle(opposing_statement_nested_list)
		choices_nested_list = copy.copy(opposing_statement_nested_list[:num_wrong_choices])
		choices_list = []
		for nest_choice_list in choices_nested_list:
			choice = random.choice(nest_choice_list)
			choices_list.append(choice)
		#assign answer, add, and shuffle
		answer_string = bptools.applyReplacementRulesToText(main_statement, replacement_rules_dict)
		#choices_list = bptools.applyReplacementRulesToList(choices_list, replacement_rules_dict)

		choices_list.append(answer_string)
		random.shuffle(choices_list)
		N = random.randint(1, 999)

		question_text = bptools.applyReplacementRulesToText(question_text, replacement_rules_dict)
		bbformat = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_string)
		question_list.append(bbformat)

	return question_list

#=======================
def writeQuestion(yaml_data, question_type):
	if question_type is True and yaml_data.get('override_question_true', 'default') != 'default':
		return yaml_data['override_question_true']
	if question_type is False and yaml_data.get('override_question_false', 'default') != 'default':
		return yaml_data['override_question_false']

	topic = yaml_data['topic']
	if yaml_data.get('connection_words', None) is not None:
		connection_word_list = yaml_data.get('connection_words')
	else:
		connection_word_list = global_connection_words

	if question_type is False:
		question_type_html = 'FALSE '
	elif question_type is True:
		question_type_html = 'TRUE '
	else:
		question_type_html = '<strong>{0}</strong> '.format(str(question_type).upper())

	question_text = ("<p>Which one of the following statements is "
		+"{0} {1} {2}?</p>".format(question_type_html, random.choice(connection_word_list), topic) )
	return question_text


#=======================
def sortStatements(yaml_data, notrue=False, nofalse=False):
	true_statement_tree = yaml_data['true_statements']
	false_statement_tree = yaml_data['false_statements']
	conflict_rules = yaml_data['conflict_rules']

	list_of_complete_questions = []
	replacement_rules_dict = yaml_data.get('replacement_rules')

	question_text = writeQuestion(yaml_data, True)
	print(question_text)
	if notrue is False and question_text is not None:
		for true_statement_id,true_statement in true_statement_tree.items():

			filtered_false_statement_nested_list = filterOpposingStatements(true_statement_id, false_statement_tree, conflict_rules)
			question_string_list = makeQuestionsFromStatement(true_statement, filtered_false_statement_nested_list, question_text, replacement_rules_dict)
			list_of_complete_questions.extend(question_string_list)
	else:
		print("Skipping all of the TRUE statement questions")

	question_text = writeQuestion(yaml_data, False)
	print(question_text)
	if nofalse is False and question_text is not None:
		for false_statement_id,false_statement in false_statement_tree.items():

			filtered_true_statement_nested_list = filterOpposingStatements(false_statement_id, true_statement_tree, conflict_rules)
			question_string_list = makeQuestionsFromStatement(false_statement, filtered_true_statement_nested_list, question_text, replacement_rules_dict)
			list_of_complete_questions.extend(question_string_list)
	else:
		print("Skipping all of the FALSE statement questions")
	list_of_complete_questions = bptools.applyReplacementRulesToList(list_of_complete_questions, replacement_rules_dict)
	return list_of_complete_questions

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = argparse.ArgumentParser(description="Generate questions.")

	parser.add_argument('-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='yaml input file to process')


	parser.add_argument('--nofalse', '--no-false', action='store_true', dest='nofalse', default=False,
		help='do not create the false form (which one is false) of the question')
	parser.add_argument('--notrue', '--no-true', action='store_true', dest='notrue', default=False,
		help='do not create the true form (which one is true) of the question')

	parser.add_argument('-x', '--max-questions', metavar='#', type=int, dest='max_questions',
		help='yaml input file to process', default=199)

	# Add an argument to specify the number of duplicate questions to generate
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create',
		default=1
	)
	parser = bptools.add_anticheat_args(parser)

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args


#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	args = parse_arguments()
	bptools.apply_anticheat_args(args)

	if args.input_yaml_file is None or not os.path.isfile(args.input_yaml_file):
		print("Usage: {0} -y <input_yaml_file>".format(__file__))
		sys.exit(0)

	yaml_data = bptools.readYamlFile(args.input_yaml_file)
	checkUnique(yaml_data)
	pprint.pprint(yaml_data)
	autoAddConflictRules(yaml_data)

	list_of_complete_questions = []
	for i in range(args.duplicates):
		list_of_complete_questions += sortStatements(yaml_data, notrue=args.notrue, nofalse=args.nofalse)
		if len(list_of_complete_questions) > 2*args.max_questions:
			break

	#list_of_complete_questions = list(set(list_of_complete_questions))
	if len(list_of_complete_questions) > args.max_questions:
		print(f"\nToo many questions, trimming down to {args.max_questions} questions.")
		random.shuffle(list_of_complete_questions)
		less_questions = list_of_complete_questions[:args.max_questions]
		less_questions.sort()
		list_of_complete_questions = less_questions

	#list_of_complete_questions = bptools.applyReplacementRulesToList(list_of_complete_questions,
	#	yaml_data.get('replacement_rules'))

	# Generate the output file name based on the script name and question type
	base_name = os.path.splitext(os.path.basename(args.input_yaml_file))[0]
	outfile = (
		'bbq'
		'-TFMS'
		f'-{base_name}'  # Add the script name to the file name
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}\n')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for bbformat_question in list_of_complete_questions:
			N += 1
			f.write(bbformat_question)

	# print a histogram of results
	bptools.print_histogram()

	# Print a message indicating how many questions were saved
	print(f'saved {N} questions to {outfile}')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
