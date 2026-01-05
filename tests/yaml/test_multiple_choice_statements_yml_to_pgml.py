#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_yml_to_pgml_group_statements_sorts_and_groups():
	mod = import_from_repo_path("multiple_choice_statements/yml_to_pgml.py")
	block = {
		"truth2b": "T2b",
		"truth1": "T1",
		"truth2a": "T2a",
		"truth10": "T10",
		"no_digits": "X",
	}
	groups = mod.group_statements(block)
	assert groups[0] == ["T1"]
	assert groups[1] == ["T2b", "T2a"] or groups[1] == ["T2a", "T2b"]
	assert groups[2] == ["T10"]


def test_yml_to_pgml_escape_perl_string_escapes_special_chars():
	mod = import_from_repo_path("multiple_choice_statements/yml_to_pgml.py")
	assert mod.escape_perl_string(None) == ""
	out = mod.escape_perl_string('a\\b "c" $d @e')
	assert "\\\\" in out
	assert '\\"' in out
	assert "\\$" in out
	assert "\\@" in out


def test_yml_to_pgml_perl_array_quotes_are_escaped():
	mod = import_from_repo_path("multiple_choice_statements/yml_to_pgml.py")
	groups = [["He said \"hi\""]]
	out = mod.perl_array("x", groups)
	assert "@x" in out
	assert '\\"hi\\"' in out

