#!/usr/bin/env python3

# PIP3 modules
import PIL.Image
import PIL.ImageDraw

# Local repo modules
import pedigree_code_lib


#===============================
def _draw_half_rect(draw, box, fill_left, fill_right, outline_color, line_width):
	x0, y0, x1, y1 = box
	mid_x = int((x0 + x1) / 2)
	draw.rectangle([x0, y0, mid_x, y1], fill=fill_left, outline=outline_color, width=line_width)
	draw.rectangle([mid_x, y0, x1, y1], fill=fill_right, outline=outline_color, width=line_width)


#===============================
def _draw_half_circle(draw, box, fill_left, fill_right, outline_color, line_width):
	x0, y0, x1, y1 = box
	mid_x = int((x0 + x1) / 2)
	left_box = [x0, y0, mid_x, y1]
	right_box = [mid_x, y0, x1, y1]
	draw.ellipse(left_box, fill=fill_left, outline=outline_color, width=line_width)
	draw.ellipse(right_box, fill=fill_right, outline=outline_color, width=line_width)


#===============================
def _draw_shape_cell(draw, cell_box, shape_name, line_width):
	x0, y0, x1, y1 = cell_box
	padding = max(3, int((x1 - x0) * 0.15))
	shape_box = [x0 + padding, y0 + padding, x1 - padding, y1 - padding]
	black = "#000000"
	white = "#ffffff"

	if shape_name == 'BLACK SQUARE':
		draw.rectangle(shape_box, fill=black, outline=black, width=line_width)
	elif shape_name == 'WHITE SQUARE':
		draw.rectangle(shape_box, fill=white, outline=black, width=line_width)
	elif shape_name == 'LEFT-HALF BLACK SQUARE':
		_draw_half_rect(draw, shape_box, black, white, black, line_width)
	elif shape_name == 'RIGHT-HALF BLACK SQUARE':
		_draw_half_rect(draw, shape_box, white, black, black, line_width)
	elif shape_name == 'BLACK CIRCLE':
		draw.ellipse(shape_box, fill=black, outline=black, width=line_width)
	elif shape_name == 'WHITE CIRCLE':
		draw.ellipse(shape_box, fill=white, outline=black, width=line_width)
	elif shape_name == 'LEFT-HALF BLACK CIRCLE':
		_draw_half_circle(draw, shape_box, black, white, black, line_width)
	elif shape_name == 'RIGHT-HALF BLACK CIRCLE':
		_draw_half_circle(draw, shape_box, white, black, black, line_width)


#===============================
def _draw_edge_cell(draw, cell_box, edge_binary, line_width):
	x0, y0, x1, y1 = cell_box
	center_x = int((x0 + x1) / 2)
	center_y = int((y0 + y1) / 2)
	offset = max(2, line_width + 1)
	black = "#000000"

	# up
	if edge_binary[0] == '1':
		draw.line([center_x, y0, center_x, center_y], fill=black, width=line_width)
	elif edge_binary[0] == '2':
		draw.line([center_x - offset, y0, center_x - offset, center_y], fill=black, width=line_width)
		draw.line([center_x + offset, y0, center_x + offset, center_y], fill=black, width=line_width)

	# down
	if edge_binary[1] == '1':
		draw.line([center_x, center_y, center_x, y1], fill=black, width=line_width)
	elif edge_binary[1] == '2':
		draw.line([center_x - offset, center_y, center_x - offset, y1], fill=black, width=line_width)
		draw.line([center_x + offset, center_y, center_x + offset, y1], fill=black, width=line_width)

	# left
	if edge_binary[2] == '1':
		draw.line([x0, center_y, center_x, center_y], fill=black, width=line_width)
	elif edge_binary[2] == '2':
		draw.line([x0, center_y - offset, center_x, center_y - offset], fill=black, width=line_width)
		draw.line([x0, center_y + offset, center_x, center_y + offset], fill=black, width=line_width)

	# right
	if edge_binary[3] == '1':
		draw.line([center_x, center_y, x1, center_y], fill=black, width=line_width)
	elif edge_binary[3] == '2':
		draw.line([center_x, center_y - offset, x1, center_y - offset], fill=black, width=line_width)
		draw.line([center_x, center_y + offset, x1, center_y + offset], fill=black, width=line_width)


#===============================
def make_pedigree_png(code_string: str, scale: float = 1.0) -> PIL.Image.Image:
	"""
	Render a pedigree code string into a PNG image.

	Args:
		code_string (str): Pedigree code string.
		scale (float): Scaling factor for the output image size.

	Returns:
		PIL.Image.Image: Rendered pedigree image.
	"""
	rows = pedigree_code_lib.get_code_rows(code_string)
	if not rows:
		raise ValueError("Empty pedigree code string.")

	max_cols = max(len(row) for row in rows)
	cell_size = max(8, int(pedigree_code_lib.table_cell_dimension * scale))
	width = max_cols * cell_size
	height = len(rows) * cell_size

	image = PIL.Image.new("RGB", (width, height), "#ffffff")
	draw = PIL.ImageDraw.Draw(image)
	line_width = max(2, int(cell_size * 0.05))

	for row_idx, row in enumerate(rows):
		for col_idx, char in enumerate(row):
			shape_name = pedigree_code_lib.short_hand_lookup.get(char, None)
			if shape_name is None:
				continue
			x0 = col_idx * cell_size
			y0 = row_idx * cell_size
			x1 = x0 + cell_size
			y1 = y0 + cell_size
			cell_box = [x0, y0, x1, y1]
			if shape_name.endswith('SHAPE'):
				edge_binary = pedigree_code_lib.shape_binary_edges[shape_name]
				_draw_edge_cell(draw, cell_box, edge_binary, line_width)
			elif shape_name.endswith('CIRCLE') or shape_name.endswith('SQUARE'):
				_draw_shape_cell(draw, cell_box, shape_name, line_width)
			else:
				continue

	return image


#===============================
def save_pedigree_png(code_string: str, output_file: str, scale: float = 1.0) -> None:
	"""
	Render and save a pedigree PNG image.

	Args:
		code_string (str): Pedigree code string.
		output_file (str): Output file path.
		scale (float): Scaling factor for the output image size.
	"""
	image = make_pedigree_png(code_string, scale)
	image.save(output_file, format="PNG")


#===============================
#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	save_pedigree_png(sample_code, "pedigree_preview.png", scale=1.2)

## THE END
