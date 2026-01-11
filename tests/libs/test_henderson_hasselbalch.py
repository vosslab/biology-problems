#!/usr/bin/env python3

import math

from lib_test_utils import import_from_repo_path


def test_henderson_hasselbalch_ph_examples_and_inverses():
	hh = import_from_repo_path("problems/biochemistry-problems/Henderson-Hasselbalch.py")

	# Acid buffer example: acetic acid / sodium acetate
	pH1 = hh.compute_pH_from_pKa_conc(4.76, 0.520, 0.305)
	expected1 = 4.76 + math.log10(0.520 / 0.305)
	assert abs(pH1 - expected1) < 1e-12

	pKa1 = hh.compute_pKa_from_pH_conc(pH1, 0.520, 0.305)
	assert abs(pKa1 - 4.76) < 1e-12

	ratio1 = hh.compute_ratio_from_pH_pKa(pH1, 4.76)
	assert abs(ratio1 - (0.520 / 0.305)) < 1e-12

	# Base buffer example: ethylamine / ethylammonium chloride
	pH2 = hh.compute_pH_from_pKb_conc(3.99, 0.0400, 0.0865)
	expected2 = 14.00 - (3.99 + math.log10(0.0865 / 0.0400))
	assert abs(pH2 - expected2) < 1e-12

	pKb2 = hh.compute_pKb_from_pH_conc(pH2, 0.0400, 0.0865)
	assert abs(pKb2 - 3.99) < 1e-12

	ratio2 = hh.compute_ratio_from_pH_pKb(pH2, 3.99)
	assert abs(ratio2 - (0.0400 / 0.0865)) < 1e-12

