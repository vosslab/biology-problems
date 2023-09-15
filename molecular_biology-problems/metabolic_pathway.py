#!/usr/bin/env python3

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

	question = '<p>Look at the metabolic pathway in the table above.</p>'
	question += '<p>Metabolite '
	color = color_wheel[len(metabolites)]
	question += '<span style="color: {0};"><strong>{1}</strong></span>'.format(color, metabolites[-1])
	question += ' is needed for the bacteria to grow.</p>'

	enzyme_num = random.choice(range(1, len(metabolites)))

	question += '<p>Consider a bacterial strain that is mutant for the gene coding for enzyme {0:d}</p>'.format(enzyme_num)
	question += '<p>Which nutrients, when added to minimal media, will help this bacteria grow?</p>'
	question += '<p>Multiple answers may be correct.</p>'

	question = enzyme_table(metabolites, color_wheel) + question

	choices_list = []
	answers_list = []

	indices = list(range(len(metabolites)))
	random.shuffle(indices)
	indices = indices[:2]
	indices.sort()
	#for i in range(len(metabolites)):
	for i,meta in enumerate(metabolites):
		color_txt = color_wheel[i]
		meta_txt = '<span style="color: {0};"><strong>{1}</strong></span>'.format(color_txt, meta)
		choice = "Supplemented with nutrient {0}".format(meta_txt)
		choices_list.append(choice)
		if i >= enzyme_num:
			answers_list.append(choice)

	bbformat_question = bptools.formatBB_MA_Question(N, question, choices_list, answers_list)
	#bbformat_question = bptools.formatBB_MC_Question(N, question, choices_list, answer)
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

	

