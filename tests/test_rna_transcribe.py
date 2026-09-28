"""Protect transcription direction and unambiguous MC answer keys."""

# Standard Library
import os
import sys

# PIP3 modules
import pytest

# local repo modules
import file_utils

SEQ_DIR = os.path.join(file_utils.get_repo_root(), 'problems', 'molecular_biology-problems')
if SEQ_DIR not in sys.path:
	sys.path.insert(0, SEQ_DIR)

import seqlib
import rna_transcribe_lib


#============================================
@pytest.mark.parametrize('strand,fivetothree,expected', [
	('template', False, 'UACGGC'),
	('template', True, 'CGGCAU'),
	('coding', True, 'AUGCCG'),
	('coding', False, 'GCCGUA'),
])
def test_rna_respects_strand_and_direction(strand: str, fivetothree: bool,
		expected: str) -> None:
	answer = rna_transcribe_lib.transcribe_sequence('ATGCCG', strand, fivetothree)
	assert answer == expected
	accepted = rna_transcribe_lib.fib_answers(answer, prime=True)
	assert expected in accepted and f"5'-{expected}-3'" in accepted
	assert seqlib.insertCommas(expected) in accepted


#============================================
@pytest.mark.parametrize('direction_mode', ['directionless', 'prime'])
@pytest.mark.parametrize('fivetothree', [True, False])
@pytest.mark.parametrize('choice_fivetothree', [True, False])
def test_mc_has_one_correct_rna_product(monkeypatch: pytest.MonkeyPatch,
		direction_mode: str, fivetothree: bool, choice_fivetothree: bool) -> None:
	sequence = 'ATGCCG'
	monkeypatch.setattr(seqlib, 'makeSequence', lambda length: sequence)
	directions = [fivetothree, choice_fivetothree] if direction_mode == 'prime' else [True]
	selection = iter(directions)
	monkeypatch.setattr(rna_transcribe_lib.random, 'choice', lambda options: next(selection))
	monkeypatch.setattr(rna_transcribe_lib.random, 'shuffle', lambda choices: None)
	item = rna_transcribe_lib.generate_question(1, len(sequence), 'mc', direction_mode)
	if direction_mode == 'prime':
		answer = 'CGGCAU' if fivetothree else 'UACGGC'
		display = answer if choice_fivetothree else answer[::-1]
		expected_table = seqlib.Single_Strand_Table(display, fivetothree=choice_fivetothree)
	else:
		expected_table = seqlib.Single_Strand_Table_No_Primes('UACGGC')
		assert '&prime;' not in item.question_text
	assert item.answer_text == expected_table
	assert item.choices_list.count(expected_table) == 1
	assert len(item.choices_list) == len(set(item.choices_list))


#============================================
@pytest.mark.parametrize('strand,fivetothree,expected', [
	('template', False, 'UACGGC'),
	('template', True, 'CGGCAU'),
	('coding', True, 'AUGCCG'),
	('coding', False, 'GCCGUA'),
])
def test_prime_fib_generated_answer_key(monkeypatch: pytest.MonkeyPatch,
		strand: str, fivetothree: bool, expected: str) -> None:
	monkeypatch.setattr(seqlib, 'makeSequence', lambda length: 'ATGCCG')
	selection = iter([fivetothree, strand])
	monkeypatch.setattr(rna_transcribe_lib.random, 'choice', lambda options: next(selection))
	item = rna_transcribe_lib.generate_question(1, 6, 'fib', 'prime')
	assert expected in item.answers_list
	plain_answers = [answer for answer in item.answers_list if '-' not in answer]
	assert {answer.replace(',', '') for answer in plain_answers} == {expected}
