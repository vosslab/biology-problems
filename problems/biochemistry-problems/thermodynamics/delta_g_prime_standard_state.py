#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools

# HTML symbol fragments for thermodynamic quantities
DG_STD = "&Delta;G&deg;"
DG_PRIME = "&Delta;G&deg;&prime;"

# colored emphasis spans for key terms
DG_STD_EMPH = f"<span style='color:#0077bb;font-weight:700;'>{DG_STD}</span>"
DG_PRIME_EMPH = f"<span style='color:#cc6600;font-weight:700;'>{DG_PRIME}</span>"

# spoken-form parentheticals
DG_STD_SPOKEN = f"(delta G naught, {DG_STD_EMPH})"
DG_PRIME_SPOKEN = f"(delta G naught-prime, {DG_PRIME_EMPH})"

# correct answer (always present)
CORRECT_ANSWER = (
	"pH is fixed at 7 "
	"([H<sup>+</sup>] = 1 &times; 10<sup>&minus;7</sup> M instead of 1 M)"
)

# always-present distractors
CORE_DISTRACTORS = [
	"temperature is different from 298 K (25 &deg;C)",
	"pressure is different from 1 atm",
	"all reactant concentrations are at 1 M",
]

# extra distractor pool (pick 1 per question)
EXTRA_DISTRACTORS = [
	"volume of the system is standardized to 1 liter",
	"ionic strength is fixed at 0.1 M",
	"a buffer is required in the reaction mixture",
	"a catalyst must be present for the reaction",
]

# stem wording variants
STEM_VARIANTS = [
	(
		f"The biochemical standard free energy change {DG_PRIME_SPOKEN} "
		f"differs from the chemical standard free energy change {DG_STD_SPOKEN}. "
		f"Which factor is treated differently?"
	),
	(
		f"{DG_PRIME_EMPH} {DG_PRIME_SPOKEN} adjusts the standard state "
		f"conditions used in {DG_STD_EMPH} {DG_STD_SPOKEN}. "
		f"What does it adjust?"
	),
	(
		f"What additional condition is assumed when using the biochemical "
		f"standard free energy change {DG_PRIME_SPOKEN} "
		f"instead of {DG_STD_SPOKEN}?"
	),
	(
		f"Which condition is specified differently in the biochemical "
		f"standard state {DG_PRIME_SPOKEN} compared to the chemical "
		f"standard state {DG_STD_SPOKEN}?"
	),
]


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""
	Create a complete formatted MC question about standard vs biochemical
	standard state.

	Args:
		question_num (int): the question number for labeling.
		args (argparse.Namespace): parsed command-line arguments.

	Returns:
		str: a formatted BBQ question string.
	"""
	# pick a stem wording variant
	question_text = random.choice(STEM_VARIANTS)

	# pick 1 extra distractor from pool
	extra_pick = random.choice(EXTRA_DISTRACTORS)

	# assemble 5 choices: correct + 3 core distractors + 1 extra
	choices_list = [CORRECT_ANSWER] + list(CORE_DISTRACTORS) + [extra_pick]
	random.shuffle(choices_list)

	answer_text = CORRECT_ANSWER

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
		description="Generate standard vs biochemical standard state MC questions."
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
