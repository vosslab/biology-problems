#!/usr/bin/env python3

import random

import bptools


df_ratios = [
	(2, 1), (3, 1), (4, 1),
	(3, 2), (5, 2), (7, 2),
	(4, 3), (5, 3), (7, 3), (8, 3),
	(5, 4), (7, 4), (9, 4),
	(6, 5), (7, 5), (8, 5), (9, 5),
]


#==================================================
#==================================================
def question_text(volume, df1, df2):
	volume_text = f"<span style='font-family: monospace;'>{volume} &mu;L</span>"
	question = (
		f"<p>Using a previous diluted sample at DF={df1}, "
		f"create a new dilution with a final dilution of DF={df2} and a total volume of {volume_text}.</p>"
		"<p>What volume of diluent in microliters (&mu;L) do you add to the aliquoted sample?</p>"
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
	volume, df1, df2 = df_ratio_to_values(df_ratio)
	q = question_text(volume, df1, df2)
	aliquot = volume * df_ratio[1] / df_ratio[0]
	diluent = volume - aliquot
	tolerance = 0.9
	bbf = bptools.formatBB_NUM_Question(N, q, diluent, tolerance)
	return bbf

#==================================================
#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description='Generate serial dilution factor diluent numeric questions.'
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
