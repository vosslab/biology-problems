#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_enzymelib_tree_and_html_table():
	enzymelib = import_from_repo_path("biochemistry-problems/enzymelib.py")
	enzyme_tree = enzymelib.makeEnzymeTree(1)
	assert isinstance(enzyme_tree, list)
	assert len(enzyme_tree) == 4
	for entry in enzyme_tree:
		assert set(entry.keys()) == {"name", "optim_pH", "temp1", "temp2"}

	html = enzymelib.makeEnzymeHTMLTable(enzyme_tree)
	assert "<table" in html
	assert "Enzyme" in html
