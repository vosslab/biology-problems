import importlib.util
import sys
import types
from pathlib import Path


def _make_bptools_stub():
	stub = types.SimpleNamespace()

	def apply_replacements(text, rules):
		if text is None:
			return ""
		result = str(text)
		for key, value in (rules or {}).items():
			result = result.replace(str(key), str(value))
		return result

	def apply_replacements_list(values, rules):
		return [apply_replacements(value, rules) for value in values]

	stub.applyReplacementRulesToText = apply_replacements
	stub.applyReplacementRulesToList = apply_replacements_list
	stub.readYamlFile = lambda path: {}
	stub.dark_color_wheel = {}
	stub.get_indices_for_color_wheel = lambda count, size: list(range(count))
	return stub


def _load_module(monkeypatch, name, path):
	monkeypatch.setitem(sys.modules, "bptools", _make_bptools_stub())
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def test_yaml_match_to_pgml_inline_colors(monkeypatch):
	module_path = Path(
		"/Users/vosslab/nsh/biology-problems/problems/matching_sets/yaml_match_to_pgml.py"
	)
	module = _load_module(monkeypatch, "yaml_match_to_pgml_test", module_path)

	yaml_data = {
		"matching pairs": {
			"ionic bond": "salt",
			"covalent bond": "H<sub>2</sub>O",
		},
		"keys description": "bonds",
		"values description": "examples",
		"replacement_rules": {
			"ionic bond": "<span style=\"color: #009900;\">ionic bond</span>",
		},
	}

	pgml_text, warnings = module.build_pgml_text(yaml_data, 2, "inline")

	assert "%answer_html" in pgml_text
	assert "color: #009900" in pgml_text
	assert "H\u2082O" in pgml_text
	assert "[$answers_html[$shuffle" in pgml_text
	assert warnings == []


def test_yaml_which_one_mc_to_pgml_inline_colors(monkeypatch):
	module_path = Path(
		"/Users/vosslab/nsh/biology-problems/problems/matching_sets/yaml_which_one_mc_to_pgml.py"
	)
	module = _load_module(monkeypatch, "yaml_which_one_mc_to_pgml_test", module_path)

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

	assert "Which one of the following [$plural_choice]*" in pgml_text
	assert "<span style=\"color: #e60000;\">enzyme</span>" in pgml_text
	assert "The correct answer is: [$correct]*" in pgml_text
	assert warnings == []


def test_yaml_mc_statements_to_pgml_inline_colors(monkeypatch):
	module_path = Path(
		"/Users/vosslab/nsh/biology-problems/problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py"
	)
	module = _load_module(monkeypatch, "yaml_mc_statements_to_pgml_test", module_path)

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

	assert "$topic = '<span style=\"color: #e60000;\">ATP</span>';" in pgml_text
	assert "<span style=\"color: #e60000;\">ATP</span> stores energy" in pgml_text
	assert warnings == []


def test_pgml_generator_smoke_outputs(tmp_path, monkeypatch):
	match_module = _load_module(
		monkeypatch,
		"yaml_match_to_pgml_smoke",
		Path("/Users/vosslab/nsh/biology-problems/problems/matching_sets/yaml_match_to_pgml.py"),
	)
	which_module = _load_module(
		monkeypatch,
		"yaml_which_one_mc_to_pgml_smoke",
		Path("/Users/vosslab/nsh/biology-problems/problems/matching_sets/yaml_which_one_mc_to_pgml.py"),
	)
	mc_module = _load_module(
		monkeypatch,
		"yaml_mc_statements_to_pgml_smoke",
		Path("/Users/vosslab/nsh/biology-problems/problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py"),
	)

	match_yaml = {
		"matching pairs": {"A": "alpha", "B": "beta"},
		"keys description": "letters",
		"values description": "names",
	}
	match_text, _ = match_module.build_pgml_text(match_yaml, 2, "inline")
	match_path = tmp_path / "match.pgml"
	match_path.write_text(match_text, encoding="utf-8")
	assert "DOCUMENT();" in match_text
	assert "BEGIN_PGML" in match_text
	assert "ENDDOCUMENT();" in match_text

	which_yaml = {
		"matching pairs": {"cat": "mammal", "oak": "tree"},
		"keys description": "items",
		"values description": "categories",
		"key description": "item",
		"value description": "category",
	}
	which_text, _ = which_module.build_pgml_text(which_yaml, 2, False, "inline")
	which_path = tmp_path / "which.pgml"
	which_path.write_text(which_text, encoding="utf-8")
	assert "DOCUMENT();" in which_text
	assert "BEGIN_PGML" in which_text
	assert "ENDDOCUMENT();" in which_text

	mc_yaml = {
		"topic": "cells",
		"true_statements": {"truth1a": "cells have membranes"},
		"false_statements": {"false1a": "cells are rocks"},
	}
	mc_text, _ = mc_module.build_pgml_text(mc_yaml, "inline")
	mc_path = tmp_path / "mc.pgml"
	mc_path.write_text(mc_text, encoding="utf-8")
	assert "DOCUMENT();" in mc_text
	assert "BEGIN_PGML" in mc_text
	assert "ENDDOCUMENT();" in mc_text
