#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
from lib_test_utils import import_from_repo_path


#===============================
def load_pedigree_libs():
	graph_parse = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py"
	)
	inheritance = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/inheritance_assign.py"
	)
	skeleton = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py"
	)
	validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/validation.py"
	)
	return graph_parse, inheritance, skeleton, validate


#===============================
def test_layout_smoke():
	"""
	Generate a simple three-generation pedigree and print the code string.
	"""
	graph_parse, inheritance, skeleton, validate = load_pedigree_libs()
	rng = random.Random(7)
	graph = skeleton.generate_basic_three_gen_graph(rng=rng)
	inheritance.assign_phenotypes(graph, "autosomal recessive", rng, False)
	code_string = graph_parse.render_graph_to_code(graph, show_carriers=False)
	errors = validate.validate_code_string_strict(code_string, max_width_cells=60, max_height_cells=20)
	assert errors == []


#===============================
## THE END
