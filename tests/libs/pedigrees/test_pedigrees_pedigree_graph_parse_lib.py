#!/usr/bin/env python3

import random
import os

from lib_test_utils import import_from_repo_path
from lib_test_utils import repo_root
from lib_test_utils import temp_sys_path


def test_pedigree_graph_parse_lib_compile_to_valid_code():
	pedigree_graph_parse_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py")
	pedigree_validate_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_validate_lib.py")

	rng = random.Random(1)
	pedigree_dir = os.path.join(repo_root(), "problems", "inheritance-problems", "pedigrees")
	with temp_sys_path(pedigree_dir):
		spec_string = pedigree_graph_parse_lib.generate_pedigree_graph_spec("autosomal recessive", rng=rng)
		code_string = pedigree_graph_parse_lib.compile_graph_spec_to_code(spec_string, show_carriers=True)
		assert pedigree_validate_lib.validate_code_string(code_string) == []
