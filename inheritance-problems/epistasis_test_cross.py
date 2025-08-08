#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
import copy
import math
# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

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
def get_forward_question_text(f2_ratio: str) -> str:
	"""
	Build the question stem for a given modified dihybrid F2 ratio (forward mode).

	Args:
		f2_ratio (str): The modified dihybrid F2 ratio (e.g., '12:3:1') shown in the F2 generation.

	Returns:
		str: HTML question text asking for the expected test-cross phenotype ratio.
	"""
	assert f2_ratio in forward_epistasis_ratios
	text = ''
	text += (
		"<p>In a standard dihybrid cross involving two independent genes, "
		"the expected F<sub>2</sub> phenotypic ratio is <b>9:3:3:1</b>. "
		"A test-cross with an F<sub>1</sub> individual and a double recessive "
		"usually yields a <b>1:1:1:1</b> phenotypic ratio if the genes assort independently.</p>"
	)
	text += (
		"<p>In a specific cross, F<sub>2</sub> progeny exhibit a modified dihybrid "
		f"ratio of <b>{f2_ratio}</b> (instead of 9:3:3:1).</p> "
	)
	text += (
		"<p>What phenotypic ratio would be expected from a test-cross with an "
		"individual from the F<sub>1</sub> progeny?</p> "
	)
	return text

# Simple assertion test
assert isinstance(get_forward_question_text('15:1'), str)

#===========================================================
#===========================================================
def get_inverse_question_text(test_ratio: str) -> str:
	"""
	Build the question stem for a given test-cross ratio (inverse mode).

	Args:
		test_ratio (str): The observed test-cross phenotype ratio (e.g., '3:1').

	Returns:
		str: HTML question text asking for the expected F2 phenotypic ratio.
	"""
	assert test_ratio in inverse_epistasis_ratios

	text = ''
	text += (
		"<p>In a standard dihybrid cross involving two independent genes, "
		"the expected F<sub>2</sub> phenotypic ratio is <b>9:3:3:1</b>. "
		"A test-cross with an F<sub>1</sub> individual and a double recessive "
		"usually yields a <b>1:1:1:1</b> phenotypic ratio if the genes assort independently.</p> "
	)
	text += (
		"<p>The progeny from the test-cross exhibited a modified "
		f"ratio of <b>{test_ratio}</b>, "
		"different from the expected 1:1:1:1 ratio.</p> "
	)
	text += (
		"<p>What phenotypic ratio would be expected in the F<sub>2</sub> generation "
		"if the original dihybrid cross is continued?</p> "
	)
	return text

# Simple assertion test
assert isinstance(get_inverse_question_text('3:1'), str)


#===========================================================
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
def write_question(N: int, direction: str, num_choices: int) -> str:
	"""
	Format a single MC Blackboard question for the provided F2 ratio.

	Args:
		N (int): Question number.
		f2_ratio (str): Modified dihybrid F2 ratio to display in the prompt.
		num_choices (int): Number of answer choices.

	Returns:
		str: Formatted Blackboard question string.
	"""
	if direction == 'forward':
		progeny_ratios = list(forward_epistasis_ratios.keys())
		progeny_ratio = progeny_ratios[(N - 1) % len(progeny_ratios)]
		question_text = get_forward_question_text(progeny_ratio)
		choices_list, answer_text = generate_forward_choices(progeny_ratio, num_choices)

	elif direction == 'inverse':
		progeny_ratios = list(inverse_epistasis_ratios.keys())
		progeny_ratio = progeny_ratios[(N - 1) % len(progeny_ratios)]
		question_text = get_inverse_question_text(progeny_ratio)
		choices_list, answer_text = generate_inverse_choices(progeny_ratio, num_choices)

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
	parser = argparse.ArgumentParser(description="Generate epistasis test-cross ratio questions.")
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='How many passes through the ratio list to generate.',
		default=1
	)
	parser.add_argument(
		'-x', '--max-questions', type=int, dest='max_questions',
		default=99, help='Max number of questions to write.'
	)
	parser.add_argument(
		'-c', '--num_choices', type=int, dest='num_choices',
		default=6, help='Number of choices per question.'
	)

	direction_group = parser.add_mutually_exclusive_group(required=True)

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

	# Generate the output file name based on the script name and arguments
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'              # Add the script name to the file name
		f'-{args.direction}_direction' # Append direction
		f'-{args.num_choices}_choices' # Append number of choices
		'-questions.txt'               # File extension
	)

	# Store all complete formatted questions
	question_bank_list = []

	# Initialize question counter
	N = 0

	# Create the specified number of questions
	for _ in range(args.duplicates):
		# Create a full formatted question (Blackboard format)
		complete_question = write_question(N+1, args.direction, args.num_choices)

		# Append question if successfully generated
		if complete_question is not None:
			N += 1
			question_bank_list.append(complete_question)

		if N >= args.max_questions:
			break

	# Histogram (choices distribution)
	bptools.print_histogram()

	# Shuffle and limit the number of questions if over max
	if len(question_bank_list) > args.max_questions:
		random.shuffle(question_bank_list)
		question_bank_list = question_bank_list[:args.max_questions]

	# Announce where output is going
	print(f'\nWriting {N} question to file: {outfile}')

	# Write all questions to file
	with open(outfile, 'w') as f:
		for complete_question in question_bank_list:
			f.write(complete_question)

	# Final status message
	print(f'... saved {N} questions to {outfile}\n')

#===========================================================
#===========================================================
if __name__ == '__main__':
	main()

## THE END


