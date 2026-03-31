#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
import bptools
import metaboliclib

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
#============================================
def _build_pathway(trunk_len: int, b1_len: int, b2_len: int,
		letter_shift: int) -> dict:
	"""Build pathway via shorthand pipeline: letters -> shorthand -> schema -> display model.

	Adds question context (convenience aliases) on top of the display model.

	Args:
		trunk_len (int): Number of metabolites in trunk (3 or 4).
		b1_len (int): Number of metabolites in upper branch (3 or 4).
		b2_len (int): Number of metabolites in lower branch (3 or 4).
		letter_shift (int): Starting index in the alphabet.

	Returns:
		dict: Display model + question context keys.
	"""
	# pick sequential letters starting at letter_shift
	total = trunk_len + b1_len + b2_len
	letters = list(metaboliclib.ALL_LETTERS[letter_shift:letter_shift + total])
	trunk_letters = letters[:trunk_len]
	b1_letters = letters[trunk_len:trunk_len + b1_len]
	b2_letters = letters[trunk_len + b1_len:]

	# build shorthand, parse, and decorate
	shorthand = metaboliclib.build_shorthand('split', trunk_letters, b1_letters, b2_letters)
	schema = metaboliclib.parse_shorthand(shorthand)
	display = metaboliclib.build_display_model(schema)

	# add question-context convenience aliases
	display['bp_mol'] = display['junction_mol']
	display['b1_end'] = display['end_products']['b1']
	display['b2_end'] = display['end_products']['b2']
	display['e_b1_first'] = display['committed_step_enzymes']['b1']
	display['e_b2_first'] = display['committed_step_enzymes']['b2']
	return display

#============================================
#============================================
def _make_feedback_inhibitor_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: which metabolite is most likely a feedback inhibitor.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch end product, 2 for lower.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	trunk = pathway['trunk']
	b1 = pathway['b1']
	b2 = pathway['b2']
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']

	# correct answer is the end product of the focus branch
	if focus_branch == 1:
		correct_mol = b1_end
	else:
		correct_mol = b2_end
	answer_text = f"metabolite {metaboliclib.color_text(correct_mol[0], correct_mol[1])}"

	# build distractor set from other metabolites
	distractors = [trunk[0], b1[0], b2[0]]
	if len(trunk) >= 3:
		distractors.append(trunk[1])
	if focus_branch == 1 and len(b2) >= 2:
		distractors.append(b2[1])
	elif focus_branch == 2 and len(b1) >= 2:
		distractors.append(b1[1])
	choices_list = metaboliclib.build_metabolite_choices(answer_text, correct_mol, distractors)

	# question text
	# build diagram inline for this question
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += "<p>In feedback regulation, end products inhibit "
	question_text += "earlier enzymes in their own branch. "
	question_text += "<b>Which metabolite is most likely to act as a feedback "
	question_text += "inhibitor in this pathway?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_regulated_enzyme_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: which enzyme is most likely a target of feedback inhibition.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']
	total_enzymes = len(pathway['enzymes'])

	# correct answer is the committed step of the focus branch
	if focus_branch == 1:
		correct_enzyme = e_b1_first
	else:
		correct_enzyme = e_b2_first
	answer_text = f"enzyme E<sub>{correct_enzyme}</sub>"

	# build distractor enzyme IDs (trunk always has 3+ metabolites, so E2 always exists)
	distractor_ids = [1, 2]
	if e_b1_first + 1 <= total_enzymes:
		distractor_ids.append(e_b1_first + 1)
	if e_b2_first + 1 <= total_enzymes:
		distractor_ids.append(e_b2_first + 1)
	if focus_branch == 1:
		distractor_ids.append(e_b2_first)
	else:
		distractor_ids.append(e_b1_first)
	choices_list = metaboliclib.build_enzyme_choices(answer_text, correct_enzyme, distractor_ids)

	# which end product inhibits this enzyme
	if focus_branch == 1:
		end_txt = metaboliclib.color_text(pathway['b1_end'][0], pathway['b1_end'][1])
	else:
		end_txt = metaboliclib.color_text(pathway['b2_end'][0], pathway['b2_end'][1])

	# question text
	# build diagram inline for this question
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>The end product {end_txt} acts as a feedback inhibitor. "
	question_text += "<b>Which enzyme is the most likely target of this feedback "
	question_text += "inhibition?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_accumulation_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when an end product concentration is very high.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	bp_mol = pathway['bp_mol']
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']

	if focus_branch == 1:
		focus_end = b1_end
		other_end = b2_end
		focus_first = pathway['b1'][0]
	else:
		focus_end = b2_end
		other_end = b1_end
		focus_first = pathway['b2'][0]

	bp_txt = metaboliclib.color_text(bp_mol[0], bp_mol[1])
	focus_end_txt = metaboliclib.color_text(focus_end[0], focus_end[1])
	other_end_txt = metaboliclib.color_text(other_end[0], other_end[1])
	focus_first_txt = metaboliclib.color_text(focus_first[0], focus_first[1])

	# question text
	# build diagram inline for this question
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If the concentration of {focus_end_txt} becomes "
	question_text += "<b>very high</b>, how would this most likely affect the pathway?</p>"

	answer_text = (
		f"metabolite {bp_txt} accumulates; "
		f"metabolite {other_end_txt} increases"
	)
	choices_list = [
		answer_text,
		f"metabolite {focus_first_txt} increases; metabolite {other_end_txt} decreases",
		f"metabolite {bp_txt} decreases; metabolite {focus_end_txt} continues to increase",
		f"all metabolites downstream of {bp_txt} decrease equally",
		f"metabolite {bp_txt} decreases; metabolite {other_end_txt} increases",
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_mutation_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when feedback inhibition is eliminated by mutation.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	bp_mol = pathway['bp_mol']
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']

	if focus_branch == 1:
		focus_enzyme = pathway['e_b1_first']
		focus_end = b1_end
		other_end = b2_end
	else:
		focus_enzyme = pathway['e_b2_first']
		focus_end = b2_end
		other_end = b1_end

	bp_txt = metaboliclib.color_text(bp_mol[0], bp_mol[1])
	focus_end_txt = metaboliclib.color_text(focus_end[0], focus_end[1])
	other_end_txt = metaboliclib.color_text(other_end[0], other_end[1])

	# question text
	# build diagram inline for this question
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If the inhibition of E<sub>{focus_enzyme}</sub> is "
	question_text += "<b>eliminated</b> by a mutation, but the "
	question_text += f"E<sub>{focus_enzyme}</sub> enzyme remains functional, "
	question_text += "what is the most likely outcome?</p>"

	answer_text = (
		f"metabolite {focus_end_txt} accumulates because "
		f"enzyme E<sub>{focus_enzyme}</sub> remains active"
	)
	choices_list = [
		answer_text,
		f"metabolite {focus_end_txt} decreases because feedback is required for enzyme activity",
		f"metabolite {other_end_txt} increases because both branches are activated",
		f"metabolite {bp_txt} accumulates because upstream reactions stop",
		f"metabolite {other_end_txt} decreases because less {bp_txt} is available",
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_rerouting_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when a branch enzyme is completely inactivated.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	bp_mol = pathway['bp_mol']
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']

	if focus_branch == 1:
		focus_enzyme = pathway['e_b1_first']
		other_end = b2_end
		other_name = 'lower'
	else:
		focus_enzyme = pathway['e_b2_first']
		other_end = b1_end
		other_name = 'upper'

	bp_txt = metaboliclib.color_text(bp_mol[0], bp_mol[1])
	other_end_txt = metaboliclib.color_text(other_end[0], other_end[1])

	# question text
	# build diagram inline for this question
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If enzyme <b>E<sub>{focus_enzyme}</sub></b> is completely "
	question_text += f"inactivated, what happens to the production of {other_end_txt}?</p>"

	answer_text = (
		f"metabolite {other_end_txt} "
		f"<span style='color: #1a7a1a; font-weight: 700;'>increases</span> "
		f"because {bp_txt} is redirected into the {other_name} branch"
	)
	choices_list = [
		answer_text,
		(
			f"metabolite {other_end_txt} "
			f"<span style='color: #c93030; font-weight: 700;'>decreases</span> "
			f"because {bp_txt} accumulates upstream"
		),
		(
			f"metabolite {other_end_txt} production is "
			"<span style='font-weight: 700;'>unchanged</span> because "
			"the branches are independent"
		),
		(
			f"metabolite {other_end_txt} "
			"<span style='color: #c93030; font-weight: 700;'>stops</span> "
			"because one branch is blocked"
		),
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_feedback_effects_question(pathway: dict, focus_branch: int, sub_type: str) -> tuple:
	"""MC question about feedback effects: either accumulation or mutation.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.
		sub_type (str): 'accumulation' or 'mutation'.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	if sub_type == 'accumulation':
		return _make_accumulation_question(pathway, focus_branch)
	elif sub_type == 'mutation':
		return _make_mutation_question(pathway, focus_branch)
	else:
		raise ValueError(f"Unknown sub_type: {sub_type}")

#============================================
#============================================
# question type dispatch table
QUESTION_MAKERS = {
	'inhibitor': _make_feedback_inhibitor_question,
	'enzyme': _make_regulated_enzyme_question,
	'feedback_effects': _make_feedback_effects_question,
	'rerouting': _make_rerouting_question,
}

#============================================
#============================================
def _get_scenarios(question_types: list) -> list:
	"""Generate all scenario combinations: pathway parameters x question type x branch.

	Args:
		question_types (list): List of question type keys to include.

	Returns:
		list: Each entry is (trunk_len, b1_len, b2_len, letter_shift,
		      question_type, focus_branch, sub_type).
	"""
	scenarios = []
	for trunk_len in (3, 4):
		for b1_len in (3, 4):
			for b2_len in (3, 4):
				total_mols = trunk_len + b1_len + b2_len
				for l_shift in range(0, 26 - total_mols, 4):
					for qtype in question_types:
						for focus_branch in (1, 2):
							if qtype == 'feedback_effects':
								for sub_type in ('accumulation', 'mutation'):
									scenarios.append((
										trunk_len, b1_len, b2_len,
										l_shift, qtype,
										focus_branch, sub_type
									))
							else:
								scenarios.append((
									trunk_len, b1_len, b2_len,
									l_shift, qtype,
									focus_branch, None
								))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""Creates a formatted MC question about feedback splitting in a branched pathway.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted MC question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	trunk_len, b1_len, b2_len, l_shift, qtype, focus_branch, sub_type = SCENARIOS[idx]

	# build the pathway via shorthand pipeline
	pathway = _build_pathway(trunk_len, b1_len, b2_len, l_shift)

	# generate the question using the dispatch table
	make_fn = QUESTION_MAKERS[qtype]
	if sub_type is not None:
		question_text, choices_list, answer_text = make_fn(pathway, focus_branch, sub_type)
	else:
		question_text, choices_list, answer_text = make_fn(pathway, focus_branch)

	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices_list, answer_text
	)
	return complete_question

#============================================
#============================================
# valid part names mapped to question type keys
PART_MAP = {
	'A': ['inhibitor'],
	'B': ['enzyme'],
	'C': ['feedback_effects'],
	'D': ['rerouting'],
}

#============================================
#============================================
def parse_arguments():
	"""Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate feedback splitting pathway MC questions."
	)
	parser = bptools.add_scenario_args(parser)
	valid_parts = list(PART_MAP.keys())
	parser.add_argument(
		'-p', '--part', dest='question_part', type=str.upper,
		choices=valid_parts, default=None,
		help=(
			"Generate only one question type: "
			"A=feedback inhibitors, B=regulated enzymes, "
			"C=feedback effects (accumulation/mutation), "
			"D=branch rerouting. Default: all parts."
		),
	)
	args = parser.parse_args()
	return args

#============================================
#============================================
def main():
	"""Main function that orchestrates question generation and file output."""
	args = parse_arguments()

	# determine which question types to include
	if args.question_part is not None:
		question_types = PART_MAP[args.question_part]
	else:
		question_types = list(QUESTION_MAKERS.keys())

	# initialize scenarios
	global SCENARIOS
	SCENARIOS = _get_scenarios(question_types)
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
