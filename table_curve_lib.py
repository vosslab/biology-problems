#!/usr/bin/env python3

# CSS border-radius sigmoid curve renderer.
# Renders N sigmoid transitions as quarter-ellipse arcs in an HTML table.
# Each sigmoid is a BR arc (bottom half) + TL arc (top half) arranged
# diagonally in a (2N x 2N) grid, with optional axis labels and
# dashed crosshair guide lines.


#============================================
def _td_style(col_w: int, row_h: int, bg: str, show_grid: bool) -> str:
	"""Base cell style for a grid cell."""
	style = ""
	style += f"width:{col_w}px; height:{row_h}px; "
	style += "padding:0; margin:0; border:none; "
	style += f"background:{bg}; "
	style += "overflow:hidden; "
	if show_grid:
		style += "outline:2px solid #2f8f2f; outline-offset:-1px; "
	return style


#============================================
def _style_tl_arc(rx: int, ry: int, stroke_px: int, color: str) -> str:
	"""Top-left quarter-ellipse arc (upper half of a sigmoid)."""
	style = ""
	style += f"border-top:{stroke_px}px solid {color}; "
	style += f"border-left:{stroke_px}px solid {color}; "
	style += f"border-top-left-radius:{rx}px {ry}px; "
	return style


#============================================
def _style_br_arc(rx: int, ry: int, stroke_px: int, color: str) -> str:
	"""Bottom-right quarter-ellipse arc (lower half of a sigmoid)."""
	style = ""
	style += f"border-bottom:{stroke_px}px solid {color}; "
	style += f"border-right:{stroke_px}px solid {color}; "
	style += f"border-bottom-right-radius:{rx}px {ry}px; "
	return style


#============================================
def _compute_row_heights(
	transitions: list, y_range: tuple, total_height_px: int
) -> list:
	"""Compute pixel heights for 2N rows from N transition y-values.

	Row ordering is top-to-bottom (row 1 = highest y, row 2N = lowest y).
	Each transition splits into a BR arc row (below) and TL arc row (above).
	The buffer-zone rows between transitions are split equally.
	"""
	n = len(transitions)
	y_min, y_max = y_range
	total_span = y_max - y_min

	# Build spans bottom-to-top: row 2N, 2N-1, ..., 2, 1
	spans = []
	spans.append(transitions[0] - y_min)
	for i in range(n - 1):
		half_gap = (transitions[i + 1] - transitions[i]) / 2.0
		spans.append(half_gap)
		spans.append(half_gap)
	spans.append(y_max - transitions[n - 1])

	# Reverse to top-to-bottom order for table rows
	spans.reverse()

	# Convert to pixels with minimum 1px
	heights = []
	for span in spans:
		px = max(1, round(span / total_span * total_height_px))
		heights.append(px)
	return heights


#============================================
def _compute_col_widths(n: int, total_width_px: int) -> list:
	"""Compute equal pixel widths for 2N columns."""
	col_w = total_width_px // (2 * n)
	return [col_w] * (2 * n)


#============================================
def _build_arc_sets(n: int) -> tuple:
	"""Return (tl_arcs, br_arcs) as sets of (col, row) 1-indexed.

	For transition i (0-indexed, sorted ascending by y-value):
	  BR arc at col (2i+1), row (2N - 2i)     -- lower half of sigmoid
	  TL arc at col (2i+2), row (2N - 2i - 1) -- upper half of sigmoid
	"""
	tl_arcs = set()
	br_arcs = set()
	for i in range(n):
		br_arcs.add((2 * i + 1, 2 * n - 2 * i))
		tl_arcs.add((2 * i + 2, 2 * n - 2 * i - 1))
	return tl_arcs, br_arcs


#============================================
def _build_crosshair_sets(n: int) -> tuple:
	"""Return (xh_rows, xh_cols) for dashed guide lines.

	xh_rows: TL-arc rows that get border-bottom at transition boundary.
	xh_cols: BR-arc columns that get border-right at midpoint vertical.
	"""
	xh_rows = set()
	xh_cols = set()
	for i in range(n):
		xh_rows.add(2 * n - 2 * i - 1)
		xh_cols.add(2 * i + 1)
	return xh_rows, xh_cols


#============================================
def render_sigmoid_curve(
	transitions: list,
	y_range: tuple,
	x_labels: list = None,
	y_labels: list = None,
	x_axis_title: str = "",
	total_width_px: int = 600,
	total_height_px: int = 450,
	stroke_px: int = 3,
	stroke_color: str = "#000",
	show_crosshairs: bool = False,
	crosshair_color: str = "#999",
	show_grid: bool = False,
	debug_fill: bool = False,
) -> str:
	"""Render N sigmoid transitions as CSS border-radius arcs.

	Args:
		transitions: y-values at sigmoid midpoints, sorted ascending.
		y_range: (y_min, y_max) for the chart.
		x_labels: labels at column-pair boundaries (len N+1).
		y_labels: list of (y_value, label_html) for right annotations.
			Must be in same order as transitions.
		x_axis_title: optional centered title below x-axis labels.
		total_width_px: chart curve-area width in pixels.
		total_height_px: chart curve-area height in pixels.
		stroke_px: curve line thickness.
		stroke_color: curve color.
		show_crosshairs: if True, draw dashed guide lines at transitions.
		crosshair_color: dashed guide line color (when enabled).
		show_grid: debug grid outlines.
		debug_fill: color arc cells for visual debugging.

	Returns:
		Single-line HTML table string (safe for BBQ embedding).
	"""
	n = len(transitions)
	if n < 1:
		raise ValueError("Need at least 1 transition")

	col_widths = _compute_col_widths(n, total_width_px)
	row_heights = _compute_row_heights(transitions, y_range, total_height_px)
	tl_arcs, br_arcs = _build_arc_sets(n)
	if show_crosshairs:
		xh_rows, xh_cols = _build_crosshair_sets(n)
	else:
		xh_rows, xh_cols = set(), set()

	# Map y_labels to annotation column by transition index
	annot_map = {}
	if y_labels:
		for i, (_y_val, label_html) in enumerate(y_labels):
			if i < n:
				tl_row = 2 * n - 2 * i - 1
				annot_map[tl_row] = label_html

	bg_empty = "#ffffff"
	bg_arc_a = "#7fa0cf" if debug_fill else "#ffffff"
	bg_arc_b = "#f07b7b" if debug_fill else "#ffffff"

	annot_w = 80

	table_style = ""
	table_style += "border-collapse:separate; "
	table_style += "border-spacing:0; "
	table_style += "table-layout:fixed; "

	out = ""
	out += "<table style='" + table_style + "'>"

	# --- Data rows ---
	for r in range(1, 2 * n + 1):
		row_h = row_heights[r - 1]
		out += "<tr>"

		for c in range(1, 2 * n + 1):
			col_w = col_widths[c - 1]
			bg = bg_empty
			extra = ""

			if (c, r) in tl_arcs:
				bg = bg_arc_b
				extra += _style_tl_arc(col_w, row_h, stroke_px, stroke_color)
			elif (c, r) in br_arcs:
				bg = bg_arc_a
				extra += _style_br_arc(col_w, row_h, stroke_px, stroke_color)

			# Horizontal crosshair: dashed bottom on TL rows
			if r in xh_rows:
				extra += f"border-bottom:1px dashed {crosshair_color}; "

			# Vertical crosshair: dashed right on BR columns
			# Skip BR arc cells (they already have solid border-right)
			if c in xh_cols and (c, r) not in br_arcs:
				extra += f"border-right:1px dashed {crosshair_color}; "

			style = _td_style(col_w, row_h, bg, show_grid) + extra
			out += "<td style='" + style + "'>&nbsp;</td>"

		# Annotation column
		a_style = f"width:{annot_w}px; height:{row_h}px; "
		a_style += "padding:0 0 0 6px; margin:0; border:none; "
		a_style += "vertical-align:bottom; "
		a_style += "font-size:12px; white-space:nowrap; "
		if r in xh_rows:
			a_style += f"border-bottom:1px dashed {crosshair_color}; "
		label = annot_map.get(r, "&nbsp;")
		out += "<td style='" + a_style + "'>" + label + "</td>"

		out += "</tr>"

	# --- X-axis label row ---
	if x_labels:
		x_row_h = 20
		out += "<tr>"
		for c in range(1, 2 * n + 1):
			col_w = col_widths[c - 1]
			x_style = f"width:{col_w}px; height:{x_row_h}px; "
			x_style += "padding:2px 0 0 0; margin:0; border:none; "
			x_style += "font-size:12px; "

			if c in xh_cols:
				x_style += f"border-right:1px dashed {crosshair_color}; "

			label = ""
			if c == 1:
				x_style += "text-align:left; "
				label = x_labels[0]
			elif c % 2 == 0:
				label_idx = c // 2
				if label_idx < len(x_labels):
					x_style += "text-align:right; "
					label = x_labels[label_idx]

			out += "<td style='" + x_style + "'>" + label + "</td>"

		# Empty annotation column in x-label row
		out += "<td style='width:" + str(annot_w)
		out += "px; border:none;'>&nbsp;</td>"
		out += "</tr>"

	# --- X-axis title row ---
	if x_axis_title:
		out += "<tr>"
		t_style = "height:20px; padding:2px 0 0 0; margin:0; "
		t_style += "border:none; text-align:center; font-size:12px; "
		out += f"<td colspan='{2 * n}' style='" + t_style + "'>"
		out += x_axis_title + "</td>"
		out += "<td style='border:none;'>&nbsp;</td>"
		out += "</tr>"

	out += "</table>"
	return out
