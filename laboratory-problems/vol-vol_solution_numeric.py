#!/usr/bin/env python3

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
	question = f"<p>How many milliliters (mL) of {solute} you would need to make "
	question += f"{volume} mL of a {concentration}% (v/v) {solute} solution?</p> "
	mw = molecular_weights[solute]
	question += f"<p>The molecular weight of {solute} is {mw:.2f} g/mol. "
	question += f"{solute.title()} is a liquid at room temperature.</p> "
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

def write_question_batch(N, args):
	question_list = []
	question_number = N
	for solute in liquids:
		volume, concentration, answer = get_vol_conc_answer()
		q = question_text(solute, volume, concentration)
		tolerance = 0.9
		bbf = bptools.formatBB_NUM_Question(question_number, q, answer, tolerance)
		question_list.append(bbf)
		question_number += 1
	return question_list

#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description='Generate volume/volume numeric questions.',
		batch=True
	)
	args = parser.parse_args()
	return args

#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#==================================================
if __name__ == '__main__':
	main()
