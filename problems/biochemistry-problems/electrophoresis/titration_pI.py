#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
import bptools
import table_image_raster_lib

#===========================================================
#===========================================================
# Color badge helper: wraps text in a colored span for charge display
def badge(txt: str, sign: str) -> str:
	"""
	Wrap text in a colored HTML span based on charge sign.

	Args:
		txt: HTML fragment to colorize.
		sign: '+' for green (positive), '-' for red (negative), else neutral.

	Returns:
		str: Colored HTML span string.
	"""
	if sign == '+':
		colored_text = f"<span style='color:#1f7a1f;font-weight:800;'>{txt}</span>"
	elif sign == '-':
		colored_text = f"<span style='color:#b00020;font-weight:800;'>{txt}</span>"
	else:
		colored_text = f"<span style='color:#333;font-weight:700;'>{txt}</span>"
	return colored_text

#===========================================================
#===========================================================
# Build a single 2x2 molecule tile with a label and four corner groups
def mol_tile_2x2(label: str, TL: str, TR: str, BL: str, BR: str) -> str:
	"""
	Render a single molecule protonation-state tile as an HTML div with
	four corner positions for functional groups.

	Args:
		label: Tile heading (e.g. "State 1").
		TL: Top-left group HTML.
		TR: Top-right group HTML.
		BL: Bottom-left group HTML.
		BR: Bottom-right group HTML.

	Returns:
		str: HTML string for the tile.
	"""
	tile_html = ""
	tile_html += "<div style='border:1px solid #ccc;border-radius:10px;"
	tile_html += "padding:8px 10px;min-width:160px;background:#fff;'>"
	# Tile label centered at top
	tile_html += "<div style='text-align:center;font-size:13px;"
	tile_html += f"font-weight:700;margin-bottom:6px;'>{label}</div>"
	# 2x2 grid for functional groups using absolute positioning
	tile_html += "<div style='position:relative;height:72px;'>"
	tile_html += f"<div style='position:absolute;left:0;top:0;font-size:14px;'>{TL}</div>"
	tile_html += "<div style='position:absolute;right:0;top:0;"
	tile_html += f"font-size:14px;text-align:right;'>{TR}</div>"
	tile_html += f"<div style='position:absolute;left:0;bottom:0;font-size:14px;'>{BL}</div>"
	tile_html += "<div style='position:absolute;right:0;bottom:0;"
	tile_html += f"font-size:14px;text-align:right;'>{BR}</div>"
	tile_html += "</div></div>"
	return tile_html

#===========================================================
#===========================================================
# Generate randomized pKa values for a random amino acid family
def generate_pka_values() -> tuple:
	"""
	Pick acidic or basic family and generate three pKa values with
	minimum 1.0 pH-unit gaps between them.

	Returns:
		tuple: (family, pKa1, pKaR, pKa2, net_charges)
			family: 0 for acidic, 1 for basic
			pKa1: N-terminus pKa (1.8-2.5)
			pKaR: R-group pKa
			pKa2: C-terminus pKa (9.0-10.5)
			net_charges: list of 4 net charges for states 1-4
	"""
	# 50/50 acidic vs basic family
	family = random.randint(0, 1)

	# N-terminus pKa (amino group)
	pKa1 = random.randint(18, 25) / 10.0
	# C-terminus pKa (carboxyl group)
	pKa2 = random.randint(90, 105) / 10.0

	if family == 0:
		# Acidic side chain (like Asp, Glu): charges go +1 -> 0 -> -1 -> -2
		pKaR = random.randint(35, 50) / 10.0
		net_charges = [+1, 0, -1, -2]
	else:
		# Basic side chain (like Lys, His): charges go +2 -> +1 -> 0 -> -1
		pKaR = random.randint(55, 80) / 10.0
		net_charges = [+2, +1, 0, -1]

	# Enforce minimum 1.0 pH-unit gap between successive pKa values
	if pKaR < pKa1 + 1.0:
		pKaR = pKa1 + 1.0
	if pKa2 < pKaR + 1.0:
		pKa2 = pKaR + 1.0

	return (family, pKa1, pKaR, pKa2, net_charges)

#===========================================================
#===========================================================
# Build 4 protonation state tiles with randomized corner positions
def make_protonation_states(family: int) -> list:
	"""
	Build four HTML state tiles showing functional group charges,
	with randomized corner assignment to prevent memorization.

	Args:
		family: 0 for acidic side chain, 1 for basic side chain.

	Returns:
		list: 4 HTML tile strings.
	"""
	# Corner rotation: randomize which group goes where
	corners = ["TL", "TR", "BL", "BR"]
	groups = ["N", "C", "R", "M"]
	rot = random.randint(0, 3)
	# Rotate the group list so each run gets a different layout
	groups_rot = groups[rot:] + groups[:rot]
	# Map each group to its assigned corner
	corner_map = {}
	for i in range(4):
		corner_map[groups_rot[i]] = corners[i]

	# Define functional group HTML for each state per family
	# Protonated amino group (shared across most states)
	nh3_plus = badge("H<sub>3</sub>N<sup>+</sup>", '+')
	# Deprotonated carboxyl (shared across most states)
	coo_minus = badge("COO<sup>&minus;</sup>", '-')
	# Methyl placeholder (always neutral)
	ch3 = "CH<sub>3</sub>"

	if family == 0:
		# Acidic: +1 -> 0 -> -1 -> -2
		states = [
			{"N": nh3_plus, "C": "COOH", "R": "COOH", "M": ch3},
			{"N": nh3_plus, "C": coo_minus, "R": "COOH", "M": ch3},
			{"N": nh3_plus, "C": coo_minus, "R": coo_minus, "M": ch3},
			{"N": "H<sub>2</sub>N", "C": coo_minus, "R": coo_minus, "M": ch3},
		]
	else:
		# Basic: +2 -> +1 -> 0 -> -1
		nh3r_plus = badge("NH<sub>3</sub><sup>+</sup>", '+')
		states = [
			{"N": nh3_plus, "C": "COOH", "R": nh3r_plus, "M": ch3},
			{"N": nh3_plus, "C": coo_minus, "R": nh3r_plus, "M": ch3},
			{"N": nh3_plus, "C": coo_minus, "R": "NH<sub>2</sub>", "M": ch3},
			{"N": "H<sub>2</sub>N", "C": coo_minus, "R": "NH<sub>2</sub>", "M": ch3},
		]

	# Build tile HTML for each state using the rotated corner positions
	tiles_html = []
	for idx, state in enumerate(states):
		corner_contents = {"TL": "", "TR": "", "BL": "", "BR": ""}
		for group_name in ("N", "C", "R", "M"):
			corner_pos = corner_map[group_name]
			corner_contents[corner_pos] = state[group_name]
		tile = mol_tile_2x2(
			f"State {idx + 1}",
			corner_contents["TL"], corner_contents["TR"],
			corner_contents["BL"], corner_contents["BR"],
		)
		tiles_html.append(tile)
	return tiles_html

#===========================================================
#===========================================================
# Build the 4-tile layout as an HTML table (2 per row with arrows)
def build_tile_layout(tiles_html: list) -> str:
	"""
	Arrange four state tiles in a 2x2 grid with arrows between them.

	Args:
		tiles_html: list of 4 HTML tile strings.

	Returns:
		str: HTML table showing the titration progression.
	"""
	arrow = "<div style='text-align:center;font-size:20px;'>&rarr;</div>"
	layout = ""
	layout += "<table style='margin:0 auto;border-collapse:collapse;'>"
	# Row 1: State 1 -> State 2
	layout += "<tr>"
	layout += f"<td style='padding:4px;'>{tiles_html[0]}</td>"
	layout += f"<td style='padding:4px;'>{arrow}</td>"
	layout += f"<td style='padding:4px;'>{tiles_html[1]}</td>"
	layout += "</tr>"
	# Row 2: State 3 -> State 4
	layout += "<tr>"
	layout += f"<td style='padding:4px;'>{tiles_html[2]}</td>"
	layout += f"<td style='padding:4px;'>{arrow}</td>"
	layout += f"<td style='padding:4px;'>{tiles_html[3]}</td>"
	layout += "</tr>"
	layout += "</table>"
	return layout

#===========================================================
#===========================================================
# Render a titration curve as an HTML table of colored cells
def build_titration_curve_html(pKa1: float, pKaR: float, pKa2: float) -> str:
	"""
	Build an HTML table that renders a titration curve using colored cells.

	Uses TableImageRaster at doubled resolution (61x51 grid, 6px cells)
	for a smooth curve. The curve plots pH (y-axis) vs equivalents of
	OH- added (x-axis) using the three-proton speciation formula.

	Args:
		pKa1: first pKa (N-terminus).
		pKaR: second pKa (R-group, in sorted order).
		pKa2: third pKa (C-terminus).

	Returns:
		str: HTML table string for the titration curve chart.
	"""
	# Create raster chart: 121x101 grid at 3px cells (4x resolution)
	chart = table_image_raster_lib.TableImageRaster(
		x_range=(0.0, 3.0),
		y_range=(0.0, 12.5),
		cols=121, rows=101, cell_px=3
	)
	chart.set_y_tick_interval(2)
	chart.set_x_tick_values([0, 1, 2, 3])
	chart.set_x_axis_title("OH<sup>&minus;</sup> (equivalents)")

	# Compute dissociation constants from pKa values
	Ka1 = 10 ** (-pKa1)
	Ka2 = 10 ** (-pKaR)
	Ka3 = 10 ** (-pKa2)

	# Sweep pH and compute curve points via speciation formula
	# n-bar = average number of protons lost (0 to 3)
	points = []
	num_sweep = 2400
	for i in range(num_sweep + 1):
		ph = 0.5 + (12.0 * i / num_sweep)
		H = 10 ** (-ph)
		denom = (H ** 3
			+ Ka1 * H ** 2
			+ Ka1 * Ka2 * H
			+ Ka1 * Ka2 * Ka3)
		nbar = (Ka1 * H ** 2
			+ 2 * Ka1 * Ka2 * H
			+ 3 * Ka1 * Ka2 * Ka3) / denom
		points.append((nbar, ph))
	chart.plot_curve(points, antialiased=True)

	# Dashed crosshair guide lines and labels at each pKa
	pKa_vals = [pKa1, pKaR, pKa2]
	half_eqs = [0.5, 1.5, 2.5]
	pka_names = ['pK<sub>a1</sub>', 'pK<sub>aR</sub>', 'pK<sub>a2</sub>']
	for pka, half_eq, name in zip(pKa_vals, half_eqs, pka_names):
		chart.add_crosshair(half_eq, pka)
		chart.add_dot(half_eq, pka)
		chart.add_right_label(pka, name)

	result_html = chart.to_html()
	return result_html

#===========================================================
#===========================================================
# Find which state index has net charge = 0
def find_neutral_index(net_charges: list) -> int:
	"""
	Find the index of the neutral (net charge 0) protonation state.

	Args:
		net_charges: list of 4 net charge values.

	Returns:
		int: Index (0-3) of the neutral state.
	"""
	for idx, charge in enumerate(net_charges):
		if charge == 0:
			return idx
	return 0

#===========================================================
#===========================================================
# Calculate pI and generate distractor values
def calculate_pI_and_distractors(
	pKa1: float, pKaR: float, pKa2: float, neutral_index: int
) -> tuple:
	"""
	Calculate the correct pI and three distractors.

	The pI is the average of the two pKa values that bracket the
	neutral protonation state. Distractors use wrong pKa pairs
	and the middle pKa alone.

	Args:
		pKa1: N-terminus pKa.
		pKaR: R-group pKa.
		pKa2: C-terminus pKa.
		neutral_index: index of the neutral state (0-3).

	Returns:
		tuple: (correct_pI, distractor_values)
	"""
	# Transitions: state 0->1 at pKa1, 1->2 at pKaR, 2->3 at pKa2
	pKa_list = [pKa1, pKaR, pKa2]
	# Bracket pKa values flanking the neutral state
	pKa_lo = pKa_list[neutral_index - 1]
	pKa_hi = pKa_list[neutral_index]
	correct_pI = 0.5 * (pKa_lo + pKa_hi)

	# All four candidate pI values (one is correct, three are distractors)
	avg_1R = 0.5 * (pKa1 + pKaR)
	avg_R2 = 0.5 * (pKaR + pKa2)
	avg_12 = 0.5 * (pKa1 + pKa2)
	mid_pKaR = pKaR

	# Filter to get exactly 3 distractors
	correct_rounded = round(correct_pI, 1)
	all_candidates = [avg_1R, avg_R2, mid_pKaR, avg_12]
	distractors = [v for v in all_candidates
		if round(v, 1) != correct_rounded]
	distractors = distractors[:3]
	return (correct_pI, distractors)

#===========================================================
#===========================================================
# Build the complete question text for the pI calculation
def get_question_text(
	tile_layout_html: str, curve_html: str,
	pKa1: float, pKaR: float, pKa2: float
) -> str:
	"""
	Build the question asking students to calculate the isoelectric point.

	Args:
		tile_layout_html: HTML of the protonation state tiles.
		curve_html: HTML of the titration curve chart.
		pKa1: N-terminus pKa value.
		pKaR: R-group pKa value.
		pKa2: C-terminus pKa value.

	Returns:
		str: Complete question text in HTML.
	"""
	question_text = ""
	question_text += "<h6>Isoelectric Point from Titration Curve</h6> "
	question_text += "<p>Below are four protonation states of a hypothetical "
	question_text += "amino acid, shown in order as the solution is titrated "
	question_text += "from low pH to high pH.</p> "
	question_text += tile_layout_html
	question_text += " "
	question_text += curve_html
	question_text += " <p>Given pK<sub>a</sub> values: "
	question_text += f"pK<sub>a1</sub>&nbsp;=&nbsp;{pKa1:.1f}, "
	question_text += f"pK<sub>aR</sub>&nbsp;=&nbsp;{pKaR:.1f}, "
	question_text += f"pK<sub>a2</sub>&nbsp;=&nbsp;{pKa2:.1f}.</p> "
	question_text += "<p>The isoelectric point (pI) is closest "
	question_text += "to which value?</p>"
	return question_text

#===========================================================
#===========================================================
# Generate choices for the pI calculation question
def generate_pI_choices(correct_pI: float, distractors: list) -> tuple:
	"""
	Build MC choices for the pI question.

	Args:
		correct_pI: the correct isoelectric point value.
		distractors: list of 3 incorrect pI values.

	Returns:
		tuple: (choices_list, answer_text)
	"""
	answer_text = f"pI = {correct_pI:.1f}"
	choices_list = [answer_text]
	for d in distractors:
		choices_list.append(f"pI = {d:.1f}")
	random.shuffle(choices_list)
	return (choices_list, answer_text)

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	"""
	Generate one pI calculation question with tiles and titration curve.

	Args:
		N: question number for formatting.
		args: parsed command-line arguments.

	Returns:
		str: formatted BBQ question string.
	"""
	# Generate random pKa values and family
	family, pKa1, pKaR, pKa2, net_charges = generate_pka_values()

	# Build the protonation state tiles with rotated corners
	tiles_html = make_protonation_states(family)
	tile_layout_html = build_tile_layout(tiles_html)

	# Build the HTML table-based titration curve
	curve_html = build_titration_curve_html(pKa1, pKaR, pKa2)

	# Find the neutral state to determine pI bracket
	neutral_index = find_neutral_index(net_charges)
	correct_pI, distractors = calculate_pI_and_distractors(
		pKa1, pKaR, pKa2, neutral_index
	)

	# Assemble question text and choices
	question_text = get_question_text(
		tile_layout_html, curve_html, pKa1, pKaR, pKa2
	)
	choices_list, answer_text = generate_pI_choices(correct_pI, distractors)

	# Format with bptools MC formatter
	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices_list, answer_text
	)
	return complete_question

#===========================================================
#===========================================================
def parse_arguments():
	"""
	Parse command-line arguments for the titration pI generator.

	Returns:
		argparse.Namespace: parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate amino acid titration pI questions."
	)
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
def main():
	"""
	Main function: parse args, generate questions, write output file.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
if __name__ == '__main__':
	main()
