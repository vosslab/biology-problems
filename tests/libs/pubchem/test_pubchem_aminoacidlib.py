
from lib_test_utils import import_from_repo_path


def test_pubchem_aminoacidlib_formula_parsing():
	pubchem_aminoacidlib = import_from_repo_path("problems/biochemistry-problems/PUBCHEM/aminoacidlib.py")
	assert pubchem_aminoacidlib.parse_formula("C6H12O6") == {"C": 6, "H": 12, "O": 6}
	assert pubchem_aminoacidlib.formula_disimilarity("C6H12O6", "C6H12O6") == 0
