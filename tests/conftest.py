#!/usr/bin/env python3

import importlib.util
import os
import sys
import tempfile
import types

import pytest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
	sys.path.insert(0, REPO_ROOT)

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
if TESTS_DIR not in sys.path:
	sys.path.insert(0, TESTS_DIR)

MPLCONFIGDIR_DEFAULT = os.path.join(tempfile.gettempdir(), "mplconfig-biology-problems")
os.makedirs(MPLCONFIGDIR_DEFAULT, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", MPLCONFIGDIR_DEFAULT)


def _ensure_qti_package_maker_on_path():
	if importlib.util.find_spec("qti_package_maker") is not None:
		return

	qti_root = os.path.join(os.path.expanduser("~"), "nsh", "qti_package_maker")
	if not os.path.isdir(qti_root):
		return

	if qti_root not in sys.path:
		sys.path.insert(0, qti_root)


_ensure_qti_package_maker_on_path()


@pytest.fixture
def stub_bptools(monkeypatch):
	"""
	Provide a minimal bptools stub for PGML generator imports.
	"""
	module = types.ModuleType("bptools")

	def applyReplacementRulesToText(text_string, replacement_rules):
		return text_string

	def applyReplacementRulesToList(list_of_text_strings, replacement_rules):
		return list_of_text_strings

	module.applyReplacementRulesToText = applyReplacementRulesToText
	module.applyReplacementRulesToList = applyReplacementRulesToList
	monkeypatch.setitem(sys.modules, "bptools", module)
	return module
