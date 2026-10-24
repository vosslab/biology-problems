
import random

from lib_test_utils import import_from_repo_path


def test_chisquarelib_probability_helpers():
	chisquarelib = import_from_repo_path("problems/inheritance-problems/chi_square/chisquarelib.py")
	p_value = chisquarelib.get_p_value(7.81472790325, 3)
	assert abs(p_value - 0.05) < 1e-9
	critical = chisquarelib.get_critical_value(0.05, 3)
	assert abs(critical - 7.81472790325) < 1e-9


def test_chisquarelib_create_observed_progeny_is_deterministic_with_seed():
	chisquarelib = import_from_repo_path("problems/inheritance-problems/chi_square/chisquarelib.py")
	random.seed(0)
	counts = chisquarelib.create_observed_progeny(20, "9:2:4:1")
	assert isinstance(counts, list)
	assert len(counts) == 4
	assert sum(counts) == 20


def test_supplied_tables_preserve_wrong_work_for_any_category_count():
	chisquarelib = import_from_repo_path("problems/inheritance-problems/chi_square/chisquarelib.py")
	for count in (2, 3, 6):
		labels = [f"Biological category {index}" for index in range(count)]
		# The omitted square and incorrect total are intentional student errors.
		rows = [[10, 12, "(12 - 10) / 10", "0.200"] for _ in labels]
		text = chisquarelib.create_data_table(rows + ["999.000"], labels=labels)
		assert all(label in text for label in labels)
		assert text.count('(12 - 10) / 10') == count
		assert '999.000' in text
		assert 'Yellow' not in text


def test_worked_tables_sum_exact_contributions_before_rounding():
	chisquarelib = import_from_repo_path("problems/inheritance-problems/chi_square/chisquarelib.py")
	text = chisquarelib.create_worked_table(
		["One", "Two", "Three", "Four", "Five", "Six"],
		[2, 4, 8, 9, 3, 10], [6] * 6)
	# Rounded row contributions add to 9.668, but the exact total rounds to 9.667.
	assert '16 / 6' in text
	assert '&chi;<sup>2</sup> = 9.667' in text
	assert 'scope="col"' in text and 'scope="row"' in text

	# Fractional expected counts need grouping in the displayed division as well.
	text = chisquarelib.create_worked_table(["Purple", "White"], [1, 2], [1.5, 1.5])
	assert '(1/4) / (3/2)' in text
	assert '&chi;<sup>2</sup> = 0.333' in text


def test_reference_table_supports_requested_degrees_and_tail_probability():
	chisquarelib = import_from_repo_path("problems/inheritance-problems/chi_square/chisquarelib.py")
	text = chisquarelib.make_chi_square_table(degrees_of_freedom=(5,), p_values=(0.05,))
	assert '11.07' in text
	assert '0.05' in text
	assert 'probability in the right tail' in text
