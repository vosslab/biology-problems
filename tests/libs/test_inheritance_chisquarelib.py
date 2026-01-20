
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
