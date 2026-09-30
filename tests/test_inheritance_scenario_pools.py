import random
import argparse

import pytest
import bptools
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


@pytest.mark.parametrize("filename", [
	"lethal_allele_survival.py",
	"monohybrid_litter_inference.py",
])
@pytest.mark.parametrize("maximum", [None, 3])
def test_main_caps_requests_at_scenario_capacity(
		filename: str, maximum: int | None, monkeypatch: pytest.MonkeyPatch,
		capsys: pytest.CaptureFixture) -> None:
	"""Oversized requests report the shortfall; an explicit smaller cap still wins."""
	module = lib_test_utils.import_from_repo_path(f"problems/inheritance-problems/{filename}")
	capacity = len(module.build_scenarios())
	args = argparse.Namespace(duplicates=capacity + 10, max_questions=maximum)
	monkeypatch.setattr(module, "parse_arguments", lambda: args)
	monkeypatch.setattr(module, "random", random.Random(31415))
	captured = []

	def collect_questions(writer: object, options: argparse.Namespace, outfile: str) -> None:
		captured.append(options.max_questions)

	monkeypatch.setattr(bptools, "collect_and_write_questions", collect_questions)
	module.main()
	assert captured == [capacity if maximum is None else maximum]
	error_text = capsys.readouterr().err
	assert ("unique scenarios are available" in error_text) == (maximum is None)
