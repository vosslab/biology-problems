#!/usr/bin/env python3

import pytest

from lib_test_utils import import_from_repo_path


def test_sugarlib_validation_and_coloring():
	sugarlib = import_from_repo_path("problems/biochemistry-problems/carbohydrates_classification/sugarlib.py")
	assert sugarlib.validate_sugar_code("ARLRRDM") is True
	assert sugarlib.validate_sugar_code("MKM") is True

	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("BRLRRDM")
	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("ARLRRD")
	with pytest.raises(ValueError):
		sugarlib.validate_sugar_code("ADRM")

	colored = sugarlib.color_question_choices(["hexose (6)", "foo"])
	assert "color:" in colored[0]
	assert colored[1] == "foo"
