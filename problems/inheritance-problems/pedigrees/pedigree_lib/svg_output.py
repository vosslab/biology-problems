"""Editable vector shapes and text from the same layout used by HTML."""

# Standard Library
import html

# local repo modules
import pedigree_lib.layout as layout


#============================================
def render_svg(diagram: layout.Diagram, observations: dict, affected_color: str = '#111') -> str:
	"""Render editable shapes and text from shared geometry.

	Args:
		diagram: Shared layout geometry; this renderer does not arrange people.
		observations: Visible observations keyed by person ID.
		affected_color: Fill color for affected symbols and carrier half-fills.

	Returns:
		SVG document with native shapes and escaped text.

	Raises:
		ValueError: Geometry fails the readability gate.
	"""
	errors = layout.layout_errors(diagram)
	if errors:
		raise ValueError('; '.join(errors))
	result = '<svg xmlns="http://www.w3.org/2000/svg" '
	result += f'width="{diagram.width * layout.DISPLAY_SCALE:g}" '
	result += f'height="{diagram.height * layout.DISPLAY_SCALE:g}" '
	result += f'viewBox="0 0 {diagram.width:g} {diagram.height:g}">'
	result += '<title>Family pedigree</title><rect width="100%" height="100%" fill="white"/>'
	for line in diagram.segments:
		result += f'<line x1="{line.x1:g}" y1="{line.y1:g}" x2="{line.x2:g}" '
		result += f'y2="{line.y2:g}" stroke="#111" stroke-width="2"/>'
	for person in diagram.symbols:
		obs = observations[person.person]
		x, y = person.x, person.y
		fill = affected_color if obs.affected else '#fff'
		if person.sex == 'female':
			result += f'<circle cx="{x:g}" cy="{y:g}" r="15" fill="{fill}" stroke="#111" stroke-width="2"/>'
			if obs.carrier:
				result += f'<path d="M {x:g} {y-14:g} A 14 14 0 0 0 {x:g} {y+14:g} Z" '
				result += f'fill="{affected_color}"/>'
		else:
			result += f'<rect x="{x-15:g}" y="{y-15:g}" width="30" height="30" '
			result += f'fill="{fill}" stroke="#111" stroke-width="2"/>'
			if obs.carrier:
				result += f'<rect x="{x-14:g}" y="{y-14:g}" width="14" height="28" '
				result += f'fill="{affected_color}"/>'
		if obs.affected is None:
			result += _text(x, y + 6, '?', 20)
		if person.label:
			result += _text(x, y + 35, person.label, 14)
	result += '</svg>'
	return result


#============================================
def _text(x: float, y: float, text: str, size: int) -> str:
	# ASVS 1.2.1: labels remain literal editable text, never XML markup.
	escaped = html.escape(text).encode('ascii', 'xmlcharrefreplace').decode('ascii')
	result = f'<text x="{x:g}" y="{y:g}" text-anchor="middle" '
	result += f'font-family="monospace" font-size="{size}" fill="#111">{escaped}</text>'
	return result
