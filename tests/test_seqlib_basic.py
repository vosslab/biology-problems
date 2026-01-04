#!/usr/bin/env python3

import importlib.util
import os


def _repo_root() -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _load_seqlib():
	path = os.path.join(_repo_root(), "molecular_biology-problems", "seqlib.py")
	spec = importlib.util.spec_from_file_location("seqlib_for_tests", path)
	assert spec is not None
	assert spec.loader is not None
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def test_reverse_complement_smoke():
	seqlib = _load_seqlib()
	assert seqlib.reverse_complement("ATGCCG") == "CGGCAT"
