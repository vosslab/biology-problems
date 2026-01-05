#!/usr/bin/env python3

import random
import bptools

#==================================================
#==================================================
def make_question_text(volume, df_value):
	volume_text = f"<span style='font-family: monospace;'>{volume:.1f} mL</span>"
	question = (
		f"<p>You are preparing {volume_text} of a new solution with a dilution factor of DF={df_value}.</p>"
		"<p>What volume of diluent in milliliters (mL) do you add to the aliquoted sample?</p>"
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
def write_question(N, args):
	df_value, volume_mL, aliquot_uL = get_random_values()
	q = make_question_text(volume_mL, df_value)
	diluent_mL = volume_mL - aliquot_uL / 1000.0
	answer = diluent_mL
	tolerance = 0.9
	bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
	return bbf

def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate dilution factor diluent questions.")
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
