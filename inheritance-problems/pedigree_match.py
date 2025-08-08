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
import pedigree_lib
import pedigree_code_strings

#=======================
def bbFormatMatchingQuestion(N, question_text, prompts_list, choices_list, max_choices=5):
	complete_question = question_text
	num_items = min(len(prompts_list), len(choices_list))
	indices = list(range(num_items))
	random.shuffle(indices)
	indices = indices[:max_choices]
	indices.sort()
	for i in indices:
		complete_question += '\t' + prompts_list[i] + '\t' + choices_list[i]
	crc16_value = getCrc16_FromString(complete_question)
	#MAT TAB question_text TAB answer_text TAB matching text TAB answer two text TAB matching two text
	bb_output_format = "MAT\t<p>{0:03d}. {1}</p> {2}\n".format(N, crc16_value, complete_question)
	return bb_output_format

#=======================
def matchingQuestionSet():
	bb_output_format_list = []
	question_text = "<p>Match the following pedigrees to their most likely inheritance type.</p> "
	question_text += "<p>Note: <i>each inheritance type will only be used ONCE.</i></p> "
	choices_list = ['autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked']
	N = 0
	for ad in pedigree_code_strings.autosomal_dominant:
		for ar in pedigree_code_strings.autosomal_recessive:			
			for xd in pedigree_code_strings.x_linked_dominant:
				for xr in pedigree_code_strings.x_linked_recessive:
					for yl in pedigree_code_strings.y_linked:
						if random.random() < 0.5:
							ad = pedigree_lib.mirrorPedigree(ad)
						adc = pedigree_lib.translateCode(ad)
						if random.random() < 0.5:
							ar = pedigree_lib.mirrorPedigree(ar)
						arc = pedigree_lib.translateCode(ar)
						if random.random() < 0.5:
							xd = pedigree_lib.mirrorPedigree(xd)
						xdc = pedigree_lib.translateCode(xd)
						if random.random() < 0.5:
							xr = pedigree_lib.mirrorPedigree(xr)
						xrc = pedigree_lib.translateCode(xr)
						if random.random() < 0.5:
							yl = pedigree_lib.mirrorPedigree(yl)
						ylc = pedigree_lib.translateCode(yl)

						prompts_list = [adc, arc, xdc, xrc, ylc]
						N += 1
						bb_output_format = bptools.formatBB_MAT_Question(N, question_text, prompts_list, choices_list)
						bb_output_format_list.append(bb_output_format)

	return bb_output_format_list


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
	outfile = (
		'bbq'
		f'-{script_name}'              # Add the script name to the file name
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
		bb_output_format_list = matchingQuestionSet()

		# Append question if successfully generated
		if bb_output_format_list is not None:
			N += len(bb_output_format_list)
			question_bank_list += bb_output_format_list

		if N >= args.max_questions:
			break

	# Show a histogram of answer distributions for MC/MA types
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
