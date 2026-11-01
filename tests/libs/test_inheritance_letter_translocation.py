import random

import lxml.html
import pytest

import lib_test_utils


def test_visual_products_have_one_impossible_orientation(monkeypatch: pytest.MonkeyPatch) -> None:
	visual = lib_test_utils.import_from_repo_path(
		'problems/inheritance-problems/translocation/letter_translocation_problem_visual.py')
	model = visual.letter_model
	monkeypatch.setattr(visual, 'random', random.Random(417))
	chromosome1 = model.Chromosome(model.Fragment('ABC', 'A', 'C'),
		model.Fragment('DEF', 'F', 'D'))
	chromosome2 = model.Chromosome(model.Fragment('JKL', 'J', 'L'),
		model.Fragment('OPQ', 'Q', 'O'))
	candidates, answer = visual.generate_choices(chromosome1, chromosome2)
	valid_sequences = {'ABCLKJ', 'ABCOPQ', 'FEDLKJ', 'FEDOPQ'}
	sequences = []
	for candidate in candidates:
		table = lxml.html.fromstring(visual.draw_chromosome(candidate))
		left, right = [''.join(cell.text_content().split()) for cell in table.xpath('./tr/td')
			if cell.text_content()]
		assert set(left) <= set('ABCDEF')
		assert set(right) <= set('JKLOPQ')
		sequences.append(left + right)
	assert len(sequences) == len(set(sequences)) == 5
	key = sequences[candidates.index(answer)]
	assert key not in valid_sequences
	assert set(sequences) - {key} == valid_sequences


def test_visual_rendering_preserves_reversed_fragment_color_and_telomere() -> None:
	visual = lib_test_utils.import_from_repo_path(
		'problems/inheritance-problems/translocation/letter_translocation_problem_visual.py')
	model = visual.letter_model
	chromosome = model.Chromosome(
		model.Fragment('ABC', 'A', 'C', rgb_color='coral'),
		model.Fragment('JKL', 'L', 'J', rgb_color='royalblue'),
		telomere_A_improper=True)
	table = lxml.html.fromstring(visual.draw_chromosome(chromosome))
	all_cells = table.xpath('./tr/td')
	assert [''.join(cell.text_content().split()) for cell in all_cells] == ['CBA', '', 'JKL', '']
	cells = [cell for cell in all_cells if cell.text_content()]
	assert [''.join(cell.text_content().split()) for cell in cells] == ['CBA', 'JKL']
	assert 'background-color: coral;' in cells[0].get('style')
	assert 'background-color: royalblue;' in cells[1].get('style')
	# Browser HTML parsing must not nest caps inside self-closing decoration spans.
	exported = lxml.html.tostring(table, encoding='unicode', method='xml')
	assert exported.count('<span') == exported.count('</span>')
