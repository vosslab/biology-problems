#!/usr/bin/env python

import os
import random
import bptools

#==================================================
#==================================================
def make_question_text(volume, df_value):
	question = ''
	question += "<p>You are preparing {0}&nbsp;mL of a new solution with a dilution factor of DF={1}.</p>".format(volume, df_value)
	question += "<p>What volume of diluent in milliliters (mL) do you add to the aliquoted sample?</p>"
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
		q = make_question_text(volume_mL, df_value)
		diluent_mL = volume_mL - aliquot_uL / 1000.
		answer = diluent_mL
		tolerance = 0.9
		bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
		f.write(bbf+'\n')
	f.close()
	bptools.print_histogram()
