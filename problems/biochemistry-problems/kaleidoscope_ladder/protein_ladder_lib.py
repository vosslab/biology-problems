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
def mw_to_ln_fraction(mw_kda: float, mw_high_kda: float, mw_low_kda: float) -> float:
	"""
	Return the fraction along a ladder between two marker weights using ln(MW).

	`mw_high_kda` should be the higher marker (larger MW).
	`mw_low_kda` should be the lower marker (smaller MW).

	Returns a value in [0, 1] when `mw_kda` is between the markers.
	"""
	ln_high = math.log(float(mw_high_kda))
	ln_low = math.log(float(mw_low_kda))
	ln_val = math.log(float(mw_kda))
	return (ln_val - ln_high) / (ln_low - ln_high)


#====================================================================
def ln_fraction_to_mw_kda(mw_high_kda: float, mw_low_kda: float, fraction: float) -> float:
	"""
	Inverse of `mw_to_ln_fraction`: return MW (kDa) at a fraction between markers.
	"""
	ln_high = math.log(float(mw_high_kda))
	ln_low = math.log(float(mw_low_kda))
	ln_val = ln_high + float(fraction) * (ln_low - ln_high)
	return math.exp(ln_val)


#====================================================================
def simulate_kaleidoscope_band_y_positions_px(
	gel_height_px: int,
	run_factor: float=1.0,
	top_margin_px: int=28,
	bottom_margin_px: int=22,
) -> dict[int, float]:
	"""
	Return simulated y-positions (px from top) for the Kaleidoscope ladder bands.

	The mapping assumes migration distance is proportional to ln(MW) across the
	ladder range, then scales the run distance by `run_factor`:
	- `run_factor < 1.0`: gel run too short (bands compressed near the top)
	- `run_factor > 1.0`: gel run too long (low-MW bands may run off the bottom)
	"""
	if gel_height_px <= 0:
		raise ValueError("gel_height_px must be positive")
	if top_margin_px < 0 or bottom_margin_px < 0:
		raise ValueError("margins must be non-negative")
	if top_margin_px + bottom_margin_px >= gel_height_px:
		raise ValueError("margins exceed gel height")

	mw_values = get_kaleidoscope_mw_values()
	mw_high = float(mw_values[0])
	mw_low = float(mw_values[-1])

	usable = float(gel_height_px - top_margin_px - bottom_margin_px)
	ln_range = math.log(mw_high) - math.log(mw_low)

	positions: dict[int, float] = {}
	for mw in mw_values:
		# 0 at top marker, 1 at bottom marker.
		frac = (math.log(mw_high) - math.log(float(mw))) / ln_range
		y = float(top_margin_px) + float(run_factor) * frac * usable
		positions[mw] = y
	return positions


#====================================================================
def band_is_visible(y_px: float, gel_height_px: int, band_height_px: int=8) -> bool:
	top = y_px - band_height_px / 2.0
	bottom = y_px + band_height_px / 2.0
	return top >= 0.0 and bottom <= float(gel_height_px)


#====================================================================
def gen_gel_lanes_html(
	lanes: list[dict],
	gel_height_px: int=340,
	lane_width_px: int=72,
	band_height_px: int=8,
	lane_gap_px: int=18,
) -> str:
	"""
	Render a simple 1D SDS-PAGE gel cartoon using positioned div bands.

	Each lane dict supports:
	- label: str
	- bands: list of dicts with keys: y_px (float), color (str), optional border (str)
	"""
	lanes_html = f'<div style="display:flex; align-items:flex-start; gap:{lane_gap_px}px;">'
	for lane in lanes:
		label = lane.get("label", "")
		bands = lane.get("bands", [])
		lanes_html += '<div style="text-align:center; font-family:Arial, sans-serif;">'
		lanes_html += f'<div style="margin-bottom:6px;"><b>{label}</b></div>'
		lanes_html += (
			f'<div style="position:relative; width:{lane_width_px}px; height:{gel_height_px}px; '
			'border:2px solid #000; background-color:#f7f7f7;">'
		)
		for band in bands:
			y_px = float(band["y_px"])
			color = band.get("color", "#000")
			border = band.get("border", "1px solid #000")
			top_px = y_px - band_height_px / 2.0
			lanes_html += (
				f'<div style="position:absolute; left:6px; right:6px; '
				f'top:{top_px:.1f}px; height:{band_height_px}px; '
				f'background-color:{color}; border:{border};"></div>'
			)
		lanes_html += '</div></div>'
	lanes_html += '</div>'
	return lanes_html

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
