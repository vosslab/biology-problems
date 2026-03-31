#!/usr/bin/env python3

"""
Shared helpers for metabolic pathway question generators.
Provides color palettes, metabolite node rendering, letter/color assignment,
and linear pathway diagram generation.
"""

import random

# PIP3 modules / local shared library
import qti_package_maker.common.color_wheel

# Define the set of letters to be used
ALL_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#============================================
#============================================
def _generate_colors(num_colors: int) -> list:
	"""Generate perceptually distinct colors, rotated by a random offset.

	Args:
		num_colors (int): Number of colors to generate.

	Returns:
		list: Hex color strings with '#' prefix.
	"""
	raw = qti_package_maker.common.color_wheel.generate_color_wheel(num_colors, mode="dark")
	colors = [f"#{c}" for c in raw]
	# rotate by a random offset for variety between questions
	offset = random.randint(0, num_colors - 1)
	colors = colors[offset:] + colors[:offset]
	return colors

#============================================
#============================================
def get_metabolite_data(num_letters: int, shift: int = 0) -> list:
	"""Generate (letter, color) tuples for a linear pathway.

	Args:
		num_letters (int): Number of metabolite letters.
		shift (int): Starting index in the alphabet.

	Returns:
		list: List of (letter, color) tuples.
	"""
	letter_index = shift % (len(ALL_LETTERS) - num_letters)
	letters = list(ALL_LETTERS[letter_index:letter_index + num_letters])
	colors = _generate_colors(num_letters)
	metabolites = list(zip(letters, colors))
	return metabolites

#============================================
#============================================
def generate_metabolic_pathway(metabolites: list) -> str:
	"""Generate an HTML table showing a linear metabolic pathway with circular nodes.

	Args:
		metabolites (list): List of (letter, color) tuples from get_metabolite_data().

	Returns:
		str: HTML-formatted table representing the metabolic pathway.
	"""
	if len(metabolites) < 3:
		raise ValueError('Not enough molecules provided for the pathway.')

	# enzyme label row
	enzyme_positions = []
	for i in range(len(metabolites) - 1):
		# arrows are at odd columns (1, 3, 5, ...), metabolites at even (0, 2, 4, ...)
		enzyme_positions.append((2 * i + 1, i + 1))
	total_cols = 2 * len(metabolites) - 1
	label_row = make_enzyme_label_row(total_cols, enzyme_positions)

	# metabolite + arrow row
	met_row = make_metabolite_row(total_cols, metabolites, 0)

	metabolic_table = assemble_pathway_table([label_row, met_row])
	return metabolic_table

#============================================
#============================================
def color_text(letter: str, color: str) -> str:
	"""Wrap a metabolite letter in colored bold HTML.

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
def met_node(letter: str, color: str) -> str:
	"""Create a circular metabolite node for pathway diagrams.

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
# CSS styles for branched pathway diagram table cells
CSS_MET = "border: 0; text-align: center; padding: 2px 4px;"
CSS_ARR = "border: 0; text-align: center; padding: 2px 2px; font-size: 150%;"
CSS_LBL = "border: 0; text-align: center; padding: 0 2px; font-size: 75%; vertical-align: bottom;"
CSS_EMPTY = "border: 0; padding: 2px 4px;"
CSS_DOTS = "border: 0; text-align: center; padding: 2px 2px; font-size: 120%; color: #888; letter-spacing: 2px;"

#============================================
#============================================
def make_empty_row(total_cols: int) -> list:
	"""Create a row of empty table cells.

	Args:
		total_cols (int): Number of columns in the row.

	Returns:
		list: List of empty <td> HTML strings.
	"""
	row = [f"<td style='{CSS_EMPTY}'></td>"] * total_cols
	return row

#============================================
#============================================
def make_enzyme_label_row(total_cols: int, enzyme_positions: list) -> list:
	"""Create a row with enzyme labels placed at specific columns.

	Args:
		total_cols (int): Number of columns in the row.
		enzyme_positions (list): List of (column_index, enzyme_number) tuples.

	Returns:
		list: Row of <td> HTML strings with enzyme labels placed.
	"""
	row = make_empty_row(total_cols)
	for col, en in enzyme_positions:
		if 0 <= col < total_cols:
			row[col] = f"<td style='{CSS_LBL}'>E<sub>{en}</sub></td>"
	return row

#============================================
#============================================
def make_metabolite_row(total_cols: int, metabolites: list, start_col: int) -> list:
	"""Create a row with metabolite nodes and arrows between them.

	Metabolites are placed at even offsets from start_col, arrows at odd offsets.

	Args:
		total_cols (int): Number of columns in the row.
		metabolites (list): List of (letter, color) tuples.
		start_col (int): Column index for the first metabolite.

	Returns:
		list: Row of <td> HTML strings with metabolite nodes and arrows.
	"""
	row = make_empty_row(total_cols)
	for i, (letter, color) in enumerate(metabolites):
		col = start_col + 2 * i
		if 0 <= col < total_cols:
			row[col] = f"<td style='{CSS_MET}'>{met_node(letter, color)}</td>"
		# arrow between metabolites
		if i < len(metabolites) - 1:
			arrow_col = col + 1
			if 0 <= arrow_col < total_cols:
				row[arrow_col] = f"<td style='{CSS_ARR}'>&rarr;</td>"
	return row

#============================================
#============================================
def assemble_pathway_table(rows: list) -> str:
	"""Wrap a list of table rows into a borderless HTML table.

	Args:
		rows (list): List of row lists, each containing <td> HTML strings.

	Returns:
		str: Complete HTML table string.
	"""
	table = "<table border='0' style='border-collapse: collapse; border: 0;'>"
	for row in rows:
		table += "<tr>" + "".join(row) + "</tr>"
	table += "</table>"
	return table

#============================================
#============================================
def pathway_intro_text(diagram: str) -> str:
	"""Build the common intro paragraph with a pathway diagram.

	Args:
		diagram (str): HTML table string for the pathway diagram.

	Returns:
		str: HTML intro paragraph followed by the diagram.
	"""
	intro = ""
	intro += "<p>A series of enzymes catalyze reactions involving the "
	intro += "metabolites in the branched metabolic pathway shown below. "
	intro += "The ellipsis (...) indicates that additional upstream steps "
	intro += "are not shown.</p>"
	intro += diagram
	return intro

#======================================
# Shorthand-based pathway pipeline
#======================================
def build_shorthand(topology: str, trunk_letters: list, b1_letters: list, b2_letters: list) -> str:
	"""Build a shorthand string from metabolite letter lists.

	Args:
		topology (str): 'split' or 'merge'.
		trunk_letters (list): Letters for the trunk strand.
		b1_letters (list): Letters for branch 1 (upper).
		b2_letters (list): Letters for branch 2 (lower).

	Returns:
		str: Shorthand string, e.g. 'ABCD<(EFG,HIJ)' or '(ABC,DEF)>GHIJ'.
	"""
	trunk_str = ''.join(trunk_letters)
	b1_str = ''.join(b1_letters)
	b2_str = ''.join(b2_letters)
	if topology == 'split':
		shorthand = f"{trunk_str}<({b1_str},{b2_str})"
	elif topology == 'merge':
		shorthand = f"({b1_str},{b2_str})>{trunk_str}"
	else:
		raise ValueError(f"Unknown topology: {topology!r}. Use 'split' or 'merge'.")
	return shorthand

#============================================
#============================================
def parse_shorthand(shorthand: str) -> dict:
	"""Parse a pathway shorthand string into a schema dict.

	Supported forms:
		merge: (ABCD,EFG)>HIJ
		split: ABCD<(EFG,HIJ)

	Args:
		shorthand (str): The shorthand string.

	Returns:
		dict: Schema with 'topology', 'left_strands', 'right_strands'.
	"""
	# normalize whitespace
	text = shorthand.replace(' ', '')

	# detect topology
	has_gt = '>' in text
	has_lt = '<' in text
	if has_gt and has_lt:
		raise ValueError(f"Shorthand has both '>' and '<': {shorthand!r}")
	if not has_gt and not has_lt:
		raise ValueError(f"Shorthand has no junction symbol ('>' or '<'): {shorthand!r}")

	if has_gt:
		topology = 'merge'
		left_raw, right_raw = text.split('>', 1)
	else:
		topology = 'split'
		left_raw, right_raw = text.split('<', 1)

	left_strands = _parse_side(left_raw)
	right_strands = _parse_side(right_raw)

	# validate: one-to-two or two-to-one only
	if len(left_strands) > 2 or len(right_strands) > 2:
		raise ValueError(f"Too many strands (max 2 per side): {shorthand!r}")
	if len(left_strands) == 1 and len(right_strands) == 1:
		raise ValueError(f"Both sides have one strand (no branching): {shorthand!r}")
	if len(left_strands) == 2 and len(right_strands) == 2:
		raise ValueError(f"Both sides have two strands (not supported): {shorthand!r}")
	# merge must have 2 left, 1 right
	if topology == 'merge' and not (len(left_strands) == 2 and len(right_strands) == 1):
		raise ValueError(f"Merge topology needs 2 left strands and 1 right: {shorthand!r}")
	# split must have 1 left, 2 right
	if topology == 'split' and not (len(left_strands) == 1 and len(right_strands) == 2):
		raise ValueError(f"Split topology needs 1 left strand and 2 right: {shorthand!r}")

	schema = {
		'topology': topology,
		'left_strands': left_strands,
		'right_strands': right_strands,
	}
	return schema

#============================================
#============================================
def _parse_side(raw: str) -> list:
	"""Parse one side of a shorthand into a list of letter lists.

	Args:
		raw (str): e.g. '(ABCD,EFG)' or 'HIJ'

	Returns:
		list: List of lists of single letters.
	"""
	raw = raw.strip()
	if not raw:
		raise ValueError("Empty side in shorthand")
	# check for nested parentheses
	if raw.count('(') > 1 or raw.count(')') > 1:
		raise ValueError(f"Nested parentheses not supported: {raw!r}")
	if raw.startswith('(') and raw.endswith(')'):
		# multiple strands: (ABC,DEF)
		inner = raw[1:-1]
		parts = inner.split(',')
		strands = [list(p) for p in parts]
	else:
		# single strand: ABCD
		if '(' in raw or ')' in raw:
			raise ValueError(f"Mismatched parentheses: {raw!r}")
		strands = [list(raw)]
	# validate only uppercase letters
	for strand in strands:
		for ch in strand:
			if not ch.isupper():
				raise ValueError(f"Invalid character in shorthand: {ch!r}")
		if len(strand) == 0:
			raise ValueError("Empty strand in shorthand")
	return strands

#============================================
#============================================
def build_display_model(schema: dict) -> dict:
	"""Build a display model from a parsed schema: add colors and enzyme IDs.

	Assigns colors from the palette in metabolite traversal order.
	Assigns enzyme IDs in pathway traversal order appropriate for the topology.

	For split: trunk enzymes first (E1..E(n-1)), then b1 committed step, then b1 internal,
	then b2 committed step, then b2 internal.
	For merge: b1 enzymes first, then merge enzyme, then trunk enzymes, then b2 enzymes.

	Args:
		schema (dict): Parsed schema from parse_shorthand().

	Returns:
		dict: Display model with colored metabolites, enzyme edges, and junction info.
	"""
	topology = schema['topology']
	left_strands = schema['left_strands']
	right_strands = schema['right_strands']

	# collect all metabolite letters in order for color assignment
	traversal_order = []
	if topology == 'split':
		# trunk, then b1, then b2
		trunk_letters = left_strands[0]
		b1_letters = right_strands[0]
		b2_letters = right_strands[1]
	else:
		# merge: b1, then b2, then trunk
		b1_letters = left_strands[0]
		b2_letters = left_strands[1]
		trunk_letters = right_strands[0]
	traversal_order = trunk_letters + b1_letters + b2_letters

	# generate exactly the colors needed, rotated by a random offset
	colors = _generate_colors(len(traversal_order))

	# assign colors to each metabolite letter in traversal order
	color_map = {}
	for i, letter in enumerate(traversal_order):
		color_map[letter] = (letter, colors[i])

	# color each strand
	colored_trunk = [color_map[ch] for ch in trunk_letters]
	colored_b1 = [color_map[ch] for ch in b1_letters]
	colored_b2 = [color_map[ch] for ch in b2_letters]

	# assign enzyme IDs and build edge list
	enzymes = []
	enzyme_id = 1

	if topology == 'split':
		# trunk enzymes: E1 through E(trunk_len-1)
		for i in range(len(trunk_letters) - 1):
			enzymes.append({
				'id': enzyme_id, 'from': trunk_letters[i],
				'to': trunk_letters[i + 1], 'strand': 'trunk',
			})
			enzyme_id += 1
		# committed step of b1
		e_b1_first = enzyme_id
		enzymes.append({
			'id': enzyme_id, 'from': trunk_letters[-1],
			'to': b1_letters[0], 'strand': 'b1',
		})
		enzyme_id += 1
		# b1 internal enzymes
		for i in range(len(b1_letters) - 1):
			enzymes.append({
				'id': enzyme_id, 'from': b1_letters[i],
				'to': b1_letters[i + 1], 'strand': 'b1',
			})
			enzyme_id += 1
		# committed step of b2
		e_b2_first = enzyme_id
		enzymes.append({
			'id': enzyme_id, 'from': trunk_letters[-1],
			'to': b2_letters[0], 'strand': 'b2',
		})
		enzyme_id += 1
		# b2 internal enzymes
		for i in range(len(b2_letters) - 1):
			enzymes.append({
				'id': enzyme_id, 'from': b2_letters[i],
				'to': b2_letters[i + 1], 'strand': 'b2',
			})
			enzyme_id += 1

		junction_mol = color_map[trunk_letters[-1]]
		end_products = {'b1': color_map[b1_letters[-1]], 'b2': color_map[b2_letters[-1]]}
		committed_step_enzymes = {'b1': e_b1_first, 'b2': e_b2_first}

	else:
		# merge: b1 enzymes, merge enzyme, trunk enzymes, b2 enzymes
		# b1 internal
		e_b1_first = enzyme_id
		for i in range(len(b1_letters) - 1):
			enzymes.append({
				'id': enzyme_id, 'from': b1_letters[i],
				'to': b1_letters[i + 1], 'strand': 'b1',
			})
			enzyme_id += 1
		# merge enzyme: last b1 -> first trunk
		e_merge = enzyme_id
		enzymes.append({
			'id': enzyme_id, 'from': b1_letters[-1],
			'to': trunk_letters[0], 'strand': 'junction',
		})
		enzyme_id += 1
		# trunk internal
		e_trunk_first = enzyme_id
		for i in range(len(trunk_letters) - 1):
			enzymes.append({
				'id': enzyme_id, 'from': trunk_letters[i],
				'to': trunk_letters[i + 1], 'strand': 'trunk',
			})
			enzyme_id += 1
		# b2 enzymes
		e_b2_first = enzyme_id
		for i in range(len(b2_letters) - 1):
			enzymes.append({
				'id': enzyme_id, 'from': b2_letters[i],
				'to': b2_letters[i + 1], 'strand': 'b2',
			})
			enzyme_id += 1

		junction_mol = color_map[trunk_letters[0]]
		end_products = {
			'b1': color_map[b1_letters[-1]],
			'b2': color_map[b2_letters[-1]],
			'trunk': color_map[trunk_letters[-1]],
		}
		committed_step_enzymes = {'b1': e_b1_first, 'b2': e_b2_first}

	display = {
		'topology': topology,
		'trunk': colored_trunk,
		'b1': colored_b1,
		'b2': colored_b2,
		'enzymes': enzymes,
		'junction_mol': junction_mol,
		'end_products': end_products,
		'committed_step_enzymes': committed_step_enzymes,
	}
	# add merge-specific keys
	if topology == 'merge':
		display['e_merge'] = e_merge
		display['e_trunk_first'] = e_trunk_first

	return display

#============================================
#============================================
def build_layout_plan(display: dict) -> list:
	"""Convert a display model into a flat row/column layout plan.

	Uses fixed templates:
	- split: ellipsis+trunk on middle row, b1 above, b2 below, junction between
	- merge: b1 above, b2 below on left, junction, trunk on right with trailing ellipsis

	Args:
		display (dict): Display model from build_display_model().

	Returns:
		list: List of rows. Each row is a list of cell dicts.
	"""
	topology = display['topology']
	trunk = display['trunk']
	b1 = display['b1']
	b2 = display['b2']

	if topology == 'split':
		return _build_split_layout(display, trunk, b1, b2)
	else:
		return _build_merge_layout(display, trunk, b1, b2)

#============================================
#============================================
def _build_split_layout(display: dict, trunk: list, b1: list, b2: list) -> list:
	"""Build layout plan for a splitting pathway: trunk -> junction -> branches.

	Layout structure (6 rows):
		Row 0: b1 enzyme labels (above branch 1)
		Row 1: junction arrow NE + b1 metabolites
		Row 2: trunk enzyme labels
		Row 3: ellipsis + trunk metabolites
		Row 4: junction arrow SE + b2 metabolites
		Row 5: b2 enzyme labels (below branch 2)
	"""
	trunk_len = len(trunk)
	# grid geometry: 2 cols for ellipsis+arrow, then trunk, then junction, then branches
	first_trunk_col = 2
	last_trunk_col = first_trunk_col + 2 * (trunk_len - 1)
	junction_col = last_trunk_col + 1
	branch_start = junction_col + 1
	max_branch = max(len(b1), len(b2))
	total_cols = branch_start + 2 * max_branch - 1

	# get enzyme IDs from display model
	e_b1_first = display['committed_step_enzymes']['b1']
	e_b2_first = display['committed_step_enzymes']['b2']

	rows = []

	# Row 0: b1 enzyme labels
	b1_enzyme_positions = [(junction_col, e_b1_first)]
	for i in range(1, len(b1)):
		col = branch_start + 2 * i - 1
		if col < total_cols:
			b1_enzyme_positions.append((col, e_b1_first + i))
	rows.append(_make_cell_row_enzyme_labels(total_cols, b1_enzyme_positions))

	# Row 1: b1 metabolites with NE junction arrow
	row1 = _make_cell_row_metabolites(total_cols, b1, branch_start)
	row1[junction_col] = {'type': 'junction_arrow', 'direction': 'NE'}
	rows.append(row1)

	# Row 2: trunk enzyme labels
	trunk_enzyme_positions = []
	for i in range(trunk_len - 1):
		col = first_trunk_col + 1 + 2 * i
		if col < total_cols:
			trunk_enzyme_positions.append((col, i + 1))
	rows.append(_make_cell_row_enzyme_labels(total_cols, trunk_enzyme_positions))

	# Row 3: trunk metabolites with leading ellipsis
	row3 = _make_cell_row_metabolites(total_cols, trunk, first_trunk_col)
	row3[0] = {'type': 'ellipsis'}
	row3[1] = {'type': 'arrow', 'direction': 'right'}
	rows.append(row3)

	# Row 4: b2 enzyme labels
	b2_enzyme_positions = [(junction_col, e_b2_first)]
	for i in range(1, len(b2)):
		col = branch_start + 2 * i - 1
		if col < total_cols:
			b2_enzyme_positions.append((col, e_b2_first + i))
	rows.append(_make_cell_row_enzyme_labels(total_cols, b2_enzyme_positions))

	# Row 5: b2 metabolites with SE junction arrow
	row5 = _make_cell_row_metabolites(total_cols, b2, branch_start)
	row5[junction_col] = {'type': 'junction_arrow', 'direction': 'SE'}
	rows.append(row5)

	return rows

#============================================
#============================================
def _build_merge_layout(display: dict, trunk: list, b1: list, b2: list) -> list:
	"""Build layout plan for a merging pathway: branches -> junction -> trunk.

	Layout structure (6 rows):
		Row 0: b1 enzyme labels
		Row 1: b1 metabolites + SE junction arrow
		Row 2: trunk enzyme labels + merge enzyme label at junction
		Row 3: merge arrow + trunk metabolites + trailing ellipsis
		Row 4: b2 metabolites + NE junction arrow
		Row 5: b2 enzyme labels
	"""
	max_branch = max(len(b1), len(b2))
	# right-align each branch so its last metabolite is adjacent to the junction
	b1_start = 2 * (max_branch - len(b1))
	b2_start = 2 * (max_branch - len(b2))
	branch_cols = 2 * max_branch - 1
	junction_col = branch_cols
	# junction_col = merge arrow-tail, junction_col+1 = regular arrow, then trunk
	trunk_start = junction_col + 2
	trunk_cols = 2 * len(trunk) - 1
	total_cols = trunk_start + trunk_cols + 1  # +1 for trailing ellipsis

	e_b1_first = display['committed_step_enzymes']['b1']
	e_b2_first = display['committed_step_enzymes']['b2']
	e_merge = display['e_merge']
	e_trunk_first = display['e_trunk_first']

	rows = []

	# Row 0: b1 enzyme labels
	b1_enzyme_positions = []
	for i in range(len(b1) - 1):
		col = b1_start + 2 * i + 1
		if col < total_cols:
			b1_enzyme_positions.append((col, e_b1_first + i))
	rows.append(_make_cell_row_enzyme_labels(total_cols, b1_enzyme_positions))

	# Row 1: b1 metabolites + SE junction arrow
	row1 = _make_cell_row_metabolites(total_cols, b1, b1_start)
	row1[junction_col] = {'type': 'junction_arrow', 'direction': 'SE'}
	rows.append(row1)

	# Row 2: trunk enzyme labels + merge enzyme at junction
	trunk_enzyme_positions = [(junction_col, e_merge)]
	for i in range(len(trunk) - 1):
		col = trunk_start + 1 + 2 * i
		if col < total_cols:
			trunk_enzyme_positions.append((col, e_trunk_first + i))
	rows.append(_make_cell_row_enzyme_labels(total_cols, trunk_enzyme_positions))

	# Row 3: merge arrow + trunk metabolites + trailing ellipsis
	row3 = _make_cell_row_metabolites(total_cols, trunk, trunk_start)
	row3[junction_col] = {'type': 'merge_arrow'}
	row3[junction_col + 1] = {'type': 'arrow', 'direction': 'right'}
	# trailing ellipsis in last column
	if trunk_cols + trunk_start + 2 <= total_cols:
		row3[-1] = {'type': 'ellipsis'}
	rows.append(row3)

	# Row 4: b2 metabolites + NE junction arrow
	row4 = _make_cell_row_metabolites(total_cols, b2, b2_start)
	row4[junction_col] = {'type': 'junction_arrow', 'direction': 'NE'}
	rows.append(row4)

	# Row 5: b2 enzyme labels
	b2_enzyme_positions = []
	for i in range(len(b2) - 1):
		col = b2_start + 2 * i + 1
		if col < total_cols:
			b2_enzyme_positions.append((col, e_b2_first + i))
	rows.append(_make_cell_row_enzyme_labels(total_cols, b2_enzyme_positions))

	return rows

#============================================
#============================================
def _make_cell_row_metabolites(total_cols: int, metabolites: list, start_col: int) -> list:
	"""Build a row of cell dicts for metabolites with arrows between them.

	Args:
		total_cols (int): Total number of columns.
		metabolites (list): List of (letter, color) tuples.
		start_col (int): Starting column for the first metabolite.

	Returns:
		list: Row of cell dicts.
	"""
	row = [{'type': 'empty'} for _ in range(total_cols)]
	for i, (letter, color) in enumerate(metabolites):
		col = start_col + 2 * i
		if 0 <= col < total_cols:
			row[col] = {'type': 'metabolite', 'letter': letter, 'color': color}
		if i < len(metabolites) - 1:
			arrow_col = col + 1
			if 0 <= arrow_col < total_cols:
				row[arrow_col] = {'type': 'arrow', 'direction': 'right'}
	return row

#============================================
#============================================
def _make_cell_row_enzyme_labels(total_cols: int, positions: list) -> list:
	"""Build a row of cell dicts for enzyme labels.

	Args:
		total_cols (int): Total number of columns.
		positions (list): List of (column_index, enzyme_id) tuples.

	Returns:
		list: Row of cell dicts.
	"""
	row = [{'type': 'empty'} for _ in range(total_cols)]
	for col, eid in positions:
		if 0 <= col < total_cols:
			row[col] = {'type': 'enzyme_label', 'id': eid}
	return row

#============================================
#============================================
# cell type -> HTML rendering
_JUNCTION_ARROWS = {
	'NE': '&#8599;',  # north-east arrow
	'SE': '&#8600;',  # south-east arrow
}

#============================================
#============================================
def render_pathway_table(layout_plan: list) -> str:
	"""Render a layout plan into an HTML table.

	Each cell dict has a 'type' key. Supported types:
		metabolite: {letter, color} -> circular node
		arrow: {direction} -> right arrow
		junction_arrow: {direction} -> NE or SE diagonal arrow
		merge_arrow: {} -> merge arrow symbol
		enzyme_label: {id} -> subscript label
		ellipsis: {} -> continuation dots
		empty: {} -> blank cell

	Args:
		layout_plan (list): List of rows from build_layout_plan().

	Returns:
		str: Complete HTML table string.
	"""
	html_rows = []
	for row in layout_plan:
		cells = []
		for cell in row:
			cells.append(_render_cell(cell))
		html_rows.append(cells)
	return assemble_pathway_table(html_rows)

#============================================
#============================================
def _render_cell(cell: dict) -> str:
	"""Render a single cell dict to an HTML <td> string.

	Args:
		cell (dict): Cell descriptor with 'type' and type-specific keys.

	Returns:
		str: HTML <td> string.
	"""
	cell_type = cell['type']
	if cell_type == 'metabolite':
		return f"<td style='{CSS_MET}'>{met_node(cell['letter'], cell['color'])}</td>"
	elif cell_type == 'arrow':
		return f"<td style='{CSS_ARR}'>&rarr;</td>"
	elif cell_type == 'junction_arrow':
		arrow_html = _JUNCTION_ARROWS[cell['direction']]
		return f"<td style='{CSS_ARR}'>{arrow_html}</td>"
	elif cell_type == 'merge_arrow':
		return f"<td style='{CSS_ARR}'>&#x291A;</td>"
	elif cell_type == 'enzyme_label':
		return f"<td style='{CSS_LBL}'>E<sub>{cell['id']}</sub></td>"
	elif cell_type == 'ellipsis':
		return f"<td style='{CSS_DOTS}'>&middot;&middot;&middot;</td>"
	elif cell_type == 'empty':
		return f"<td style='{CSS_EMPTY}'></td>"
	else:
		raise ValueError(f"Unknown cell type: {cell_type!r}")

#============================================
#============================================
def build_metabolite_choices(answer_text: str, correct_mol: tuple,
		distractors: list, max_distractors: int = 4) -> list:
	"""Build a shuffled MC choices list from metabolite distractors.

	Deduplicates by letter, formats as colored text, and shuffles.

	Args:
		answer_text (str): The pre-formatted correct answer string.
		correct_mol (tuple): (letter, color) of the correct metabolite.
		distractors (list): List of (letter, color) tuples for distractors.
		max_distractors (int): Maximum number of distractors to include.

	Returns:
		list: Shuffled list of choice strings.
	"""
	seen = {correct_mol[0]}
	unique = []
	for mol in distractors:
		if mol[0] not in seen:
			seen.add(mol[0])
			unique.append(mol)
	choices = [answer_text]
	for mol in unique[:max_distractors]:
		choices.append(f"metabolite {color_text(mol[0], mol[1])}")
	random.shuffle(choices)
	return choices

#============================================
#============================================
def build_enzyme_choices(answer_text: str, correct_enzyme: int,
		all_enzyme_ids: list, max_distractors: int = 4) -> list:
	"""Build a shuffled MC choices list from enzyme ID distractors.

	Deduplicates by ID, formats as subscript labels, and shuffles.

	Args:
		answer_text (str): The pre-formatted correct answer string.
		correct_enzyme (int): The correct enzyme ID.
		all_enzyme_ids (list): List of all enzyme IDs to draw distractors from.
		max_distractors (int): Maximum number of distractors to include.

	Returns:
		list: Shuffled list of choice strings.
	"""
	seen = {correct_enzyme}
	unique = []
	for eid in all_enzyme_ids:
		if eid not in seen:
			seen.add(eid)
			unique.append(eid)
	choices = [answer_text]
	for eid in unique[:max_distractors]:
		choices.append(f"enzyme E<sub>{eid}</sub>")
	random.shuffle(choices)
	return choices
