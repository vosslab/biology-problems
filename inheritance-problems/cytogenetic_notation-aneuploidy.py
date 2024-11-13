#!/usr/bin/env python3

# built-in python modules
import os
import random
import argparse

# external pip modules

# local repo modules
import bptools

def get_karyotype():
	chromosome_count = 46
	sex_chromosome_list = ['X'] + [random.choice(['X', 'Y'])]

	# Chromosome numbers for human (1-22 autosomes and sex chromosomes X, Y)
	chromosome_list = [str(i) for i in range(1, 23)] + ['X', 'Y']

	# Step 1: Choose aneuploid karyotype
	ploidy_change = random.choice(["+", "-"])  # One more or one less
	chromosome = random.choice(chromosome_list)  # Random chromosome choice

	# Ensure females cannot "lose" a Y chromosome
	if ploidy_change == "-" and chromosome == 'Y' and 'Y' not in sex_chromosome_list:
		chromosome = 'X'  # Switch to X if chromosome loss would be invalid

	# Update karyotype based on the ploidy change
	if ploidy_change == "+":
		chromosome_count += 1
		if chromosome in 'XY':
			sex_chromosome_list.append(chromosome)
			base_karyotype = f"{chromosome_count}"
		else:
			base_karyotype = f"{chromosome_count},{ploidy_change}{chromosome}"
	elif ploidy_change == "-":
		chromosome_count -= 1
		if chromosome in 'XY' and chromosome in sex_chromosome_list:
			sex_chromosome_list.remove(chromosome)
			base_karyotype = f"{chromosome_count}"
		else:
			base_karyotype = f"{chromosome_count},{ploidy_change}{chromosome}"

	# Sort and join sex chromosomes
	sex_chromosome_str = ''.join(sorted(sex_chromosome_list))
	full_karyotype_str = f'{base_karyotype},{sex_chromosome_str}'
	karyotype_tuple = (chromosome_count, sex_chromosome_list, ploidy_change, chromosome)
	return full_karyotype_str, karyotype_tuple

#======================================
#======================================
# Function to generate varied question text
def get_question_text(karyotype_str) -> str:
	"""
	Generates and returns the main text for the question with varied phrasing.

	This function is responsible for creating the base question text,
	randomly selecting from different ways to ask about the meaning
	of the cytogenetic notation.

	Returns:
		str: A string containing the main question text.
	"""
	phrases = [
		f'For human karyotypes, what does the cytogenetic notation "{karyotype_str}" refer to?',
		f'In human genetics, what does the notation "{karyotype_str}" indicate?',
		f'In cytogenetic terms, what is meant by the human karyotype "{karyotype_str}"?',
		f'What does the notation "{karyotype_str}" describe in human karyotypes?',
		f'What does "{karyotype_str}" signify in a human karyotype?',
		f'In the context of human karyotypes, what does "{karyotype_str}" mean?',
		f'How is the notation "{karyotype_str}" interpreted in human genetics?',
		f'What does "{karyotype_str}" imply in terms of human chromosome structure?',
	]
	question_text = random.choice(phrases)
	return question_text

#======================================
#======================================
def sex_chromosomes_to_gender(sex_chromosome_list):
	if 'Y' in sex_chromosome_list:
		return 'male'
	return 'female'

import random

#======================================
#======================================
def ploidy_change_to_text(ploidy_change):
	"""
	Generates text describing the correct ploidy change in the karyotype.
	"""
	if ploidy_change == '+':
		base_text = random.choice(['with an extra', 'with an additional', 'with an added'])
	else:
		base_text = random.choice(['with a missing', 'lacking', 'with an absent'])
	#optional "copy of" at the end.
	base_text += random.choice([' copy of', ''])
	return base_text

#======================================
#======================================
def wrong_ploidy_change_to_text(ploidy_change):
	"""
	Generates text describing incorrect or misleading ploidy change options for distractors.
	"""
	if ploidy_change == '+':
		return random.choice(['with an extra pair of', 'with a partial duplication of', 'with two extra copies of'])
	return random.choice(['with a partial deletion of',])


#======================================
#======================================
def generate_choices(karyotype_tuple: tuple, num_choices: int) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer for a cytogenetic question.

	Args:
		karyotype (str): The karyotype notation to interpret.
		num_choices (int): The total number of answer choices to generate.

	Returns:
		tuple: A tuple containing:
			- list: A list of answer choices (mixed correct and incorrect).
			- str: The correct answer text.
	"""
	# Parse the karyotype to determine correct answer
	(chromosome_count, sex_chromosome_list, ploidy_change, chromosome) = karyotype_tuple
	answer_gender = sex_chromosomes_to_gender(sex_chromosome_list)
	ploidy_text = ploidy_change_to_text(ploidy_change)


	gender_choices = ['male', 'female']
	ploidy_choices = ['+', '-']
	#chromosome_choices = [str(i) for i in range(1, 23) if str(i) != chromosome] + ['X', 'Y']

	# Generate distractors by modifying gender and ploidy text
	# this will only generate 3 distractors and 1 answer text
	# chromosome change would be too obvious
	answer_text = None
	distractors = []
	for gender in gender_choices:
		for ploidy in ploidy_choices:
			ploidy_text = ploidy_change_to_text(ploidy)
			choice_text = f"This indicates a {gender} human karyotype {ploidy_text} chromosome {chromosome}."
			if gender == answer_gender and ploidy == ploidy_change:
				answer_text = choice_text
			else:
				distractors.append(choice_text)
			wrong_ploidy_text = wrong_ploidy_change_to_text(ploidy)
			choice_text = f"This indicates a {gender} human karyotype {wrong_ploidy_text} chromosome {chromosome}."
			distractors.append(choice_text)


	if answer_text is None:
		raise ValueError("Something went wrong: answer text not created.")

	#Base choice "This indicates a {gender} human karyotype with {extra/missing} chromosome {chromosome}"
	#print(distractors)
	distractors = list(set(distractors))
	random.shuffle(distractors)
	if len(distractors) > num_choices - 1:
		distractors = distractors[:num_choices-1]

	# Combine the correct answer with distractors and shuffle
	choices_list = [answer_text] + distractors
	choices_list = list(set(choices_list))
	random.shuffle(choices_list)


	return choices_list, answer_text


#======================================
#======================================
def write_question(N: int, num_choices: int) -> str:
	"""
	Creates a complete formatted question for output.

	This function combines the question text and choices generated by
	other functions into a formatted question string. The formatting
	is handled by a helper function from the `bptools` module.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string suitable for output, containing
		the question text, answer choices, and correct answer.
	"""
	karyotype_str, karyotype_tuple = get_karyotype()

	# Generate the question text
	question_text = get_question_text(karyotype_str)

	# Generate answer choices and correct answer
	choices_list, answer_text = generate_choices(karyotype_tuple, num_choices)

	# Format the complete question with the specified module function
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
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
		'-c', '--num_choices', type=int, default=5,
		help="Number of choices to create."
	)

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.

	This function uses parsed command-line arguments to control the number
	of questions to generate, the type of question (multiple choice or numeric),
	and the number of answer choices per question. It creates a formatted output
	file with all generated questions, and calls a helper function to display
	a histogram for multiple-choice questions.
	"""
	# Parse arguments from the command line
	args = parse_arguments()

	# Setup output file name
	outfile = f'bbq-{os.path.splitext(os.path.basename(__file__))[0]}-questions.txt'
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			complete_question = write_question(N, args.num_choices)
			continue
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram if question type is multiple choice
	bptools.print_histogram()

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
