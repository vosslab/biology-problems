#!/usr/bin/env python3

import math
import copy
import random

import bptools

#=============================
SCENARIOS = None

def makeXvals(mode=1):
	if mode == 1:
		generators = [0.0001, 0.001, 0.01]
		xvals = [0.1, 1, 10]
	else:
		generators = [0.001, 0.01, 0.1]
		xvals = [1, 10, 100]
	for g in generators:
		xvals.append(g)
		xvals.append(g*2)
		xvals.append(g*5)
	xvals.sort()
	return xvals

def makeTable2(xvals, yvals, Vmax):
	table = ''
	table += '<table cellpadding="2" cellspacing="2" '
	table += ' style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;">'
	w = 120
	table += '<colgroup width="{0}"></colgroup> '.format(w)
	table += '<colgroup width="{0}"></colgroup> '.format(w)
	table += '<tr>'
	table += ' <th align="center">substrate<br/>concentration<br/>[S]</th>'
	table += ' <th align="center">initial<br/>reaction<br/>velocity<br/>V<sub>0</sub></th>'
	table += '</tr>'
	mono_span = '<span style="font-family: courier, monospace;">'
	numrows = min(len(xvals), len(yvals))
	for i in range(numrows):
		x = xvals[i]
		y = yvals[i]
		table += '<tr>'
		if xvals[0] < 0.0002:
			table += ' <td align="right">{1}{0:.4f}&nbsp;</span></td>'.format(x, mono_span)
		else:
			table += ' <td align="right">{1}{0:.3f}&nbsp;</span></td>'.format(x, mono_span)
		table += ' <td align="right">{1}{0:.1f}&nbsp;</span></td>'.format(y, mono_span)
		table += '</tr>'
		if (Vmax - y) < 0.099:
			print(y)
			print(Vmax - y)
			break
	table += '</table>'
	return table

#=============================
# Function to create an HTML table with specified data and styling improvements
def makeTable(xvals, yvals, Vmax):
	# Initialize the table with basic properties and custom styling
	table = '<table cellpadding="2" cellspacing="2" '
	table += 'style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;">'

	# Define the width for each column
	col_width = 160
	for _ in range(2):  # Assuming three columns for simplicity
		table += f'<colgroup width="{col_width}"></colgroup> '

	# Header row with custom styling for smaller text and same size variable names
	table += '<tr style="background-color: lightgray; border-bottom: 2px solid black;">'
	table += ('<th align="center" style="padding: 5px; font-size: 10px;">'
		+'substrate<br/>concentration, '
		+'<span style="font-size: 14px;">[S]</span></th>')
	table += ('<th align="center" style="padding: 5px; font-size: 10px;">'
		+'initial reaction<br/>velocity<br/>'
		+'<span style="font-size: 14px;">V<sub>0</sub></span></th>')
	table += '</tr>'

	# Styling for monospace font span
	mono_span = '<span style="font-family: courier, monospace;">'

	# Determine the number of rows
	numrows = min(len(xvals), len(yvals))

	# Loop to create each row of the table
	for i in range(numrows):
		bgcolor = "#FFFFDD" if i % 2 == 0 else "#FFFFFF"  # Subtle yellow for even rows, white for odd
		x = xvals[i]
		y = yvals[i]
		table += f'<tr style="background-color: {bgcolor};">'
		if xvals[0] < 0.0002:
			table += f' <td style="border: 1px solid black;" align="right">{mono_span}{x:.4f}&nbsp;</span></td>'
		else:
			table += f' <td style="border: 1px solid black;" align="right">{mono_span}{x:.3f}&nbsp;</span></td>'
		table += f' <td style="border: 1px solid black;" align="right">{mono_span}{y:.1f}&nbsp;</span></td>'
		table += '</tr>'

		# Break out of the loop if the difference between Vmax and y is less than 0.099
		if (Vmax - y) < 0.099:
			break
	table += '</table>'
	return table


def michaelis_menten(substrate_conc, Km, Vmax):
	V0 = Vmax * substrate_conc / float(substrate_conc + Km)
	V0 = math.ceil(V0*10.)/10.
	return V0


def makeCompleteProblem(N, xvals, Km, Vmax):
	header = ""
	header += "<p><u>Michaelis-Menten question.</u>"
	header += " The following question refers to the table (<i>below</i>) of enzyme activity.</p> "
	question = "<p>Using the table (<i>above</i>), calculate the value for the Michaelis-Menten constant, K<sub>M</sub>.</p>"


	yvals = []
	for x in xvals:
		y = michaelis_menten(x, Km, Vmax)
		yvals.append(y)
	table = makeTable(xvals, yvals, Vmax)

	choices = copy.copy(xvals[:7])
	choices.remove(Km)
	random.shuffle(choices)
	while len(choices) > 4:
		choices.pop()
	choices.append(Km)
	choices.sort()

	mono_span = '<span style="font-family: courier, monospace;">'
	choices_list = []
	for choice in choices:
		if xvals[0] < 0.0002:
			choice_text = f"K<sub>M</sub> = {mono_span}{choice:.4f}</span>"
		else:
			choice_text = f"K<sub>M</sub> = {mono_span}{choice:.3f}</span>"
		choices_list.append(choice_text)
		if abs(choice - Km) < 1e-6:
			answer_text = choice_text

	question_text = header + table + '<br/>' + question
	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	return bb_question

#=============================
def _get_scenarios() -> list[tuple[int, int, float]]:
	# acceptable range: >40, <200, multiple of 20
	Vmax_choices = [40, 60, 80, 100, 120, 140, 160, 180, 200]
	scenarios: list[tuple[int, int, float]] = []
	for mode in (1, 2):
		xvals = makeXvals(mode)
		Km_choices = xvals[:6]
		for Vmax in Vmax_choices:
			for Km in Km_choices:
				scenarios.append((mode, Vmax, Km))
	return scenarios


#=============================
def write_question(N: int, args) -> str:
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	mode, Vmax, Km = SCENARIOS[idx]
	xvals = makeXvals(mode)
	return makeCompleteProblem(N, xvals, Km, Vmax)

#=============================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate Michaelis-Menten Km table questions.",
	)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#=============================
def main():
	args = parse_arguments()
	global SCENARIOS
	SCENARIOS = _get_scenarios()
	if len(SCENARIOS) == 0:
		raise ValueError("No scenarios were generated.")
	if args.scenario_order == 'random':
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
