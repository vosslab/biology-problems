#!/usr/bin/env python3

import random
import bptools
import lab_helper_lib

#==================================================
#==================================================
def make_question_text(volume, df_value):
	df_text = lab_helper_lib.format_df(lab_helper_lib.format_monospace(f"DF={df_value}"))
	df_request = lab_helper_lib.format_key_request(df_text)
	volume_text = lab_helper_lib.format_monospace(f"{volume:.1f} mL")
	volume_request = lab_helper_lib.format_key_request(volume_text)
	question = (
		"<p>Dilution factors are used in biology labs to make solutions at precise "
		"concentrations, ensure consistency across experiments, and preserve valuable "
		"samples while still meeting volume requirements. For example, if a student "
		"needs 400 mL of a working solution, it is much easier to measure a small "
		"aliquot from a concentrated stock and add water to reach the final volume "
		"than to prepare the solution from scratch each time.</p>"
		f"<p>You are preparing a new solution with a dilution factor of {df_request}.</p>"
		f"<p>How much liquid do you add to make a total of {volume_request}?</p>"
	)
	return question

#==================================================
#==================================================
def format_volumes(vol1, vol2):
	aliquot_amount = lab_helper_lib.format_monospace(f"{vol1:.1f} mL")
	diluent_amount = lab_helper_lib.format_monospace(f"{vol2:.1f} mL")
	aliquot_text = lab_helper_lib.format_aliquot(f"{aliquot_amount} stock solution (aliquot)")
	diluent_text = lab_helper_lib.format_diluent(f"{diluent_amount} distilled water (diluent)")
	choice_text = (
		f"{aliquot_text}<br/>&nbsp;&nbsp;{diluent_text}"
	)
	return choice_text

#==================================================
#==================================================
def make_choices(df_value, volume, num_choices):
	# Compute the correct aliquot/diluent volumes (mL).
	aliquot_mL = volume / df_value
	diluent_mL = volume - aliquot_mL

	if aliquot_mL == diluent_mL:
		return None

	# Format the correct answer string.
	answer_text = format_volumes(aliquot_mL, diluent_mL)
	# The most tempting distractor is swapping aliquot and diluent.
	swapped_text = format_volumes(diluent_mL, aliquot_mL)

	wrong_choice_texts = []

	# Common mix-ups: swapping or using total where aliquot/diluent should be.
	wrong_choice_texts.append(format_volumes(diluent_mL, volume))
	wrong_choice_texts.append(format_volumes(volume, diluent_mL))
	wrong_choice_texts.append(format_volumes(aliquot_mL, volume))
	wrong_choice_texts.append(format_volumes(volume, aliquot_mL))

	# Another plausible mistake: using double the aliquot.
	double_aliquot_mL = volume / df_value * 2
	double_diluent_mL = volume - double_aliquot_mL
	wrong_choice_texts.append(format_volumes(double_aliquot_mL, double_diluent_mL))
	wrong_choice_texts.append(format_volumes(double_diluent_mL, double_aliquot_mL))

	# Remove any accidental duplicates of the correct answer or the best distractor.
	if answer_text in wrong_choice_texts:
		wrong_choice_texts.remove(answer_text)
	if swapped_text in wrong_choice_texts:
		wrong_choice_texts.remove(swapped_text)
	wrong_choice_texts = list(set(wrong_choice_texts))

	# Keep enough wrong choices to leave room for the correct answer and swapped distractor.
	# Target size is (num_choices - 2) from this pool; the correct answer and swapped
	# distractor are always included.
	target_wrong = max(1, num_choices - 2)
	random.shuffle(wrong_choice_texts)
	choices_list = wrong_choice_texts[:target_wrong]

	# Assemble and shuffle final choices.
	choices_list.append(answer_text)
	# Add the swapped text last; it is the best distractor and should always be included.
	choices_list.append(swapped_text)
	choices_list = list(set(choices_list))
	random.shuffle(choices_list)

	return choices_list, answer_text

#==================================================
#==================================================
def get_random_values():
	volume_mL = 0.1
	df_value = 0.1
	while volume_mL == df_value or volume_mL % 1 != 0:
		df_value = random.randint(3, 100)
		aliquot_uL = random.randint(1, 100) * 100
		volume_mL = aliquot_uL * df_value / 1000.
	#aliquot_uL = volume_mL / df_value * 1000
	return df_value, volume_mL, aliquot_uL

#==================================================
#==================================================
def write_question(N, args):
	df_value, volume_mL, aliquot_uL = get_random_values()
	q = make_question_text(volume_mL, df_value)
	choices, answer_text = make_choices(df_value, volume_mL, args.num_choices)
	if answer_text not in choices:
		return None
	bbf = bptools.formatBB_MC_Question(N, q, choices, answer_text)
	return bbf

#==================================================
#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate dilution factor MC questions.")
	parser = bptools.add_choice_args(parser, default=5)
	args = parser.parse_args()
	return args

#==================================================
#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
