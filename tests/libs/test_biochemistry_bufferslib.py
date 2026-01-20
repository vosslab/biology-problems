
from lib_test_utils import import_from_repo_path


def test_bufferslib_protonation_state_and_formatting():
	bufferslib = import_from_repo_path("problems/biochemistry-problems/buffers/bufferslib.py")

	assert "pK<sub>a</sub>" in bufferslib.pKa_list_to_words([4.76])
	assert "and" in bufferslib.pKa_list_to_words([3.0, 4.0])

	buffer_dict = bufferslib.monoprotic["acetate"]
	state_low, _ = bufferslib.get_protonation_state(buffer_dict, 3.0)
	state_high, _ = bufferslib.get_protonation_state(buffer_dict, 7.0)
	assert state_low == "CH3COOH"
	assert state_high == "CH3COO-1"

	formula = bufferslib.format_chemical_formula_html("CH3COO-1")
	assert "CH<sub>3</sub>" in formula
	assert "<sup>-</sup>" in formula
