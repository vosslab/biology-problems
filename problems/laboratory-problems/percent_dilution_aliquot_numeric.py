#!/usr/bin/env python3

import random

import bptools
import lab_helper_lib

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
		raise ValueError("conc1 must be less than conc2")
	unit1 = 'microliters (&mu;L)'
	unit2 = 'milliliters (mL)'
	unit = random.choice((unit1,unit2))
	if unit == unit1:
		volume_text = lab_helper_lib.format_monospace(f"{volume} &mu;L")
	else:
		volume_text = lab_helper_lib.format_monospace(f"{volume} mL")
	stock_text = lab_helper_lib.format_stock(lab_helper_lib.format_monospace(f"{conc2}%"))
	stock_label = lab_helper_lib.format_stock('stock solution')
	target_text = lab_helper_lib.format_monospace(f"{conc1}%")
	full_name = solute_full_names.get(solute, solute)
	compound_text = solute
	if full_name != solute:
		compound_text = f"{full_name} ({solute})"
	mw = molecular_weights[solute]
	mw_text = lab_helper_lib.format_monospace(f"{mw:.2f} g/mol")
	info_rows = [
		('Final volume', volume_text),
		('Target concentration', target_text),
		('Stock concentration', stock_text),
		('Molecular weight', mw_text),
		('Aliquot unit', unit),
	]
	question = lab_helper_lib.build_info_table(info_rows, compound_text)
	question += '<p>You have an already prepared {0} of {1} {2} on the shelf.</p>'.format(
		stock_label, stock_text, solute
	)
	key_request = lab_helper_lib.format_key_request(f"{volume_text} of {target_text} {solute} solution")
	question += '<p>Prepare <strong>{0}</strong> using the {1}.</p>'.format(key_request, stock_label)
	diluent_label = lab_helper_lib.format_diluent('distilled water')
	question += "<p>What volume of aliquot in {0} do you add to {1} to make the final dilution?</p>".format(
		unit, diluent_label
	)
	return question

#==================================================
#==================================================
def df_ratio_to_values(df_ratio):
	#dfsum = df_ratio[0] + df_ratio[1]
	max_int = 100 // df_ratio[0]
	volume = df_ratio[0] * random.randint(1, max_int) * 10
	multiplier = random.choice((4,5,8,10,20,25,40,50))
	df1 = df_ratio[1]*multiplier
	df2 = df_ratio[0]*multiplier
	return volume, df1, df2

#==================================================
#==================================================
def write_question(N: int, args) -> str:
	valid_ratios = [ratio for ratio in df_ratios if ratio[1] >= 3]
	df_ratio = random.choice(valid_ratios)
	solute = random.choice(list(solute_full_names.keys()))
	volume, df1, df2 = df_ratio_to_values(df_ratio)
	q = question_text(solute, volume, df1, df2)
	aliquot = volume * df_ratio[1] / df_ratio[0]
	tolerance = 0.9
	bbf = bptools.formatBB_NUM_Question(N, q, aliquot, tolerance)
	return bbf

#==================================================
#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description='Generate percent dilution aliquot numeric questions.'
	)
	args = parser.parse_args()
	return args

#==================================================
#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#==================================================
#==================================================
if __name__ == '__main__':
	main()
