#!/usr/bin/env python3

# Standard Library
import os
import subprocess
import tempfile

# Local repo modules
import code_definitions


#===============================
def _draw_half_rect(svg_parts, box, fill_left, fill_right, outline_color, line_width):
	x0, y0, x1, y1 = box
	mid_x = (x0 + x1) / 2
	svg_parts.append(
		f"<rect x='{x0}' y='{y0}' width='{mid_x - x0}' height='{y1 - y0}' fill='{fill_left}' stroke='{outline_color}' stroke-width='{line_width}'/>")
	svg_parts.append(
		f"<rect x='{mid_x}' y='{y0}' width='{x1 - mid_x}' height='{y1 - y0}' fill='{fill_right}' stroke='{outline_color}' stroke-width='{line_width}'/>")


#===============================
def _draw_half_circle(svg_parts, defs_parts, box, fill_left, fill_right, outline_color, line_width, clip_id_prefix):
	x0, y0, x1, y1 = box
	cx = (x0 + x1) / 2
	cy = (y0 + y1) / 2
	radius = min(x1 - x0, y1 - y0) / 2
	mid_x = (x0 + x1) / 2

	clip_left_id = f"{clip_id_prefix}_L"
	clip_right_id = f"{clip_id_prefix}_R"

	defs_parts.append(
		f"<clipPath id='{clip_left_id}'>"
		f"<rect x='{x0}' y='{y0}' width='{mid_x - x0}' height='{y1 - y0}'/></clipPath>")
	defs_parts.append(
		f"<clipPath id='{clip_right_id}'>"
		f"<rect x='{mid_x}' y='{y0}' width='{x1 - mid_x}' height='{y1 - y0}'/></clipPath>")

	svg_parts.append(
		f"<circle cx='{cx}' cy='{cy}' r='{radius}' fill='{fill_left}' clip-path='url(#{clip_left_id})'/>")
	svg_parts.append(
		f"<circle cx='{cx}' cy='{cy}' r='{radius}' fill='{fill_right}' clip-path='url(#{clip_right_id})'/>")
	svg_parts.append(
		f"<circle cx='{cx}' cy='{cy}' r='{radius}' fill='none' stroke='{outline_color}' stroke-width='{line_width}'/>")


#===============================
def _draw_shape_cell(svg_parts, defs_parts, cell_box, shape_name, line_width, clip_id_prefix):
	x0, y0, x1, y1 = cell_box
	padding = max(3, int((x1 - x0) * 0.15))
	shape_box = [x0 + padding, y0 + padding, x1 - padding, y1 - padding]
	black = '#000000'
	white = '#ffffff'

	if shape_name == 'BLACK SQUARE':
		svg_parts.append(
			f"<rect x='{shape_box[0]}' y='{shape_box[1]}' width='{shape_box[2] - shape_box[0]}' height='{shape_box[3] - shape_box[1]}' fill='{black}' stroke='{black}' stroke-width='{line_width}'/>")
	elif shape_name == 'WHITE SQUARE':
		svg_parts.append(
			f"<rect x='{shape_box[0]}' y='{shape_box[1]}' width='{shape_box[2] - shape_box[0]}' height='{shape_box[3] - shape_box[1]}' fill='{white}' stroke='{black}' stroke-width='{line_width}'/>")
	elif shape_name == 'LEFT-HALF BLACK SQUARE':
		_draw_half_rect(svg_parts, shape_box, black, white, black, line_width)
	elif shape_name == 'RIGHT-HALF BLACK SQUARE':
		_draw_half_rect(svg_parts, shape_box, white, black, black, line_width)
	elif shape_name == 'BLACK CIRCLE':
		cx = (shape_box[0] + shape_box[2]) / 2
		cy = (shape_box[1] + shape_box[3]) / 2
		radius = min(shape_box[2] - shape_box[0], shape_box[3] - shape_box[1]) / 2
		svg_parts.append(
			f"<circle cx='{cx}' cy='{cy}' r='{radius}' fill='{black}' stroke='{black}' stroke-width='{line_width}'/>")
	elif shape_name == 'WHITE CIRCLE':
		cx = (shape_box[0] + shape_box[2]) / 2
		cy = (shape_box[1] + shape_box[3]) / 2
		radius = min(shape_box[2] - shape_box[0], shape_box[3] - shape_box[1]) / 2
		svg_parts.append(
			f"<circle cx='{cx}' cy='{cy}' r='{radius}' fill='{white}' stroke='{black}' stroke-width='{line_width}'/>")
	elif shape_name == 'LEFT-HALF BLACK CIRCLE':
		_draw_half_circle(svg_parts, defs_parts, shape_box, black, white, black, line_width, clip_id_prefix)
	elif shape_name == 'RIGHT-HALF BLACK CIRCLE':
		_draw_half_circle(svg_parts, defs_parts, shape_box, white, black, black, line_width, clip_id_prefix)


#===============================
def _draw_edge_cell(svg_parts, cell_box, edge_binary, line_width):
	x0, y0, x1, y1 = cell_box
	center_x = (x0 + x1) / 2
	center_y = (y0 + y1) / 2
	offset = max(2, line_width + 1)
	black = '#000000'

	# up
	if edge_binary[0] == '1':
		svg_parts.append(f"<line x1='{center_x}' y1='{y0}' x2='{center_x}' y2='{center_y}' stroke='{black}' stroke-width='{line_width}'/>")
	elif edge_binary[0] == '2':
		svg_parts.append(f"<line x1='{center_x - offset}' y1='{y0}' x2='{center_x - offset}' y2='{center_y}' stroke='{black}' stroke-width='{line_width}'/>")
		svg_parts.append(f"<line x1='{center_x + offset}' y1='{y0}' x2='{center_x + offset}' y2='{center_y}' stroke='{black}' stroke-width='{line_width}'/>")

	# down
	if edge_binary[1] == '1':
		svg_parts.append(f"<line x1='{center_x}' y1='{center_y}' x2='{center_x}' y2='{y1}' stroke='{black}' stroke-width='{line_width}'/>")
	elif edge_binary[1] == '2':
		svg_parts.append(f"<line x1='{center_x - offset}' y1='{center_y}' x2='{center_x - offset}' y2='{y1}' stroke='{black}' stroke-width='{line_width}'/>")
		svg_parts.append(f"<line x1='{center_x + offset}' y1='{center_y}' x2='{center_x + offset}' y2='{y1}' stroke='{black}' stroke-width='{line_width}'/>")

	# left
	if edge_binary[2] == '1':
		svg_parts.append(f"<line x1='{x0}' y1='{center_y}' x2='{center_x}' y2='{center_y}' stroke='{black}' stroke-width='{line_width}'/>")
	elif edge_binary[2] == '2':
		svg_parts.append(f"<line x1='{x0}' y1='{center_y - offset}' x2='{center_x}' y2='{center_y - offset}' stroke='{black}' stroke-width='{line_width}'/>")
		svg_parts.append(f"<line x1='{x0}' y1='{center_y + offset}' x2='{center_x}' y2='{center_y + offset}' stroke='{black}' stroke-width='{line_width}'/>")

	# right
	if edge_binary[3] == '1':
		svg_parts.append(f"<line x1='{center_x}' y1='{center_y}' x2='{x1}' y2='{center_y}' stroke='{black}' stroke-width='{line_width}'/>")
	elif edge_binary[3] == '2':
		svg_parts.append(f"<line x1='{center_x}' y1='{center_y - offset}' x2='{x1}' y2='{center_y - offset}' stroke='{black}' stroke-width='{line_width}'/>")
		svg_parts.append(f"<line x1='{center_x}' y1='{center_y + offset}' x2='{x1}' y2='{center_y + offset}' stroke='{black}' stroke-width='{line_width}'/>")


#===============================
def _label_color(shape_name: str) -> str:
	if shape_name.startswith('BLACK'):
		return '#ffffff'
	return '#000000'


#===============================
def make_pedigree_svg(code_string: str, scale: float = 1.0, show_grid: bool = False, label_string: str | None = None) -> str:
	"""
	Render a pedigree code string into an SVG image.

	Args:
		code_string (str): Pedigree code string.
		scale (float): Scaling factor for the output image size.
		show_grid (bool): Whether to draw faint grid lines.
		label_string (str | None): Optional label string aligned to code_string.

	Returns:
		str: Rendered SVG content.
	"""
	rows = code_definitions.get_code_rows(code_string)
	if not rows:
		raise ValueError('Empty pedigree code string.')

	max_cols = max(len(row) for row in rows)
	label_rows = None
	if label_string is not None:
		import label_strings
		errors = label_strings.validate_label_string(label_string, code_string)
		if errors:
			raise ValueError('Invalid label string: ' + '; '.join(errors))
		label_rows = code_definitions.get_code_rows(label_string)
	rows = [row.ljust(max_cols, '.') for row in rows]
	cell_size = max(8, int(code_definitions.table_cell_dimension * scale))
	width = max_cols * cell_size
	height = len(rows) * cell_size
	line_width = max(2, int(cell_size * 0.05))

	svg_parts = []
	defs_parts = []

	svg_parts.append(
		f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"
	)

	if show_grid:
		grid_color = '#dddddd'
		for row_idx in range(len(rows)):
			for col_idx in range(max_cols):
				x0 = col_idx * cell_size
				y0 = row_idx * cell_size
				svg_parts.append(
					f"<rect x='{x0}' y='{y0}' width='{cell_size}' height='{cell_size}' fill='none' stroke='{grid_color}' stroke-width='1'/>"
				)

	for row_idx, row in enumerate(rows):
		for col_idx, char in enumerate(row):
			shape_name = code_definitions.short_hand_lookup.get(char, None)
			if shape_name is None:
				continue
			x0 = col_idx * cell_size
			y0 = row_idx * cell_size
			x1 = x0 + cell_size
			y1 = y0 + cell_size
			cell_box = [x0, y0, x1, y1]
			clip_id_prefix = f"clip_{row_idx}_{col_idx}"
			if shape_name.endswith('SHAPE'):
				edge_binary = code_definitions.shape_binary_edges[shape_name]
				_draw_edge_cell(svg_parts, cell_box, edge_binary, line_width)
			elif shape_name.endswith('CIRCLE') or shape_name.endswith('SQUARE'):
				_draw_shape_cell(svg_parts, defs_parts, cell_box, shape_name, line_width, clip_id_prefix)
				if label_rows is not None and row_idx < len(label_rows) and col_idx < len(label_rows[row_idx]):
					label_char = label_rows[row_idx][col_idx]
					if label_char != '.':
						fill = _label_color(shape_name)
						text_x = x0 + cell_size / 2
						text_y = y0 + cell_size / 2
						font_size = max(10, int(cell_size * 0.52))
						svg_parts.append(
							f"<text x='{text_x}' y='{text_y}' text-anchor='middle' dominant-baseline='central' "
							f"font-size='{font_size}' font-weight='bold' fill='{fill}' dy='-0.1em'>{label_char}</text>"
						)

	if defs_parts:
		svg_parts.insert(1, '<defs>' + ''.join(defs_parts) + '</defs>')

	svg_parts.append('</svg>')
	return ''.join(svg_parts)


#===============================
def save_pedigree_svg(code_string: str, output_file: str, scale: float = 1.0, label_string: str | None = None) -> None:
	"""
	Render and save a pedigree SVG image.

	Args:
		code_string (str): Pedigree code string.
		output_file (str): Output file path.
		scale (float): Scaling factor for the output image size.
		label_string (str | None): Optional label string aligned to code_string.
	"""
	svg_text = make_pedigree_svg(code_string, scale, label_string=label_string)
	with open(output_file, 'w') as handle:
		handle.write(svg_text)


#===============================
def save_pedigree_png(code_string: str, output_file: str, scale: float = 1.0, label_string: str | None = None) -> None:
	"""
	Render and save a pedigree PNG image by converting SVG output.

	Args:
		code_string (str): Pedigree code string.
		output_file (str): Output file path.
		scale (float): Scaling factor for the output image size.
		label_string (str | None): Optional label string aligned to code_string.
	"""
	svg_text = make_pedigree_svg(code_string, scale, label_string=label_string)
	with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as handle:
		handle.write(svg_text)
		tmp_path = handle.name
	try:
		subprocess.run(
			['rsvg-convert', tmp_path, '-o', output_file, '--background-color', '#ffffff'],
			check=True
		)
	finally:
		if os.path.exists(tmp_path):
			os.remove(tmp_path)


#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	save_pedigree_svg(sample_code, 'pedigree_preview.svg', scale=1.2)

## THE END
