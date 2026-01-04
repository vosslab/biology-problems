#!/usr/bin/env python3

# built-in python modules
import random

# external pip modules

# local repo modules
import bptools

#======================================
#======================================
def make_band_tuple() -> tuple:
	"""
	Create a random band tuple (region, band, subband).

	Returns:
		tuple: (region, band, subband) integers.
	"""
	region = random.randint(1, 4)
	band = random.randint(1, 9)
	subband = random.choice([0, 1, 2, 3])
	return region, band, subband

#======================================
#======================================
def band_key(band_tuple: tuple) -> tuple:
	"""
	Return a sortable key for band ordering (proximal to distal).

	Args:
		band_tuple (tuple): (region, band, subband)

	Returns:
		tuple: Sortable key.
	"""
	region, band, subband = band_tuple
	return region, band, subband

#======================================
#======================================
def band_to_text(chromosome: str, arm: str, band_tuple: tuple) -> str:
	"""
	Format a band tuple into cytogenetic notation text.

	Args:
		chromosome (str): Chromosome identifier (1-22, X, Y).
		arm (str): 'p' or 'q' arm.
		band_tuple (tuple): (region, band, subband)

	Returns:
		str: Cytogenetic notation string.
	"""
	region, band, subband = band_tuple
	band_text = f"{chromosome}{arm}{region}{band}"
	if subband > 0:
		band_text += f".{subband}"
	return band_text

#======================================
#======================================
def format_band_choice(band_text: str) -> str:
	"""
	Wrap a band string in monospace formatting.

	Args:
		band_text (str): Cytogenetic band string.

	Returns:
		str: HTML formatted choice string.
	"""
	choice_text = (
		"<span style='font-family: monospace; font-weight: bold;'>"
		f"{band_text}"
		"</span>"
	)
	return choice_text

#======================================
#======================================
def build_question_text(chromosome: str, arm: str, target: str) -> str:
	"""
	Create a question string with varied phrasing.

	Args:
		chromosome (str): Chromosome identifier.
		arm (str): 'p' or 'q'.
		target (str): 'distal' or 'proximal'.

	Returns:
		str: Question text.
	"""
	if target == "distal":
		target_text = "most distal (farthest from the centromere)"
	else:
		target_text = "most proximal (closest to the centromere)"

	phrases = [
		f"On chromosome {chromosome}{arm}, which band is {target_text}?",
		f"For chromosome {chromosome}{arm}, which band lies {target_text}?",
		f"Which band is {target_text} on chromosome {chromosome}{arm}?",
	]
	return random.choice(phrases)

#======================================
#======================================
def generate_question_data(num_choices: int) -> tuple:
	"""
	Generate the question text, choices, and answer for band ordering.

	Args:
		num_choices (int): Number of answer choices to provide.

	Returns:
		tuple: (question_text, choices_list, answer_text)
	"""
	chromosome_list = [str(i) for i in range(1, 23)] + ['X', 'Y']
	chromosome = random.choice(chromosome_list)
	arm = random.choice(['p', 'q'])

	band_set = set()
	while len(band_set) < num_choices:
		band_set.add(make_band_tuple())
	band_list = list(band_set)

	target = random.choice(["distal", "proximal"])
	if target == "distal":
		answer_tuple = max(band_list, key=band_key)
	else:
		answer_tuple = min(band_list, key=band_key)

	choices_list = []
	answer_text = None
	for band_tuple in band_list:
		band_text = band_to_text(chromosome, arm, band_tuple)
		choice_text = format_band_choice(band_text)
		choices_list.append(choice_text)
		if band_tuple == answer_tuple:
			answer_text = choice_text

	if answer_text is None:
		raise ValueError("answer_text was not set during choice generation.")

	random.shuffle(choices_list)
	question_text = build_question_text(chromosome, arm, target)
	return question_text, choices_list, answer_text

#======================================
#======================================
def write_question(N: int, args) -> str:
	"""
	Generate a formatted multiple-choice question.

	Args:
		N (int): Question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: Formatted question string.
	"""
	question_text, choices_list, answer_text = generate_question_data(args.num_choices)
	complete_question = bptools.formatBB_MC_Question(
		N,
		question_text,
		choices_list,
		answer_text,
	)
	return complete_question

#=====================
def parse_arguments():
	"""
	Parse command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate cytogenetic band-order questions."
	)
	parser = bptools.add_choice_args(parser, default=5)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
