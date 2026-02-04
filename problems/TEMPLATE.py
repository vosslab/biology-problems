#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random

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
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Generate the main question text
	question_text = get_question_text()

	# Generate answer choices and the correct answer
	choices_list, answer_text = generate_choices(args.num_choices)

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
		`max_questions`, `num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser()

	# Add standard argument bundles
	parser = bptools.add_choice_args(parser)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(parser, required=True)

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
	3. Generate and write formatted questions using shared helpers.
	4. Print status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output file name based on the script name and arguments
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(
		args.question_type.upper(),
		hint_mode,
		f"{args.num_choices}_choices"
	)

	# Collect and write questions using shared helper
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
