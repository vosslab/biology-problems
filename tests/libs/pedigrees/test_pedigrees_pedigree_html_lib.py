#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_html_lib_make_html():
	pedigree_html_lib = import_from_repo_path("inheritance-problems/pedigrees/pedigree_html_lib.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	html = pedigree_html_lib.make_pedigree_html(sample_code)
	assert "<table" in html
