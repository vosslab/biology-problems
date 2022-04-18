#!/usr/bin/env python

import os
import sys
import copy
import random
import bptools
import itertools

def enzyme_table(metabolites, color_wheel):
	htmltext = ""
	tdopen_top = '<td align="center" valign="top" >'
	tdopen_bot = '<td align="center" valign="bottom" >'
	htmltext += '<table cellpadding="2" cellspacing="2"'
	htmltext += '  style="background-color: #efefef; text-align:center; '
	htmltext += '  border: 1px solid black; font-size: 14px;"> '  
	htmltext += '<tr> '
	enzyme_count = len(metabolites) - 1
	for i in range(enzyme_count):
		enzyme_num = i+1
		htmltext += '<td></td> {0}<span style="font-size: 12px;">enzyme {1:d}</span></td> '.format(tdopen_bot, enzyme_num)
	htmltext += '</tr><tr> '
	for i,meta in enumerate(metabolites):
		color = color_wheel[i]
		htmltext += '{0}<span style="color: {1}; font-size: 20px;"><strong>{2}</strong></span></td> '.format(tdopen_top, color, meta)
		if i+1 != len(metabolites):
			htmltext += '{0}<span style="font-size: 16px;">&xrarr;</span></td> '.format(tdopen_top)
	htmltext += '</tr> '
	htmltext += '</table>'
	return htmltext


def make_question(N, num_metabolites):
	metabolites = bptools.getGeneLetters(num_metabolites, shift=N, upper=True)
	#print("metabolites letters = ", metabolites)
	
	deg_step = int(round(360./len(metabolites) - 1))
	color_amount = 240
	color_wheel = bptools.make_color_wheel(color_amount, 0, 0, deg_step)
	
	question = '<p>Refer to the metabolic pathway in the table above.</p>'
	question += '<p>Metabolites '
	for i, meta in enumerate(metabolites):
		color = color_wheel[i]
		question += '<span style="color: {0};"><strong>{1}</strong></span>, '.format(color, meta)
		if i == len(metabolites) - 2:
			question += 'and '
	question = question[:-2]
	question += ' are ALL required for growth.</p>'

	enzyme_num = random.choice(range(1, len(metabolites)))
	
	question += '<p>Which one of the following supplemented media conditions '
	question += 'would a bacterial strain that <strong>CANNOT</strong> make '
	question += '<strong>enzyme {0:d}</strong> be able to grow?</p>'.format(enzyme_num)

	question = enzyme_table(metabolites, color_wheel) + question

	choices_list = []
	
	indices = list(range(len(metabolites)))
	random.shuffle(indices)
	indices = indices[:2]
	indices.sort()	
	#for i in range(len(metabolites)):
	for i in indices:
		color1 = color_wheel[i]
		meta1 = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color1, metabolites[i])
		choice = "Nutrient {0} only".format(meta1)
		choices_list.append(choice)

	
	indices = list(range(1, len(metabolites)))
	indices.remove(enzyme_num)
	random.shuffle(indices)
	indices = indices[:2]
	indices.append(enzyme_num)
	indices.sort()
	for i in indices:
		color1 = color_wheel[i-1]
		meta1 = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color1, metabolites[i-1])
		color2 = color_wheel[i]
		meta2 = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color2, metabolites[i])		
		choice = "Nutrients {0} and {1} only".format(meta1, meta2)
		if i == enzyme_num:
			answer = choice
		choices_list.append(choice)

	indices = list(range(2, len(metabolites)))
	try:
		indices.remove(enzyme_num+1)
	except ValueError:
		pass
	try:
		indices.remove(enzyme_num)
	except ValueError:
		pass
	random.shuffle(indices)
	indices = indices[:1]
	indices.sort()
	for i in indices:
		color1 = color_wheel[i-2]
		meta1 = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color1, metabolites[i-2])
		color2 = color_wheel[i-1]
		meta2 = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color2, metabolites[i-1])		
		color3 = color_wheel[i]
		meta3 = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color3, metabolites[i])		
		choice = "Nutrients {0}, {1}, and {2} only".format(meta1, meta2, meta3)
		choices_list.append(choice)

	#choices_list.sort()
	#f = open('temp.html', 'w')
	#f.write(question)
	#for c in choices_list:
	#	f.write(c+'<br/>')
	#f.close()

	#print(answer)


	bbformat_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbformat_question

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_metabolites = int(sys.argv[1])
	else:
		num_metabolites = 4

	duplicates = 24

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(duplicates):
		N = i + 1
		bbformat_question = make_question(N, num_metabolites)
		f.write(bbformat_question)
	f.close()	

	

