#!/usr/bin/env python3

import math
import random
import os
import sys

import bptools

_BIOCHEM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _BIOCHEM_DIR not in sys.path:
	sys.path.insert(0, _BIOCHEM_DIR)

import protein_ladder_lib


def _color_swatch(hex_color: str, width_px: int=26, height_px: int=12) -> str:
	return (
		'<span style="'
		f'display:inline-block; width:{width_px}px; height:{height_px}px; '
		f'background-color:{hex_color}; border:1px solid #000; '
		'vertical-align:middle;"></span>'
	)


def write_prelim_mapping_question(N: int, table_height: int=450) -> str:
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()
	ladder_html = protein_ladder_lib.gen_kaleidoscope_table(
		mw_values,
		protein_ladder_lib.KALEIDOSCOPE_MW_COLOR_MAP,
		table_height,
		show_labels=False,
	)

	# Pick bands with visually distinct colors (avoid the multiple blues).
	target_mw_values = [150, 75, 37, 25, 10]
	prompts_list = []
	choices_list = []
	for mw_kda in target_mw_values:
		color_hex = protein_ladder_lib.KALEIDOSCOPE_MW_COLOR_MAP[mw_kda]
		prompts_list.append(f'{_color_swatch(color_hex)}&nbsp;colored band')
		choices_list.append(f"{mw_kda} kDa")

	question_text = (
		'<p>Lane 1 shows a simulated Kaleidoscope-style pre-stained protein ladder.</p>'
		f'{ladder_html}'
		'<p><b>Match each colored band to its molecular weight.</b></p>'
	)
	return bptools.formatBB_MAT_Question(N, question_text, prompts_list, choices_list)


def _mw_to_distance_mm(mw_kda: float, intercept_mm: float=120.0, slope_mm: float=18.0) -> float:
	return intercept_mm - slope_mm * math.log(mw_kda)


def _interp_mw_from_two_markers(mw_high: float, dist_high: float, mw_low: float, dist_low: float, dist_unknown: float) -> float:
	"""
	Estimate MW assuming ln(MW) is linear with migration distance.

	`mw_high` should be the higher molecular weight marker (travels less; smaller distance).
	`mw_low` should be the lower molecular weight marker (travels more; larger distance).
	"""
	ln_high = math.log(mw_high)
	ln_low = math.log(mw_low)
	fraction = (dist_unknown - dist_high) / (dist_low - dist_high)
	ln_unknown = ln_high + fraction * (ln_low - ln_high)
	return math.exp(ln_unknown)


def write_prelim_estimate_unknown_question(N: int) -> str:
	mw_values = protein_ladder_lib.get_kaleidoscope_mw_values()
	gap_index = random.randint(0, len(mw_values) - 2)

	mw_high = float(mw_values[gap_index])
	mw_low = float(mw_values[gap_index + 1])
	dist_high = _mw_to_distance_mm(mw_high)
	dist_low = _mw_to_distance_mm(mw_low)

	# Place unknown between the two marker distances.
	frac = random.random() * 0.6 + 0.2
	dist_unknown = dist_high + frac * (dist_low - dist_high)
	unknown_mw = _interp_mw_from_two_markers(mw_high, dist_high, mw_low, dist_low, dist_unknown)
	tolerance = unknown_mw * 0.06

	table_html = (
		'<table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse;">'
		'<tr><th>Band</th><th>Molecular weight (kDa)</th><th>Distance migrated (mm)</th></tr>'
		f'<tr><td>Marker (upper)</td><td>{mw_high:.0f}</td><td>{dist_high:.1f}</td></tr>'
		f'<tr><td>Marker (lower)</td><td>{mw_low:.0f}</td><td>{dist_low:.1f}</td></tr>'
		f'<tr><td><b>Unknown</b></td><td>?</td><td><b>{dist_unknown:.1f}</b></td></tr>'
		'</table>'
	)

	question_text = (
		'<p>The standard protein ladder bands below were run on an SDS&ndash;PAGE gel.</p>'
		f'{table_html}'
		'<p><b>Estimate the molecular weight (kDa) of the unknown band.</b></p>'
	)
	return bptools.formatBB_NUM_Question(N, question_text, round(unknown_mw, 3), tolerance)


def main():
	parser = bptools.make_arg_parser(description="Kaleidoscope-style protein ladder mapping questions.")
	parser.add_argument("--table-height", type=int, default=450, help="Ladder table height (px)")
	parser.add_argument(
		"--question-type",
		choices=("mapping", "estimate", "both"),
		default="mapping",
		help="Question type to generate",
	)
	parser.add_argument("--seed", type=int, default=None, help="Random seed (for estimate/both)")
	args = parser.parse_args()

	if args.seed is not None:
		random.seed(args.seed)

	def write_question(N: int, args):
		if args.question_type == "mapping":
			return write_prelim_mapping_question(N, table_height=args.table_height)
		if args.question_type == "estimate":
			return write_prelim_estimate_unknown_question(N)
		if args.question_type == "both":
			if N % 2 == 1:
				return write_prelim_mapping_question(N, table_height=args.table_height)
			return write_prelim_estimate_unknown_question(N)
		raise ValueError(f"Unknown question type: {args.question_type}")

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
