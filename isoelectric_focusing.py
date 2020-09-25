#!/usr/bin/env python

import csv
import math
import random

def parse_protein_file():
	filename = "protein_isoelectric_points.csv"
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
	print("Read data for {0} proteins".format(len(protein_tree)))
	return protein_tree

def random_select_proteins(protein_tree):
	random.shuffle(protein_tree)
	protein1 = protein_tree.pop()
	print("Selected: pI={0:.1f}, {1}".format(protein1['pI'], protein1['fullname']))
	pI1 = protein1['pI']
	pI2 = protein1['pI']
	while abs(pI1 - pI2) < 1.5:
		random.shuffle(protein_tree)
		protein2 = protein_tree.pop()
		pI2 = protein2['pI']
	print("Selected: pI={0:.1f}, {1}".format(protein2['pI'], protein2['fullname']))
	return protein1, protein2

def get_midpoint_pH(protein1, protein2):
	pI1 = protein1['pI']
	pI2 = protein2['pI']
	print("{0:.1f} / {1:.1f}".format(pI1,pI2))
	average = (pI1 + pI2)/2.0
	print("Average  pH: {0:.1f}".format(average))
	midpoint = round( (pI1 + pI2)) / 2.0
	print("Midpoint pH: {0:.1f}".format(midpoint))
	return midpoint

def get_peak_pH(protein1, protein2):
	pI1 = protein1['pI']
	pI2 = protein2['pI']
	min_pI = min(pI1, pI2)
	max_pI = max(pI1, pI2)
	print("{0:.1f} / {1:.1f} ... {2:.1f} / {3:.1f}".format(min_pI, max_pI, abs(min_pI - 7.0), abs(max_pI - 7.0) ))
	if abs(min_pI - 7.0) < abs(max_pI - 7.0):
		print("min")
		more_neutral_pI = min_pI
		best_peak_pI = math.floor(2*min_pI)/2. - 1
		other_peak_pI = math.ceil(2*max_pI)/2. + 1
	else:
		print("max")
		more_neutral_pI = max_pI
		best_peak_pI = math.ceil(2*max_pI)/2. + 1
		other_peak_pI = math.floor(2*min_pI)/2. - 1
	print("More Neutral pH: {0:.1f}".format(more_neutral_pI))
	print("Best Peak pH: {0:.1f}".format(best_peak_pI))
	print("Other Peak pH: {0:.1f}".format(other_peak_pI))
	return best_peak_pI,other_peak_pI

def writeQuestion(protein1, protein2, pH):
	question = "<h6>Isoelectric Point Problem</h6> "
	question += "<p>A mixture of two proteins are to be separated by isoelectric focusing.</p> "
	question += ('<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">')
	question += ('<tr><th>Protein Name</th><th>isoelectric point (pI)</th><th>molecular weight</th></tr>')
	question += ('<tr><td>{0} ({1})</td><td align="right">{2:.1f}</td><td align="right">{3:.1f}</td></tr>'.format(protein1['fullname'], protein1['abbr'], protein1['pI'], protein1['MW']))
	question += ('<tr><td>{0} ({1})</td><td align="right">{2:.1f}</td><td align="right">{3:.1f}</td></tr>'.format(protein2['fullname'], protein2['abbr'], protein2['pI'], protein2['MW']))
	question += "</table>"
	question += '<p>Both protein samples are placed into a gel with a constant pH of {0:.1f}. '.format(pH)
	question += 'The gel is then placed into an electric field. '
	'<span style="color:darkblue">'
	'<span style="color:darkred">'

	question += "In which direction will each protein in the table migrate at pH {0:.1f}</p>".format(pH)
	"""
	A. both tran and gal toward the positive (+) terminal
	C. tran toward the positive (+) and gal toward the negative (–)
	B. both tran and gal toward the negative (–) terminal
	D. tran toward the negative (–) and gal toward the positive (+)
	"""
	return question

	pass

if __name__ == '__main__':
	protein_tree = parse_protein_file()
	protein1, protein2 = random_select_proteins(protein_tree)
	midpoint_pH = get_midpoint_pH(protein1, protein2)
	best_peak_pI,other_peak_pI = get_peak_pH(protein1, protein2)
	print(writeQuestion(protein1, protein2, best_peak_pI))


