#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools

# HTML emphasis spans for properties and system types
ENERGY_EMPH = "<span style='color:#b32020;font-weight:700;'>total energy</span>"
ENTROPY_EMPH = "<span style='color:#1a5fb4;font-weight:700;'>total entropy</span>"
FIRST_LAW_EMPH = "<span style='color:#b32020;font-weight:700;'>first law</span>"
SECOND_LAW_EMPH = "<span style='color:#1a5fb4;font-weight:700;'>second law</span>"
ISOLATED_EMPH = "<span style='color:#6b21a8;font-weight:700;'>isolated</span>"
CLOSED_EMPH = "<span style='color:#6b21a8;font-weight:700;'>closed</span>"
OPEN_EMPH = "<span style='color:#6b21a8;font-weight:700;'>open</span>"

# fixed ordered choices (categorical, not shuffled)
CHOICES = [
	"always zero",
	"always increasing",
	"always decreasing",
	"always constant (conserved)",
	"cannot be determined without more information",
]


#======================================
#======================================
def get_scenarios() -> list:
	"""
	Return the list of all 6 scenario definitions.

	Returns:
		list: scenario dicts with prompt, choices, and answer keys.
	"""
	scenarios = [
		# energy in isolated system -> always constant
		{
			"prompt": (
				f"According to the {FIRST_LAW_EMPH} of thermodynamics, "
				f"the {ENERGY_EMPH} of an {ISOLATED_EMPH} system is:"
			),
			"answer": "always constant (conserved)",
		},
		# entropy in isolated system -> always increasing
		{
			"prompt": (
				f"According to the {SECOND_LAW_EMPH} of thermodynamics, "
				f"the {ENTROPY_EMPH} of an {ISOLATED_EMPH} system is:"
			),
			"answer": "always increasing",
		},
		# energy in closed system -> cannot be determined
		{
			"prompt": (
				f"According to the {FIRST_LAW_EMPH} of thermodynamics, "
				f"the {ENERGY_EMPH} of a {CLOSED_EMPH} system is:"
			),
			"answer": "cannot be determined without more information",
		},
		# entropy in closed system -> cannot be determined
		{
			"prompt": (
				f"According to the {SECOND_LAW_EMPH} of thermodynamics, "
				f"the {ENTROPY_EMPH} of a {CLOSED_EMPH} system is:"
			),
			"answer": "cannot be determined without more information",
		},
		# energy in open system -> cannot be determined
		{
			"prompt": (
				f"According to the {FIRST_LAW_EMPH} of thermodynamics, "
				f"the {ENERGY_EMPH} of an {OPEN_EMPH} system is:"
			),
			"answer": "cannot be determined without more information",
		},
		# entropy in open system -> cannot be determined
		{
			"prompt": (
				f"According to the {SECOND_LAW_EMPH} of thermodynamics, "
				f"the {ENTROPY_EMPH} of an {OPEN_EMPH} system is:"
			),
			"answer": "cannot be determined without more information",
		},
	]
	return scenarios


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""
	Create a complete formatted MC question about thermodynamic
	properties in different system types.

	Args:
		question_num (int): the question number for labeling.
		args (argparse.Namespace): parsed command-line arguments.

	Returns:
		str: a formatted BBQ question string.
	"""
	# pick one random scenario
	scenarios = get_scenarios()
	scenario = random.choice(scenarios)

	question_text = scenario["prompt"]
	# choices are categorical/ordered, not shuffled
	choices_list = list(CHOICES)
	answer_text = scenario["answer"]

	# format as a standard MC question
	complete_question = bptools.formatBB_MC_Question(
		question_num, question_text, choices_list, answer_text
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
		description="Generate thermodynamic system laws MC questions."
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
