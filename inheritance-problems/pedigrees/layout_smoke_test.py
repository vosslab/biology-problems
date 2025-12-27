#!/usr/bin/env python3

# Standard Library
import random

# Local repo modules
import pedigree_graph_parse_lib
import pedigree_inheritance_lib
import pedigree_skeleton_lib
import pedigree_validate_lib


#===============================
def main():
	"""
	Generate a simple three-generation pedigree and print the code string.
	"""
	rng = random.Random(7)
	graph = pedigree_skeleton_lib.generate_basic_three_gen_graph(rng=rng)
	pedigree_inheritance_lib.assign_phenotypes(graph, 'autosomal recessive', rng, False)
	code_string = pedigree_graph_parse_lib.render_graph_to_code(graph, show_carriers=False)
	errors = pedigree_validate_lib.validate_code_string_strict(code_string, max_width_cells=60, max_height_cells=20)
	print(f"errors: {errors}")
	print(code_string)


#===============================
if __name__ == '__main__':
	main()

## THE END
