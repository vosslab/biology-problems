#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_proteinlib_midpoint_and_peak():
	proteinlib = import_from_repo_path("problems/biochemistry-problems/proteinlib.py")
	protein1 = {"pI": 6.0}
	protein2 = {"pI": 8.0}
	assert proteinlib.get_midpoint_pH(protein1, protein2) == 7.0

	protein3 = {"pI": 5.0}
	protein4 = {"pI": 9.0}
	best_peak, other_peak = proteinlib.get_peak_pH(protein3, protein4)
	assert (best_peak, other_peak) == (10.0, 4.0)


def test_proteinlib_parse_file_smoke():
	proteinlib = import_from_repo_path("problems/biochemistry-problems/proteinlib.py")
	tree = proteinlib.parse_protein_file()
	assert isinstance(tree, list)
	assert len(tree) > 0
	assert "pI" in tree[0]
