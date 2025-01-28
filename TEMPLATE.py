#!/usr/bin/env python3

# built-in python modules
import os
import random
import argparse

# external pip modules

# local repo modules
import bptools

#======================================
#======================================
def get_question_text() -> str:
	"""
	Generates and returns the main text for the question.

	This function is responsible for creating the base question text.
	Currently, it returns a generic placeholder string, but in a real
	application, this could involve generating a dynamic question based
	on various inputs or parameters.

	Returns:
		str: A string containing the main question text.
	"""
	question_text = ""
	question_text += "This is a hard question?"
	return question_text

#======================================
#======================================
def generate_choices(num_choices: int) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer.

	Defines a fixed set of choices for multiple-choice questions.
	This function randomly selects a correct answer from a predefined
	list of correct choices, then adds a few incorrect choices from
	another list to fill out the choices list. The number of choices
	is constrained by `num_choices`.

	Args:
		num_choices (int): The total number of answer choices to generate.

	Returns:
		tuple: A tuple containing:
			- list: A list of answer choices (mixed correct and incorrect).
			- str: The correct answer text.
	"""
	# Define possible correct choices and incorrect choices
	choices_list = [
		'competitive inhibitor',
		'non-competitive inhibitor',
	]
	answer_text = random.choice(choices_list)
	wrong_choices_list = [
		'molecular stopper',
		'metabolic blocker',
	]
	random.shuffle(wrong_choices_list)
	choices_list.extend(wrong_choices_list[:num_choices - len(choices_list)])

	# Shuffle choices for random ordering
	random.shuffle(choices_list)

	return choices_list, answer_text

#======================================
#======================================
def write_question(N: int, num_choices: int) -> str:
	"""
	Creates a complete formatted question for output.

	This function combines the question text and choices generated by
	other functions into a formatted question string. The formatting
	is handled by a helper function from the `bptools` module.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string suitable for output, containing
		the question text, answer choices, and correct answer.
	"""
	# Generate the question text
	question_text = get_question_text()

	# Generate answer choices and correct answer
	choices_list, answer_text = generate_choices(num_choices)

	# Format the complete question with the specified module function
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create', default=1
	)
	parser.add_argument(
		'-c', '--num_choices', type=int, default=5, dest='num_choices',
		help="Number of choices to create."
	)

	# Create a mutually exclusive group for question type and make it required
	question_group = parser.add_mutually_exclusive_group(required=True)
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('num', 'mc'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)
	question_group.add_argument(
		'-n', '--num', dest='question_type', action='store_const', const='num',
		help='Set question type to numeric'
	)

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Define output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'
		f'-{args.question_type.upper() }'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			gene_letters_str = bptools.generate_gene_letters(3)
			complete_question = write_question(N, args.num_choices)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram if question type is multiple choice
	if args.question_type == "mc":
		bptools.print_histogram()

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
