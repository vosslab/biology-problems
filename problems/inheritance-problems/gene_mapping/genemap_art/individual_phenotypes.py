"""Approved single-phenotype fly portraits with question-specific gene colors."""

import copy

import lxml.etree

import genemap_art.phenotype_art as phenotype_art


# Study accents repeat across unrelated portraits; question colors are supplied per gene.
STUDY_COLORS = {
	'a': '#C80085', 'b': '#935D00', 'c': '#00775F', 'd': '#007576',
	'e': '#A719DB', 'f': '#D40000', 'g': '#3B7600', 'h': '#B74300',
	'i': '#076DAD', 'j': '#C80085', 'k': '#A719DB', 'l': '#007A00',
	'm': '#CC0066', 'n': '#007A00', 'o': '#3B7600', 'p': '#003FFF',
	'q': '#935D00', 'r': '#B74300', 's': '#D40000', 't': '#A719DB',
	'u': '#6C6C00', 'v': '#0067CC', 'w': '#00775F', 'x': '#6C6C00',
	'y': '#3B7600', 'z': '#076DAD',
}
SVG_NS = 'http://www.w3.org/2000/svg'


def fragment(markup: str):
	"""Parse an authored SVG group for insertion into the editable drawing."""
	return lxml.etree.fromstring(('<g xmlns="' + SVG_NS + '">' + markup + '</g>').encode())


def color_character(root: lxml.etree._Element, trait: str, accent: str) -> str:
	"""Color selected phenotype surfaces while retaining neutral anatomy and materials."""
	channels = [int(accent[index:index + 2], 16) for index in (1, 3, 5)]
	shades = []
	for weight in (.2, .45, .7):
		shades.append('#' + ''.join(f'{round(c * weight + 255 * (1 - weight)):02X}' for c in channels))
	pale, light, middle = shades
	materials = {
		'artsy': {'#F0D8FA': light, '#D9F3D9': pale},
		'bumpy': {'#E9B65F': middle, '#FFF1CC': pale},
		'chummy': {'#FF8FA8': middle},
		'dewy': {}, 'eery': {'#F0D8FA': pale, '#D7C4DA': light},
		'fuzzy': {}, 'nerdy': {}, 'prickly': {}, 'tipsy': {},
		'gooey': {'#B3D66F': middle, '#D9F3D9': pale, '#F4FFD6': pale},
		'horsey': {'#935D00': accent},
		'icy': {'#C9EBFF': light},
		'jerky': {}, 'kidney': {'#DDB7ED': light, '#F7E6FF': '#FFF1CC'},
		'leafy': {'#B8E5B8': light, '#3B7600': accent},
		'mushy': {'#F0B5D0': light},
		'okra': {'#CBE59B': light},
		'quacky': {},
		'rusty': {},
		'spicy': {},
		'ugly': {'#AAA696': light},
		'valley': {'#F0D5A4': light},
		'waxy': {},
		'xanthic': {'#AAA': middle, '#555': accent},
		'yucky': {'#D6D99D': light, '#6D7346': accent},
		'zippy': {},
	}
	colors = materials[trait]
	for node in root.iter():
		for attribute in ('fill', 'stroke'):
			value = node.get(attribute)
			if value in colors:
				node.set(attribute, colors[value])
	# Select anatomical regions explicitly; the same skin color also appears on the face.
	if trait in {'chummy', 'dewy', 'eery', 'horsey', 'jerky', 'tipsy', 'zippy'}:
		for body in root.findall('.//*[@class="body"]'):
			body[0].set('fill', light)
			if trait == 'horsey':
				body[1].set('fill', pale)
	if trait in {'nerdy', 'rusty', 'xanthic'}:
		root.find('.//*[@class="thorax"]').set('fill', middle)
	for wings in root.findall('.//*[@class="wings"]'):
		wings.set('fill', light)
		wings.set('stroke', accent)
	if trait == 'bumpy':
		# Keep a few warm bumps as material contrast within the colored texture.
		for bump in root.findall('.//*[@class="bumpy"]/{' + SVG_NS + '}circle')[::3]:
			bump.set('fill', '#E9B65F')
	if trait == 'fuzzy':
		root.find('.//*[@class="fuzzy"]')[0].set('fill', '#FFF1DB')
	if trait == 'quacky':
		root.find('.//*[@class="face"]')[0].set('fill', '#FFDE48')
	root.set('data-gene-color', accent)
	return lxml.etree.tostring(root, encoding='unicode')


def fly_portrait(trait: str, size: int = 72, color: str = None) -> str:
	"""Draw one named phenotype with a selective gene-color treatment."""
	gene = trait[0]
	accent = STUDY_COLORS[gene] if color is None else color
	channels = [int(accent[index:index + 2], 16) for index in (1, 3, 5)]
	light = '#' + ''.join(f'{round(channel * .45 + 255 * .55):02X}' for channel in channels)
	known = {trait} if trait in phenotype_art.TRAIT_GENES else set()
	root = lxml.etree.fromstring(phenotype_art.plush_fly(known, trait, size, {gene: accent}).encode())
	root.set('data-phenotype', trait)
	root.find('{' + SVG_NS + '}desc').text = 'Playful single-trait illustration: ' + trait + '. Props and scenes are visual metaphors; the adjacent gene description defines the phenotype.'
	if known:
		return color_character(root, trait, accent)
	main = root.find('{' + SVG_NS + '}g')
	body = main.find('.//*[@class="body"]')
	wings = main.find('.//*[@class="wings"]')
	legs = main.find('.//*[@class="legs"]')
	face = main.find('.//*[@class="face"]')
	thorax = main.find('.//*[@class="thorax"]')
	art = ''
	if trait == 'artsy':
		wings.clear()
		wings.extend(fragment(f'<g stroke="{accent}" stroke-width="2"><path fill="#F0D8FA" d="M94 59 C47 57 21 11 42 5 C71 -3 98 23 101 52Z"/><path fill="#D9F3D9" d="M98 55 C106 14 148 -2 166 9 C182 33 148 65 98 55Z"/><path fill="#FF8F8F" d="M36 15 Q55 9 71 22 L64 45 Q46 37 36 15Z"/><path fill="#8FABFF" d="M122 20 L156 11 L151 41 L112 49Z"/><path fill="#FFDF70" d="M72 25 L88 35 L96 52 L70 44Z"/><circle fill="#C80085" cx="137" cy="28" r="7"/><path fill="none" stroke="#FFF" stroke-width="4" d="M46 19 L58 32 M120 37 L143 17"/></g>'))
		art = f'<path fill="{accent}" d="M28 39 Q25 25 44 24 Q62 23 65 39Z"/><path fill="none" stroke="#493215" stroke-width="3" d="M30 40 H68 M45 25 L47 20"/>'
	elif trait == 'bumpy':
		for x, y, radius in ((73, 46, 9), (91, 42, 10), (112, 43, 10), (132, 50, 10), (144, 68, 10), (140, 86, 10), (122, 96, 10), (101, 94, 9), (80, 91, 9), (65, 77, 8), (71, 63, 10), (91, 62, 10), (114, 62, 10), (128, 79, 10), (105, 80, 10), (86, 80, 8)):
			art += f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#E9B65F"/><path fill="none" stroke="#FFF1CC" stroke-width="3" d="M{x - 4} {y - 1} q0 -5 5 -5"/>'
	elif trait == 'chummy':
		main.set('transform', 'translate(0 35) scale(.62)')
		friend = copy.deepcopy(main)
		friend.set('transform', 'translate(72 21) scale(.62)')
		root.append(friend)
		art = f'<path fill="#FF8FA8" stroke="{accent}" d="M89 43 C47 23 63 -2 84 12 L89 17 C111 -7 137 17 89 43Z"/><path fill="none" stroke="#FFF" stroke-width="4" d="M70 17 Q67 24 74 28"/><path fill="none" stroke-width="4" d="M77 90 Q92 103 101 87"/>'
	elif trait == 'dewy':
		for x, y, scale in ((73, 54, .65), (93, 51, .7), (119, 55, .9), (139, 69, .65), (74, 78, .7), (96, 76, .8), (121, 82, .75), (104, 96, .6), (52, 72, .45)):
			art += f'<g transform="translate({x} {y}) scale({scale})"><path fill="#BFEFF6" d="M0 -13 C-2 -5 -10 1 -7 7 C-4 15 9 11 8 4 C8 -2 1 -7 0 -13Z"/><path fill="none" stroke="#FFF" stroke-width="3" d="M-3 1 Q-6 6 -2 7"/></g>'
	elif trait == 'eery':
		legs.clear()
		legs.extend(fragment('<path fill="none" stroke="#493215" stroke-width="6" d="M76 77 C39 78 40 111 57 110 C73 109 65 91 56 99 M98 80 L89 100 L111 95 L105 114 M119 77 C163 72 176 101 153 105 C135 109 137 90 150 93"/>'))
		wings.clear()
		wings.extend(fragment(f'<path fill="#F0D8FA" stroke="{accent}" d="M95 53 C58 55 53 21 73 24 C93 27 70 45 72 30 C54 11 88 7 96 53Z M104 51 C126 50 160 42 147 26 C134 13 125 34 138 35 C155 52 114 69 104 51Z"/>'))
		face[1].set('d', 'M43 48 C13 38 22 17 34 27 C47 40 15 43 18 25 M58 46 L68 29 L54 25 L63 13')
		thorax.set('fill', '#D7C4DA')
		art = f'<path fill="{accent}" d="M34 23 L37 5 L53 18 L61 22Z"/><circle fill="#FFF" stroke="none" cx="44" cy="17" r="2"/>'
	elif trait == 'gooey':
		art = '<ellipse fill="#D9F3D9" stroke="none" cx="116" cy="110" rx="40" ry="5"/><path fill="#B3D66F" d="M83 52 Q105 34 130 51 Q147 60 143 76 L144 101 Q140 115 135 101 L131 78 L124 97 Q117 106 114 94 L112 77 L103 87 Q95 93 94 80 L87 72Z"/><path stroke="#F4FFD6" stroke-width="4" fill="none" d="M96 53 Q111 44 124 54"/>'
	elif trait == 'horsey':
		body.clear()
		body.extend(fragment('<path fill="#B87745" d="M73 47 C98 37 146 36 153 61 L155 85 Q139 101 105 91 L75 88Z"/><path fill="#EAC28E" stroke="none" d="M92 47 Q121 41 140 49 L134 63 L97 64Z"/>'))
		thorax.set('rx', '24')
		thorax.set('ry', '29')
		thorax.set('fill', '#B87745')
		legs.clear()
		legs.extend(fragment('<path fill="#B87745" d="M75 80 L86 81 L81 107 L67 107Z M124 81 L139 79 L147 107 L132 107Z"/><path fill="#493215" d="M64 103 H82 V113 H62Z M131 103 H149 L154 113 H130Z"/>'))
		face.clear()
		face.extend(fragment('<path fill="#B87745" d="M77 50 L68 25 L57 38 L40 38 L27 64 Q17 82 34 88 L56 83 L71 67Z"/><path fill="#EAC28E" d="M28 63 Q44 57 51 74 L40 88 Q17 93 23 74Z"/><circle fill="#493215" cx="49" cy="49" r="5"/><circle fill="#493215" stroke="none" cx="29" cy="76" r="2.5"/><path fill="#493215" d="M72 38 L82 41 L77 47 L87 53 L78 57 L86 65 L76 71Z"/>'))
		art = f'<path fill="#935D00" stroke="#493215" d="M35 30 Q44 23 43 11 Q56 16 68 10 L73 28 Q89 22 88 30 Q63 42 30 35Z"/><path fill="none" stroke="{accent}" stroke-width="5" d="M43 28 Q58 32 73 26"/><path fill="none" stroke="#704020" stroke-width="3" d="M77 58 Q92 55 91 76 M126 68 Q145 58 147 79"/>'
	elif trait == 'icy':
		body[0].set('fill', '#DCEEFF')
		body[1].set('stroke', '#76A9CF')
		art = '<path fill="#C9EBFF" d="M78 58 L84 39 L93 49 L103 33 L112 48 L127 37 L133 57 L143 66 L131 70 L125 58 L113 64 L103 54 L89 64Z"/><g fill="none" stroke-width="2.5"><path d="M155 20 L155 46 M144 26 L166 40 M144 40 L166 26 M151 22 L155 27 L159 22 M151 44 L155 39 L159 44"/></g>'
	elif trait == 'jerky':
		legs.clear()
		for x in (70, 131):
			legs.extend(fragment(f'<g fill="none" stroke="{accent}" stroke-width="3"><path stroke-opacity=".35" d="M{x - 10} 83 C{x - 10} 77 {x + 10} 77 {x + 10} 83 M{x - 10} 92 C{x - 10} 86 {x + 10} 86 {x + 10} 92 M{x - 10} 101 C{x - 10} 95 {x + 10} 95 {x + 10} 101"/><path d="M{x + 3} 76 L{x + 10} 83 C{x + 10} 90 {x - 10} 84 {x - 10} 90 C{x - 10} 97 {x + 10} 91 {x + 10} 97 C{x + 10} 104 {x - 10} 98 {x - 10} 104 Q{x - 10} 110 {x + 3} 110"/></g>'))
		legs.extend(fragment('<path fill="#493215" d="M56 109 H80 V115 H53Z M119 109 H144 L147 115 H119Z"/>'))
		body.set('transform', 'rotate(-15 90 70)')
		art = f'<path fill="#FFF8DA" d="M144 69 L157 54 L172 68 L159 82Z"/><path fill="none" stroke="{accent}" stroke-width="3" d="M155 63 V73 M163 63 V73"/><path fill="none" stroke-width="4" d="M25 97 L12 81 L22 72 L10 57 M9 57 L9 67 M9 57 L20 57"/>'
	elif trait == 'kidney':
		body.clear()
		main.remove(thorax)
		body.extend(fragment(f'<path fill="#DDB7ED" stroke="{accent}" d="M62 61 C57 30 110 28 142 45 C174 62 150 108 121 103 C91 100 119 76 99 72 C80 68 69 84 62 61Z"/><path fill="none" stroke="#F7E6FF" stroke-width="5" d="M74 52 Q94 36 120 46"/><path fill="none" stroke="{accent}" stroke-width="4" d="M120 87 Q138 96 146 74"/>'))
	elif trait == 'leafy':
		wings.clear()
		wings.extend(fragment('<g stroke="#3B7600" fill="#B8E5B8"><path d="M96 54 C48 55 31 26 32 4 C64 8 100 15 96 54Z"/><path d="M98 54 C100 15 142 2 169 5 C166 38 134 64 98 54Z"/><path fill="none" stroke-width="2" d="M96 54 L39 10 M68 32 L63 17 M68 32 L48 30 M98 54 L161 11 M130 33 L133 18 M130 33 L151 30"/></g>'))
		art = f'<path fill="none" stroke="{accent}" stroke-width="5" d="M65 83 Q78 94 87 79"/>'
	elif trait == 'mushy':
		wings.set('transform', 'translate(0 10)')
		body.clear()
		body.extend(fragment(f'<path fill="#F0B5D0" stroke="{accent}" d="M79 75 Q83 50 102 68 Q113 49 129 69 Q158 74 147 91 Q127 106 90 98 Q71 94 79 75Z"/><path fill="none" stroke="{accent}" d="M98 77 Q101 92 110 91 M124 77 Q126 88 137 88"/>'))
		face.set('transform', 'translate(0 10)')
		art = '<path fill="none" stroke-width="3" d="M90 105 Q118 113 147 104 M151 84 L161 90 L153 96"/>'
	elif trait == 'okra':
		body.clear()
		main.remove(thorax)
		body.extend(fragment('<path fill="#CBE59B" stroke="#3B7600" d="M64 51 C100 39 142 61 171 88 C127 100 91 91 64 81Z"/><path fill="none" stroke="#3B7600" stroke-width="2.5" d="M72 55 Q123 57 165 86 M72 66 Q119 73 165 86 M72 77 Q113 88 165 86"/>'))
		art = f'<path fill="none" stroke="{accent}" stroke-width="5" d="M67 51 L68 80"/>'
	elif trait == 'quacky':
		wings.set('transform', 'translate(0 13)')
		body.clear()
		main.remove(thorax)
		body.extend(fragment(f'<path fill="{light}" d="M57 58 Q85 61 102 73 Q134 77 152 55 Q166 101 114 102 Q64 108 57 78Z"/><path fill="{accent}" d="M85 76 Q103 64 125 79 Q109 98 90 91Z"/>'))
		face.clear()
		face.extend(fragment(f'<path fill="{light}" d="M75 61 Q73 91 47 79 Q23 68 34 44 Q42 25 62 36 Q78 40 75 61Z"/><path fill="#F29224" d="M35 58 L11 62 Q6 71 35 71Z"/><circle fill="#493215" cx="46" cy="51" r="5"/><circle fill="#FFF" stroke="none" cx="44" cy="49" r="1.5"/><path fill="none" d="M56 34 L61 24 L70 27"/>'))
		art = f'<path fill="{accent}" d="M34 34 L36 20 Q53 10 70 22 L70 34Z"/><path fill="#FFF" stroke="none" d="M47 21 H57 V31 H47Z"/><path fill="none" stroke="#493215" d="M29 35 H74"/>'
	elif trait == 'rusty':
		for node in main.iter():
			if node.get('fill') in ('#F3CC75', '#E9B65F'):
				node.set('fill', '#B76539')
		art = '<path fill="#73452B" stroke="none" d="M89 57 L100 54 L105 65 L95 70Z M119 76 L131 71 L136 82 L125 87Z"/><g fill="#D88A51" stroke="none"><circle cx="111" cy="54" r="3"/><circle cx="107" cy="81" r="4"/></g>'
	elif trait == 'spicy':
		body.clear()
		main.remove(thorax)
		body.extend(fragment(f'<path fill="{accent}" stroke="#493215" d="M65 51 C98 38 131 55 129 78 Q146 97 171 72 Q162 114 117 102 Q81 97 65 78Z"/><path fill="none" stroke="{light}" stroke-width="6" d="M80 55 Q104 49 116 66"/><path fill="#3B7600" stroke="#284E00" d="M63 49 L85 45 L80 55 L89 62 L74 64 L72 79 L62 73Z"/>'))
		art = f'<path fill="{accent}" stroke="#493215" d="M25 35 Q21 25 30 24 Q30 10 43 14 Q53 4 61 17 Q77 17 70 33Z"/><path fill="#FFF" stroke="none" d="M28 33 H70 V40 H28Z"/><path fill="none" stroke="#B74300" stroke-width="3" d="M151 55 Q163 45 154 35 Q146 26 156 16"/>'
	elif trait == 'ugly':
		for node in main.iter():
			if node.get('fill') in ('#F3CC75', '#E9B65F'):
				node.set('fill', '#ACA88B')
		body.clear()
		body.extend(fragment('<path fill="#AAA696" d="M80 54 L106 45 L112 58 L140 55 L135 74 L150 88 L122 98 L111 83 L93 93 L82 75Z"/>'))
		wings[0].set('d', 'M91 64 C54 29 57 10 72 10 C94 13 104 39 96 63Z')
		wings[1].set('d', 'M100 49 L112 39 L117 50Z')
		face[2].set('rx', '10')
		face[2].set('ry', '13')
		art = '<circle fill="#FFF" cx="65" cy="64" r="5"/><circle fill="#493215" stroke="none" cx="66" cy="65" r="2"/><path fill="#FFF" stroke="#493215" stroke-width="1.5" d="M47 79 L49 87 L55 79 L59 85 L62 77"/>'
	elif trait == 'valley':
		body.clear()
		main.remove(thorax)
		for x in (77, 89, 101, 113, 125):
			body.extend(fragment(f'<path fill="#F0D5A4" stroke="#493215" stroke-width="1.5" d="M{x} 55 l6 -12 l6 12 v34 l-6 12 l-6 -12Z"/><path fill="#715038" stroke="none" d="M{x + 6} 43 l6 12 v34 l-6 12Z"/><path fill="none" stroke="#FFF8DA" stroke-width="2" d="M{x + 2} 56 l3 -7 v45"/>'))
		body.extend(fragment(f'<path fill="{accent}" stroke="#493215" d="M63 50 L76 47 V96 L63 92Z M138 47 L151 53 V93 L138 98Z"/><path fill="#FFF8DA" stroke="#493215" stroke-width="1" d="M65 56 H73 V86 H65Z"/><path fill="none" stroke="#493215" stroke-width="2" d="M68 62 H74 M68 69 H74 M68 76 H74 M68 83 H74"/><g fill="#FFF8DA" stroke="none"><circle cx="144" cy="64" r="2"/><circle cx="144" cy="74" r="2"/><circle cx="144" cy="84" r="2"/></g>'))
	elif trait == 'waxy':
		art = '<path fill="#F7F2C9" stroke-width="4" d="M61 54 Q77 42 91 49 Q114 37 134 53 Q150 68 137 91 Q116 107 90 94 Q68 96 62 81Z"/><path fill="none" stroke="#FFF" stroke-width="7" d="M72 56 Q80 50 91 55 M100 53 Q115 48 129 58"/><path fill="none" stroke-width="2" d="M73 81 Q100 103 132 83"/><path fill="#BFEFF6" d="M151 28 Q138 43 151 47 Q165 44 151 28Z"/><path fill="none" d="M149 51 Q156 60 168 56"/>'
	elif trait == 'xanthic':
		for node in main.iter():
			if node.get('fill') in ('#F3CC75', '#E9B65F'):
				node.set('fill', '#FFFF00')
		body.clear()
		body.extend(fragment('<path fill="#FFF47A" stroke="#B18B00" d="M89 55 C100 54 106 40 123 40 C161 38 169 92 134 102 C112 110 103 89 89 87Z"/><path fill="none" stroke="#B74300" stroke-width="2.5" d="M94 63 L120 59 L123 64 L127 58 L131 64 L135 59 L139 65 L136 78 L132 73 L128 79 L124 73 L120 78 L94 80"/><path fill="none" stroke="#FFF" stroke-width="5" d="M114 48 Q135 42 146 58"/>'))
		socket = fragment('<path fill="#AAA" stroke="#493215" stroke-width="2" d="M62 57 Q57 70 62 83 H98 Q103 70 98 57Z"/><path fill="none" stroke="#FFF" stroke-width="2.5" d="M66 60 H94"/><path fill="none" stroke="#555" stroke-width="3" d="M66 57 Q73 70 66 83 M74 57 Q81 70 74 83 M82 57 Q89 70 82 83 M90 57 Q97 70 90 83"/><path fill="none" stroke="#493215" stroke-width="2" d="M98 57 Q103 70 98 83"/>')
		socket.set('class', 'thorax')
		main.replace(thorax, socket)
		art = '<g fill="none" stroke="#C6B800" stroke-width="3"><path d="M151 38 L158 30 M162 59 L173 56 M162 83 L172 89 M135 109 L139 117 M115 32 L113 24"/></g>'
	elif trait == 'yucky':
		body[0].set('fill', '#A7B379')
		thorax.set('fill', '#A7B379')
		art = '<path fill="#D6D99D" stroke="#6D7346" stroke-width="2" opacity=".8" d="M130 71 Q155 75 151 60 Q175 56 161 40 Q177 23 158 19 Q160 2 143 9 Q127 0 123 19 Q107 25 121 40 Q111 54 132 54Z"/><g fill="none" stroke="#6D7346" stroke-width="3"><path d="M137 58 Q151 48 136 39 Q127 30 140 21 M153 36 Q162 27 152 20"/></g><path fill="#6D7346" stroke="none" d="M70 64 L83 56 L91 69 L79 77Z M105 78 L123 71 L134 83 L117 91Z"/>'
	elif trait == 'zippy':
		body.clear()
		main.remove(thorax)
		legs.clear()
		body.extend(fragment(f'<path fill="#DCE6FF" stroke="#493215" d="M59 68 Q82 38 132 51 L143 70 L131 89 Q82 100 59 68Z"/><path fill="{accent}" d="M101 49 L124 32 L129 51Z M100 91 L124 109 L130 88Z"/><path fill="#555" d="M133 53 H143 V87 H133Z"/><path fill="#FF9E2C" stroke="#B74300" d="M145 57 L175 48 L162 68 L176 84 L145 81Z"/><path fill="#FFF0A0" stroke="none" d="M145 64 L166 60 L156 70 L166 76 L145 74Z"/>'))
		art = f'<path fill="{accent}" stroke="#493215" d="M29 51 Q28 26 52 29 Q74 29 76 54 L64 58 Q63 43 49 43 Q38 43 35 56Z"/><path fill="#DCEEFF" stroke="#493215" d="M30 52 Q43 43 62 49 L59 65 Q39 68 29 61Z"/><path fill="none" stroke="#FFF" stroke-width="3" d="M37 52 L47 50"/>'
	else:
		raise ValueError(f'unknown portrait phenotype: {trait}')
	for node, name in ((body, 'body'), (wings, 'wings'), (legs, 'legs'), (face, 'face')):
		node.set('class', name)
	feature = fragment(art)
	feature.set('class', trait)
	feature.set('data-gene', gene)
	feature.set('stroke', accent)
	feature.set('stroke-width', '2.5')
	feature.set('stroke-linecap', 'round')
	feature.set('stroke-linejoin', 'round')
	root.append(feature)
	return color_character(root, trait, accent)

