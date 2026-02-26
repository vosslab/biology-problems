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

	question = '<br/>'
	question += '<p>Under which one of the following conditions would '
	question += f'<strong>enzyme {enzyme_dict["name"]}</strong> be '
	question += '<span style="color: DarkGreen;">most active</span>?</p> '

	good_pH = enzyme_dict['optim_pH'] + random.randint(-2,2)/5.0

	good_temp = random.randint(enzyme_dict['temp1']+1, enzyme_dict['temp2']-1)

	answer_text = f'The temperature is {good_temp}&deg;C and the pH is {good_pH:.1f}.'
	values = (-1, 0, 1)
	choices_list = []
	for pH_mult in values:
		for temp_mult in values:
			if pH_mult == temp_mult == 0:
				# this is the answer
				continue
			if temp_mult == -1:
				temp = enzyme_dict['temp1'] - random.randint(6,15)
			elif temp_mult == 1:
				temp = enzyme_dict['temp2'] + random.randint(6,15)
			else:
				temp = random.randint(enzyme_dict['temp1']+1, enzyme_dict['temp2']-1)

			if pH_mult == 0:
				pH = enzyme_dict['optim_pH'] + random.randint(-2,2)/5.0
			else:
				pH = enzyme_dict['optim_pH'] + pH_mult * random.randint(3,5)/2.0
			choice = f'The temperature is {temp}&deg;C and the pH is {pH:.1f}.'
			choices_list.append(choice)
	random.shuffle(choices_list)
	choices_list = choices_list[:4]

	choices_list.append(answer_text)
	random.shuffle(choices_list)
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
