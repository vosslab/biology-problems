#!/usr/bin/env python3

import os
import sys
import time
import random
import argparse

import bptools
import sugarlib

def write_question(N, sugar_name, anomeric, ring_type, sugar_codes_cls):
	sugar_code = sugar_codes_cls.sugar_name_to_code[sugar_name]
	if len(sugar_code) == 5 and sugar_code[0] == 'A':
		#aldo pentose
		ring='furan'
	elif len(sugar_code) == 6 and sugar_code[0] == 'M':
		#keto hexose
		ring='furan'
	elif len(sugar_code) == 6 and sugar_code[0] == 'A':
		#aldo hexose
		ring='pyran'
	elif len(sugar_code) == 7 and sugar_code[0] == 'M':
		#keto pentose
		ring='pyran'
	else:
		print(sugar_code)
		sys.exit(1)
	if ring != ring_type:
		raise ValueError("ring types do not match")

	sugar_struct = sugarlib.SugarStructure(sugar_code)
	#print(sugar_struct.structural_part_txt())
	fischer = sugar_struct.Fischer_projection_html()

	question = ''
	#question += 'This is a challenging questiom, so it is <b>extra credit</b>. Don&prime;t waste too much time solving it.<br/> '
	question += 'Above is a Fischer projection of the monosaccharide {0}. '.format(sugar_name)
	question += 'Which one of the following Haworth projections is of the monosaccharide <b>&{0};-{1}</b>? '.format(anomeric, sugar_name)
	answer_code = sugar_code
	enantiomer_code = sugar_codes_cls.get_enantiomer_code_from_code(sugar_code)
	choice_codes = [(answer_code, anomeric), ]
	if anomeric == 'alpha':
		other_anomeric = 'beta'
	elif anomeric == 'beta':
		other_anomeric = 'alpha'
	choice_codes.append((answer_code, other_anomeric))

	if sugar_code[0] == 'A':
		first_stereocarbon = 2
	else:
		first_stereocarbon = 3

	extra_choices = []
	extra_choices.append((enantiomer_code, other_anomeric))
	extra_choices.append((enantiomer_code, anomeric))
	for i in range(first_stereocarbon, first_stereocarbon+1+1):
		wrong = sugar_codes_cls.flip_position(sugar_code, i)
		extra_choices.append((wrong, anomeric))
		extra_choices.append((wrong, other_anomeric))

		wrong = sugar_codes_cls.flip_position(enantiomer_code, i)
		extra_choices.append((wrong, anomeric))
		extra_choices.append((wrong, other_anomeric))

	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)
	while len(choice_codes) < 5:
		choice_codes.append(extra_choices.pop(0))
		random.shuffle(extra_choices)

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		print("Lost some choices {0} -> {1}".format(prelen, postlen))
		sys.exit(1)

	full_quesiton = '<p>{1}&xrarr;&{0};-{1}</p> '.format(anomeric, sugar_name)
	full_quesiton += fischer
	full_quesiton += question

	choices_list = []
	for s,a in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_haworth = my_sugar_struct.Haworth_projection_html(ring=ring, anomeric=a)
		if s == answer_code and a == anomeric:
			answer = my_haworth
		choices_list.append(my_haworth)
	random.shuffle(choices_list)

	bbformat = bptools.formatBB_MC_Question(N, full_quesiton, choices_list, answer)

	return bbformat

#======================================
#======================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")

	# Create a mutually exclusive group for question type and make it required
	ring_group = parser.add_mutually_exclusive_group(required=True)
	ring_group.add_argument(
		'-t', '--type', dest='ring_type', type=str, choices=('pyran', 'furan'),
		help='Set the ring type: pyran (pyranose) or furan (furanose)'
	)
	ring_group.add_argument(
		'-p', '--pyran', '--pyranose', dest='ring_type', action='store_const', const='pyran',
		help='Set ring type to pyran (pyranose)'
	)
	ring_group.add_argument(
		'-f', '--furan', '--furanose', dest='ring_type', action='store_const', const='furan',
		help='Set ring type to furan (furanose)'
	)

	args = parser.parse_args()
	return args

#======================================
#======================================
def get_sugar_codes(ring_type, sugar_codes_cls):
	sugar_names_list = []
	#rings need to have exactly one extra carbon off the end, so D/L can easily be determined.
	# Furanose-forming sugars (both D/L types))
	if ring_type == 'furan':
		sub_sugar_names_list = sugar_codes_cls.get_sugar_names(5, "all", 'aldo')  # Aldopentoses
		print(f"Retrieved {len(sub_sugar_names_list)} Aldopentoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
		sub_sugar_names_list = sugar_codes_cls.get_sugar_names(6, "all", 'keto')  # Ketohexoses
		print(f"Retrieved {len(sub_sugar_names_list)} Ketohexoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
	elif ring_type == 'pyran':
		sub_sugar_names_list = sugar_codes_cls.get_sugar_names(6, "all", 'aldo')  # Aldohexoses
		print(f"Retrieved {len(sub_sugar_names_list)} Aldohexoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
		sub_sugar_names_list = sugar_codes_cls.get_sugar_names(7, "all", 'keto')  # Ketoheptoses
		print(f"Retrieved {len(sub_sugar_names_list)} Ketoheptoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
	# better be no duplicates
	if len(sugar_names_list) != len(list(set(sugar_names_list))):
		raise ValueError

	#sugar_names_list += sugar_codes_cls.get_sugar_names(6, None, 'aldo')
	print(f"Retrieved {len(sugar_names_list)} sugars for the ring type '{ring_type}' from the sugar library.")
	time.sleep(2)
	return sugar_names_list


#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()

	# Define output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'
		f'-{args.ring_type.upper()}'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')

	sugar_codes_cls = sugarlib.SugarCodes()
	sugar_names_list = get_sugar_codes(args.ring_type, sugar_codes_cls)

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for anomeric in ('alpha', 'beta'):
			for sugar_name in sugar_names_list:
				#content = makeQuestion(N, sugar_name, anomeric)
				complete_question = write_question(N, sugar_name, anomeric, args.ring_type, sugar_codes_cls)
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
