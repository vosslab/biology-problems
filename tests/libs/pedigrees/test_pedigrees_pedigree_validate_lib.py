#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_validate_lib_smoke():
	pedigree_validate_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_validate_lib.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	assert pedigree_validate_lib.validate_code_string(sample_code) == []
	assert pedigree_validate_lib.is_valid_code_string(sample_code) is True

	assert pedigree_validate_lib.is_valid_code_string("!bad") is False
