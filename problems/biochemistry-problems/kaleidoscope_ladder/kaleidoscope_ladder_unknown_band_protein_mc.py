#!/usr/bin/env python3

import math
import os
import random
import sys

import bptools

_BIOCHEM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _BIOCHEM_DIR not in sys.path:
	sys.path.insert(0, _BIOCHEM_DIR)

import protein_ladder_lib
import proteinlib


def _choice_text(protein: dict) -> str:
	fullname = str(protein.get("fullname", "")).strip()
	mw = float(protein.get("MW", 0.0))
	return f"{fullname} ({mw:.1f} kDa)"


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
		# Randomize scan order but keep it deterministic via rng.
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

	if run_scenario not in ("random", "normal", "too_short", "too_long"):
		raise ValueError(f"Unknown run_scenario: {run_scenario}")

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
		raise AssertionError("unreachable")

	marker_positions = protein_ladder_lib.simulate_kaleidoscope_band_y_positions_px(
		gel_height_px=gel_height_px,
		run_factor=run_factor,
	)
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()

	visible_markers: list[int] = []
	for mw in mw_values:
		y = marker_positions[mw]
		if protein_ladder_lib.band_is_visible(y, gel_height_px):
			visible_markers.append(mw)

	if len(visible_markers) < 3:
		run_factor = 1.0
		marker_positions = protein_ladder_lib.simulate_kaleidoscope_band_y_positions_px(
			gel_height_px=gel_height_px,
			run_factor=run_factor,
		)
		visible_markers = [mw for mw in mw_values if protein_ladder_lib.band_is_visible(marker_positions[mw], gel_height_px)]

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

	# Convert MW to y-position using the same ln(MW) mapping.
	mw_top = float(mw_values[0])
	mw_bottom = float(mw_values[-1])
	ln_range = math.log(mw_top) - math.log(mw_bottom)
	usable = float(gel_height_px - 28 - 22)
	frac_from_top = (math.log(mw_top) - math.log(float(unknown_mw))) / ln_range
	unknown_y = 28.0 + float(run_factor) * frac_from_top * usable

	ladder_bands = []
	for mw in mw_values:
		y = marker_positions[mw]
		if not protein_ladder_lib.band_is_visible(y, gel_height_px):
			continue
		ladder_bands.append(
			{
				"y_px": y,
				"color": protein_ladder_lib.KALEIDOSCOPE_MW_COLOR_MAP[mw],
			}
		)

	unknown_bands = [
		{
			"y_px": unknown_y,
			"color": "#111111",
			"border": "1px solid #000",
		}
	]

	gel_html = protein_ladder_lib.gen_gel_lanes_html(
		lanes=[
			{"label": "Lane 1", "bands": ladder_bands},
			{"label": "Lane 2", "bands": unknown_bands},
		],
		gel_height_px=gel_height_px,
		band_height_px=8,
	)

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
		f"{gel_html}"
		f"<p><b>Which protein (name and molecular weight) best matches {unknown_label}?</b></p>"
		"<p><i>Use the ladder to estimate the band size. You do not need outside knowledge about the proteins.</i></p>"
	)
	return bptools.formatBB_MC_Question(N, question_text, choices, answer_text)


def write_question(N: int, args) -> str:
	rng = random.Random(args.seed) if args.seed is not None else random.Random()
	return write_lane2_unknown_band_protein_mc_question(
		N,
		num_choices=args.num_choices,
		gel_height_px=args.gel_height,
		run_scenario=args.run_scenario,
		unknown_label=args.unknown_label,
		rng=rng,
	)


def main():
	parser = bptools.make_arg_parser(description="Kaleidoscope ladder: identify anonymous protein from MW (MC).")
	parser = bptools.add_choice_args(parser, default=5)
	parser.add_argument(
		"--run-scenario",
		choices=("random", "normal", "too_short", "too_long"),
		default="random",
		help="Choose how the gel was run.",
	)
	parser.add_argument("--gel-height", type=int, default=340, help="Gel height (px).")
	parser.add_argument("--seed", type=int, default=None, help="Random seed.")
	parser.add_argument("--unknown-label", type=str, default="Protein X17", help="Label to show for lane 2.")
	args = parser.parse_args()

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()

