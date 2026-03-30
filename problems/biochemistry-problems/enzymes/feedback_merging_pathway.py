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
def _build_pathway(b1_len: int, b2_len: int, trunk_len: int, color_shift: int, letter_shift: int) -> dict:
	"""
	Build the pathway data for a merging topology: two branches converge to a trunk.

	Args:
		b1_len (int): Number of metabolites in upper branch (3 or 4).
		b2_len (int): Number of metabolites in lower branch (3 or 4).
		trunk_len (int): Number of metabolites in trunk (3 or 4).
		color_shift (int): Starting index in the color palette.
		letter_shift (int): Starting index in the alphabet.

	Returns:
		dict: Pathway structure with trunk, branches, enzyme info, and merge point.
	"""
	# total molecules: both branches + trunk
	total_mols = b1_len + b2_len + trunk_len

	# use metaboliclib to assign letters and colors
	all_metabolites = metaboliclib.assign_metabolites(total_mols, color_shift, letter_shift)

	# assign metabolites: b1 first, then b2, then trunk
	b1 = all_metabolites[:b1_len]
	b2 = all_metabolites[b1_len:b1_len + b2_len]
	trunk = all_metabolites[b1_len + b2_len:]

	# enzyme numbering:
	# E1 through E(b1_len-1) are b1 internal enzymes
	# E(b1_len) is the merge enzyme
	# E(b1_len+1) through E(b1_len+trunk_len-1) are trunk enzymes
	# E(b1_len+trunk_len) through E(b1_len+trunk_len+b2_len-1) are b2 internal enzymes
	# Actually: b1 has b1_len-1 internal steps, then merge step, then trunk has trunk_len-1 steps,
	# then b2 has b2_len-1 steps.
	# Simpler: E1 thru E(b1_len-1) = b1, E(b1_len) = merge, E(b1_len+1) thru E(b1_len+trunk_len-1) = trunk,
	# E(b1_len+trunk_len) thru E(b1_len+trunk_len+b2_len-1) = b2

	e_b1_first = 1
	e_merge = b1_len
	e_trunk_first = b1_len + 1
	e_b2_first = b1_len + trunk_len

	pathway = {
		'b1': b1,
		'b2': b2,
		'trunk': trunk,
		'b1_len': b1_len,
		'b2_len': b2_len,
		'trunk_len': trunk_len,
		'e_b1_first': e_b1_first,
		'e_merge': e_merge,
		'e_trunk_first': e_trunk_first,
		'e_b2_first': e_b2_first,
		'mp_mol': trunk[0],
		'trunk_end': trunk[-1],
		'b1_end': b1[-1],
		'b2_end': b2[-1],
	}
	return pathway

#============================================
#============================================
def _make_pathway_diagram(pathway: dict) -> str:
	"""
	Build an HTML table showing a merging metabolic pathway.
	Branches converge from left (down and up arrows) into a single trunk on the right.

	Args:
		pathway (dict): Pathway structure from _build_pathway.

	Returns:
		str: HTML table string for the pathway diagram.
	"""
	b1 = pathway['b1']
	b2 = pathway['b2']
	trunk = pathway['trunk']
	e_b1_first = pathway['e_b1_first']
	e_merge = pathway['e_merge']
	e_trunk_first = pathway['e_trunk_first']
	e_b2_first = pathway['e_b2_first']

	# grid geometry:
	# branch columns on the left (max(b1_len, b2_len) determines width)
	# junction column in the middle
	# trunk columns on the right
	max_branch = max(len(b1), len(b2))
	branch_start = 0
	branch_cols = 2 * max_branch - 1
	junction_col = branch_cols
	# junction_col = merge arrow-tail, junction_col+1 = regular arrow, then trunk metabolites
	trunk_start = junction_col + 2
	trunk_cols = 2 * len(trunk) - 1
	total_cols = trunk_start + trunk_cols + 1  # +1 for ellipsis on far right

	# === Row 0: B1 enzyme labels (left columns only) ===
	b1_enzyme_positions = [
		(branch_start + 2 * i + 1, e_b1_first + i)
		for i in range(len(b1) - 1)
	]
	b1_enzyme_row = metaboliclib.make_enzyme_label_row(total_cols, b1_enzyme_positions)

	# === Row 1: B1 metabolites + arrows, then SE arrow at junction ===
	b1_struct_row = metaboliclib.make_metabolite_row(total_cols, b1, branch_start)
	# SE arrow at junction (b1 goes down to merge)
	b1_struct_row[junction_col] = f"<td style='{metaboliclib.CSS_ARR}'>&#8600;</td>"

	# === Row 2: Trunk enzyme labels (right columns only) ===
	trunk_enzyme_positions = [
		(trunk_start + 1 + 2 * i, e_trunk_first + i)
		for i in range(len(trunk) - 1)
	]
	trunk_enzyme_row = metaboliclib.make_enzyme_label_row(total_cols, trunk_enzyme_positions)
	# merge enzyme label (at junction)
	trunk_enzyme_row[junction_col] = f"<td style='{metaboliclib.CSS_LBL}'>E<sub>{e_merge}</sub></td>"

	# === Row 3: Trunk metabolites + arrows (starting after junction) ===
	trunk_struct_row = metaboliclib.make_metabolite_row(total_cols, trunk, trunk_start)
	# merge arrow-tail + regular arrow before first trunk metabolite
	trunk_struct_row[junction_col] = f"<td style='{metaboliclib.CSS_ARR}'>&#x291A;</td>"
	trunk_struct_row[junction_col + 1] = f"<td style='{metaboliclib.CSS_ARR}'>&rarr;</td>"
	# ellipsis on far right to show continuation
	if trunk_cols + trunk_start + 2 < total_cols:
		trunk_struct_row[-1] = f"<td style='{metaboliclib.CSS_DOTS}'>&middot;&middot;&middot;</td>"

	# === Row 4: B2 metabolites + arrows, then NE arrow at junction ===
	b2_struct_row = metaboliclib.make_metabolite_row(total_cols, b2, branch_start)
	# NE arrow at junction (b2 goes up to merge)
	b2_struct_row[junction_col] = f"<td style='{metaboliclib.CSS_ARR}'>&#8599;</td>"

	# === Row 5: B2 enzyme labels (left columns only) ===
	b2_enzyme_positions = [
		(branch_start + 2 * i + 1, e_b2_first + i)
		for i in range(len(b2) - 1)
	]
	b2_enzyme_row = metaboliclib.make_enzyme_label_row(total_cols, b2_enzyme_positions)

	# assemble the table in 6 rows: B1 enzymes, B1 struct, Trunk enzymes, Trunk struct, B2 struct, B2 enzymes
	rows = [b1_enzyme_row, b1_struct_row, trunk_enzyme_row, trunk_struct_row, b2_struct_row, b2_enzyme_row]
	table = metaboliclib.assemble_pathway_table(rows)

	return table

#============================================
#============================================
def _make_feedback_inhibitor_question(pathway: dict, focus_branch: int) -> tuple:
	"""
	MC question: which metabolite is most likely a feedback inhibitor.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch (not used, trunk_end is always correct).

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	b1 = pathway['b1']
	b2 = pathway['b2']
	trunk_end = pathway['trunk_end']
	mp_mol = pathway['mp_mol']

	# correct answer is the trunk end product (it inhibits both input branches)
	correct_mol = trunk_end
	answer_text = f"metabolite {metaboliclib.color_text(correct_mol[0], correct_mol[1])}"

	# build distractor set
	distractors = [b1[0], b2[0], mp_mol]
	if len(b1) > 1:
		distractors.append(b1[1])
	if len(b2) > 1:
		distractors.append(b2[1])

	# deduplicate
	seen = {correct_mol[0]}
	unique_distractors = []
	for mol in distractors:
		if mol[0] not in seen:
			seen.add(mol[0])
			unique_distractors.append(mol)

	# build choices
	choices_list = [answer_text]
	for mol in unique_distractors[:4]:
		choices_list.append(f"metabolite {metaboliclib.color_text(mol[0], mol[1])}")
	random.shuffle(choices_list)

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
	"""
	MC question: which enzyme is most likely a target of feedback inhibition.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	b1 = pathway['b1']
	b2 = pathway['b2']
	trunk = pathway['trunk']
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']
	e_trunk_first = pathway['e_trunk_first']
	e_merge = pathway['e_merge']
	trunk_end = pathway['trunk_end']

	# correct answer is the committed step of the focus branch
	if focus_branch == 1:
		correct_enzyme = e_b1_first
	else:
		correct_enzyme = e_b2_first
	answer_text = f"enzyme E<sub>{correct_enzyme}</sub>"

	# build distractor enzyme numbers
	distractor_nums = [e_merge]
	if e_trunk_first < len(b1) + len(b2) + len(trunk):
		distractor_nums.append(e_trunk_first)
	if e_trunk_first + 1 < len(b1) + len(b2) + len(trunk):
		distractor_nums.append(e_trunk_first + 1)
	# add the other branch's committed step
	if focus_branch == 1:
		distractor_nums.append(e_b2_first)
	else:
		distractor_nums.append(e_b1_first)

	# deduplicate, remove correct
	seen = {correct_enzyme}
	unique_distractors = []
	for e in distractor_nums:
		if e not in seen:
			seen.add(e)
			unique_distractors.append(e)

	# build choices
	choices_list = [answer_text]
	for e in unique_distractors[:4]:
		choices_list.append(f"enzyme E<sub>{e}</sub>")
	random.shuffle(choices_list)

	# determine which end product inhibits this enzyme
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
	"""
	MC question: what happens when the trunk end product concentration becomes very high.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	b1 = pathway['b1']
	b2 = pathway['b2']
	trunk_end = pathway['trunk_end']
	mp_mol = pathway['mp_mol']

	if focus_branch == 1:
		focus_first = b1[0]
		other_first = b2[0]
	else:
		focus_first = b2[0]
		other_first = b1[0]

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
	"""
	MC question: what happens when feedback inhibition is eliminated by mutation.

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
		f"metabolite {focus_first_txt} accumulates and overproduces {mp_txt} "
		f"from that branch; {trunk_end_txt} increases"
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
	"""
	MC question: what happens when a branch enzyme is completely inactivated.
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
	"""
	MC question about feedback effects: either accumulation or mutation.

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
	"""
	Generate all scenario combinations: pathway parameters x question type x branch.

	For 'feedback_effects', generates both 'accumulation' and 'mutation' sub-types.

	Args:
		question_types (list): List of question type keys to include.

	Returns:
		list: Each entry is (b1_len, b2_len, trunk_len, color_shift, letter_shift,
		      question_type, focus_branch, sub_type).
		      sub_type is a string ('accumulation' or 'mutation') for 'feedback_effects',
		      or None for other question types.
	"""
	scenarios = []
	for b1_len in (3, 4):
		for b2_len in (3, 4):
			for trunk_len in (3, 4):
				total_mols = b1_len + b2_len + trunk_len
				# color shifts (sample 5 from the palette)
				for c_shift in range(0, len(metaboliclib.all_colors), 3):
					# letter shifts (sample a few starting positions)
					for l_shift in range(0, 26 - total_mols, 4):
						for qtype in question_types:
							for focus_branch in (1, 2):
								if qtype == 'feedback_effects':
									# generate both sub-types for feedback effects
									for sub_type in ('accumulation', 'mutation'):
										scenarios.append((
											b1_len, b2_len, trunk_len,
											c_shift, l_shift, qtype, focus_branch, sub_type
										))
								else:
									# other question types have no sub_type
									scenarios.append((
										b1_len, b2_len, trunk_len,
										c_shift, l_shift, qtype, focus_branch, None
									))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted MC question about feedback regulation in a merging pathway.

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

	# build the pathway
	pathway = _build_pathway(b1_len, b2_len, trunk_len, c_shift, l_shift)

	# generate the question using the dispatch table
	make_fn = QUESTION_MAKERS[qtype]
	if sub_type is not None:
		question_text, choices_list, answer_text = make_fn(pathway, focus_branch, sub_type)
	else:
		question_text, choices_list, answer_text = make_fn(pathway, focus_branch)

	# format as MC question
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
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate feedback merging pathway MC questions."
	)
	parser = bptools.add_scenario_args(parser)
	# part selection: restrict to one or more question types
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
	"""
	Main function that orchestrates question generation and file output.
	"""
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
