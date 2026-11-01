import lxml.html

import lib_test_utils


def test_translocation_diagrams_preserve_arm_order_and_proportions() -> None:
	lib = lib_test_utils.import_from_repo_path(
		'problems/inheritance-problems/translocation/translocationlib.py')
	cases = (
		(lib.draw_robertsonian_chromosome(
			14, 21, 'coral', 'deepskyblue', scale=3, centromere_width=24),
			['14q', '', '21q'], [258, 24, 93], ['coral', None, 'deepskyblue']),
		(lib.draw_translocated_chromosome(
			13, 21, 'red', 'blue', scale_main=2, scale_trans=1, centromere_width=20),
			['', '13', '', ''], [26, 20, 92, 30],
			[lib.COLOR_SCALES['red'][2], None,
			lib.COLOR_SCALES['red'][2], lib.COLOR_SCALES['blue'][2]]),
	)
	for markup, labels, widths, arm_colors in cases:
		table = lxml.html.fromstring(markup)
		cells = table.xpath('./tr/td')
		assert [cell.text_content().strip() for cell in cells] == labels
		assert [float(width) for width in table.xpath('./colgroup/@width')] == widths
		for cell, color in zip(cells, arm_colors):
			if color is not None:
				assert f'background-color: {color};' in cell.get('style')
