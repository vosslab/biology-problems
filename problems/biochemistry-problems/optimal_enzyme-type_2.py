#!/usr/bin/env python3

import random

import bptools
import enzymelib


#======================================
def write_question(N, args):
	enzyme_tree = enzymelib.makeEnzymeTree(N)
	html_table = enzymelib.makeEnzymeHTMLTable(enzyme_tree)

	## choose enzyme
	enzyme_dict = random.choice(enzyme_tree)

	temp = random.randint(enzyme_dict['temp1']+1, enzyme_dict['temp2']-1)
	pH = enzyme_dict['optim_pH'] + random.randint(-2,2)/5.0

	question = ''
	question += '<p>Which one of the enzymes would be most active under the following conditions?</p> '
	question += '<p>The temperature is {0}&deg;C and the pH is {1:.1f}.</p>'.format(temp, pH)

	choices_list = []
	for edict in enzyme_tree:
		choice = "Enzyme {0}".format(edict['name'])
		choices_list.append(choice)
		if edict['name'] == enzyme_dict['name']:
			answer_text = choice

	#random.shuffle(choices_list)
	complete_question = bptools.formatBB_MC_Question(N, html_table+question, choices_list, answer_text)
	return complete_question

#======================================
#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate enzyme activity questions.")
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
