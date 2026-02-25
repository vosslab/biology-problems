#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools

# HTML emphasis spans for key terms
DG_SYMBOL = "&Delta;G"
DG_EMPH = f"<span style='color:#0066cc;font-weight:700;'>{DG_SYMBOL}</span>"
EXERGONIC_EMPH = "<span style='color:#0077bb;font-weight:700;'>exergonic</span>"
ENDERGONIC_EMPH = "<span style='color:#cc6600;font-weight:700;'>endergonic</span>"
NEGATIVE_EMPH = "<span style='color:#0077bb;font-weight:700;'>negative</span>"
POSITIVE_EMPH = "<span style='color:#cc6600;font-weight:700;'>positive</span>"

# shared distractor phrases
DISTRACTOR_ACTIVATION = "no activation energy is required for this reaction"
DISTRACTOR_ENZYME = "the number of substrates exceeds the number of enzymes"
DISTRACTOR_DG_ZERO = f"{DG_SYMBOL} = 0 (the reaction is at equilibrium)"


#======================================
#======================================
def get_scenarios() -> list:
	"""
	Return the list of all 8 scenario definitions.

	Returns:
		list: scenario dicts with prompt, choices, and answer keys.
	"""
	scenarios = [
		# Template A: given reaction type, ask about relative free energies
		{
			"prompt": (
				f"In an {EXERGONIC_EMPH} reaction, which of the following "
				f"statements about the free energy is <strong>true</strong>?"
			),
			"choices": [
				"reactants have <strong>more</strong> free energy than products",
				"reactants have <strong>less</strong> free energy than products",
				DISTRACTOR_ACTIVATION,
				DISTRACTOR_ENZYME,
			],
			"answer": "reactants have <strong>more</strong> free energy than products",
		},
		{
			"prompt": (
				f"In an {ENDERGONIC_EMPH} reaction, which of the following "
				f"statements about the free energy is <strong>true</strong>?"
			),
			"choices": [
				"reactants have <strong>less</strong> free energy than products",
				"reactants have <strong>more</strong> free energy than products",
				DISTRACTOR_ACTIVATION,
				DISTRACTOR_ENZYME,
			],
			"answer": "reactants have <strong>less</strong> free energy than products",
		},
		# Template B: given reaction type, ask about sign of delta-G
		{
			"prompt": (
				f"A reaction is classified as {EXERGONIC_EMPH}. "
				f"Which statement about {DG_EMPH} is <strong>true</strong>?"
			),
			"choices": [
				f"{DG_SYMBOL} &lt; 0 (negative)",
				f"{DG_SYMBOL} &gt; 0 (positive)",
				DISTRACTOR_DG_ZERO,
				DISTRACTOR_ACTIVATION,
			],
			"answer": f"{DG_SYMBOL} &lt; 0 (negative)",
		},
		{
			"prompt": (
				f"A reaction is classified as {ENDERGONIC_EMPH}. "
				f"Which statement about {DG_EMPH} is <strong>true</strong>?"
			),
			"choices": [
				f"{DG_SYMBOL} &gt; 0 (positive)",
				f"{DG_SYMBOL} &lt; 0 (negative)",
				DISTRACTOR_DG_ZERO,
				DISTRACTOR_ACTIVATION,
			],
			"answer": f"{DG_SYMBOL} &gt; 0 (positive)",
		},
		# Template C: given sign of delta-G, ask about free energy relationship
		{
			"prompt": (
				f"A reaction has a {NEGATIVE_EMPH} {DG_EMPH} "
				f"({DG_SYMBOL} &lt; 0). Which statement about the free energy "
				f"is <strong>true</strong>?"
			),
			"choices": [
				"reactants have <strong>more</strong> free energy than products",
				"reactants have <strong>less</strong> free energy than products",
				DISTRACTOR_ACTIVATION,
				"cannot be determined from the information given",
			],
			"answer": "reactants have <strong>more</strong> free energy than products",
		},
		{
			"prompt": (
				f"A reaction has a {POSITIVE_EMPH} {DG_EMPH} "
				f"({DG_SYMBOL} &gt; 0). Which statement about the free energy "
				f"is <strong>true</strong>?"
			),
			"choices": [
				"reactants have <strong>less</strong> free energy than products",
				"reactants have <strong>more</strong> free energy than products",
				DISTRACTOR_ACTIVATION,
				"cannot be determined from the information given",
			],
			"answer": "reactants have <strong>less</strong> free energy than products",
		},
		# Template D: given sign of delta-G, ask about reaction classification
		{
			"prompt": (
				f"A reaction has a {NEGATIVE_EMPH} {DG_EMPH} "
				f"({DG_SYMBOL} &lt; 0). This reaction is classified as:"
			),
			"choices": [
				"exergonic (energy-releasing)",
				"endergonic (energy-absorbing)",
				"at equilibrium",
				"activation-energy independent",
			],
			"answer": "exergonic (energy-releasing)",
		},
		{
			"prompt": (
				f"A reaction has a {POSITIVE_EMPH} {DG_EMPH} "
				f"({DG_SYMBOL} &gt; 0). This reaction is classified as:"
			),
			"choices": [
				"endergonic (energy-absorbing)",
				"exergonic (energy-releasing)",
				"at equilibrium",
				"activation-energy independent",
			],
			"answer": "endergonic (energy-absorbing)",
		},
	]
	return scenarios


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""
	Create a complete formatted MC question about exergonic/endergonic
	reactions.

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
	choices_list = list(scenario["choices"])
	answer_text = scenario["answer"]

	# shuffle the choices
	random.shuffle(choices_list)

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
		description="Generate exergonic/endergonic reaction property MC questions."
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
