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

#===========================================================
#===========================================================
#The main substrates of chymotrypsin are peptide bonds in which the amino acid N-terminal to the bond is a
#tryptophan, tyrosine, phenylalanine, or leucine, sometimes 'Met', but removed.
# cuts after large hydrophobic amino acid

#chymotrypsin_cleavage_aminos = ['Phe', 'Trp', 'Tyr', 'Leu', 'Met']
chymotrypsin_cleavage_aminos = ['Phe', 'Trp', 'Tyr', 'Leu',]
# use these as distractors
regular_aminos = ['Gly', 'Ala', 'Asn', 'Ser', 'Thr', 'Gln', 'Glu', 'Asp', 'Cys', 'Arg', 'Lys',]
# avoid these for confusion purposes
bad_aminos = ['Pro', 'His', 'Ile', 'Val', ]

dark_color_wheel = {
	'red': 'b30000',
	'brown': '663300',
	'gold': 'b37100',
	'yellow': '999900',
	'green': '008000',
	'cyan': '008080',
	'blue': '002db3',
	'magenta': '800055',
}

amino_acid_colors = {
    'Tyr': 'cyan',
    'Trp': 'cyan',
    'Phe': 'cyan',
    'Leu': 'green',
    'Met': 'green',

	 'Gly': 'brown',
    'Ala': 'brown',
    'Asn': 'magenta',
    'Ser': 'magenta',
    'Thr': 'magenta',
    'Gln': 'magenta',
    'Glu': 'red',
    'Asp': 'red',
    'Cys': 'gold',
    'Lys': 'blue',
    'Arg': 'blue',
}
#===========================================================
#===========================================================

#============================================================
#============================================================
def get_question_text(peptide_sequence: list) -> str:
	"""
	Generate a digestion experiment question involving chymotrypsin cleavage
	of a given peptide sequence.
	"""
	# Convert the peptide sequence to a color-coded HTML representation
	peptide_html_str = peptide_sequence_to_html_str(peptide_sequence)

	# Compose the expanded experiment question using <p> tags
	question = (
		"<p>Your professor provides your group with a peptide that will be the focus "
		"of your next enzymatic digestion experiment. Before performing the reaction, "
		"you are asked to predict where cleavage is most likely to occur under the planned conditions.</p>"

		"<p>The peptide sequence is:<br/>"
		f"<strong>{peptide_html_str}</strong></p>"

		"<p>You will be incubating the peptide with <strong>chymotrypsin</strong> in a buffered solution "
		"at physiological pH. Following digestion, you will analyze the products using mass spectrometry.</p>"

		"<p><strong>Which peptide bond will most likely to be cleaved during the incubation?</strong></p>"
	)
	return question

#============================================================
#============================================================
def peptide_sequence_to_html_str(peptide_sequence: list) -> str:
	"""
	Convert a peptide sequence list into an HTML-formatted string with amino acid coloring.
	"""
	# Create an empty list to accumulate HTML segments
	peptide_html_list = []
	# Convert each amino acid to its color-coded HTML representation
	for amino_acid in peptide_sequence:
		amino_acid_html = bptools.colorHTMLText(
			amino_acid,
			dark_color_wheel[amino_acid_colors[amino_acid]]
		)
		peptide_html_list.append(amino_acid_html)
	# Join the amino acids with HTML em-dash separators, and add N/C-termini
	peptide_html_str = (
		'NH<sub>3</sub><sup>+</sup>&mdash;'
		+ '&mdash;'.join(peptide_html_list)
		+ '&mdash;COO<sup>&ndash;</sup>'
	)
	return peptide_html_str

#============================================================
#============================================================
def make_peptide(peptide_length: int) -> tuple:
	"""
	Generate a synthetic peptide with a single cleavage amino acid placed at a random position.
	No two identical amino acids may be adjacent, and no dipeptide pair may repeat.
	"""
	# Select an amino acid to represent the cleavage site
	cleavage_amino_acid = random.choice(chymotrypsin_cleavage_aminos)

	# Randomly choose an internal position for the cleavage site
	cleavage_site_index = random.randint(2, peptide_length - 2)

	# Initialize the peptide sequence and state tracking
	peptide_sequence = []
	used_pairs = set()
	previous_amino_acid = None

	for position_index in range(peptide_length):
		if position_index == cleavage_site_index:
			amino_acid = cleavage_amino_acid
		else:
			# Filter out invalid choices
			valid_choices = []
			for aa in regular_aminos:
				if aa == previous_amino_acid:
					continue
				if previous_amino_acid is not None:
					dipeptide = (previous_amino_acid, aa)
					if dipeptide in used_pairs:
						continue
				valid_choices.append(aa)

			# If no valid options, raise an error
			if not valid_choices:
				print("No valid amino acid choices available at position:", position_index)
				raise ValueError("Failed to generate peptide: constraints too tight.")

			# Randomly select from filtered list
			amino_acid = random.choice(valid_choices)

			# Record dipeptide pair
			if previous_amino_acid is not None:
				used_pairs.add((previous_amino_acid, amino_acid))

		peptide_sequence.append(amino_acid)
		previous_amino_acid = amino_acid

	return peptide_sequence, cleavage_site_index

#===========================================================
#===========================================================
def format_choice_text(index: int, peptide_sequence: list) -> str:
	"""
	Format a peptide bond between two adjacent amino acids as a color-coded HTML string.
	"""
	# Get the two amino acids at the cleavage site
	amino_acid_1 = peptide_sequence[index]
	amino_acid_2 = peptide_sequence[index + 1]

	# Convert each amino acid to its color-coded HTML representation
	amino_acid_1_html = bptools.colorHTMLText(
		amino_acid_1,
		dark_color_wheel[amino_acid_colors[amino_acid_1]]
	)
	amino_acid_2_html = bptools.colorHTMLText(
		amino_acid_2,
		dark_color_wheel[amino_acid_colors[amino_acid_2]]
	)

	# Concatenate the formatted amino acids with an HTML em-dash between them
	choice_html_text = f"<strong>{amino_acid_1_html}&mdash;{amino_acid_2_html}</strong>"

	return choice_html_text

#===========================================================
#===========================================================
def generate_choices(num_choices: int, peptide_sequence: list, cleavage_site_index: int) -> tuple:
	"""
	Generate multiple-choice answers for a peptide cleavage question.
	"""
	# Initialize list to store all answer choices
	choices_list = []

	# Generate the correct answer: cleavage after a large hydrophobic amino acid
	answer_text = format_choice_text(cleavage_site_index, peptide_sequence)
	choices_list.append(answer_text)

	# Add a plausible distractor: the bond just before the correct one
	wrong1_text = format_choice_text(cleavage_site_index - 1, peptide_sequence)
	choices_list.append(wrong1_text)

	# Build a list of all valid indices excluding correct and adjacent positions
	valid_indices = list(range(len(peptide_sequence) - 1))
	valid_indices.remove(cleavage_site_index)
	valid_indices.remove(cleavage_site_index - 1)

	# Shuffle and select remaining distractors
	random.shuffle(valid_indices)
	for _ in range(num_choices - 2):
		index = valid_indices.pop()
		wrong_text = format_choice_text(index, peptide_sequence)
		choices_list.append(wrong_text)

	# Final shuffle before returning
	random.shuffle(choices_list)

	return choices_list, answer_text

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, num_choices: int, peptide_length: int) -> str:
	"""
	Creates a complete formatted question for output.
	"""
	peptide_sequence, cleavage_site_index = make_peptide(peptide_length)

	# Generate the main question text
	question_text = get_question_text(peptide_sequence)

	# Generate answer choices and the correct answer
	choices_list, answer_text = generate_choices(num_choices, peptide_sequence, cleavage_site_index)

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
#============================================================
#============================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes:
			- duplicates (int): Number of questions to generate.
			- num_choices (int): Number of choices per question.
			- min_length (int): Minimum peptide sequence length (inclusive).
			- max_length (int): Maximum peptide sequence length (inclusive).
	"""
	# Create an argument parser with a description of the script's functionality
	parser = argparse.ArgumentParser(description="Generate peptide digestion questions.")

	# Add an argument to specify how many questions to generate
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create',
		default=99
	)

	# Add an argument to specify the number of answer choices for each question
	parser.add_argument(
		'-c', '--num-choices', type=int, dest='num_choices',
		help="Number of choices to create.",
		default=5
	)

	# Add an argument for minimum peptide length
	parser.add_argument(
		'-m', '--min-length', type=int, dest='min_length',
		help="Minimum peptide sequence length (inclusive).",
		default=7
	)

	# Add an argument for maximum peptide length
	parser.add_argument(
		'-x', '--max-length', type=int, dest='max_length',
		help="Maximum peptide sequence length (inclusive).",
		default=11
	)

	# Parse and return the command-line arguments
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
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		count = 0

		# Generate the specified number of questions
		for _ in range(args.duplicates):
			peptide_length = random.randint(args.min_length,args.max_length)

			# Generate the complete formatted question
			complete_question = write_question(count+1, args.num_choices, peptide_length)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				count += 1
				f.write(complete_question)

	# print a histogram of results
	bptools.print_histogram()

	# Print a message indicating how many questions were saved
	print(f'saved {count} questions to {outfile}')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END

