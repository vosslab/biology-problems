#!/usr/bin/env python3

import random

from lib_test_utils import import_from_repo_path


def test_pedigree_mode_validate_lib_roundtrip():
	pedigree_graph_parse_lib = import_from_repo_path("inheritance-problems/pedigrees/pedigree_graph_parse_lib.py")
	pedigree_inheritance_lib = import_from_repo_path("inheritance-problems/pedigrees/pedigree_inheritance_lib.py")
	pedigree_mode_validate_lib = import_from_repo_path("inheritance-problems/pedigrees/pedigree_mode_validate_lib.py")
	pedigree_skeleton_lib = import_from_repo_path("inheritance-problems/pedigrees/pedigree_skeleton_lib.py")

	mode = "autosomal dominant"
	rng = random.Random(3)
	graph = pedigree_skeleton_lib.generate_basic_three_gen_graph(rng=rng)
	pedigree_inheritance_lib.assign_phenotypes(graph, mode, rng=random.Random(3), show_carriers=True)
	code = pedigree_graph_parse_lib.render_graph_to_code(graph, show_carriers=True)
	errors = pedigree_mode_validate_lib.validate_mode_from_code(code, mode, allow_de_novo=True)
	assert errors == []
