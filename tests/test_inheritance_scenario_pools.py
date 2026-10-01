"""Permanent contract: distinct assessment items, valid answer choices, finite consumption."""

import random
import argparse

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
