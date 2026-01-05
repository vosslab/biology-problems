#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_graph_spec_lib_parse_and_format():
	pedigree_graph_spec_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_lib/graph_spec.py")
	spec = pedigree_graph_spec_lib.parse_pedigree_graph_spec("F:AmBf;A-B:Cm")
	assert spec.main_couple == ("A", "B")
	assert spec.people["A"].sex == "male"
	assert spec.people["B"].sex == "female"
	assert spec.people["C"].sex == "male"

	formatted = pedigree_graph_spec_lib.format_pedigree_graph_spec(spec)
	assert formatted.startswith("F:")
	assert "A-B:" in formatted
