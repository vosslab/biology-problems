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


# genotypes are dominant first, because female / male are interchangable in this context
PUNNETT_CONTEXTS = [
	("AA x AA", "a cross of two different true-breeding purple flower plants?"),

	("AA x Aa", "a backcross between a true-breeding purple flower plant from the P generation and a purple F<sub>1</sub> hybrid plant?"),
	("AA x Aa", "a cross between a true-breeding purple-flowered plant and a purple hybrid from the F<sub>1</sub> generation?"),

	("AA x aa", "the first cross between the parental generation to produce the F<sub>1</sub> hybrids in a monohybrid cross?"),
	("AA x aa", "a cross between a true-breeding purple flower plant and a true-breeding white flower plant?"),
	("AA x aa", "a monohybrid cross between two true-breeding parents, one with purple dominant and one with white recessive phenotypes?"),

	("Aa x Aa", "the cross between the hybrids of the F<sub>1</sub> generation to produce the F<sub>2</sub> generation in a monohybrid cross?"),
	("Aa x Aa", "the cross between two different F<sub>1</sub> hybrid plants that have purple flowers?"),
	("Aa x Aa", "a cross between two purple-flowered plants, both from the F<sub>1</sub> generation?"),
	("Aa x Aa", "a mating between two F<sub>1</sub> hybrids that each came from true-breeding purple and white parents?"),

	("Aa x aa", "a backcross between a true-breeding white flower plant from the P generation and a purple F<sub>1</sub> hybrid plant?"),
	("Aa x aa", "a backcross between a purple F<sub>1</sub> hybrid plant and a true-breeding white flower plant?"),

	("aa x aa", "a cross of two different white flower plants of unknown genotype?"),
	("aa x aa", "a cross between two true-breeding white-flowered plants?"),
]

#===========================================================
#===========================================================
# This function generates and returns the main question text.
def get_question_text(N) -> tuple:
	"""
	Generates and returns the main text for the question.
	"""
	# Initialize an empty string for the question text
	# Shared Mendel intro
	MENDEL_INTRO = (
		"In his experiments, Mendel discovered that the purple flower phenotype "
		"was dominant to the white flower phenotype."
	)

	# Shared ending prompt
	PUNNETT_PROMPT = (
		"Which one of the following Punnett squares represents "
	)

	context_tuple = PUNNETT_CONTEXTS[N % len(PUNNETT_CONTEXTS)]
	answer_genotypes_key = context_tuple[0]
	context = context_tuple[1]
	question_text = f"{MENDEL_INTRO}\n\n{PUNNETT_PROMPT}{context}"

	# Return the complete question text
	return question_text, answer_genotypes_key


#==========================
def get_cell_html(geno: str) -> str:
	"""
	Returns HTML <td> for a given genotype with color formatting.

	Args:
		geno (str): Genotype string (e.g., 'AA', 'Aa', 'aa').

	Returns:
		str: HTML string for one cell of the Punnett square.
	"""
	if geno == 'AA':
		return '<td align="center" bgcolor="black"><span style="color: #f8f8f8; font-family: monospace;">AA</span></td>'
	elif geno in ['Aa', 'aA']:
		return '<td align="center" bgcolor="#777"><span style="color: #f8f8f8; font-family: monospace;">Aa</span></td>'
	elif geno == 'aa':
		return '<td align="center" bgcolor="#CCC"><span style="color: #080808; font-family: monospace;">aa</span></td>'
	raise ValueError

#==========================
def make_punnett_square_html(female_geno: str, male_geno: str) -> str:
	"""
	Generates HTML table for a Punnett square given two parental genotypes.

	Args:
		female_geno (str): Genotype of the female parent (e.g., 'Aa').
		male_geno (str): Genotype of the male parent (e.g., 'Aa').

	Returns:
		str: HTML string representing the Punnett square.
	"""
	female_alleles = list(female_geno)
	male_alleles = list(male_geno)

	html = '<table border="1" cellpadding="4" cellspacing="0" style="margin: 2px; border-collapse: collapse;">'

	# Header row: male alleles
	html += '<tr><td></td>'
	for allele in male_alleles:
		html += f'<td align="center"><span style="font-family: monospace; font-weight: bold;">{allele}</span></td>'
	html += '</tr>'

	# Rows: female alleles
	for fa in female_alleles:
		html += f'<tr><td align="center"><span style="font-family: monospace; font-weight: bold;">{fa}</span></td>'
		for ma in male_alleles:
			child_geno = ''.join(sorted([fa, ma]))
			html += get_cell_html(child_geno)
		html += '</tr>'

	html += '</table><br/>'
	return html

#==========================
def generate_choices() -> str:
	"""
	Generates HTML for all 6 unique single-gene Punnett squares with color coding.

	Returns:
		str: Combined HTML for all Punnett squares in a flex container.
	"""
	genotype_pairs = [
		('AA', 'AA'),
		('AA', 'Aa'),
		('AA', 'aa'),
		('Aa', 'Aa'),
		('Aa', 'aa'),
		('aa', 'aa'),
	]

	all_punnett_squares_html_dict = {}

	for female, male in genotype_pairs:
		assert [female,male] == sorted([female,male])
		genotype_key = f"{female} x {male}"
		punnett_html = make_punnett_square_html(female, male)
		all_punnett_squares_html_dict[genotype_key] = punnett_html
	return all_punnett_squares_html_dict

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, all_punnett_squares_html_dict: dict) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Generate the main question text
	question_text, answer_genotypes_key = get_question_text(N)

	# Generate answer choices and the correct answer
	choices_list = [all_punnett_squares_html_dict[key] for key in sorted(all_punnett_squares_html_dict)]
	answer_text = all_punnett_squares_html_dict[answer_genotypes_key]

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Generate the output file name based on the script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'  # Add the script name to the file name
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	all_punnett_squares_html_dict = generate_choices()

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for _ in range(len(PUNNETT_CONTEXTS)):

			# Generate the complete formatted question
			complete_question = write_question(N+1, all_punnett_squares_html_dict)

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
