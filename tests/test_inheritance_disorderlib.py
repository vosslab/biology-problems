#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_disorderlib_small_helpers_without_io():
	disorderlib = import_from_repo_path("inheritance-problems/disorderlib.py")
	md = disorderlib.MultiDisorderClass.__new__(disorderlib.MultiDisorderClass)

	assert md.capitalFirstLetterOnly("hello") == "Hello"

	locus = md.breakUpGeneLocus("12p13.1-p12")
	assert locus["arm"] == "short"
	assert locus["chromosome"] == "12"
	assert locus["band"] == "13.1"

	locus2 = md.breakUpGeneLocus("7q31.2")
	assert locus2["arm"] == "long"
	assert locus2["chromosome"] == "7"
	assert locus2["band"] == "31.2"

	short = md.getDisorderShortName({"name": "thing", "abbreviation": "ABC"})
	assert short == "ABC"
