"""Inline-CSS primitives shared by restriction-digest DNA maps.

Graphical spans keep a non-empty &nbsp; so Blackboard HTML-to-image export
does not serialize them as self-closing XML that Chromium then drops.
"""

import html


DNA_ORANGE = "#b74300"
COORDINATE_BLACK = "#202020"
ENZYME_COLORS = ("#0067cc", "#00775f")  # navy, teal
TICK_THICKNESS = 3
TICK_LENGTH = 16
TICK_LABEL_EXTRA = 4


#============================================
def enzyme_color_map(enzyme_names: list[str] | tuple[str, ...]) -> dict[str, str]:
	"""Assign the approved enzyme colors in stable alphabetical enzyme-name order."""
	unique_names = sorted(set(enzyme_names))
	colors = {
		enzyme_name: ENZYME_COLORS[index % len(ENZYME_COLORS)]
		for index, enzyme_name in enumerate(unique_names)
	}
	return colors


#============================================
def make_vertical_tick(color: str, length: int = TICK_LENGTH) -> str:
	"""Return a 3 px wide vertical map tick."""
	tick_html = (
		'<span style="background-color: ' + color
		+ '; display: inline-block; font-size: 0; height: ' + str(length)
		+ 'px; line-height: 0; width: ' + str(TICK_THICKNESS) + 'px;">&nbsp;</span>'
	)
	return tick_html


#============================================
def make_horizontal_tick(color: str, length: int = TICK_LENGTH) -> str:
	"""Return a 3 px tall horizontal map tick."""
	tick_html = (
		'<span style="background-color: ' + color
		+ '; display: inline-block; font-size: 0; height: ' + str(TICK_THICKNESS)
		+ 'px; line-height: 0; width: ' + str(length) + 'px;">&nbsp;</span>'
	)
	return tick_html


#============================================
def make_rotated_tick(color: str, angle_deg: float, length: int = TICK_LENGTH) -> str:
	"""Return a 3 px tick rotated clockwise from vertical."""
	tick_html = (
		'<span style="background-color: ' + color
		+ '; display: inline-block; font-size: 0; height: ' + str(length)
		+ 'px; line-height: 0; transform: rotate(' + str(round(angle_deg, 1))
		+ 'deg); width: ' + str(TICK_THICKNESS) + 'px;">&nbsp;</span>'
	)
	return tick_html


#============================================
def make_enzyme_label(enzyme_name: str, color: str) -> str:
	"""Return a colored italic restriction-enzyme label."""
	name_html = html.escape(enzyme_name, quote=True)
	label_html = (
		'<span style="color: ' + color
		+ '; font-size: 18px; white-space: nowrap;"><i>' + name_html + '</i></span>'
	)
	return label_html


#============================================
def colored_enzyme_name(enzyme_name: str, color: str) -> str:
	"""Return an italic enzyme name in the map color for question prose."""
	name_html = html.escape(enzyme_name, quote=True)
	name_span = '<span style="color: ' + color + ';"><i>' + name_html + '</i></span>'
	return name_span


#============================================
def make_coordinate_label(coordinate: int, include_unit: bool = True) -> str:
	"""Return a black DNA-coordinate label, optionally including its kb unit."""
	label = str(coordinate)
	if include_unit:
		label += ' kb'
	label_html = (
		'<span style="color: ' + COORDINATE_BLACK
		+ '; font-size: 18px; white-space: nowrap;">' + label + '</span>'
	)
	return label_html


#============================================
def make_positioned(content: str, left: int, top: int, anchor: str = 'center') -> str:
	"""Place one map element at a fixed point inside a table-image canvas."""
	translations = {
		'center': 'translateX(-50%)',
		'left': 'none',
		'right': 'translateX(-100%)',
		'middle': 'translate(-50%, -50%)',
	}
	transform = translations[anchor]
	positioned_html = (
		f'<span style="left: {left}px; position: absolute; top: {top}px; '
		f'transform: {transform};">{content}</span>'
	)
	return positioned_html


#============================================
def make_canvas(width: int, height: int, content: str, description: str) -> str:
	"""Return one fixed-size drawing table for Blackboard HTML-to-image export."""
	description_html = html.escape(description, quote=True)
	# Absolute ticks and labels need a relative containing block.
	canvas_html = (
		'<table align="center" border="0" cellpadding="0" cellspacing="0" '
		f'role="img" aria-label="{description_html}" '
		'style="border-collapse: collapse; table-layout: fixed;"><tbody><tr>'
		f'<td style="background-color: #ffffff; height: {height}px; padding: 0; '
		f'width: {width}px;"><div style="height: {height}px; position: relative; '
		f'width: {width}px;">{content}</div></td>'
		'</tr></tbody></table>'
	)
	return canvas_html
