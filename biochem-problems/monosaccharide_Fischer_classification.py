#!/usr/bin/env python

import os
import sys
import random
import sugarlib

N = 0

def makeQuestion(sugar_name):
	global N
	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	sugar_struct = sugarlib.SugarStructure(sugar_code)
	#print(sugar_struct.structural_part_txt())
	haworth = sugar_struct.Fischer_projection_html()

	question = ''
	question += 'Above is a Fischer projection of a monosaccharide. '
	question += 'For each of the following categorizations, '
	question += 'check all the categorizations that apply to the sugar above. '
	question += 'You will check exactly three (3) boxes. '

	choices = [
		'triose (3)',
		'tetrose (4)',
		'pentose (5)',
		'hexose (6)',
		'D-configuration',
		'L-configuration',
		'aldose',
		'ketose',
		'3-ketose',
	]

	answers = {}

	if len(sugar_code) == 3:
		answers['triose (3)'] = True
	elif len(sugar_code) == 4:
		answers['tetrose (4)'] = True
	elif len(sugar_code) == 5:
		answers['pentose (5)'] = True
	elif len(sugar_code) == 6:
		answers['hexose (6)'] = True
	elif len(sugar_code) == 7:
		answers['septose (7)'] = True

	if sugar_code[-2] == 'D':
		answers['D-configuration'] = True
	elif sugar_code[-2] == 'L':
		answers['L-configuration'] = True

	if sugar_code.startswith('MK'):
		answers['ketose'] = True
	elif sugar_code.startswith('A'):
		answers['aldose'] = True
	if sugar_code.startswith('M') and sugar_code[2] == 'K':
		answers['3-ketose'] = True

	N += 1
	content = 'MA\t<p>Fischer classification problem &num;{0}</p> '.format(N)
	content += haworth
	content += question

	for choice in choices:
		content += "\t"+choice
		if answers.get(choice, False) is True:
			content += "\tCorrect"
		else:
			content += "\tIncorrect"
	return content

if __name__ == '__main__':
	sugar_codes_class = sugarlib.SugarCodes()
	sugars = []
	sugars += sugar_codes_class.get_sugar_names(4, 'D', None)
	sugars += sugar_codes_class.get_sugar_names(4, 'L', None)
	sugars += sugar_codes_class.get_sugar_names(5, 'D', None)
	sugars += sugar_codes_class.get_sugar_names(5, 'L', None)
	#sugars += sugar_codes_class.get_sugar_names(6, None, 'aldo')
	#print(sugars)
	sugars.remove('D-ribose')
	#sugars.remove('D-fructose')
	#sugars.remove('D-glucose')
	#sugars.remove('D-galactose')
	#sugars.remove('D-idose')
	#sugars.remove('D-tagatose')

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for sugar_name in sugars:
		print(sugar_name)
		content = makeQuestion(sugar_name)
		f.write(content+'\n')
	f.close()
