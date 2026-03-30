#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
import bptools

# emphasized key phrases style (inline CSS only, no JS)
EMPH_STYLE = "font-weight: 700; color: #1a3a6e; font-size: 1.05em;"

# blank-line style for the missing model name
BLANK_HTML = "<span style='border-bottom: 2px solid #333; padding: 0 2em;'>&nbsp;</span>"

# Pool of plausible wrong answers with fake abbreviations
DISTRACTOR_POOL = [
	'induced fit (IF)',
	'cooperative (COOP)',
	'equilibrium (EQ)',
	'Michaelis-Menten (MM)',
	'lock and key (LK)',
	'competitive (CI)',
	'allosteric (ALLO)',
	'Hill (HC)',
]

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
#============================================
def _build_question_pool() -> list:
	"""
	Build the pool of question variants for allosteric enzyme models.

	Returns:
		list: Each entry is (question_html, correct_answer).
	"""
	# Question pool: each entry tests concerted vs sequential distinction
	question_pool = [
		(
			f"The {BLANK_HTML} model states that "
			f"<span style='{EMPH_STYLE}'>all subunits</span> "
			"in an allosteric enzyme must be in either the T or the R state; "
			f"there <span style='{EMPH_STYLE}'>cannot be hybrids</span>.",
			'concerted (MWC)',
		),
		(
			f"The {BLANK_HTML} model allows a "
			f"<span style='{EMPH_STYLE}'>mixture of states</span> "
			"in an allosteric enzyme and "
			f"<span style='{EMPH_STYLE}'>each individual subunit</span> "
			"can be in either the T or the R state.",
			'sequential (KNF)',
		),
	]
	return question_pool

#============================================
#============================================
def _get_scenarios() -> list:
	"""
	Generate all scenarios: each question variant x each set of 3 distractors.

	Returns:
		list: Each entry is (question_html, correct_answer, distractors_list).
	"""
	question_pool = _build_question_pool()
	scenarios = []
	# Generate multiple distractor combinations for variety
	for q_html, correct in question_pool:
		# determine the other model (always included as strong distractor)
		if correct == 'concerted (MWC)':
			other_model = 'sequential (KNF)'
		else:
			other_model = 'concerted (MWC)'
		# create several distractor sets from the pool
		for start_idx in range(len(DISTRACTOR_POOL) - 2):
			distractors = [other_model] + DISTRACTOR_POOL[start_idx:start_idx + 3]
			scenarios.append((q_html, correct, distractors))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted MC question for allosteric enzyme model identification.

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
	q_html, correct_answer, distractors = SCENARIOS[idx]

	# build intro text
	question_text = ""
	question_text += "<p>Allosteric enzymes are regulated by conformational changes "
	question_text += "between the T (tense, low-affinity) and R (relaxed, high-affinity) states. "
	question_text += "Two classical models describe how these transitions occur across subunits.</p>"
	question_text += f"<p>{q_html}</p>"
	question_text += "<p>Which allosteric model is being described above?</p>"

	# build choices: correct + distractors
	choices_list = [correct_answer] + list(distractors)
	random.shuffle(choices_list)

	# format as MC question
	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices_list, correct_answer
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
		description="Generate allosteric enzyme model identification questions."
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
