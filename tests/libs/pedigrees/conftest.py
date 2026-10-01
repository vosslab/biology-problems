"""Import the pedigree package using the same directory as its three commands."""

import sys
import pathlib

import file_utils

PEDIGREE_ROOT = pathlib.Path(file_utils.get_repo_root()) / 'problems/inheritance-problems/pedigrees'
sys.path.insert(0, str(PEDIGREE_ROOT))
