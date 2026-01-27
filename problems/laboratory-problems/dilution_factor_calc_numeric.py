#!/usr/bin/env python3

import random
import bptools
import lab_helper_lib

#==================================================
#==================================================
def make_question_text(aliquot_mL, diluent_mL):
	aliquot_text = lab_helper_lib.format_monospace(f"{aliquot_mL:.1f} mL")
	diluent_text = lab_helper_lib.format_monospace(f"{diluent_mL:.1f} mL")
	stock_text = lab_helper_lib.format_stock('stock solution')
	diluent_label = lab_helper_lib.format_diluent('distilled water')
	key_request = lab_helper_lib.format_key_request(
		f"{aliquot_text} {stock_text} into {diluent_text} {diluent_label}"
	)
	question = (
		"<p>You are preparing a new solution.</p>"
		+ "<p>You dilute {0} to make a dilution.</p>".format(key_request)
		+ "<p>What is the dilution factor?</p>"
	)
	return question

#==================================================
#==================================================
def get_random_values():
	volume_mL = 0.1
	df_value = 0.1
	while volume_mL == df_value or volume_mL % 1 != 0:
		df_value = random.randint(2, 100)
		aliquot_uL = random.randint(1, 100) * 100
		volume_mL = aliquot_uL * df_value / 1000.
	#aliquot_uL = volume_mL / df_value * 1000
	return df_value, volume_mL, aliquot_uL

#==================================================
#==================================================
def write_question(N: int, args) -> str:
	df_value, volume_mL, aliquot_uL = get_random_values()
	aliquot_mL = aliquot_uL / 1000.0
	diluent_mL = volume_mL - aliquot_mL
	question_text = make_question_text(aliquot_mL, diluent_mL)
	answer = df_value
	tolerance = 0.9
	complete_question = bptools.formatBB_NUM_Question(N, question_text, answer, tolerance)
	return complete_question

#==================================================
#==================================================
def parse_arguments():
	"""
	Parse command-line arguments.
	"""
	parser = bptools.make_arg_parser(description="Generate dilution factor numeric questions.")
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
