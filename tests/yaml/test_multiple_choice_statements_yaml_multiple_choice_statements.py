#!/usr/bin/env python3

import random

from lib_test_utils import import_from_repo_path


def test_yaml_multiple_choice_statements_autoAddConflictRules_generates_and_prunes():
	mod = import_from_repo_path("multiple_choice_statements/yaml_multiple_choice_statements.py")

	yaml_data = {
		"true_statements": {
			"truth1a": "T1a",
			"truth1b": "T1b",
			"truth2": "T2",
		},
		"false_statements": {
			"false1a": "F1a",
			"false1b": "F1b",
		},
	}

	mod.autoAddConflictRules(yaml_data)
	conflict_rules = yaml_data["conflict_rules"]

	assert "bool1" in conflict_rules
	assert conflict_rules["bool1"]["truth1a"] is True
	assert conflict_rules["bool1"]["truth1b"] is True
	assert conflict_rules["bool1"]["false1a"] is True
	assert conflict_rules["bool1"]["false1b"] is True

	# truth2 has no false2*, so that base should be pruned (len == 1)
	assert "bool2" not in conflict_rules


def test_yaml_multiple_choice_statements_checkIfConflict_uses_rules():
	mod = import_from_repo_path("multiple_choice_statements/yaml_multiple_choice_statements.py")

	conflict_rules = {
		"bool1": {"truth1a": True, "false1b": True},
	}
	assert mod.checkIfConflict("truth1a", "false1b", conflict_rules) is True
	assert mod.checkIfConflict("truth2", "false1b", conflict_rules) is False


def test_yaml_multiple_choice_statements_filterOpposingStatements_groups_conflicts():
	mod = import_from_repo_path("multiple_choice_statements/yaml_multiple_choice_statements.py")

	conflict_rules = {
		"bool1": {"truth1a": True, "false1": True, "false1a": True},
		"bool3": {"false3": True, "false3a": True},
	}
	opposing_tree = {
		"false1": "F1",
		"false1a": "F1a",
		"false3": "F3",
		"false3a": "F3a",
		"false9": "F9",
	}
	nested = mod.filterOpposingStatements("truth1a", opposing_tree, conflict_rules)

	flat = [s for group in nested for s in group]
	assert "F1" not in flat
	assert "F1a" not in flat
	assert "F3" in flat
	assert "F3a" in flat
	assert "F9" in flat

	lengths = sorted(len(group) for group in nested)
	assert lengths == [1, 2]


def test_yaml_multiple_choice_statements_writeQuestion_overrides_and_default():
	mod = import_from_repo_path("multiple_choice_statements/yaml_multiple_choice_statements.py")

	yaml_data = {
		"topic": "biology",
		"connection_words": ["about"],
		"override_question_true": "<p>TRUE OVERRIDE</p>",
		"override_question_false": "<p>FALSE OVERRIDE</p>",
	}
	assert mod.writeQuestion(yaml_data, True) == "<p>TRUE OVERRIDE</p>"
	assert mod.writeQuestion(yaml_data, False) == "<p>FALSE OVERRIDE</p>"

	yaml_data2 = {
		"topic": "biology",
		"connection_words": ["about"],
	}
	q = mod.writeQuestion(yaml_data2, "maybe")
	assert "<strong>MAYBE</strong>" in q
	assert "biology" in q


def test_yaml_multiple_choice_statements_makeQuestionsFromStatement_calls_formatter(monkeypatch):
	mod = import_from_repo_path("multiple_choice_statements/yaml_multiple_choice_statements.py")

	def fake_format(N, question_text, choices_list, answer_text):
		return f"MC\t{N}\t{answer_text}\t{len(choices_list)}\t{question_text}\n"

	monkeypatch.setattr(mod.bptools, "formatBB_MC_Question", fake_format)
	random.seed(0)

	main_statement = "alpha"
	opposing_nested = [["d1"], ["d2"], ["d3"], ["d4"]]
	question_text = "<p>Which is TRUE?</p>"
	replacement_rules = {"alpha": "ALPHA"}

	questions = mod.makeQuestionsFromStatement(main_statement, opposing_nested, question_text, replacement_rules)
	assert len(questions) >= 1
	for q in questions:
		assert q.startswith("MC\t")
		assert "<strong>ALPHA</strong>" in q
		assert "\t5\t" in q

