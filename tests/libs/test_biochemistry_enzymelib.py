
from lib_test_utils import import_from_repo_path


def test_enzymelib_tree_and_html_table():
	enzymelib = import_from_repo_path("problems/biochemistry-problems/enzymes/enzymelib.py")
	enzyme_tree = enzymelib.makeEnzymeTree(1)
	assert isinstance(enzyme_tree, list)

	html = enzymelib.makeEnzymeHTMLTable(enzyme_tree)
	assert "<table" in html
	assert "Enzyme" in html
