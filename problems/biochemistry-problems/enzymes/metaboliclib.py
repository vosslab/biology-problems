#!/usr/bin/env python3

"""
Shared helpers for metabolic pathway question generators.
Provides color palettes, metabolite node rendering, letter/color assignment,
and linear pathway diagram generation.
"""

import sys

# Define the set of letters to be used and their associated colors
all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_colors = [
	'#d40000', #RED
	'#b74300', #DARK ORANGE
	'#935d00', #LIGHT ORANGE
	'#6c6c00', #DARK YELLOW
	'#3b7600', #LIME GREEN
	'#007a00', #GREEN
	'#00775f', #TEAL
	'#007576', #CYAN
	'#076dad', #SKY BLUE
	'#003fff', #BLUE
	'#0067cc', #NAVY
	'#a719db', #PURPLE
	'#c80085', #MAGENTA
	'#cc0066', #PINK
]

#======================================
#======================================
def get_letters(num_letters=6, shift=0):
	"""Fetch a list of HTML-formatted letters with a given color.

	Args:
		num_letters (int): The number of letters to get.
		shift (int): The index to start from for letter and color.

	Returns:
		html_letters (list): List of HTML formatted letters with color.
	"""

	# Determine the starting index for fetching letters and colors
	letter_index = shift % (len(all_letters) - num_letters)

	# Extract letters and colors based on the calculated index
	letters = list(all_letters[letter_index:letter_index+num_letters])
	local_colors = all_colors + all_colors  # Double the list to handle rollover
	color_index = shift % len(all_colors)
	colors = local_colors[color_index:color_index+num_letters]

	# Format letters as HTML with color
	html_letters = []
	for i, ltr in enumerate(letters):
		clr = colors[i]
		html_text = '<strong><span style="color: {0}">{1}</span></strong>'.format(clr, ltr)
		html_letters.append(html_text)

	return html_letters

#======================================
#======================================
def generate_metabolic_pathway(num_letters, shift=0):
	"""Generate an HTML table showing a metabolic pathway.

	Args:
		num_letters (int): Number of molecules (letters) in the pathway.
		shift (int): Index to start from for letter and color selection.

	Returns:
		metabolic_table (str): HTML-formatted table representing the metabolic pathway.
	"""

	# Validate the number of molecules
	if num_letters < 3:
		print('Not enough molecules provided for the pathway.')
		sys.exit(1)

	# Fetch HTML-formatted letters
	letters = get_letters(num_letters, shift)

	# Initialize the HTML table (avoid colspan-heavy layouts which render as extra columns in text previews)
	metabolic_table = "<table border='0' style='border-collapse: collapse;'>"

	# Row for enzyme labels (aligned above the arrows)
	metabolic_table += "<tr>"
	for i in range(len(letters) - 1):
		metabolic_table += "<td>&nbsp;</td>"
		metabolic_table += ("<td style='font-size: 75%; text-align:center; vertical-align: bottom;'>"
			f"enzyme {i+1}</td>")
	metabolic_table += "<td>&nbsp;</td></tr>"

	# Row for molecules and arrows
	metabolic_table += "<tr>"
	for i in range(len(letters) - 1):
		metabolic_table += f"<td style='font-size: 150%; text-align:center; padding: 0 6px;'>{letters[i]}</td>"
		metabolic_table += "<td style='text-align:center; padding: 0 6px;'>&xrarr;</td>"
	metabolic_table += f"<td style='font-size: 150%; text-align:center; padding: 0 6px;'>{letters[-1]}</td>"
	metabolic_table += "</tr></table>"

	return metabolic_table

#======================================
#======================================
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

#======================================
#======================================
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

#======================================
#======================================
def assign_metabolites(total: int, color_shift: int, letter_shift: int) -> list:
	"""Assign sequential letters and colors to metabolites.

	Args:
		total (int): Number of metabolites to assign.
		color_shift (int): Starting index in the color palette.
		letter_shift (int): Starting index in the alphabet.

	Returns:
		list: List of (letter, color) tuples.
	"""
	# pick colors with wraparound
	dbl_pal = all_colors + all_colors
	colors = dbl_pal[color_shift:color_shift + total]
	# pick letters
	letters = list(all_letters[letter_shift:letter_shift + total])
	# pair them up
	metabolites = [(letters[i], colors[i]) for i in range(total)]
	return metabolites

#======================================
#======================================
# ======================================
# CSS styles for branched pathway diagram table cells
# ======================================
CSS_MET = "border: 0; text-align: center; padding: 2px 4px;"
CSS_ARR = "border: 0; text-align: center; padding: 2px 2px; font-size: 150%;"
CSS_LBL = "border: 0; text-align: center; padding: 0 2px; font-size: 75%; vertical-align: bottom;"
CSS_EMPTY = "border: 0; padding: 2px 4px;"
CSS_DOTS = "border: 0; text-align: center; padding: 2px 2px; font-size: 120%; color: #888; letter-spacing: 2px;"

#======================================
#======================================
def make_empty_row(total_cols: int) -> list:
	"""Create a row of empty table cells.

	Args:
		total_cols (int): Number of columns in the row.

	Returns:
		list: List of empty <td> HTML strings.
	"""
	row = [f"<td style='{CSS_EMPTY}'></td>"] * total_cols
	return row

#======================================
#======================================
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

#======================================
#======================================
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

#======================================
#======================================
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

#======================================
#======================================
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
