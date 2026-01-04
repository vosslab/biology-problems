#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_metaboliclib_letters_and_pathway_html():
	metaboliclib = import_from_repo_path("biochemistry-problems/metaboliclib.py")
	letters = metaboliclib.get_letters(3, shift=0)
	assert len(letters) == 3
	assert "A" in letters[0]
	assert "B" in letters[1]
	assert "C" in letters[2]

	html = metaboliclib.generate_metabolic_pathway(4, shift=0)
	assert "<table" in html
	assert "&xrarr;" in html
