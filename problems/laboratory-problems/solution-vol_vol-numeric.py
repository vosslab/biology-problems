#!/usr/bin/env python3

import random
import bptools
import lab_helper_lib


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
	compound_text = solute
	volume_text = lab_helper_lib.format_monospace(f"{volume} mL")
	concentration_text = lab_helper_lib.format_monospace(f"{concentration}% (v/v)")
	mw_text = lab_helper_lib.format_monospace(f"{molecular_weights[solute]:.2f} g/mol")
	info_rows = [
		('Volume', volume_text),
		('Concentration', concentration_text),
		('Molecular weight', mw_text),
		('State', 'Liquid at room temperature'),
	]
	question = lab_helper_lib.build_info_table(info_rows, compound_text)
	key_request = lab_helper_lib.format_key_request(f"{volume_text} of a {concentration_text}")
	question += f"<p>How many milliliters (mL) of {solute} you would need to make "
	question += f"<strong>{key_request}</strong> {solute} solution?</p> "
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

def write_question(N: int, args) -> str:
	solute = random.choice(liquids)
	volume, concentration, answer = get_vol_conc_answer()
	q = question_text(solute, volume, concentration)
	tolerance = 0.9
	bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
	return bbf

#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description='Generate volume/volume numeric questions.'
	)
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
