#!/usr/bin/env python

import csv
import math
import random

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

def writeQuestion(protein_dict, pH, N=77):
	question = "\n"
	question += "{0:d}. {1} <h6>Isoelectric Point Problem</h6> ".format(N, protein_dict['abbr'].lower())
	question += ('<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">')
	question += ('<tr><th>Protein Name</th><th>isoelectric point (pI)</th><th>molecular weight</th></tr>')
	question += ('<tr><td>{0} ({1})</td><td align="center">{2:.1f}</td><td align="center">{3:.1f}</td></tr>'.format(protein_dict['fullname'], protein_dict['abbr'], protein_dict['pI'], protein_dict['MW']))
	question += "</table>"
	question += '<p>The protein in the table (above) is placed in a buffer solution with a pH of {0:.1f}.</p> '.format(pH)
	#question += '<p>Check all of the answers below that apply. </p> '
	question += '<p>What is the correct net charge on the {0} protein at <b>pH of {1:.1f}</b>? '.format(protein_dict['abbr'], pH)

	'<span style="color:darkblue">'
	'<span style="color:darkred">'

	low_pH_answers = []
	high_pH_answers = []

	#low_pH_answers.append("Many amino groups will be protonated (&ndash;NH<sub>3</sub><sup>+</sup>)")
	#high_pH_answers.append("Many amino groups will be deprotonated (&ndash;NH<sub>2</sub>)")

	#low_pH_answers.append("Many carboxyl groups will be protonated (&ndash;COOH)")
	#high_pH_answers.append("Many carboxyl groups will be deprotonated (&ndash;COO<sup>&ndash;</sup>)")

	low_pH_answers.append('The protein will have a net <span style="color:darkblue">positive (+)</span> charge')
	high_pH_answers.append('The protein will have a net <span style="color:darkred">negative (&ndash;)</span> charge')
	neutral = ('The protein will have a <span style="color:goldenrod">neutral (0)</span> charge')

	if pH > protein_dict['pI']:
		answers = high_pH_answers
		wrongs = low_pH_answers
	else:
		answers = low_pH_answers
		wrongs = high_pH_answers

	wrongs.append(neutral)

	return question, answers, wrongs


def printQuestion(question, answers, wrongs):
	letters = "ABCDEFGH"
	print(question)

	for i in range(len(answers)):
		item_number = 2*i
		if random.random() < 0.5:
			print("*{0}. {1}".format(letters[2*i], answers[i]))
			print("{0}. {1}".format(letters[2*i+1], wrongs[i]))
		else:
			print("{0}. {1}".format(letters[2*i], wrongs[i]))
			print("*{0}. {1}".format(letters[2*i+1], answers[i]))
	print("{0}. {1}".format(letters[2*i+2], wrongs[-1]))



if __name__ == '__main__':
	question_count = 0
	protein_tree = parse_protein_file()
	answer_count = {1:0, 2:0, 3:0, 4:0}

	for protein_dict in protein_tree:
		pI = protein_dict['pI']
		low_pH = math.floor(2*pI)/2. - 1
		high_pH = math.ceil(2*pI)/2. + 1

		for pH in (low_pH, high_pH):
			if pH < 2 or pH > 12:
				continue
			question_count += 1
			question, answers, wrongs = writeQuestion(protein_dict, pH, question_count)
			printQuestion(question, answers, wrongs)
