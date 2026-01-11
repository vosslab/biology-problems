#!/usr/bin/env python3

import sys
import math
import copy
import random

import bptools

#=============================
#=============================
SCENARIOS = None

#=============================
#=============================
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

#=============================
#=============================
def makeTable2(xvals, yvals, inhibvals, Vmax, inhib_Vmax):
	table = ''
	table += '<table cellpadding="2" cellspacing="2" '
	table += ' style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;">'
	w = 160
	table += '<colgroup width="{0}"></colgroup> '.format(w)
	table += '<colgroup width="{0}"></colgroup> '.format(w)
	table += '<colgroup width="{0}"></colgroup> '.format(w)
	table += '<tr>'
	table += ' <th align="center">substrate<br/>concentration, [S]</th>'
	table += ' <th align="center">initial reaction<br/>velocity no inhibitor<br/>V<sub>0</sub> (&ndash;inh)</th>'
	table += ' <th align="center">initial reaction<br/>velocity with inhibitor<br/>V<sub>0</sub> (+inh)</th>'
	table += '</tr>'
	mono_span = '<span style="font-family: courier, monospace;">'
	numrows = min(len(xvals), len(yvals))
	for i in range(numrows):
		x = xvals[i]
		y = yvals[i]
		z = inhibvals[i]
		table += '<tr>'
		if xvals[0] < 0.0002:
			table += ' <td align="right">{1}{0:.4f}&nbsp;</span></td>'.format(x, mono_span)
		else:
			table += ' <td align="right">{1}{0:.3f}&nbsp;</span></td>'.format(x, mono_span)
		table += ' <td align="right">{1}{0:.1f}&nbsp;</span></td>'.format(y, mono_span)
		table += ' <td align="right">{1}{0:.1f}&nbsp;</span></td>'.format(z, mono_span)
		table += '</tr>'
		if (Vmax - y) < 0.099:
			#print(y)
			#print(Vmax - y)
			break
	table += '</table>'
	return table

#=============================
# Function to create an HTML table with specified data and styling improvements
def makeTable(xvals, yvals, inhibvals, Vmax, inhib_Vmax):
	# Initialize the table with basic properties and custom styling
	table = '<table cellpadding="2" cellspacing="2" '
	table += 'style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;">'

	# Define the width for each column
	col_width = 160
	for _ in range(3):  # Assuming three columns for simplicity
		table += f'<colgroup width="{col_width}"></colgroup> '

	# Header row with custom styling for smaller text and same size variable names
	table += '<tr style="background-color: lightgray; border-bottom: 2px solid black;">'
	table += '<th align="center" style="padding: 5px; font-size: 10px;">substrate<br/>concentration, <span style="font-size: 14px;">[S]</span></th>'
	table += '<th align="center" style="padding: 5px; font-size: 10px;">initial reaction<br/>velocity no inhibitor<br/><span style="font-size: 14px;">V<sub>0</sub> (&ndash;inh)</span></th>'
	table += '<th align="center" style="padding: 5px; font-size: 10px;">initial reaction<br/>velocity with inhibitor<br/><span style="font-size: 14px;">V<sub>0</sub> (+inh)</span></th>'
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
		z = inhibvals[i]
		table += f'<tr style="background-color: {bgcolor};">'
		if xvals[0] < 0.0002:
			table += f' <td style="border: 1px solid black;" align="right">{mono_span}{x:.4f}&nbsp;</span></td>'
		else:
			table += f' <td style="border: 1px solid black;" align="right">{mono_span}{x:.3f}&nbsp;</span></td>'
		table += f' <td style="border: 1px solid black;" align="right">{mono_span}{y:.1f}&nbsp;</span></td>'
		table += f' <td style="border: 1px solid black;" align="right">{mono_span}{z:.1f}&nbsp;</span></td>'
		table += '</tr>'

		# Break out of the loop if the difference between Vmax and y is less than 0.099
		if (Vmax - y) < 0.099:
			break
	table += '</table>'
	return table


#=============================
#=============================
def michaelis_menten(substrate_conc, Km, Vmax):
	V0 = Vmax * substrate_conc / float(substrate_conc + Km)
	V0 = math.ceil(V0*10.)/10.
	return V0

#=============================
#=============================
def adjust_MM_values(Km, Vmax, inhibition, xvals):
	Km_choices = copy.copy(xvals)
	Km_choices.pop(-1)
	Km_choices.pop(-1)
	random.shuffle(Km_choices)
	if inhibition == "competitive":
		#Vmax unchanged
		inhib_Vmax = Vmax
		x = 0
		while x <= Km:
			x = Km_choices.pop()
		inhib_Km = x
	elif inhibition == "un-competitive":
		# KM/Vmax unchanged
		if round(math.log10(Km / 5.) % 1, 3) < 0.001:
			## ends with a 5
			inhib_Km = round(Km / 2.5, 5)
		else:
			## ends with 1 or 2
			inhib_Km = round(Km / 2, 5)
		# slope KM/Vmax unchanged
		raw_Vmax = Vmax * inhib_Km / Km
		inhib_Vmax = round(raw_Vmax/20.)*20
	elif inhibition == "non-competitive":
		#Km unchanged
		inhib_Km = Km
		Vmax_choices = [20, 40, 60, 80, 100, 120, 140, 160, 180]
		random.shuffle(Vmax_choices)
		inhib_Vmax = 300
		while inhib_Vmax >= Vmax:
			inhib_Vmax = Vmax_choices.pop(0)

	#double-check everything
	print("{0}: Vmax={1}, Km={2} and Vmax={3}, Km={4}".format(inhibition, Vmax, Km, inhib_Vmax, inhib_Km))
	while abs(Km - inhib_Km) < 0.00001 and abs(Vmax - inhib_Vmax) < 0.01:
		print("{0}: Vmax={1}, Km={2} and Vmax={3}, Km={4}".format(inhibition, Vmax, Km, inhib_Vmax, inhib_Km))
		#inhib_Km, inhib_Vmax = adjust_MM_values(Km, Vmax, inhibition, xvals)
		sys.exit(1)
	while inhibition == "competitive" and (inhib_Km - Km <= 1e-5 or abs(Vmax - inhib_Vmax) > 0.01):
		#Vmax unchanged, Km goes up
		print("{0}: Vmax={1}, Km={2} and Vmax={3}, Km={4}".format(inhibition, Vmax, Km, inhib_Vmax, inhib_Km))
		#inhib_Km, inhib_Vmax = adjust_MM_values(Km, Vmax, inhibition, xvals)
		sys.exit(1)
	while inhibition == "un-competitive" and (Km - inhib_Km <= 1e-5 or Vmax - inhib_Vmax <= 0):
		# slope KM/Vmax mostly unchanged - not perfect
		# Vmax goes down, Km goes down
		print("{0}: Vmax={1}, Km={2} and Vmax={3}, Km={4}".format(inhibition, Vmax, Km, inhib_Vmax, inhib_Km))
		#inhib_Km, inhib_Vmax = adjust_MM_values(Km, Vmax, inhibition, xvals)
		sys.exit(1)
	while inhibition == "non-competitive" and ( abs(Km - inhib_Km) > 1e-6 or Vmax - inhib_Vmax <= 0.01):
		#Km unchanged, Vmax goes down
		print("{0}: Vmax={1}, Km={2} and Vmax={3}, Km={4}".format(inhibition, Vmax, Km, inhib_Vmax, inhib_Km))
		#inhib_Km, inhib_Vmax = adjust_MM_values(Km, Vmax, inhibition, xvals)
		sys.exit(1)
	return inhib_Km, inhib_Vmax

#=============================
#=============================
def makeCompleteProblem(N, xvals, Km, Vmax, inhibition):
	header = "<p><u>Michaelis-Menten Kinetics and Inhibition Type Determination</u></p>"
	header += "<p>The table below presents data on enzyme activity measured as initial reaction"
	header += " velocities (V<sub>0</sub>) with and without the presence of an inhibitor at various substrate"
	header += " concentrations ([S]).</p>"

	question = "<p>Based on the data provided, determine the type of inhibition show by"
	question += " the inhibitor. Consider how the addition of the inhibitor affects the initial"
	question += " reaction velocities (V<sub>0</sub>) at various substrate concentrations ([S]).</p>"


	yvals = []
	for x in xvals:
		y = michaelis_menten(x, Km, Vmax)
		yvals.append(y)
	inhib_Km, inhib_Vmax = adjust_MM_values(Km, Vmax, inhibition, xvals)
	inhibvals = []
	for x in xvals:
		y = michaelis_menten(x, inhib_Km, inhib_Vmax)
		inhibvals.append(y)
	table = makeTable(xvals, yvals, inhibvals, Vmax, inhib_Vmax)

	choices = copy.copy(xvals[:7])
	choices.remove(Km)
	random.shuffle(choices)
	while len(choices) > 4:
		choices.pop()
	choices.append(Km)
	choices.sort()

	#print(header+"\n")
	#print(table+"\n")
	#print(question+"\n")
	choices = ['competitive', 'un-competitive', 'non-competitive']
	extra_prefixes = [
		'ultra', 'hetero', 'homo', 'anti', 'super', 'dis', 'over', 'self', 'contra', 'intra', 'omni', 'ortho',
		'inter', 'mis', 'semi', 'auto', 'extra', 'hyper', 'pre', 'post', 'eco', 'hypo', 'iso', 'mega', 'para',
		'poly', 'oligo', 'proto', 'pseudo', 'quasi', 'supra', 'idio', 'epi',
		]
	for i in range(2):
		random.shuffle(extra_prefixes)
		prefix = extra_prefixes.pop(0)
		choices.append(prefix+'-competitive')
	choices.sort()

	question_text = header + table + '<br/>' + question
	bb_question = bptools.formatBB_MC_Question(N, question_text, choices, inhibition)
	return bb_question

#=============================
def _get_scenarios() -> list[tuple[str, int, float]]:
	# acceptable range: >40, <200, multiple of 20
	Vmax_choices = [40, 60, 80, 100, 120, 140, 160, 180, 200]
	inhibition_types = ['competitive', 'un-competitive', 'non-competitive']
	mode = 1

	xvals = makeXvals(mode)
	Km_choices = xvals[1:6]

	scenarios: list[tuple[str, int, float]] = []
	for inhibition in inhibition_types:
		for Vmax in Vmax_choices:
			for Km in Km_choices:
				scenarios.append((inhibition, Vmax, Km))
	return scenarios


#=============================
def write_question(N: int, args) -> str:
	mode = 1
	xvals = makeXvals(mode)
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	inhibition, Vmax, Km = SCENARIOS[idx]
	return makeCompleteProblem(N, xvals, Km, Vmax, inhibition)

#=============================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate Michaelis-Menten inhibition table questions.",
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
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
