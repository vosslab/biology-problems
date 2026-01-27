#!/usr/bin/env python3

import random
import bptools

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

#==================================================
def question_text(solute, volume, concentration):
	full_name = solute_full_names.get(solute, None)
	if full_name is None:
		merge_name = solute
	else:
		merge_name = "{0} ({1})".format(full_name.lower(), solute)
	volume_text = f"<span style='font-family: monospace;'>{volume:.1f} mL</span>"
	concentration_text = f"<span style='font-family: monospace;'>{concentration:.1f} mg/mL</span>"
	question = "<p>How many milligrams (mg) of {0} would you need to make ".format(merge_name)
	question += "<strong>{1} of a {2}</strong> {0} solution?</p> ".format(solute, volume_text, concentration_text)
	mw = molecular_weights[solute]
	question += "<p>The molecular weight of {0} is {1:.2f} g/mol. ".format(merge_name, mw)
	question += "{0} is a solid powder at room temperature.</p> ".format(full_name)

	return question

#==================================================
def get_vol_conc_answer(solute):
	valid_values = []
	#valid_values += range(1,10)
	valid_values += range(10,900,10)

	answer = 10000
	while answer > 1000 or answer % 1 > 0:
		volume = random.choice(valid_values)/2.0
		concentration = random.choice(valid_values)/20.0
		#answer should be a whole number
		answer = volume * concentration

	return volume, concentration, answer

#==================================================
def write_question(N: int, args) -> str:
	powders = list(molecular_weights.keys())
	solute = random.choice(powders)
	volume, concentration, answer = get_vol_conc_answer(solute)
	if concentration is None:
		return None
	q = question_text(solute, volume, concentration)
	bbf = bptools.formatBB_NUM_Question(N, q, answer, 0.9)
	return bbf

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate mass solution numeric questions."
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
