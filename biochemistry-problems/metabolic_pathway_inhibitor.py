#!/usr/bin/env python

import os
import sys
import copy
import random

import bptools

all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_colors = ['DarkRed', 'DarkOrange', 'DarkGoldenRod', 'DarkGreen',
				  'DarkCyan', 'DarkBlue', 'DarkSlateBlue', 'DarkMagenta',
				  'DarkViolet', ]

#======================================
#======================================
def getLetters(N):
	letter_index = N % (len(all_letters) - 4)
	letters = list(all_letters[letter_index:letter_index+4])

	color_index = N % len(all_colors)
	local_colors = all_colors + all_colors
	colors = local_colors[color_index:color_index+4]

	html_letters = []
	for i,ltr in enumerate(letters):
		clr = colors[i]
		html_text = '<strong><span style="color: {0}">{1}</span></strong>'.format(clr, ltr)
		html_letters.append(html_text)
	return html_letters

#======================================
#======================================
def writeQuestion(N):
	letters = getLetters(N)
	
	question_text = ''
	question_text += '<p>A series of enzymes catalyze the reaction'
	question_text += ' {0} &rarr; {1} &rarr; {2} &rarr; {3}.</p> '.format(letters[0],letters[1],letters[2],letters[3],)
	question_text += '<p>Product {2} binds to the enzyme that converts {0} &rarr; {1} '.format(letters[0],letters[1],letters[3],)

	question_text_list = [
		'in its active site.</p> ',
		'at a location far away from its active site.</p> ',
		'at a location far away from its active site.</p> ',
		]
	choices_list = [
		'competitive inhibitor',
		'non-competitive inhibitor',
		'activator',
		'molecular stopper',
		]
	choice_index = random.randint(0,2)
	answer_text = choices_list[choice_index]
	question_text += question_text_list[choice_index]

	if choice_index in (0,1,):
		question_text += '<p>This binding <strong><span style="color: brown">decreases</span></strong> the activity of the enzyme.</p> '
	else:
		question_text += '<p>This binding <strong><span style="color: seagreen">increases</span></strong> the activity of the enzyme.</p> '
	question_text += '<p>What does substance {0} functions as?</p>'.format(letters[3],)

	new_choices_list = copy.copy(choices_list)
	random.shuffle(new_choices_list)

	complete_question = bptools.formatBB_MC_Question(N, question_text, new_choices_list, answer_text)
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
		complete_question = writeQuestion(d)
		f.write(complete_question)
	f.close()
