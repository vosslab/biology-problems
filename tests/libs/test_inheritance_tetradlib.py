#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_tetradlib_ditype_and_tetratype_helpers():
	tetradlib = import_from_repo_path("problems/inheritance-problems/gene_mapping/tetradlib.py")
	tetradlib.debug = False

	ditype = tetradlib.make_ditype_from_genotype_str("++", "ab")
	assert ditype == ("++", "++", "ab", "ab")

	tetratype = tetradlib.make_tetratype_from_genotype_strings("++", "+b", "ab")
	assert set(tetratype) == {"++", "+b", "a+", "ab"}


def test_tetradlib_all_ditypes_small():
	tetradlib = import_from_repo_path("problems/inheritance-problems/gene_mapping/tetradlib.py")
	tetradlib.debug = False
	all_ditypes = tetradlib.get_all_ditype_tetrads("ab")
	assert len(all_ditypes) == 2
