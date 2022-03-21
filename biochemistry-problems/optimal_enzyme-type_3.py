#!/usr/bin/env python

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

	question = '<br/>'
	question += '<p>Under which one of the following conditions would '
	question += '<strong>enzyme {0}</strong> be '.format(enzyme_dict['name'])
	question += '<span style="color: DarkGreen;">most active</span>?</p> '
	
	good_pH = enzyme_dict['optim_pH'] + random.randint(-2,2)/5.0
	too_low_pH = enzyme_dict['optim_pH'] - random.randint(3,5)/2.0
	too_high_pH = enzyme_dict['optim_pH'] - random.randint(3,5)/2.0

	good_temp = random.randint(enzyme_dict['temp1']+1, enzyme_dict['temp2']-1)
	too_low_temp = enzyme_dict['temp1'] - random.randint(6,15)
	too_high_temp = enzyme_dict['temp1'] + random.randint(6,15)

	temp_values = [too_low_temp, good_temp, too_high_temp,]
	pH_values = [too_low_pH, good_pH, too_high_pH,]
	
	answer_text = 'The temperature is {0}&deg;C and the pH is {1:.1f}.'.format(good_temp, good_pH)
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
			choice = 'The temperature is {0}&deg;C and the pH is {1:.1f}.'.format(temp, pH)
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
#======================================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 95

	for d in range(duplicates):
		complete_question = writeQuestion1(d+1)
		if complete_question is not None:
			f.write(complete_question)
	f.close()



