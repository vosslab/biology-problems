#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_label_lib_make_and_validate():
	pedigree_label_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/label_strings.py")
	sample_code = "#To%r^d%#.o"
	positions = {(0, 0): "A", (0, 2): "B", (2, 0): "C", (2, 2): "D"}
	labels = pedigree_label_lib.make_label_string(sample_code, positions)
	assert labels.count("%") == sample_code.count("%")
	assert pedigree_label_lib.validate_label_string(labels, sample_code) == []
