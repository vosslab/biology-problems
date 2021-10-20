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
	fischer = sugar_struct.Fischer_projection_html()

	question = ''
	#question += 'This is a challenging questiom, so it is <b>extra credit</b>. Don&prime;t waste too much time solving it.<br/> '
	question += 'Above is a Fischer projection of the monosaccharide {0}. '.format(sugar_name)
	question += 'Which one of the following Haworth projections is of the monosaccharide <b>&{0};-{1}</b>? '.format(anomeric, sugar_name)
	answer_code = sugar_code
	enantiomer_code = sugar_codes_class.get_enantiomer_code_from_code(sugar_code)
	choice_codes = [(answer_code, anomeric), ]
	if anomeric == 'alpha':
		other_anomeric = 'beta'
	elif anomeric == 'beta':
		other_anomeric = 'alpha'
	choice_codes.append((answer_code, other_anomeric))

	if sugar_code[0] == 'A':
		first_stereocarbon = 2
	else:
		first_stereocarbon = 3

	extra_choices = []
	extra_choices.append((enantiomer_code, other_anomeric))
	extra_choices.append((enantiomer_code, anomeric))
	for i in range(first_stereocarbon, first_stereocarbon+1+1):
		wrong = sugar_codes_class.flip_position(sugar_code, i)
		extra_choices.append((wrong, anomeric))
		extra_choices.append((wrong, other_anomeric))

		wrong = sugar_codes_class.flip_position(enantiomer_code, i)
		extra_choices.append((wrong, anomeric))
		extra_choices.append((wrong, other_anomeric))

	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)
	while len(choice_codes) < 5:
		choice_codes.append(extra_choices.pop(0))
		random.shuffle(extra_choices)

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		print("Lost some choices {0} -> {1}".format(prelen, postlen))
		sys.exit(1)

	content = 'MC\t<p>{1}&xrarr;&{0};-{1}</p> '.format(anomeric, sugar_name)
	content += fischer
	content += question

	random.shuffle(choice_codes)
	for s,a in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_haworth = my_sugar_struct.Haworth_projection_html(ring=ring, anomeric=a)
		content += "\t"+my_haworth #+'<br/>'+a+s
		if s == answer_code and a == anomeric:
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
	D_sugars.remove('D-ribose')
	D_sugars.remove('D-fructose')
	D_sugars.remove('D-glucose')
	D_sugars.remove('D-galactose')
	D_sugars.remove('D-idose')
	D_sugars.remove('D-tagatose')
	f = open('bbq-monosaccharide_Fischer_to_Haworth.txt', 'w')
	for anomeric in ('alpha', 'beta'):
		for sugar_name in D_sugars:
			#random.shuffle(D_hexose_names)
			#sugar_name = D_hexose_names.pop()
			print(sugar_name)
			content = makeQuestion(sugar_name, anomeric)
			f.write(content+'\n')
	f.close()
