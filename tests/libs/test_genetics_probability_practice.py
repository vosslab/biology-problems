"""Protect chi-square arithmetic used by quiz answer keys."""

import fractions
import unittest.mock

import lib_test_utils


def test_dice_counts_keep_six_outcomes_and_the_expected_total() -> None:
	module = lib_test_utils.import_from_repo_path(
		"problems/chi_square/chi2-analyze_dice.py")
	# The video example retains all six distinct face counts.
	data = module.dice_data(6, [-4, -2, 2, 3, -3, 4])
	assert data["observed"] == [2, 4, 8, 9, 3, 10]
	assert sum(data["observed"]) == data["total"]
	assert data["expected"] == fractions.Fraction(data["total"], 6)


def test_quiz_arithmetic_is_supplied_without_duplicate_answer_values() -> None:
	module = lib_test_utils.import_from_repo_path(
		"problems/chi_square/chi2-analyze_dice.py")
	options = [("72/6", 12), ("72/5", fractions.Fraction(72, 5)),
		("72/2", 36), ("6+6", 12), ("rounded duplicate", fractions.Fraction(12001, 1000)),
		("lower", 6), ("lowest", 1)]
	with unittest.mock.patch.object(module.bptools, "formatBB_MC_Question") as formatter:
		module.arithmetic_question(1, "<p>Expected count?</p>", options)
	_, _, choices, answer = formatter.call_args.args
	assert len(choices) == 5
	assert "72/6" in answer and "<strong>12</strong>" in answer
	assert all("=" in choice for choice in choices)
	assert sum("<strong>12</strong>" in choice for choice in choices) == 1
	assert all("duplicate" not in choice for choice in choices)


def test_numeric_choices_can_place_the_key_at_every_feasible_rank() -> None:
	module = lib_test_utils.import_from_repo_path(
		"problems/chi_square/chi2-analyze_dice.py")
	# Binary/four-row carryover, two subtractions, no subtraction, double-counting,
	# and counting rolls supply plausible values on both sides of the correct df.
	options = [(str(value), value) for value in (5, 1, 3, 4, 6, 12, 59)]
	for lower_count in range(4):
		with unittest.mock.patch.object(module.random, "choice", return_value=lower_count):
			selected = module.select_options(options, 4)
		values = [value for expression, value in selected]
		assert values[lower_count] == 5
		assert values == sorted(values)


def test_row_choices_evaluate_the_requested_face_and_supply_exact_work() -> None:
	module = lib_test_utils.import_from_repo_path(
		"problems/chi_square/chi2-analyze_dice.py")
	data = module.dice_data(10, [4, -4, 0, 0, 0, 0])
	for face in (1, 2):
		options = module.row_calc_options(data, face)
		assert options[0][1] == fractions.Fraction(8, 5)
		assert "16" in options[0][0] and "&frasl;" in options[0][0]
		with unittest.mock.patch.object(module.bptools, "formatBB_MC_Question") as formatter:
			module.arithmetic_question(1, "<p>Face contribution?</p>", options, fixed_decimals=True)
		_, _, choices, answer = formatter.call_args.args
		assert len(choices) == 5
		assert "<strong>1.60</strong>" in answer
		assert sum("<strong>1.60</strong>" in choice for choice in choices) == 1
	# Matching counts and zero observations remain in tables, but cannot be target rows.
	data = module.dice_data(6, [-6, -1, 0, 0, 1, 6])
	assert module.target_faces(data) == [6]
