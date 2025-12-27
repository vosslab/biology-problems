#!/usr/bin/env python3

import random
import bptools

#==================================================
#==================================================
def make_question_text(volume_mL, df_value):
	question = ''
	question += "<p>You are preparing {0}&nbsp;mL of a new solution with a dilution factor of DF={1}.</p>".format(volume_mL, df_value)
	question += "<p>What volume of aliquot in milliliters (mL) do you add to distilled water to make the dilution?</p>"
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
	answer = aliquot_uL / 1000.0
	tolerance = 0.9
	return bptools.formatBB_NUM_Question(N, q, answer, tolerance)

def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate dilution factor aliquot questions.")
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
