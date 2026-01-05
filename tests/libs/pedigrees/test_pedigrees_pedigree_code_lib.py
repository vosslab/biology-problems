#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_code_lib_helpers():
	pedigree_code_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_code_lib.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	assert pedigree_code_lib.count_generations(sample_code) == 3
	assert pedigree_code_lib.mirror_pedigree(sample_code).count("%") == sample_code.count("%")
