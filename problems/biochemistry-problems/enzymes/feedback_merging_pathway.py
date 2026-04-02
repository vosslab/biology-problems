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
		letter_shift: int) -> dict:
	"""Build pathway via shorthand pipeline: letters -> shorthand -> schema -> display model.

	Adds question context (convenience aliases) on top of the display model.

	Args:
		b1_len (int): Number of metabolites in upper branch (3 or 4).
		b2_len (int): Number of metabolites in lower branch (3 or 4).
		trunk_len (int): Number of metabolites in trunk (3 or 4).
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
	display = metaboliclib.build_display_model(schema)

	# add question-context convenience aliases
	display['mp_mol'] = display['junction_mol']
	display['b1_end'] = display['end_products']['b1']
	display['b2_end'] = display['end_products']['b2']
	display['e_b1_first'] = display['committed_step_enzymes']['b1']
	display['e_b2_first'] = display['committed_step_enzymes']['b2']
	return display

#============================================
#============================================
def _make_feedforward_activator_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: which metabolite provides feed-forward activation to the other branch.

	In a merging pathway, each branch's end product activates the committed
	step of the OTHER branch (cross-activation for coordinated supply).

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower (which branch is activated).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	b1 = pathway['b1']
	b2 = pathway['b2']
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']
	mp_mol = pathway['mp_mol']

	# the activator of the focus branch's committed step is the OTHER branch's end product
	if focus_branch == 1:
		# upper branch committed step is activated by the lower branch end product
		correct_mol = b2_end
		target_enzyme = pathway['e_b1_first']
	else:
		# lower branch committed step is activated by the upper branch end product
		correct_mol = b1_end
		target_enzyme = pathway['e_b2_first']
	answer_text = f"metabolite {metaboliclib.color_text(correct_mol[0], correct_mol[1])}"

	# distractors: metabolites that are NOT the correct activator
	distractors = [b1[0], b2[0], mp_mol]
	if focus_branch == 1 and len(b1) > 1:
		distractors.append(b1[1])
	elif focus_branch == 2 and len(b2) > 1:
		distractors.append(b2[1])
	choices_list = metaboliclib.build_metabolite_choices(answer_text, correct_mol, distractors)

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += "<p><b>Which metabolite provides a positive regulatory signal "
	question_text += f"to E<sub>{target_enzyme}</sub>?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_feedforward_target_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: which enzyme is the target of cross-activation from the focus branch.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower (which branch produces the activator).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']
	e_merge = pathway['e_merge']
	total_enzymes = len(pathway['enzymes'])

	# the focus branch's end product activates the OTHER branch's committed step
	if focus_branch == 1:
		focus_end = pathway['b1_end']
		# upper branch end product activates lower branch committed step
		correct_enzyme = e_b2_first
	else:
		focus_end = pathway['b2_end']
		# lower branch end product activates upper branch committed step
		correct_enzyme = e_b1_first
	answer_text = f"enzyme E<sub>{correct_enzyme}</sub>"

	# distractor enzyme IDs
	distractor_ids = [e_merge]
	# add the focus branch's own committed step (common misconception: same-branch)
	if focus_branch == 1:
		distractor_ids.append(e_b1_first)
	else:
		distractor_ids.append(e_b2_first)
	# add downstream enzymes
	if correct_enzyme + 1 <= total_enzymes:
		distractor_ids.append(correct_enzyme + 1)
	if e_merge + 1 <= total_enzymes:
		distractor_ids.append(e_merge + 1)
	choices_list = metaboliclib.build_enzyme_choices(answer_text, correct_enzyme, distractor_ids)

	focus_end_txt = metaboliclib.color_text(focus_end[0], focus_end[1])

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += "<p><b>Which enzyme receives a positive regulatory signal "
	question_text += f"from {focus_end_txt}?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_overproduction_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when one branch overproduces its end product.

	Tests whether students understand cross-activation consequences.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower (which branch overproduces).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	if focus_branch == 1:
		focus_end = pathway['b1_end']
		other_end = pathway['b2_end']
		other_enzyme = pathway['e_b2_first']
		focus_name = 'upper'
		other_name = 'lower'
	else:
		focus_end = pathway['b2_end']
		other_end = pathway['b1_end']
		other_enzyme = pathway['e_b1_first']
		focus_name = 'lower'
		other_name = 'upper'

	focus_end_txt = metaboliclib.color_text(focus_end[0], focus_end[1])
	other_end_txt = metaboliclib.color_text(other_end[0], other_end[1])

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If the {focus_name} branch overproduces {focus_end_txt}, "
	question_text += f"what is the most likely effect on the {other_name} branch?</p>"

	answer_text = (
		f"the {other_name} branch is stimulated because "
		f"{focus_end_txt} activates E<sub>{other_enzyme}</sub>, "
		f"tending to increase {other_end_txt} production"
	)
	choices_list = [
		answer_text,
		(
			f"the {other_name} branch slows because "
			f"{focus_end_txt} inhibits E<sub>{other_enzyme}</sub>"
		),
		(
			f"the {other_name} branch is unaffected because "
			f"the two branches are independent"
		),
		(
			f"the excess {focus_end_txt} is rerouted into "
			f"the {other_name} branch"
		),
		(
			f"the {other_name} branch shuts down because "
			f"only one branch is needed"
		),
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_lost_crossactivation_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when cross-activation is eliminated by mutation.

	Tests whether students understand coordination consequences.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower (which branch's signal is lost).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	mp_mol = pathway['mp_mol']

	if focus_branch == 1:
		focus_end = pathway['b1_end']
		other_end = pathway['b2_end']
		other_enzyme = pathway['e_b2_first']
		focus_name = 'upper'
		other_name = 'lower'
	else:
		focus_end = pathway['b2_end']
		other_end = pathway['b1_end']
		other_enzyme = pathway['e_b1_first']
		focus_name = 'lower'
		other_name = 'upper'

	focus_end_txt = metaboliclib.color_text(focus_end[0], focus_end[1])
	other_end_txt = metaboliclib.color_text(other_end[0], other_end[1])
	mp_txt = metaboliclib.color_text(mp_mol[0], mp_mol[1])

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += "<p>If a mutation eliminates the activation of "
	question_text += f"E<sub>{other_enzyme}</sub> by {focus_end_txt}, "
	question_text += "but all enzymes remain functional, "
	question_text += "what is the most likely effect on the pathway?</p>"

	answer_text = (
		f"the {other_name} branch loses feed-forward stimulation; "
		f"substrate supply becomes imbalanced; the merge step tends to be "
		f"limited by {other_end_txt} availability"
	)
	choices_list = [
		answer_text,
		(
			f"the {other_name} branch shuts down completely because "
			f"E<sub>{other_enzyme}</sub> requires activation to function"
		),
		(
			f"the {focus_name} branch compensates by increasing its "
			f"own production of {focus_end_txt}"
		),
		(
			"the pathway is unaffected because feed-forward activation "
			"is not essential for enzyme function"
		),
		(
			f"{mp_txt} production increases because the "
			f"{other_name} branch runs unchecked"
		),
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_imbalance_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when one branch has excess and the other is deficient.

	Core constraint-thinking question: the merge requires BOTH substrates.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower (which branch overproduces).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	mp_mol = pathway['mp_mol']

	if focus_branch == 1:
		focus_end = pathway['b1_end']
		other_end = pathway['b2_end']
		focus_name = 'upper'
		other_name = 'lower'
	else:
		focus_end = pathway['b2_end']
		other_end = pathway['b1_end']
		focus_name = 'lower'
		other_name = 'upper'

	focus_end_txt = metaboliclib.color_text(focus_end[0], focus_end[1])
	other_end_txt = metaboliclib.color_text(other_end[0], other_end[1])
	mp_txt = metaboliclib.color_text(mp_mol[0], mp_mol[1])

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If the {focus_name} branch produces an excess of "
	question_text += f"{focus_end_txt} but the {other_name} branch produces "
	question_text += f"less {other_end_txt} than normal, what is the most "
	question_text += f"likely effect on {mp_txt} production?</p>"

	answer_text = (
		f"{mp_txt} production is limited by the {other_name} branch; "
		f"excess {focus_end_txt} cannot compensate for "
		f"insufficient {other_end_txt}"
	)
	choices_list = [
		answer_text,
		(
			f"{mp_txt} increases because more {focus_end_txt} "
			f"is available for the merge reaction"
		),
		(
			f"excess {focus_end_txt} drives the merge reaction forward "
			f"despite low {other_end_txt}"
		),
		(
			f"the excess {focus_end_txt} is rerouted to increase "
			f"{other_end_txt} production"
		),
		(
			f"{mp_txt} is unchanged because the branches "
			f"are independent of each other"
		),
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_coordination_question(pathway: dict, focus_branch: int, sub_type: str) -> tuple:
	"""MC question about coordination effects: overproduction, lost activation, or imbalance.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.
		sub_type (str): 'overproduction', 'lost_crossactivation', or 'imbalance'.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	if sub_type == 'overproduction':
		return _make_overproduction_question(pathway, focus_branch)
	elif sub_type == 'lost_crossactivation':
		return _make_lost_crossactivation_question(pathway, focus_branch)
	elif sub_type == 'imbalance':
		return _make_imbalance_question(pathway, focus_branch)
	else:
		raise ValueError(f"Unknown sub_type: {sub_type}")

#============================================
#============================================
def _make_blocked_branch_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: what happens when a branch enzyme is completely inactivated.

	In a merging pathway, blocking one branch reduces total input to the merge.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	mp_mol = pathway['mp_mol']

	if focus_branch == 1:
		focus_enzyme = pathway['e_b1_first']
		other_name = 'lower'
	else:
		focus_enzyme = pathway['e_b2_first']
		other_name = 'upper'

	mp_txt = metaboliclib.color_text(mp_mol[0], mp_mol[1])

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += f"<p>If enzyme <b>E<sub>{focus_enzyme}</sub></b> is completely "
	question_text += f"inactivated, what happens to the production of {mp_txt}?</p>"

	answer_text = (
		f"metabolite {mp_txt} "
		f"<span style='color: #c93030; font-weight: 700;'>decreases</span> "
		f"because one required input branch is blocked; "
		f"the {other_name} branch alone cannot supply enough substrate"
	)
	choices_list = [
		answer_text,
		(
			f"metabolite {mp_txt} "
			f"<span style='color: #1a7a1a; font-weight: 700;'>increases</span> "
			f"because the {other_name} branch compensates fully"
		),
		(
			f"metabolite {mp_txt} production is "
			"<span style='font-weight: 700;'>unchanged</span> because "
			"both branches contribute equally"
		),
		(
			f"metabolite {mp_txt} production "
			"<span style='color: #c93030; font-weight: 700;'>stops completely</span> "
			"because the merge reaction requires input from both branches"
		),
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_feedforward_purpose_question(pathway: dict, focus_branch: int) -> tuple:
	"""MC question: why does cross-activation exist in converging pathways.

	Tests whether students understand the coordination problem.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper, 2 for lower (not used; question is general).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']

	b1_end_txt = metaboliclib.color_text(b1_end[0], b1_end[1])
	b2_end_txt = metaboliclib.color_text(b2_end[0], b2_end[1])

	# question text
	diagram = metaboliclib.render_pathway_table(metaboliclib.build_layout_plan(pathway))
	question_text = metaboliclib.pathway_intro_text(diagram)
	question_text += "<p>In this converging pathway, "
	question_text += f"{b1_end_txt} activates E<sub>{e_b2_first}</sub> "
	question_text += f"and {b2_end_txt} activates E<sub>{e_b1_first}</sub> "
	question_text += "(feed-forward cross-activation). "
	question_text += "<b>What problem does this regulatory mechanism solve?</b></p>"

	answer_text = (
		"it matches production of both substrates required for the "
		"merge reaction; when one branch increases output, it stimulates "
		"the other branch to keep pace"
	)
	choices_list = [
		answer_text,
		(
			"it provides a backup pathway if one branch fails, ensuring "
			"the merge product is still produced"
		),
		(
			"it inhibits the other branch to prevent overproduction "
			"of merge substrates"
		),
		(
			"it has no functional advantage; it is an evolutionary "
			"artifact with no effect on pathway flux"
		),
	]
	random.shuffle(choices_list)

	return question_text, choices_list, answer_text

#============================================
#============================================
# question type dispatch table
QUESTION_MAKERS = {
	'activator': _make_feedforward_activator_question,
	'target': _make_feedforward_target_question,
	'coordination': _make_coordination_question,
	'blocked_branch': _make_blocked_branch_question,
	'feedforward_purpose': _make_feedforward_purpose_question,
}

#============================================
#============================================
def _get_scenarios(question_types: list) -> list:
	"""Generate all scenario combinations: pathway parameters x question type x branch.

	Args:
		question_types (list): List of question type keys to include.

	Returns:
		list: Each entry is (b1_len, b2_len, trunk_len, letter_shift,
		      question_type, focus_branch, sub_type).
	"""
	scenarios = []
	for b1_len in (3, 4):
		for b2_len in (3, 4):
			for trunk_len in (3, 4):
				total_mols = b1_len + b2_len + trunk_len
				for l_shift in range(0, 26 - total_mols, 4):
					for qtype in question_types:
						for focus_branch in (1, 2):
							if qtype == 'coordination':
								for sub_type in ('overproduction', 'lost_crossactivation', 'imbalance'):
									scenarios.append((
										b1_len, b2_len, trunk_len,
										l_shift, qtype,
										focus_branch, sub_type
									))
							else:
								scenarios.append((
									b1_len, b2_len, trunk_len,
									l_shift, qtype,
									focus_branch, None
								))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""Creates a formatted MC question about coordination in a merging pathway.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted MC question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	b1_len, b2_len, trunk_len, l_shift, qtype, focus_branch, sub_type = SCENARIOS[idx]

	# build the pathway via shorthand pipeline
	pathway = _build_pathway(b1_len, b2_len, trunk_len, l_shift)

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
	'A': ['activator'],
	'B': ['target'],
	'C': ['coordination'],
	'D': ['blocked_branch'],
	'E': ['feedforward_purpose'],
}

#============================================
#============================================
def parse_arguments():
	"""Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate merging pathway coordination MC questions."
	)
	parser = bptools.add_scenario_args(parser)
	valid_parts = list(PART_MAP.keys())
	parser.add_argument(
		'-p', '--part', dest='question_part', type=str.upper,
		choices=valid_parts, default=None,
		help=(
			"Generate only one question type: "
			"A=feed-forward activators, B=cross-activation targets, "
			"C=coordination effects (overproduction/lost activation/imbalance), "
			"D=blocked branch, E=why coordination exists. Default: all parts."
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
