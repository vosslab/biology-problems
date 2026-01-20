
import random

from lib_test_utils import import_from_repo_path


def test_genemaplib_small_pure_helpers():
	genemaplib = import_from_repo_path("problems/inheritance-problems/gene_mapping/genemaplib.py")
	assert genemaplib.is_almost_integer(5.0000001) is True
	assert genemaplib.is_almost_integer(5.001) is False

	random.seed(0)
	a, b = genemaplib.split_number_in_two(100, 0.5)
	assert a + b == 100
	assert 0 <= a <= 100
	assert 0 <= b <= 100

	assert genemaplib.invert_genotype("+b+d", "abcd") == "a+c+"
	assert genemaplib.flip_gene_by_letter("+b+d", "b", "abcd") == "+++d"
	assert genemaplib.flip_gene_by_index("+b+d", 2, "abcd") == "+++d"
	assert genemaplib.crossover_after_index("++++", 2, "adcb") == "+bc+"
