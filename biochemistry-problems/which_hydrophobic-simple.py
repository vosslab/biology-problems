#!/usr/bin/env python3

import random

import bptools

hydrophobic_compounds = [
	'benzene, C<sub>6</sub>H<sub>6</sub>',
	'ethylene, CH<sub>2</sub>CH<sub>2</sub>',
	'butane, CH<sub>3</sub>CH<sub>2</sub>CH<sub>2</sub>CH<sub>3</sub>',
]

hydrophillic_compounds = [
	'acetate, C<sub>2</sub>H<sub>3</sub>O<sub>2</sub>',
	'erythrose, C<sub>4</sub>H<sub>8</sub>O<sub>4</sub>',
	'glycine, NH<sub>2</sub>CH<sub>2</sub>COOH',
	'ethanol, CH<sub>3</sub>CH<sub>2</sub>OH',
	'methanol, CH<sub>3</sub>OH',
	'ammonia, NH<sub>3</sub>',
	'phosphoric acid, H<sub>3</sub>PO<sub>4</sub>',
	'urea, CO(NH<sub>2</sub>)<sub>2</sub>',
]

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
	answer_text = random.choice(hydrophobic_compounds)
	choices_list = random.sample(hydrophillic_compounds, num_choices-1)
	choices_list.append(answer_text)

	# Shuffle choices for presentation
	random.shuffle(choices_list)

	return choices_list, answer_text

#======================================
#======================================
def get_question_text() -> str:
	"""Generates the question text.

	Returns:
		str: The question text in HTML format.
	"""
	return "<h4>Based on their molecular formula, which one of the following compounds is most likely hydrophobic?</h4>"

#======================================
#======================================
def write_question(N: int, args) -> str:
	"""Creates a complete formatted question.

	Args:
		N (int): The question number.
		num_choices (int): The number of choices for the question.

	Returns:
		str: The complete formatted question.
	"""
	assert N > 0, "Question number must be positive"
	assert args.num_choices >= 2, "Number of choices must be at least 2"

	# Add more to the question based on the given letters
	question_text = get_question_text()

	# Choices and answers
	choices_list, answer_text = generate_choices(args.num_choices)

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
def main():
	parser = bptools.make_arg_parser(description="Generate hydrophobic compound questions.")
	parser = bptools.add_choice_args(parser, default=5)
	args = parser.parse_args()

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == '__main__':
	main()
