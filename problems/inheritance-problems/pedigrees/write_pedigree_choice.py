#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import pedigree_html_lib
import pedigree_code_lib
import pedigree_code_templates


#=======================
def multipleChoiceQuestionSet(start_num: int):
	bb_output_format_list = []
	choices_list = ['autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked']
	question_text = ("<p>Examine the pedigree above. "
	+"Which one of the following patterns of inheritance is most likely demonstrated in the above pedigree inheritance?</p> "
	)
	N = start_num - 1
	for ad in pedigree_code_templates.autosomal_dominant:
		if random.random() < 0.5:
			ad = pedigree_code_lib.mirror_pedigree(ad)
		adc = pedigree_html_lib.translateCode(ad)
		answer = 'autosomal dominant'
		N += 1
		bb_output_format = bptools.formatBB_MC_Question(N, adc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for ar in pedigree_code_templates.autosomal_recessive:			
		if random.random() < 0.5:
			ar = pedigree_code_lib.mirror_pedigree(ar)
		arc = pedigree_html_lib.translateCode(ar)
		answer = 'autosomal recessive'
		N += 1
		bb_output_format = bptools.formatBB_MC_Question(N, arc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for xd in pedigree_code_templates.x_linked_dominant:
		if random.random() < 0.5:
			xd = pedigree_code_lib.mirror_pedigree(xd)
		xdc = pedigree_html_lib.translateCode(xd)
		answer = 'x-linked dominant'
		N += 1
		bb_output_format = bptools.formatBB_MC_Question(N, xdc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for xr in pedigree_code_templates.x_linked_recessive:
		if random.random() < 0.5:
			xr = pedigree_code_lib.mirror_pedigree(xr)
		xrc = pedigree_html_lib.translateCode(xr)
		answer = 'x-linked recessive'
		N += 1
		bb_output_format = bptools.formatBB_MC_Question(N, xrc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for yl in pedigree_code_templates.y_linked:
		if random.random() < 0.5:
			yl = pedigree_code_lib.mirror_pedigree(yl)
		ylc = pedigree_html_lib.translateCode(yl)
		answer = 'y-linked'
		N += 1
		bb_output_format = bptools.formatBB_MC_Question(N, ylc+question_text, choices_list, answer)
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
	parser = bptools.make_arg_parser(description="Generate questions.", batch=True)


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

	outfile = bptools.make_outfile(None)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#===========================================================
def write_question_batch(start_num: int, args) -> list:
	questions = multipleChoiceQuestionSet(start_num)
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return []
		if len(questions) > remaining:
			questions = questions[:remaining]
	return questions

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
