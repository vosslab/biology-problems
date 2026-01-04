#!/usr/bin/env python3

import re

from lib_test_utils import import_from_repo_path


def test_pubchem_moleculelib_crc_and_html_snippets():
	moleculelib = import_from_repo_path("biochemistry-problems/PUBCHEM/moleculelib.py")
	crc = moleculelib.getCrc16_FromString("C6H12O6")
	assert re.match(r"^[0-9a-f]{4}$", crc) is not None

	html = moleculelib.generate_html_for_molecule("C1=CN(C(=O)NC1=O)[Si@H]", "uracil")
	assert "<canvas" in html
	assert "initRDKitModule" in html
