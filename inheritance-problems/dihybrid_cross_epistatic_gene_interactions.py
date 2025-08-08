#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
import copy

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import hybridcrosslib as crossinglib

#===================
#===================
def questionContent(gene_id):
	question = ''
	question += '<p>Above are the phenotypic results from a dihybrid cross and double heterozygote test cross. '
	question += 'The phenotypes were '
	ratio = crossinglib.gene_type_ratios[gene_id]
	counts = ratio.split(':')
	for count in counts:
		question += '{0} to '.format(crossinglib.num2word[int(count)])
	question = question[:-4]
	question += ' ({0}).</p>'.format(ratio)
	question += '<p><strong>What type of gene interaction is being shown?</strong></p>'
	#print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	assigned_colors = crossinglib.dihybridAssignColorsOriginal(gene_id, color_set)
	dihybrid_table = crossinglib.createDiHybridTable(letter1, letter2, assigned_colors)
	testcross_table = crossinglib.createTestCrossTable(letter1, letter2, assigned_colors)

	# write the question content
	question = questionContent(gene_id)

	complete_question = '<table style="border: 0px solid white; border-collapse: collapse; ">'
	complete_question += ' <tr><td> '
	complete_question += dihybrid_table
	complete_question += ' </td><td> '
	complete_question += '&nbsp;'
	complete_question += ' </td><td> '
	complete_question += testcross_table
	complete_question += '</td></tr></table> '

	complete_question += " <br/> "
	complete_question += question

	#print(complete_question)
	return complete_question


#===================
#===================
def writeQuestion(N, gene_id, color_set):
	# make the question
	letter_pool = copy.copy(crossinglib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = [letter_pool.pop(), letter_pool.pop()]
	two_letters.sort()
	letter1 = two_letters[0]
	letter2 = two_letters[1]
	question_text = makeQuestion(gene_id, color_set, letter1, letter2)



	# write the question
	choice_letters = "ABCDEFGHI"
	file_handle.write("MC\t{0}".format(question_text))
	answer = gene_id
	gene_ids = list(crossinglib.gene_interaction_names.keys())
	random.shuffle(gene_ids)
	for k, sub_gene_id in enumerate(gene_ids):
		if sub_gene_id == answer:
			prefix = "*"
			status = "Correct"
		else:
			prefix = ""
			status = "Incorrect"
		name = crossinglib.gene_interaction_names[sub_gene_id]
		description = crossinglib.gene_type_description[sub_gene_id]
		choice_text = "These two genes show <strong>{0}</strong>. {1}.".format(name, description)
		file_handle.write("\t{0}\t{1}".format(choice_text, status))
		print("{0}{1}. {2}".format(prefix, choice_letters[k], choice_text))
	file_handle.write("\n")

#===================
#===================
def gene_id_to_choice_text(gene_id: str) -> str:
	"""
	Converts a gene interaction ID to a formatted choice text.

	Args:
		gene_id (str): The gene interaction identifier.

	Returns:
		str: Formatted choice text string.
	"""
	name = crossinglib.gene_interaction_names[gene_id]
	description = crossinglib.gene_type_description[gene_id]
	choice_text = f"These two genes show <strong>{name}</strong> {description}."
	return choice_text

#===================
#===================
def write_question(N: int, answer_gene_id: str, color_set: list, num_choices: int) -> str:
	"""
	Creates a formatted MC question about gene interaction types.

	Args:
		N (int): Question number
		answer_gene_id (str): The correct gene interaction type ID
		color_set (list): List of colors involved in the genetic scenario

	Returns:
		str: Complete formatted Blackboard question string
	"""
	# Select and sort two gene letters for use in question table
	letter_pool = copy.copy(crossinglib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = sorted([letter_pool.pop(), letter_pool.pop()])

	# Create the main question text
	question_text = makeQuestion(answer_gene_id, color_set, two_letters[0], two_letters[1])

	# Build answer and choices
	answer_text = gene_id_to_choice_text(answer_gene_id)

	all_gene_ids = set(crossinglib.gene_interaction_names.keys())
	if len(all_gene_ids) > num_choices:
		# Exclude the correct answer first using a set
		available_distractors = list(all_gene_ids - {answer_gene_id})
		# Sample random distractors
		distractors = set(random.sample(available_distractors, num_choices - 1))
		# Add the correct answer
		all_gene_ids = distractors | {answer_gene_id}

	choices_list = []
	for sub_gene_id in all_gene_ids:
		choice_text = gene_id_to_choice_text(sub_gene_id)
		choices_list.append(choice_text)

	random.shuffle(choices_list)
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

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

	# Add an argument to specify the number of duplicate questions to generate
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create',
		default=1
	)

	parser.add_argument(
		'-x', '--max-questions', type=int, dest='max_questions',
		default=99, help='Max number of questions'
	)

	# Add an argument to specify the number of answer choices for each question
	parser.add_argument(
		'-c', '--num_choices', type=int, default=4, dest='num_choices',
		help="Number of choices to create."
	)

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output file name based on the script name and arguments
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'              # Add the script name to the file name
		f'-{args.num_choices}_choices' # Append number of choices
		'-questions.txt'               # File extension
	)

	# Store all complete formatted questions
	question_bank_list = []

	# Initialize question counter
	N = 0

	# these are just numbers
	all_gene_ids = list(crossinglib.gene_interaction_names.keys())
	all_color_sets = crossinglib.get_four_color_sets()
	#print(all_color_sets)

	# Create the specified number of questions
	for _ in range(args.duplicates):
		gene_id = N % len(all_gene_ids)
		color_set = random.choice(all_color_sets)

		# Create a full formatted question (Blackboard format)
		complete_question = write_question(N+1, gene_id, color_set, args.num_choices)

		# Append question if successfully generated
		if complete_question is not None:
			N += 1
			question_bank_list.append(complete_question)

	# Show a histogram of answer distributions for MC/MA types
	bptools.print_histogram()

	# Shuffle and limit the number of questions if over max
	if len(question_bank_list) > args.max_questions:
		random.shuffle(question_bank_list)
		question_bank_list = question_bank_list[:args.max_questions]

	# Announce where output is going
	print(f'\nWriting {N} question to file: {outfile}')

	# Write all questions to file
	with open(outfile, 'w') as f:
		for complete_question in question_bank_list:
			f.write(complete_question)

	# Final status message
	print(f'... saved {N} questions to {outfile}\n')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END




