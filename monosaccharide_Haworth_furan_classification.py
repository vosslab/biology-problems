#!/usr/bin/env python

import sys
import random
import sugarlib

N = 0

def makeQuestion(sugar_name, anomeric):
	global N
	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	ring='furan'
	sugar_struct = sugarlib.SugarStructure(sugar_code)
	#print(sugar_struct.structural_part_txt())
	haworth = sugar_struct.Haworth_projection_html(ring=ring, anomeric=anomeric)

	question = ''
	question += 'Above is a Haworth projection of a monosaccharide. '
	question += 'For each of the following categorizations, '
	question += 'check all the categorizations that apply to the sugar above. '
	question += 'You will check exactly five (5) boxes. '

	choices = [
		'tetrose (4)',
		'pentose (5)',
		'hexose (6)',
		'D-configuration',
		'L-configuration',
		'aldose',
		'ketose',
		'furanose',
		'pyranose',
		'&alpha;-anomer',
		'&beta;-anomer',
	]

	answers = {}

	if len(sugar_code) == 4:
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

	if ring.startswith('furan'):
		answers['furanose'] = True
	elif ring.startswith('pyran'):
		answers['pyranose'] = True

	if anomeric == 'alpha':
		answers['&alpha;-anomer'] = True
	elif anomeric == 'beta':
		answers['&beta;-anomer'] = True

	N += 1
	content = 'MA\t<p>Haworth classification problem &num;{0}</p> '.format(N)
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
	sugars += sugar_codes_class.get_sugar_names(4, None, 'aldo')
	sugars += sugar_codes_class.get_sugar_names(5, None, 'keto')
	#sugars += sugar_codes_class.get_sugar_names(6, None, 'aldo')
	#print(D_sugars)
	#D_sugars.remove('D-ribose')
	#D_sugars.remove('D-fructose')
	#D_sugars.remove('D-glucose')
	#D_sugars.remove('D-galactose')
	#D_sugars.remove('D-idose')
	#D_sugars.remove('D-tagatose')

	f = open('bbq-monosaccharide_Haworth_furan_classification.txt', 'w')
	for anomeric in ('alpha', 'beta'):
		for sugar_name in sugars:
			print("{0}-{1}".format(anomeric, sugar_name))
			content = makeQuestion(sugar_name, anomeric)
			f.write(content+'\n')
	f.close()
