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
	print(metabolic_table)

	# Add the generated metabolic table to the question
	question_text += metabolic_table

	question_text += '<p>In a typical metabolic pathway, an allosteric enzyme is sensitive to changes in concentration of specific molecules and can regulate the rate of reactions.</p>'

	question_text += '<p>Which one of the enzymes in the metabolic pathway above is most likely to be an allosteric enzyme?</p>'

	choices_list = []
	for i in range(num_letters-1):
		choice_str = f'enzyme {i+1}'
		choices_list.append(choice_str)
	answer_text = choices_list[0]

	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
#======================================
#======================================
# Main function that serves as the entry point of the program
if __name__ == '__main__':
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions about metabolic pathways.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-n', '--num_letters', type=int, default=4, help="Number of letters in the metabolic pathway.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 0
		for d in range(args.duplicates):
			N += 1
			complete_question = writeQuestion(N, args.num_letters)
			f.write(complete_question)
			print(complete_question)
