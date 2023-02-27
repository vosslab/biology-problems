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

	#Three question types:
	## A. good temp, too low pH
	## B. good temp, too high pH
	## C. too low temp, good pH
	question_type = random.choice(list('ABC'))
	increased = '<span style="color: DarkGreen;">increased</span>'
	decreased = '<span style="color: DarkRed;">decreased</span>'
	kept_same = '<i><span style="color: Gray;">kept the same</span></i>'

	good_temp = random.randint(enzyme_dict['temp1']+1, enzyme_dict['temp2']-1)
	optim_pH = enzyme_dict['optim_pH']
	too_low_pH = enzyme_dict['optim_pH'] - random.randint(3,5)/2.0
	too_high_pH = enzyme_dict['optim_pH'] - random.randint(3,5)/2.0
	too_low_temp = enzyme_dict['temp1'] - random.randint(6,15)

	question = '<br/>'
	question += '<p>If <strong>enzyme {0}</strong> is currently functioning '.format(enzyme_dict['name'])
	if question_type == 'A': ## A. good temp, too low pH
		current_temp = good_temp
		current_pH = too_low_pH
		question += 'at {0}&deg;C and a pH of {1}.</p> '.format(good_temp, too_low_pH)
	elif question_type == 'B': ## B. good temp, too high pH
		current_temp = good_temp
		current_pH = too_high_pH
		question += 'at {0}&deg;C and a pH of {1}.</p> '.format(good_temp, too_high_pH)
	elif question_type == 'C': ## C. too low temp, good pH
		current_temp = too_low_temp
		current_pH = optim_pH
		question += 'at {0}&deg;C and a pH of {1}.</p> '.format(too_low_temp, optim_pH)

	question += '<p>Which one of the following conditions would '
	question += '<strong><span style="color: DarkGreen;">increase</span></strong> '
	question += 'the rate of enzyme activity</p>'

	low_temp = current_temp - random.randint(5,14)
	choice1 = 'The temperature is {1} to {0}&deg;C and the pH is {2}.'.format(low_temp, decreased, kept_same)
	if question_type == 'A': ## A. good temp, too low pH
		high_temp = enzyme_dict['temp1'] + random.randint(5,14)
		choice2 = 'The temperature is {1} to {0}&deg;C and the pH is {2}.'.format(high_temp, increased, kept_same)
		low_pH = current_pH - random.randint(2,5)/2.0
		choice3 = 'The temperature is {2} and the pH is {1} to {0}.'.format(low_pH, decreased, kept_same)
		new_pH = enzyme_dict['optim_pH'] - 0.5
		answer_text = 'The temperature is {2} and the pH is {1} to {0}.'.format(new_pH, increased, kept_same)
	elif question_type == 'B': ## B. good temp, too high pH
		high_temp = enzyme_dict['temp1'] + random.randint(5,14)
		choice2 = 'The temperature is {1} to {0}&deg;C and the pH is {2}.'.format(high_temp, increased, kept_same)
		high_pH = current_pH + random.randint(2,5)/2.0
		choice3 = 'The temperature is {2} and the pH is {1} to {0}.'.format(high_pH, increased, kept_same)
		new_pH = enzyme_dict['optim_pH'] + 0.5
		answer_text = 'The temperature is {2} and the pH is {1} to {0}.'.format(new_pH, decreased, kept_same)
	elif question_type == 'C': ## C. too low temp, good pH
		high_pH = current_pH + random.randint(2,5)/2.0
		choice2 = 'The temperature is {2} and the pH is {1} to {0}.'.format(high_pH, increased, kept_same)
		low_pH = current_pH - random.randint(2,5)/2.0
		choice3 = 'The temperature is {2} and the pH is {1} to {0}.'.format(low_pH, decreased, kept_same)
		answer_text = 'The temperature is {1} to {0}&deg;C and the pH is {2}.'.format(good_temp, increased, kept_same)

	choices_list = [choice1, choice2, choice3, answer_text]
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
	duplicates = 97

	for d in range(duplicates):
		complete_question = writeQuestion1(d+1)
		if complete_question is not None:
			f.write(complete_question)
	f.close()



