#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools

# HTML symbol fragments for thermodynamic quantities
DG_SYMBOL = "&Delta;G&deg;&prime;"
DG_ACTUAL = "&Delta;G"
KEQ_SYMBOL = "K&prime;<sub>eq</sub>"

# colored emphasis spans for key terms in question stems
DG_EMPH = f"<span style='color:#0066cc;font-weight:700;'>{DG_SYMBOL}</span>"
DG_ACTUAL_EMPH = f"<span style='color:#0066cc;font-weight:700;'>{DG_ACTUAL}</span>"
KEQ_EMPH = f"<span style='color:#997300;font-weight:700;'>{KEQ_SYMBOL}</span>"

# Type A choices: sign of delta-G standard prime
SIGN_CHOICES = ["negative", "zero", "positive"]

# Type B choices: K'eq relative to 1
KEQ_CHOICES = ["less than 1", "equal to 1", "greater than 1"]

# Type C choices: value of actual delta-G at equilibrium
ACTUAL_DG_CHOICES = ["zero", "negative", "positive"]


#======================================
#======================================
def get_scenarios() -> list:
	"""
	Return the list of all 7 scenario definitions.

	Returns:
		list: scenario dicts with prompt, choices, and answer keys.
	"""
	scenarios = [
		# --- Type A: given K'eq, ask sign of DG standard prime ---
		{
			"prompt": (
				f"If the equilibrium constant ({KEQ_EMPH}) is "
				f"<strong>greater than 1</strong>, "
				f"what is the sign of the standard transformed "
				f"Gibbs free energy change ({DG_EMPH})?"
			),
			"choices": SIGN_CHOICES,
			"answer": "negative",
		},
		{
			"prompt": (
				f"If the equilibrium constant ({KEQ_EMPH}) is "
				f"<strong>equal to 1</strong>, "
				f"what is the sign of the standard transformed "
				f"Gibbs free energy change ({DG_EMPH})?"
			),
			"choices": SIGN_CHOICES,
			"answer": "zero",
		},
		{
			"prompt": (
				f"If the equilibrium constant ({KEQ_EMPH}) is "
				f"<strong>less than 1</strong>, "
				f"what is the sign of the standard transformed "
				f"Gibbs free energy change ({DG_EMPH})?"
			),
			"choices": SIGN_CHOICES,
			"answer": "positive",
		},
		# --- Type B: given DG standard prime, ask K'eq relative to 1 ---
		{
			"prompt": (
				f"If the standard transformed Gibbs free energy change "
				f"({DG_EMPH}) is <strong>negative</strong> (less than zero), "
				f"what is the value of the equilibrium constant ({KEQ_EMPH}) "
				f"relative to 1?"
			),
			"choices": KEQ_CHOICES,
			"answer": "greater than 1",
		},
		{
			"prompt": (
				f"If the standard transformed Gibbs free energy change "
				f"({DG_EMPH}) is <strong>equal to zero</strong>, "
				f"what is the value of the equilibrium constant ({KEQ_EMPH}) "
				f"relative to 1?"
			),
			"choices": KEQ_CHOICES,
			"answer": "equal to 1",
		},
		{
			"prompt": (
				f"If the standard transformed Gibbs free energy change "
				f"({DG_EMPH}) is <strong>positive</strong> (greater than zero), "
				f"what is the value of the equilibrium constant ({KEQ_EMPH}) "
				f"relative to 1?"
			),
			"choices": KEQ_CHOICES,
			"answer": "less than 1",
		},
		# --- Type C: at equilibrium, ask actual delta-G ---
		{
			"prompt": (
				f"When a reaction has reached equilibrium, "
				f"what is the value of the <strong>actual</strong> "
				f"(not standard) Gibbs free energy change "
				f"({DG_ACTUAL_EMPH})?"
			),
			"choices": ACTUAL_DG_CHOICES,
			"answer": "zero",
		},
	]
	return scenarios


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""
	Create a complete formatted MC question.

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
	# choices are categorical bins in logical order, not shuffled
	choices_list = list(scenario["choices"])
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
		description="Generate free energy / equilibrium constant relationship MC questions."
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
