
"""Tests for pedigree layout centering and validation.

These tests ensure that:
1. Parents are always centered above their children
2. No negative slot values occur after rendering
3. No slot collisions occur within a generation
4. The founding couple is not pushed to the far left when descendants extend right
"""

import random

from lib_test_utils import import_from_repo_path


def test_parents_centered_above_children_multiple_seeds():
	"""Verify parents are centered above children across many random pedigrees."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	for seed in range(20):
		for generations in [2, 3, 4]:
			rng = random.Random(seed)
			graph = skeleton.generate_skeleton_graph(
				generations=generations,
				rng=rng,
				min_children=2,
				max_children=4,
			)
			graph_parse._assign_slots(graph)

			errors = graph_parse.validate_parents_centered_above_children(graph, tolerance=1)
			assert not errors, (
				f"Centering errors for gens={generations}, seed={seed}: {errors}"
			)


def test_no_negative_slots_after_rendering():
	"""Verify no negative slot values exist after full rendering."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	for seed in range(15):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)
		# render_graph_to_code calls _assign_slots internally
		graph_parse.render_graph_to_code(graph)

		errors = graph_parse.validate_no_negative_slots(graph)
		assert not errors, f"Negative slot errors for seed={seed}: {errors}"


def test_no_slot_collisions():
	"""Verify no two individuals share the same slot in the same generation."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	for seed in range(15):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)
		graph_parse._assign_slots(graph)

		errors = graph_parse.validate_no_slot_collisions(graph)
		assert not errors, f"Slot collision errors for seed={seed}: {errors}"


def test_validate_layout_comprehensive():
	"""Run full layout validation across multiple configurations."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	configs = [
		{'generations': 2, 'min_children': 2, 'max_children': 3},
		{'generations': 3, 'min_children': 2, 'max_children': 4},
		{'generations': 4, 'min_children': 2, 'max_children': 3},
	]

	for seed in range(10):
		for config in configs:
			rng = random.Random(seed)
			graph = skeleton.generate_skeleton_graph(rng=rng, **config)
			graph_parse._assign_slots(graph)

			errors = graph_parse.validate_layout(graph, tolerance=1)
			assert not errors, (
				f"Layout errors for seed={seed}, config={config}: {errors}"
			)


def test_founding_couple_not_at_far_left():
	"""Verify the founding couple is not pushed to column 0 when pedigree is wide."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	for seed in range(20):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)
		code_string = graph_parse.render_graph_to_code(graph)
		lines = code_string.split('%')

		if not lines:
			continue

		# For a properly centered pedigree, if the pedigree is wide,
		# the founding couple should have some leading space (dots)
		first_row = lines[0]
		max_width = max(len(line.rstrip('.')) for line in lines)

		# Only check if the pedigree is reasonably wide
		if max_width > 8:
			first_content_col = len(first_row) - len(first_row.lstrip('.'))
			# The founding couple should not start at column 0 for wide pedigrees
			# unless the children are also near the left
			child_row = lines[2] if len(lines) > 2 else ''
			child_start = len(child_row) - len(child_row.lstrip('.'))

			# Parents should start at or after the leftmost child position
			# (they are centered above children, so they shouldn't be further left)
			assert first_content_col >= child_start - 2, (
				f"Seed {seed}: Founding couple at col {first_content_col} but "
				f"children start at col {child_start}. Code:\n{code_string}"
			)


def test_col_shift_centers_founding_couple():
	"""Verify _compute_col_shift centers the founding couple in asymmetric pedigrees."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	# Generate several pedigrees and verify the founding couple is reasonably centered
	for seed in range(15):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)
		graph_parse._assign_slots(graph)

		min_slot = min(ind.slot for ind in graph.individuals.values() if ind.slot is not None)
		max_slot = max(ind.slot for ind in graph.individuals.values() if ind.slot is not None)
		col_shift = graph_parse._compute_col_shift(graph, min_slot, max_slot)

		# After shift, min column should be >= 0
		assert min_slot + col_shift >= 0, f"Seed {seed}: negative column after shift"

		# Find founding couple
		top_couples = [c for c in graph.couples if c.generation == 1]
		if top_couples:
			tc = top_couples[0]
			pa = graph.individuals[tc.partner_a]
			pb = graph.individuals[tc.partner_b]
			couple_mid = (pa.slot + pb.slot) / 2 + col_shift

			# The couple should have roughly equal space on left and right
			left_space = couple_mid - 0
			right_space = (max_slot + col_shift) - couple_mid

			# Allow some tolerance for integer rounding
			assert abs(left_space - right_space) <= 2, (
				f"Seed {seed}: couple not centered, left={left_space}, right={right_space}"
			)


def test_layout_preserved_after_code_generation():
	"""Verify that generating code doesn't break the centered layout."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	for seed in range(10):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=3,
			rng=rng,
			min_children=2,
			max_children=4,
		)

		# Generate code (this assigns slots internally)
		code_string = graph_parse.render_graph_to_code(graph)

		# Validate the graph layout after code generation
		errors = graph_parse.validate_layout(graph, tolerance=1)
		assert not errors, (
			f"Layout broke after code generation, seed={seed}: {errors}\n"
			f"Code:\n{code_string}"
		)


def test_wide_pedigree_centering():
	"""Test that very wide pedigrees maintain proper centering."""
	skeleton = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph_parse = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")

	# Use seeds that tend to produce wider pedigrees
	for seed in range(30):
		rng = random.Random(seed)
		graph = skeleton.generate_skeleton_graph(
			generations=4,
			rng=rng,
			min_children=3,
			max_children=4,
		)

		graph_parse._assign_slots(graph)

		# Check centering for all couples
		errors = graph_parse.validate_parents_centered_above_children(graph, tolerance=1)
		assert not errors, f"Wide pedigree centering failed, seed={seed}: {errors}"
