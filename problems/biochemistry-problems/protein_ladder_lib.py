#!/usr/bin/env python3

import math
from collections import defaultdict

KALEIDOSCOPE_MW_COLOR_MAP = {
	250: "#99dbfb",
	150: "#adafdf",
	100: "#83c6ee",
	75:  "#feacd6",
	50:  "#80caf1",
	37:  "#9adb7f",
	25:  "#ffbbdc",
	20:  "#6dbfec",
	15:  "#b3def6",
	10:  "#ffee00",
}
DEFAULT_BLUE_COLOR_MAP = defaultdict(lambda: "#83c6ee")

# Backwards-compat aliases (older scripts used these names)
mw_color_map = KALEIDOSCOPE_MW_COLOR_MAP
default_blue_color_map = DEFAULT_BLUE_COLOR_MAP

band_height = 9
band_width = 50
spacer_height = 25
spacer_width = 12
label_width = 30

#====================================================================
def gen_spacer_cell(height: int, width: int|None=None) -> str:
	spacer_cell_html = '<td style="'
	spacer_cell_html += f' height: {height}px; '
	if width is not None:
		spacer_cell_html += f' width: {width}px; '
	spacer_cell_html += ' background-color: #ddd; "></td>'
	return spacer_cell_html

#====================================================================
def gen_spacer_row(height: int, columns: int=5) -> str:
	"""
	Generate an HTML spacer row with a specified height.
	"""
	spacer_cell_html = gen_spacer_cell(height)
	spacer_row_html = '<tr>'
	for _ in range(columns):
		spacer_row_html += spacer_cell_html
	spacer_row_html += '</tr>\n'
	return spacer_row_html

#====================================================================
def gen_band_row(mw_kda: int, color_map: dict[int, str], label: str) -> str:
	rgb_color = color_map[mw_kda]
	band_spacer_cell_html = gen_spacer_cell(band_height)
	return (
		'<tr>'
		f'{band_spacer_cell_html}'
		f'  <td style="width: {band_width}px; height: {band_height}px; '
		f'    background-color: {rgb_color};"></td>'
		f'{band_spacer_cell_html}'
		f'  <td style="width: {label_width}px; vertical-align: top;" align="left">'
		f'    {label}</td>'
		f'{band_spacer_cell_html}'
		'</tr>\n'
	)

#====================================================================
def gen_kaleidoscope_table(mw_values, color_map, table_height: int, show_labels: bool=True, label_prefix: str="") -> str:
	"""
	Generate an HTML table representing a pre-stained protein ladder.

	Notes:
	- Spacing between bands is proportional to ln(MW) differences.
	- This is intended as a visual aid / simulation, not a measured gel.
	"""
	scale_constant = table_height - 2*spacer_height - len(mw_values)*band_height
	table_width = label_width + band_width + spacer_width*3
	html_table = (
		f'<table cellspacing="0" cellpadding="0" border="1" width="{table_width}" height="{table_height}" '
		 ' style="border-spacing: 0; border-collapse: collapse; border: 2px solid black; display: inline-block;">'
	)
	html_table += f'<tr><td colspan="5" style="height: {spacer_height}px; background-color: #ddd;"></td></tr>\n'

	def _label(mw_kda: int) -> str:
		if show_labels is False:
			return ""
		return f"{label_prefix}{mw_kda}"

	html_table += gen_band_row(mw_values[0], color_map, _label(mw_values[0]))
	gaps = calculate_mw_gaps(mw_values, scale_constant)
	for gap_height, mw_kda in zip(gaps, mw_values[1:], strict=True):
		html_table += gen_spacer_row(gap_height)
		html_table += gen_band_row(mw_kda, color_map, _label(mw_kda))

	html_table += (
		 '<!-- Final White All Column Spacer to Clean Up Border -->'
		f'<tr><td colspan="5" style="height: {spacer_height//2}px;"></td></tr>\n'
	)
	html_table += '</table>'
	return html_table

#====================================================================
def calculate_mw_gaps(mw_values: list[int], scale_constant: float) -> list[int]:
	"""
	Takes a list of molecular weights (mw_values), computes the log, differences,
	normalizes them, scales them by a constant, and returns the rounded list.

	Parameters:
		mw_values (list): List of molecular weights.
		scale_constant (float): Scaling factor to adjust the normalized values.

	Returns:
		list: Rounded scaled values as integers. (list length less one)
	"""
	sorted_mw_values = sorted(mw_values, reverse=True)
	if sorted_mw_values != mw_values:
		# raise error, otherwise outcome would be unpredictable
		raise ValueError("List must be sorted in reverse")

	# Step 1: Compute natural log of MW
	ln_mw = [math.log(x) for x in mw_values]

	# Step 2: Compute difference between adjacent bands (previous row minus current row)
	differences = [ln_mw[i] - ln_mw[i + 1] for i in range(len(ln_mw) - 1)]

	# Step 3: Normalize the differences by dividing by (MAX(B:B) - MIN(B:B))
	range_ln = max(ln_mw) - min(ln_mw)
	sum_diff = sum(differences)
	if not math.isclose(range_ln, sum_diff):
		raise ValueError

	# Step 4: Scale by the given scale constant
	# Step 5: Round to nearest integer
	rounded_scaled = [round(d * scale_constant / range_ln) for d in differences]

	# Return the final rounded scaled list (excluding None)
	return rounded_scaled

#====================================================================
def get_kaleidoscope_mw_values() -> list[int]:
	return sorted(KALEIDOSCOPE_MW_COLOR_MAP.keys(), reverse=True)

#====================================================================
def get_kaleidoscope_markers() -> list[tuple[int, str]]:
	"""
	Returns a list of (mw_kda, color_hex) tuples in descending MW order.
	"""
	return [(mw, KALEIDOSCOPE_MW_COLOR_MAP[mw]) for mw in get_kaleidoscope_mw_values()]

#====================================================================
def main():
	import argparse

	parser = argparse.ArgumentParser(description="Generate an HTML representation of the Kaleidoscope protein ladder.")
	parser.add_argument("-o", "--outfile", default="test_html_table.html", help="Output HTML file")
	parser.add_argument("--height", type=int, default=450, help="Table height (px)")
	args = parser.parse_args()

	mw_values = get_kaleidoscope_mw_values()
	html_table = gen_kaleidoscope_table(mw_values, KALEIDOSCOPE_MW_COLOR_MAP, args.height, show_labels=True, label_prefix="")
	html_table += "&nbsp;"
	html_table += gen_kaleidoscope_table(mw_values, DEFAULT_BLUE_COLOR_MAP, args.height, show_labels=False, label_prefix="")

	with open(args.outfile, "w") as handle:
		handle.write(html_table)
	print(args.outfile)

#====================================================================
#====================================================================
if __name__ == "__main__":
	main()
