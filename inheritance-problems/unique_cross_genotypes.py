#!/usr/bin/env python3

# Import required libraries
import os
import random
import argparse

# Import custom modules
import bptools
import genotypelib

def generate_choices(total_genotypes, num_genes, max_choices, hint_flag):
	# Decompose total_genotypes into its components based on 2 and 3 powers
	power2, power3 = genotypelib.deconstructPowerOfNumber(total_genotypes)

	# Generate the formatted choice text for the answer
	answer_string = genotypelib.format_choice_plus(power2, power3, hint_flag)

	# Create a tuple holding the total_genotypes and the formatted choice text
	answer_tuple = (total_genotypes, answer_string)

	# Initialize an empty list to store choices as tuples
	choices_tuple_list = []

	# Loop through possible power differences to generate choices
	for diff_power2 in range(-2, 3):
		for diff_power3 in range(-2, 3):
			# Skip generating a choice that is the same as the answer
			if diff_power2 == 0 and diff_power3 == 0:
				continue

			# Calculate new powers based on the differences
			npow2 = power2 + diff_power2
			npow3 = power3 + diff_power3

			# Skip invalid or unrealistic scenarios
			if npow2 < 0 or npow3 < 0:
				continue
			if npow2 + npow3 > num_genes:
				continue
			if npow2 + npow3 < 2:
				continue

			# Calculate the number of genotypes based on new powers
			num = 2**npow2 * 3**npow3

			# Generate the formatted choice text for these new powers
			choice_text = genotypelib.format_choice_plus(npow2, npow3, hint_flag)

			# Append the tuple (number, choice_text) to the choices list
			choices_tuple_list.append((num, choice_text))

	# Shuffle choices and truncate list to max_choices - 1
	random.shuffle(choices_tuple_list)
	choices_tuple_list = choices_tuple_list[:max_choices-1]

	# Add the actual answer to the list
	choices_tuple_list.append(answer_tuple)

	# Sort the choices based on the numbers
	choices_tuple_list.sort()

	# Initialize list for storing final choices and find the answer_string
	choices_list = []
	for i, choice_tuple in enumerate(choices_tuple_list):
		value, choice_text = choice_tuple
		choices_list.append(choice_text)

	# Return the list of choices and the correct answer string
	return choices_list, answer_string


# Function to write a genotype-based question
def write_genotype_question(N, num_genes, max_choices, hint_flag):
	# Initialize the question string
	question = ""

	# Add contextual information and the actual question text
	question += '<h3>Genotype Diversity in Hybrid Cross</h3>'
	question += '<p>In a hybrid cross, the range of possible genotypes in the offspring is determined '
	question += 'by the genetic makeup of the parental organisms.</p>'

	question += "<p>Assume that all genes sort independently and display complete dominance.</p>"

	if hint_flag:
		question += '<p><i>Hint: For each gene pair from the parents, you can get 1, 2, or 3 unique genotypes.'
		question += '<br/>This is based on the combinations: homozygous x homozygous (1), '
		question += 'homozygous x heterozygous (2), and heterozygous x heterozygous (3).</i></p>'

	question += '<p>Considering the principle of independent assortment, how many unique '
	question += '<span style="color: MediumBlue;"><strong>GENOTYPES</strong></span> could be '
	question += 'produced in a hybrid cross between the following individuals?</p>'

	# Generate genotypes and counts for two parents, within specified range
	gamete_count1 = 1
	while gamete_count1 < 2 or gamete_count1 > 16:
		gene_list1 = genotypelib.createGenotypeList(num_genes)
		geno1, gamete_count1 = genotypelib.createGenotypeStringFromList(gene_list1)
	gamete_count2 = 1
	while gamete_count2 < 2 or gamete_count2 > 16:
		gene_list2= genotypelib.createGenotypeList(num_genes)
		geno2, gamete_count2 = genotypelib.createGenotypeStringFromList(gene_list2)
	total_genotypes = genotypelib.countGenotypesForCross(gene_list1, gene_list2)

	# Randomly order parent genotypes
	monospace_geno1 = bptools.html_monospace(geno1)
	monospace_geno2 = bptools.html_monospace(geno2)

	# Randomly decide the order of genotypes for male and female
	male_row = "<tr><td style='padding-left: 10px; padding-right: 10px;'>Male (&male;)</td>"
	male_row += f"<td style='padding-left: 10px; padding-right: 10px;'>{monospace_geno1}</td></tr>"
	female_row = "<tr><td style='padding-left: 10px; padding-right: 10px;'>Female (&female;)</td>"
	female_row += f"<td style='padding-left: 10px; padding-right: 10px;'>{monospace_geno2}</td></tr>"

	# Conditionally set the order of the rows
	if random.random() < 0.5:
		rows = male_row + female_row
	else:
		rows = female_row + male_row

	# Construct the table as a single string
	table = "<table style='border-collapse: collapse; border: 1px solid black;'>"
	table += f"<tbody>{rows}</tbody></table>"
	#print(table)

	# Add the table to the question
	question += table

	# Create multiple choice options
	choices_list, answer_string = generate_choices(total_genotypes, num_genes, max_choices, hint_flag)

	# Format question for Blackboard and write to file
	bbformat = bptools.formatBB_MC_Question(N, question, choices_list, answer_string)

	return bbformat



if __name__ == '__main__':
	# Initialize argparse for command line arguments
	parser = argparse.ArgumentParser(description='Generate blackboard questions.')

	# Add command line options for number of genes and number of questions
	parser.add_argument('-n', '--num_genes', type=int, default=6, help='Number of genes')
	parser.add_argument('-x', '--num_questions', type=int, default=24, help='Number of questions')
	parser.add_argument('-c', '--max_choices', type=int, default=5, help='Number of choices')
	parser.add_argument('--hint', dest='hint', action='store_true', help='Include a hint in the question')
	parser.add_argument('--no-hint', dest='hint', action='store_false', help='Do not include a hint in the question')
	parser.set_defaults(hint=True)  # Set default value for hint

	# Parse the command line arguments
	args = parser.parse_args()

	# Assign parsed arguments to variables
	num_genes = args.num_genes
	num_questions = args.num_questions
	max_choices = args.max_choices
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
			formatted_question = write_genotype_question(N, num_genes, max_choices, hint_flag)  # Generate the question
			output_file.write(formatted_question)  # Write the question to the file
	bptools.print_histogram()

