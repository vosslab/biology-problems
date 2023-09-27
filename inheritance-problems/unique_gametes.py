#!/usr/bin/env python3

# Import required libraries
import os
import argparse

# Import custom modules
import bptools
import genotypelib

# Function to write a question based on the genotype
def write_gametes_question(N, num_genes, hint_flag):
	# Initialize the question string
	question = ""

	# Add contextual information and the actual question text
	question += '<h3>Gamete Diversity in Sexual Reproduction</h3>'
	question += '<p>In sexual reproduction, the potential diversity of gametes &ndash; such as '
	question += 'sperm and eggs in animals, or pollen and ovules in plants &ndash; can be calculated '
	question += 'based on the genotype of an individual.</p>'

	# Add the main question
	question += '<p>How many unique <span style="color: Green;"><strong>GAMETES</strong></span> could be produced'
	question += ' through the process of independent assortment by '
	question += ' an individual with the following genotype?</p> '

	# If hint_flag is True, add a hint
	if hint_flag:
		question += '<p><i>Hint: Remember, each heterozygous gene pair (like `Aa` or `Bb`)'
		question += ' can give rise to two (2) different gametes,'
		question += ' while homozygous pairs (like `AA`, `BB`, and `aa`, `bb`)'
		question += ' can only give rise to one gamete.</i></p>'

	# Calculate the gamete count; ensure it falls within specified range
	gamete_count = 1
	while gamete_count < 4 or gamete_count > 32:
		genotype_code, gamete_count = genotypelib.createGenotype(num_genes)

	# Add genotype to the question
	monospace_genotype_code = bptools.html_monospace(genotype_code)
	question += f'<p><strong>Genotype:</strong>{monospace_genotype_code}</p>'

	# Create a list of answer choices
	choices_list = []
	for power in range(2, 7):
		value = 2**power
		choice = '2<sup>{0:d}</sup> = {1:d}'.format(power, value)
		if hint_flag:
			choice += ' (i.e., {0} genes with two alternative forms each)'.format(bptools.number_to_cardinal(power))
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
	parser.add_argument('--hint', dest='hint', action='store_true', help='Include a hint in the question')
	parser.add_argument('--no-hint', dest='hint', action='store_false', help='Do not include a hint in the question')
	parser.set_defaults(hint=True)  # Set default value for hint

	# Parse the command line arguments
	args = parser.parse_args()

	# Assign parsed arguments to variables
	num_genes = args.num_genes
	num_questions = args.num_questions
	hint_flag = args.hint

	# Initialize question counter
	N = 0

	# Construct output file name based on script name
	output_filename = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'

	# Notify the user about the output file
	print('writing to file: ' + output_filename)

	# Open the output file for writing using a context manager
	with open(output_filename, 'w') as output_file:
		# Loop through to write each question
		for i in range(num_questions):
			N += 1  # Increment the question number
			formatted_question = write_gametes_question(N, num_genes, hint_flag)  # Generate the question
			output_file.write(formatted_question)  # Write the question to the file
	bptools.print_histogram()

