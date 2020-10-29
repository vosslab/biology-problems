#!/usr/bin/env python

import sys
import random
import sugarlib


def makeQuestion(sugar_name, anomeric):
	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	if len(sugar_code) == 5 and sugar_code[0] == 'A':
		#aldo pentose
		ring='furan'
	elif len(sugar_code) == 6 and sugar_code[0] == 'M':
		#keto hexose
		ring='furan'
	elif len(sugar_code) == 6 and sugar_code[0] == 'A':
		#aldo hexose
		ring='pyran'
	elif len(sugar_code) == 7 and sugar_code[0] == 'M':
		#keto pentose
		ring='pyran'
	else:
		print(sugar_code)
		sys.exit(1)

	sugar_struct = sugarlib.SugarStructure(sugar_code)
	#print(sugar_struct.structural_part_txt())
	haworth = sugar_struct.Haworth_projection_html(ring=ring, anomeric=anomeric)

	question = ''
	question += 'Above is a Haworth projection of the monosaccharide &{0};-{1}. '.format(anomeric, sugar_name)
	L_sugar_name = sugar_name.replace('D-', 'L-')
	question += 'Which one of the following Haworth projections is of the monosaccharide &{0};-{1}? '.format(anomeric, L_sugar_name)
	answer_code = sugar_codes_class.get_enantiomer_code_from_code(sugar_code)
	choice_codes = [(answer_code, anomeric), ]
	if anomeric == 'alpha':
		other_anomeric = 'beta'
	elif anomeric == 'beta':
		other_anomeric = 'alpha'
	choice_codes += [(answer_code, other_anomeric), ]
	if sugar_code[0] == 'A':
		first_stereocarbon = 2
	else:
		first_stereocarbon = 3
	flip_first_OH_code = sugar_codes_class.flip_position(sugar_code, first_stereocarbon)
	choice_codes.append((flip_first_OH_code, anomeric))

	flip_next_OH_code = sugar_codes_class.flip_position(sugar_code, first_stereocarbon+1)
	choice_codes.append((flip_next_OH_code, anomeric))

	enantiomer_flip_first_OH_code = sugar_codes_class.flip_position(answer_code, first_stereocarbon)
	choice_codes.append((enantiomer_flip_first_OH_code, anomeric))

	enantiomer_flip_next_OH_code = sugar_codes_class.flip_position(answer_code, first_stereocarbon+1)
	choice_codes.append((enantiomer_flip_next_OH_code, anomeric))

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		sys.exit(1)

	content = 'MC\t<p>&{0};-{1}</p> '.format(anomeric, sugar_name)
	content += haworth
	content += question

	random.shuffle(choice_codes)
	for s,a in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_haworth = my_sugar_struct.Haworth_projection_html(ring=ring, anomeric=anomeric)
		content += "\t"+my_haworth
		if s == answer_code:
			content += "\tCorrect"
		else:
			content += "\tIncorrect"
	return content

if __name__ == '__main__':
	sugar_codes_class = sugarlib.SugarCodes()
	D_sugars = []
	D_sugars += sugar_codes_class.get_sugar_names(5, 'D', 'aldo')
	#print(D_sugars)
	D_sugars += sugar_codes_class.get_sugar_names(6, 'D', 'keto')
	#print(D_sugars)
	D_sugars += sugar_codes_class.get_sugar_names(6, 'D', 'aldo')
	#print(D_sugars)
	D_sugars += sugar_codes_class.get_sugar_names(7, 'D', 'keto')
	#print(D_sugars)

	f = open('bbq-monosaccharide_Haworth_D_to_L_configuration.txt', 'w')
	for anomeric in ('alpha', 'beta'):
		for sugar_name in D_sugars:
			#random.shuffle(D_hexose_names)
			#sugar_name = D_hexose_names.pop()
			print(sugar_name)
			content = makeQuestion(sugar_name, anomeric)
			f.write(content+'\n')
	f.close()
