
from lib_test_utils import import_from_repo_path


def test_pubchemlib_format_and_ratio_helpers_without_network():
	pubchemlib = import_from_repo_path("problems/biochemistry-problems/PUBCHEM/pubchemlib.py")
	pcl = pubchemlib.PubChemLib.__new__(pubchemlib.PubChemLib)

	formula_html = pcl.format_molecular_formula("C6H12O6")
	assert "<sub>6</sub>" in formula_html

	assert abs(pcl.calculate_c_to_on_ratio("C6H12O6") - 1.0) < 1e-9
	assert abs(pcl.calculate_c_to_on_ratio("C10H16N5O13P3") - (10.0 / 9.0)) < 1e-9
