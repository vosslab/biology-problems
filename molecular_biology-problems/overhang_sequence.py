#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
import sys
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import seqlib
import restrictlib


#==========================
def get_question_header(enzyme_class) -> str:
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))
	web_data = restrictlib.get_web_data(enzyme_class)
	organism = web_data.get('Organism')

	# Intro to restriction enzymes
	opening = (
		f"<p>Restriction enzymes are proteins that cut DNA at specific sequences "
		f"to produce fragments for further study. These enzymes are obtained from "
		f"various types of bacteria and have the ability to recognize short nucleotide "
		f"sequences within a larger DNA molecule.</p>"
	)

	# Specific enzyme context
	setup = (
		f"<p>The restriction enzyme we are focusing on is "
		f"<strong><i>{name}</i></strong>, which is derived from the bacterium {organism}.</p>"
	)

	# Cut site explanation
	cut_info = (
		f"<p><strong><i>{name}</i></strong> cuts the DNA sequence as follows: "
		f"{cut_description}, where the '|' indicates the cleavage site.</p>"
	)

	# Return full question introduction
	question_text = opening + setup + cut_info
	return question_text



#================================================
def makeFillInBlankQuestion(N, enzyme_class):
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))
	web_data = restrictlib.get_web_data(enzyme_class)
	organism = web_data.get('Organism')

	question_text = get_question_header(enzyme_class)
	prompt = (
		f"<p>Based on this information, enter the overhang sequence in the blank below.</p>"
	)
	question_text += prompt

	answer1 = enzyme_class.ovhgseq
	answer2 = f"5'-{answer1}-3'"
	answer3 = f"5&prime;-{answer1}-3&prime;"
	#answer4 = f"5′-{answer1}-3′"
	answer_list = [answer1, answer2, answer3]

	bb_question = bptools.formatBB_FIB_Question(N, question_text, answer_list)
	return bb_question


#================================================
def makeMultipleChoiceQuestion(N, enzyme_class, num_choices):
	name = restrictlib.html_monospace(enzyme_class.__name__)

	question_text = get_question_header(enzyme_class)
	prompt = (
		f"<p>Based on this information, which one of the following sequences below "
		f"corresponds to the overhang region of the DNA after cleavage by "
		f"the restriction enzyme <strong><i>{name}</i></strong>?</p>"
	)
	question_text += prompt


	#A. 5'-TGCA-3' B. 5'-CTGCA-3' C. 5'-TGCAG-3' D. 5'-ACGT-3'
	#print(enzyme_class.ovhgseq)
	#print(enzyme_class.site)
	#print(enzyme_class.elucidate())

	# Compute shift based on overhang length vs full site
	shift = (len(enzyme_class.site) - len(enzyme_class.ovhgseq)) // 2
	#print(shift)

	choices_list = []

	#==========================
	# Distractor: flipped (reversed) overhang sequence
	distractor_flipped_ovhg = f"5'-{seqlib.flip(enzyme_class.ovhgseq)}-3'"
	choices_list.append(distractor_flipped_ovhg)

	# Distractor: site from center to end
	distractor_expanded_right = f"5'-{enzyme_class.site[shift:]}-3'"
	choices_list.append(distractor_expanded_right)

	# Distractor: site from start to center
	distractor_expanded_left = f"5'-{enzyme_class.site[:-shift]}-3'"
	choices_list.append(distractor_expanded_left)

	# Distractor: flipped (reversed) expanded_right
	distractor_flipped_right = f"5'-{seqlib.flip(enzyme_class.site[shift:])}-3'"
	choices_list.append(distractor_flipped_right)

	# Distractor: flipped (reversed) expanded_left
	distractor_flipped_left = f"5'-{seqlib.flip(enzyme_class.site[:-shift])}-3'"
	choices_list.append(distractor_flipped_left)

	#==========================
	# Remove duplicates
	choices_list = list(set(choices_list))

	# Set the correct answer
	answer_text = f"5'-{enzyme_class.ovhgseq}-3'"
	# Ensure the correct answer is not already in the list
	if answer_text in choices_list:
		choices_list.remove(answer_text)

	# Ensure the bad (empty) choice is not in the list
	bad_choice_text = "5'--3'"
	if bad_choice_text in choices_list:
		choices_list.remove(bad_choice_text)

	# Trim to num_choices - 1 (to make space for the correct answer)
	random.shuffle(choices_list)
	choices_list = choices_list[:num_choices - 1]

	# Add the correct answer back
	choices_list.append(answer_text)

	#==========================
	#random.shuffle(choices_list)
	choices_list.sort()

	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_question

#=====================
#=====================
def write_question(N, enzyme_name, num_choices, question_type):
	enzyme_class = restrictlib.enzyme_name_to_class(enzyme_name)
	if not enzyme_class.overhang().endswith('overhang'):
		raise ValueError(f"NON OVERHANG FOUND: {enzyme_name} -- {enzyme_class.overhang()}")
	if question_type == "mc":
		bb_question = makeMultipleChoiceQuestion(N, enzyme_class, num_choices)
	else:
		bb_question = makeFillInBlankQuestion(N, enzyme_class)
	return bb_question

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

	parser.add_argument(
		'-x', '--max-questions', type=int, dest='max_questions',
		default=199, help='Max number of questions'
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
		choices=('fib', 'mc'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)

	# Add a shortcut option to set the question type to multiple choice
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)

	# Add a shortcut option to set the question type to numeric
	question_group.add_argument(
		'-f', '--fib', dest='question_type', action='store_const', const='fib',
		help='Set question type to fill-in-the-blank'
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

	enzyme_names = restrictlib.get_enzyme_list(include_blunt=False)
	print(f"Found {len(enzyme_names)} valid restriction enzymes...")
	random.shuffle(enzyme_names)


	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for enzyme_name in enzyme_names:

			# Generate the complete formatted question
			complete_question = write_question(N+1, enzyme_name, args.num_choices, args.question_type)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)

			if N > args.max_questions:
				break

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

