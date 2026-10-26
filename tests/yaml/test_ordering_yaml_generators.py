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
	answer = [int(value) for value in item.answer_text.split(' &rarr; ')]
	assert [displayed[label - 1] for label in answer] == ['Collect.', 'Extract.', 'Amplify.']
	assert len(set(item.choices_list)) == 4
	assert item.choices_list.count(item.answer_text) == 1
	for choice in item.choices_list:
		assert sorted(int(value) for value in choice.split(' &rarr; ')) == [1, 2, 3]
	native = ordering.write_question(2, argparse.Namespace(), bank, steps, mc=False)
	assert native.ordered_answers_list == ['Collect.', 'Extract.', 'Amplify.']
	assert isinstance(native, bptools.item_types.ORDER)
