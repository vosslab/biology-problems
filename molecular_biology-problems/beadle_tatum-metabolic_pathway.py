#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
import sys
import copy
import itertools

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools


#===========================================================
#===========================================================
def enzyme_table(metabolites, color_wheel):
	htmltext = ""
	tdopen_top = '<td align="center" valign="top" >'
	tdopen_bot = '<td align="center" valign="bottom" >'
	htmltext += '<table cellpadding="2" cellspacing="2"'
	htmltext += '  style="background-color: #efefef; text-align:center; '
	htmltext += '  border: 1px solid black; font-size: 14px;"> '  
	htmltext += '<tr> '
	enzyme_count = len(metabolites) - 1
	for i in range(enzyme_count):
		enzyme_num = i+1
		htmltext += '<td></td> {0}<span style="font-size: 12px;">enzyme {1:d}</span></td> '.format(tdopen_bot, enzyme_num)
	htmltext += '</tr><tr> '
	for i,meta in enumerate(metabolites):
		color = color_wheel[i]
		htmltext += '{0}<span style="color: {1}; font-size: 20px;"><strong>{2}</strong></span></td> '.format(tdopen_top, color, meta)
		if i+1 != len(metabolites):
			htmltext += '{0}<span style="font-size: 16px;">&xrarr;</span></td> '.format(tdopen_top)
	htmltext += '</tr> '
	htmltext += '</table>'
	return htmltext

#===========================================================
#===========================================================
def write_question(N, num_metabolites):
	metabolite_letters_lower = bptools.generate_gene_letters(num_metabolites, clear=True)
	metabolite_letters_upper = metabolite_letters_lower.upper()
	#print("metabolite_letters_upper = ", metabolite_letters_upper)
	
	deg_step = int(round(360./len(metabolite_letters_upper) - 1))
	color_amount = 240
	color_wheel = bptools.make_color_wheel(color_amount, 0, 0, deg_step)

	question_text = '<p>Look at the metabolic pathway in the table above.</p>'
	question_text += '<p>Metabolite '
	color = color_wheel[len(metabolite_letters_upper)]
	question_text += f'<span style="color: {color};"><strong>{metabolite_letters_upper[-1]}</strong></span>'
	question_text += ' is needed for the bacteria to grow.</p>'

	enzyme_num = random.choice(range(1, len(metabolite_letters_upper)-1))

	question_text += f'<p>Consider a bacterial strain that is mutant for the gene coding for enzyme {enzyme_num:d}</p>'
	question_text += '<p>Which nutrients, when added to minimal media, will help this bacteria grow?</p>'
	question_text += '<p>Multiple answers may be correct.</p>'

	question_text = enzyme_table(metabolite_letters_upper, color_wheel) + question_text

	choices_list = []
	answers_list = []

	indices = list(range(len(metabolite_letters_upper)))
	random.shuffle(indices)
	indices = indices[:2]
	indices.sort()
	#for i in range(len(metabolite_letters_upper)):
	for i,meta in enumerate(metabolite_letters_upper):
		color_txt = color_wheel[i]
		meta_txt = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color_txt, meta)
		choice = "Supplemented with nutrient {0}".format(meta_txt)
		choices_list.append(choice)
		if i >= enzyme_num:
			answers_list.append(choice)

	bbformat_question = bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)
	#bbformat_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbformat_question

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
		'-c', '--num-metabolites', type=int, default=5, dest='num_metabolites',
		help="Number of choices to create."
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
		f'-{args.num_metabolites}_metabolites'

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

			# Generate the complete formatted question
			complete_question = write_question(N+1, args.num_metabolites)

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

