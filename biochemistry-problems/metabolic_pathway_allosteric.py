#!/usr/bin/env python3

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
def getLetters(N, num_letters=6):
	letter_index = N % (len(all_letters) - num_letters)
	letters = list(all_letters[letter_index:letter_index+num_letters])

	color_index = N % len(all_colors)
	local_colors = all_colors + all_colors
	colors = local_colors[color_index:color_index+num_letters]

	html_letters = []
	for i,ltr in enumerate(letters):
		clr = colors[i]
		html_text = '<strong><span style="color: {0}">{1}</span></strong>'.format(clr, ltr)
		html_letters.append(html_text)
	return html_letters

#======================================
#======================================
def generate_metabolic_pathway(letters):
	# Ensure there are at least 3 letters for the pathway
	if len(letters) < 3:
		return 'Not enough molecules provided for the pathway.'

	# Create the base of the question
	question_text = '<p>A series of enzymes catalyze the reactions in the following metabolic pathway:</p>'

	# Create the table
	question_text += '<table border="2" style="border-collapse: collapse;">'

	# Add the enzymes row
	question_text += '<tr>'
	question_text += '<td></td>'  # Leading empty cell
	question_text += '<td></td>'  # Leading empty cell
	for i in range(len(letters) - 1):
		question_text += f'<td style="font-size: 50%; text-align:center; vertical-align: bottom;" colspan=3>enzyme {i+1}</td>\n'
		question_text += '<td>&nbsp;</td>\n'  # Trailing empty cell
	question_text += '<td></td>\n'  # Trailing empty cell
	question_text += '</tr>\n'

	# Add the molecules and arrows row
	question_text += '<tr>'
	for i in range(len(letters) - 1):
		question_text += f'<td style="font-size: 125%; text-align:center;" colspan=3>{letters[i]}</td>\n'
		question_text += '<td style="text-align:center; vertical-align:top;">&nbsp;&xrarr;&nbsp;</td>\n'
	# Add the last molecule
	question_text += f'<td style="font-size: 125%; text-align:center;" colspan=3>{letters[-1]}</td>\n'
	question_text += '</tr>\n'

	question_text += '<tr>'
	for i in range(len(letters)*4-1):
		question_text += "<td><span style='font-size: 1px; color: white;'>&nbsp;</span></td>"
	question_text += '</tr>\n'
	question_text += '</table>'

	return question_text

#======================================
#======================================
def writeQuestion(N):
	letters = getLetters(N)
	question_text = generate_metabolic_pathway(letters)
	print(question_text)
	sys.exit(1)
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
