#!/usr/bin/env python3

# CSS border-radius sigmoid curve renderer.
# Renders N sigmoid transitions as quarter-ellipse arcs in an HTML table.
# Each sigmoid is a BR arc (bottom half) + TL arc (top half) arranged
# diagonally in a (2N x 2N) grid, with optional axis labels and
# separator-row/column crosshair guide lines with filled dot markers.


# Module-level curve color: easy to change in one place
CURVE_COLOR = "#003399"


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
def _build_row_sequence(
	n: int, row_heights: list, show_crosshairs: bool, sep_px: int
) -> list:
	"""Build row rendering sequence top-to-bottom.

	Returns list of (kind, index, height_px) tuples where kind is
	'data' or 'sep'. Data rows use 1-indexed row numbers; separator
	rows use the transition index they represent.
	"""
	seq = []
	# Walk transitions from highest (top) to lowest (bottom)
	for i in range(n - 1, -1, -1):
		tl_row = 2 * n - 2 * i - 1
		br_row = 2 * n - 2 * i
		# TL arc row (upper half of sigmoid)
		seq.append(('data', tl_row, row_heights[tl_row - 1]))
		# Separator row at transition boundary
		if show_crosshairs:
			seq.append(('sep', i, sep_px))
		# BR arc row (lower half of sigmoid)
		seq.append(('data', br_row, row_heights[br_row - 1]))
		# Buffer separator between consecutive transitions
		if show_crosshairs and i > 0:
			seq.append(('buf', i - 1, sep_px))
	return seq


#============================================
def _build_col_sequence(
	n: int, col_widths: list, show_crosshairs: bool, sep_px: int
) -> list:
	"""Build column rendering sequence left-to-right.

	Returns list of (kind, index, width_px) tuples where kind is
	'data' or 'sep'. Data cols use 1-indexed col numbers; separator
	cols use the transition index they represent.
	"""
	seq = []
	# Walk transitions from lowest (left) to highest (right)
	for i in range(n):
		br_col = 2 * i + 1
		tl_col = 2 * i + 2
		# BR arc column (left half of sigmoid pair)
		seq.append(('data', br_col, col_widths[br_col - 1]))
		# Separator column at midpoint vertical
		if show_crosshairs:
			seq.append(('sep', i, sep_px))
		# TL arc column (right half of sigmoid pair)
		seq.append(('data', tl_col, col_widths[tl_col - 1]))
		# Buffer separator between consecutive transitions
		if show_crosshairs and i < n - 1:
			seq.append(('buf', i, sep_px))
	return seq


#============================================
def _render_data_data_cell(
	col_idx: int, row_idx: int, col_w: int, row_h: int,
	tl_arcs: set, br_arcs: set,
	stroke_px: int, stroke_color: str,
	bg_empty: str, bg_arc_a: str, bg_arc_b: str,
	show_grid: bool,
) -> str:
	"""Render a regular data cell (may contain an arc)."""
	bg = bg_empty
	extra = ""
	if (col_idx, row_idx) in tl_arcs:
		bg = bg_arc_b
		extra += _style_tl_arc(col_w, row_h, stroke_px, stroke_color)
	elif (col_idx, row_idx) in br_arcs:
		bg = bg_arc_a
		extra += _style_br_arc(col_w, row_h, stroke_px, stroke_color)
	style = _td_style(col_w, row_h, bg, show_grid) + extra
	cell = "<td style='" + style + "'>&nbsp;</td>"
	return cell


#============================================
def _render_sep_col_in_data_row(
	sep_w: int, row_h: int, xh_color: str, show_vline: bool = True
) -> str:
	"""Render a separator-column cell inside a data row.

	Thin vertical spacer; dashed right border if show_vline is True.
	"""
	style = f"width:{sep_w}px; height:{row_h}px; "
	style += "padding:0; margin:0; border:none; "
	style += "font-size:0; line-height:0; "
	if show_vline:
		style += f"border-right:1px dashed {xh_color}; "
	style += "background:#ffffff; overflow:hidden; "
	cell = "<td style='" + style + "'>&nbsp;</td>"
	return cell


#============================================
def _render_data_col_in_sep_row(
	col_w: int, sep_h: int, xh_color: str
) -> str:
	"""Render a data-column cell inside a separator row.

	Thin horizontal spacer with dashed bottom border (horizontal guide).
	"""
	style = f"width:{col_w}px; height:{sep_h}px; "
	style += "padding:0; margin:0; "
	style += "font-size:0; line-height:0; "
	style += f"border:none; border-bottom:1px dashed {xh_color}; "
	style += "background:#ffffff; overflow:hidden; "
	cell = "<td style='" + style + "'>&nbsp;</td>"
	return cell


#============================================
def _render_sep_intersection(
	sep_w: int, sep_h: int, is_dot: bool,
	dot_color: str, xh_color: str, show_vline: bool = True
) -> str:
	"""Render a separator-row x separator-col intersection cell.

	If is_dot is True, fills the cell as a visible dot marker.
	Otherwise draws dashed borders (horizontal always, vertical
	only if show_vline is True).
	"""
	style = f"width:{sep_w}px; height:{sep_h}px; "
	style += "padding:0; margin:0; overflow:hidden; "
	style += "font-size:0; line-height:0; "
	if is_dot:
		# Filled dot at the sigmoid midpoint
		style += f"background:{dot_color}; border:none; "
		style += "border-radius:50%; "
	else:
		# Non-matching intersection: guide lines crossing
		style += "background:#ffffff; border:none; "
		# Horizontal guide always present
		style += f"border-bottom:1px dashed {xh_color}; "
		# Vertical guide only below the curve
		if show_vline:
			style += f"border-right:1px dashed {xh_color}; "
	cell = "<td style='" + style + "'>&nbsp;</td>"
	return cell


#============================================
def _render_buf_cell(
	w: int, h: int, is_dot: bool, dot_color: str
) -> str:
	"""Render a buffer separator cell: dot marker or blank spacer.

	Buffer cells appear at the horizontal-tangent connection points
	between consecutive sigmoids (buffer plateaus). A filled dot
	marks each connection; all other buffer cells are blank.
	"""
	style = f"width:{w}px; height:{h}px; "
	style += "padding:0; margin:0; overflow:hidden; "
	style += "font-size:0; line-height:0; "
	if is_dot:
		style += f"background:{dot_color}; border:none; "
		style += "border-radius:50%; "
	else:
		style += "background:#ffffff; border:none; "
	cell = "<td style='" + style + "'>&nbsp;</td>"
	return cell


#============================================
def _render_y_axis_table(
	y_range: tuple, tick_interval: float, actual_h_px: int
) -> str:
	"""Generate a left-side y-axis label table.

	Creates a table with the same total pixel height as the curve table
	but with rows at regular y-value intervals, so pH tick labels land
	at evenly spaced vertical positions.

	Args:
		y_range: (y_min, y_max) matching the curve chart.
		tick_interval: spacing between tick labels in y-units.
		actual_h_px: exact pixel height the y-axis must match.

	Returns:
		HTML table string for the y-axis.
	"""
	y_min, y_max = y_range
	total_span = y_max - y_min

	# Generate tick values from y_min upward
	ticks = []
	val = y_min
	while val <= y_max:
		ticks.append(val)
		val += tick_interval

	# Build rows top-to-bottom (highest y first)
	# Each row spans from an upper boundary to a lower boundary
	# The label sits at the bottom edge (= the lower tick value)
	rows = []

	# Top strip: y_max down to highest tick (may be thin or zero)
	if ticks[-1] < y_max:
		rows.append((y_max, ticks[-1], ""))

	# Main rows: between consecutive ticks, descending
	for i in range(len(ticks) - 1, 0, -1):
		# Format label: integer if whole number, else one decimal
		tick_val = ticks[i]
		if tick_val == int(tick_val):
			label = str(int(tick_val))
		else:
			label = f"{tick_val:.1f}"
		rows.append((ticks[i], ticks[i - 1], label))

	# Convert spans to pixel heights
	axis_style = ""
	axis_style += "border-collapse:separate; "
	axis_style += "border-spacing:0; "
	axis_style += "table-layout:fixed; "

	out = ""
	out += "<table style='" + axis_style + "'>"
	for y_top, y_bottom, label in rows:
		span = y_top - y_bottom
		h_px = max(1, round(span / total_span * actual_h_px))
		td_style = f"width:30px; height:{h_px}px; "
		td_style += "padding:0 4px 0 0; margin:0; border:none; "
		td_style += "text-align:right; vertical-align:bottom; "
		td_style += ""
		out += "<tr><td style='" + td_style + "'>"
		out += label + "</td></tr>"
	out += "</table>"
	return out


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
	stroke_color: str = CURVE_COLOR,
	show_crosshairs: bool = False,
	crosshair_color: str = "#999",
	dot_color: str = "#000",
	sep_px: int = 4,
	y_tick_interval: float = 0,
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
		show_crosshairs: if True, insert separator rows/columns with
			dashed guide lines and filled dot markers at transitions.
		crosshair_color: dashed guide line color.
		dot_color: filled dot color at sigmoid midpoints.
		sep_px: separator row height / column width in pixels.
		y_tick_interval: if > 0, add a left y-axis table with labels
			at this interval (e.g., 2 for pH labels every 2 units).
		show_grid: debug grid outlines.
		debug_fill: color arc cells for visual debugging.

	Returns:
		Single-line HTML table string (safe for BBQ embedding).
	"""
	n = len(transitions)
	if n < 1:
		raise ValueError("Need at least 1 transition")

	col_widths = _compute_col_widths(n, total_width_px)
	row_heights = _compute_row_heights(
		transitions, y_range, total_height_px
	)
	tl_arcs, br_arcs = _build_arc_sets(n)

	# Build rendering sequences for rows and columns
	row_seq = _build_row_sequence(
		n, row_heights, show_crosshairs, sep_px
	)
	col_seq = _build_col_sequence(
		n, col_widths, show_crosshairs, sep_px
	)

	# Map y_labels to TL data rows for annotation column
	# When crosshairs on, these cells get rowspan=2 to span into
	# the separator row below, with valign bottom at the boundary
	annot_map = {}
	if y_labels:
		for i, (_y_val, label_html) in enumerate(y_labels):
			if i < n:
				tl_row = 2 * n - 2 * i - 1
				annot_map[('data', tl_row)] = label_html

	# Track which separator rows are covered by a rowspan above
	spanned_seps = set()
	if show_crosshairs and y_labels:
		for i in range(min(len(y_labels), n)):
			spanned_seps.add(i)

	bg_empty = "#ffffff"
	bg_arc_a = "#7fa0cf" if debug_fill else "#ffffff"
	bg_arc_b = "#f07b7b" if debug_fill else "#ffffff"
	annot_w = 80

	# Solid axis lines on left and bottom edges of the curve area
	axis_px = 2
	axis_left = f"border-left:{axis_px}px solid #000; "

	# Table container style
	table_style = ""
	table_style += "border-collapse:separate; "
	table_style += "border-spacing:0; "
	table_style += "table-layout:fixed; "

	out = ""
	out += "<table style='" + table_style + "'>"

	# --- Data and separator rows ---
	for row_kind, row_idx, row_h in row_seq:
		out += "<tr>"

		# Emit cells for each column in the sequence
		for col_kind, col_idx, col_w in col_seq:
			# Buffer cell: dot at matching buf x buf, blank otherwise
			if row_kind == 'buf' or col_kind == 'buf':
				is_dot = (row_kind == 'buf' and col_kind == 'buf'
					and row_idx == col_idx)
				cell = _render_buf_cell(
					col_w, row_h, is_dot, dot_color
				)
			elif row_kind == 'data' and col_kind == 'data':
				# Regular data cell (may have arc)
				cell = _render_data_data_cell(
					col_idx, row_idx, col_w, row_h,
					tl_arcs, br_arcs,
					stroke_px, stroke_color,
					bg_empty, bg_arc_a, bg_arc_b,
					show_grid,
				)
			elif row_kind == 'data' and col_kind == 'sep':
				# Vertical guide only below the curve
				# BR row for this transition is at (2N - 2*col_idx)
				br_row = 2 * n - 2 * col_idx
				show_vline = (row_idx >= br_row)
				cell = _render_sep_col_in_data_row(
					col_w, row_h, crosshair_color, show_vline
				)
			elif row_kind == 'sep' and col_kind == 'data':
				# Data column in a separator row: horizontal guide
				cell = _render_data_col_in_sep_row(
					col_w, row_h, crosshair_color
				)
			else:
				# Separator intersection: dot if indices match
				is_dot = (row_idx == col_idx)
				# Vertical guide only below the curve:
				# row_idx < col_idx means this sep row is
				# lower in the table (below the curve)
				show_vline = (row_idx < col_idx)
				cell = _render_sep_intersection(
					col_w, row_h, is_dot,
					dot_color, crosshair_color, show_vline,
				)

			# Inject solid left axis border on leftmost column
			# Placed after border:none so arcs can still override
			axis_extra = ""
			if col_kind == 'data' and col_idx == 1:
				axis_extra += axis_left
			if axis_extra:
				cell = cell.replace(
					"border:none; ",
					"border:none; " + axis_extra,
					1,
				)
			out += cell

		# Annotation column cell
		if row_kind == 'buf':
			# Blank annotation for buffer separator rows
			a_style = f"width:{annot_w}px; "
			a_style += "padding:0; margin:0; border:none; "
			a_style += "font-size:0; line-height:0; "
			out += "<td style='" + a_style + "'>&nbsp;</td>"
		elif row_kind == 'sep' and row_idx in spanned_seps:
			# Skip: covered by rowspan from TL row above
			pass
		else:
			annot_key = (row_kind, row_idx)
			label = annot_map.get(annot_key, "&nbsp;")
			has_label = annot_key in annot_map
			a_style = f"width:{annot_w}px; "
			a_style += "padding:0 0 0 6px; margin:0; border:none; "
			a_style += "white-space:nowrap; "
			a_style += "vertical-align:bottom; "
			# Labeled TL row with crosshairs: span into separator row
			if has_label and show_crosshairs:
				a_style += "border-bottom:1px dashed "
				a_style += f"{crosshair_color}; "
				out += "<td rowspan='2' style='"
				out += a_style + "'>" + label + "</td>"
			else:
				out += "<td style='"
				out += a_style + "'>" + label + "</td>"

		out += "</tr>"

	# --- X-axis solid line row ---
	# Thin row spanning all columns to draw one continuous bottom axis
	out += "<tr>"
	for _col_kind, _col_idx, col_w in col_seq:
		ax_style = f"width:{col_w}px; height:{axis_px}px; "
		ax_style += "padding:0; margin:0; border:none; "
		ax_style += "font-size:0; line-height:0; "
		ax_style += "background:#000; overflow:hidden; "
		out += "<td style='" + ax_style + "'>&nbsp;</td>"
	# Blank annotation cell for axis row
	out += "<td style='width:" + str(annot_w)
	out += "px; border:none; font-size:0; line-height:0;'>&nbsp;</td>"
	out += "</tr>"

	# --- X-axis label row ---
	if x_labels:
		x_row_h = 20
		out += "<tr>"
		for col_kind, col_idx, col_w in col_seq:
			x_style = f"width:{col_w}px; height:{x_row_h}px; "
			x_style += "padding:2px 0 0 0; margin:0; border:none; "
			x_style += ""

			label = ""
			if col_kind == 'data':
				# First data col: left-aligned first label
				if col_idx == 1:
					x_style += "text-align:left; "
					label = x_labels[0]
				# Even data cols: right-aligned boundary label
				elif col_idx % 2 == 0:
					label_idx = col_idx // 2
					if label_idx < len(x_labels):
						x_style += "text-align:right; "
						label = x_labels[label_idx]
			# Separator cols in x-axis row are just spacers

			out += "<td style='" + x_style + "'>" + label + "</td>"

		# Empty annotation column in x-label row
		out += "<td style='width:" + str(annot_w)
		out += "px; border:none;'>&nbsp;</td>"
		out += "</tr>"

	# --- X-axis title row ---
	if x_axis_title:
		# Span across all data + separator columns
		n_content_cols = len(col_seq)
		out += "<tr>"
		t_style = "height:20px; padding:2px 0 0 0; margin:0; "
		t_style += "border:none; text-align:center; "
		out += "<td colspan='" + str(n_content_cols)
		out += "' style='" + t_style + "'>"
		out += x_axis_title + "</td>"
		out += "<td style='border:none;'>&nbsp;</td>"
		out += "</tr>"

	out += "</table>"

	# Wrap with y-axis table if tick interval is set
	if y_tick_interval > 0:
		# Compute actual curve data-area pixel height for alignment
		actual_h = sum(row_heights) + axis_px
		if show_crosshairs:
			# n transition seps + (n-1) buffer seps
			actual_h += (2 * n - 1) * sep_px
		y_axis_html = _render_y_axis_table(
			y_range, y_tick_interval, actual_h
		)
		# Wrapper table: y-axis left of curve
		wrapper = ""
		wrapper += "<table style='border-collapse:collapse;"
		wrapper += "border:none;'><tr>"
		wrapper += "<td style='vertical-align:top;"
		wrapper += "padding:0;border:none;'>"
		wrapper += y_axis_html
		wrapper += "</td>"
		wrapper += "<td style='vertical-align:top;"
		wrapper += "padding:0;border:none;'>"
		wrapper += out
		wrapper += "</td>"
		wrapper += "</tr></table>"
		result = wrapper
	else:
		result = out
	return result
