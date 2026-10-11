"""Permanent contract: distinct assessment items, valid answer choices, finite consumption."""

import random
import argparse
import itertools
from fractions import Fraction

import pytest
import lib_test_utils


@pytest.mark.parametrize("filename", [
	"lethal_allele_survival.py",
	"monohybrid_litter_inference.py",
])
def test_scenario_pool_has_unique_stems_and_stops_at_exhaustion(
		filename: str, monkeypatch: pytest.MonkeyPatch) -> None:
	"""Answer shuffling must never disguise a repeated question setup."""
	module = lib_test_utils.import_from_repo_path(f"problems/inheritance-problems/{filename}")
	monkeypatch.setattr(module, "random", random.Random(31415))
	module.SCENARIOS = module.build_scenarios()
	module.random.shuffle(module.SCENARIOS)
	items = [module.write_question(n, argparse.Namespace())
		for n in range(1, len(module.SCENARIOS) + 1)]
	stems = [item.question_text for item in items]
	assert len(stems) > 0
	assert len(stems) == len(set(stems))
	assert module.write_question(len(items) + 1, argparse.Namespace()) is None
	assert all(item.choices_list.count(item.answer_text) == 1 for item in items)


def test_two_trait_scenarios_require_both_traits_and_match_gamete_counts():
	"""Exclude fixed-trait crosses and verify every retained key independently."""
	module = lib_test_utils.import_from_repo_path(
		"problems/inheritance-problems/dominant_and_X-linked_recessive_variations.py")
	expected = set()
	event_targets = {
		'both': (True, True), 'only_ad': (True, False),
		'only_xlr': (False, True), 'neither': (False, False),
	}
	for ad, xlr, group in itertools.product(
		module.AD_GENOTYPE_CHOICES, module.XLR_GENOTYPE_CHOICES, module.GROUP_TYPES,
	):
		# Enumerate equiprobable gametes, retaining duplicates from homozygotes.
		father_x = (xlr[0][:-1], 'Y')
		mother_x = (xlr[1][:2], xlr[1][2:])
		outcomes = []
		for dad_a, mom_a, dad_x, mom_x in itertools.product(ad[0], ad[1], father_x, mother_x):
			if group == 'sons' and dad_x != 'Y':
				continue
			if group == 'daughters' and dad_x == 'Y':
				continue
			ad_affected = 'A' in (dad_a, mom_a)
			xlr_affected = mom_x == 'Xa' and dad_x in ('Y', 'Xa')
			outcomes.append((ad_affected, xlr_affected))
		# Both phenotypes must be possible at each locus within the requested group.
		if any(len({outcome[locus] for outcome in outcomes}) < 2 for locus in (0, 1)):
			continue
		for event, target in event_targets.items():
			probability = Fraction(outcomes.count(target), len(outcomes))
			if probability in module.ALLOWED_ANSWERS:
				expected.add((ad, xlr, event, group, probability))
	pools = module.scenarios_by_answer()
	actual = {scenario for scenarios in pools.values() for scenario in scenarios}
	assert actual == expected
	assert len(pools) > 1
	assert all(scenarios and all(s[-1] == probability for s in scenarios)
		for probability, scenarios in pools.items())


@pytest.mark.parametrize("female, male, daughter_fraction", [
	("orange", "orange", Fraction(0)),
	("orange", "black", Fraction(1)),
	("black", "orange", Fraction(1)),
	("black", "black", Fraction(0)),
	("tortoiseshell", "orange", Fraction(1, 2)),
	("tortoiseshell", "black", Fraction(1, 2)),
])
def test_tortoiseshell_daughter_and_all_offspring_denominators(
		female, male, daughter_fraction, monkeypatch):
	"""Daughter questions must select female kittens instead of an empty group."""
	module = lib_test_utils.import_from_repo_path(
		"problems/inheritance-problems/x_linked_tortoiseshell.py")
	monkeypatch.setattr(module, "random", random.Random(31415))
	# Daughters inherit their father's color allele. No sons are tortoiseshell
	# in these XX/XY crosses, so the fraction among all kittens is halved.
	for group, expected in (("daughters", daughter_fraction), ("offspring", daughter_fraction / 2)):
		draws = iter((female, male, group))
		monkeypatch.setattr(module.random, "choice", lambda options: next(draws))
		assert module.make_cross() == (female, male, group, expected)
