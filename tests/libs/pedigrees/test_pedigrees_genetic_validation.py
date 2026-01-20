
from lib_test_utils import import_from_repo_path


def test_genetic_validation_xlr_flags_unaffected_daughter_of_affected_father():
	genetic_validation = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_validation.py"
	)
	mode_validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py"
	)

	code_string = "xTo%.|%.o."
	individuals, couples, _ = mode_validate.parse_pedigree_graph(code_string)
	errors = genetic_validation.validate_x_linked_recessive_constraints(
		individuals,
		couples,
		carriers_visible=True,
	)

	assert errors
	assert any("unaffected female with affected father" in error for error in errors)


def test_validation_xlr_unaffected_daughter_of_affected_father_allowed_when_carriers_hidden():
	genetic_validation = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_validation.py"
	)
	mode_validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py"
	)

	code_string = "xTo%.|%.o."
	individuals, couples, _ = mode_validate.parse_pedigree_graph(code_string)
	errors = genetic_validation.validate_x_linked_recessive_constraints(
		individuals,
		couples,
		carriers_visible=False,
	)

	assert errors == []


def test_genetic_validation_xld_flags_affected_female_with_unaffected_parents():
	genetic_validation = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_validation.py"
	)
	mode_validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py"
	)

	code_string = "#To%.|.%.*"
	individuals, couples, carriers_visible = mode_validate.parse_pedigree_graph(code_string)
	errors = genetic_validation.validate_x_linked_dominant_constraints(individuals, couples)

	assert errors
	assert any("affected female with unaffected parents" in error for error in errors)


def test_genetic_validation_xld_flags_unaffected_daughter_of_affected_father():
	genetic_validation = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_validation.py"
	)
	mode_validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py"
	)

	code_string = "xTo%.|%.o."
	individuals, couples, carriers_visible = mode_validate.parse_pedigree_graph(code_string)
	errors = genetic_validation.validate_x_linked_dominant_constraints(individuals, couples)

	assert errors
	assert any("unaffected female with affected father" in error for error in errors)


def test_genetic_validation_yl_allows_clean_father_son_chain():
	genetic_validation = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_validation.py"
	)
	mode_validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py"
	)

	code_string = "xTo%.|.%x."
	individuals, couples, carriers_visible = mode_validate.parse_pedigree_graph(code_string)
	errors = genetic_validation.validate_y_linked_constraints(individuals, couples)

	assert errors == []


def test_genetic_validation_yl_flags_affected_son_with_unaffected_father():
	genetic_validation = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/genetic_validation.py"
	)
	mode_validate = import_from_repo_path(
		"problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py"
	)

	code_string = "#To%.|%.x."
	individuals, couples, carriers_visible = mode_validate.parse_pedigree_graph(code_string)
	errors = genetic_validation.validate_y_linked_constraints(individuals, couples)

	assert errors
	assert any("affected son of unaffected father" in error for error in errors)
