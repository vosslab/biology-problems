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
import disorderlib

#sample question:
#  A man (&male;) with both hemophilia and Huntington's disease marries
#    a normal phenotype woman (&female;) without either disease.
#  The man's (&male;) father also had Huntington's disease, but not his mother.
#  The woman's (&female;) father suffered from hemophilia, but her mother did not.
#  Huntington's disease is autosomal dominant, and hemophilia is X-linked recessive.

# step 1: pick a dominant disease
# step 2: pick a X-linked disease; mother is a carrier

#easy, ask the genotype of one of the individuals
#hard, ask a compounded question: What fraction of their sons (&male;) will suffer from Huntington's disease AND hemophilia?
#hard, ask a compounded question: What fraction of their daughters (&female;) will suffer from Huntington's disease AND hemophilia?

#A. None, 0%
#B. 1/4, 25%
#C. 1/2, 50%
#D. 3/4, 75%
#E. All, 100%

#=====================
#=====================
#=====================
def write_question(N):
	md = disorderlib.MultiDisorderClass()

	# Pick one random X-linked recessive disorder (name and its data dictionary)
	XLR_disorder_name, XLR_disorder_dict = random.choice(
		list(md.disorder_data['X-linked recessive'].items())
	)
	# Get the paragraph description for the chosen X-linked recessive disorder
	XLR_description = md.getDisorderParagraph(XLR_disorder_dict)
	# Get the short name (abbreviation) for the disorder
	XLR_short_name = md.getDisorderShortName(XLR_disorder_dict)

	# Pick one random autosomal dominant disorder (name and its data dictionary)
	AD_disorder_name, AD_disorder_dict = random.choice(
		list(md.disorder_data['autosomal dominant'].items())
	)
	# Get the paragraph description for the chosen autosomal dominant disorder
	AD_description = md.getDisorderParagraph(AD_disorder_dict)
	# Get the short name (abbreviation) for the disorder
	AD_short_name = md.getDisorderShortName(AD_disorder_dict)

	# Start building the HTML question text
	question_text = ''
	# Include the X-linked recessive disorder description
	question_text += f'<p>{XLR_description}</p>'
	# Include the autosomal dominant disorder description
	question_text += f'<p>{AD_description}</p>'
	# Describe the family background and genetic status of the man
	question_text += f'<p>A man (&male;) with both {XLR_short_name} and {AD_short_name} genetic disorders marries '
	question_text += 'a wild-type phenotype woman (&female;) with neither disorder. '
	# State the woman's father has the X-linked recessive disorder, but her mother does not
	question_text += f'The father (&male;) of the woman has the {XLR_short_name} genetic disorder,'
	question_text += 'but mother (&female;) of the woman does not. '
	# Randomly pick which parent of the man is wild-type for the autosomal dominant disorder
	parent = random.choice(('father (&male;)', 'mother (&female;)'))
	question_text += f'The {parent} of the man is wild-type phenotype and does not have the {AD_short_name} genetic disorder.</p> '

	# Add a reminder about which disorder is which type
	question_text += f'<p>Reminder: {XLR_short_name} is {XLR_disorder_dict["type"]} and {AD_short_name} is {AD_disorder_dict["type"]}.</p>'

	# Randomly choose whether the question asks about daughters or sons
	offspring_gender = random.choice(['daughters (&female;)' , 'sons (&male;)'])
	# Ask what fraction of those offspring will have both disorders
	question_text += f'<p>What fraction of their {offspring_gender} will have both {XLR_short_name} and {AD_short_name} genetic disorders?</p>'

	# Get the standard multiple-choice list of answer options
	choices_list = md.getStandardChoicesList()
	# Set the correct answer (currently fixed, not computed dynamically)
	answer_text = '1/4, 25%'
	# Format the Blackboard multiple-choice question using the helper function
	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Return the fully formatted question
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
		# Create a full formatted question (Blackboard format)
		complete_question = write_question(N+1)

		# Append question if successfully generated
		if complete_question is not None:
			N += 1
			question_bank_list.append(complete_question)

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


