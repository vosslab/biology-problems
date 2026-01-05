#!/usr/bin/env python3

import random
import re

from lib_test_utils import import_from_repo_path


def test_yaml_to_pg_norm_and_uniq():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")
	assert mod.norm("  A  B ") == "a b"
	assert mod.uniq(["A", " a ", "B", "b"]) == ["A", "B"]


def test_yaml_to_pg_apply_replacements_longest_first_and_no_rereplace():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")

	rules = {"foo bar": "X", "foo": "Y"}
	assert mod.apply_replacements("foo bar", rules) == "X"

	# Ensure replacement text isn't scanned for further replacements.
	text = "cat dog"
	rules2 = {"cat": "<b>cat</b>", "dog": "cat"}
	out = mod.apply_replacements(text, rules2)
	assert out == "<b>cat</b> cat"


def test_yaml_to_pg_family_id_and_group_by_family_dedup():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")
	assert mod.family_id("truth1a") == 1
	assert mod.family_id("false 12") == 12
	assert mod.family_id("other") == -1

	grouped = mod.group_by_family({
		"truth1": "A",
		"truth1a": " a ",
		"truth2": "B",
		"other": "C",
	})
	assert sorted(grouped.keys()) == [1, 2]
	assert len(grouped[1]) == 1
	assert grouped[1][0][1] == "A"


def test_yaml_to_pg_esc_pg_single_escapes_backslash_and_quote():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")
	out = mod.esc_pg_single(r"back\slash 'quote'")
	assert "\\\\" in out
	assert "\\'" in out


def test_yaml_to_pg_mc_part_block_caps_and_includes_correct():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")
	random.seed(0)
	block = mod.mc_part_block(
		1,
		"<p>Prompt</p>",
		["a", "b", "c", "d", "e", "f", "a", "b"],
		"c",
	)
	assert "RadioButtons(" in block
	assert "ANS( $rb_1->cmp() );" in block
	assert "Prompt" in block
	assert "c" in block

	m = re.search(r"my @choices_1 = \((.*)\);", block)
	assert m is not None
	inside = m.group(1)
	# Count perl string literals in the array.
	assert inside.count("'") // 2 <= 5


def test_yaml_to_pg_pick_distractors_avoids_family_and_dedups():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")
	rng = random.Random(0)
	out = mod.pick_distractors_from_opposite_pool({1: ["a", "b"], 2: ["c", " c "], 3: ["d"]}, 1, 2, rng)
	assert len(out) == 2
	assert all(x.strip().lower() not in ("a", "b") for x in out)
	assert len({x.strip().lower() for x in out}) == 2


def test_yaml_to_pg_build_every_statement_items_basic_shape():
	mod = import_from_repo_path("multiple_choice_statements/yaml_to_pg.py")
	data = {
		"topic": "cells",
		"connection_words": ["about"],
		"replacement_rules": {"CELL": "cell"},
		"true_statements": {
			"truth1": "Cells have membranes.",
			"truth2": "Cells contain water.",
			"truth3": "Cells can divide.",
			"truth4": "Cells contain DNA.",
			"truth5": "Cells have ribosomes.",
		},
		"false_statements": {
			"false6": "Cells are made of rocks.",
			"false7": "Cells have no chemistry.",
			"false8": "Cells do not contain carbon.",
			"false9": "Cells cannot be observed.",
			"false10": "Cells are always square.",
		},
	}
	rng = random.Random(0)
	items = mod.build_every_statement_items(data, rng, choices_per_q=5)
	assert len(items) == 10
	for prompt, choices, correct in items:
		assert isinstance(prompt, str)
		assert len(choices) == 5
		assert correct in choices
