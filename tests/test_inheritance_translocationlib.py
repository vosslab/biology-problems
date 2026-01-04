#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_translocationlib_draw_helpers():
	translocationlib = import_from_repo_path("inheritance-problems/translocation/translocationlib.py")
	html = translocationlib.draw_meiosis_chromosome(13)
	assert "<table" in html
	assert "13" in html

	merged = translocationlib.merge_tables([html, html])
	assert merged.count('<td align="left">') == 2
