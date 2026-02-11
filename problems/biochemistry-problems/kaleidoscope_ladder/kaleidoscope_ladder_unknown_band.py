#!/usr/bin/env python3

import os
import sys
import random

import bptools

_BIOCHEM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _BIOCHEM_DIR not in sys.path:
	sys.path.insert(0, _BIOCHEM_DIR)

import protein_ladder_lib
import proteinlib


#====================================================================
def _choose_run_factor_and_text(
	run_scenario: str,
	rng: random.Random,
) -> tuple[float, str]:
	"""Pick a run_factor and descriptive HTML text for the chosen scenario."""
	if run_scenario == "random":
		run_scenario = rng.choice(["normal", "too_short", "too_long"])

	if run_scenario == "normal":
		run_factor = rng.random() * 0.12 + 0.94
		scenario_text = "<p>The gel was run for a typical amount of time.</p>"
	elif run_scenario == "too_short":
		run_factor = rng.random() * 0.15 + 0.70
		scenario_text = "<p>The gel was run for <b>too short</b> a time (bands are compressed near the top).</p>"
	elif run_scenario == "too_long":
		run_factor = rng.random() * 0.45 + 1.15
		scenario_text = "<p>The gel was run for <b>too long</b> a time (some small bands may run off the bottom).</p>"
	else:
		raise ValueError(f"Unknown run_scenario: {run_scenario}")
	return run_factor, scenario_text


#====================================================================
def _simulate_gel_setup(
	gel_height_px: int,
	run_scenario: str,
	rng: random.Random,
) -> tuple[float, str, dict, list[int]]:
	"""
	Shared gel-simulation setup for both question formats.

	Returns:
		run_factor, scenario_text, marker_positions, visible_markers
	"""
	if run_scenario not in ("random", "normal", "too_short", "too_long"):
		raise ValueError(f"Unknown run_scenario: {run_scenario}")

	run_factor, scenario_text = _choose_run_factor_and_text(run_scenario, rng)

	marker_positions = protein_ladder_lib.simulate_kaleidoscope_band_y_positions_px(
		gel_height_px=gel_height_px,
		run_factor=run_factor,
	)
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()

	# Keep only visible marker bands to simulate run-off / out-of-frame bands.
	visible_markers: list[int] = [
		mw for mw in mw_values
		if protein_ladder_lib.band_is_visible(marker_positions[mw], gel_height_px)
	]

	# Ensure we can still bracket an unknown band with at least two markers.
	if len(visible_markers) < 3:
		run_factor = 1.0
		marker_positions = protein_ladder_lib.simulate_kaleidoscope_band_y_positions_px(
			gel_height_px=gel_height_px,
			run_factor=run_factor,
		)
		visible_markers = [
			mw for mw in mw_values
			if protein_ladder_lib.band_is_visible(marker_positions[mw], gel_height_px)
		]

	return run_factor, scenario_text, marker_positions, visible_markers


#====================================================================
def _build_reference_table_html(gel_height_px: int) -> str:
	"""Generate the standard Kaleidoscope ladder reference card with MW labels."""
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()
	return protein_ladder_lib.gen_kaleidoscope_table(
		mw_values,
		protein_ladder_lib.KALEIDOSCOPE_MW_COLOR_MAP,
		gel_height_px,
		show_labels=True,
		label_prefix="",
	)


#====================================================================
def _build_gel_html(
	mw_values: list[int],
	marker_positions: dict,
	unknown_y: float,
	gel_height_px: int,
	band_height_px: int=8,
) -> str:
	"""Build the two-lane gel HTML (lane 1 = ladder, lane 2 = unknown band)."""
	ladder_bands = []
	for mw in mw_values:
		y = marker_positions[mw]
		if not protein_ladder_lib.band_is_visible(y, gel_height_px):
			continue
		ladder_bands.append({
			"y_px": y,
			"color": protein_ladder_lib.KALEIDOSCOPE_MW_COLOR_MAP[mw],
		})

	unknown_bands = [{
		"y_px": unknown_y,
		"color": "#111111",
		"border": "1px solid #000",
	}]

	return protein_ladder_lib.gen_gel_lanes_html(
		lanes=[
			{"label": "Lane 1", "bands": ladder_bands},
			{"label": "Lane 2", "bands": unknown_bands},
		],
		gel_height_px=gel_height_px,
		band_height_px=band_height_px,
	)


#====================================================================
def _pick_interval(
	visible_markers: list[int],
	marker_positions: dict,
	rng: random.Random,
	band_height_px: int=8,
) -> tuple[int, int]:
	"""Choose a visible marker interval where the band spacing isn't too tiny."""
	min_spacing_px = float(band_height_px + 4)

	intervals: list[tuple[int, int]] = []
	for hi, lo in zip(visible_markers[:-1], visible_markers[1:]):
		if (marker_positions[lo] - marker_positions[hi]) >= min_spacing_px:
			intervals.append((hi, lo))

	if not intervals:
		best = None
		best_gap = -1.0
		for hi, lo in zip(visible_markers[:-1], visible_markers[1:]):
			gap = marker_positions[lo] - marker_positions[hi]
			if gap > best_gap:
				best_gap = gap
				best = (hi, lo)
		assert best is not None
		intervals = [best]

	return rng.choice(intervals)


#====================================================================
def write_lane2_unknown_band_mw_question(
	N: int,
	gel_height_px: int=340,
	run_scenario: str="random",
	rng: random.Random | None=None,
) -> str:
	"""
	Lane 1: Kaleidoscope ladder bands (some may be off-gel if run too long).
	Lane 2: single unknown band.

	Asks for the molecular weight (kDa) of the unknown band (numeric).
	"""
	if rng is None:
		rng = random.Random()

	run_factor, scenario_text, marker_positions, visible_markers = _simulate_gel_setup(
		gel_height_px, run_scenario, rng,
	)
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()
	band_height_px = 8

	mw_high, mw_low = _pick_interval(visible_markers, marker_positions, rng, band_height_px)

	# Pick a band between the two markers (avoid being too close to a marker).
	frac = rng.random() * 0.50 + 0.25
	unknown_mw = protein_ladder_lib.ln_fraction_to_mw_kda(float(mw_high), float(mw_low), frac)

	unknown_y = protein_ladder_lib.mw_to_y_px(unknown_mw, gel_height_px, run_factor)

	gel_html = _build_gel_html(mw_values, marker_positions, unknown_y, gel_height_px, band_height_px)
	ref_html = _build_reference_table_html(gel_height_px)

	tolerance = float(unknown_mw) * 0.10
	question_text = (
		"<p>Below is a simulated SDS&ndash;PAGE gel.</p>"
		"<p>Lane 1 contains a Kaleidoscope-style pre-stained protein ladder. Lane 2 contains a single protein band.</p>"
		f"{scenario_text}"
		'<p><b>Standard ladder reference (kDa):</b></p>'
		f"{ref_html}"
		'<p><b>Gel results:</b></p>'
		f"{gel_html}"
		"<p><b>What is the molecular weight (kDa) of the band in lane 2?</b></p>"
		"<p><i>Assume ln(MW) is approximately linear with migration distance.</i></p>"
	)
	return bptools.formatBB_NUM_Question(N, question_text, round(float(unknown_mw), 3), tolerance)


#====================================================================
def _choice_text(protein: dict) -> str:
	fullname = str(protein.get("fullname", "")).strip()
	mw = float(protein.get("MW", 0.0))
	return f"{fullname} ({mw:.1f} kDa)"


#====================================================================
def _pick_distractors(
	proteins_sorted: list[dict],
	correct_index: int,
	num_choices: int,
	rng: random.Random,
) -> list[dict]:
	target_count = max(0, int(num_choices) - 1)
	if target_count == 0:
		return []

	near = proteins_sorted[max(0, correct_index - 18):correct_index] + proteins_sorted[correct_index + 1:correct_index + 19]
	rest = proteins_sorted[:correct_index] + proteins_sorted[correct_index + 1:]

	picked: list[dict] = []
	seen_names: set[str] = set()

	def _try_add(pool: list[dict]):
		for cand in rng.sample(pool, k=min(len(pool), max(1, target_count * 4))):
			if len(picked) >= target_count:
				return
			name = str(cand.get("fullname", "")).strip()
			if len(name) == 0 or name in seen_names:
				continue
			seen_names.add(name)
			picked.append(cand)

	_try_add(near)
	if len(picked) < target_count:
		_try_add(rest)
	return picked[:target_count]


#====================================================================
def write_lane2_unknown_band_protein_mc_question(
	N: int,
	num_choices: int=5,
	gel_height_px: int=340,
	run_scenario: str="random",
	unknown_label: str="Protein X17",
	rng: random.Random | None=None,
) -> str:
	"""
	Lane 1: Kaleidoscope ladder bands.
	Lane 2: single band labeled with an anonymous protein ID.

	Question is MC-only. Choices are real protein names plus their MW from `proteinlib.py`.
	"""
	if rng is None:
		rng = random.Random()

	run_factor, scenario_text, marker_positions, visible_markers = _simulate_gel_setup(
		gel_height_px, run_scenario, rng,
	)
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()

	mw_high_visible = float(visible_markers[0])
	mw_low_visible = float(visible_markers[-1])

	# Pick a real protein whose MW would place it within the visible marker range.
	all_proteins = proteinlib.parse_protein_file()
	candidates = []
	for p in all_proteins:
		try:
			mw = float(p.get("MW", 0.0))
		except (TypeError, ValueError):
			continue
		if mw <= 0:
			continue
		if mw < mw_low_visible or mw > mw_high_visible:
			continue
		name = str(p.get("fullname", "")).strip()
		if len(name) == 0:
			continue
		candidates.append(p)

	if len(candidates) == 0:
		raise ValueError("No proteins found in MW range for this run scenario")

	# Avoid landing essentially on a marker band: keep at least ~2 kDa away.
	marker_mw_set = set(mw_values)
	filtered = []
	for p in candidates:
		mw = float(p["MW"])
		if any(abs(mw - float(m)) < 2.0 for m in marker_mw_set):
			continue
		filtered.append(p)
	if filtered:
		candidates = filtered

	correct_protein = rng.choice(candidates)
	unknown_mw = float(correct_protein["MW"])

	unknown_y = protein_ladder_lib.mw_to_y_px(unknown_mw, gel_height_px, run_factor)

	gel_html = _build_gel_html(mw_values, marker_positions, unknown_y, gel_height_px)
	ref_html = _build_reference_table_html(gel_height_px)

	proteins_sorted = sorted(candidates, key=lambda p: float(p["MW"]))
	correct_index = proteins_sorted.index(correct_protein)
	distractors = _pick_distractors(proteins_sorted, correct_index, num_choices, rng)

	choices = [_choice_text(correct_protein)] + [_choice_text(p) for p in distractors]
	# Ensure uniqueness; top off from remaining if collisions occur.
	unique = []
	seen = set()
	for c in choices:
		if c in seen:
			continue
		seen.add(c)
		unique.append(c)
	choices = unique

	if len(choices) < num_choices:
		remaining = [p for p in proteins_sorted if _choice_text(p) not in seen]
		for p in rng.sample(remaining, k=min(len(remaining), num_choices - len(choices))):
			choices.append(_choice_text(p))
			seen.add(choices[-1])

	choices = choices[:max(2, int(num_choices))]
	rng.shuffle(choices)
	answer_text = _choice_text(correct_protein)

	question_text = (
		"<p>Below is a simulated SDS&ndash;PAGE gel.</p>"
		"<p>Lane 1 contains a Kaleidoscope-style pre-stained protein ladder.</p>"
		f"<p>Lane 2 contains a single band labeled <b>{unknown_label}</b>.</p>"
		f"{scenario_text}"
		'<p><b>Standard ladder reference (kDa):</b></p>'
		f"{ref_html}"
		'<p><b>Gel results:</b></p>'
		f"{gel_html}"
		f"<p><b>Which protein (name and molecular weight) best matches {unknown_label}?</b></p>"
		"<p><i>Use the ladder to estimate the band size. You do not need outside knowledge about the proteins.</i></p>"
	)
	return bptools.formatBB_MC_Question(N, question_text, choices, answer_text)


#====================================================================
def write_question(N: int, args) -> str:
	rng = random.Random(args.seed) if args.seed is not None else random.Random()
	if args.question_type == 'num':
		return write_lane2_unknown_band_mw_question(
			N,
			gel_height_px=args.gel_height,
			run_scenario=args.run_scenario,
			rng=rng,
		)
	if args.question_type == 'mc':
		return write_lane2_unknown_band_protein_mc_question(
			N,
			num_choices=args.num_choices,
			gel_height_px=args.gel_height,
			run_scenario=args.run_scenario,
			unknown_label=args.unknown_label,
			rng=rng,
		)
	raise ValueError(f"Unknown question_type: {args.question_type}")


#====================================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Kaleidoscope ladder: determine MW or identify protein from unknown band in lane 2."
	)
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc', 'num'],
		required=False,
		default='num',
	)
	parser.add_argument(
		"--run-scenario", dest="run_scenario",
		choices=("random", "normal", "too_short", "too_long"),
		default="random",
		help="Choose how the gel was run.",
	)
	parser.add_argument("--gel-height", dest="gel_height", type=int, default=340, help="Gel height (px).")
	parser.add_argument("--seed", dest="seed", type=int, default=None, help="Random seed.")
	parser.add_argument("--unknown-label", dest="unknown_label", type=str, default="Protein X17", help="Label to show for lane 2 (MC only).")
	return parser.parse_args()


#====================================================================
#====================================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#====================================================================
#====================================================================
if __name__ == "__main__":
	main()
