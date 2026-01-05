#!/usr/bin/env python3

import random

from lib_test_utils import import_from_repo_path


def test_pedigree_skeleton_lib_generate_graph_smoke():
	pedigree_skeleton_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")
	graph = pedigree_skeleton_lib.generate_skeleton_graph(generations=3, rng=random.Random(1))
	assert graph.generations == 3
	assert len(graph.individuals) > 0
	assert len(graph.couples) > 0
