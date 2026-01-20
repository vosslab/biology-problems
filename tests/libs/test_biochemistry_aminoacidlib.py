
from lib_test_utils import import_from_repo_path


def test_aminoacidlib_structure_and_formula():
	aminoacidlib = import_from_repo_path("problems/biochemistry-problems/aminoacidlib.py")
	aa = aminoacidlib.AminoAcidStructure("ADM")
	assert "C=O" in aa.structural_part_txt()
	assert "CHOH" in aa.structural_part_txt()
	assert "C3" in aa.molecular_formula_txt()
	assert "H6" in aa.molecular_formula_txt()
	assert "O3" in aa.molecular_formula_txt()
