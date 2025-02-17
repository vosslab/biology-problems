#!/usr/bin/env python

import os
import math
import random
from collections import defaultdict

mw_color_map = {
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
default_blue_color_map = defaultdict(lambda: "#83c6ee")

band_height = 9
band_width = 50
spacer_height = 25
spacer_width = 12
label_width = 30
label_prefix = "&ndash; "
label_prefix = ""

row_count = 0

def spacer_row(height):
	if random.random() < 0.02 and height == band_height:
		spacer_row = (
			'<!-- White Spacer -->'
			f'<tr><td style="height: {height}px; background-color: #34a7e5;"></td></tr>'
		)
	else:
		spacer_row = (
			'<!-- White Spacer -->'
			f'<tr><td style="height: {height}px;"></td></tr>'
		)
	return spacer_row

def gen_band_rows(mw, gap_height, mw_color_map):
	global row_count
	rgb_color = mw_color_map[mw]
	quotient, remainder = divmod(gap_height, band_height)
	band_row = ""
	for _ in range(quotient):
		row_count += 1
		band_row += spacer_row(band_height)
	band_row += spacer_row(remainder)
	row_count += 1
	band_row += (
		f'<!-- Band = {mw} kD -->'
		'<tr>'
		f'  <td style="width: {band_width}px; height: {band_height}px; '
		f'    background-color: {rgb_color};"></td>'
		f'  <td rowspan="3" style="width: {label_width}px; vertical-align: top;" align="left">'
		f'    {label_prefix}{mw}</td>'
		'</tr>'
	)
	row_count += 1
	#print(f".. pre_row_count = {row_count}")
	return band_row


def gen_kaleidoscope_table(mw_values, mw_color_map, table_height):
	global row_count
	row_count = 0
	scale_constant = (table_height - 2*spacer_height - len(mw_values)*band_height)
	num_rows = 3 * len(mw_values) + 1
	num_rows = scale_constant // band_height + 20
	#print(f"num_rows = {num_rows}")
	table_width = label_width + band_width + spacer_width*3

	html_table = (
		f'<table cellspacing="0" cellpadding="0" width="{table_width}" height="{table_height}" '
		 ' style="border-spacing: 0; border-collapse: collapse; border: 2px solid black; display: inline-block;">'
		 '<!-- First and Third Columns Span All Rows -->\n'
		 '<tr>'
		f'  <td rowspan="{num_rows}" style="width: {spacer_width}px;"></td> <!-- Left White Column -->'
		f'  <td style="width: 50px; height: {spacer_height}px;"></td> <!-- White Spacer -->'
		f'  <td rowspan="{num_rows}" style="width: {spacer_width}px;"></td> <!-- Gap White Column -->'
		f'  <td rowspan="3" style="width: {label_width}px; vertical-align: middle;" align="left">'
		f'     {label_prefix}{mw_values[0]}</td> <!-- Right Label Column -->'
		f'  <td rowspan="{num_rows}" style="width: {spacer_width}px;"></td> <!-- Right White Column -->'
		 '</tr>\n'
		f'<tr><td style="width: {band_width}px; height: {band_height}px; '
		f'  background-color: {mw_color_map[mw_values[0]]};"></td></tr>'
	)
	row_count += 2
	gaps = calculate_mw_gaps(mw_values, scale_constant)
	quotient, remainder = divmod(scale_constant, band_height)
	for i, mw in enumerate(mw_values[1:]):
		gap_height = gaps[i]
		html_table += gen_band_rows(mw, gap_height, mw_color_map)
	html_table += (
		 '<!-- White Spacer -->'
		f'<tr><td style="height: {spacer_height//2}px;"></td></tr>'
		 '<!-- Final White All Column Spacer to Clean Up Border -->'
		f'<tr><td colspan="5" style="height: {spacer_height//2}px;"></td></tr>'
	)
	row_count += 2
	html_table += '</table>'
	#print(f"row_count = {row_count}")
	return html_table


def calculate_mw_gaps(mw_values, scale_constant):
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
assert calculate_mw_gaps([100, 50, 10], 100) == [30, 70]


def main():
	# Example usage:
	mw_values = [250, 150, 100, 75, 50, 37, 25, 20, 15, 10]
	scale_constant = 215

	result = calculate_mw_gaps(mw_values, scale_constant)
	#print(result)  # Expected Output: [34, 27, 19, 27, 20, 26, 15, 19, 27]

	mw_values = sorted(mw_color_map.keys(), reverse=True)
	#gen_kaleidoscope_table(mw_color_map, 580)
	gen_kaleidoscope_table(mw_values, mw_color_map, 450)
	# Create a defaultdict that always returns "#83c6ee"

	html_table = ""
	html_table += gen_kaleidoscope_table(mw_values, mw_color_map, 450)
	html_table += "&nbsp;"
	html_table += gen_kaleidoscope_table(mw_values, default_blue_color_map, 450)
	output_file = 'test_html_table.html'
	with open(output_file, 'w') as f:
		f.write(html_table)
	os.system(f"open {output_file}")

if __name__ == "__main__":
	main()
