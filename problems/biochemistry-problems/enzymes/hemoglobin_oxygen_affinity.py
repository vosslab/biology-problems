#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
import bptools

# Color-coded answer choice HTML fragments
COLOR_INCREASE = '#1a7a1a'
COLOR_DECREASE = '#c93030'
COLOR_NO_CHANGE = '#555555'

CHOICE_INCREASE = (
	f"<span style='color: {COLOR_INCREASE}; font-weight: 700;'>"
	"Increases</span> affinity for oxygen (O<sub>2</sub>) binding"
)
CHOICE_DECREASE = (
	f"<span style='color: {COLOR_DECREASE}; font-weight: 700;'>"
	"Decreases</span> affinity for oxygen (O<sub>2</sub>) binding"
)
CHOICE_NO_CHANGE = (
	f"Would show <span style='color: {COLOR_NO_CHANGE}; font-weight: 700;'>"
	"no major change</span> in oxygen binding affinity"
)

# Map answer keys to display text
ANSWER_MAP = {
	'increase': CHOICE_INCREASE,
	'decrease': CHOICE_DECREASE,
	'no_change': CHOICE_NO_CHANGE,
}

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
#============================================
def _build_question_pool() -> list:
	"""
	Build the pool of hemoglobin oxygen affinity conditions.

	Returns:
		list: Each entry is (condition_text, answer_key).
	"""
	question_pool = [
		# Temperature effects
		("Cooler temperatures of the lungs", 'increase'),
		("Warmer temperatures of the bodily tissues", 'decrease'),
		# 2,3-BPG effects
		("The presence of 2,3-bisphosphoglycerate (2,3-BPG)", 'decrease'),
		(
			"The presence of 2,3-bisphosphoglycerate (2,3-BPG) on the "
			"<b>fetal hemoglobin</b> protein when compared to its "
			"effect on adult hemoglobin",
			'no_change',
		),
		# CO2 effects (Bohr effect)
		(
			"An increase in the partial pressure of carbon dioxide "
			"(CO<sub>2</sub>)",
			'decrease',
		),
		(
			"A decrease in the partial pressure of carbon dioxide "
			"(CO<sub>2</sub>)",
			'increase',
		),
		# T and R states
		("The R state", 'increase'),
		("The T state", 'decrease'),
		# Cooperativity effects
		("The binding of oxygen at two other subunits", 'increase'),
		(
			"Having three subunits already bound to oxygen "
			"(O<sub>2</sub>)",
			'increase',
		),
		# pH effects (Bohr effect)
		("A lower pH of 7.2", 'decrease'),
		("A higher pH of 7.6", 'increase'),
		# H+ concentration effects
		(
			"A lower concentration of hydrogen ions "
			"[H<sup>+</sup>]",
			'increase',
		),
		(
			"A higher concentration of hydrogen ions "
			"[H<sup>+</sup>]",
			'decrease',
		),
	]
	return question_pool

#============================================
#============================================
def _get_scenarios() -> list:
	"""
	Generate all scenarios from the question pool.

	Returns:
		list: Each entry is (condition_text, answer_key).
	"""
	return _build_question_pool()

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted MC question about hemoglobin oxygen affinity.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	# select scenario using modulo
	idx = (N - 1) % len(SCENARIOS)
	condition_text, answer_key = SCENARIOS[idx]

	# build the emphasized condition HTML
	emph_style = "font-weight: 700; color: #1a3a6e; font-size: 1.1em;"
	condition_html = f"<span style='{emph_style}'>{condition_text}</span>"

	# build question text
	question_text = ""
	question_text += "<p>Hemoglobin is one of the most heavily modulated proteins "
	question_text += "in the body. Its oxygen binding affinity is regulated by "
	question_text += "multiple physiological factors that shift the balance between "
	question_text += "different conformational states of the protein.</p>"
	question_text += f"<p>{condition_html} has this effect on the normal adult "
	question_text += "hemoglobin protein:</p>"

	# 3 fixed choices (always the same, always in this order)
	choices_list = [CHOICE_INCREASE, CHOICE_DECREASE, CHOICE_NO_CHANGE]
	answer_text = ANSWER_MAP[answer_key]

	# format as MC question
	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices_list, answer_text
	)
	return complete_question

#============================================
#============================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate hemoglobin oxygen binding affinity questions."
	)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#============================================
#============================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()

	# initialize scenarios
	global SCENARIOS
	SCENARIOS = _get_scenarios()
	if args.scenario_order == 'random':
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
#============================================
if __name__ == '__main__':
	main()

## THE END
