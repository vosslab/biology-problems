#!/usr/bin/env python3

"""Generate Michaelis-Menten Km-from-table multiple choice questions."""

# Standard Library
import random

# Local repo modules
import bptools
import mm_lib

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
def make_complete_problem(N: int, km: float, vmax: float) -> str:
	"""Build a complete MC question asking students to determine Km from a table.

	Args:
		N: The question number.
		km: The correct Michaelis constant.
		vmax: Maximum velocity.

	Returns:
		A formatted Blackboard question string.
	"""
	# compute velocities for each substrate concentration
	velocities = []
	for s_val in mm_lib.SUBSTRATE_CONCS:
		v0 = mm_lib.michaelis_menten(s_val, km, vmax)
		velocities.append(v0)

	# build the data table
	data_table = mm_lib.make_data_table(mm_lib.SUBSTRATE_CONCS, velocities, vmax)

	# build question text
	question_text = ""
	question_text += "<p><u>Michaelis-Menten question.</u> "
	question_text += "The following question refers to the table "
	question_text += "(<i>below</i>) of enzyme activity.</p>"
	question_text += data_table
	question_text += "<br/>"
	question_text += "<p>Using the table (<i>above</i>), calculate the value "
	question_text += "for the Michaelis-Menten constant, K<sub>M</sub>.</p>"

	# build answer choices: 4 random distractors + the correct Km
	distractors = [s for s in mm_lib.SUBSTRATE_CONCS[:7] if abs(s - km) > 1e-8]
	random.shuffle(distractors)
	# take 4 distractors and add the correct answer
	choices = distractors[:4]
	choices.append(km)
	choices.sort()

	# format choices with monospace styling
	mono = "<span style='font-family: courier, monospace;'>"
	choices_list = []
	answer_text = None
	for choice in choices:
		choice_text = f"K<sub>M</sub> = {mono}{choice:.3f}</span> mM"
		choices_list.append(choice_text)
		if abs(choice - km) < 1e-8:
			answer_text = choice_text

	# format as MC question
	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices_list, answer_text
	)
	return complete_question

#============================================
def _get_scenarios() -> list:
	"""Generate all (vmax, km) scenario combinations.

	Returns:
		List of (vmax, km) tuples.
	"""
	# Vmax choices: 40 to 200 in steps of 20
	vmax_choices = list(range(40, 201, 20))
	scenarios = []
	for vmax in vmax_choices:
		for km in mm_lib.KM_CHOICES:
			scenarios.append((vmax, km))
	return scenarios

#============================================
def write_question(N: int, args) -> str:
	"""Create a formatted MC question for Km determination from a table.

	Args:
		N: The question number.
		args: Parsed command-line arguments.

	Returns:
		A formatted question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	vmax, km = SCENARIOS[idx]
	return make_complete_problem(N, km, vmax)

#============================================
def parse_arguments():
	"""Parse command-line arguments.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate Michaelis-Menten Km-from-table questions."
	)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#============================================
def main():
	"""Main function that orchestrates question generation and file output."""
	args = parse_arguments()

	# initialize scenarios
	global SCENARIOS
	SCENARIOS = _get_scenarios()
	if len(SCENARIOS) == 0:
		raise ValueError("No scenarios were generated.")
	if args.scenario_order == 'random':
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
if __name__ == '__main__':
	main()
