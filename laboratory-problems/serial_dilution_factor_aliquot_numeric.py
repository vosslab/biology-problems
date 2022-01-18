#!/usr/bin/env python

import os
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
	print(df_ratio)
	#dfsum = df_ratio[0] + df_ratio[1]
	max_int = 100 // df_ratio[0]
	volume = df_ratio[0] * random.randint(1, max_int) * 10
	multiplier = random.choice((4,5,8,10,20,25,40,50))
	df1 = df_ratio[1]*multiplier
	df2 = df_ratio[0]*multiplier
	return volume, df1, df2

#==================================================
#==================================================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 99 // len(df_ratios)
	#duplicates = 1
	N = 0
	for i in range(duplicates):
		for df_ratio in df_ratios:
			if df_ratio[1] < 3:
				continue
			N += 1
			volume, df1, df2 = df_ratio_to_values(df_ratio)
			q = question_text(volume, df1, df2)
			aliquot = volume * df_ratio[1] / df_ratio[0]
			diluent = volume - aliquot
			answer = aliquot
			tolerance = 0.9
			bbf = bptools.formatBB_NUM_Question(N, q, answer, tolerance)
			f.write(bbf+'\n')
	f.close()
	bptools.print_histogram()
