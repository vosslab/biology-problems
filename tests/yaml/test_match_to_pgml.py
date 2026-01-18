#!/usr/bin/env python3

import importlib.util
import pathlib
import sys
import types


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB_PATH = REPO_ROOT / "tests" / "lib_test_utils.py"
spec = importlib.util.spec_from_file_location("lib_test_utils", LIB_PATH)
lib_test_utils = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(lib_test_utils)


#============================================
def _stub_bptools():
	"""
	Create a minimal bptools stub for PGML generator imports.
	"""
	module = types.ModuleType("bptools")

	def applyReplacementRulesToText(text_string, replacement_rules):
		return text_string

	def applyReplacementRulesToList(list_of_text_strings, replacement_rules):
		return list_of_text_strings

	module.applyReplacementRulesToText = applyReplacementRulesToText
	module.applyReplacementRulesToList = applyReplacementRulesToList
	return module


#============================================
def test_yaml_match_to_pgml_header():
	"""
	Ensure matching PGML output includes an OPL header.
	"""
	sys.modules["bptools"] = _stub_bptools()
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
