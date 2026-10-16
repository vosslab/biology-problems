
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
	assert "BEGIN_PGML" in pgml_text
	assert "ENDDOCUMENT();" in pgml_text
	assert "PGcourse.pl" in pgml_text


#============================================
def test_yaml_generators_preserve_apostrophes(stub_bptools):
	"""PG doubles backslashes, so escaped apostrophes break executable literals."""
	match = lib_test_utils.import_from_repo_path(
		"problems/matching_sets/yaml_match_to_pgml.py"
	)
	which = lib_test_utils.import_from_repo_path(
		"problems/matching_sets/yaml_which_one_mc_to_pgml.py"
	)
	term = "Mendel's law"
	definition = "an organism's inheritance"
	outputs = [
		match.render_match_data({term: [definition]}),
		match.render_exclude_pairs([(term, definition)]),
		match.build_statement_text(term, definition, False, "none", {}, False),
		which.build_setup_text([{
			"item_name": term,
			"plural_choice_description": definition,
			"singular_item_description": term,
			"choices": [definition],
			"correct": definition,
		}]),
	]
	for output in outputs:
		assert term in output
		assert definition in output
		assert "\\'" not in output
