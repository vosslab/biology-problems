#!/usr/bin/env python3

import os
import sys
import random
import bptools
import sugarlib

def write_question(N, sugar_name):
	sugar_codes_class = sugarlib.SugarCodes()
	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	sugar_struct = sugarlib.SugarStructure(sugar_code)
	print(sugar_struct.structural_part_txt())
	fischer = sugar_struct.Fischer_projection_html()

	question = ''
	question += 'Above is a Fischer projection of the monosaccharide {0}. '.format(sugar_name)
	L_sugar_name = sugar_name.replace('D-', 'L-')
	question += 'Which one of the following Fischer projections is of the monosaccharide {0}? '.format(L_sugar_name)
	enantiomer_code = sugar_codes_class.get_enantiomer_code_from_code(sugar_code)
	answer_code = enantiomer_code
	choice_codes = [answer_code, ]
	if sugar_code[0] == 'A':
		first_stereocarbon = 2
	else:
		first_stereocarbon = 3

	extra_choices = []
	for i in range(first_stereocarbon, 5+1):
		wrong = sugar_codes_class.flip_position(sugar_code, i)
		extra_choices.append(wrong)

		wrong = sugar_codes_class.flip_position(answer_code, i)
		extra_choices.append(wrong)

	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)
	while len(choice_codes) < 5:
		choice_codes.append(extra_choices.pop(0))
		random.shuffle(extra_choices)

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		sys.exit(1)

	sugar_names_text = f"<p>{sugar_name}&xrarr;{L_sugar_name}</p>"
	question_content = sugar_names_text + fischer + question

	html_fischer_choices_list = []
	random.shuffle(choice_codes)
	for s in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_fischer = my_sugar_struct.Fischer_projection_html()
		html_fischer_choices_list.append(my_fischer)
		if s == answer_code:
			html_fischer_answer_text = my_fischer

	# Format the question for Blackboard
	complete_question = bptools.formatBB_MC_Question(
		N, question_content, html_fischer_choices_list, html_fischer_answer_text
	)
	return complete_question

#======================================
#======================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")

	args = parser.parse_args()
	return args

#======================================
#======================================
def get_sugar_codes():
	sugar_codes_class = sugarlib.SugarCodes()
	D_hexose_names = sugar_codes_class.get_D_hexoses()
	#D_hexose_names.remove('D-ribose')
	D_hexose_names.remove('D-fructose')
	D_hexose_names.remove('D-glucose')
	D_hexose_names.remove('D-galactose')
	D_hexose_names.remove('D-idose')

	#D_hexose_names = sugar_codes_class.get_D_aldohexoses()
	print(f"Retrieved {len(D_hexose_names)} from the sugar library")
	return D_hexose_names

#======================================
#======================================
def main():

	# Define output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')

	sugar_names_list = get_sugar_codes()

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for sugar_name in sugar_names_list:
			complete_question = write_question(N, sugar_name)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram if question type is multiple choice
	bptools.print_histogram()

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END

