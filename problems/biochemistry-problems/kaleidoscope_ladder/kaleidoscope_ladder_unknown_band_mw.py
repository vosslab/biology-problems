#!/usr/bin/env python3

import math
import random

import bptools
import protein_ladder_lib


def write_lane2_unknown_band_mw_question(
	N: int,
	gel_height_px: int=340,
	run_scenario: str="random",
) -> str:
	"""
	Lane 1: Kaleidoscope ladder bands (some may be off-gel if run too long).
	Lane 2: single unknown band.

	Asks for the molecular weight (kDa) of the unknown band.
	"""
	if run_scenario not in ("random", "normal", "too_short", "too_long"):
		raise ValueError(f"Unknown run_scenario: {run_scenario}")

	if run_scenario == "random":
		run_scenario = random.choice(["normal", "too_short", "too_long"])

	if run_scenario == "normal":
		run_factor = random.random() * 0.12 + 0.94
		scenario_text = "<p>The gel was run for a typical amount of time.</p>"
	elif run_scenario == "too_short":
		run_factor = random.random() * 0.15 + 0.70
		scenario_text = "<p>The gel was run for <b>too short</b> a time (bands are compressed near the top).</p>"
	elif run_scenario == "too_long":
		run_factor = random.random() * 0.45 + 1.15
		scenario_text = "<p>The gel was run for <b>too long</b> a time (some small bands may run off the bottom).</p>"
	else:
		raise AssertionError("unreachable")

	marker_positions = protein_ladder_lib.simulate_kaleidoscope_band_y_positions_px(
		gel_height_px=gel_height_px,
		run_factor=run_factor,
	)

	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()

	# Keep only visible marker bands to simulate run-off / out-of-frame bands.
	visible_markers: list[int] = []
	for mw in mw_values:
		y = marker_positions[mw]
		if protein_ladder_lib.band_is_visible(y, gel_height_px):
			visible_markers.append(mw)

	# Ensure we can still bracket an unknown band with at least two markers.
	if len(visible_markers) < 3:
		# If the run_factor pushes too many bands off-gel, fall back to normal.
		run_factor = 1.0
		marker_positions = protein_ladder_lib.simulate_kaleidoscope_band_y_positions_px(
			gel_height_px=gel_height_px,
			run_factor=run_factor,
		)
		visible_markers = [mw for mw in mw_values if protein_ladder_lib.band_is_visible(marker_positions[mw], gel_height_px)]

	# Choose a visible marker interval where the band spacing isn't too tiny.
	band_height_px = 8
	min_spacing_px = float(band_height_px + 4)

	intervals: list[tuple[int, int]] = []
	for hi, lo in zip(visible_markers[:-1], visible_markers[1:], strict=False):
		# hi has higher MW (smaller y), lo has lower MW (larger y)
		if (marker_positions[lo] - marker_positions[hi]) >= min_spacing_px:
			intervals.append((hi, lo))

	if not intervals:
		# As a last resort, pick the largest visible gap.
		best = None
		best_gap = -1.0
		for hi, lo in zip(visible_markers[:-1], visible_markers[1:], strict=False):
			gap = marker_positions[lo] - marker_positions[hi]
			if gap > best_gap:
				best_gap = gap
				best = (hi, lo)
		assert best is not None
		intervals = [best]

	mw_high, mw_low = random.choice(intervals)

	# Pick a band between the two markers (avoid being too close to a marker).
	frac = random.random() * 0.50 + 0.25
	unknown_mw = protein_ladder_lib.ln_fraction_to_mw_kda(float(mw_high), float(mw_low), frac)

	# Convert MW to y-position using the same mapping.
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
		band_height_px=band_height_px,
	)

	tolerance = float(unknown_mw) * 0.10
	question_text = (
		"<p>Below is a simulated SDS&ndash;PAGE gel.</p>"
		"<p>Lane 1 contains a Kaleidoscope-style pre-stained protein ladder. Lane 2 contains a single protein band.</p>"
		f"{scenario_text}"
		f"{gel_html}"
		"<p><b>What is the molecular weight (kDa) of the band in lane 2?</b></p>"
		"<p><i>Assume ln(MW) is approximately linear with migration distance.</i></p>"
	)
	return bptools.formatBB_NUM_Question(N, question_text, round(float(unknown_mw), 3), tolerance)


def write_question(N: int, args) -> str:
	return write_lane2_unknown_band_mw_question(
		N,
		gel_height_px=args.gel_height,
		run_scenario=args.run_scenario,
	)


def main():
	parser = bptools.make_arg_parser(description="Kaleidoscope ladder: determine MW of unknown band in lane 2.")
	parser.add_argument(
		"--run-scenario",
		choices=("random", "normal", "too_short", "too_long"),
		default="random",
		help="Choose how the gel was run.",
	)
	parser.add_argument("--gel-height", type=int, default=340, help="Gel height (px).")
	parser.add_argument("--seed", type=int, default=None, help="Random seed.")
	args = parser.parse_args()

	if args.seed is not None:
		random.seed(args.seed)

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
