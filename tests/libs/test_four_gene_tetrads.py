import random

import lxml.html

from lib_test_utils import import_from_repo_path

BASE = 'problems/inheritance-problems/gene_mapping/'


def test_four_gene_tetrads_preserve_distances_and_order():
	mod = import_from_repo_path(BASE + 'tetrad_unordered_four_gene-distances_plus.py')
	pool = mod.gml.get_four_gene_distance_pool()
	for key in random.Random(17).sample(list(pool), 20):
		rows = mod.construct_tetrads('abcd', 'cadb', '+b+d', pool[key][0])
		assert len(rows) == 16 and min(rows.values()) > 0
		assert sum(rows.values()) == 12000
		for tetrad in rows:
			assert all(sum(spore[i] == '+' for spore in tetrad) == 2 for i in range(4))
		divisor = mod.math.gcd(*rows.values())
		for scale in (1, 4):
			scaled = {tetrad: n // divisor * scale for tetrad, n in rows.items()}
			answers = mod.get_answer_mapping(scaled, 'abcd')
			assert set(answers['geneorder']) == {'cadb', 'bdac'}
			for (i, j), expected in zip(mod.PAIR_POSITIONS, key):
				pair = ''.join(sorted(('cadb'[i], 'cadb'[j]))).upper()
				assert answers[pair][0] == f'{expected / 10:.1f}'


def test_four_gene_question_rendering_and_variable_totals(monkeypatch):
	mod = import_from_repo_path(BASE + 'tetrad_unordered_four_gene-distances_plus.py')
	captured = []
	monkeypatch.setattr(mod.bptools, 'formatBB_FIB_PLUS_Question',
		lambda number, text, answers: captured.append((text, answers)))
	totals = set()
	state = random.getstate()
	try:
		for seed in range(8):
			random.seed(seed)
			mod.write_question(1, None)
	finally:
		random.setstate(state)
	for text, answers in captured:
		document = lxml.html.fromstring(('<root>' + text + '</root>').encode())
		visual, = document.xpath('.//table[not(ancestor::table)][.//*[@data-genotype]]')
		assert [len(row) for row in visual] == [4, 4, 4, 4]
		assert len(visual.xpath('.//*[@data-genotype]')) == 64
		counts = [int(node.text.split()[0].replace(',', ''))
			for node in visual.xpath('./tr/td/div[1]')]
		total = sum(counts)
		assert 0 < total <= 100000
		totals.add(total)
		assert len(document.xpath('.//td[@data-pair]')) == 16 * 6
		assert len(answers) == 7
		assert all(text.count(f'[{key}]') == 1 for key in answers)
		assert all(order.islower() for order in answers['geneorder'])
	assert len(totals) > 1
	# Diagonal endpoints give four fixed top/right/bottom/left sectors.
	svg = mod.tetradlib.asci.ascus_svg(('abcd',) * 4, 'abcd')
	assert 'L-14.142 -12.728 A20 18 0 0 1 14.142 -12.728Z' in svg
