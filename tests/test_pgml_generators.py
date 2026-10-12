from lib_test_utils import import_from_repo_path


def test_yaml_which_one_mc_to_pgml_inline_colors():
	module = import_from_repo_path("problems/matching_sets/yaml_which_one_mc_to_pgml.py")

	yaml_data = {
		"matching pairs": {
			"enzyme": ["catalyst", "protein"],
			"substrate": ["reactant"],
		},
		"keys description": "terms",
		"values description": "definitions",
		"key description": "term",
		"value description": "definition",
		"replacement_rules": {
			"enzyme": "<span style=\"color: #e60000;\">enzyme</span>",
		},
	}

	pgml_text, warnings = module.build_pgml_text(yaml_data, 2, False, "inline")

	assert "DOCUMENT();" in pgml_text
	assert "BEGIN_PGML" in pgml_text
	assert "ENDDOCUMENT();" in pgml_text
	assert "color: #e60000" in pgml_text
	assert "enzyme</span>" in pgml_text
	assert warnings == []


def test_yaml_mc_statements_to_pgml_inline_colors():
	module = import_from_repo_path("problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py")

	yaml_data = {
		"topic": "ATP",
		"true_statements": {
			"truth1a": "ATP stores energy",
		},
		"false_statements": {
			"false1a": "ATP is a lipid",
		},
		"replacement_rules": {
			"ATP": "<span style=\"color: #e60000;\">ATP</span>",
		},
	}

	pgml_text, warnings = module.build_pgml_text(yaml_data, "inline")

	assert "color: #e60000" in pgml_text
	assert "ATP</span> stores energy" in pgml_text
	assert warnings == []
