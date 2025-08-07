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
import hybridcrosslib


#===================
def styled_color(color_name: str) -> str:
	"""
	Returns an HTML-styled version of a color name.
	"""
	common_color_name = hybridcrosslib.color_translate.get(color_name, color_name)
	return (
		f'<strong>{common_color_name} '
		f'(<span style="color: {color_name}; font-size: 1.8em;">&#x25A0;</span>)</strong>'
	)

#===================
#===================
#===================
def make_question_content(gene_type, color_set):
	"""
	Generates the descriptive question text for a gene dominance problem.

	Args:
		gene_type (str): Type of dominance ('complete dominance', 'incomplete dominance', 'codominance')
		color_set (list[str]): List of three color names [dominant, intermediate, recessive]

	Returns:
		str: HTML string for the question body
	"""
	# Create styled versions of the color names
	color1_text = styled_color(color_set[0])
	color2_text = styled_color(color_set[1])
	color3_text = styled_color(color_set[2])

	# Start question
	question = '<p>Two organisms were crossed in a monohybrid experiment. '

	if gene_type == 'complete dominance':
		question += (
			f'The offspring showed three {color1_text} and one {color3_text} phenotype.</p>'
		)

	else:
		truebreeds = [color1_text, color3_text]
		random.shuffle(truebreeds)

		question += f'The offspring phenotypes included {truebreeds[0]} and {truebreeds[1]}'

		if gene_type == 'incomplete dominance':
			question += f', along with an intermediate {color2_text} phenotype.</p>'

		elif gene_type == 'codominance':
			question += (
				f', along with a speckled combination of {truebreeds[0]} and {truebreeds[1]}.</p>'
			)

	# Final prompt
	question += '<p><strong>What type of dominance best explains these results?</strong></p>'
	return question

#===================
#===================
def get_question_text(gene_type, color_set, letter):
	"""
	gene types

	0: 'complete dominance',
	1: 'incomplete dominance',
	2: 'codominance',
	"""
	gene_table = hybridcrosslib.createSingleGeneTable(gene_type, letter, color_set, 'Gene 1')

	# write the question content
	question_content = make_question_content(gene_type, color_set)

	question_text = ''
	question_text += gene_table
	question_text += " <br/> "
	question_text += question_content

	return question_text


#===================
#===================
def write_question(N: int, gene_letter: str, gene_type: str, color_set: list) -> None:
	"""
	Creates a formatted MC question about gene type interpretation.

	Args:
		gene_letter (str): Label (e.g., A, B, C).
		gene_type (str): Gene dominance type.
		color_set (list[str]): Three-color phenotype set.

	Returns:
		str: Formatted multiple choice question
	"""
	# Build question text
	question_text = get_question_text(gene_type, color_set, gene_letter)

	# Create shuffled list of choices
	all_gene_types = copy.copy(hybridcrosslib.single_gene_types)
	all_gene_types += ['epistasis', 'X-linked recessive']
	random.shuffle(all_gene_types)

	# Create choice text list
	choices_list = [f"The gene shows {gtype}" for gtype in all_gene_types]
	answer_text = f"The gene shows {gene_type}"

	# Format with bptools
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Write to file
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
			gene_letter = random.choice(hybridcrosslib.gene_letters)
			gene_type = random.choice(hybridcrosslib.single_gene_types)
			color_set = random.choice(hybridcrosslib.get_three_color_sets())

			# Generate the complete formatted question
			complete_question = write_question(N+1, gene_letter, gene_type, color_set)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)

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
