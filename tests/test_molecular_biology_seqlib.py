#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_seqlib_core_functions():
	seqlib = import_from_repo_path("molecular_biology-problems/seqlib.py")
	assert seqlib.complement("ATGC") == "TACG"
	assert seqlib.flip("ATGC") == "CGTA"
	assert seqlib.reverse_complement("ATGC") == "GCAT"
	assert seqlib.insertCommas("ATGC", separate=2) == "AT,GC"
	assert seqlib.transcribe("ATGC") == "AUGC"
	assert seqlib.translate("AUGGCU") == "MA"
