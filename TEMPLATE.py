#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#===========================================================
#===========================================================
# This function generates and returns the main question text.
def get_question_text() -> str:
	"""
	Generates and returns the main text for the question.

	Returns:
		str: A string containing the main question text.
	"""
	# Initialize an empty string for the question text
	question_text = ""

	# Add the actual question text to the string
	question_text += "This is a hard question?"

	# Return the complete question text
	return question_text

#===========================================================
#===========================================================
# This function generates multiple answer choices for a question.
def generate_choices(num_choices: int) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer.

	Args:
		num_choices (int): The total number of answer choices to generate.

	Returns:
		tuple: A tuple containing:
			- list: A list of answer choices (mixed correct and incorrect).
			- str: The correct answer text.
	"""
	# Define a list of correct answer choices
	choices_list = [
		'competitive inhibitor',
		'non-competitive inhibitor',
	]

	# Randomly select one correct answer from the list
	answer_text = random.choice(choices_list)

	# Define a list of incorrect answer choices
	wrong_choices_list = [
		'molecular stopper',
		'metabolic blocker',
	]

	# Shuffle the incorrect choices to add randomness
	random.shuffle(wrong_choices_list)

	# Add incorrect choices to the choices list to reach the desired number of choices
	choices_list.extend(wrong_choices_list[:num_choices - len(choices_list)])

	# Shuffle all the choices to randomize their order
	random.shuffle(choices_list)

	# Return the list of choices and the correct answer
	return choices_list, answer_text

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, num_choices: int) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Generate the main question text
	question_text = get_question_text()

	# Generate answer choices and the correct answer
	choices_list, answer_text = generate_choices(num_choices)

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Return the formatted question string
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
		'-c', '--num_choices', type=int, default=5, dest='num_choices',
		help="Number of choices to create."
	)

	# Create a mutually exclusive group for question type selection
	# The group ensures only one of these options can be chosen at a time
	question_group = parser.add_mutually_exclusive_group(required=True)

	# Add an option to manually set the question type
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str,
		choices=('num', 'mc'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)

	# Add a shortcut option to set the question type to multiple choice
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)

	# Add a shortcut option to set the question type to numeric
	question_group.add_argument(
		'-n', '--num', dest='question_type', action='store_const', const='num',
		help='Set question type to numeric'
	)

	parser.add_argument(
		'--hint', dest='hint', action='store_true',
		help='Include a hint in the question'
	)
	parser.add_argument(
		'--no-hint', dest='hint', action='store_false',
		help='Do not include a hint in the question'
	)
	parser.set_defaults(hint=True)  # Set default value for hint

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using write_question().
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output file name based on the script name and arguments
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = (
		'bbq'
		f'-{script_name}'              # Add the script name to the file name
		f'-{args.question_type.upper()}'  # Append question type in uppercase (e.g., MC, MA)
		f'-{hint_mode}'  	# Append question type in uppercase (e.g., MC, MA)
		f'-{args.num_choices}_choices' # Append number of choices
		'-questions.txt'               # File extension
	)

	# Store all complete formatted questions
	question_bank_list = []

	# Initialize question counter
	N = 0

	# Create the specified number of questions
	for _ in range(args.duplicates):
		# Generate gene letters (if needed by question logic)
		gene_letters_str = bptools.generate_gene_letters(3)

		# Create a full formatted question (Blackboard format)
		complete_question = write_question(N+1, args.num_choices)

		# Append question if successfully generated
		if complete_question is not None:
			N += 1
			question_bank_list.append(complete_question)

		if N >= args.max_questions:
			break

	# Show a histogram of answer distributions for MC/MA types
	if args.question_type == "mc" or args.question_type == "ma":
		bptools.print_histogram()

	# Shuffle and limit the number of questions if over max
	if len(question_bank_list) > args.max_questions:
		random.shuffle(question_bank_list)
		question_bank_list = question_bank_list[:args.max_questions]

	# Announce where output is going
	print(f'\nWriting {len(question_bank_list)} question to file: {outfile}')

	# Write all questions to file
	write_count = 0
	with open(outfile, 'w') as f:
		for complete_question in question_bank_list:
			write_count += 1
			f.write(complete_question)

	# Final status message
	print(f'... saved {write_count} questions to {outfile}\n')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
