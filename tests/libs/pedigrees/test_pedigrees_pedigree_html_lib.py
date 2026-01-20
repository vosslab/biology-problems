
from lib_test_utils import import_from_repo_path


def test_pedigree_html_lib_make_html():
	pedigree_html_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/html_output.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	html = pedigree_html_lib.make_pedigree_html(sample_code)
	assert "<table" in html


def test_pedigree_html_debug_comment_with_graph_spec():
	"""Verify that graph spec is included as HTML comment when provided."""
	pedigree_html_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/html_output.py")

	code_string = "#To%|.%xo"
	graph_spec = "F:AmBf;A-B:CmDf"
	html = pedigree_html_lib.translateCode(code_string, debug_spec=graph_spec)

	# Should contain pedigree_graph_spec comment
	assert "pedigree_graph_spec:" in html
	assert graph_spec in html


def test_pedigree_html_no_comment_without_graph_spec():
	"""Verify no debug comment is added when graph spec is not provided."""
	pedigree_html_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/html_output.py")

	code_string = "#To%|.%xo"
	html = pedigree_html_lib.translateCode(code_string)

	# Should NOT contain pedigree_graph_spec comment
	assert "pedigree_graph_spec:" not in html
