#!/usr/bin/env python3

import time
import random

import bptools
import sugarlib

def write_question(N, sugar_name, anomeric, ring_type, sugar_codes_cls, num_choices):
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
		#keto heptose
		ring='pyran'
	else:
		raise ValueError(f"Unsupported sugar code for ring selection: {sugar_code}")
	if ring != ring_type:
		raise ValueError("ring types do not match")

	sugar_struct = sugarlib.SugarStructure(sugar_code)
	#print(sugar_struct.structural_part_txt())
	haworth = sugar_struct.Haworth_projection_html(ring=ring, anomeric=anomeric)
	if haworth is None:
		return None

	question = ''
	question += 'Above is a Haworth projection of the monosaccharide &{0};-{1}. '.format(anomeric, sugar_name)
	question += 'Which one of the following Fischer projections is of the monosaccharide <b>{0}</b>? '.format(sugar_name)
	answer_code = sugar_code
	enantiomer_code = sugar_codes_cls.get_enantiomer_code_from_code(sugar_code)
	choice_codes = [answer_code, enantiomer_code,]
	if sugar_code[0] == 'A':
		first_stereocarbon = 2
	else:
		first_stereocarbon = 3

	extra_choices = []
	for i in range(first_stereocarbon, first_stereocarbon+2+1):
		wrong = sugar_codes_cls.flip_position(sugar_code, i)
		extra_choices.append(wrong)

		wrong = sugar_codes_cls.flip_position(enantiomer_code, i)
		extra_choices.append(wrong)

	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)
	while len(choice_codes) < num_choices:
		choice_codes.append(extra_choices.pop(0))
		random.shuffle(extra_choices)

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		raise ValueError("Lost some choices {0} -> {1}".format(prelen, postlen))

	full_quesiton = '<p>&{0};-{1}&xrarr;{1}</p> '.format(anomeric, sugar_name)
	full_quesiton += haworth
	full_quesiton += question

	random.shuffle(choice_codes)
	choices_list = []
	for s in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_fischer = my_sugar_struct.Fischer_projection_html()
		if s == answer_code:
			answer = my_fischer
		choices_list.append(my_fischer)
	random.shuffle(choices_list)

	bbformat = bptools.formatBB_MC_Question(N, full_quesiton, choices_list, answer)

	return bbformat

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
	time.sleep(0.5)
	return sugar_names_list


#======================================
#======================================
def write_question_batch(start_num: int, args) -> list:
	questions = []
	N = start_num
	for anomeric in ('alpha', 'beta'):
		for sugar_name in args.sugar_names_list:
			complete_question = write_question(
				N,
				sugar_name,
				anomeric,
				args.ring_type,
				args.sugar_codes_cls,
				args.num_choices
			)
			if complete_question is None:
				continue
			questions.append(complete_question)
			N += 1
	return questions

#======================================
#======================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = bptools.make_arg_parser(
		description="Generate Haworth-to-Fischer conversion questions.",
		batch=True
	)
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc'],
		required=False,
		default='mc'
	)

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

	parser.set_defaults(duplicates=1)
	args = parser.parse_args()
	return args


#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	sugar_codes_cls = sugarlib.SugarCodes()
	sugar_names_list = get_sugar_codes(args.ring_type, sugar_codes_cls)

	args.sugar_codes_cls = sugar_codes_cls
	args.sugar_names_list = sugar_names_list

	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(args.question_type.upper(),
		hint_mode,
		args.ring_type.upper(),
		f"{args.num_choices}_choices"
	)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)


#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
