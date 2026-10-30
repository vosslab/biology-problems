import argparse
import random
import re

import bptools
from lib_test_utils import import_from_repo_path


ordering = import_from_repo_path('problems/ordering/orderinglib.py')


def test_numeric_steps_and_alternative_replacements(monkeypatch) -> None:
	bank = {
		'topic': 'DNA preparation',
		'steps': {'step 10': ['Finish.'], 'step 2': ['Extract DNA.', 'Isolate DNA.'],
			'step 1': ['Collect.']},
		'replacement_rules': {'DNA': '<span>DNA</span>'},
	}
	monkeypatch.setattr(random, 'choice', lambda values: values[-1])
	steps = ordering.ordered_steps(bank)
	prompt, items, _ = ordering.question_content(bank, steps, False)
	assert items == ['Collect.', 'Isolate <strong><span>DNA</span></strong>.', 'Finish.']
	assert prompt == (
		'<p>Place the following steps of <strong><span>DNA</span></strong> preparation '
		'in order from first to last.</p>')
	bank['question override'] = 'Rank DNA samples.'
	prompt, _, lead_out = ordering.question_content(bank, steps, True)
	assert prompt == '<p>Rank <strong><span>DNA</span></strong> samples.</p>'
	assert lead_out == 'Which sequence gives the correct order?'


def test_mc_labels_recover_complete_order(monkeypatch) -> None:
	bank = {'topic': 'a workflow', 'steps': {
		'step 1': ['Collect.'], 'step 2': ['Extract.'], 'step 3': ['Amplify.']}}
	rng = random.Random(17)
	monkeypatch.setattr(random, 'sample', rng.sample)
	monkeypatch.setattr(random, 'shuffle', rng.shuffle)
	monkeypatch.setattr(random, 'choice', rng.choice)
	steps = ordering.ordered_steps(bank)
	item = ordering.write_question(1, argparse.Namespace(), bank, steps, mc=True)
	displayed = re.findall(r'<li>(.*?)</li>', item.question_text)
	answer = [int(value) for value in re.findall(r'\[(\d+)\]', item.answer_text)]
	assert [re.sub(r'<[^>]+>', '', displayed[label - 1]).endswith(text) for label, text in
		zip(answer, ['Collect.', 'Extract.', 'Amplify.'])] == [True, True, True]
	assert len(set(item.choices_list)) == 4
	assert item.choices_list.count(item.answer_text) == 1
	for choice in item.choices_list:
		assert sorted(int(value) for value in re.findall(r'\[(\d+)\]', choice)) == [1, 2, 3]
	native = ordering.write_question(2, argparse.Namespace(), bank, steps, mc=False)
	assert native.ordered_answers_list == ['Collect.', 'Extract.', 'Amplify.']
	assert isinstance(native, bptools.item_types.ORDER)


def test_choice_label_colors_match_the_prompt_positions(monkeypatch) -> None:
	bank = {'topic': 'a workflow', 'steps': {
		'step 1': ['Collect.'], 'step 2': ['Extract.'], 'step 3': ['Amplify.']}}
	rng = random.Random(31)
	monkeypatch.setattr(random, 'sample', rng.sample)
	monkeypatch.setattr(random, 'shuffle', rng.shuffle)
	monkeypatch.setattr(random, 'choice', rng.choice)
	item = ordering.write_question(1, argparse.Namespace(), bank,
		ordering.ordered_steps(bank), mc=True)
	label_colors = {}
	for line in re.findall(r'<li>(.*?)</li>', item.question_text):
		color, label = re.search(r'<span style="color: (#[0-9A-F]+);">(\[\d+\])</span>', line).groups()
		label_colors[label] = color
	for choice in item.choices_list:
		choice_pairs = re.findall(
			r'<span style="color: (#[0-9A-F]+);">(\[\d+\])</span>', choice)
		assert len(choice_pairs) == 3
		choice_label_colors = {label: color for color, label in choice_pairs}
		assert len(choice_label_colors) == 3
		assert choice_label_colors == label_colors
	assert len(label_colors) == 3


def test_color_modes_only_color_requested_material(monkeypatch) -> None:
	bank = {'topic': 'a workflow', 'steps': {
		'step 1': ['Collect.'], 'step 2': ['Extract.'], 'step 3': ['Amplify.']}}
	steps = ordering.ordered_steps(bank)
	rng = random.Random(17)
	monkeypatch.setattr(random, 'sample', rng.sample)
	monkeypatch.setattr(random, 'shuffle', rng.shuffle)
	monkeypatch.setattr(random, 'choice', rng.choice)
	full = ordering.write_question(1, argparse.Namespace(), bank, steps, mc=True)
	assert 'style="color:' in full.question_text
	assert 'style="color:' in ''.join(full.choices_list)
	full_prompt_items = re.findall(r'<li>(.*?)</li>', full.question_text)
	assert len(full_prompt_items) == 3
	assert all('style="color:' in re.sub(
		r'<span style="color: #[0-9A-F]+;">\[\d+\]</span>', '', line)
		for line in full_prompt_items)
	labels = ordering.write_question(2, argparse.Namespace(color_mode='labels'), bank, steps, mc=True)
	assert 'style="color:' in labels.question_text
	assert 'style="color:' in ''.join(labels.choices_list)
	prompt_items = re.findall(r'<li>(.*?)</li>', labels.question_text)
	assert len(prompt_items) == 3
	assert all('style="color:' not in re.sub(
		r'<span style="color: #[0-9A-F]+;">\[\d+\]</span>', '', line)
		for line in prompt_items)
	none = ordering.write_question(3, argparse.Namespace(color_mode='none'), bank, steps, mc=True)
	assert 'style="color:' not in none.question_text
	assert 'style="color:' not in ''.join(none.choices_list)
