#!/usr/bin/env python

import math
import copy
import random

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

def makeTable(xvals, yvals, Vmax):
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

def michaelis_menten(substrate_conc, Km, Vmax):
	V0 = Vmax * substrate_conc / float(substrate_conc + Km)
	V0 = math.ceil(V0*10.)/10.
	return V0


def makeCompleteProblem(xvals, Km, Vmax, header, question):
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

	bb_question = "MC\t{0}{1}<br/>{2}".format(header, table, question)

	print(header+"\n")
	print(table+"\n")
	print(question+"\n")
	letters = "ABCDEF"
	for i, choice in enumerate(choices):
		if abs(choice - Km) < 1e-6:
			prefix = "x"
			status = "Correct"
		else:
			prefix = " "
			status = "Incorrect"
		if xvals[0] < 0.0002:
			print("- [{0}] {1}. K<sub>M</sub> = {2:.4f}".format(prefix, letters[i], choice))
			bb_question += "\tK<sub>M</sub> = {0:.4f}\t{1}".format(choice, status)
		else:
			print("- [{0}] {1}. K<sub>M</sub> = {2:.3f}".format(prefix, letters[i], choice))
			bb_question += "\tK<sub>M</sub> = {0:.3f}\t{1}".format(choice, status)
	return bb_question

if __name__ == '__main__':
	### things don't change
	#acceptable range: >40, <200, multiple of 20
	Vmax_choices = [40, 60, 80, 100, 120, 140, 160, 180, 200]

	header = ""
	header += "<p><u>Michaelis-Menten question.</u>"
	header += " The following question refers to the table (<i>below</i>) of enzyme activity.</p> "
	question = "<p>Using the table (<i>above</i>), calculate the value for the Michaelis-Menten constant, K<sub>M</sub>.</p>"

	f = open('bbq-michaelis_menten_table-Km.txt', 'w')

	### things that do change
	#Vmax = random.choice(Vmax_choices)
	#Km = random.choice(Km_choices)

	for mode in (1,2):
		for Vmax in Vmax_choices:
			xvals = makeXvals(mode)
			Km_choices = xvals[:6]
			for Km in Km_choices:
				bb_question = makeCompleteProblem(xvals, Km, Vmax, header, question)
				f.write("{0}\n".format(bb_question))
	f.close()
