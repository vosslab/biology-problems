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
