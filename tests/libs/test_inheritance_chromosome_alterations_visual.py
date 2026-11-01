import argparse
import random
import re

import lxml.html
import pytest

import lib_test_utils


def displayed_sequences(markup: str) -> tuple[str, ...]:
	"""Read gene order independently of captions, colors, and junction decorations."""
	root = lxml.html.fragment_fromstring(markup, create_parent=True)
	sequences = []
	for table in root.xpath('.//table[colgroup]'):
		cells = table.xpath('./tr/td')
		p = ''.join(re.findall(r'\b[A-Z]\b', cells[1].text_content()))
		q = ''.join(re.findall(r'\b[A-Z]\b', ' '.join(cell.text_content() for cell in cells[3:-1])))
		sequences.append(p + '|' + q)
	return tuple(sequences)


def test_alterations_change_the_intended_regions_and_preserve_source_colors() -> None:
	"""Prevent incorrect gene loss, duplication, orientation, or exchange in answer diagrams."""
	visual = lib_test_utils.import_from_repo_path(
		'problems/inheritance-problems/translocation/chromosome_alterations_visual.py')
	first = visual.Chromosome('AB', 'coral', tuple((g, 'coral') for g in 'CDEFGH'))
	second = visual.Chromosome('MN', 'skyblue', tuple((g, 'skyblue') for g in 'OPQRST'))
	outcomes = visual.make_alterations((first, second), 1, 4, 4, 4)
	expected = {
		'del': ('CGH', 'OPQRST'),
		'dup': ('CDEDEFGH', 'OPQRST'),
		'inv': ('CFEDGH', 'OPQRST'),
		't': ('CDEFST', 'OPQRGH'),
	}
	expected_junctions = {
		'del': ((1,), ()), 'dup': ((3,), ()),
		'inv': ((1, 4), ()), 't': ((4,), (4,)),
	}
	for code, pair in outcomes.items():
		assert tuple(''.join(gene for gene, color in chromosome.q)
			for chromosome in pair) == expected[code]
		assert [(c.p, c.color) for c in pair] == [('AB', 'coral'), ('MN', 'skyblue')]
		assert tuple(c.junctions for c in pair) == expected_junctions[code]
		for chromosome in pair:
			for gene, color in chromosome.q:
				assert color == ('coral' if gene in 'CDEFGH' else 'skyblue')
	short_source = visual.Chromosome('ABC', 'coral', tuple((g, 'coral') for g in 'DEFGH'))
	deleted = visual.make_alterations((short_source, second), 1, 4, 2, 4)['del'][0]
	markup = visual.draw_chromosomes((deleted,))
	assert displayed_sequences(markup) == ('ABC|DH',)
	assert lxml.html.fromstring(markup).xpath('.//table[@role="img"]/@aria-label') == [
		'A B C centromere D break H']


def test_scenario_preserves_consecutive_letters_and_original_arm_lengths(monkeypatch: pytest.MonkeyPatch) -> None:
	"""Avoid false source deletions and keep original arm sizes within the requested range."""
	visual = lib_test_utils.import_from_repo_path(
		'problems/inheritance-problems/translocation/chromosome_alterations_visual.py')
	monkeypatch.setattr(visual, 'random', random.Random(1))
	originals, outcomes = visual.generate_scenario()
	assert len(originals[0].q) >= 5
	assert len(originals[0].q) - len(outcomes['del'][0].q) >= 3
	inversion = outcomes['inv'][0].junctions
	assert inversion[1] - inversion[0] >= 3
	assert len(outcomes['dup'][0].q) - len(originals[0].q) == 2
	all_genes = ''
	for chromosome in originals:
		assert 2 <= len(chromosome.p) <= 5
		assert 4 <= len(chromosome.q) <= 11
		assert len(chromosome.p) < len(chromosome.q)
		for arm in (chromosome.p, ''.join(g for g, color in chromosome.q)):
			assert [ord(gene) for gene in arm] == list(range(ord(arm[0]), ord(arm[0]) + len(arm)))
			all_genes += arm
	assert len(set(all_genes)) == len(all_genes)


def test_matching_and_both_mc_directions_keep_the_correct_mapping(monkeypatch: pytest.MonkeyPatch) -> None:
	"""Format changes and choice shuffling must not disconnect the diagram from its key."""
	visual = lib_test_utils.import_from_repo_path(
		'problems/inheritance-problems/translocation/chromosome_alterations_visual.py')
	first = visual.Chromosome('AB', 'coral', tuple((g, 'coral') for g in 'CDEFGH'))
	second = visual.Chromosome('MN', 'skyblue', tuple((g, 'skyblue') for g in 'OPQRST'))
	originals = (first, second)
	outcomes = visual.make_alterations(originals, 1, 4, 4, 4)
	monkeypatch.setattr(visual, 'generate_scenario', lambda: (originals, outcomes))
	monkeypatch.setattr(visual, 'random', random.Random(13))
	mapping = {
		'del': ('AB|CGH', 'MN|OPQRST'),
		'dup': ('AB|CDEDEFGH', 'MN|OPQRST'),
		'inv': ('AB|CFEDGH', 'MN|OPQRST'),
		't': ('AB|CDEFST', 'MN|OPQRGH'),
	}
	names = {'del': 'Deletion', 'dup': 'Duplication', 'inv': 'Inversion', 't': 'Translocation'}
	args = argparse.Namespace(question_type='matching', flip=False, always_two=False)
	matching = visual.write_question(1, args)
	assert displayed_sequences(matching.question_text) == ('AB|CDEFGH', 'MN|OPQRST')
	assert {lxml.html.fromstring(term).text_content(): displayed_sequences(diagram)
		for term, diagram in zip(matching.prompts_list, matching.choices_list)} == {
		names[code]: pair for code, pair in mapping.items()}
	# Cover each count rule once rather than every combination of format options.
	for target, flipped, always_two, count in (
		('dup', False, False, 1), ('dup', True, False, 1),
		('t', True, False, 2), ('dup', True, True, 2),
	):
		monkeypatch.setattr(visual.random, 'choice', lambda choices: target)
		args = argparse.Namespace(question_type='mc', flip=flipped, always_two=always_two)
		item = visual.write_question(2, args)
		assert item.choices_list.count(item.answer_text) == 1
		if flipped:
			pool = set(mapping.values()) if count == 2 else {
				mapping[code][:1] for code in ('del', 'dup', 'inv')}
			if count == 1:
				pool.add(('AB|CDEFGH',))
			assert {displayed_sequences(choice) for choice in item.choices_list} == pool
			assert displayed_sequences(item.answer_text) == mapping[target][:count]
			question_text = lxml.html.fragment_fromstring(item.question_text, create_parent=True).text_content()
			assert re.findall(r'\b(?:Deletion|Duplication|Inversion|Translocation)\b', question_text) == [names[target]]
		else:
			assert {lxml.html.fromstring(choice).text_content() for choice in item.choices_list} == set(names.values())
			assert lxml.html.fromstring(item.answer_text).text_content() == names[target]
			assert displayed_sequences(item.question_text)[count:] == mapping[target][:count]
