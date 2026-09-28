"""Protect translation answer keys and plausible, distinct peptide choices."""

import os
import re
import sys
import random

import pytest

import file_utils

SEQ_DIR = os.path.join(file_utils.get_repo_root(), 'problems', 'molecular_biology-problems')
if SEQ_DIR not in sys.path:
	sys.path.insert(0, SEQ_DIR)

import seqlib
import translate_genetic_code


def test_hamming_and_nearest_word_choices(monkeypatch: pytest.MonkeyPatch) -> None:
	generator = translate_genetic_code
	monkeypatch.setattr(generator, 'random', random.Random(12345))
	words = ['MIMIC', 'MAGIC', 'MANIC', 'MEDIC', 'MAMMA', 'MAMMA', 'CIVIC']
	monkeypatch.setattr(generator, 'read_wordle_list', lambda: words)
	choices = generator.make_peptide_choices('MIMIC', 4, wordle=True)
	assert set(choices) == {'MIMIC', 'MAGIC', 'MANIC', 'MEDIC'}
	assert len(choices) == len(set(choices))
	assert generator.hamming_distance('MIMIC', 'MAGIC') == 2
	with pytest.raises(ValueError, match='same length'):
		generator.hamming_distance('MIMIC', 'MIMICS')
	with pytest.raises(ValueError, match='Not enough'):
		generator.make_peptide_choices('M', 2, wordle=False)


@pytest.mark.parametrize('length', [2, 5, 6, 10])
@pytest.mark.parametrize('extra', [False, True])
def test_mc_key_matches_mrna_and_choices_share_hint(monkeypatch: pytest.MonkeyPatch,
		length: int, extra: bool) -> None:
	generator = translate_genetic_code
	seeded = random.Random(12345)
	monkeypatch.setattr(generator, 'random', seeded)
	monkeypatch.setattr(seqlib, 'random', seeded)
	item = generator.make_complete_question(1, length, extra, 'mc', 4)
	sequences = re.findall(r'<!--\s*([ACGU]+)\s*-->', item.question_text)
	mrna = sequences[-1]
	start = mrna.index('AUG')
	translated = seqlib.translate(mrna[start:start + 3 * (length + 1)])
	assert translated == item.answer_text + '_'
	assert len(item.choices_list) == len(set(item.choices_list)) == 4
	assert item.choices_list.count(item.answer_text) == 1
	assert all(len(choice) == length and choice.startswith('M') for choice in item.choices_list)
	if length % 5 == 0:
		words = set(generator.read_wordle_list())
		assert all(choice[i:i + 5] in words for choice in item.choices_list
			for i in range(0, length, 5))
	else:
		assert all(generator.hamming_distance(item.answer_text, choice) == 1
			for choice in item.choices_list if choice != item.answer_text)


def test_short_fib_answers_remain_unique(monkeypatch: pytest.MonkeyPatch) -> None:
	generator = translate_genetic_code
	monkeypatch.setattr(generator, 'random', random.Random(12345))
	item = generator.make_complete_question(1, 5)
	assert len(item.answers_list) == len(set(item.answers_list))
	assert len({answer.replace(',', '') for answer in item.answers_list}) == 1
