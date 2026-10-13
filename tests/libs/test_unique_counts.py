"""Protect shared-cross answers with independent gamete enumeration."""

import sys
import copy
import argparse
import pathlib
import itertools

import pytest
import lxml.html

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'problems/inheritance-problems/large_crosses'))
import unique_counts_lib


def test_counts_against_enumerated_crosses() -> None:
	"""All two-locus parental combinations include fixed and variable outcomes."""
	parents = list(itertools.product(('AA', 'Aa', 'aa'), ('BB', 'Bb', 'bb')))
	for first, second in itertools.product(parents, repeat=2):
		scenario = {'parents': [
			{'name': 'First', 'name_color': '#663399', 'genotype': list(first)},
			{'name': 'Second', 'name_color': '#006B5E', 'genotype': list(second)},
		]}
		unique_counts_lib.validate_scenario(scenario)
		gametes1 = set(itertools.product(*first))
		gametes2 = set(itertools.product(*second))
		offspring = {tuple(''.join(sorted(pair)) for pair in zip(a, b))
			for a, b in itertools.product(gametes1, gametes2)}
		phenotypes = {tuple(any(allele.isupper() for allele in pair) for pair in child)
			for child in offspring}
		counts = unique_counts_lib.count_outcomes(scenario)
		assert counts['gametes'] == [len(gametes1), len(gametes2)]
		assert counts['genotypes'] == len(offspring)
		assert counts['phenotypes'] == len(phenotypes)
		for kind in ('gametes', 'genotypes', 'phenotypes'):
			answer = counts[kind][0] if kind == 'gametes' else counts[kind]
			choices, key = unique_counts_lib.generate_choices(answer, 2, 5, kind, True)
			assert len(set(choices)) == 5
			assert choices.count(key) == 1


def test_saved_scenario_is_reusable_and_protected(tmp_path: pathlib.Path) -> None:
	"""Saved names and colors render together; invalid data and overwrites fail."""
	scenario = {'parents': [
		{'name': 'First & One', 'name_color': '#663399', 'genotype': ['Aa', 'BB', 'Cc', 'dd']},
		{'name': 'Second <Two>', 'name_color': '#006B5E', 'genotype': ['aa', 'Bb', 'Cc', 'Dd']},
	]}
	path = str(tmp_path / 'cross.json')
	unique_counts_lib.save_scenario(path, scenario)
	loaded = unique_counts_lib.load_scenario(path)
	assert loaded == scenario
	for kind, parent in (('gametes', 1), ('gametes', 2), ('genotypes', 1), ('phenotypes', 1)):
		args = argparse.Namespace(question_type=kind, parent=parent, num_choices=5, hint=True)
		item = unique_counts_lib.write_question(1, args, loaded)
		document = lxml.html.fromstring(item.question_text)
		shown_parents = [loaded['parents'][parent - 1]] if kind == 'gametes' else loaded['parents']
		for person in shown_parents:
			spans = [span for span in document.iter('span') if span.text == person['name']]
			assert document.xpath('//table//span[text()=$name]', name=person['name'])
			assert document.xpath('//p//span[text()=$name]', name=person['name'])
			assert all(span.get('style') == f"color: {person['name_color']};" for span in spans)
	with pytest.raises(FileExistsError):
		unique_counts_lib.save_scenario(path, scenario)
	invalid = copy.deepcopy(scenario)
	invalid['parents'][1]['genotype'][0] = 'Bb'
	with pytest.raises(ValueError):
		unique_counts_lib.validate_scenario(invalid)
	for color in ('green', '#123', '#006400; background: red', None):
		invalid = copy.deepcopy(scenario)
		invalid['parents'][0]['name_color'] = color
		with pytest.raises(ValueError, match='name_color'):
			unique_counts_lib.validate_scenario(invalid)
	invalid = copy.deepcopy(scenario)
	del invalid['parents'][0]['name_color']
	with pytest.raises(ValueError, match='name_color'):
		unique_counts_lib.validate_scenario(invalid)
