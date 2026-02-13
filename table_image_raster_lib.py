#!/usr/bin/env python3

"""Reusable HTML table raster chart library.

Renders data as a grid of colored HTML table cells, producing
chart images that survive Blackboard HTML sanitizer (no SVG,
Canvas, or JavaScript required).
"""

# Standard Library
import math


#===========================================================
#===========================================================
class TableImageRaster:
	"""Rasterize 2-D data onto a grid of HTML table cells.

	Each cell is a fixed-size colored square. Three rendering layers
	(guides, curves, dots) are composited with dot > curve > guide
	priority. Axis labels and right-margin annotations are supported.
	"""

	#===========================================================
	#===========================================================
	def __init__(
		self, x_range: tuple, y_range: tuple,
		cols: int, rows: int, cell_px: int = 12
	):
		"""Create a new raster chart.

		Args:
			x_range: (x_min, x_max) data range for horizontal axis.
			y_range: (y_min, y_max) data range for vertical axis.
			cols: number of grid columns.
			rows: number of grid rows.
			cell_px: pixel width and height of each cell (default 12).
		"""
		self.x_min, self.x_max = x_range
		self.y_min, self.y_max = y_range
		self.cols = cols
		self.rows = rows
		self.cell_px = cell_px

		# Computed spacing between grid cells in data units
		self.x_step = (self.x_max - self.x_min) / max(1, cols - 1)
		self.y_step = (self.y_max - self.y_min) / max(1, rows - 1)
		# Dash stride adapts to cell size for ~12px visual dashes
		self._dash_stride = max(1, round(12.0 / cell_px))

		# Cell layers: (row, col) -> color string
		self._curve_cells = {}
		self._guide_cells = {}
		self._dot_cells = {}

		# Axis configuration
		self._y_tick_interval = None
		self._x_tick_values = []
		self._right_labels = {}
		self._x_axis_title = None

		# Default colors
		self.color_curve = '#2563eb'
		self.color_guide = '#d1d5db'
		self.color_dot = '#1f2937'
		self.color_bg = '#f8fafc'
		self.color_border = '#e5e7eb'

	#===========================================================
	#===========================================================
	def _x_to_col(self, x: float) -> int:
		"""Map an x data value to the nearest grid column index."""
		col = int(round((x - self.x_min) / self.x_step))
		return col

	#===========================================================
	#===========================================================
	def _y_to_row(self, y: float) -> int:
		"""Map a y data value to the nearest grid row index."""
		row = int(round((y - self.y_min) / self.y_step))
		return row

	#===========================================================
	#===========================================================
	@staticmethod
	def _parse_hex(hex_color: str) -> tuple:
		"""Parse '#rrggbb' hex color to (r, g, b) integer tuple."""
		h = hex_color.lstrip('#')
		r = int(h[0:2], 16)
		g = int(h[2:4], 16)
		b = int(h[4:6], 16)
		return (r, g, b)

	#===========================================================
	#===========================================================
	@staticmethod
	def _blend_hex(fg_hex: str, bg_hex: str, alpha: float) -> str:
		"""Blend foreground over background at given alpha.

		Args:
			fg_hex: foreground color as '#rrggbb'.
			bg_hex: background color as '#rrggbb'.
			alpha: blend factor (0.0 = pure bg, 1.0 = pure fg).

		Returns:
			str: blended color as '#rrggbb'.
		"""
		fg_rgb = TableImageRaster._parse_hex(fg_hex)
		bg_rgb = TableImageRaster._parse_hex(bg_hex)
		blended = []
		for fc, bc in zip(fg_rgb, bg_rgb):
			blended.append(int(fc * alpha + bc * (1 - alpha)))
		result = f"#{blended[0]:02x}{blended[1]:02x}{blended[2]:02x}"
		return result

	#===========================================================
	#===========================================================
	def plot_curve(
		self, points: list, color: str = None,
		antialiased: bool = False
	) -> None:
		"""Plot a curve from a sequence of (x, y) data points.

		Each point is mapped to the nearest grid cell and colored.
		Points outside the grid are silently clipped.

		Args:
			points: iterable of (x, y) tuples.
			color: CSS color string (default: self.color_curve).
			antialiased: if True, use bilinear sub-pixel blending
				to smooth curve edges.
		"""
		if color is None:
			color = self.color_curve
		if not antialiased:
			# Simple nearest-cell rendering
			for x, y in points:
				col = self._x_to_col(x)
				row = self._y_to_row(y)
				if 0 <= col < self.cols and 0 <= row < self.rows:
					self._curve_cells[(row, col)] = color
			return
		# Anti-aliased: bilinear sub-pixel blending across 4 neighbors
		alpha_map = {}
		for x, y in points:
			col_f = (x - self.x_min) / self.x_step
			row_f = (y - self.y_min) / self.y_step
			col_lo = int(math.floor(col_f))
			row_lo = int(math.floor(row_f))
			col_frac = col_f - col_lo
			row_frac = row_f - row_lo
			# Bilinear weights for the four surrounding cells
			weights = [
				(row_lo, col_lo, (1 - row_frac) * (1 - col_frac)),
				(row_lo, col_lo + 1, (1 - row_frac) * col_frac),
				(row_lo + 1, col_lo, row_frac * (1 - col_frac)),
				(row_lo + 1, col_lo + 1, row_frac * col_frac),
			]
			for row, col, alpha in weights:
				# Skip near-zero contributions
				if alpha < 0.05:
					continue
				if not (0 <= row < self.rows and 0 <= col < self.cols):
					continue
				key = (row, col)
				# Keep the highest alpha per cell
				if alpha > alpha_map.get(key, 0):
					alpha_map[key] = alpha
					blended = self._blend_hex(
						color, self.color_bg, alpha
					)
					self._curve_cells[key] = blended

	#===========================================================
	#===========================================================
	def add_hline(
		self, y: float, x_max: float = None,
		color: str = None, dashed: bool = True
	) -> None:
		"""Add a horizontal guide line at a given y value.

		Args:
			y: y data value for the line.
			x_max: draw from x_min to x_max (default: full width).
			color: CSS color (default: self.color_guide).
			dashed: if True, alternate on/off cells for a dashed look.
		"""
		if color is None:
			color = self.color_guide
		row = self._y_to_row(y)
		if x_max is not None:
			end_col = self._x_to_col(x_max) + 1
		else:
			end_col = self.cols
		stride2 = self._dash_stride * 2
		for c in range(min(end_col, self.cols)):
			if not dashed or (c % stride2 < self._dash_stride):
				if 0 <= row < self.rows:
					self._guide_cells[(row, c)] = color

	#===========================================================
	#===========================================================
	def add_vline(
		self, x: float, y_max: float = None,
		color: str = None, dashed: bool = True
	) -> None:
		"""Add a vertical guide line at a given x value.

		Args:
			x: x data value for the line.
			y_max: draw from y_min up to y_max (default: full height).
			color: CSS color (default: self.color_guide).
			dashed: if True, alternate on/off cells for a dashed look.
		"""
		if color is None:
			color = self.color_guide
		col = self._x_to_col(x)
		if y_max is not None:
			end_row = self._y_to_row(y_max) + 1
		else:
			end_row = self.rows
		stride2 = self._dash_stride * 2
		for r in range(min(end_row, self.rows)):
			if not dashed or (r % stride2 < self._dash_stride):
				if 0 <= col < self.cols:
					self._guide_cells[(r, col)] = color

	#===========================================================
	#===========================================================
	def add_crosshair(
		self, x: float, y: float,
		color: str = None, dashed: bool = True
	) -> None:
		"""Add crossing horizontal and vertical guide lines at (x, y).

		Convenience wrapper around add_hline and add_vline.
		"""
		self.add_hline(y, x_max=x, color=color, dashed=dashed)
		self.add_vline(x, y_max=y, color=color, dashed=dashed)

	#===========================================================
	#===========================================================
	def add_dot(
		self, x: float, y: float, color: str = None
	) -> None:
		"""Place a dot marker at a data point.

		Dots render with highest priority (above curves and guides).
		"""
		if color is None:
			color = self.color_dot
		col = self._x_to_col(x)
		row = self._y_to_row(y)
		if 0 <= col < self.cols and 0 <= row < self.rows:
			self._dot_cells[(row, col)] = color

	#===========================================================
	#===========================================================
	def set_y_tick_interval(self, interval: float) -> None:
		"""Set the interval for y-axis tick labels."""
		self._y_tick_interval = interval

	#===========================================================
	#===========================================================
	def set_x_tick_values(self, values: list) -> None:
		"""Set specific x values to label on the x-axis."""
		self._x_tick_values = list(values)

	#===========================================================
	#===========================================================
	def add_right_label(self, y: float, text: str) -> None:
		"""Add an annotation label on the right margin at y value."""
		row = self._y_to_row(y)
		self._right_labels[row] = text

	#===========================================================
	#===========================================================
	def set_x_axis_title(self, title: str) -> None:
		"""Set the title shown below the x-axis."""
		self._x_axis_title = title

	#===========================================================
	#===========================================================
	def to_html(self) -> str:
		"""Render the chart as an HTML table string.

		Cells are composited with priority: dot > curve > guide > empty.
		Uses table-layout:fixed so column widths are set once in the
		first row, keeping subsequent rows compact.

		Returns:
			str: self-contained HTML table fragment.
		"""
		px = self.cell_px
		has_right = bool(self._right_labels)
		# Width style only needed on first-row data cells
		w_sty = f"width:{px}px"

		# Open table with fixed layout for compact cell rendering
		html = ""
		html += "<table style='table-layout:fixed;"
		html += "border-collapse:collapse;margin:8px auto;"
		html += f"background:{self.color_bg};"
		html += f"border:1px solid {self.color_border};'>"

		# Data rows from top (high y) to bottom (low y)
		is_first_row = True
		for row_idx in range(self.rows - 1, -1, -1):
			y_val = self.y_min + row_idx * self.y_step
			# Row height set here instead of per-cell
			html += f"<tr style='height:{px}px'>"

			# Left column: y-axis tick label
			label = ""
			if self._y_tick_interval is not None:
				quotient = y_val / self._y_tick_interval
				if abs(quotient - round(quotient)) < 0.01:
					label = f"{y_val:g}"
			if is_first_row:
				html += "<td style='width:20px;font-size:10px;"
			else:
				html += "<td style='font-size:10px;"
			html += f"text-align:right;padding-right:2px;'>{label}</td>"

			# Data cells for the grid
			for col_idx in range(self.cols):
				key = (row_idx, col_idx)
				# Priority: dot > curve > guide > empty
				if key in self._dot_cells:
					bg = self._dot_cells[key]
				elif key in self._curve_cells:
					bg = self._curve_cells[key]
				elif key in self._guide_cells:
					bg = self._guide_cells[key]
				else:
					bg = None
				if is_first_row:
					# First row sets column widths for table-layout:fixed
					if bg is not None:
						html += f"<td style='{w_sty};background:{bg}'></td>"
					else:
						html += f"<td style='{w_sty}'></td>"
				else:
					# Subsequent rows inherit widths, only need bg
					if bg is not None:
						html += f"<td style='background:{bg}'></td>"
					else:
						html += "<td></td>"

			# Right column: annotation label
			if has_right:
				right_text = self._right_labels.get(row_idx, "")
				if is_first_row:
					html += "<td style='width:50px;font-size:9px;"
				else:
					html += "<td style='font-size:9px;"
				html += f"padding-left:3px;'>{right_text}</td>"

			html += "</tr>"
			is_first_row = False

		# X-axis tick labels
		if self._x_tick_values:
			tick_map = {}
			for x_val in self._x_tick_values:
				col = self._x_to_col(x_val)
				if 0 <= col < self.cols:
					tick_map[col] = f"{x_val:g}"
			html += "<tr><td></td>"
			for col_idx in range(self.cols):
				if col_idx in tick_map:
					html += "<td style='font-size:10px;"
					html += "text-align:center;'>"
					html += f"{tick_map[col_idx]}</td>"
				else:
					html += "<td></td>"
			if has_right:
				html += "<td></td>"
			html += "</tr>"

		# X-axis title
		if self._x_axis_title is not None:
			html += "<tr><td></td>"
			html += f"<td colspan='{self.cols}' style='font-size:10px;"
			html += "text-align:center;padding-top:2px;'>"
			html += f"{self._x_axis_title}</td>"
			if has_right:
				html += "<td></td>"
			html += "</tr>"

		html += "</table>"
		return html
