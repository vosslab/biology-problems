
import random

from lib_test_utils import import_from_repo_path


def test_pedigree_skeleton_lib_generate_graph_smoke():
	pedigree_skeleton_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph = pedigree_skeleton_lib.generate_skeleton_graph(generations=3, rng=random.Random(1))
	assert graph.generations == 3
	assert len(graph.individuals) > 0
	assert len(graph.couples) > 0


def test_pedigree_skeleton_no_childless_couples():
	"""Verify that skeleton generation never produces couples without children."""
	pedigree_skeleton_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")

	# Test with multiple random seeds to ensure robustness
	for seed in range(10):
		for generations in [2, 3, 4]:
			graph = pedigree_skeleton_lib.generate_skeleton_graph(
				generations=generations,
				rng=random.Random(seed),
				min_children=2,
				max_children=4,
			)
			# Every couple must have at least one child
			for couple in graph.couples:
				assert len(couple.children) > 0, (
					f"Couple {couple.id} has no children (seed={seed}, gens={generations})"
				)
