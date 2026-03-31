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
def _build_pathway(b1_len: int, b2_len: int, trunk_len: int,
		color_shift: int, letter_shift: int) -> dict:
	"""Build pathway via shorthand pipeline: letters -> shorthand -> schema -> display model.

	Adds question context (convenience aliases) on top of the display model.

	Args:
		b1_len (int): Number of metabolites in upper branch (3 or 4).
		b2_len (int): Number of metabolites in lower branch (3 or 4).
		trunk_len (int): Number of metabolites in trunk (3 or 4).
		color_shift (int): Starting index in the color palette.
		letter_shift (int): Starting index in the alphabet.

	Returns:
		dict: Display model + question context keys.
	"""
	# pick sequential letters starting at letter_shift
	# merging order: b1 first, then b2, then trunk (matches original assignment)
	total = b1_len + b2_len + trunk_len
	letters = list(metaboliclib.ALL_LETTERS[letter_shift:letter_shift + total])
	b1_letters = letters[:b1_len]
	b2_letters = letters[b1_len:b1_len + b2_len]
	trunk_letters = letters[b1_len + b2_len:]

	# build shorthand, parse, and decorate
	shorthand = metaboliclib.build_shorthand('merge', trunk_letters, b1_letters, b2_letters)
	schema = metaboliclib.parse_shorthand(shorthand)
	display = metaboliclib.build_display_model(schema, color_shift)

	# add question-context convenience aliases
	display['mp_mol'] = display['junction_mol']
	display['trunk_end'] = display['end_products']['trunk']
	display['b1_end'] = display['end_products']['b1']
	display['b2_end'] = display['end_products']['b2']
	display['e_b1_first'] = display['committed_step_enzymes']['b1']
	display['e_b2_first'] = display['committed_step_enzymes']['b2']
	display['trunk_len'] = trunk_len
	display['b1_len'] = b1_len
	display['b2_len'] = b2_len
	display['shorthand'] = shorthand
	return display

#============================================
#============================================
def _make_pathway_diagram(pathway: dict) -> str:
	"""Render the pathway diagram via the layout pipeline.

	Args:
		pathway (dict): Display model from _build_pathway.

	Returns:
		str: HTML table string.
	"""
	layout = metaboliclib.build_layout_plan(pathway)
	table = metaboliclib.render_pathway_table(layout)
	return table

#============================================
#============================================
def _make_feedback_inhibitor_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: which metabolite is most likely a feedback inhibitor.

	In a merging pathway, the trunk end product inhibits both input branches.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 or 2 (not used; trunk_end is always correct).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	b1 = pathway['b1']
	b2 = pathway['b2']
	trunk_end = pathway['trunk_end']
	mp_mol = pathway['mp_mol']

	# correct answer is the trunk end product
	correct_mol = trunk_end
	answer_text = f"metabolite {metaboliclib.color_text(correct_mol[0], correct_mol[1])}"

	# build distractor set
	distractors = [b1[0], b2[0], mp_mol]
	if len(b1) > 1:
		distractors.append(b1[1])
	if len(b2) > 1:
		distractors.append(b2[1])
	choices_list = metaboliclib.build_metabolite_choices(answer_text, correct_mol, distractors)

	# question text
	diagram = _make_pathway_diagram(pathway)
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += "<p>In feedback regulation, end products inhibit "
	question_text += "the committed steps of their input pathways. "
	question_text += "<b>Which metabolite is most likely to act as a feedback "
	question_text += "inhibitor in this pathway?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_regulated_enzyme_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: which enzyme is most likely a target of feedback inhibition.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']
	e_trunk_first = pathway['e_trunk_first']
	e_merge = pathway['e_merge']
	trunk_end = pathway['trunk_end']
	total_enzymes = len(pathway['enzymes'])

	# correct answer is the committed step of the focus branch
	if focus_branch == 1:
		correct_enzyme = e_b1_first
	else:
		correct_enzyme = e_b2_first
	answer_text = f"enzyme E<sub>{correct_enzyme}</sub>"

	# build distractor enzyme IDs
	distractor_ids = [e_merge]
	if e_trunk_first <= total_enzymes:
		distractor_ids.append(e_trunk_first)
	if e_trunk_first + 1 <= total_enzymes:
		distractor_ids.append(e_trunk_first + 1)
	if focus_branch == 1:
		distractor_ids.append(e_b2_first)
	else:
		distractor_ids.append(e_b1_first)
	choices_list = metaboliclib.build_enzyme_choices(answer_text, correct_enzyme, distractor_ids)

	trunk_end_txt = metaboliclib.color_text(trunk_end[0], trunk_end[1])

	# question text
	diagram = _make_pathway_diagram(pathway)
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>The end product {trunk_end_txt} acts as a feedback inhibitor. "
	question_text += "<b>Which enzyme is the most likely target of this feedback "
	question_text += "inhibition?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_accumulation_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when trunk end product concentration becomes very high.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	trunk_end = pathway['trunk_end']
	mp_mol = pathway['mp_mol']

	if focus_branch == 1:
		focus_first = pathway['b1'][0]
		other_first = pathway['b2'][0]
	else:
		focus_first = pathway['b2'][0]
		other_first = pathway['b1'][0]

	trunk_end_txt = metaboliclib.color_text(trunk_end[0], trunk_end[1])
	mp_txt = metaboliclib.color_text(mp_mol[0], mp_mol[1])
	focus_first_txt = metaboliclib.color_text(focus_first[0], focus_first[1])
	other_first_txt = metaboliclib.color_text(other_first[0], other_first[1])

	# question text
	diagram = _make_pathway_diagram(pathway)
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If the concentration of {trunk_end_txt} becomes "
	question_text += "<b>very high</b>, how would this most likely affect the pathway?</p>"

	answer_text = (
		f"metabolite {focus_first_txt} and metabolite {other_first_txt} "
		f"both accumulate; input into {mp_txt} decreases"
	)
	choices_list = [
		answer_text,
		f"metabolite {mp_txt} increases dramatically; metabolite {focus_first_txt} continues to accumulate",
		f"metabolite {focus_first_txt} increases; metabolite {other_first_txt} decreases",
		f"all metabolites upstream of {mp_txt} decrease equally",
		f"metabolite {mp_txt} accumulates while {focus_first_txt} and {other_first_txt} are depleted",
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_mutation_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when feedback inhibition is eliminated by mutation.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	mp_mol = pathway['mp_mol']
	trunk_end = pathway['trunk_end']

	if focus_branch == 1:
		focus_enzyme = pathway['e_b1_first']
		focus_first = pathway['b1'][0]
	else:
		focus_enzyme = pathway['e_b2_first']
		focus_first = pathway['b2'][0]

	trunk_end_txt = metaboliclib.color_text(trunk_end[0], trunk_end[1])
	mp_txt = metaboliclib.color_text(mp_mol[0], mp_mol[1])
	focus_first_txt = metaboliclib.color_text(focus_first[0], focus_first[1])

	# question text
	diagram = _make_pathway_diagram(pathway)
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If the inhibition of E<sub>{focus_enzyme}</sub> by "
	question_text += f"{trunk_end_txt} is <b>eliminated</b> by a mutation, but the "
	question_text += f"E<sub>{focus_enzyme}</sub> enzyme remains functional, "
	question_text += "what is the most likely outcome?</p>"

	answer_text = (
		f"enzyme E<sub>{focus_enzyme}</sub> runs unchecked, overproducing "
		f"{mp_txt} from that branch; {trunk_end_txt} increases"
	)
	choices_list = [
		answer_text,
		f"metabolite {focus_first_txt} decreases because feedback is required for enzyme activity",
		f"metabolite {focus_first_txt} continues normally because the other branch compensates",
		f"metabolite {mp_txt} cannot accumulate because it is immediately converted to {trunk_end_txt}",
		f"enzyme E<sub>{focus_enzyme}</sub> becomes completely inactive",
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_blocked_branch_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when a branch enzyme is completely inactivated.

	In a merging pathway, blocking one branch reduces total input to the trunk.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	mp_mol = pathway['mp_mol']
	trunk_end = pathway['trunk_end']

	if focus_branch == 1:
		focus_enzyme = pathway['e_b1_first']
		other_name = 'lower'
	else:
		focus_enzyme = pathway['e_b2_first']
		other_name = 'upper'

	trunk_end_txt = metaboliclib.color_text(trunk_end[0], trunk_end[1])
	mp_txt = metaboliclib.color_text(mp_mol[0], mp_mol[1])

	# question text
	diagram = _make_pathway_diagram(pathway)
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If enzyme <b>E<sub>{focus_enzyme}</sub></b> is completely "
	question_text += f"inactivated, what happens to the production of {trunk_end_txt}?</p>"

	answer_text = (
		f"metabolite {trunk_end_txt} "
		f"<span style='color: #c93030; font-weight: 700;'>decreases</span> "
		f"because one required input branch is blocked; "
		f"only the {other_name} branch provides {mp_txt}"
	)
	choices_list = [
		answer_text,
		(
			f"metabolite {trunk_end_txt} "
			f"<span style='color: #1a7a1a; font-weight: 700;'>increases</span> "
			f"because the {other_name} branch compensates fully"
		),
		(
			f"metabolite {trunk_end_txt} production is "
			"<span style='font-weight: 700;'>unchanged</span> because "
			"both branches contribute equally"
		),
		(
			f"metabolite {trunk_end_txt} "
			"<span style='color: #c93030; font-weight: 700;'>stops</span> "
			"because the trunk requires input from both branches"
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
	'blocked_branch': _make_blocked_branch_question,
}

#============================================
#============================================
def _get_scenarios(question_types: list) -> list:
	"""Generate all scenario combinations: pathway parameters x question type x branch.

	Args:
		question_types (list): List of question type keys to include.

	Returns:
		list: Each entry is (b1_len, b2_len, trunk_len, color_shift, letter_shift,
		      question_type, focus_branch, sub_type).
	"""
	scenarios = []
	for b1_len in (3, 4):
		for b2_len in (3, 4):
			for trunk_len in (3, 4):
				total_mols = b1_len + b2_len + trunk_len
				for c_shift in range(0, len(metaboliclib.ALL_COLORS), 3):
					for l_shift in range(0, 26 - total_mols, 4):
						for qtype in question_types:
							for focus_branch in (1, 2):
								if qtype == 'feedback_effects':
									for sub_type in ('accumulation', 'mutation'):
										scenarios.append((
											b1_len, b2_len, trunk_len,
											c_shift, l_shift, qtype,
											focus_branch, sub_type
										))
								else:
									scenarios.append((
										b1_len, b2_len, trunk_len,
										c_shift, l_shift, qtype,
										focus_branch, None
									))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""Creates a formatted MC question about feedback regulation in a merging pathway.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted MC question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	b1_len, b2_len, trunk_len, c_shift, l_shift, qtype, focus_branch, sub_type = SCENARIOS[idx]

	# build the pathway via shorthand pipeline
	pathway = _build_pathway(b1_len, b2_len, trunk_len, c_shift, l_shift)

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
	'D': ['blocked_branch'],
}

#============================================
#============================================
def parse_arguments():
	"""Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate feedback merging pathway MC questions."
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
			"D=blocked branch effects. Default: all parts."
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
