#!/usr/bin/env python3

import random

import bptools
import lab_helper_lib


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
	full_name = solute_full_names.get(solute, solute)
	merge_name = solute
	if full_name != solute:
		merge_name = f"{full_name.lower()} ({solute})"
	compound_text = solute
	if full_name != solute:
		compound_text = f"{full_name} ({solute})"
	volume_text = lab_helper_lib.format_monospace(f"{volume} mL")
	concentration_text = lab_helper_lib.format_monospace(f"{concentration} mM")
	mw_text = lab_helper_lib.format_monospace(f"{molecular_weights[solute]:.2f} g/mol")
	info_rows = [
		('Volume', volume_text),
		('Concentration', concentration_text),
		('Molecular weight', mw_text),
		('State', 'Solid powder at room temperature'),
	]
	question = lab_helper_lib.build_info_table(info_rows, compound_text)
	key_request = lab_helper_lib.format_key_request(f"{volume_text} of a {concentration_text}")
	question += f"<p>How many milligrams (mg) of {merge_name} would you need to make "
	question += f"<strong>{key_request}</strong> {solute} solution?</p> "
	return question

#==================================================
def get_vol_conc_answer(solute):
	valid_values = []
	valid_values += range(1, 10)
	valid_values += range(10, 900, 10)

	volume = random.choice(valid_values)
	mw = molecular_weights[solute]

	min_remainer = 1
	min_concentration_value = -1
	for concentration in valid_values:
		# mL   x   mmol / L   x  mg / mmol  x   1/ 1000
		answer = volume * concentration * mw / 1000.0
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
	concentration = min_concentration_value
	#answer should be a whole number
	# there for the numbers 2, 2, 5, 5 need to be in the numbers
	answer = volume * concentration * mw / 1000.0
	return volume, concentration, answer

#==================================================
def write_question(N, args):
	solutes = list(molecular_weights.keys())
	solute = random.choice(solutes)
	volume, concentration, answer = get_vol_conc_answer(solute)
	if concentration is None:
		return None
	question = question_text(solute, volume, concentration)
	tolerance = 0.9
	bbf = bptools.formatBB_NUM_Question(N, question, answer, tolerance)
	return bbf

#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate molar solution problems.")
	args = parser.parse_args()
	return args

#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#==================================================
if __name__ == '__main__':
	main()
