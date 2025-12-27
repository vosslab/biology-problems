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
	question = "<p>Using a previous diluted sample at DF={0}, ".format(df1)
	question += "create a new dilution with a final dilution of DF={0} and a total volume of {1}&nbsp;&mu;L.</p>".format(df2, volume)
	question += "<p>What volume of aliquot in microliters (&mu;L) do you add to distilled water to make the dilution?</p>"
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
def write_question_batch(N: int, args) -> list[str]:
	questions = []
	question_num = N
	for df_ratio in df_ratios:
		if df_ratio[1] < 3:
			continue
		volume, df1, df2 = df_ratio_to_values(df_ratio)
		q = question_text(volume, df1, df2)
		aliquot = volume * df_ratio[1] / df_ratio[0]
		answer = aliquot
		tolerance = 0.9
		complete_question = bptools.formatBB_NUM_Question(question_num, q, answer, tolerance)
		questions.append(complete_question)
		question_num += 1
	return questions

#==================================================
def parse_arguments():
	duplicates_default = max(1, 99 // len(df_ratios))
	parser = bptools.make_arg_parser(
		description="Generate serial dilution aliquot questions.",
		batch=True,
		duplicates_default=duplicates_default
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
