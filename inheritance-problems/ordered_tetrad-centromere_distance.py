#!/usr/bin/env python3

import os
import sys
import random
import argparse

import bptools
debug = False

# Python 3 script to generate HTML for an ordered tetrad problem in genetics

def generate_html_for_pattern(pattern, color_dominant, color_recessive):
	"""
	Generate an HTML string for a given genetic pattern.

	Args:
	- pattern (str): The pattern of '+' and 'a' representing genetic outcomes.
	- color_dominant (str): The color representing '+'.
	- color_recessive (str): The color representing 'a'.

	Returns:
	- str: An HTML string representing the pattern.
	"""
	html_output = '<table border="0" style="padding: 10px;"> <tr>'

	# Create table cells based on the pattern
	for char in pattern:
		bgcolor = color_dominant if char == char.upper() or char == '+' else color_recessive
		html_output += f'<td width="40" height="40" bgcolor="{bgcolor}" style="border-radius: 30%; text-align: center; vertical-align: middle; color: #f0f0f0; font-size: 20px;"> '
		html_output += f'{char} </td> '

	html_output += '</tr></table>\n '
	return html_output

#=====================
#=====================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicates):
		N += 1

		# Define colors for the alleles
		color_dominant = "#FF0000"  # Red color for '+'
		color_recessive = "#0000FF"  # Blue color for 'a'

		# Define the four specific patterns
		patterns = [
			"++++aaaa",
			"aaaa++++",
			"aa++aa++",
			"++aa++aa",
			"aa++++aa",
			"++aaaa++",
		]

		formula = ( ''
			+ '<table border="0" style="border-collapse: collapse">'
			+ '<tr><td rowspan="2" style="; vertical-align: middle; text-align: right;">'
			+ 'distance between a gene<br/>and its centromere</td>'
			+ '<td rowspan="2" style="; vertical-align: middle; padding: 10px;">=</td>'
			+ '<td style="border-bottom: 1px solid black; text-align: center">'
			+ '&half; &times; (recombinant asci)'
			+ '</td></tr><tr><td style="border-top: 1px solid black; text-align: center">'
			+ 'total number of asci'
			+ '</td></tr></table>'
			)
		#ascomycetes

		color_dominant, color_recessive = bptools.default_color_wheel(2)

		octads_table = ''
		octads_table += '<table style="border: 1px solid black; border-collapse: collapse">'
		octads_table += '<tr><th style="padding: 10px; border: 1px solid gray; background-color: lightgray;">'
		octads_table += 'Octad'
		octads_table += '</th>'
		octads_table += '<th style="padding: 10px; border: 1px solid gray; background-color: lightgray;">'
		octads_table += 'Progeny<br/>Count'
		octads_table += '</th></tr>'
		# Generate and print the HTML for each pattern
		for i, pattern in enumerate(patterns, start=1):
			octads_table += '<tr><td style="padding: 10px; border: 1px solid gray;">'
			html_for_pattern = generate_html_for_pattern(pattern, color_dominant, color_recessive)
			octads_table += html_for_pattern
			octads_table += '</td><td style="padding: 10px; border: 1px solid gray; text-align: center">'
			octads_table += f'{12034:,d}'
			octads_table += '</td></tr>'
		octads_table += '</table>'

		full_question = octads_table + formula
		g = open('test.html', 'w')
		g.write(full_question)
		g.close()
		#bb_question = bptools.formatBB_MA_Question(N, full_question, choices_list, answers_list)
		#f.write(bb_question)
	f.close()
	bptools.print_histogram()
