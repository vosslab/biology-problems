
from lib_test_utils import import_from_repo_path


def test_hybridcrosslib_color_sets_and_tables_smoke():
	hybridcrosslib = import_from_repo_path("problems/inheritance-problems/hybridcrosslib.py")
	three_sets = hybridcrosslib.get_three_color_sets()
	assert len(three_sets) > 0
	assert all(len(s) == 3 for s in three_sets)

	four_sets = hybridcrosslib.get_four_color_sets()
	assert len(four_sets) > 0
	assert all(len(s) == 4 for s in four_sets)

	html = hybridcrosslib.createSingleGeneTable("complete dominance", "A", ["tomato", "orange", "yellow"])
	assert "<table" in html
