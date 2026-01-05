#!/usr/bin/env python3

import bptools
from lib_test_utils import import_from_repo_path


def test_protein_ladder_lib_calculate_mw_gaps_smoke():
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/protein_ladder_lib.py")
	assert mod.calculate_mw_gaps([100, 50, 10], 100) == [30, 70]


def test_protein_ladder_lib_calculate_mw_gaps_requires_reverse_sorted():
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/protein_ladder_lib.py")
	try:
		mod.calculate_mw_gaps([10, 50, 100], 100)
		assert False, "expected ValueError for non-reverse-sorted MW list"
	except ValueError:
		pass


def test_protein_ladder_lib_get_kaleidoscope_markers_has_expected_entries():
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/protein_ladder_lib.py")
	markers = mod.get_kaleidoscope_markers()
	assert len(markers) == 10
	assert markers[0][0] == 250
	assert markers[-1][0] == 10
	assert mod.KALEIDOSCOPE_MW_COLOR_MAP[10] == "#ffee00"


def test_kaleidoscope_ladder_mapping_prelim_question_builds_expected_parts(monkeypatch):
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py")

	def fake_format(N, question_text, prompts_list, choices_list):
		return f"MAT\t{N}\t{question_text}\t{prompts_list}\t{choices_list}\n"

	monkeypatch.setattr(bptools, "formatBB_MAT_Question", fake_format)
	q = mod.write_prelim_mapping_question(1, table_height=200)
	assert q.startswith("MAT\t1\t")
	assert "#ffee00" in q
	assert "150 kDa" in q


def test_kaleidoscope_ladder_mapping_estimate_unknown_question_smoke(monkeypatch):
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py")

	def fake_num(N, question_text, answer_float, tolerance_float, tol_message=True):
		return f"NUM\t{N}\t{answer_float}\t{tolerance_float}\t{question_text}\n"

	monkeypatch.setattr(bptools, "formatBB_NUM_Question", fake_num)
	mod.random.seed(0)
	q = mod.write_prelim_estimate_unknown_question(1)
	assert q.startswith("NUM\t1\t")
	assert "<table" in q


def test_kaleidoscope_ladder_lane2_unknown_mw_question_smoke(monkeypatch):
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band_mw.py")

	def fake_num(N, question_text, answer_float, tolerance_float, tol_message=True):
		return f"NUM\t{N}\t{answer_float}\t{tolerance_float}\t{question_text}\n"

	monkeypatch.setattr(bptools, "formatBB_NUM_Question", fake_num)
	mod.random.seed(0)
	q = mod.write_lane2_unknown_band_mw_question(1, gel_height_px=280, run_scenario="too_long")
	assert q.startswith("NUM\t1\t")
	assert "Lane 1" in q
	assert "Lane 2" in q
	assert "too long" in q.lower()
	assert "display:flex" in q


def test_kaleidoscope_ladder_lane2_unknown_protein_mc_question_smoke(monkeypatch):
	mod = import_from_repo_path("problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band_protein_mc.py")

	def fake_mc(N, question_text, choices_list, answer_text):
		return f"MC\t{N}\t{answer_text}\t{len(choices_list)}\t{question_text}\n"

	monkeypatch.setattr(bptools, "formatBB_MC_Question", fake_mc)
	rng = mod.random.Random(0)
	q = mod.write_lane2_unknown_band_protein_mc_question(
		1,
		num_choices=5,
		gel_height_px=280,
		run_scenario="too_short",
		unknown_label="Protein X17",
		rng=rng,
	)
	assert q.startswith("MC\t1\t")
	assert "Protein X17" in q
	assert "Lane 1" in q
	assert "Lane 2" in q
	assert "kDa" in q
