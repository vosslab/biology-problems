#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_pedigree_template_gen_lib_normalize_and_choose():
	pedigree_template_gen_lib = import_from_repo_path("problems/inheritance-problems/pedigrees/pedigree_template_gen_lib.py")
	assert pedigree_template_gen_lib.normalize_mode("ad") == "autosomal dominant"
	assert pedigree_template_gen_lib.normalize_mode("Xr") == "x-linked recessive"

	template = pedigree_template_gen_lib.choose_template("autosomal dominant", generations=4)
	assert template.generations == 4
