#!/usr/bin/env python

import sys
import random
import sugarlib


def makeQuestion(sugar_name):

	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	sugar_struct = sugarlib.SugarStructure(sugar_code)
	print(sugar_struct.structural_part_txt())
	fischer = sugar_struct.Fischer_projection_html()

	question = ''
	question += 'Above is a Fischer projection of the monosaccharide D-{0}. '.format(sugar_name)
	question += 'Which one of the following Fischer projections is of the monosaccharide L-{0}? '.format(sugar_name)
	answer_code = sugar_codes_class.get_enantiomer_code_from_code(sugar_code)
	choice_codes = [answer_code, ]
	if sugar_code[0] == 'A':
		first_stereocarbon = 2
	else:
		first_stereocarbon = 3
	flip_first_OH_code = sugar_codes_class.flip_position(sugar_code, first_stereocarbon)
	choice_codes.append(flip_first_OH_code)

	flip_last_OH_code = sugar_codes_class.flip_position(sugar_code, 5)
	choice_codes.append(flip_last_OH_code)

	enantiomer_flip_first_OH_code = sugar_codes_class.flip_position(answer_code, first_stereocarbon)
	choice_codes.append(enantiomer_flip_first_OH_code)

	enantiomer_flip_last_OH_code = sugar_codes_class.flip_position(answer_code, 5)
	choice_codes.append(enantiomer_flip_last_OH_code)

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		sys.exit(1)


	content = 'MC\t<p>D-{0}</p> '.format(sugar_name)
	content += fischer
	content += question

	random.shuffle(choice_codes)
	for s in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_fischer = my_sugar_struct.Fischer_projection_html()
		content += "\t"+my_fischer
		if s == answer_code:
			content += "\tCorrect"
		else:
			content += "\tIncorrect"
	return content

if __name__ == '__main__':
	sugar_codes_class = sugarlib.SugarCodes()
	D_hexose_names = sugar_codes_class.get_D_hexoses()
	#D_hexose_names = sugar_codes_class.get_D_aldohexoses()
	f = open('bbq-monosaccharide_Fischer_D_to_L_configuration.txt', 'w')
	for sugar_name in D_hexose_names:
		#random.shuffle(D_hexose_names)
		#sugar_name = D_hexose_names.pop()
		print(sugar_name)
		content = makeQuestion(sugar_name)
		f.write(content+'\n')
	f.close()

