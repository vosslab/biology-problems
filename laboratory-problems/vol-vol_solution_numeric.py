#!/usr/bin/env python3

import os
import random
import bptools


#https://en.wikipedia.org/wiki/List_of_water-miscible_solvents
liquids = ['ethanol', 'hydrogen peroxide', 'acetone', 'glycerol',
					 'isopropyl alcohol', 'acetic acid', 'formic acid',]

molecular_weights = {
	'ethanol': 46.07,
	'hydrogen peroxide': 34.01,
	'acetone': 58.08,
	'glycerol': 92.09,
	'isopropyl alcohol': 60.1,
	'acetic acid': 60.05,
	'formic acid': 46.03,
}

def question_text(solute, volume, concentration):
	question = "<p>How many milliliters (mL) of {0} you would need to make ".format(solute)
	question += "{1} mL of a {2}% (v/v) {0} solution?</p> ".format(solute, volume, concentration)
	mw = molecular_weights[solute]
	question += "<p>The molecular weight of {0} is {1:.2f} g/mol. ".format(solute, mw)
	question += "{0} is a liquid at room temperature.</p> ".format(solute.title())
	return question

#==================================================
def get_vol_conc_answer():
	volume = random.randint(2, 10)
	concentration = random.randint(2, 10)
	for n in (2,2,5,5):
		if concentration*n > 90 or random.random() < 0.5:
			volume *= n
		else:
			concentration *= n

	#answer should be a whole number
	# there for the numbers 2, 2, 5, 5 need to be in the numbers
	answer = int(volume * concentration / 100.)
	return volume, concentration, answer

if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for solute in liquids:
		for i in range(13):
			N += 1
			volume, concentration, answer = get_vol_conc_answer()
			q = question_text(solute, volume, concentration)
			tolerance = 0.9
			bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
			f.write(bbf)
	f.close()
	bptools.print_histogram()
