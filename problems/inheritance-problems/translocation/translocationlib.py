import html

CHROMOSOME_LENGTHS = {
	1: (125, 124),
	2: (93, 149),
	3: (91, 107),
	4: (50, 140),
	5: (48, 133),
	6: (61, 110),
	7: (60, 99),
	8: (46, 101),
	9: (49, 92),
	10: (40, 95),
	11: (54, 81),
	12: (36, 98),
	13: (18, 97),
	14: (17, 90),
	15: (19, 84),
	16: (37, 54),
	17: (24, 57),
	18: (17, 61),
	19: (27, 33),
	20: (28, 36),
	21: (13, 35),
	22: (15, 37),
}

ACROCENTRIC_CHROMOSOMES = [13, 14, 15, 21, 22]

COLOR_SCALES = {
	'red': ['coral', '#ffe7de', 'crimson'],
	'blue': ['deepskyblue', '#e1f3fe', 'royalblue'],
}
CHROMOSOME_HEIGHT = 30
DEFAULT_CENTROMERE_WIDTH = 32
CENTROMERE_FILLS = {
	arm_color: shades[1]
	for shades in COLOR_SCALES.values()
	for arm_color in (shades[0], shades[2])
}

CHROMOSOME_TABLE_STYLE = (
	'border-collapse: separate; border-spacing: 0; border: 0; '
	f'height: {CHROMOSOME_HEIGHT}px; '
	'color: #000; background-color: #fff;'
)
CHROMOSOME_SHEEN = (
	'linear-gradient(to bottom, rgba(255, 255, 255, 0.25), '
	'rgba(255, 255, 255, 0) 45%, rgba(0, 0, 0, 0.16))'
)
CHROMOSOME_DEPTH_STYLE = (
	'box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.55), '
	'inset 0 -3px 0 rgba(0, 0, 0, 0.18);'
)
CHROMOSOME_ARM_STYLE = (
	f'background-image: {CHROMOSOME_SHEEN}, '
	'linear-gradient(95deg, transparent 0 5px, '
	'rgba(0, 0, 0, 0.09) 5px 7px, rgba(255, 255, 255, 0.08) 7px 8px, '
	'transparent 8px 18px, '
	'rgba(0, 0, 0, 0.09) 18px 21px, rgba(255, 255, 255, 0.08) 21px 22px, '
	'transparent 22px 29px, '
	'rgba(0, 0, 0, 0.09) 29px 30px, rgba(255, 255, 255, 0.08) 30px 31px, '
	'transparent 31px 46px, '
	'rgba(0, 0, 0, 0.09) 46px 48px, rgba(255, 255, 255, 0.08) 48px 49px, '
	'transparent 49px 59px, '
	'rgba(0, 0, 0, 0.09) 59px 62px, rgba(255, 255, 255, 0.08) 62px 63px, '
	'transparent 63px); '
	# Fixed tile geometry keeps the irregular pattern identical wherever an arm reappears.
	'background-size: 100% 100%, 79px 100%; background-position: 0 0; '
	'background-origin: border-box; '
	+ CHROMOSOME_DEPTH_STYLE
)
# Overlap the rod outline so the collar spans the chromosome's full height.
CENTROMERE_STYLE = (
	'display: block; box-sizing: border-box; '
	f'height: {CHROMOSOME_HEIGHT}px; line-height: {CHROMOSOME_HEIGHT - 4}px; margin: -2px 0; '
	'border: 2px solid #40474E; border-radius: 4px; text-align: center; '
	'color: #000; font-weight: bold; '
	f'background-image: {CHROMOSOME_SHEEN}; '
	+ CHROMOSOME_DEPTH_STYLE
)
ARM_EDGE_STYLES = {
	'left': 'border-right: 0; border-radius: 6px 0 0 6px;',
	'right': 'border-left: 0; border-radius: 0 6px 6px 0;',
	'middle': 'border-left: 0; border-right: 0;',
	'junction': 'border-left: 0; border-right: 0; position: relative;',
}


#======================================
def _draw_arm(color: str, edge: str, label: str = '', *,
		mark_junction: bool = False, textured: bool = True) -> str:
	"""Render a chromosome cell, with optional arm texture and exchange junction."""
	cell = f'<td style="background-color: {color}; border: 2px solid black; '
	cell += 'padding: 0; '
	if mark_junction:
		cell += 'position: relative; '
	cell += ARM_EDGE_STYLES[edge]
	if textured:
		cell += ' ' + CHROMOSOME_ARM_STYLE
	cell += '" align="center">'
	cell += '<span style="display: block; padding: 0 1px; font-size: small; '
	cell += 'color: #000; font-weight: bold; '
	cell += 'text-shadow: -0.5px 0 0 #fff, 0.5px 0 0 #fff, '
	cell += '0 -0.5px 0 #fff, 0 0.5px 0 #fff; '
	content = label if label else '<!-- -->'
	cell += f'line-height: {CHROMOSOME_HEIGHT - 4}px;">{content}</span>'
	if edge == 'junction' or mark_junction:
		cell += '<span aria-hidden="true" style="position: absolute; top: 0; bottom: 0; '
		cell += 'right: -3px; width: 6px; background-color: #fff; z-index: 1; '
		cell += 'pointer-events: none; clip-path: polygon(50% 0, 100% 16.667%, '
		cell += '50% 33.333%, 100% 50%, 50% 66.667%, 100% 83.333%, 50% 100%, '
		cell += '0 100%, 50% 83.333%, 0 66.667%, 50% 50%, 0 33.333%, '
		# Nonempty spans retain closing tags when exported markup is serialized as XML.
		cell += '50% 16.667%, 0 0);"><!-- --></span>'
	cell += '</td>'
	return cell


#======================================
def _draw_centromere(left_color: str, right_color: str, width: int,
		label: int | str = '') -> str:
	"""Render a full-height collar over joined arm colors, with an optional number."""
	fill_color = CENTROMERE_FILLS.get(left_color, '#e6eaf0')
	# Continue the chromosome behind the rounded collar so its corners reveal no white gaps.
	cell = '<td style="border: 0; border-top: 2px solid black; '
	cell += 'border-bottom: 2px solid black; padding: 0; '
	cell += f'background-color: {left_color}; background-image: {CHROMOSOME_SHEEN}, '
	cell += f'linear-gradient(to right, {left_color} 50%, {right_color} 50%);">'
	cell += f'<span style="min-width: {width}px; background-color: {fill_color}; '
	cell += f'{CENTROMERE_STYLE}">'
	cell += f'{label}</span></td>'
	return cell


#======================================
def _chromosome_table(widths: tuple[float, ...], cells: tuple[str, ...]) -> str:
	"""Assemble ordered chromosome cells using their arm and centromere widths."""
	table = f'<table style="{CHROMOSOME_TABLE_STYLE}">'
	for width in widths:
		table += f'<colgroup width="{width}"></colgroup>'
	table += '<tr>' + ''.join(cells) + '</tr></table>'
	return table


#======================================
def merge_tables(table_list):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white;">'
	for chromo_table in table_list:
		table += '<tr>'
		table += '  <td align="left">{0}</td>'.format(chromo_table)
		table += '</tr>'
	table += '</table>'
	return table


#======================================
def format_gamete_choice(label: str, chromosomes: list[str]) -> str:
	"""Group chromosomes inside one rounded frame, with a label when supplied."""
	table = '<table style="border-collapse: separate; border-spacing: 0; '
	table += 'border: 1px solid #adb5bd; border-radius: 8px; '
	table += 'color: #000; background-color: #fff;">'
	contents = [label, *chromosomes] if label else chromosomes
	for content in contents:
		table += '<tr><td style="border: 0; padding: 4px 8px;">'
		table += content + '</td></tr>'
	table += '</table>'
	return table


#======================================
def draw_sequence_chromosome(left_sequence: str, right_sequence: str,
		left_color: str, right_color: str, *, source: bool = False,
		telomeres: tuple[str, str] = ('left', 'right')) -> str:
	"""Draw gene sequences and separate gray telomere regions, with optional break arrows."""
	widths = []
	cells = []
	break_offset = 0
	for index, (sequence, color, telomere) in enumerate(zip(
		(left_sequence, right_sequence), (left_color, right_color), telomeres)):
		label = '<span style="font-family: monospace; font-size: 15px; white-space: nowrap;">'
		for gene in sequence:
			label += '<span style="display: inline-block; width: 18px;">'
			label += html.escape(gene) + '</span>'
		label += '</span>'
		outer_edge = 'left' if index == 0 else 'right'
		cap_is_outer = telomere == outer_edge
		arm_edge = 'middle' if cap_is_outer else outer_edge
		cap_edge = outer_edge if cap_is_outer else 'middle'
		arm = _draw_arm(color, arm_edge, label,
			mark_junction=index == 0 and telomere == 'left')
		cap = _draw_arm('#888', cap_edge, textured=False,
			mark_junction=index == 0 and telomere == 'right')
		arm_width = len(sequence) * 18 + 2 + (0 if cap_is_outer else 2)
		cap_width = 6 + (2 if cap_is_outer else 0)
		if telomere == 'left':
			widths.extend((cap_width, arm_width))
			cells.extend((cap, arm))
		else:
			widths.extend((arm_width, cap_width))
			cells.extend((arm, cap))
		if index == 0:
			break_offset = arm_width + cap_width
	table = _chromosome_table(tuple(widths), tuple(cells))
	if source:
		arrow = '<span aria-hidden="true" style="position: absolute; top: 0; '
		arrow += f'left: {break_offset}px; transform: translateX(-50%); '
		arrow += 'font-size: 18px; line-height: 18px; color: #555;">&darr;</span>'
		wrapper = '<div style="display: inline-block; position: relative; padding-top: 18px; '
		wrapper += 'color: #000; background-color: #fff;">'
		table = wrapper + arrow + table + '</div>'
	return table


#======================================
def draw_meiosis_chromosome(chromosome1: int, color: str = 'red', scale: float = 2.4,
		centromere_width: int = DEFAULT_CENTROMERE_WIDTH) -> str:
	distance = CHROMOSOME_LENGTHS[chromosome1]
	arm_color = COLOR_SCALES[color][2]
	widths = (distance[0] * scale - centromere_width / 2, centromere_width,
		distance[1] * scale - centromere_width / 2)
	cells = (
		_draw_arm(arm_color, 'left'),
		_draw_centromere(arm_color, arm_color, centromere_width, chromosome1),
		_draw_arm(arm_color, 'right'),
	)
	table = _chromosome_table(widths, cells)
	return table


#======================================
def draw_translocated_chromosome(chromosome1: int, chromosome2: int,
		color1: str = 'red', color2: str = 'blue', scale_main: float = 2.4,
		scale_trans: float = 1.2, centromere_width: int = DEFAULT_CENTROMERE_WIDTH) -> str:
	distance1 = CHROMOSOME_LENGTHS[chromosome1]
	distance2 = CHROMOSOME_LENGTHS[chromosome2]
	arm_color1 = COLOR_SCALES[color1][2]
	arm_color2 = COLOR_SCALES[color2][2]
	widths = (distance1[0] * scale_main - centromere_width / 2, centromere_width,
		distance1[1] * scale_trans - centromere_width / 4,
		distance2[1] * scale_trans - centromere_width / 4)
	cells = (
		_draw_arm(arm_color1, 'left'),
		_draw_centromere(arm_color1, arm_color1, centromere_width, chromosome1),
		_draw_arm(arm_color1, 'junction'),
		_draw_arm(arm_color2, 'right'),
	)
	table = _chromosome_table(widths, cells)
	return table


#======================================
def draw_robertsonian_chromosome(chromosome1: int, chromosome2: int,
		color1: str = 'coral', color2: str = 'deepskyblue', scale: float = 3,
		centromere_width: int = DEFAULT_CENTROMERE_WIDTH) -> str:
	distance1 = CHROMOSOME_LENGTHS[chromosome1]
	distance2 = CHROMOSOME_LENGTHS[chromosome2]
	widths = (distance1[1] * scale - centromere_width / 2, centromere_width,
		distance2[1] * scale - centromere_width / 2)
	cells = (
		_draw_arm(color1, 'left', f'{chromosome1}q'),
		_draw_centromere(color1, color2, centromere_width),
		_draw_arm(color2, 'right', f'{chromosome2}q'),
	)
	table = _chromosome_table(widths, cells)
	return table


#======================================
def draw_robertsonian_single_chromosome(chromosome1: int, color: str = 'coral',
		scale: float = 3, centromere_width: int = DEFAULT_CENTROMERE_WIDTH) -> str:
	distance = CHROMOSOME_LENGTHS[chromosome1]
	widths = (distance[0] * scale - centromere_width / 2, centromere_width,
		distance[1] * scale - centromere_width / 2)
	cells = (
		_draw_arm(color, 'left', f'{chromosome1}p'),
		_draw_centromere(color, color, centromere_width),
		_draw_arm(color, 'right', f'{chromosome1}q'),
	)
	table = _chromosome_table(widths, cells)
	return table
