#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_code_lib_helpers():
	code_definitions = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/code_definitions.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	assert code_definitions.count_generations(sample_code) == 3
	assert code_definitions.mirror_pedigree(sample_code).count("%") == sample_code.count("%")
