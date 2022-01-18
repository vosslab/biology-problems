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
	question = "<p>Using a previous diluted sample at DF={0}, create a new dilution with a final dilution of DF={1}.</p>".format(df1, df2)
	question += "<p>How much liquid do you add to make a total of {0} &mu;L?</p>".format(volume)
	return question

#==================================================
#==================================================
def MC_format_for_blackboard(question, answer, choices):
	bbtext = "MC\t{0}".format(question)
	for choice in choices:
		status = "Incorrect"
		if choice == answer:
			status = "Correct"
		bbtext += "\t{0}\t{1}".format(choice, status)
	bbtext += "\n"
	return bbtext

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
def format_volumes(vol1, vol2):
	return '{0:.0f} &mu;L previously diluted sample and <span style="color: darkblue;">{1:.0f} &mu;L distilled water</span>'.format(vol1, vol2)

#==================================================
#==================================================
def get_nearest_df_ratios(orig_df_ratio):
	ratio_dict = {}
	for df_ratio in df_ratios:
		if df_ratio == orig_df_ratio:
			continue
		ratio = (df_ratio[0] * 10000) // df_ratio[1]
		ratio_dict[ratio] = df_ratio
	ratios = list(ratio_dict.keys())
	ratios.sort()
	differences = []
	orig_ratio = (orig_df_ratio[0] * 10000) // orig_df_ratio[1]
	for ratio in ratios:
		diff = abs(ratio - orig_ratio)
		differences.append(diff)
	differences.sort()
	#print(differences)
	cutoff = differences[5]
	near_df_ratios = []
	for ratio in ratios:
		diff = abs(ratio - orig_ratio)
		if diff <= cutoff:
			df_ratio = ratio_dict[ratio]
			near_df_ratios.append(df_ratio)
	return near_df_ratios

#==================================================
#==================================================
def make_choices(df_ratio, volume):
	#100 &mu;L previous diluted sample + 300 &mu;L water
	vol1 = volume * df_ratio[1] / df_ratio[0]
	vol2 = volume - vol1

	answer = format_volumes(vol1, vol2)
	wrong_choices = []
	wrong = format_volumes(vol2, vol1)
	wrong_choices.append(wrong)

	#new_ratio = (df_ratio[0])
	vol1 = volume * df_ratio[1] / df_ratio[0]
	vol2 = volume - vol1

	near_df_ratios = get_nearest_df_ratios(df_ratio)
	for wrong_df_ratio in near_df_ratios:
		wvol1 = volume * wrong_df_ratio[1] / wrong_df_ratio[0]
		if wvol1 % 1 != 0:
			continue
		wvol2 = volume - wvol1
		wrong1 = format_volumes(wvol1, wvol2)
		wrong_choices.append(wrong1)
		wrong2 = format_volumes(wvol2, wvol1)
		wrong_choices.append(wrong2)

	random.shuffle(wrong_choices)
	wrong_choices = wrong_choices[:3]

	wrong = format_volumes(vol2, vol1)
	wrong_choices.append(wrong)
	#print(wrong_choices)

	choices = wrong_choices
	choices.append(answer)
	random.shuffle(choices)

	return choices, answer

#==================================================
#==================================================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 99 // len(df_ratios)
	#duplicates = 1
	N = 1
	for i in range(duplicates):
		for df_ratio in df_ratios:
			if df_ratio[1] < 3:
				continue
			N += 1
			volume, df1, df2 = df_ratio_to_values(df_ratio)
			q = question_text(volume, df1, df2)
			choices, answer = make_choices(df_ratio, volume)
			bbf = bptools.formatBB_MC_Question(N, q, choices, answer)
			#bbf = MC_format_for_blackboard(q, answer, choices)
			f.write(bbf)
	f.close()
	bptools.print_histogram()
