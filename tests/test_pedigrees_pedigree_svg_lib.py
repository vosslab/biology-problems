#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_svg_lib_render_svg_smoke():
	pedigree_svg_lib = import_from_repo_path("inheritance-problems/pedigrees/pedigree_svg_lib.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	svg = pedigree_svg_lib.make_pedigree_svg(sample_code, scale=0.2)
	assert svg.startswith("<svg")
	assert "width=" in svg
