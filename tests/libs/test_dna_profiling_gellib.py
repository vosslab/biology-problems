#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_gellib_band_tree_smoke():
	gellib = import_from_repo_path("problems/dna_profiling-problems/gellib.py")
	gel = gellib.GelClass()
	gel.createBandTree(total_bands=10)
	assert isinstance(gel.band_tree, list)
	assert len(gel.band_tree) == 10
	assert gel.max_distance is not None
	assert gel.max_distance > 0


def test_gellib_html_table_helpers():
	gellib = import_from_repo_path("problems/dna_profiling-problems/gellib.py")
	gel = gellib.GelClassHtml()
	gel.createBandTree(total_bands=5)
	widths = gel.tableWidths()
	assert "<table" in widths
	block = gel.tdBlock()
	assert "<td" in block
