#!/usr/bin/env python3

import os
import sys
import importlib.util


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
	sys.path.insert(0, REPO_ROOT)


def _ensure_qti_package_maker_on_path():
	if importlib.util.find_spec("qti_package_maker") is not None:
		return

	qti_root = os.path.join(os.path.expanduser("~"), "nsh", "qti_package_maker")
	if not os.path.isdir(qti_root):
		return

	if qti_root not in sys.path:
		sys.path.insert(0, qti_root)


_ensure_qti_package_maker_on_path()
