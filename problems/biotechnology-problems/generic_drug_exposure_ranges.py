#!/usr/bin/env python3
"""Recognize similar drug levels in the Set #6 generic drug diagram."""

import random

import bptools


# LECT11C Set #6, topic 23. These are invented intervals for one measure of drug exposure.
# FDA's example acceptance limits are 80% and 125% for the full 90% confidence interval.
# https://www.fda.gov/media/163638/download
AXIS_MIN = 70
AXIS_MAX = 135
LIMITS = (80, 125)


def plot_position(value: int) -> float:
	return 110 + 238 * (value - AXIS_MIN) / (AXIS_MAX - AXIS_MIN)


def get_question_text(studies: list[tuple[str, int, int]]) -> str:
	"""Draw the ranges and the band on one scale for both browser and image export."""
	left, right = map(plot_position, LIMITS)
	description = []
	plot = (
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 164" '
		'role="img" aria-label="Drug levels compared with the brand-name drug" '
		'style="display:block;width:100%;height:auto;">'
		f'<rect x="{left:.2f}" y="24" width="{right - left:.2f}" height="136" fill="#e5edf5"/>'
		'<g stroke="#435e79" stroke-width="1" stroke-dasharray="4 3">'
		f'<path d="M {left:.2f} 24 V 160 M {right:.2f} 24 V 160"/></g>'
		'<g fill="#172a3a" font-family="sans-serif" font-size="16">'
		f'<text x="{left:.2f}" y="17" text-anchor="middle">80%</text>'
		f'<text x="{right:.2f}" y="17" text-anchor="middle">125%</text>'
	)
	for i, (label, low, high) in enumerate(studies):
		y = 42 + 32 * i
		start, end = map(plot_position, (low, high))
		start_description = 'left of the band' if low < LIMITS[0] else 'in the band'
		end_description = 'right of the band' if high > LIMITS[1] else 'in the band'
		description.append(f'{label} starts {start_description} and ends {end_description}.')
		plot += (
			f'<text x="5" y="{y + 5}">{label}</text>'
			f'<path d="M {start:.2f} {y} H {end:.2f} M {start:.2f} {y - 6} V {y + 6} '
			f'M {end:.2f} {y - 6} V {y + 6}" stroke="#233d56" stroke-width="2.5"/>'
		)
	plot += f'</g><desc>{" ".join(description)}</desc></svg>'
	return (
		'<table style="border-collapse:collapse;width:100%;max-width:400px;background-color:#fff;">'
		'<caption style="text-align:left;font-weight:bold;padding:0 0 6px;">'
		'Drug levels compared with the brand-name drug</caption>'
		f'<tr><td style="padding:0;">{plot}</td></tr></table>'
		'<p>Each line shows a 90% confidence interval. The whole line must fit inside '
		'the shaded band.</p>'
		'<p>Which generic meets this study rule?</p>'
	)


def write_question(N: int, args):
	inside_low = random.randint(83, 92)
	inside_high = random.randint(108, 122)
	outside_low = random.randint(72, 78)
	outside_high = random.randint(127, 133)
	answer_range = (inside_low, inside_high)
	ranges = [
		answer_range,
		(outside_low, random.randint(94, 110)),  # Checks only the upper end.
		(random.randint(100, 116), outside_high),  # Checks only the lower end.
		(outside_low, outside_high),  # Checks only whether the line crosses the band.
	]
	random.shuffle(ranges)
	choices = ['Generic A', 'Generic B', 'Generic C', 'Generic D']
	studies = [(label, low, high) for label, (low, high) in zip(choices, ranges)]
	answer = choices[ranges.index(answer_range)]
	return bptools.formatBB_MC_Question(N, get_question_text(studies), choices, answer)


def parse_arguments():
	return bptools.make_arg_parser(description=__doc__).parse_args()


def main():
	args = parse_arguments()
	bptools.collect_and_write_questions(write_question, args, bptools.make_outfile('MC'))


if __name__ == '__main__':
	main()
