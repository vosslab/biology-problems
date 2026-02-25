#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools

# all symbol-to-term pairs in the Gibbs free energy equation
ALL_ITEMS = [
	{"symbol": "&Delta;G", "term": "change in Gibbs free energy"},
	{"symbol": "&Delta;H", "term": "change in enthalpy"},
	{"symbol": "&Delta;S", "term": "change in entropy"},
	{"symbol": "T",        "term": "absolute temperature (Kelvin)"},
]

# stem wording variants
STEM_VARIANTS = [
	(
		"The Gibbs free energy equation is "
		"<strong>&Delta;G = &Delta;H &minus; T&Delta;S</strong>. "
		"Match each symbol to its meaning."
	),
	(
		"In the equation "
		"<strong>&Delta;G = &Delta;H &minus; T&Delta;S</strong>, "
		"match each symbol to the quantity it represents."
	),
	(
		"Given the relationship "
		"<strong>&Delta;G = &Delta;H &minus; T&Delta;S</strong>, "
		"identify what each symbol stands for."
	),
]


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""
	Create a complete formatted matching question for Gibbs free energy
	equation symbols.

	Args:
		question_num (int): the question number for labeling.
		args (argparse.Namespace): parsed command-line arguments.

	Returns:
		str: a formatted BBQ question string.
	"""
	# pick subset size: 3 or 4 items
	num_items = random.choice([3, 4])

	# pick which items to include
	selected = random.sample(ALL_ITEMS, num_items)

	# shuffle the selected items for prompt ordering
	random.shuffle(selected)

	# pick a stem wording variant
	question_text = random.choice(STEM_VARIANTS)

	# build the prompts (symbols) and choices (terms) lists
	prompts_list = [item["symbol"] for item in selected]
	choices_list = [item["term"] for item in selected]

	# format as a matching question
	complete_question = bptools.formatBB_MAT_Question(
		question_num, question_text, prompts_list, choices_list
	)
	return complete_question


#======================================
#======================================
def parse_arguments():
	"""
	Parse command-line arguments for the script.

	Returns:
		argparse.Namespace: parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate Gibbs free energy equation symbol matching questions."
	)
	args = parser.parse_args()
	return args


#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == "__main__":
	main()
