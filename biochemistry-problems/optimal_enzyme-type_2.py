#!/usr/bin/env python3

import os
import random

import bptools
import enzymelib


#======================================
def writeQuestion1(N):
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
#======================================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 96

	for d in range(duplicates):
		complete_question = writeQuestion1(d+1)
		if complete_question is not None:
			f.write(complete_question)
	f.close()



