
import random

from lib_test_utils import import_from_repo_path


def test_pedigree_mode_validate_lib_roundtrip():
	pedigree_graph_parse_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py")
	pedigree_inheritance_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/inheritance_assign.py")
	pedigree_mode_validate_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py")
	pedigree_skeleton_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py")

	mode = "autosomal dominant"
	rng = random.Random(3)
	graph = pedigree_skeleton_lib.generate_basic_three_gen_graph(rng=rng)
	pedigree_inheritance_lib.assign_phenotypes(graph, mode, rng=random.Random(3), show_carriers=True)
	code = pedigree_graph_parse_lib.render_graph_to_code(graph, show_carriers=True)
	errors = pedigree_mode_validate_lib.validate_mode_from_code(code, mode)
	assert errors == []
