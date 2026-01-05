#!/usr/bin/env python3

# built-in python modules
import random

# external pip modules

# local repo modules
import bptools

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
def arm_text(arm: str) -> str:
	"""
	Returns a textual representation of the chromosome arm with HTML color.

	Args:
		arm (str): The arm identifier ('p' or 'q').

	Returns:
		str: 'long' for 'q' (long arm), 'short' for 'p' (short arm), with color coding.
	"""
	if arm == 'q':
		return "<span style='color: #0039e6;'>long arm</span>"  # BLUE for long arm
	return "<span style='color: #59b300;'>short arm</span>"  # LIME GREEN for short arm

#======================================
#======================================
def rearrangement_text(rearrangement_type: str) -> str:
	"""
	Returns a textual description for a chromosome rearrangement type with HTML color.

	Args:
		rearrangement_type (str): The type of rearrangement ('t', 'dup', 'del', 'inv').

	Returns:
		str: A human-readable description of the rearrangement type with color coding.

	Raises:
		ValueError: If the rearrangement type is unknown.
	"""
	if rearrangement_type == 't':
		return "<span style='color: #e60000;'>A translocation</span>"  # RED
	elif rearrangement_type == 'dup':
		return "<span style='color: #e65400;'>A duplication</span>"  # DARK ORANGE
	elif rearrangement_type == 'del':
		return "<span style='color: #7b12a1;'>A deletion</span>"  # PURPLE
	elif rearrangement_type == 'inv':
		return "<span style='color: #00b38f;'>An inversion</span>"  # TEAL
	raise ValueError(f"Unknown rearrangement_type {rearrangement_type}")

#======================================
#======================================
def make_choice_text_regular(karyotype_tuple: tuple) -> str:
	"""
	Generates descriptive text for a chromosome rearrangement, excluding translocations.

	Args:
		karyotype_tuple (tuple): A tuple with 4 elements: (rearrangement_type, chromosome, arm, band).

	Returns:
		str: A human-readable description of the rearrangement with HTML color.

	Raises:
		ValueError: If the tuple does not have exactly 4 elements.
	"""
	if len(karyotype_tuple) != 4:
		raise ValueError("length of tuple must be 4 to use make_choice_text_regular()")

	# Unpack mandatory fields
	rearrangement_type, chromosome, arm, band = karyotype_tuple

	# Non-translocation rearrangement (del, dup, inv)
	choice_text = f"{rearrangement_text(rearrangement_type)} "
	choice_text += f"involving the {arm_text(arm)} "
	choice_text += f"of chromosome <span style='color: #004d99;'>{chromosome}</span> "  # NAVY for chromosome
	choice_text += f"at band <span style='color: #e69100;'>{band}</span>"  # LIGHT ORANGE for band
	return choice_text

#======================================
#======================================
def make_choice_text_translocation(karyotype_tuple: tuple) -> str:
	"""
	Generates descriptive text for a translocation rearrangement between two chromosome regions.

	Args:
		karyotype_tuple (tuple): A tuple with 7 elements:
			(rearrangement_type, chromosome1, arm1, band1, chromosome2, arm2, band2).

	Returns:
		str: A human-readable description of the translocation with HTML color.

	Raises:
		ValueError: If the tuple does not have exactly 7 elements.
	"""
	if len(karyotype_tuple) != 7:
		raise ValueError("length of tuple must be 7 to use make_choice_text_translocation()")

	# Unpack mandatory fields
	rearrangement_type, chromosome1, arm1, band1, chromosome2, arm2, band2 = karyotype_tuple

	# Translocation rearrangement with color coding for clarity
	choice_text = f"{rearrangement_text(rearrangement_type)} "  # Color from rearrangement_text
	choice_text += f"involving the {arm_text(arm1)} "  # Color from arm_text
	choice_text += f"of <span style='color: #004d99;'>chromosome {chromosome1}</span> "  # NAVY for chromosome1
	choice_text += f"at <span style='color: #e69100;'>band {band1}</span> "  # LIGHT ORANGE for band1
	choice_text += f"and the {arm_text(arm2)} "  # Color from arm_text
	choice_text += f"of <span style='color: #0a9bf5;'>chromosome {chromosome2}</span> "  # SKY BLUE for chromosome2
	choice_text += f"at <span style='color: #b3b300;'>band {band2}</span>"  # DARK YELLOW for band2

	return choice_text

#======================================
#======================================
# Function to generate all possible answer choices
def generate_choices_regular(karyotype_tuple):
	if len(karyotype_tuple) != 4:
		raise ValueError("length of tuple must be 4 to use generate_choices_regular()")

	rearrangement_type, chromosome, arm, band = karyotype_tuple

	# Options for generating distractors
	arm_options = ["p", "q"]
	rearrangement_options = ["del", "dup", "inv", "t"]
	# Choose between correct chromosome and placeholder band
	chromosome_options = [chromosome, band]

	# Generate plausible distractors
	distractor_diff_type = []
	distractor_same_type = []

	# Create all possible distractors
	for type_choice in rearrangement_options:
		for chromosome_choice in chromosome_options:
			for arm_choice in arm_options:
				band_choice = band if chromosome_choice == chromosome else chromosome
				choice_tuple = type_choice, chromosome_choice, arm_choice, band_choice
				choice_text = make_choice_text_regular(choice_tuple)
				# Ensure uniqueness and avoid adding the correct answer as a distractor
				if choice_tuple == karyotype_tuple:
					answer_text = choice_text
				elif type_choice == rearrangement_type:
					distractor_same_type.append(choice_text)
				else:
					distractor_diff_type.append(choice_text)

	return distractor_diff_type, distractor_same_type, answer_text

#======================================
#======================================
# Function to generate all possible answer choices
def generate_choices_translocation(karyotype_tuple):
	if len(karyotype_tuple) != 7:
		raise ValueError("length of tuple must be 7 to use generate_choices_translocation()")

	# Parse the karyotype tuple
	answer_text = make_choice_text_translocation(karyotype_tuple)

	rearrangement_type, chromosome, arm, band, chromosome2, arm2, band2 = karyotype_tuple

	# Options for generating distractors
	arm_options = ["p", "q"]
	rearrangement_options = ["del", "dup", "inv", "t"]
	chromosome_options = [chromosome, band, chromosome2, band2]

	# Generate plausible distractors
	distractor_diff_type = []
	distractor_same_type = []

	# Create all possible distractors
	for type_choice in rearrangement_options:
		for arm_choice1 in arm_options:
			for arm_choice2 in arm_options:
				for _ in range(4):
					random.shuffle(chromosome_options)
					chr1, bnd1, chr2, bnd2 = chromosome_options
					choice_tuple = type_choice, chr1, arm_choice1, bnd1, chr2, arm_choice2, bnd2
					swap_tuple = type_choice, chr2, arm_choice2, bnd2, chr1, arm_choice1, bnd1
					choice_text = make_choice_text_translocation(choice_tuple)

					# Ensure uniqueness and avoid adding the correct answer as a distractor
					if choice_tuple == karyotype_tuple:
						answer_text = choice_text
					elif swap_tuple == karyotype_tuple:
						# avoid a confusing choice that could be technically correct
						continue
					elif type_choice == rearrangement_type:
						distractor_same_type.append(choice_text)
					else:
						distractor_diff_type.append(choice_text)

	return distractor_diff_type, distractor_same_type, answer_text

#======================================
#======================================
# Function to generate all possible answer choices
def generate_choices(karyotype_tuple, num_choices=4):
	if len(karyotype_tuple) == 4:
		distractor_diff_type, distractor_same_type, answer_text = generate_choices_regular(karyotype_tuple)
	else:
		distractor_diff_type, distractor_same_type, answer_text = generate_choices_translocation(karyotype_tuple)

	# Remove duplicates
	distractor_diff_type = list(set(distractor_diff_type))
	distractor_same_type = list(set(distractor_same_type))

	print(f"Generated {len(distractor_same_type)} same and {len(distractor_diff_type)} different unique distractors")

	random.shuffle(distractor_diff_type)
	random.shuffle(distractor_same_type)
	choices_list = []
	while len(choices_list) < num_choices - 1:
		if len(distractor_same_type) > 0:
			choices_list.append(distractor_same_type.pop())
		if len(choices_list) < num_choices - 1:
			choices_list.append(distractor_diff_type.pop())

	choices_list.append(answer_text)
	choices_list = list(set(choices_list))
	#random.shuffle(choices_list)
	choices_list.sort()

	return choices_list, answer_text

#======================================
#======================================
def write_question(N: int, args) -> str:
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
	choices_list, answer_text = generate_choices(karyotype_tuple, args.num_choices)

	# Format the complete question with the specified module function
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
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
	parser = bptools.make_arg_parser(description="Generate questions.")
	parser = bptools.add_choice_args(parser, default=5)

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

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
