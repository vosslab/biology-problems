#!/usr/bin/env python

import math
import random

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
def NUM_format_for_blackboard(question, answer, tolerance):
	#https://experts.missouristate.edu/plugins/servlet/mobile?contentId=63486780#content/view/63486780
	#"NUM TAB question text TAB answer TAB [optional]tolerance"
	return "NUM\t{0}\t{1:.1f}\t{2:.1f}".format(question,answer,tolerance)

#==================================================
#==================================================
def df_ratio_to_values(df_ratio):
	print(df_ratio)
	dfsum = df_ratio[0] + df_ratio[1]
	max_int = 100 // df_ratio[0]
	volume = df_ratio[0] * random.randint(1, max_int) * 10
	multiplier = random.choice((4,5,8,10,20,25,40,50))
	df1 = df_ratio[1]*multiplier
	df2 = df_ratio[0]*multiplier
	return volume, df1, df2

#==================================================
#==================================================
if __name__ == '__main__':
	f = open('bbq-dilution_factor_aliquot.txt', 'w')
	duplicates = 99 // len(df_ratios)
	#duplicates = 1
	for i in range(duplicates):
		for df_ratio in df_ratios:
			if df_ratio[1] < 3:
				continue
			volume, df1, df2 = df_ratio_to_values(df_ratio)
			q = question_text(volume, df1, df2)
			print(q)
			aliquot = volume * df_ratio[1] / df_ratio[0]
			diluent = volume - aliquot
			answer = aliquot
			tolerance = 0.9
			bbf = NUM_format_for_blackboard(q, answer, tolerance)
			f.write(bbf+'\n')
	f.close()

	print("")