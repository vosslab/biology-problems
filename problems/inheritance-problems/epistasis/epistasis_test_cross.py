#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random
import copy
import os
import sys
# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

inheritance_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if inheritance_root not in sys.path:
	sys.path.insert(0, inheritance_root)
import hybridcrosslib

#===========================================================
# Data: map modified F2 dihybrid ratios -> expected test-cross phenotype ratios
forward_epistasis_ratios = {
	'15:1': '3:1',
	'13:3': '3:1',
	'12:4': '2:2 or 1:1',
	'12:3:1': '2:1:1',
	'10:6': '2:2 or 1:1',
	'10:3:3': '2:1:1',
	'9:7': '1:3',
	'9:6:1': '1:2:1 or 1:1:2',
	'9:4:3': '1:2:1 or 1:1:2',
}

# Pools of distractors grouped by number of colons in the answer
forward_one_colon_choices = [
	'4:1', '3:2', '3:1', '2:3', '2:2 or 1:1', '2:1', '1:4', '1:3', '1:2',
]

forward_two_colon_choices = [
	'3:1:1', '2:2:1', '2:1:2', '2:1:1', '1:3:1',
	'1:2:2', '1:2:1 or 1:1:2', '1:1:3', '1:1:1',
]

inverse_epistasis_ratios = {
	'3:1':	['15:1', '13:3'],
	'2:1:1':	['12:3:1', '10:3:3'],
	'1:3':	['9:7'],
	'1:2:1':	['9:6:1', '9:4:3'],
	'2:2':	['12:4', '10:6',]
}

#Fake 16:0, 14:2, 11:5, 8:8
inverse_one_colon_choices = [
	'16:0', '15:1', '14:2', '13:3', '12:4', '11:5', '10:6', '9:7', '8:8', '5:11', '2:14', '0:16',
]

#Fake 14, 13, 11, 8, 7, 6
inverse_two_colon_choices = [
	'14:1:1', '13:2:1', '12:3:1', '11:3:2', '10:3:3', '9:6:1', '9:4:3', '8:8:0', '8:4:4', '7:5:4', '6:5:5',
]

#===========================================================
#===========================================================
def get_cross_reference(letter1: str, letter2: str, color_set: list) -> str:
	"""Show the four baseline classes without revealing any epistatic grouping."""
	heterozygote = f"{letter1}{letter1.lower()}{letter2}{letter2.lower()}"
	recessive = f"{letter1.lower() * 2}{letter2.lower() * 2}"
	assigned_colors = hybridcrosslib.dihybridAssignColorsOriginal(0, color_set)
	f2_table = hybridcrosslib.createDiHybridTable(letter1, letter2, assigned_colors)
	test_table = hybridcrosslib.createTestCrossTable(letter1, letter2, assigned_colors)
	text = (
		'<p><strong>Baseline: four distinct phenotypes</strong><br/>'
		'The two genes assort independently and each shows complete dominance. '
		'The colors below distinguish the four baseline classes.</p>'
	)
	panels = [
		('F<sub>1</sub> &times; F<sub>1</sub>', heterozygote, '9:3:3:1', f2_table),
		('Test cross', recessive, '1:1:1:1', test_table),
	]
	for title, partner, ratio, table in panels:
		text += (
			'<div style="display: inline-block; vertical-align: top; '
			'max-width: 100%; overflow-x: auto; margin: 0 12px 12px 0;">'
			f'<p><strong>{title}</strong><br/>{heterozygote} &times; {partner}</p>'
			f'{table}<p>Baseline phenotype ratio: <strong>{ratio}</strong></p></div> '
		)
	classes = [
		f'{letter1}_{letter2}_', f'{letter1}_{letter2.lower() * 2}',
		f'{letter1.lower() * 2}{letter2}_', recessive,
	]
	text += '<p>Baseline genotype classes: '
	for i, (label, color) in enumerate(zip(classes, color_set)):
		if i > 0:
			text += ' &nbsp; '
		text += (
			f'<span style="display: inline-block; background-color: {color}; '
			f'color: black; padding: 2px 6px; border: 1px solid black;">{label}</span>'
		)
	text += '. An underscore means either allele.</p>'
	return text


#===========================================================
def get_modified_cross_comparison(f2_ratio: str, test_ratio: str,
		letter1: str, letter2: str) -> str:
	"""Display the observed and unknown ratios without phenotype colors."""
	heterozygote = f"{letter1}{letter1.lower()}{letter2}{letter2.lower()}"
	recessive = f"{letter1.lower() * 2}{letter2.lower() * 2}"
	text = (
		'<p><strong>With a gene interaction</strong><br/>'
		'Some baseline classes now share a phenotype. '
		'Apply the same phenotype grouping to both crosses.</p>'
		'<table style="border-collapse: collapse; width: 100%; max-width: 640px;">'
		'<tr><th scope="col" style="border: 1px solid black; padding: 8px;">'
		'F<sub>2</sub> offspring</th>'
		'<th scope="col" style="border: 1px solid black; padding: 8px;">'
		'Test-cross offspring</th></tr><tr>'
	)
	for partner, ratio in [(heterozygote, f2_ratio), (recessive, test_ratio)]:
		text += (
			'<td style="border: 1px solid black; padding: 8px; text-align: center;">'
			f'{heterozygote} &times; {partner}<br/>&darr;<br/>'
			f'<strong style="font-size: 125%;">{ratio}</strong></td>'
		)
	text += '</tr></table>'
	return text


#===========================================================
def get_forward_question_text(f2_ratio: str, letter1: str,
		letter2: str, color_set: list) -> str:
	"""Ask for the test-cross ratio using an unmodified visual reference."""
	text = get_cross_reference(letter1, letter2, color_set)
	text += get_modified_cross_comparison(f2_ratio, '?', letter1, letter2)
	text += (
		'<p><strong>What phenotypic ratio would you expect among the '
		'test-cross offspring?</strong></p>'
	)
	return text


#===========================================================
def get_inverse_question_text(test_ratio: str, letter1: str,
		letter2: str, color_set: list) -> str:
	"""Ask for a possible F2 ratio using the same unmodified visual reference."""
	text = get_cross_reference(letter1, letter2, color_set)
	text += get_modified_cross_comparison('?', test_ratio, letter1, letter2)
	text += (
		'<p><strong>Which phenotypic ratio could occur among the '
		'F<sub>2</sub> offspring?</strong></p>'
	)
	return text


#===========================================================
def generate_forward_choices(f2_ratio: str, num_choices: int) -> (list, str):
	"""
	Generate choices and correct answer for a given modified F2 ratio.

	Args:
		f2_ratio (str): The modified dihybrid F2 ratio provided in the prompt.
		num_choices (int): Total number of choices to return.

	Returns:
		tuple: (choices_list, answer_text)
	"""
	answer_text = forward_epistasis_ratios[f2_ratio]
	colon_count = answer_text.split(' ')[0].count(':')

	# Pick a distractor pool based on the answer's colon-count "family"
	if colon_count == 2:
		pool = copy.copy(forward_two_colon_choices)
	else:
		pool = copy.copy(forward_one_colon_choices)

	# Ensure the answer is not duplicated in distractors
	pool.remove(answer_text)

	# Build choices: sample distractors then append the answer
	random.shuffle(pool)
	distractors = pool[:num_choices - 1]
	choices_list = distractors + [answer_text]
	random.shuffle(choices_list)

	return choices_list, answer_text

# Simple assertion test
_choices, _ans = generate_forward_choices('12:3:1', 5)
assert _ans in _choices

#===========================================================
#===========================================================
def generate_inverse_choices(test_ratio: str, num_choices: int) -> (list, str):
	"""
	Generate choices and a single correct F2 ratio given a test-cross ratio.

	Args:
		test_ratio (str): Observed test-cross ratio (e.g., '3:1').
		num_choices (int): Total number of choices to return.

	Returns:
		tuple: (choices_list, answer_text)
	"""
	# All valid F2 answers for this test-cross ratio
	possible_answers = inverse_epistasis_ratios[test_ratio]
	# Pick one to be the correct answer
	answer_text = random.choice(possible_answers)

	# Choose distractor pool based on colon count in the F2 answer
	colon_count = answer_text.count(':')
	if colon_count == 2:
		pool = copy.copy(inverse_two_colon_choices)
	else:
		pool = copy.copy(inverse_one_colon_choices)

	# Remove all valid answers so we don't include another correct option
	for valid in possible_answers:
		if valid in pool:
			pool.remove(valid)

	# Build choices: sample distractors then append the answer
	random.shuffle(pool)
	distractors = pool[:max(0, num_choices - 1)]
	choices_list = distractors + [answer_text]
	random.shuffle(choices_list)

	return choices_list, answer_text

# Simple assertion test
_choices_i, _ans_i = generate_inverse_choices('3:1', 5)
assert _ans_i in _choices_i

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	"""
	Format a single MC Blackboard question for the provided F2 ratio.

	Args:
		N (int): Question number.
		f2_ratio (str): Modified dihybrid F2 ratio to display in the prompt.
		num_choices (int): Number of answer choices.

	Returns:
		str: Formatted Blackboard question string.
	"""
	letter1, letter2 = sorted(random.sample(hybridcrosslib.gene_letters, 2))
	color_set = random.choice(hybridcrosslib.get_four_color_sets())

	if args.direction == 'forward':
		progeny_ratios = list(forward_epistasis_ratios.keys())
		progeny_ratio = progeny_ratios[(N - 1) % len(progeny_ratios)]
		question_text = get_forward_question_text(progeny_ratio, letter1, letter2, color_set)
		choices_list, answer_text = generate_forward_choices(progeny_ratio, args.num_choices)

	elif args.direction == 'inverse':
		progeny_ratios = list(inverse_epistasis_ratios.keys())
		progeny_ratio = progeny_ratios[(N - 1) % len(progeny_ratios)]
		question_text = get_inverse_question_text(progeny_ratio, letter1, letter2, color_set)
		choices_list, answer_text = generate_inverse_choices(progeny_ratio, args.num_choices)

	formatted_choices = []
	for i, choice_text in enumerate(choices_list):
		#print(f'choices_item [{i+1}] "{choice_text}", "{bptools.makeQuestionPretty(choice_text)}"')
		formatted_text = f'a ratio of {choice_text}'
		formatted_choices.append(formatted_text)

	formatted_choices.sort()
	formatted_answer_text = f'a ratio of {answer_text}'

	complete_question = bptools.formatBB_MC_Question(N, question_text, formatted_choices, formatted_answer_text)
	return complete_question

#===========================================================
#===========================================================
def parse_arguments():
	"""
	Parse command-line arguments.

	Returns:
		argparse.Namespace: Parsed args.
	"""
	parser = bptools.make_arg_parser(description="Generate epistasis test-cross ratio questions.")
	parser = bptools.add_choice_args(parser, default=6)

	direction_group = parser.add_mutually_exclusive_group(required=False)

	direction_group.add_argument(
		'-t', '--type', dest='direction', type=str,
		choices=('forward', 'inverse'),
		help='Set the question type: forward or inverse'
	)

	direction_group.add_argument(
		'-f', '--forward', dest='direction', action='store_const', const='forward',
		help='Set question type to forward'
	)

	direction_group.add_argument(
		'-i', '--inverse', dest='direction', action='store_const', const='inverse',
		help='Set question type to inverse'
	)

	parser.set_defaults(direction='forward')

	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile(f"{args.direction}_direction", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
if __name__ == '__main__':
	main()

## THE END
