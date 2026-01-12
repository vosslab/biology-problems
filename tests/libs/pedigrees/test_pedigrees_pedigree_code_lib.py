#!/usr/bin/env python3

import random

from lib_test_utils import import_from_repo_path


def test_pedigree_code_lib_helpers():
	code_definitions = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/code_definitions.py")
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	assert code_definitions.count_generations(sample_code) == 3
	assert code_definitions.mirror_pedigree(sample_code).count("%") == sample_code.count("%")


def test_mirror_preserves_connector_alignment():
	"""Verify that mirroring preserves vertical alignment of connectors."""
	code_definitions = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/code_definitions.py")
	validation = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/validation.py")
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	# Generate pedigrees and verify mirroring preserves alignment
	for seed in range(20):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)
		code = graph_parse.render_graph_to_code(graph)

		# Mirror the code
		mirrored = code_definitions.mirror_pedigree(code)

		# Validate the mirrored code has valid connections
		errors = validation.validate_row_parity_semantics(mirrored)
		assert not errors, (
			f"Mirror broke alignment at seed {seed}:\n"
			f"Original: {code}\n"
			f"Mirrored: {mirrored}\n"
			f"Errors: {errors}"
		)


def test_strip_empty_columns():
	"""Verify that empty column stripping removes only fully empty columns."""
	code_definitions = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/code_definitions.py")
	validation = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/validation.py")

	# Test with known empty columns
	code = "#To...#To%r^d...|.%x.*...#"
	stripped = code_definitions.strip_empty_columns(code)

	# Should remove 3 empty columns (positions 3, 4, 5)
	assert stripped == "#To#To%r^d|%x.*#", f"Got: {stripped}"

	# Test that non-empty columns are preserved
	code2 = "#To%r^d%x.*"
	stripped2 = code_definitions.strip_empty_columns(code2)
	assert stripped2 == code2, "Should not modify code with no empty columns"

	# Test that stripped code is still valid
	errors = validation.validate_code_string(stripped)
	assert not errors, f"Stripped code is invalid: {errors}"


def test_strip_empty_columns_preserves_connections():
	"""Verify that empty column stripping preserves connector alignment."""
	code_definitions = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/code_definitions.py")
	validation = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/validation.py")
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	# Generate pedigrees and verify stripping preserves alignment
	for seed in range(20):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)
		code = graph_parse.render_graph_to_code(graph)

		# Code should already be stripped (done in render_graph_to_code)
		# Re-stripping should not change it
		re_stripped = code_definitions.strip_empty_columns(code)
		assert code == re_stripped, (
			f"Code changed on re-strip at seed {seed}:\n"
			f"Original: {code}\n"
			f"Re-stripped: {re_stripped}"
		)

		# Validate the code has valid connections
		errors = validation.validate_row_parity_semantics(code)
		assert not errors, f"Seed {seed}: {errors}"
