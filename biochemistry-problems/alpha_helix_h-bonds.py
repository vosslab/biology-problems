#!/usr/bin/env python3

import os
import copy
import random
import argparse

import bptools

def format_amino_acid(amino_acid_num):
	return f"amino acid {amino_acid_num:d}"

def format_amino_acid_pair(amino_acid_num, shift):
	choice_text = ""
	choice_text += f"amino acids {amino_acid_num-shift:d} "
	choice_text += f"and {amino_acid_num+shift:d} "
	if shift > 1:
		choice_text += f"(a residue shift of {shift} positions)"
	else:
		choice_text += f"(a residue shift of {shift} position)"
	return choice_text

def get_choices_mc(amino_acid_num, num_choices):
	shift = 4
	answer_text = format_amino_acid_pair(amino_acid_num, shift)

	choices_list = []
	choices_list.append(answer_text)

	for shift in (2,3,5):
		choice = format_amino_acid_pair(amino_acid_num, shift)
		choices_list.append(choice)

	extra_choices = []
	for shift in (1,6,7,8):
		if shift >= amino_acid_num:
			continue
		choice = format_amino_acid_pair(amino_acid_num, shift)
		extra_choices.append(choice)
	random.shuffle(extra_choices)
	while len(choices_list) < num_choices:
		choices_list.append(extra_choices.pop())
	choices_list = list(set(choices_list))
	print(choices_list)
	#choices_list.sort()
	sorted_amino_list = sorted(choices_list, key=lambda x: int(x.split()[-2]))
	return sorted_amino_list, answer_text

def get_choices_ma(amino_acid_num, num_choices):

	shift = 4
	answers_list = [
		format_amino_acid(amino_acid_num - shift),
		format_amino_acid(amino_acid_num + shift),
	]

	choices_list = copy.copy(answers_list)
	for shift in (2,3,5):
		choices_list.append(format_amino_acid(amino_acid_num - shift))
		choices_list.append(format_amino_acid(amino_acid_num + shift))

	extra_choices = []
	for shift in (1,6,7,8):
		if shift >= amino_acid_num:
			continue
		extra_choices.append(format_amino_acid(amino_acid_num - shift))
		extra_choices.append(format_amino_acid(amino_acid_num + shift))
	random.shuffle(extra_choices)
	while len(choices_list) < num_choices:
		choices_list.append(extra_choices.pop())
	choices_list = list(set(choices_list))
	print(choices_list)
	sorted_amino_list = sorted(choices_list, key=lambda x: int(x.split()[-1]))
	return sorted_amino_list, answers_list

def write_question(N, num_choices, question_type):
	amino_acid_num = random.randint(6,9)
	question_statement = ""
	question_statement += "<p>The &alpha;-helix is a right-handed coil in which "
	question_statement += "each backbone N&ndash;H group forms a hydrogen bond with "
	question_statement += "the C=O group of an amino acid located a few residues away. "
	question_statement += "The regular pattern of hydrogen bonding stabilizes the helix, "
	question_statement += "preventing it from unraveling.</p> "
	question_statement += f"<p>In a long &alpha;-helix, amino acid <b>number {amino_acid_num}</b>"
	question_statement += " would form a hydrogen bond with which two other amino acids?</p>"

	if question_type == "mc":
		question_statement += "<p>Select the correct pair of amino acids below.</p>"
		choices_list, answer_text = get_choices_mc(amino_acid_num, num_choices)
		complete_question = bptools.formatBB_MC_Question(N, question_statement, choices_list, answer_text)
	elif question_type == "ma":
		question_statement += "<p>Select two correct answers.</p>"
		choices_list, answers_list = get_choices_ma(amino_acid_num, num_choices)
		complete_question = bptools.formatBB_MA_Question(N, question_statement, choices_list, answers_list)
	else:
		raise ValueError

	return complete_question


#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create', default=1
	)
	parser.add_argument(
		'-c', '--num_choices', type=int, default=5, dest='num_choices',
		help="Number of choices to create."
	)

	# Create a mutually exclusive group for question type and make it required
	question_group = parser.add_mutually_exclusive_group(required=True)
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('ma', 'mc'),
		help='Set the question type: ma (multiple answer) or mc (multiple choice)'
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)
	question_group.add_argument(
		'-a', '--ma', dest='question_type', action='store_const', const='ma',
		help='Set question type to multiple answer'
	)

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Define output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'
		f'-{args.question_type.upper() }'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			complete_question = write_question(N, args.num_choices, args.question_type)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram if question type is multiple choice
	bptools.print_histogram()
	print(f'saved {N} questions to {outfile}')

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
