#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_restrictlib_good_ending_and_strict_sequence():
	restrictlib = import_from_repo_path("problems/molecular_biology-problems/restrictlib.py")
	assert restrictlib.check_for_good_ending("EcoRI") is True
	assert restrictlib.check_for_good_ending("Eco_mut1") is True
	assert restrictlib.check_for_good_ending("Eco_3") is True
	assert restrictlib.check_for_good_ending("Eco") is False

	enzyme_class = restrictlib.enzyme_name_to_class("EcoRI")
	assert restrictlib.has_strict_sequence(enzyme_class) is True
