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
	'glucose': 180.16,
	'sucrose': 342.3,
	'valine': 117.15,
	'cysteine': 121.16,
	'MgSO<sub>4</sub>': 120.37,
	'MgCl<sub>2</sub>': 95.21,
	'NaHCO<sub>3</sub>': 84.01,
	'CaCO<sub>3</sub>': 100.09,
	'NaH<sub>2</sub>PO<sub>4</sub>': 119.98,
}

def question_text(solute, volume, concentration):
	full_name = solute_full_names.get(solute, None)
	if full_name is None:
		merge_name = solute
	else:
		merge_name = "{0} ({1})".format(full_name.lower(), solute)
	question = "<p>How many milligrams (mg) of {0} would you need to make ".format(merge_name)
	question += "<strong>{1} mL of a {2} mM</strong> {0} solution?</p> ".format(solute, volume, concentration)
	mw = molecular_weights[solute]
	question += "<p>The molecular weight of is {1:.2f} g/mol. ".format(merge_name, mw)
	question += "{0} is a solid powder at room temperature.</p> ".format(full_name)
	
	return question

#==================================================
def format_for_blackboard(question, answer, tolerance):
	#https://experts.missouristate.edu/plugins/servlet/mobile?contentId=63486780#content/view/63486780
	#"NUM TAB question text TAB answer TAB [optional]tolerance"
	return "NUM\t{0}\t{1:.3f}\t{2:.2f}".format(question,answer,tolerance)

def get_vol_conc_answer(solute):
	valid_values = []
	valid_values += range(1,10)
	valid_values += range(10,900,10)

	volume = random.choice(valid_values)
	#concentration = random.randint(2, 10)
	mw = molecular_weights[solute]
	
	min_remainer = 1
	min_concentration_value = -1
	for concentration in valid_values:
		answer = volume * concentration / 100. / mw * 1000
		if answer < 10:
			continue
		if answer > 980:
			break
		remainer = answer % 1
		if remainer < min_remainer:
			min_remainer = remainer
			min_concentration_value = concentration
	if min_remainer > 0.1:
		return None, None, None
	else:
		concentration = min_concentration_value

	
	#answer should be a whole number
	# there for the numbers 2, 2, 5, 5 need to be in the numbers
	answer = volume * concentration / 100. / mw * 1000
	return volume, concentration, answer

if __name__ == '__main__':
	f = open('bbq-mw_solution.txt', 'w')
	powders = list(molecular_weights.keys())
	duplicates = 99 // len(powders) + 1
	#duplicates = 1
	for solute in powders:
		for i in range(duplicates):
			volume, concentration, answer = get_vol_conc_answer(solute)
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