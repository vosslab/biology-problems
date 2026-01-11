#!/usr/bin/env python3

import csv
import math
import random

import bptools

debug = False
_protein_tree_cache = None

#======================================
#======================================
def parse_protein_file():
	data_file_path = bptools.get_repo_data_path('protein_isoelectric_points.csv')
	file_handle = open(data_file_path, "r")
	reader = csv.reader(file_handle)
	protein_tree = []
	for row in reader:
		if reader.line_num == 1:
			#header = row
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
	question += '<p>What is the correct net charge on the {0} protein at <b>pH of {1:.1f}</b></p>? '.format(protein_dict['abbr'], pH)
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
#======================================
#======================================
def get_protein_tree() -> list:
	global _protein_tree_cache
	if _protein_tree_cache is None:
		_protein_tree_cache = parse_protein_file()
	return _protein_tree_cache

#======================================
#======================================
def write_question(N, args):
	protein_tree = get_protein_tree()
	protein_dict = random.choice(protein_tree)
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

def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with duplicates and max_questions.
	"""
	parser = bptools.make_arg_parser(description="Generate isoelectric point questions.")
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()
