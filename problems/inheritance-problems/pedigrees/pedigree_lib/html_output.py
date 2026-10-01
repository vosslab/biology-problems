"""Positioned HTML from shared geometry; one borderless rasterization container."""

# Standard Library
import html

# local repo modules
import pedigree_lib.layout as layout


#============================================
def render_html(diagram: layout.Diagram, observations: dict) -> str:
	"""Render a proportional diagram that fits its available width without scrolling.

	Args:
		diagram: Shared layout geometry; this renderer does not arrange people.
		observations: Visible observations keyed by person ID.

	Returns:
		HTML with one borderless drawing table and escaped labels.

	Raises:
		ValueError: Geometry fails the readability gate.
	"""
	errors = layout.layout_errors(diagram)
	if errors:
		raise ValueError('; '.join(errors))
	width, height = diagram.width, diagram.height
	result = f'<div style="width: {width:g}px; max-width: 100%; margin: 12px 0;">'
	# Material wraps unclassed tables in a scrolling container; this is a drawing.
	result += '<table class="pedigree-diagram" role="presentation" cellpadding="0" cellspacing="0" style="'
	result += 'display: table; table-layout: fixed; border-collapse: collapse; border-spacing: 0; '
	result += 'border: 0; background: #fff; padding: 0; margin: 0; '
	result += f'width: {width:g}px; max-width: 100%; min-width: 0;">'
	result += '<tr><td style="border: 0; background: #fff; padding: 0; margin: 0; '
	result += 'font-size: 0; line-height: 0; vertical-align: top;">'
	result += '<div role="img" aria-label="Family pedigree" style="position: relative; '
	# Percent coordinates preserve the shared geometry as the container narrows.
	result += f'width: 100%; aspect-ratio: {width:g} / {height:g}; '
	result += 'container-type: inline-size; color: #111; background: #fff;">'
	for line in diagram.segments:
		left, top = min(line.x1, line.x2), min(line.y1, line.y2)
		w, h = abs(line.x2 - line.x1), abs(line.y2 - line.y1)
		result += '<span style="display: block; position: absolute; box-sizing: border-box; '
		result += f'left: {100 * (left - (1 if w == 0 else 0)) / width:g}%; '
		result += f'top: {100 * (top - (1 if h == 0 else 0)) / height:g}%; '
		result += f'width: {100 * max(w, 2) / width:g}%; height: {100 * max(h, 2) / height:g}%; '
		result += 'background: #111; font-size: 0; line-height: 0;">&#160;</span>'
	for person in diagram.symbols:
		obs = observations[person.person]
		fill = '#111' if obs.affected else '#fff'
		if obs.carrier:
			fill = 'linear-gradient(to right, #111 50%, #fff 50%)'
		radius = '50%' if person.sex == 'female' else '0'
		result += '<span style="display: block; position: absolute; box-sizing: border-box; '
		result += f'left: {100 * (person.x - layout.RADIUS) / width:g}%; '
		result += f'top: {100 * (person.y - layout.RADIUS) / height:g}%; '
		result += f'width: {3200 / width:g}%; height: {3200 / height:g}%; '
		result += f'border: min(2px, calc(200cqi / {width:g})) solid #111; '
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
	result += f'color: #111; font: min({size}px, {100 * size / width:g}cqi)/1.4 monospace;">'
	result += escaped + '</span>'
	return result
