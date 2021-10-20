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

def makeTable(xvals, yvals, inhibvals, Vmax, inhib_Vmax):
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
			print(y)
			print(Vmax - y)
			break
	table += '</table>'
	return table

def michaelis_menten(substrate_conc, Km, Vmax):
	V0 = Vmax * substrate_conc / float(substrate_conc + Km)
	V0 = math.ceil(V0*10.)/10.
	return V0

def adjust_MM_values(Km, Vmax, inhibition, xvals):
	Km_choices = copy.copy(xvals)
	random.shuffle(Km_choices)
	if inhibition == "competitive":
		inhib_Vmax = Vmax
		x = 1000
		while x > Km:
			x = Km_choices.pop()
		inhib_Km = x
	elif inhibition == "uncompetitive":
		if round(math.log10(Km / 2.) % 1, 3) < 0.001:
			## ends with a 2
			inhib_Km = round(Km * 2.5, 5)
		else:
			## ends with 1 or 5
			inhib_Km = round(Km * 2, 5)
		# KM/Vmax unchange
		raw_Vmax = Vmax * Km / inhib_Km
		inhib_Vmax = round(raw_Vmax/20.)*20
	elif inhibition == "noncompetitive":
		inhib_Km = Km
		index = random.randint(2, 4)
		Vmax_choices = [40, 60, 80, 100, 120, 140, 160, 180]
		random.shuffle(Vmax_choices)
		inhib_Vmax = 300
		while inhib_Vmax > Vmax:
			inhib_Vmax = Vmax_choices.pop(0)
	return inhib_Km, inhib_Vmax

def makeCompleteProblem(xvals, Km, Vmax, header, question, inhibition):
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

	bb_question = "MC\t{0}{1}<br/>{2}".format(header, table, question)

	print(header+"\n")
	print(table+"\n")
	print(question+"\n")
	letters = "ABCDEF"
	choices = ['competitive', 'uncompetitive', 'noncompetitive']
	extra_prefixes = [
		'ultra', 'hetero', 'homo', 'anti', 'super', 'dis', 'over', 'self', 'contra', 'intra', 'omni', 'ortho',
		'inter', 'mis', 'semi', 'auto', 'extra', 'hyper', 'pre', 'post', 'eco', 'hypo', 'iso', 'mega', 'para',
		'poly', 'oligo', 'proto', 'pseudo', 'quasi', 'supra', 'idio', 'epi',
		]
	for i in range(2):
		random.shuffle(extra_prefixes)
		prefix = extra_prefixes.pop(0)
		choices.append(prefix+'competitive')
	choices.sort()

	for i, choice in enumerate(choices):
		if choice == inhibition:
			prefix = "x"
			status = "Correct"
		else:
			prefix = " "
			status = "Incorrect"
		print("- [{0}] {1}. {2}".format(prefix, letters[i], choice))
		bb_question += "\t{0}\t{1}".format(choice, status)
	return bb_question

if __name__ == '__main__':
	### things don't change
	#acceptable range: >40, <200, multiple of 20
	Vmax_choices = [40, 60, 80, 100, 120, 140, 160, 180, 200]

	header = ""
	header += "<p><u>Michaelis-Menten question.</u>"
	header += " The following question refers to the table (<i>below</i>) of enzyme activity with and without an inhibitor.</p> "
	question = "<p>Using the table (<i>above</i>), determine the type of inhibition.</p>"

	f = open('bbq-michaelis_menten_table-inhibition.txt', 'w')

	### things that do change
	#Vmax = random.choice(Vmax_choices)
	#Km = random.choice(Km_choices)
	inhibition_types = ['competitive', 'uncompetitive', 'noncompetitive']

	mode = 1
	for inhibition in inhibition_types:
		for Vmax in Vmax_choices:
			xvals = makeXvals(mode)
			Km_choices = xvals[1:6]
			for Km in Km_choices:
				bb_question = makeCompleteProblem(xvals, Km, Vmax, header, question, inhibition)
				f.write("{0}\n".format(bb_question))
	f.close()
