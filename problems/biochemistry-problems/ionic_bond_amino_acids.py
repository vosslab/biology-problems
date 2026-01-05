#!/usr/bin/env python3

# external python/pip modules
import random

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

	wrong_choices = set()
	while len(wrong_choices) < max(4, num_choices - 1):
		negative_aa = random.choice(negative_amino_acids)
		other_aa = random.choice(other_amino_acids)
		two_aas = [other_aa, negative_aa]
		wrong_choices.add(f"{two_aas[0].title()} and {two_aas[1].title()}")

		positive_aa = random.choice(positive_amino_acids)
		other_aa = random.choice(other_amino_acids)
		two_aas = [other_aa, positive_aa]
		wrong_choices.add(f"{two_aas[0].title()} and {two_aas[1].title()}")

		other_aa1 = random.choice(other_amino_acids)
		other_aa2 = other_aa1
		while other_aa2 == other_aa1:
			other_aa2 = random.choice(other_amino_acids)
		wrong_choices.add(f"{other_aa1.title()} and {other_aa2.title()}")

	wrong_choices.discard(answer_text)
	wrong_choices_list = list(wrong_choices)
	random.shuffle(wrong_choices_list)
	choices_list = [answer_text] + wrong_choices_list[:max(0, num_choices - 1)]
	random.shuffle(choices_list)

	return choices_list, answer_text

#======================================
#======================================
def write_question(N: int, args) -> str:
	"""Creates a complete formatted question.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed arguments.

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
#======================================
#======================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`max_questions`, and `num_choices`.
	"""
	parser = bptools.make_arg_parser()
	parser = bptools.add_choice_args(parser)

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	# Parse arguments from the command line
	args = parse_arguments()

	# Output file setup
	outfile = bptools.make_outfile()

	# Collect and write questions using shared helper
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == '__main__':
	main()
