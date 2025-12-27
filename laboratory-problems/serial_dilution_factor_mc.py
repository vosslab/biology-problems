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
	question = "<p>Using a previous diluted sample at DF={0}, create a new dilution with a final dilution of DF={1}.</p>".format(df1, df2)
	question += "<p>How much liquid do you add to make a total of {0} &mu;L?</p>".format(volume)
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
def format_volumes(vol1, vol2):
	choice_text = ''
	choice_text += '{0:.1f} mL previously diluted sample (aliquot) and<br/>&nbsp;&nbsp;'.format(vol1)
	choice_text += '<span style="color: darkblue;">{0:.0f} mL distilled water (diluent)</span>'.format(vol2)
	return choice_text
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

	if answer in wrong_choices:
		wrong_choices.remove(answer)
	wrong_choices = list(set(wrong_choices))
	random.shuffle(wrong_choices)
	wrong_choices = wrong_choices[:3]

	wrong = format_volumes(vol2, vol1)
	wrong_choices.append(wrong)
	wrong_choices = list(set(wrong_choices))

	choices = wrong_choices
	choices.append(answer)
	random.shuffle(choices)

	return choices, answer

#==================================================
#==================================================
def write_question_batch(start_num, args):
	question_list = []
	question_num = start_num
	for df_ratio in df_ratios:
		if df_ratio[1] < 3:
			continue
		volume, df1, df2 = df_ratio_to_values(df_ratio)
		q = question_text(volume, df1, df2)
		choices, answer = make_choices(df_ratio, volume)
		bbf = bptools.formatBB_MC_Question(question_num, q, choices, answer)
		question_list.append(bbf)
		question_num += 1
	return question_list

#==================================================
#==================================================
def parse_arguments():
	duplicates_default = 99 // len(df_ratios)
	parser = bptools.make_arg_parser(
		description='Generate serial dilution factor MC questions.',
		batch=True,
		duplicates_default=duplicates_default
	)
	args = parser.parse_args()
	return args

#==================================================
#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#==================================================
#==================================================
if __name__ == '__main__':
	main()
