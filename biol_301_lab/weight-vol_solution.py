#!/usr/bin/env python

import math
import random

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

def question_text(solute, volume, concentration):
	full_name = solute_full_names.get(solute, solute)
	question = "<p>How many grams (g) of {0} ({1}) you would need to make ".format(full_name.lower(), solute)
	question += "<strong>{1} mL of a {2}% (w/v)</strong> {0} solution?</p> ".format(solute, volume, concentration)
	mw = molecular_weights[solute]
	question += "<p>The molecular weight of {0} ({1}) is {2:.2f} g/mol. ".format(full_name.lower(), solute, mw)
	question += "{0} is a solid powder at room temperature.</p> ".format(full_name)
	
	return question

#==================================================
def format_for_blackboard(question, answer, tolerance):
	#https://experts.missouristate.edu/plugins/servlet/mobile?contentId=63486780#content/view/63486780
	#"NUM TAB question text TAB answer TAB [optional]tolerance"
	return "NUM\t{0}\t{1:.1f}\t{2:.1f}".format(question,answer,tolerance)

def get_vol_conc_answer():
	volume = random.randint(2, 10)
	concentration = random.randint(2, 10)
	for n in (2,2,5,5):
		if concentration*n > 90 or random.random() < 0.7:
			volume *= n
		else:
			concentration *= n
	
	#answer should be a whole number
	# there for the numbers 2, 2, 5, 5 need to be in the numbers
	answer = int(volume * concentration / 100.)
	return volume, concentration, answer


if __name__ == '__main__':
	f = open('bbq-weight-vol_solution.txt', 'w')
	powders = list(molecular_weights.keys())
	duplicates = 99 // len(powders)
	#duplicates = 1
	for solute in powders:
		for i in range(duplicates):
			volume, concentration, answer = get_vol_conc_answer()
			if concentration is None:
				continue
			q = question_text(solute, volume, concentration)
			print(q)
			print(answer)
			print("")
			bbf = format_for_blackboard(q, answer, 0.9)
			f.write(bbf+'\n')
	f.close()

	print("")