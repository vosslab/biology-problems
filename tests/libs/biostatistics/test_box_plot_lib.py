
from lib_test_utils import import_from_repo_path


def test_median_of_sorted_odd():
	mod = import_from_repo_path("problems/biostatistics-problems/box_plot_lib.py")
	values = [1, 2, 3, 4, 5]
	assert mod.median_of_sorted(values) == 3


def test_median_of_sorted_even():
	mod = import_from_repo_path("problems/biostatistics-problems/box_plot_lib.py")
	values = [1, 2, 3, 4]
	assert mod.median_of_sorted(values) == 2.5


def test_tukey_hinges_odd():
	mod = import_from_repo_path("problems/biostatistics-problems/box_plot_lib.py")
	values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	summary = mod.five_number_summary_tukey_hinges(values)
	assert summary == {"min": 1, "q1": 3.5, "median": 6, "q3": 8.5, "max": 11}


def test_tukey_hinges_even():
	mod = import_from_repo_path("problems/biostatistics-problems/box_plot_lib.py")
	values = [1, 2, 3, 4, 5, 6, 7, 8]
	summary = mod.five_number_summary_tukey_hinges(values)
	assert summary == {"min": 1, "q1": 2.5, "median": 4.5, "q3": 6.5, "max": 8}


def test_nondecreasing_and_ties():
	mod = import_from_repo_path("problems/biostatistics-problems/box_plot_lib.py")
	summary = {"min": 1, "q1": 2, "median": 2, "q3": 4, "max": 4}
	assert mod.is_nondecreasing(summary)
	assert mod.has_tie(summary)


def test_render_boxplot_html_handles_fractional_quartiles():
	mod = import_from_repo_path("problems/biostatistics-problems/box_plot_lib.py")
	summary = {"min": 1, "q1": 2.5, "median": 3, "q3": 3.5, "max": 5}
	html = mod.render_boxplot_html(summary)
	assert "<table" in html
