#!/usr/bin/env python3

import random

import bptools
from lib_test_utils import import_from_repo_path


def test_yaml_make_match_sets_permuteMatchingPairs_exclude_pairs_and_replacements(monkeypatch):
	mod = import_from_repo_path("matching_sets/yaml_make_match_sets.py")

	def fake_format(N, question_text, answers_list, matching_list):
		return f"MAT\t{N}\t{question_text}\t{answers_list}\t{matching_list}\n"

	monkeypatch.setattr(bptools, "formatBB_MAT_Question", fake_format)
	random.seed(0)

	yaml_data = {
		"matching pairs": {
			"A": "alpha",
			"B": "beta",
			"C": "gamma",
		},
		"keys description": "letters",
		"values description": "words",
		"items to match per question": 2,
		"exclude pairs": [("A", "B")],
		"replacement_rules": {
			"alpha": "ALPHA",
		},
	}

	questions = mod.permuteMatchingPairs(yaml_data, num_choices=2, max_questions=1)
	assert len(questions) == 2
	assert any("<strong>ALPHA</strong>" in q for q in questions)
	for q in questions:
		assert q.startswith("MAT\t")
		assert "'A', 'B'" not in q
		if "['A'" in q or ", 'A'" in q:
			assert "<strong>ALPHA</strong>" in q
			assert "alpha" not in q


def test_yaml_make_which_one_multiple_choice_makeQuestions2_nonflip_and_flip(monkeypatch):
	mod = import_from_repo_path("matching_sets/yaml_make_which_one_multiple_choice.py")

	def fake_format(N, question_text, choices_list, answer_text):
		return f"MC\t{N}\t{answer_text}\t{choices_list}\t{question_text}\n"

	monkeypatch.setattr(bptools, "formatBB_MC_Question", fake_format)
	random.seed(0)

	yaml_data = {
		"matching pairs": {
			"GeneA": ["Trait1", "Trait2"],
			"GeneB": ["Trait3"],
			"GeneC": ["Trait4"],
		},
		"keys description": "genes",
		"key description": "gene",
		"values description": "traits",
		"value description": "trait",
		"items to match per question": 2,
		"exclude pairs": [("GeneA", "GeneB")],
		"replacement_rules": {
			"Trait1": "TRAIT1",
		},
	}

	qs = mod.makeQuestions2(yaml_data, num_choices=2, flip=False)
	assert len(qs) == 4
	for q in qs:
		assert q.startswith("MC\t")
		# answer is a key when not flipped
		assert "\tGene" in q
		# choices include keys, not values
		assert "GeneA" in q or "GeneB" in q or "GeneC" in q

	# When the answer is GeneA (excluded with GeneB), ensure GeneB isn't in its choices.
	for q in qs:
		if "\tGeneA\t" in q:
			assert "GeneB" not in q

	qs_flip = mod.makeQuestions2(yaml_data, num_choices=2, flip=True)
	assert len(qs_flip) == 4
	for q in qs_flip:
		assert q.startswith("MC\t")
		# answer is a value when flipped
		assert any(trait in q for trait in ("Trait1", "Trait2", "Trait3", "Trait4"))

	# Replacement rules should be applied to answer/choices
	assert any("<strong>TRAIT1</strong>" in q for q in qs_flip)
