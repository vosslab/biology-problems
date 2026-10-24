"""Protect chi-square arithmetic used by quiz answer keys."""

import fractions
import unittest.mock

import lib_test_utils


def test_dice_counts_and_terms_determine_the_decision():
	module = lib_test_utils.import_from_repo_path(
		"problems/chi_square/chi2-analyze_dice.py")
	# Video example guards against copying its rounded 9.6 or using six df.
	data = module.dice_data(6, [-4, -2, 2, 3, -3, 4])
	assert data["observed"] == [2, 4, 8, 9, 3, 10]
	assert data["statistic"] == fractions.Fraction(58, 6)
	assert sum(data["observed"]) == data["total"]
	assert data["reject"] is False
	# Same total, concentrated observations: the decision must change.
	data = module.dice_data(6, [-6, 0, 0, 0, 0, 6])
	assert data["statistic"] == 12
	assert data["reject"] is True


def test_quiz_arithmetic_is_supplied_without_duplicate_answer_values():
	module = lib_test_utils.import_from_repo_path(
		"problems/chi_square/chi2-analyze_dice.py")
	options = [("72 / 6", 12), ("72 / 5", fractions.Fraction(72, 5)),
		("72 / 2", 36), ("6 + 6", 12)]
	with unittest.mock.patch.object(module.bptools, "formatBB_MC_Question") as formatter:
		module.arithmetic_question(1, "<p>Expected count?</p>", options)
	_, _, choices, answer = formatter.call_args.args
	assert len(choices) == 3
	assert "72/6" in answer and "<strong>12</strong>" in answer
	assert all("=" in choice for choice in choices)
	assert sum("<strong>12</strong>" in choice for choice in choices) == 1
