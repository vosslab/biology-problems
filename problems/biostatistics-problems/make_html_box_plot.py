#!/usr/bin/env python3


from fractions import Fraction
from math import lcm


def _infer_scale(values):
	"""Return a scale factor based on fractional denominators (limited to 10)."""
	scale = 1
	for value in values:
		if value is None:
			continue
		frac = Fraction(value).limit_denominator(10)
		scale = lcm(scale, frac.denominator)
	return scale


def _scale_value(value, scale):
	return int(round(value * scale))


def _is_intish(value):
	return abs(value - round(value)) <= 1e-9


def _format_axis_value(value):
	return format(value, "g")


class BoxPlot:
	"""Represents the structure of a box plot with elements such as whiskers, box edges, median, and mean."""

	def __init__(self, axis_start, whisker_start, box_start, median, box_end, whisker_end, axis_end, mean, scale=None):
		"""
		Initializes the BoxPlot object with the necessary parameters.

		Args:
			axis_start (int): Starting point of the axis.
			whisker_start (int): Starting point of the whisker.
			box_start (int): Starting point of the box.
			median (int): The median value.
			box_end (int): Ending point of the box.
			whisker_end (int): Ending point of the whisker.
			axis_end (int): Ending point of the axis.
			mean (int): The mean value.

		Raises:
			ValueError: If the input values do not follow the expected order.
		"""
		self.axis_start = axis_start
		self.whisker_start = whisker_start
		self.box_start = box_start
		self.median = median
		self.box_end = box_end
		self.whisker_end = whisker_end
		self.axis_end = axis_end
		self.mean = mean
		self.scale = scale if scale is not None else _infer_scale([
			axis_start,
			whisker_start,
			box_start,
			median,
			box_end,
			whisker_end,
			axis_end,
			mean,
		])

		# Validate inputs upon creation
		errors = self.validate_inputs()
		if errors:
			error_message = "\n".join(errors)
			raise ValueError(f"Invalid BoxPlot values:\n{error_message}")

	def validate_inputs(self):
		"""Validate the order of the input values and return a list of any values that are out of range."""
		errors = []

		# Allow ties in the five-number summary (nondecreasing order)
		if not self.axis_start <= self.whisker_start:
			errors.append(f"whisker_start ({self.whisker_start}) must be greater than or equal to axis_start ({self.axis_start})")
		if not self.whisker_start <= self.box_start:
			errors.append(f"box_start ({self.box_start}) must be greater than or equal to whisker_start ({self.whisker_start})")
		if not self.box_start <= self.median:
			errors.append(f"median ({self.median}) must be greater than or equal to box_start ({self.box_start})")
		if not self.median <= self.box_end:
			errors.append(f"box_end ({self.box_end}) must be greater than or equal to median ({self.median})")
		if not self.box_end <= self.whisker_end:
			errors.append(f"whisker_end ({self.whisker_end}) must be greater than or equal to box_end ({self.box_end})")
		if not self.whisker_end <= self.axis_end:
			errors.append(f"axis_end ({self.axis_end}) must be greater than or equal to whisker_end ({self.whisker_end})")
		if not self.axis_start < self.axis_end:
			errors.append(f"axis_end ({self.axis_end}) must be greater than axis_start ({self.axis_start})")

		return errors

	def pretty_print_values(self):
		"""Prints the values of the box plot in a formatted manner."""
		print("BoxPlot Values:")
		print(f"  Axis Start:    {self.axis_start}")
		print(f"  Whisker Start: {self.whisker_start}")
		print(f"  Box Start:     {self.box_start}")
		print(f"  Median:        {self.median}")
		print(f"  Box End:       {self.box_end}")
		print(f"  Whisker End:   {self.whisker_end}")
		print(f"  Axis End:      {self.axis_end}")
		print(f"  Mean:          {self.mean}")


#==============

def create_grid(axis_start, axis_end, scale=1):
	"""
	Initialize a grid with empty cells for the axis.

	Args:
		axis_start (int): Starting point of the axis.
		axis_end (int): Ending point of the axis.

	Returns:
		list: A list of strings representing grid cells initialized as 'empty'.
	"""
	axis_start_grid = _scale_value(axis_start, scale)
	axis_end_grid = _scale_value(axis_end, scale)
	num_cells = axis_end_grid - axis_start_grid + 2
	return ['empty' for _ in range(num_cells)]


#==============

def assign_elements(grid, box_plot):
	"""
	Assign roles to specific positions in the grid based on the box plot values.

	Args:
		grid (list): The grid to which elements are assigned.
		box_plot (BoxPlot): The BoxPlot object containing positions of various elements.

	Returns:
		list: The modified grid with elements assigned.
	"""
	# Calculate positions relative to the axis start
	axis_start_grid = _scale_value(box_plot.axis_start, box_plot.scale)
	whisker_start_idx = _scale_value(box_plot.whisker_start, box_plot.scale) - axis_start_grid + 1
	whisker_end_idx = _scale_value(box_plot.whisker_end, box_plot.scale) - axis_start_grid
	box_start_idx = _scale_value(box_plot.box_start, box_plot.scale) - axis_start_grid + 1
	box_end_idx = _scale_value(box_plot.box_end, box_plot.scale) - axis_start_grid
	median_left_idx = _scale_value(box_plot.median, box_plot.scale) - axis_start_grid + 1
	median_right_idx = median_left_idx
	mean_left_idx = _scale_value(box_plot.mean, box_plot.scale) - axis_start_grid
	mean_right_idx = mean_left_idx + 1

	# Assign roles to the grid cells
	grid[whisker_start_idx] = 'left_whisker_end'
	grid[whisker_end_idx] = 'right_whisker_end'
	grid[box_start_idx] = 'left_box_end'
	grid[box_end_idx] = 'right_box_end'

	# Assign median
	grid[median_left_idx] = 'left_median'
	grid[median_right_idx] = 'right_median'

	# Assign mean
	grid[mean_left_idx] = 'left_mean'
	grid[mean_right_idx] = 'right_mean'

	# Fill in the box area
	for i in range(box_start_idx + 1, box_end_idx):
		if grid[i] == 'empty':
			grid[i] = 'inside_box'

	# Fill in the solid line area (between the whisker and the box)
	for i in range(whisker_start_idx, box_start_idx):
		if grid[i] == 'empty':
			grid[i] = 'solid_line'

	# Fill in the solid line area (between the box and the whisker)
	for i in range(box_end_idx, whisker_end_idx):
		if grid[i + 1] == 'empty':
			grid[i + 1] = 'solid_line'

	return grid


#==============

def write_box_row_html(grid, level="top"):
	"""
	Generates an HTML row for the box plot elements.

	Args:
		grid (list): The grid representing box plot elements.
		level (str): Specifies the line level ('top' or 'bottom') for the table row.

	Returns:
		str: An HTML string for the row.
	"""
	if level == "top":
		line_level = "bottom"
	else:
		line_level = "top"

	border = "1px solid black;"
	backgr = "background-color: #f5d0a9;"
	width = "width: 30px;"

	html = '  <tr>\n'
	for cell in grid:
		if cell == 'empty':
			html += f'    <td style="{width}">&nbsp;</td>\n'
		elif cell == 'solid_line':
			html += f'    <td style="border-{line_level}: {border} {width}">&nbsp;</td>\n'
		elif cell == 'left_whisker_end':
			html += f'    <td style="border-left: {border} border-{line_level}: {border} {width}">&nbsp;</td>\n'
		elif cell == 'right_whisker_end':
			html += f'    <td style="border-right: {border} border-{line_level}: {border} {width}">&nbsp;</td>\n'
		elif cell == 'left_box_end':
			html += f'    <td style="border-left: {border} border-{level}: {border} {backgr} {width}">&nbsp;</td>\n'
		elif cell == 'right_box_end':
			html += f'    <td style="border-right: {border} border-{level}: {border} {backgr} {width}">&nbsp;</td>\n'
		elif cell == 'inside_box':
			html += f'    <td style="border-{level}: {border} {backgr} {width}">&nbsp;</td>\n'
		elif cell == 'left_median':
			html += f'    <td style="border-right: {border} border-{level}: {border} {backgr} text-align: center; {width}">&nbsp;</td>\n'
		elif cell == 'right_median':
			html += f'    <td style="border-left: {border} border-{level}: {border} {backgr} text-align: center; {width}">&nbsp;</td>\n'
		elif cell == 'left_mean':
			if level == 'bottom':
				continue
			html += f'    <td colspan=2 rowspan=2 style="border-top: {border} border-bottom: {border} {backgr} text-align: center; width: 60px;">&#10005;</td>\n'
		elif cell == 'right_mean':
			continue
	html += '  </tr>\n'
	return html

#==============
def write_axis_row_ticks_html(grid, axis_start, line_location="top"):
	"""
	Generates an HTML row for axis ticks.

	Args:
		grid (list): The grid representing box plot elements.
		axis_start (int): The starting point of the axis.
		line_location (str): The location of the line ('top' or 'bottom').

	Returns:
		str: An HTML string for the row with axis ticks.
	"""
	border = "2px solid black;"
	border_merge = f"border-{line_location}: {border} border-left: {border} border-right: {border}"
	width = "width: 30px;"

	html = '  <tr>\n'
	# Add arrows to indicate the direction if the line is on the bottom
	if line_location == 'bottom':
		html += f'    <td rowspan=2 style="{width} text-align: right;"><strong>&xlarr;</strong></td>\n'

	# Add cells with borders for axis ticks
	for _ in range(len(grid) - 2):
		html += f'    <td style="{border_merge} {width}">&nbsp;</td>\n'

	# Add arrows to indicate the direction if the line is on the bottom
	if line_location == 'bottom':
		html += f'    <td rowspan=2 style="{width} text-align: right;"><strong>&xrarr;</strong></td>\n'

	html += '  </tr>\n'
	return html



#==============

def write_axis_row_labels_html(axis_start, axis_end, label_mod=5, scale=1):
	"""
	Generates an HTML row for axis labels.

	Args:
		axis_start (int): The starting point of the axis.
		axis_end (int): The ending point of the axis.
		label_mod (int): The modulus value to determine where labels appear on the axis.

	Returns:
		str: An HTML string for the row with axis labels.
	"""
	width = "width: 30px;"
	width2 = "width: 60px;"

	html = '  <tr>\n'
	axis_start_grid = _scale_value(axis_start, scale)
	axis_end_grid = _scale_value(axis_end, scale)
	grid_index = axis_start_grid
	while grid_index <= axis_end_grid:
		value = grid_index / scale
		if _is_intish(value) and int(round(value)) % label_mod == 0:
			label = _format_axis_value(value)
			html += f'    <td colspan=2 style="{width2} text-align: center">{label}</td>\n'
			grid_index += 2
			continue
		html += f'    <td style="{width}">&nbsp;</td>'
		grid_index += 1
	html += '  </tr>\n'
	return html



#==============

def generate_html(grid, axis_start, axis_end, scale=1):
	"""
	Generate the complete HTML table code based on the grid.

	Args:
		grid (list): The grid with assigned box plot elements.
		axis_start (int): The starting point of the axis.
		axis_end (int): The ending point of the axis.

	Returns:
		str: The complete HTML for the box plot table.
	"""
	html = '<table style="border-collapse: collapse;">\n'

	# Add the top and bottom rows of the box plot
	html += write_box_row_html(grid, level="top")
	html += write_box_row_html(grid, level="bottom")

	# Spacer row for visual separation between box plot and axis
	html += '  <tr>\n'
	html += f'    <td colspan="{len(grid)}" style="height: 10px;">&nbsp;</td>\n'
	html += '  </tr>\n'

	# Add rows for the axis ticks
	html += write_axis_row_ticks_html(grid, axis_start, line_location="bottom")
	html += write_axis_row_ticks_html(grid, axis_start, line_location="top")

	# Add row for the axis labels
	html += write_axis_row_labels_html(axis_start, axis_end, scale=scale)

	html += '</table>'
	return html

#==============

def print_grid(grid, axis_start):
	"""
	Print the grid using abbreviations for each cell's role.

	Args:
		grid (list): The grid representing the box plot elements.
		axis_start (int): The starting point of the axis.
	"""
	# Print axis index numbers
	for i in range(len(grid) + 1):
		index = axis_start + i
		print(f"{index: 3d}|", end='')
	print()  # Newline for better formatting

	# Print grid cells using abbreviations
	for cell in grid:
		# Abbreviate cell name by taking the first letter of each word, padding to 3 characters
		abbreviated = ''.join([word[0] for word in cell.split('_')])
		abbreviated = abbreviated.ljust(3, abbreviated[-1])[:3]
		print(f"{abbreviated}|", end='')
	print()  # Newline for better formatting


#==============

def generate_boxplot_html(box_plot):
	"""
	Generates the HTML representation of a box plot.

	Args:
		box_plot (BoxPlot): The BoxPlot object containing the plot data.

	Returns:
		str: The generated HTML code for the box plot.
	"""
	# Create grid
	grid = create_grid(box_plot.axis_start, box_plot.axis_end, scale=box_plot.scale)

	# Assign elements to the grid
	grid = assign_elements(grid, box_plot)

	# Print the grid to the console for debugging purposes
	print_grid(grid, box_plot.axis_start)

	# Generate the HTML for the box plot
	html = generate_html(grid, box_plot.axis_start, box_plot.axis_end, scale=box_plot.scale)

	return html


#==============
if __name__ == "__main__":
	# Example usage
	box_plot = BoxPlot(10, 11, 12, 13, 16, 17, 25, 22)

	# Print box plot values
	box_plot.pretty_print_values()

	# Generate HTML code for the box plot
	html_code = generate_boxplot_html(box_plot)

	# Output the HTML to a file
	with open('boxplot.html', 'w') as file:
		file.write(html_code)

	print("HTML has been written to boxplot.html")
