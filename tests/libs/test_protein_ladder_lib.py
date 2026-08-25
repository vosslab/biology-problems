
from lib_test_utils import import_from_repo_path


def test_protein_ladder_lib_calculates_mw_gaps():
	mod = import_from_repo_path("problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/protein_ladder_lib.py")
	assert mod.calculate_mw_gaps([100, 50, 10], 100) == [30, 70]


def test_protein_ladder_lib_calculate_mw_gaps_requires_reverse_sorted():
	mod = import_from_repo_path("problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/protein_ladder_lib.py")
	try:
		mod.calculate_mw_gaps([10, 50, 100], 100)
		assert False, "expected ValueError for non-reverse-sorted MW list"
	except ValueError:
		pass


def test_kaleidoscope_ladder_mapping_both_mode_can_retry_estimate(monkeypatch):
	mod = import_from_repo_path("problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py")
	args = type("Args", (), {"question_type": "both", "table_height": 200})()
	monkeypatch.setattr(mod.random, "choice", lambda choices: False)
	monkeypatch.setattr(mod, "write_prelim_estimate_unknown_question", lambda N: f"estimate {N}")
	assert mod.write_question(3, args) == "estimate 3"
