#!/usr/bin/env python

import os
import random
import bptools

#==================================================
#==================================================
def make_question_text(volume, df_value):
	question = ''
	question += "<p>You are preparing a new solution with a dilution factor of DF={0}.</p>".format(df_value)
	question += "<p>How much liquid do you add to make a total of {0:.1f} mL?</p>".format(volume)
	return question

#==================================================
#==================================================
def format_volumes(vol1, vol2):
	choice_text = ''
	choice_text += '{0:.1f} mL stock solution (aliquot) and<br/>&nbsp;&nbsp;'.format(vol1)
	choice_text += '<span style="color: darkblue;">{0:.1f} mL distilled water (diluent)</span>'.format(vol2)
	return choice_text

#==================================================
#==================================================
def make_choices(df_value, volume):
	#100 &mu;L previous diluted sample + 300 &mu;L water
	vol1 = volume / df_value
	vol2 = volume - vol1

	answer = format_volumes(vol1, vol2)
	wrong_choices = []

	wrong = format_volumes(vol2, volume)
	wrong_choices.append(wrong)
	wrong = format_volumes(volume, vol2)
	wrong_choices.append(wrong)
	wrong = format_volumes(vol1, volume)
	wrong_choices.append(wrong)
	wrong = format_volumes(volume, vol1)
	wrong_choices.append(wrong)

	vol1a = volume / df_value * 2
	vol2a = volume - vol1a
	wrong = format_volumes(vol1a, vol2a)
	wrong_choices.append(wrong)
	wrong = format_volumes(vol2a, vol1a)
	wrong_choices.append(wrong)

	if answer in wrong_choices:
		wrong_choices.remove(answer)
	wrong_choices = list(set(wrong_choices))
	random.shuffle(wrong_choices)
	wrong_choices = wrong_choices[:3]
	wrong = format_volumes(vol2, vol1)
	wrong_choices.append(wrong)
	wrong_choices = list(set(wrong_choices))

	choices = wrong_choices
	choices.append(answer)
	random.shuffle(choices)

	return choices, answer

#==================================================
#==================================================
def get_random_values():
	volume_mL = 0.1
	df_value = 0.1
	while volume_mL == df_value or volume_mL % 1 != 0:
		df_value = random.randint(3, 100)
		aliquot_uL = random.randint(1, 100) * 100
		volume_mL = aliquot_uL * df_value / 1000.
	#aliquot_uL = volume_mL / df_value * 1000
	return df_value, volume_mL, aliquot_uL

#==================================================
#==================================================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 99
	N = 0
	for i in range(duplicates):
		N += 1
		df_value, volume_mL, aliquot_uL = get_random_values()
		q = make_question_text(volume_mL, df_value)
		diluent_mL = volume_mL - aliquot_uL / 1000.
		answer = diluent_mL
		choices, answer_text = make_choices(df_value, volume_mL)
		bbf = bptools.formatBB_MC_Question(N, q, choices, answer_text)
		f.write(bbf)
	f.close()
	bptools.print_histogram()
