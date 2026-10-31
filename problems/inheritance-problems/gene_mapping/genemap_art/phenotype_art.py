"""Shared side-view geometry for gene-mapping fly portraits.

Original phenotype character artwork: CC BY-SA 4.0.
https://creativecommons.org/licenses/by-sa/4.0/
"""

import html


GENE_COLORS = {'f': '#D40000', 'n': '#007A00', 'p': '#003FFF', 't': '#A719DB'}
TRAIT_GENES = {'fuzzy': 'f', 'nerdy': 'n', 'prickly': 'p', 'tipsy': 't'}


def plush_fly(traits: set, label: str, size: int = 54, gene_colors: dict = None) -> str:
	"""Give each expressed recessive trait its own colored, independent feature."""
	if not traits <= TRAIT_GENES.keys():
		raise ValueError(f'unknown illustration traits: {traits - TRAIT_GENES.keys()}')
	colors = GENE_COLORS if gene_colors is None else gene_colors
	svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{round(size * 1.5)}" height="{size}" viewBox="0 0 180 120" role="img" aria-label="{html.escape(label)}">'
	svg += '<desc>Exaggerated storybook fly. Curly fur, sharp spines, thick rectangular glasses with a taped bridge, and a foaming beer mug represent hypothetical traits.</desc>'
	svg += '<g stroke="#493215" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
	svg += '<g data-part="legs" fill="none"><path stroke="#9A8055" d="M79 76 L70 94 L58 94 M98 78 L105 96 L114 96 M119 75 L135 92 L145 92"/>'
	svg += '<path d="M77 79 L66 101 L51 102 M97 83 L95 105 L109 105 M115 81 L129 103 L146 103"/></g>'
	svg += '<g data-part="wings" fill="#DCE6FF" stroke="#607882" stroke-width="2"><path d="M92 60 C62 30 60 13 75 13 C94 14 103 35 101 58Z"/>'
	svg += '<path d="M96 59 C108 17 129 10 136 23 C140 38 118 58 96 61Z"/></g>'
	if 'prickly' in traits:
		svg += f'<g data-part="prickly" data-gene="p" fill="{colors["p"]}" fill-opacity=".45" stroke="{colors["p"]}" stroke-width="2"><path d="M82 51 L76 22 L97 47 L104 15 L115 45 L138 22 L132 55 L162 48 L139 68 L162 84 L135 84 L140 110 L118 91 L108 115 L97 91 L77 109 L83 82 L62 82 L78 67 L61 45Z"/></g>'
	fur = ''
	if 'fuzzy' in traits:
		channels = [int(colors['f'][index:index + 2], 16) for index in (1, 3, 5)]
		fur_fill = '#' + ''.join(f'{round(channel * .16 + 255 * .84):02X}' for channel in channels)
		fur = f'<g data-part="fuzzy" data-gene="f" stroke="{colors["f"]}"><path fill="{fur_fill}" fill-opacity=".62" stroke-width="2" d="M66 47 C60 35 77 29 86 36 C95 22 111 28 117 39 C132 30 145 42 138 53 C153 56 151 70 141 74 C153 85 141 98 130 93 C126 109 109 109 104 98 C94 110 80 102 82 92 C66 99 54 86 63 75 C48 66 51 48 66 47Z"/>'
		fur += '<path fill="none" stroke-opacity=".8" stroke-width="2.4" d="M66 56 q-6 8 4 11 M86 45 q-8 7 0 14 M112 49 q10 3 5 12 M83 75 q-11 2 -6 12 M104 75 q9 10 -1 14 M130 66 q-8 5 -2 12"/></g>'
	if 'prickly' in traits:
		# Spine roots remain behind the body; tips project beyond its contour.
		svg += f'<g data-part="bristle-tips" data-gene="p" fill="{colors["p"]}" fill-opacity=".45" stroke="{colors["p"]}" stroke-width="2"><path d="M135 53 L169 41 L143 66Z M142 68 L174 75 L140 82Z M133 85 L160 107 L125 97Z"/></g>'
	svg += '<g data-part="body"><ellipse fill="#F3CC75" cx="107" cy="70" rx="31" ry="24"/>'
	svg += '<path fill="none" stroke="#935D00" stroke-width="5" d="M107 48 Q121 70 110 92 M123 53 Q134 70 126 86"/></g>'
	svg += '<ellipse data-part="thorax" fill="#E9B65F" cx="77" cy="68" rx="16" ry="19"/>'
	svg += fur
	svg += '<g data-part="face"><path fill="#F3CC75" d="M68 53 C58 40 38 44 33 58 C28 73 41 87 57 81 C71 78 77 63 68 53Z"/>'
	svg += '<path fill="none" d="M43 48 L37 36 L29 36 M58 46 L64 34 L71 34"/>'
	if 'nerdy' in traits:
		svg += f'<g data-part="nerdy" data-gene="n" stroke="{colors["n"]}" stroke-width="4.5">'
		svg += '<path fill="none" d="M47 55 H55 M79 51 L86 56"/>'
		svg += '<rect fill="#FFF" x="23" y="46" width="24" height="22" rx="3"/>'
		svg += '<rect fill="#FFF" x="55" y="46" width="24" height="22" rx="3"/>'
		svg += '<g fill="#493215" stroke="none"><ellipse cx="35" cy="58" rx="3" ry="5"/><ellipse cx="67" cy="58" rx="3" ry="5"/></g>'
		svg += '<path stroke="#FFF8E5" stroke-width="6" d="M48 55 H54"/><path stroke="#493215" stroke-width="1" d="M50 52 L52 58"/></g>'
		svg += f'<g data-part="bow-tie" fill="{colors["n"]}" stroke-width="1.5"><path d="M64 83 L53 77 V91Z M64 83 L75 77 V91Z"/><circle cx="64" cy="84" r="3"/></g>'

	else:
		svg += '<ellipse fill="#493215" cx="46" cy="60" rx="7" ry="10"/><ellipse fill="#FFF" stroke="none" cx="44" cy="57" rx="2.5" ry="3"/>'
	svg += '<path fill="none" stroke-width="2" d="M45 76 Q53 81 59 74"/></g></g>'
	if 'tipsy' in traits:
		# The mug occupies the open space below the head, clear of fur and spines.
		svg += f'<g data-part="tipsy" data-gene="t" stroke="{colors["t"]}" stroke-width="3.5" stroke-linejoin="round">'
		svg += '<path fill="none" stroke="#493215" d="M70 80 Q60 94 39 91"/>'
		svg += '<path fill="none" d="M32 88 L42 88 Q50 100 33 102"/>'
		svg += f'<path fill="{colors["t"]}" d="M9 83 L35 83 L33 110 Q21 114 11 109Z"/>'
		svg += '<path stroke="#F0D8FA" stroke-width="3" d="M16 91 L17 104 M25 91 L25 106"/>'
		svg += '<path fill="#FFF8E5" stroke-width="2" d="M9 87 C1 87 2 78 9 78 C6 68 20 69 22 77 C29 71 37 75 35 81 C43 83 37 91 31 87 C24 93 17 84 9 87Z"/>'
		svg += '</g>'
	svg += '</svg>'
	return svg
