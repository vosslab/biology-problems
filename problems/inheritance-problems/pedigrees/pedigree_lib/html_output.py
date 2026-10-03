"""Positioned HTML from shared geometry; one framed rasterization container."""

# Standard Library
import html

# local repo modules
import pedigree_lib.layout as layout


#============================================
def render_html(diagram: layout.Diagram, observations: dict, affected_color: str = '#111') -> str:
	"""Render a text-scaled diagram with local scrolling when space is limited.

	Args:
		diagram: Shared layout geometry; this renderer does not arrange people.
		observations: Visible observations keyed by person ID.
		affected_color: Fill color for affected symbols and carrier half-fills.

	Returns:
		HTML with one thin gray drawing frame and escaped labels.

	Raises:
		ValueError: Geometry fails the readability gate.
	"""
	errors = layout.layout_errors(diagram)
	if errors:
		raise ValueError('; '.join(errors))
	width, height = diagram.width, diagram.height
	# Preserve the 75% base size at 16 px text, then follow the question's font size.
	display_width = width * layout.DISPLAY_SCALE / 16
	# Two CSS pixels are 1.5 pt; unlike 1 pt borders, browsers do not round below 1 pt.
	result = '<div role="region" aria-label="Scrollable family pedigree" tabindex="0" '
	result += 'style="max-width: 100%; overflow-x: auto; margin: 0.75em 0;">'
	# Material wraps unclassed tables in a scrolling container; this is a drawing.
	result += '<table class="pedigree-diagram" role="presentation" cellpadding="0" cellspacing="0" style="'
	result += 'display: table; table-layout: fixed; border-collapse: collapse; border-spacing: 0; '
	result += 'border: 2px solid #aaa; box-sizing: border-box; background: #fff; padding: 0; margin: 0; '
	result += 'font-size: inherit; '
	result += f'width: {display_width:g}em; max-width: none; min-width: 0;">'
	result += '<tr><td style="border: 0; background: #fff; padding: 0; margin: 0; '
	result += 'font-size: 0; line-height: 0; vertical-align: top;">'
	result += '<div role="img" aria-label="Family pedigree" style="position: relative; '
	# Percent coordinates preserve the shared geometry as the text-scaled table grows.
	result += f'width: 100%; aspect-ratio: {width:g} / {height:g}; '
	result += 'container-type: inline-size; color: #111; background: #fff;">'
	for line in diagram.segments:
		left, top = min(line.x1, line.x2), min(line.y1, line.y2)
		w, h = abs(line.x2 - line.x1), abs(line.y2 - line.y1)
		result += '<span style="display: block; position: absolute; box-sizing: border-box; '
		result += f'left: {100 * left / width:g}%; top: {100 * top / height:g}%; '
		# Keep physical stroke thickness while only lengths follow responsive scaling.
		if w == 0:
			result += f'width: 2px; height: {100 * h / height:g}%; transform: translateX(-50%); '
		else:
			result += f'width: {100 * w / width:g}%; height: 2px; transform: translateY(-50%); '
		result += 'background: #111; font-size: 0; line-height: 0;">&#160;</span>'
	for person in diagram.symbols:
		obs = observations[person.person]
		fill = affected_color if obs.affected else '#fff'
		if obs.carrier:
			fill = f'linear-gradient(to right, {affected_color} 50%, #fff 50%)'
		radius = '50%' if person.sex == 'female' else '0'
		result += '<span style="display: block; position: absolute; box-sizing: border-box; '
		result += f'left: {100 * (person.x - layout.RADIUS) / width:g}%; '
		result += f'top: {100 * (person.y - layout.RADIUS) / height:g}%; '
		result += f'width: {3200 / width:g}%; height: {3200 / height:g}%; '
		result += 'border: 2px solid #111; '
		result += f'border-radius: {radius}; '
		result += f'background: {fill}; font-size: 0; line-height: 0;">&#160;</span>'
		if obs.affected is None:
			result += _text(person.x, person.y - 10, '?', 20, width, height)
		if person.label:
			result += _text(person.x, person.y + 20, person.label, 14, width, height)
	result += '</div></td></tr></table></div>'
	return result


#============================================
def _text(x: float, y: float, text: str, size: int, width: float, height: float) -> str:
	# ASVS 1.2.1: escape authored text at the HTML output boundary.
	escaped = html.escape(text).encode('ascii', 'xmlcharrefreplace').decode('ascii')
	result = '<span style="display: block; position: absolute; '
	result += f'left: {100 * x / width:g}%; top: {100 * y / height:g}%; '
	result += 'transform: translateX(-50%); white-space: nowrap; '
	result += f'color: #111; font: {100 * size / width:g}cqi/1.4 monospace;">'
	result += escaped + '</span>'
	return result
