#!/usr/bin/env python3

# Import required libraries
import os
import argparse

# Import custom modules
import bptools
import genotype

# Function to write a question based on the genotype
def writeQuestion(N, num_genes):
	# Initialize the question string
	question = ""

	# Add the introductory text to the question
	question += '<p>How many unique <span style="color: Green;"><strong>GAMETES</strong></span> '
	question += 'could be produced through independent assortment by '
	question += 'an individual with the following genotype?</p> '

	# Calculate the gamete count; ensure it falls within specified range
	gamete_count = 1
	while gamete_count < 4 or gamete_count > 32:
		geno, gamete_count = genotype.createGenotype(num_genes)

	# Add genotype to the question
	question += '<p><code>{0}</code></p>'.format(geno)

	# Create a list of answer choices
	choices_list = []
	for power in range(2, 7):
		value = 2**power
		choice = "2<sup>{0:d}</sup> = {1:d}".format(power, value)
		choices_list.append(choice)
		if value == gamete_count:
			answer = choice

	# Format the question using Blackboard-compatible markup
	bbformat = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbformat


# Main execution starts here
if __name__ == '__main__':
	# Initialize argparse for command line arguments
	parser = argparse.ArgumentParser(description='Generate blackboard questions.')

	# Add command line options for number of genes and number of questions
	parser.add_argument('-n', '--num_genes', type=int, default=7, help='Number of genes')
	parser.add_argument('-x', '--num_questions', type=int, default=24, help='Number of questions')

	# Parse the command line arguments
	args = parser.parse_args()

	# Assign parsed arguments to variables
	num_genes = args.num_genes
	num_questions = args.num_questions

	# Initialize question counter
	question_counter = 0

	# Construct output file name based on script name
	output_filename = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'

	# Notify the user about the output file
	print('writing to file: ' + output_filename)

	# Open the output file for writing using a context manager
	with open(output_filename, 'w') as output_file:
		# Loop through to write each question
		for i in range(num_questions):
			question_counter += 1  # Increment the question number
			formatted_question = writeQuestion(question_counter, num_genes)  # Generate the question
			output_file.write(formatted_question)  # Write the question to the file

