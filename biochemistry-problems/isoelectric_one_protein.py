#!/usr/bin/env python3

import os
import csv
import math
import random
import argparse

import bptools

debug = False

#======================================
#======================================
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


#======================================
#======================================
def get_question_text(protein_dict, pH) -> str:
	"""Generates the question text.

	Returns:
		str: The question text in HTML format.
	"""
	question = ''
	question += "<h6>Isoelectric Point Problem</h6> "
	question += ('<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">')
	question += ('<tr><th>Protein Name</th><th>isoelectric point (pI)</th><th>molecular weight</th></tr>')
	question += ('<tr><td>{0} ({1})</td><td align="center">{2:.1f}</td><td align="center">{3:.1f}</td></tr>'.format(protein_dict['fullname'], protein_dict['abbr'], protein_dict['pI'], protein_dict['MW']))
	question += "</table>"
	question += '<p>The protein in the table (above) is placed in a buffer solution with a pH of {0:.1f}.</p> '.format(pH)
	#question += '<p>Check all of the answers below that apply. </p> '
	question += '<p>What is the correct net charge on the {0} protein at <b>pH of {1:.1f}</b>? '.format(protein_dict['abbr'], pH)
	return question

#======================================
#======================================
def generate_choices(isoelectric_point_pI, pH):
	#low_pH_answers.append("Many amino groups will be protonated (&ndash;NH<sub>3</sub><sup>+</sup>)")
	#high_pH_answers.append("Many amino groups will be deprotonated (&ndash;NH<sub>2</sub>)")
	#low_pH_answers.append("Many carboxyl groups will be protonated (&ndash;COOH)")
	#high_pH_answers.append("Many carboxyl groups will be deprotonated (&ndash;COO<sup>&ndash;</sup>)")
	pre_text = 'The protein will have a net <strong><span style="color:'
	end_text = '</span></strong> charge.'
	low_pH_choice = f'{pre_text} darkblue">positive (+){end_text}'
	high_pH_choice = f'{pre_text} darkred">negative (&ndash;){end_text}'
	neutral_choice = f'{pre_text} goldenrod">neutral (0){end_text}'
	choices_list = [low_pH_choice, high_pH_choice, neutral_choice]
	choices_list.sort()

	if pH > isoelectric_point_pI:
		answer_text = high_pH_choice
	else:
		answer_text = low_pH_choice

	return choices_list, answer_text


#======================================
#======================================
def write_question(N, protein_dict):
	pI = protein_dict['pI']

	pH_values = []
	low_pH = math.floor(2*pI)/2. - 1
	if 2 < low_pH < 12:
		pH_values.append(low_pH)
	high_pH = math.ceil(2*pI)/2. + 1
	if 2 < high_pH < 12:
		pH_values.append(high_pH)

	if len(pH_values) == 0:
		return None

	pH = random.choice(pH_values)
	question_text = get_question_text(protein_dict, pH)
	choices_list, answer_text = generate_choices(protein_dict['pI'], pH)
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question


#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=1, help="Number of questions to create.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	protein_tree = parse_protein_file()


	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 0
		for d in range(args.duplicates):
			for protein_dict in protein_tree:
				N += 1
				complete_question = write_question(N, protein_dict)
				if complete_question is not None:
					f.write(complete_question)
	bptools.print_histogram()


#======================================
#======================================
if __name__ == '__main__':
	main()
