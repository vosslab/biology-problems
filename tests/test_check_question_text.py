"""Protect the advisory question-text checker's normalization and check rules."""

# Standard Library
import os
import sys

# PIP3 modules
import pytest

# local repo modules
import file_utils

DEVEL_DIR = os.path.join(file_utils.get_repo_root(), 'devel')
if DEVEL_DIR not in sys.path:
	sys.path.insert(0, DEVEL_DIR)

import check_question_text


#============================================
def make_item(kind: str, stem: str, *fields: str) -> check_question_text.Item:
	"""Parse a BBQ line built from a stem and the remaining tab fields."""
	line = '\t'.join([kind, '<p>a4e3_61c6</p> ' + stem, *fields])
	item = check_question_text.parse_line(1, line)
	return item


#============================================
def make_mc(stem: str, choices: list, key_index: int) -> check_question_text.Item:
	"""Parse an MC item with one key."""
	fields = []
	for i, choice in enumerate(choices):
		fields += [choice, 'Correct' if i == key_index else 'Incorrect']
	item = make_item('MC', stem, *fields)
	return item


#============================================
def test_normalization_removes_hidden_text_and_crc_tag() -> None:
	hidden_term = "<span style='font-size: 1px; color: white;'>noise</span>"
	raw = f'<p>Which{hidden_term}enzyme<span style="display:none">secret</span> cuts DNA</p>'
	# anti-cheat terms replace a space, so the words must stay separate
	assert check_question_text.clean_field(raw).plain == 'Which enzyme cuts DNA'
	item = make_item('FIB', '<p>Stem text.</p>', 'answer')
	assert item.stem.plain == 'Stem text.'


#============================================
@pytest.mark.parametrize('key_text,findings', [
	('It joins the nucleotides of a growing DNA strand', 1),
	('It cuts the DNA strands', 0),
])
def test_k1_needs_a_clear_margin(key_text: str, findings: int) -> None:
	distractors = ['It cuts the DNA strand', 'It seals the DNA nick', 'It unwinds the helix']
	item = make_mc('<p>What does the enzyme do?</p>', [key_text] + distractors, 0)
	key_length, other_length = check_question_text.key_length_pair(item)
	# both keys are the longest choice; only the first clears the margin
	assert key_length > other_length
	assert len(check_question_text.check_k1(item)) == findings


#============================================
def build_k2_items(stem: str, count: int, key: str, distractors: list) -> list:
	"""Build count MC items that share one key and one distractor set."""
	items = [make_mc(stem, [key] + distractors, 0) for _ in range(count)]
	return items


#============================================
def test_k2_flags_hedged_keys_and_absolute_distractors() -> None:
	distractors = ['It always binds ATP.', 'It never binds DNA.', 'It only binds ATP.']
	stem = '<p>Which statement about the enzyme is true?</p>'
	items = build_k2_items(stem, 6, 'It usually binds substrate.', distractors)
	findings = check_question_text.k2_findings(check_question_text.k2_tally(items))
	assert [finding.check for finding in findings] == ['K2']
	# a NOT stem makes the distractors the true statements, so the same text is no cue
	negated = build_k2_items(
		'<p>Which statement is <strong>NOT</strong> true?</p>',
		6, 'It usually binds substrate.', distractors)
	assert check_question_text.k2_findings(check_question_text.k2_tally(negated)) == []


#============================================
def test_k3_k6_and_k7_report_distinct_text_cues() -> None:
	"""Keep the stem/key echo, unit, and generic-lead-in checks reviewable."""
	item = make_mc(
		'<p>Which statement best describes the 10 &micro;L sample?</p>',
		['The 10 mL sample is diluted.', 'The cells are divided.', 'The protein binds DNA.'], 0,
	)
	assert len(check_question_text.check_k3(item)) == 1
	assert len(check_question_text.check_k6(item)) == 1
	assert len(check_question_text.check_k7(item)) == 1


#============================================
@pytest.mark.parametrize('text,slips', [
	('A organism has an cell wall.', 2),
	('A pea has a X-linked trait.', 1),
	('An allele and a unique X-linked trait in an MRI of an mRNA after an hour.', 0),
])
def test_k4_article_slips(text: str, slips: int) -> None:
	item = make_item('FIB', f'<p>{text}</p>', 'answer')
	assert len(check_question_text.check_k4(item)) == slips


#============================================
@pytest.mark.parametrize('stem,slips', [
	('<p>hh.A pea plant</p>', 1),
	('<p>A pea plant.</p><p>Which gene is it?</p>', 0),
	('<p>A pea  plant.</p>', 1),
	('<p><i>A pea </i> plant.</p>', 0),
	('<p>Which gene is it ?</p>', 1),
	('<p>A ratio of 3 : 1 and a wait... done.</p>', 0),
])
def test_k5_spacing_slips(stem: str, slips: int) -> None:
	item = make_item('FIB', stem, 'answer')
	assert len(check_question_text.check_k5(item)) == slips


#============================================
def test_report_is_advisory_and_tolerates_bad_input(tmp_path) -> None:
	good = tmp_path / 'good.txt'
	good.write_text(
		'FIB\t<p>a4e3_61c6</p> <p>Which statement best describes it?</p>\tanswer\n'
		'not a bbq line\n'
	)
	missing = tmp_path / 'missing.txt'
	lines = check_question_text.build_report([str(good), str(missing)])
	assert any('never a pass/fail gate' in line for line in lines)
	assert any(line.lstrip().startswith('Q1') and 'K7' in line for line in lines)
	assert any('skipped: not a file' in line for line in lines)
	assert any('malformed lines skipped: 1' in line for line in lines)
