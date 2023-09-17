#!/usr/bin/env python3

import os
import sys
import random
import argparse

import bptools
import gellib

debug = None

# Define complexity styles
COMPLEXITY_STYLES = {
	'easy': {'num_males': 4, 'num_bands': 18,},
	'medium': {'num_males': 5, 'num_bands': 24,},
	'hard': {'num_males': 9, 'num_bands': 32,}
}

#================
def init_gel_params(style):
	if style not in COMPLEXITY_STYLES:
		print(f"Error: Style '{style}' not recognized. Available styles are {', '.join(COMPLEXITY_STYLES.keys())}.")
		sys.exit(1)
	return COMPLEXITY_STYLES[style]

#================
#================
def writeQuestion(N, params, debug):
	# Initialization
	rflp_class = gellib.RFLPClass(params['num_bands'])
	rflp_class.debug = debug
	results = None
	while results is None:
		results = rflp_class.create_family()
	mother, father, child = results
	# Create additional males
	males = rflp_class.create_additional_males(params['num_males'])

	# Generate the HTML table
	table, answer_index = rflp_class.make_unknown_males_HTML_table()
	rflp_class.make_unknown_males_PNG_image()

	# Define the sub-headings and questions as HTML
	background = "<h6>Background</h6><p>Restriction Fragment Length Polymorphism (RFLP) is a molecular biology technique used to distinguish between closely related DNA samples. It's commonly employed in paternity tests, among other applications.</p>"
	the_question = "<h6>The Question</h6><p>Who is the father of the child?</p>"
	instructions = "<h6>Instructions</h6><p>Use the provided DNA gel profile to determine paternity. Each band in the gel corresponds to a DNA fragment. Fragments are inherited; thus, the child's DNA will have overlapping fragments with the true father.</p>"

	# Combine all elements to form the full question
	full_question = "{0} {1} {2} {3}".format(the_question, table, background, instructions)

	choices_list = []
	for i, male in enumerate(males):
		choice = "Male &num;{0:d}".format(i+1)
		choices_list.append(choice)
		if i == answer_index:
			answer_string = choice
	bb_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_string)
	return bb_question

#================
#================
if __name__ == '__main__':
	# Command-line argument parsing moved here
	parser = argparse.ArgumentParser(description="Generate DNA gel questions.")
	parser.add_argument('-s', '--style', type=str, default='medium',
		help='The complexity style for generating questions (easy, medium, hard)')
	parser.add_argument('-d', '--debug', dest='debug', action='store_true',
		help='Enable debug mode, which changes the question output.')
	parser.add_argument('-x', '--max_questions', dest='max_questions', type=int, default=3,
		help='Number of questions to write')
	parser.set_defaults(debug=False)

	args = parser.parse_args()
	params = init_gel_params(args.style)

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')
	with open(outfile, 'w') as f:
		for i in range(args.max_questions):
			N = i + 1
			bb_question = writeQuestion(N, params, args.debug)
			if bb_question is None:
				continue
			f.write(bb_question)
		f.write("\n")
	bptools.print_histogram()
