#!/usr/bin/env python3

import os
import random
import bptools

#==================================================
#==================================================
def make_question_text(aliquot_mL, diluent_mL):
	question = ''
	question += "<p>You are preparing a new solution.</p>"
	question += "<p>You dilute {0} mL of stock solution into {1} mL distilled water to make a dilution.</p>".format(aliquot_mL, diluent_mL)
	question += '<p>What is the dilution factor?</p>'
	return question

#==================================================
#==================================================
def get_random_values():
	volume_mL = 0.1
	df_value = 0.1
	while volume_mL == df_value or volume_mL % 1 != 0:
		df_value = random.randint(2, 100)
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
		aliquot_mL = aliquot_uL / 1000.
		diluent_mL = volume_mL - aliquot_mL
		q = make_question_text(aliquot_mL, diluent_mL)
		answer = df_value
		tolerance = 0.9
		bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
		f.write(bbf+'\n')
	f.close()
	bptools.print_histogram()
