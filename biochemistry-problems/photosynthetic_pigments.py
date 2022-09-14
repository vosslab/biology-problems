#!/usr/bin/env python3

import os
import sys
import copy
import random
import bptools
import itertools

base_colors = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']

wavelengths = (410, 430, 460, 530, 580, 600, 700,)

html_colors = ('#9d159d', '#4a0080', '#000080', '#006600', '#b3b300', '#e63900', '#990000')

leaf_colors = {
	'reddish yellow':     ('red', 'orange', 'yellow',),
	'orangeish yellow':   ('orange', 'yellow',),
	'yellowish green':    ('yellow', 'green',),
	'yellowish blue':     ('yellow', 'green', 'blue',),
	'greenish blue':      ('green', 'blue',),
	'blue and violet':    ('blue', 'violet',),
}

#==================================
def colorHtml(color_name):
	color_id = base_colors.index(color_name)
	wavelength = wavelengths[color_id]
	color_code = html_colors[color_id]
	html_text = '<span style="color: {0}"><strong>{1}</strong> ({2:d} nm)</span>'.format(color_code, color_name, wavelength)
	return html_text

#==================================
def writeChoice(name1, name2):
	choice = "{0} and {1}; ".format(colorHtml(name1), colorHtml(name2))
	return choice

#==================================
def colorDescription(leaf_color):
	mycolors = leaf_color.split(' ')
	and_text = None
	if len(mycolors) == 2:
		color1, color2 = mycolors
	elif len(mycolors) == 3:
		color1, and_text, color2 = mycolors
	color1true = color1.replace('dish', '')
	color1true = color1true.replace('ish', '')
	color_index1 = base_colors.index(color1true)
	color_index2 = base_colors.index(color2)
	html_text = '<strong><span style="color: {0}">{1}</span> '.format(html_colors[color_index1], color1)
	if and_text is not None:
		html_text += 'and '
	html_text += '<span style="color: {0}">{1}</span></strong>'.format(html_colors[color_index2], color2)
	return html_text

#==================================
#==================================
if __name__ == '__main__':
	answer_hist = {}
	num_duplicates = 2
	#==================================
	indices = list(range(7))
	set_indices = list(itertools.combinations(indices, 3))
	filtered_set_indices = []
	for color_set in set_indices:
		if color_set[1] - color_set[0] == 1 or color_set[2] - color_set[1] == 1:
			#make sure the colors are not next to one another
			continue
		filtered_set_indices.append(color_set)
	print("There are {0} possible color combinations after filtering".format(len(filtered_set_indices)))
	#print(set_indices)

	#==================================
	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	
	duplicates = 10
	
	for i in range(duplicates):
		for leaf_color in leaf_colors.keys():
			N += 1
			number = "{0}. ".format(N)
			color_desc = colorDescription(leaf_color)
			question = ""
			question += "<p>A plant with unique photosynthetic pigments has leaves that appear {0}.</p>".format(color_desc)
			question += "<p>Which one of the following wavelengths of visible light "
			question += "would most effectively be absorbed by this pigment?</p>"
	
			wrong_colors = leaf_colors[leaf_color]
	
			good_color_map = [True] * len(base_colors)
			for color in wrong_colors:
				color_index = base_colors.index(color)
				if color_index-1 > 0:
					good_color_map[color_index-1] = False
				good_color_map[color_index] = False
				if color_index+1 < len(good_color_map):
					good_color_map[color_index+1] = False
			#print(good_color_map)
	
			answer_colors = []		
			for i, v in enumerate(good_color_map):
				if v is True:
					answer_colors.append(base_colors[i])
			#print(answer_colors)
			
			
			indices = random.sample(range(len(answer_colors)), 2)
			indices.sort()
			a1 = answer_colors[indices[0]]
			a2 = answer_colors[indices[1]]
			answer = writeChoice(a1, a2)
	
			choices_list = []
			for i in range(10):
				names = [random.choice(answer_colors), random.choice(wrong_colors), ]
				random.shuffle(names)
				wrong_choice = writeChoice(names[0], names[1])
				choices_list.append(wrong_choice)
			choices_list = list(set(choices_list))
			random.shuffle(choices_list)
			choices_list = choices_list[:3]
	
			choices_list.append(answer)
			random.shuffle(choices_list)
	
			bbformat = bptools.formatBB_MC_Question(N, question, choices_list, answer)
			f.write(bbformat)

	f.close()
	bptools.print_histogram()


