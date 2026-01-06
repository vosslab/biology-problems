#!/usr/bin/env python3

import pytest

from lib_test_utils import import_from_repo_path


def _import_sugarlib():
	return import_from_repo_path("problems/biochemistry-problems/carbohydrates_classification/sugarlib.py")


def test_sugarlib_validation_and_coloring():
	sugarlib = _import_sugarlib()
	assert sugarlib.validate_sugar_code("ARLRRDM") is True
	assert sugarlib.validate_sugar_code("MKM") is True
	assert sugarlib.validate_sugar_code("MRKRM") is True

	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("BRLRRDM")
	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("ARLRRD")
	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("ADRM")
	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("ARDRRDM")

	colored = sugarlib.color_question_choices(["hexose (6)", "foo"])
	assert "color:" in colored[0]
	assert colored[1] == "foo"


def test_sugarlib_sugarcodes_enantiomer_mapping():
	sugarlib = _import_sugarlib()
	sugar_codes = sugarlib.SugarCodes()

	d_code = sugar_codes.sugar_name_to_code["D-glucose"]
	l_code = sugar_codes.get_enantiomer_code_from_code(d_code)
	assert sugar_codes.sugar_code_to_name[l_code] == "L-glucose"
	assert sugar_codes.get_enantiomer_code_from_name("D-glucose") == l_code


def test_sugarlib_get_sugar_names_filters():
	sugarlib = _import_sugarlib()
	sugar_codes = sugarlib.SugarCodes()

	aldo_d_hexoses = sugar_codes.get_sugar_names(6, configuration="D", types="aldo")
	assert aldo_d_hexoses
	for name in aldo_d_hexoses:
		code = sugar_codes.sugar_name_to_code[name]
		assert len(code) == 6
		assert code[0] == "A"
		assert code[-2] == "D"

	keto_hexoses = sugar_codes.get_sugar_names(6, configuration="all", types="keto")
	assert keto_hexoses
	for name in keto_hexoses:
		code = sugar_codes.sugar_name_to_code[name]
		assert len(code) == 6
		assert code[0] == "M"
		assert code[1] == "K"


def test_sugarlib_flip_position_and_formula():
	sugarlib = _import_sugarlib()
	sugar_codes = sugarlib.SugarCodes()

	d_code = sugar_codes.sugar_name_to_code["D-glucose"]
	flipped = sugar_codes.flip_position(d_code, len(d_code) - 1)
	assert flipped[-2] == "L"
	assert flipped[:-2] == d_code[:-2]
	assert sugar_codes.sugar_code_to_name[flipped].startswith("L-")

	with pytest.raises(ValueError):
		sugar_codes.flip_position(d_code, 1)
	with pytest.raises(ValueError):
		sugar_codes.flip_position(d_code, len(d_code))

	d_struct = sugarlib.SugarStructure(d_code)
	assert d_struct.molecular_formula_txt().strip() == "C6 H12 O6"
