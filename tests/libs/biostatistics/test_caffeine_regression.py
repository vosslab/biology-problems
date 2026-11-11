"""Protect R-squared grading and the nested-model fit relationship."""

import numpy
import pytest
import scipy.stats

from lib_test_utils import import_from_repo_path


@pytest.mark.parametrize("degree", [1, 2])
@pytest.mark.parametrize("sign", [-1, 1])
def test_r_squared_matches_independent_fit(degree, sign):
	lib = import_from_repo_path("problems/biostatistics-problems/regressionlib.py")
	x = numpy.arange(25) / 3 + 3
	y = 72 + sign * 0.4 * (x - 7) ** degree + numpy.sin(x * 3) * 7
	pairs = list(zip(x, y))
	if degree == 1:
		expected = scipy.stats.linregress(x, y).rvalue ** 2
	else:
		predicted = numpy.polyval(numpy.polyfit(x, y, 2), x)
		expected = 1 - sum((y - predicted) ** 2) / sum((y - y.mean()) ** 2)
	actual = lib.r_squared(pairs, degree)
	assert numpy.isclose(actual, expected)
	assert 0 <= actual <= 1
	assert lib.r_squared(pairs, 2) >= lib.r_squared(pairs, 1) - 1e-12


def test_constant_scores_have_no_defined_r_squared():
	lib = import_from_repo_path("problems/biostatistics-problems/regressionlib.py")
	with pytest.raises(ValueError, match="variation"):
		lib.r_squared([(x, 75) for x in range(25)], 1)
