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

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output file name based on the script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'  # Add the script name to the file name
		f'-{args.question_type.upper()}'  # Add the question type in uppercase
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for _ in range(args.duplicates):
			# Generate a unique identifier for the question (e.g., gene letters)
			gene_letters_str = bptools.generate_gene_letters(3)

			# Generate the complete formatted question
			complete_question = write_question(N+1, args.num_choices)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# If the question type is multiple choice, print a histogram of results
	if args.question_type == "mc":
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
