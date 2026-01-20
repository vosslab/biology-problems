
import lib_test_utils


#============================================
def test_yaml_match_to_pgml_header(stub_bptools):
	"""
	Ensure matching PGML output includes an OPL header.
	"""
	module = lib_test_utils.import_from_repo_path(
		"problems/matching_sets/yaml_match_to_pgml.py"
	)
	yaml_data = {
		"matching pairs": {
			"Alpha": ["one", "uno"],
			"Beta": ["two"],
		},
		"keys description": "terms",
		"values description": "definitions",
	}
	pgml_text = module.build_pgml_text(yaml_data, 2)
	assert pgml_text.startswith("## DESCRIPTION")
	assert "## KEYWORDS(" in pgml_text
	assert "## DBsubject(" in pgml_text
	assert "DOCUMENT();" in pgml_text
	assert "PGcourse.pl" in pgml_text
