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
	question = "<p>How many milligrams (mg) of {0} would you need to make ".format(merge_name)
	question += "<strong>{1} mL of a {2} mg/mL</strong> {0} solution?</p> ".format(solute, volume, concentration)
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
def write_question_batch(start_num: int, args) -> list:
	powders = list(molecular_weights.keys())
	questions = []
	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return questions
	N = start_num
	for solute in powders:
		volume, concentration, answer = get_vol_conc_answer(solute)
		if concentration is None:
			continue
		q = question_text(solute, volume, concentration)
		bbf = bptools.formatBB_NUM_Question(N, q, answer, 0.9)
		questions.append(bbf)
		N += 1
		if remaining is not None and len(questions) >= remaining:
			return questions
	return questions

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate mass solution numeric questions.",
		batch=True
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

if __name__ == '__main__':
	main()
