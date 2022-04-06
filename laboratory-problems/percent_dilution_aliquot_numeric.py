#!/usr/bin/env python

import os
import random
import bptools

df_ratios = [
	(2, 1), (3, 1), (4, 1),
	(3, 2), (5, 2), (7, 2),
	(4, 3), (5, 3), (7, 3), (8, 3),
	(5, 4), (7, 4), (9, 4),
	(6, 5), (7, 5), (8, 5), (9, 5),
]

solute_full_names = {
	'NaCl': 'Sodium chloride',
	'EDTA': 'Ethylenediaminetetraacetic acid',
	'KCl': 'Potassium chloride',
	'MgCl<sub>2</sub>': 'Magnesium chloride',
	'MgSO<sub>4</sub>': 'Magnesium sulfate',
	'NaHCO<sub>3</sub>': 'Sodium bicarbonate',
	'CaCO<sub>3</sub>': 'Calcium carbonate',
	'NaH<sub>2</sub>PO<sub>4</sub>': 'Monosodium phosphate',
}

molecular_weights = {
	'EDTA': 292.24,
	'NaCl': 58.44,
	'KCl': 74.55,
	'Glucose': 180.16,
	'Sucrose': 342.3,
	'Valine': 117.15,
	'Cysteine': 121.16,
	'MgSO<sub>4</sub>': 120.37,
	'MgCl<sub>2</sub>': 95.21,
	'NaHCO<sub>3</sub>': 84.01,
	'CaCO<sub>3</sub>': 100.09,
	'NaH<sub>2</sub>PO<sub>4</sub>': 119.98,
}

#==================================================
#==================================================
def question_text(solute, volume, conc1, conc2):
	#Prepare 80 mL of 2.5% sucrose solution using a 50% stock solution.
	question = ''
	if conc1 >= conc2:
		print("ERROR: conc1 >= conc2")
		sys.exit(1)
	unit1 = 'microliters (&mu;L)'
	unit2 = 'milliliters (mL)'
	unit = random.choice((unit1,unit2))
	question += '<p>You have an already prepared stock solution of {0}% {1} on the shelf.</p>'.format(conc2, solute)
	question += '<p>Prepare {0} {1} of {2}% {3} solution using the stock solution.</p>'.format(volume, unit, conc1, solute)
	full_name = solute_full_names.get(solute, solute)
	mw = molecular_weights[solute]
	question += "<p>The molecular weight of {0} ({1}) is {2:.2f} g/mol. ".format(full_name.lower(), solute, mw)
	question += "<p>What volume of aliquot in {0} do you add to distilled water to make the final dilution?</p>".format(unit)
	return question

#==================================================
#==================================================
def df_ratio_to_values(df_ratio):
	print(df_ratio)
	#dfsum = df_ratio[0] + df_ratio[1]
	max_int = 100 // df_ratio[0]
	volume = df_ratio[0] * random.randint(1, max_int) * 10
	multiplier = random.choice((4,5,8,10,20,25,40,50))
	df1 = df_ratio[1]*multiplier
	df2 = df_ratio[0]*multiplier
	return volume, df1, df2

#==================================================
#==================================================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	#duplicates = 99 // len(df_ratios) // len(solute_full_names.keys())
	duplicates = 1
	N = 0
	for d in range(duplicates):
		for solute in solute_full_names.keys():
			for df_ratio in df_ratios:
				print(N)
				if df_ratio[1] < 3:
					continue
				N += 1
				volume, df1, df2 = df_ratio_to_values(df_ratio)
				q = question_text(solute, volume, df1, df2)
				aliquot = volume * df_ratio[1] / df_ratio[0]
				diluent = volume - aliquot
				answer = aliquot
				tolerance = 0.9
				bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
				f.write(bbf)
	f.close()
	bptools.print_histogram()
