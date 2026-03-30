#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
import bptools

# color palette (14 high-contrast colors), matching metaboliclib
PALETTE = [
	'#d40000', '#b74300', '#935d00', '#6c6c00', '#3b7600',
	'#007a00', '#00775f', '#007576', '#076dad', '#003fff',
	'#0067cc', '#a719db', '#c80085', '#cc0066',
]

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
#============================================
def _color_text(letter: str, color: str) -> str:
	"""
	Wrap a letter in colored bold HTML.

	Args:
		letter (str): The metabolite letter.
		color (str): Hex color string.

	Returns:
		str: HTML string with colored bold letter.
	"""
	html = f"<strong><span style='color: {color};'>{letter}</span></strong>"
	return html

#============================================
#============================================
def _met_node(letter: str, color: str) -> str:
	"""
	Create a circular metabolite node for the pathway diagram.

	Args:
		letter (str): The metabolite letter.
		color (str): Hex color string.

	Returns:
		str: HTML string for a circular colored node.
	"""
	html = (
		f"<span style='display: inline-block; width: 38px; height: 38px; "
		f"line-height: 38px; border-radius: 50%; background: {color}; "
		f"color: #fff; font-weight: 700; font-size: 16px; "
		f"border: 2px solid #333; text-align: center;'>{letter}</span>"
	)
	return html

#============================================
#============================================
def _build_pathway(trunk_len: int, b1_len: int, b2_len: int, color_shift: int, letter_shift: int) -> dict:
	"""
	Build the pathway data: metabolite letters, colors, and structure.

	Args:
		trunk_len (int): Number of metabolites in trunk (3 or 4).
		b1_len (int): Number of metabolites in upper branch (3 or 4).
		b2_len (int): Number of metabolites in lower branch (3 or 4).
		color_shift (int): Starting index in the color palette.
		letter_shift (int): Starting index in the alphabet.

	Returns:
		dict: Pathway structure with trunk, branches, enzyme info.
	"""
	total_mols = trunk_len + b1_len + b2_len
	all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	# pick colors with wraparound
	dbl_pal = PALETTE + PALETTE
	colors = dbl_pal[color_shift:color_shift + total_mols]

	# pick letters
	letters = list(all_letters[letter_shift:letter_shift + total_mols])

	# assign metabolites to trunk and branches
	trunk = [(letters[i], colors[i]) for i in range(trunk_len)]
	b1 = [(letters[trunk_len + i], colors[trunk_len + i]) for i in range(b1_len)]
	b2 = [(letters[trunk_len + b1_len + i], colors[trunk_len + b1_len + i]) for i in range(b2_len)]

	# enzyme numbering
	# E1 through E(trunk_len-1) are trunk enzymes
	# committed step of upper branch: enzyme number trunk_len
	# committed step of lower branch: enzyme number trunk_len + b1_len
	e_b1_first = trunk_len
	e_b2_first = trunk_len + b1_len

	pathway = {
		'trunk': trunk,
		'b1': b1,
		'b2': b2,
		'trunk_len': trunk_len,
		'b1_len': b1_len,
		'b2_len': b2_len,
		'e_b1_first': e_b1_first,
		'e_b2_first': e_b2_first,
		'bp_mol': trunk[-1],
		'b1_end': b1[-1],
		'b2_end': b2[-1],
	}
	return pathway

#============================================
#============================================
def _make_pathway_diagram(pathway: dict) -> str:
	"""
	Build an HTML table showing the branched metabolic pathway.

	Args:
		pathway (dict): Pathway structure from _build_pathway.

	Returns:
		str: HTML table string for the pathway diagram.
	"""
	trunk = pathway['trunk']
	b1 = pathway['b1']
	b2 = pathway['b2']
	trunk_len = pathway['trunk_len']
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']

	# CSS styles for table cells
	css_met = "border: 0; text-align: center; padding: 2px 4px;"
	css_arr = "border: 0; text-align: center; padding: 2px 2px; font-size: 150%;"
	css_lbl = "border: 0; text-align: center; padding: 0 2px; font-size: 75%; vertical-align: bottom;"
	css_empty = "border: 0; padding: 2px 4px;"
	css_dots = "border: 0; text-align: center; padding: 2px 2px; font-size: 120%; color: #888; letter-spacing: 2px;"

	# grid geometry
	first_trunk_col = 2
	last_trunk_col = first_trunk_col + 2 * (trunk_len - 1)
	junction_col = last_trunk_col + 1
	branch_start = junction_col + 1
	max_branch = max(len(b1), len(b2))
	total_cols = branch_start + 2 * max_branch - 1

	# helper to make an empty row
	def empty_row():
		return [f"<td style='{css_empty}'></td>"] * total_cols

	# --- Branch 1 enzyme label row ---
	b1_enzyme_row = empty_row()
	b1_enzyme_row[junction_col] = f"<td style='{css_lbl}'>E<sub>{e_b1_first}</sub></td>"
	for i in range(1, len(b1)):
		en = e_b1_first + i
		col = branch_start + 2 * i - 1
		if col < total_cols:
			b1_enzyme_row[col] = f"<td style='{css_lbl}'>E<sub>{en}</sub></td>"

	# --- Branch 1 structure row ---
	b1_struct_row = empty_row()
	b1_struct_row[junction_col] = f"<td style='{css_arr}'>&#8599;</td>"
	for i in range(len(b1)):
		col = branch_start + 2 * i
		if col < total_cols:
			b1_struct_row[col] = f"<td style='{css_met}'>{_met_node(b1[i][0], b1[i][1])}</td>"
		if i < len(b1) - 1:
			arrow_col = col + 1
			if arrow_col < total_cols:
				b1_struct_row[arrow_col] = f"<td style='{css_arr}'>&rarr;</td>"

	# --- Trunk enzyme label row ---
	trunk_enzyme_row = empty_row()
	for i in range(trunk_len - 1):
		en = i + 1
		col = first_trunk_col + 1 + 2 * i
		if col < total_cols:
			trunk_enzyme_row[col] = f"<td style='{css_lbl}'>E<sub>{en}</sub></td>"

	# --- Trunk structure row ---
	trunk_struct_row = empty_row()
	trunk_struct_row[0] = f"<td style='{css_dots}'>&middot;&middot;&middot;</td>"
	trunk_struct_row[1] = f"<td style='{css_arr}'>&rarr;</td>"
	for i in range(trunk_len):
		col = first_trunk_col + 2 * i
		if col < total_cols:
			trunk_struct_row[col] = f"<td style='{css_met}'>{_met_node(trunk[i][0], trunk[i][1])}</td>"
		if i < trunk_len - 1:
			arrow_col = col + 1
			if arrow_col < total_cols:
				trunk_struct_row[arrow_col] = f"<td style='{css_arr}'>&rarr;</td>"

	# --- Branch 2 enzyme label row ---
	b2_enzyme_row = empty_row()
	b2_enzyme_row[junction_col] = f"<td style='{css_lbl}'>E<sub>{e_b2_first}</sub></td>"
	for i in range(1, len(b2)):
		en = e_b2_first + i
		col = branch_start + 2 * i - 1
		if col < total_cols:
			b2_enzyme_row[col] = f"<td style='{css_lbl}'>E<sub>{en}</sub></td>"

	# --- Branch 2 structure row ---
	b2_struct_row = empty_row()
	b2_struct_row[junction_col] = f"<td style='{css_arr}'>&#8600;</td>"
	for i in range(len(b2)):
		col = branch_start + 2 * i
		if col < total_cols:
			b2_struct_row[col] = f"<td style='{css_met}'>{_met_node(b2[i][0], b2[i][1])}</td>"
		if i < len(b2) - 1:
			arrow_col = col + 1
			if arrow_col < total_cols:
				b2_struct_row[arrow_col] = f"<td style='{css_arr}'>&rarr;</td>"

	# assemble the table
	table = "<table border='0' style='border-collapse: collapse; border: 0;'>"
	for row in [b1_enzyme_row, b1_struct_row, trunk_enzyme_row, trunk_struct_row, b2_enzyme_row, b2_struct_row]:
		table += "<tr>" + "".join(row) + "</tr>"
	table += "</table>"

	return table

#============================================
#============================================
def _pathway_intro(pathway: dict) -> str:
	"""
	Build the common intro text with the pathway diagram.

	Args:
		pathway (dict): Pathway structure.

	Returns:
		str: HTML intro paragraph and diagram.
	"""
	diagram = _make_pathway_diagram(pathway)
	intro = ""
	intro += "<p>A series of enzymes catalyze reactions involving the "
	intro += "metabolites in the branched metabolic pathway shown below. "
	intro += "The ellipsis (...) indicates that additional upstream steps "
	intro += "are not shown.</p>"
	intro += diagram
	return intro

#============================================
#============================================
def _make_feedback_inhibitor_question(pathway: dict, focus_branch: int) -> tuple:
	"""
	MC question: which metabolite is most likely a feedback inhibitor.

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
	trunk_len = pathway['trunk_len']

	# correct answer is the end product of the focus branch
	if focus_branch == 1:
		correct_mol = b1_end
	else:
		correct_mol = b2_end
	answer_text = f"metabolite {_color_text(correct_mol[0], correct_mol[1])}"

	# build distractor set from other metabolites
	distractors = [trunk[0], b1[0], b2[0]]
	if trunk_len >= 3:
		distractors.append(trunk[1])
	# add the other branch end product as a plausible distractor
	if focus_branch == 1:
		distractors.append(b2[0])
	else:
		distractors.append(b1[0])

	# deduplicate distractors
	seen = {correct_mol[0]}
	unique_distractors = []
	for mol in distractors:
		if mol[0] not in seen:
			seen.add(mol[0])
			unique_distractors.append(mol)

	# build choices
	choices_list = [answer_text]
	for mol in unique_distractors[:4]:
		choices_list.append(f"metabolite {_color_text(mol[0], mol[1])}")
	random.shuffle(choices_list)

	# question text
	question_text = _pathway_intro(pathway)
	question_text += "<p>In negative feedback regulation, end products inhibit "
	question_text += "earlier enzymes in their own branch. "
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
		focus_branch (int): 1 for upper branch, 2 for lower.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	trunk_len = pathway['trunk_len']
	e_b1_first = pathway['e_b1_first']
	e_b2_first = pathway['e_b2_first']
	total_enzymes = trunk_len + pathway['b1_len'] + pathway['b2_len'] - 1

	# correct answer is the committed step of the focus branch
	if focus_branch == 1:
		correct_enzyme = e_b1_first
	else:
		correct_enzyme = e_b2_first
	answer_text = f"enzyme E<sub>{correct_enzyme}</sub>"

	# build distractor enzyme numbers
	distractor_nums = [1]
	if trunk_len >= 3:
		distractor_nums.append(2)
	# add downstream enzymes from both branches
	if e_b1_first + 1 <= total_enzymes:
		distractor_nums.append(e_b1_first + 1)
	if e_b2_first + 1 <= total_enzymes:
		distractor_nums.append(e_b2_first + 1)
	# add the other branch committed step as a plausible distractor
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
	if focus_branch == 1:
		end_txt = _color_text(pathway['b1_end'][0], pathway['b1_end'][1])
	else:
		end_txt = _color_text(pathway['b2_end'][0], pathway['b2_end'][1])

	# question text
	question_text = _pathway_intro(pathway)
	question_text += f"<p>The end product {end_txt} acts as a feedback inhibitor. "
	question_text += "<b>Which enzyme is the most likely target of this feedback "
	question_text += "inhibition?</b></p>"

	return question_text, choices_list, answer_text

#============================================
#============================================
def _make_accumulation_question(pathway: dict, focus_branch: int) -> tuple:
	"""
	MC question: what happens when an end product concentration is very high.

	Args:
		pathway (dict): Pathway structure.
		focus_branch (int): 1 for upper branch, 2 for lower branch.

	Returns:
		tuple: (question_text, choices_list, answer_text).
	"""
	bp_mol = pathway['bp_mol']
	b1 = pathway['b1']
	b2 = pathway['b2']
	b1_end = pathway['b1_end']
	b2_end = pathway['b2_end']

	if focus_branch == 1:
		focus_end = b1_end
		other_end = b2_end
		focus_first = b1[0]
	else:
		focus_end = b2_end
		other_end = b1_end
		focus_first = b2[0]

	bp_txt = _color_text(bp_mol[0], bp_mol[1])
	focus_end_txt = _color_text(focus_end[0], focus_end[1])
	other_end_txt = _color_text(other_end[0], other_end[1])
	focus_first_txt = _color_text(focus_first[0], focus_first[1])

	# question text
	question_text = _pathway_intro(pathway)
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
	"""
	MC question: what happens when feedback inhibition is eliminated by mutation.

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

	bp_txt = _color_text(bp_mol[0], bp_mol[1])
	focus_end_txt = _color_text(focus_end[0], focus_end[1])
	other_end_txt = _color_text(other_end[0], other_end[1])

	# question text
	question_text = _pathway_intro(pathway)
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
	"""
	MC question: what happens when a branch enzyme is completely inactivated.

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

	bp_txt = _color_text(bp_mol[0], bp_mol[1])
	other_end_txt = _color_text(other_end[0], other_end[1])

	# question text
	question_text = _pathway_intro(pathway)
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
# question type dispatch table
QUESTION_MAKERS = {
	'inhibitor': _make_feedback_inhibitor_question,
	'enzyme': _make_regulated_enzyme_question,
	'accumulation': _make_accumulation_question,
	'mutation': _make_mutation_question,
	'rerouting': _make_rerouting_question,
}

#============================================
#============================================
def _get_scenarios(question_types: list) -> list:
	"""
	Generate all scenario combinations: pathway parameters x question type x branch.

	Args:
		question_types (list): List of question type keys to include.

	Returns:
		list: Each entry is (trunk_len, b1_len, b2_len, color_shift, letter_shift,
		      question_type, focus_branch).
	"""
	scenarios = []
	for trunk_len in (3, 4):
		for b1_len in (3, 4):
			for b2_len in (3, 4):
				total_mols = trunk_len + b1_len + b2_len
				# color shifts (sample 5 from the palette)
				for c_shift in range(0, len(PALETTE), 3):
					# letter shifts (sample a few starting positions)
					for l_shift in range(0, 26 - total_mols, 4):
						for qtype in question_types:
							for focus_branch in (1, 2):
								scenarios.append((
									trunk_len, b1_len, b2_len,
									c_shift, l_shift, qtype, focus_branch
								))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted MC question about negative feedback in a branched pathway.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted MC question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	trunk_len, b1_len, b2_len, c_shift, l_shift, qtype, focus_branch = SCENARIOS[idx]

	# build the pathway
	pathway = _build_pathway(trunk_len, b1_len, b2_len, c_shift, l_shift)

	# generate the question using the dispatch table
	make_fn = QUESTION_MAKERS[qtype]
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
	'C': ['accumulation'],
	'D': ['mutation'],
	'E': ['rerouting'],
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
		description="Generate negative feedback pathway MC questions."
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
			"C=accumulation/depletion, D=mutation effects, "
			"E=branch rerouting. Default: all parts."
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
