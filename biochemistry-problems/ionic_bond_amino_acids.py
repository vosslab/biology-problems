#!/usr/bin/env python3

# external python/pip modules
import os
import random
import argparse

# local repo modules
import bptools

positive_amino_acids = ["lysine", "arginine", "histidine", ]
negative_amino_acids = ["aspartic acid", "glutamic acid", 'aspartate', 'glutamate', ]
other_amino_acids = ["alanine", "isoleucine", "leucine", "methionine",
	"phenylalanine", "proline", "tryptophan", "valine",
	"asparagine", "cysteine", "glutamine", "glycine",
	"serine", "threonine", "tyrosine"]

#======================================
#======================================
def get_question_text() -> str:
	"""Generates the question text.

	Returns:
		str: The question text in HTML format.
	"""
	return "<h4>Based on the chemical properties of amino acid side chains, which pair of amino acids listed below can form an ionic bond between their side chains?</h4>"

#======================================
#======================================
def generate_choices(num_choices: int) -> (list, str):
	"""Generates a list of choices and the correct answer text.

	Args:
		num_choices (int): The number of choices to generate.

	Returns:
		list, str: A tuple containing a list of choice strings and the correct answer string.
	"""
	# Define possible choices and wrong choices
	positive_aa = random.choice(positive_amino_acids)
	negative_aa = random.choice(negative_amino_acids)
	two_aas = [positive_aa, negative_aa]
	random.shuffle(two_aas)
	answer_text = f"{two_aas[0].title()} and {two_aas[1].title()}"

	negative_aa = random.choice(negative_amino_acids)
	other_aa = random.choice(other_amino_acids)
	two_aas = [other_aa, negative_aa]
	neg_only = f"{two_aas[0].title()} and {two_aas[1].title()}"

	positive_aa = random.choice(positive_amino_acids)
	other_aa = random.choice(other_amino_acids)
	two_aas = [other_aa, positive_aa]
	pos_only = f"{two_aas[0].title()} and {two_aas[1].title()}"

	other_aa1 = random.choice(other_amino_acids)
	other_aa2 = other_aa1
	while other_aa2 == other_aa1:
		other_aa2 = random.choice(other_amino_acids)
	other_only1 = f"{other_aa1.title()} and {other_aa2.title()}"

	other_aa1 = random.choice(other_amino_acids)
	other_aa2 = other_aa1
	while other_aa2 == other_aa1:
		other_aa2 = random.choice(other_amino_acids)
	other_only2 = f"{other_aa1.title()} and {other_aa2.title()}"

	choices_list = [answer_text, neg_only, pos_only, other_only1, other_only2]
	# Shuffle choices for presentation
	random.shuffle(choices_list)

	return choices_list, answer_text

#======================================
#======================================
def write_question(N: int, num_choices: int) -> str:
	"""Creates a complete formatted question.

	Args:
		N (int): The question number.
		num_choices (int): The number of choices for the question.

	Returns:
		str: The complete formatted question.
	"""
	assert N > 0, "Question number must be positive"
	assert num_choices >= 2, "Number of choices must be at least 2"

	# Add more to the question based on the given letters
	question_text = get_question_text()

	# Choices and answers
	choices_list, answer_text = generate_choices(num_choices)

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-n', '--num_choices', type=int, default=5, help="Number of choices to create.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 0
		for d in range(args.duplicates):
			N += 1
			complete_question = write_question(N, args.num_choices)
			f.write(complete_question)
	bptools.print_histogram()


#======================================
#======================================
if __name__ == '__main__':
	main()
