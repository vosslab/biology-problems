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


QUESTION_PROMPTS = [
	("Mating two organisms produces", "in progeny. The parental genotypes are:"),
	("Which genotype pairing would yield", "offspring?"),
	("Which mating pair would produce offspring that are", "offspring?"),
	("Which parental genotype combination would generate", "offspring?"),
	("Which parental genotype pairing would result in", "offspring?"),
	("Select the mating pair that results in", "offspring."),
	("What cross would lead to", "among the offspring?"),
	("Which pair of parental genotypes would produce", "in their offspring?"),
	("What parental genotype combination produces", "in the resulting progeny?"),
	("Identify the cross that produces", "in all offspring."),
	("Which cross leads to", "as the only outcome in the progeny?"),
	("Choose the parental genotype pairing that gives rise to", "in the offspring."),
]

QUESTION_BANK = [
	("a <b>1:1 ratio of two genotypes</b>",
	("AA x Aa", "Aa x aa")),

	("a <b>1:1 phenotype ratio</b>",
	("Aa x aa",)),

	("a <b>1:1 ratio of homozygotes to heterozygotes</b>",
	("AA x Aa", "Aa x aa", "Aa x Aa")),

	("a <b>1:2:1 genotype ratio</b>",
	("Aa x Aa",)),

	("a <b>3:1 phenotype ratio</b>",
	("Aa x Aa",)),

	("<b>only heterozygotes</b>",
	("AA x aa",)),

	("<b>only homozygotes</b>",
	("AA x AA", "aa x aa")),

	("<b>only one phenotype</b>",
	("AA x AA", "AA x Aa", "AA x aa", "aa x aa")),

	("<b>only the dominant phenotype</b>",
	("AA x AA", "AA x Aa", "AA x aa")),

	("<b>only the recessive phenotype</b>",
	("aa x aa",)),

	(r"<b>50% homozygous dominant and 50% heterozygous</b>",
	("AA x Aa",)),

	("<b>all homozygous recessive</b>",
	("aa x aa",)),

	("a <b>1:1 phenotype ratio</b>",
	("Aa x aa",)),

	("<b>all heterozygous</b>",
	("AA x aa",)),

	("<b>all homozygous dominant</b>",
	("AA x AA",)),
]

# Universe of monohybrid crosses (canonicalized "female x male")
ALL_CROSSES_SET = set([
	"AA x AA", "AA x Aa", "AA x aa",
	"Aa x Aa", "Aa x aa",
	"aa x aa",
])

#===========================================================
#===========================================================
def format_html_cross(cross_text: str) -> str:
	"""
	Formats a monohybrid cross string into styled HTML using color and bold.

	Args:
		cross_text (str): The original cross string (e.g., "Aa x aa")

	Returns:
		str: HTML-formatted string with colored alleles and multiplication symbol
	"""
	prefix = '<strong><span style="font-family: monospace; font-size: 1.5em; color: '


	# Apply formatting rules in order
	cross_html = cross_text
	cross_html = cross_html.replace('AA', prefix + '#ba372a;">AA</span></strong>')
	cross_html = cross_html.replace('Aa', prefix + '#843fa1;">Aa</span></strong>')
	cross_html = cross_html.replace('aa', prefix + '#236fa1;">aa</span></strong>')
	cross_html = cross_html.replace(' x ', ' &nbsp;&times;&nbsp; ')

	return cross_html


#===========================================================
#===========================================================
# This function generates and returns the main question text.
def get_question_text(question_root) -> str:
	"""
	Generates and returns the main text for the question.

	Returns:
		str: A string containing the main question text.
	"""
	# Initialize an empty string for the question text
	question_tuple = random.choice(QUESTION_PROMPTS)
	question_text = " ".join([question_tuple[0], question_root, question_tuple[1]])

	# Return the complete question text
	return question_text

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, question_statement: str, answer_cross_text: str, choice_pool_set: set) -> str:
	"""
	Creates a complete formatted question for output.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Generate the main question text
	question_text = get_question_text(question_statement)

	# Generate answer choices and the correct answer
	#choices_list, answer_text = generate_choices(num_choices)
	formatted_choices_list = []
	for choice_text in sorted(choice_pool_set):
		formatted_choice_text = format_html_cross(choice_text)
		formatted_choices_list.append(formatted_choice_text)

	formatted_answer_text = format_html_cross(answer_cross_text)

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, formatted_choices_list, formatted_answer_text)

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

	parser.add_argument('-x', '--max-questions', type=int, dest='max_questions',
		default=99, help='Max number of questions')

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
# Writes questions to the file until max_questions is reached
def write_question_batch(f, args) -> int:
	"""
	Generates and writes questions to file.

	Args:
		f (TextIO): Output file handle
		args (argparse.Namespace): Parsed command-line arguments

	Returns:
		int: Total number of questions written
	"""
	N = 0  # question count
	for _ in range(args.duplicates):
		for question_statement, answers in QUESTION_BANK:
			answers_set = set(answers)
			if not answers_set.issubset(ALL_CROSSES_SET):
				raise ValueError(
					"QUESTION_BANK answer set contains an unknown cross: "
					f"{sorted(list(answers_set - ALL_CROSSES_SET))}"
				)
			for answer_cross in answers_set:
				choice_pool_set = (ALL_CROSSES_SET - answers_set) | {answer_cross}
				complete_question = write_question(N + 1, question_statement, answer_cross, choice_pool_set)

				if complete_question:
					f.write(complete_question)
					N += 1
					if N >= args.max_questions:
						return N
	return N


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
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	with open(outfile, 'w') as f:
		N = write_question_batch(f, args)

	# If the question type is multiple choice, print a histogram of results
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
