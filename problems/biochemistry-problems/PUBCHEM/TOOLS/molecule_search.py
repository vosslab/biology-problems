#!/usr/bin/env python3

import os
import sys

import bptools

def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

import pubchemlib

def main():
	for o in range(3):  # 0-2 oxygens
		for n in range(3):  # 0-2 nitrogens
			max_hydrogens = 6 - (o*2 + n)  # Estimate max hydrogens based on molecular knowledge
			for h in range(max_hydrogens + 1):
				# Construct the formula string
				elements = [("C", 2), ("H", h), ("O", o), ("N", n)]
				formula = "".join(f"{element}{count}" for element, count in elements if count > 0)
				cids = pubchemlib.get_cids_for_formula(formula)
				if cids:
					chemical_names = [pubchemlib.get_chemical_name(cid) for cid in cids]
					print(f"For formula {formula}, found names: {', '.join(chemical_names)}")
					sys.exit(1)
				else:
					print(f"No compounds found for formula {formula}")


if __name__ == "__main__":
	main()
