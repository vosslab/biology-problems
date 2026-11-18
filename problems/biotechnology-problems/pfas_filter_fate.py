#!/usr/bin/env python3
"""Follow PFAS through a water filter in a Set #6 diagram."""

import random

import bptools


# LECT11C Set #6 topic 25, the annual TP membrane figure, and the PFAS fate drawing.
# The levels are invented. They describe one PFAS and give no drinking-water safety limit.
FILTERS = (
	('Carbon filter', 'Used carbon', 'Some PFAS stayed on the carbon.'),
	('Membrane filter', 'Water left behind', 'Some PFAS stayed in the water held back by the membrane.'),
)


def get_question_text(filter_name: str, retained_label: str, before: int, after: int) -> str:
	cell = 'border:1px solid #8399aa;padding:7px 14px;background-color:#e8f1f7;'
	arrow = '<tr><td colspan="2" style="padding:1px;">&#8595;</td></tr>'
	return (
		'<table style="border-collapse:collapse;width:100%;max-width:450px;text-align:center;'
		'background-color:#fff;color:#172a3a;">'
		'<caption style="text-align:left;font-weight:bold;padding:0 0 6px;">'
		'PFAS in a water filter test</caption>'
		f'<tr><td colspan="2" style="{cell}"><strong>Water in</strong><br/>{before} ng/L PFAS</td></tr>'
		f'{arrow}<tr><td colspan="2" style="{cell}"><strong>{filter_name}</strong></td></tr>'
		'<tr><td>&#8595;</td><td>&#8595;</td></tr>'
		f'<tr><td style="{cell}"><strong>Treated water</strong><br/>{after} ng/L PFAS</td>'
		f'<td style="{cell}"><strong>{retained_label}</strong><br/>PFAS found here</td></tr></table>'
		'<p>The filter had no PFAS when the test began.</p>'
		'<p>Which statement fits the results?</p>'
	)


def write_question(N: int, args):
	filter_name, retained_label, retained_result = random.choice(FILTERS)
	before = random.randint(20, 80)
	after = random.randint(1, 9)
	destroyed = 'The filter destroyed all the PFAS it removed.'
	answer = f'The treated water had {after} ng/L. {retained_result}'
	choices = [
		answer,
		# Confuses removal with destruction.
		f'The treated water had {after} ng/L. {destroyed}',
		# Reverses the inlet and outlet readings.
		f'The treated water had {before} ng/L. {retained_result}',
		# Reverses the readings and mistakes removal for destruction.
		f'The treated water had {before} ng/L. {destroyed}',
	]
	random.shuffle(choices)
	return bptools.formatBB_MC_Question(
		N, get_question_text(filter_name, retained_label, before, after), choices, answer)


def parse_arguments():
	return bptools.make_arg_parser(description=__doc__).parse_args()


def main():
	args = parse_arguments()
	bptools.collect_and_write_questions(write_question, args, bptools.make_outfile('MC'))


if __name__ == '__main__':
	main()
