#!/usr/bin/env python3

import random
from types import SimpleNamespace

from lib_test_utils import import_from_repo_path


def test_sorted_summary_rule():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_sorted_data.py")
	data = list(range(1, 12))
	summary = mod.five_number_summary_odd_exclusive_median(data)
	assert summary == {"min": 1, "q1": 3, "median": 6, "q3": 9, "max": 11}


def test_sorted_build_dataset_positions():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_sorted_data.py")
	random.seed(0)
	data = mod.build_sorted_dataset_11(1, 3, 6, 9, 12)
	assert data == sorted(data)
	assert len(data) == 11
	assert data[0] == 1
	assert data[2] == 3
	assert data[5] == 6
	assert data[8] == 9
	assert data[10] == 12


def test_sorted_generate_choices_contains_answer():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_sorted_data.py")
	data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	choices, answer = mod.generate_choices(data, 4)
	assert len(choices) == 4
	assert answer in choices


def test_unsorted_even_summary_rule():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_unsorted_even.py")
	data = [1, 2, 3, 3, 4, 6, 6, 7, 8, 8, 9, 10]
	summary = mod.five_number_summary_even_median_of_halves(data)
	assert summary == {"min": 1, "q1": 3, "median": 6, "q3": 8, "max": 10}


def test_unsorted_even_dataset_is_strict():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_unsorted_even.py")
	random.seed(1)
	data = mod.generate_dataset_12_unsorted()
	summary = mod.five_number_summary_even_median_of_halves(data)
	assert mod.is_strict(summary)
	assert len(data) == 12


def test_summary_generate_choices_contains_answer():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_summary.py")
	correct = {"min": 1, "q1": 3, "median": 5, "q3": 7, "max": 9}
	choices, answer = mod.generate_choices(correct, 4)
	assert len(choices) == 4
	assert answer in choices


def test_summary_question_text_includes_values():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_summary.py")
	summary = {"min": 2, "q1": 4, "median": 6, "q3": 8, "max": 10}
	text = mod.get_question_text(summary)
	assert "Minimum" in text
	assert "Q1" in text
	assert "Median" in text
	assert "Q3" in text
	assert "Maximum" in text


def test_cdf_quantile_rule():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_cdf.py")
	rows = mod.make_cdf_table_from_breaks([1, 3, 5], [5, 5, 5])
	assert mod.quantile_from_cdf(rows, 1) == 1
	assert mod.quantile_from_cdf(rows, 5) == 1
	assert mod.quantile_from_cdf(rows, 6) == 3
	assert mod.quantile_from_cdf(rows, 10) == 3
	assert mod.quantile_from_cdf(rows, 11) == 5


def test_cdf_generate_problem_is_strict_and_sums_to_40():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_cdf.py")
	random.seed(2)
	rows, summary = mod.generate_cdf_problem()
	assert rows[-1][1] == 40
	assert summary["min"] == rows[0][0]
	assert summary["max"] == rows[-1][0]
	assert mod.is_strict(summary)


def test_cdf_question_text_includes_ranks():
	mod = import_from_repo_path("problems/biostatistics-problems/boxplot_from_cdf.py")
	rows = mod.make_cdf_table_from_breaks([2, 4, 6], [10, 10, 20])
	text = mod.get_question_text(rows)
	assert "k = 10" in text
	assert "k = 20" in text
	assert "k = 30" in text
