#!/usr/bin/env python3

import os
import copy
import random
import argparse

import bptools
import metaboliclib

#======================================
#======================================
# Generate a multiple-choice question about metabolic pathways
def writeQuestion(N, num_letters=4):
	# Create the question stem and generate the metabolic pathway table
	question_text = '<p>A series of enzymes catalyze the reactions in the following metabolic pathway:</p>'
	metabolic_table = metaboliclib.generate_metabolic_pathway(num_letters, N)
	letters = metaboliclib.get_letters(num_letters, N)
	#print(metabolic_table)

	# Add the generated metabolic table to the question
	question_text += metabolic_table

	question_text += '<p>In a typical metabolic pathway, an allosteric enzyme is sensitive to changes in concentration of specific molecules and can regulate the rate of reactions.</p>'

	question_text += '<p>Which one of the enzymes in the metabolic pathway above is most likely to be an allosteric enzyme?</p>'

	choices_list = []
	for i in range(num_letters-1):
		choice_str = f'<strong>enzyme {i+1}</strong> '
		choice_str += f'that catalyzes the reaction from substrate {letters[i]} to product {letters[i+1]}'
		choices_list.append(choice_str)
	answer_text = choices_list[0]

	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
#======================================
#======================================
# Main function that serves as the entry point of the program
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions about metabolic pathways.")
	parser.add_argument('-d', '--duplicates', type=int, default=99, help="Number of questions to create.")
	parser.add_argument('-n', '--num_letters', type=int, default=6, help="Number of letters in the metabolic pathway.")
	args = parser.parse_args()

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
			# Generate the complete formatted question
			complete_question = writeQuestion(N+1, args.num_letters)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)

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

