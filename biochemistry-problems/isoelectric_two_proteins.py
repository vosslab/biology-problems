#!/usr/bin/env python3

import os
import csv
import math
import random

import bptools

debug = False

def parse_protein_file():
	filename = "../data/protein_isoelectric_points.csv"
	file_handle = open(filename, "r")
	reader = csv.reader(file_handle)
	protein_tree = []
	for row in reader:
		if reader.line_num == 1:
			header = row
			continue
		try:
			protein_dict = {
				'fullname': row[0],
				'abbr':	row[1],
				'pI':	float(row[2]),
				'MW': float(row[3]),
			}
			protein_tree.append(protein_dict)
		except ValueError:
			pass
	if debug is True:
		print("Read data for {0} proteins".format(len(protein_tree)))
	return protein_tree

def random_select_proteins(protein_tree):
	random.shuffle(protein_tree)
	protein1 = protein_tree.pop()
	if debug is True:
		print("Selected: pI={0:.1f}, {1}".format(protein1['pI'], protein1['fullname']))
	pI1 = protein1['pI']
	pI2 = protein1['pI']
	while abs(pI1 - pI2) < 1.5:
		random.shuffle(protein_tree)
		protein2 = protein_tree.pop()
		pI2 = protein2['pI']
	if debug is True:
		print("Selected: pI={0:.1f}, {1}".format(protein2['pI'], protein2['fullname']))
	return protein1, protein2

def get_midpoint_pH(protein1, protein2):
	pI1 = protein1['pI']
	pI2 = protein2['pI']
	if debug is True:
		print("{0:.1f} / {1:.1f}".format(pI1,pI2))
	average = (pI1 + pI2)/2.0
	if debug is True:
		print("Average  pH: {0:.1f}".format(average))
	midpoint = round( (pI1 + pI2)) / 2.0
	if debug is True:
		print("Midpoint pH: {0:.1f}".format(midpoint))
	return midpoint

def get_peak_pH(protein1, protein2):
	pI1 = protein1['pI']
	pI2 = protein2['pI']
	min_pI = min(pI1, pI2)
	max_pI = max(pI1, pI2)
	if debug is True:
		print("{0:.1f} / {1:.1f} ... {2:.1f} / {3:.1f}".format(min_pI, max_pI, abs(min_pI - 7.0), abs(max_pI - 7.0) ))
	if abs(min_pI - 7.0) < abs(max_pI - 7.0):
		if debug is True:
			print("min")
		more_neutral_pI = min_pI
		best_peak_pI = math.floor(2*min_pI)/2. - 1
		other_peak_pI = math.ceil(2*max_pI)/2. + 1
	else:
		if debug is True:
			print("max")
		more_neutral_pI = max_pI
		best_peak_pI = math.ceil(2*max_pI)/2. + 1
		other_peak_pI = math.floor(2*min_pI)/2. - 1
	if debug is True:
		print("More Neutral pH: {0:.1f}".format(more_neutral_pI))
		print("Best Peak pH: {0:.1f}".format(best_peak_pI))
		print("Other Peak pH: {0:.1f}".format(other_peak_pI))
	return best_peak_pI,other_peak_pI

def writeQuestion(protein1, protein2, pH, N=77):
	question = ''
	ab1 = protein1['abbr']
	ab2 = protein2['abbr']

	question += "<h6>Isoelectric Point Problem</h6> "
	question += "<p>A mixture of two proteins are to be separated by isoelectric focusing.</p> "
	question += ('<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black;">')
	question += ('<tr><th>Protein<br/>Name</th><th>Isoelectric<br/>Point (pI)</th><th>Molecular<br/>Weight</th></tr>')
	question += ('<tr><td>{0} ({1})</td><td align="right">{2:.1f}</td><td align="right">{3:.1f}</td></tr>'.format(protein1['fullname'], protein1['abbr'], protein1['pI'], protein1['MW']))
	question += ('<tr><td>{0} ({1})</td><td align="right">{2:.1f}</td><td align="right">{3:.1f}</td></tr>'.format(protein2['fullname'], protein2['abbr'], protein2['pI'], protein2['MW']))
	question += "</table>"
	question += '<p>Both protein samples are placed into a gel with a constant pH of {0:.1f}. '.format(pH)
	question += 'The gel is then placed into an electric field.</p> '
	'<span style="color:darkblue">'
	'<span style="color:darkred">'

	question += "<p>In which direction will each protein in the table migrate at <b>pH {0:.1f}</b></p>".format(pH)

	# when the pH is above the pI, the protein is negatively charged
	# when the pH is below the pI, the protein is positively charged

	if pH > protein1['pI'] and pH > protein2['pI']:
		#both have negative charge; go towards positive
		answer_id = 0
	elif pH < protein1['pI'] and pH < protein2['pI']:
		#both have positive charge; go towards negative
		answer_id = 1
	elif protein1['pI'] > pH > protein2['pI']:
		#protein 1 is negative and protein 2 is positive; protein 1 goes positive and protein 2 goes negative
		answer_id = 2
	elif protein1['pI'] < pH < protein2['pI']:
		#protein 1 is positive and protein 2 is negative; protein 1 goes negative and protein 2 goes positive
		answer_id = 3

	choice1 = ('Both {0} and {1} will have a <span style="color:darkred">negative (&ndash;)</span> charge '.format(ab1, ab2)
		+ 'and travel towards the <span style="color:darkblue">positive (+)</span> terminal')
	choice2 = ('Both {0} and {1} will have a <span style="color:darkblue">positive (+)</span> charge '.format(ab1, ab2)
		+ 'and travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal')
	choice3 = ('{0} will have a <span style="color:darkblue">positive (+)</span> charge '.format(ab1)
		+ 'and travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal<br/> '
		+ '{0} will have a <span style="color:darkred">negative (&ndash;)</span> charge '.format(ab2)
		+ 'and travel towards the <span style="color:darkblue">positive (+)</span> terminal ')
	choice4 = ('{0} will have a <span style="color:darkred">negative (&ndash;)</span> charge '.format(ab1)
		+ 'and travel towards the <span style="color:darkblue">positive (+)</span> terminal<br/> '
		+ '{0} will have a <span style="color:darkblue">positive (+)</span> charge '.format(ab2)
		+ 'and travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal ')

	choices_list = [choice1, choice2, choice3, choice4,]
	answer = choices_list[answer_id]

	bb_format = bptools.formatBB_MC_Question(N, question, choices_list, answer)

	return bb_format


if __name__ == '__main__':
	question_count = 0
	protein_tree = parse_protein_file()
	answer_count = {1:0, 2:0, 3:0, 4:0}

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')

	while(question_count < 24):
		protein1, protein2 = random_select_proteins(protein_tree.copy())
		midpoint_pH = get_midpoint_pH(protein1, protein2)
		best_peak_pI,other_peak_pI = get_peak_pH(protein1, protein2)

		pH_list = [midpoint_pH, best_peak_pI, other_peak_pI, midpoint_pH]
		pH = random.choice(pH_list)
		if pH < 2 or pH > 12:
			continue
		question_count += 1
		bb_format= writeQuestion(protein1, protein2, pH, question_count)
		f.write(bb_format)
	f.close()
	bptools.print_histogram()
