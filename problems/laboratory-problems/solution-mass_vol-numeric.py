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
	compound_text = solute
	if full_name != solute:
		compound_text = f"{full_name} ({solute})"
	volume_text = lab_helper_lib.format_monospace(f"{volume} mL")
	concentration_text = lab_helper_lib.format_monospace(f"{concentration}% (w/v)")
	mw_text = lab_helper_lib.format_monospace(f"{molecular_weights[solute]:.2f} g/mol")
	info_rows = [
		('Volume', volume_text),
		('Concentration', concentration_text),
		('Molecular weight', mw_text),
		('State', 'Solid powder at room temperature'),
	]
	question = lab_helper_lib.build_info_table(info_rows, compound_text)
	key_request = lab_helper_lib.format_key_request(f"{volume_text} of a {concentration_text}")
	question += "<p>How many grams (g) of {0} ({1}) you would need to make ".format(full_name.lower(), solute)
	question += "<strong>{1}</strong> {0} solution?</p> ".format(solute, key_request)
	return question

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


def write_question(N: int, args) -> str:
	powders = list(molecular_weights.keys())
	solute = random.choice(powders)
	volume, concentration, answer = get_vol_conc_answer()
	if concentration is None:
		return None
	q = question_text(solute, volume, concentration)
	bbf = bptools.formatBB_NUM_Question(N, q, answer, 0.9)
	return bbf

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate weight/volume solution questions."
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
