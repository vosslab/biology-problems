#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_genetic_assignment_carriers_limit_modes():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)
	graph_spec = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/graph_spec.py"
	)

	spec = "F:AmBfc;A-B:Cm"
	pedigree = graph_spec.parse_pedigree_graph_spec(spec)
	modes = genetic_assignment.possible_modes(pedigree)

	assert set(modes) == {
		genetic_assignment.AUTOSOMAL_RECESSIVE,
		genetic_assignment.X_LINKED_RECESSIVE,
	}


def test_genetic_assignment_excludes_xld_with_affected_father_unaffected_daughter():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)
	graph_spec = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/graph_spec.py"
	)

	spec = "F:AmiBf;A-B:Cf"
	pedigree = graph_spec.parse_pedigree_graph_spec(spec)
	modes = genetic_assignment.possible_modes(pedigree)

	assert genetic_assignment.X_LINKED_DOMINANT not in modes


def test_genetic_assignment_y_linked_possible_with_affected_father_and_son():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)
	graph_spec = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/graph_spec.py"
	)

	spec = "F:AmiBf;A-B:Cmi"
	pedigree = graph_spec.parse_pedigree_graph_spec(spec)
	modes = genetic_assignment.possible_modes(pedigree)

	assert genetic_assignment.Y_LINKED in modes
	assert genetic_assignment.X_LINKED_DOMINANT not in modes
	assert genetic_assignment.X_LINKED_RECESSIVE in modes


def test_genetic_assignment_carriers_visible_blocks_unmarked_parents():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmBfDmEf;A-B:Cmi;D-E:Ffc"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert modes == [genetic_assignment.NONE_MODE]


def test_genetic_assignment_y_linked_rejects_affected_female():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmiBf;A-B:CmiDfi"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert genetic_assignment.Y_LINKED not in modes
	assert modes != [genetic_assignment.NONE_MODE]


def test_genetic_assignment_xlr_rejects_male_carrier_allows_ar():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmcBfc;A-B:Cmc"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert genetic_assignment.AUTOSOMAL_RECESSIVE in modes
	assert genetic_assignment.X_LINKED_RECESSIVE not in modes


def test_assignment_xlr_affected_mother_cannot_have_unaffected_son():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmBfi;A-B:Cm"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert genetic_assignment.X_LINKED_RECESSIVE not in modes


def test_assignment_xld_allows_affected_mother_affected_son():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmBfi;A-B:Cmi"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert genetic_assignment.X_LINKED_DOMINANT in modes


def test_assignment_xlr_allows_affected_father_affected_son_if_mother_carrier():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmiBfc;A-B:Cmi"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert genetic_assignment.X_LINKED_RECESSIVE in modes


def test_assignment_ar_two_affected_parents_cannot_have_unaffected_child():
	genetic_assignment = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_assignment.py"
	)

	spec = "F:AmiBfi;A-B:Cm"
	modes = genetic_assignment.possible_modes_from_spec(spec)

	assert genetic_assignment.AUTOSOMAL_RECESSIVE not in modes
