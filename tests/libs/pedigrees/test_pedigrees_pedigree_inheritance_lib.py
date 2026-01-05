#!/usr/bin/env python3

import random

from lib_test_utils import import_from_repo_path


def test_pedigree_inheritance_lib_assign_phenotypes_smoke():
	pedigree_inheritance_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/inheritance_assign.py")
	pedigree_skeleton_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")

	graph = pedigree_skeleton_lib.generate_basic_three_gen_graph(rng=random.Random(2))
	pedigree_inheritance_lib.assign_phenotypes(
		graph,
		"autosomal dominant",
		rng=random.Random(2),
		show_carriers=True,
	)
	assert len(graph.individuals) > 0
