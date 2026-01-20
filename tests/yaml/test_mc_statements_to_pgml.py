
import lib_test_utils


#============================================
def test_yaml_mc_statements_to_pgml_header():
	"""
	Ensure MC statements PGML output includes an OPL header.
	"""
	module = lib_test_utils.import_from_repo_path(
		"problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py"
	)
	yaml_data = {
		"topic": "cell division",
		"true_statements": {
			"truth1a": "Mitosis produces two genetically identical cells.",
		},
		"false_statements": {
			"false1a": "Mitosis reduces chromosome number by half.",
		},
	}
	pgml_text = module.build_pgml_text(yaml_data)
	assert pgml_text.startswith("## DESCRIPTION")
	assert "## KEYWORDS(" in pgml_text
	assert "## DBsubject(" in pgml_text
	assert "DOCUMENT();" in pgml_text
	assert "PGcourse.pl" in pgml_text
