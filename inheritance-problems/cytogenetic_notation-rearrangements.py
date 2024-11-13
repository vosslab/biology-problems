#!/usr/bin/env python3

# built-in python modules
import os
import random
import argparse

# external pip modules

# local repo modules
import bptools

#======================================
#======================================
#======================================
# Helper function to generate chromosomal rearrangement karyotypes
def get_karyotype():
	base_karyotype = random.choice(["46,XY", "46,XX"])
	rearrangement_type = random.choice(["del", "dup", "inv", "t"])

	# Reinitialize and shuffle the chromosome list within each function call
	all_chromosomes_list = [str(i) for i in range(1, 23)]
	random.shuffle(all_chromosomes_list)

	chromosome = all_chromosomes_list.pop()  # Unique chromosome
	arm = random.choice(["p", "q"])  # Short or long arm
	band = all_chromosomes_list.pop()  # Unique band from remaining list

	# Format rearrangement notation
	if rearrangement_type == "t":
		# Translocation requires a second chromosome and arm
		chromosome2 = all_chromosomes_list.pop()
		arm2 = random.choice(["p", "q"])
		band2 = all_chromosomes_list.pop()
		rearrangement = f"t({chromosome};{chromosome2})({arm}{band};{arm2}{band2})"
		karyotype_tuple = rearrangement_type, chromosome, arm, band, chromosome2, arm2, band2
	else:
		# Other types use a single chromosome and arm notation
		rearrangement = f"{rearrangement_type}({chromosome}{arm}{band})"
		karyotype_tuple = rearrangement_type, chromosome, arm, band

	full_karyotype_str = f"{base_karyotype},{rearrangement}"
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
def arm_text(arm):
	if arm == 'q':
		return "long"
	return "short"

#======================================
#======================================
def rearrangement_text(rearrangement_type):
	if rearrangement_type == 't':
		return "A translocation"
	elif rearrangement_type == 'dup':
		return "A duplication"
	elif rearrangement_type == 'del':
		return "A deletion"
	elif rearrangement_type == 'inv':
		return "An inversion"
	raise ValueError(f"Unknown rearrangement_type {rearrangement_type}")


#======================================
#======================================
# Helper function to generate the choice text with tolerance for unexpected tuple lengths
def make_choice_text_regular(karyotype_tuple):
	if len(karyotype_tuple) != 4:
		raise ValueError("length of tuple must be 4 to use make_choice_text_regular()")
	# Unpack mandatory fields
	rearrangement_type, chromosome, arm, band = karyotype_tuple
	# Non-translocation rearrangement (del, dup, inv)
	choice_text = f"{rearrangement_text(rearrangement_type)} "
	choice_text += f"involving the {arm_text(arm)} arm "
	choice_text += f"of chromosome {chromosome} at band {band}"
	return choice_text

#======================================
#======================================
#======================================
# Function to generate all possible answer choices
def generate_choices_regular(karyotype_tuple):
	if len(karyotype_tuple) != 4:
		raise ValueError("length of tuple must be 4 to use generate_choices_regular()")

	rearrangement_type, chromosome, arm, band = karyotype_tuple

	# Generate plausible distractors
	distractors = []

	# Options for generating distractors
	arm_options = ["p", "q"]
	rearrangement_options = ["del", "dup", "inv", "t"]
	# Choose between correct chromosome and placeholder band
	chromosome_options = [chromosome, band]

	# Create all possible distractors
	for type_choice in rearrangement_options:
		for chromosome_choice in chromosome_options:
			for arm_choice in arm_options:
				band_choice = band if chromosome_choice == chromosome else chromosome
				choice_tuple = type_choice, chromosome_choice, arm_choice, band_choice
				choice_text = make_choice_text_regular(choice_tuple)
				# Ensure uniqueness and avoid adding the correct answer as a distractor
				if choice_tuple != karyotype_tuple:
					distractors.append(choice_text)
				else:
					answer_text = choice_text

	return distractors, answer_text

#======================================
#======================================
# Helper function to generate the choice text with tolerance for unexpected tuple lengths
def make_choice_text_translocation(karyotype_tuple):
	if len(karyotype_tuple) != 7:
		raise ValueError("length of tuple must be 7 to use make_choice_text_translocation()")
	# Unpack mandatory fields
	rearrangement_type, chromosome, arm, band, chromosome2, arm2, band2 = karyotype_tuple
	# Check if we have additional details for a translocation
	choice_text = f"{rearrangement_text(rearrangement_type)} "
	choice_text += f"involving the {arm_text(arm)} arm "
	choice_text += f"of chromosome {chromosome} at band {band}"
	choice_text += f" and the {arm_text(arm2)} arm "
	choice_text += f"of chromosome {chromosome2} at band {band2}"
	return choice_text

#======================================
#======================================
#======================================
# Function to generate all possible answer choices
def generate_choices_translocation(karyotype_tuple):
	if len(karyotype_tuple) != 7:
		raise ValueError("length of tuple must be 7 to use generate_choices_translocation()")

	# Parse the karyotype tuple
	answer_text = make_choice_text_translocation(karyotype_tuple)

	rearrangement_type, chromosome, arm, band, chromosome2, arm2, band2 = karyotype_tuple

	# Generate plausible distractors
	distractors = []

	# Options for generating distractors
	arm_options = ["p", "q"]
	rearrangement_options = ["del", "dup", "inv", "t"]
	chromosome_options = [chromosome, band, chromosome2, band2]

	# Create all possible distractors
	for type_choice in rearrangement_options:
		for arm_choice1 in arm_options:
			for arm_choice2 in arm_options:
				for _ in range(4):
					random.shuffle(chromosome_options)
					chr1, bnd1, chr2, bnd2 = chromosome_options
					choice_tuple = type_choice, chr1, arm_choice1, bnd1, chr2, arm_choice2, bnd2,
					choice_text = make_choice_text_translocation(choice_tuple)

					# Ensure uniqueness and avoid adding the correct answer as a distractor
					if choice_tuple != karyotype_tuple:
						distractors.append(choice_text)
					else:
						answer_text = choice_text

	return distractors, answer_text

#======================================
#======================================
#======================================
# Function to generate all possible answer choices
def generate_choices(karyotype_tuple, num_choices=4):
	if len(karyotype_tuple) == 4:
		distractors, answer_text = generate_choices_regular(karyotype_tuple)
	else:
		distractors, answer_text = generate_choices_translocation(karyotype_tuple)

	# Remove duplicates
	distractors = list(set(distractors))
	#print(f"Generated {len(distractors)} unique distractors")

	# Limit to requested distractors
	random.shuffle(distractors)
	if len(distractors) > num_choices - 1:
		distractors = distractors[:num_choices - 1]

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
