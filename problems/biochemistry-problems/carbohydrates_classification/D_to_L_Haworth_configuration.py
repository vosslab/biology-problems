#!/usr/bin/env python3

import random

import bptools
import sugarlib

def write_question(N, sugar_name, anomeric, sugar_codes_cls, num_choices):
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
		raise ValueError(f"not sure how to cyclize this sugar code {sugar_code}")

	sugar_struct = sugarlib.SugarStructure(sugar_code)

	haworth = sugar_struct.Haworth_projection_html(ring=ring, anomeric=anomeric)
	if haworth is None:
		return None

	question_text = ''
	question_text += '<p>Above is a Haworth projection of the monosaccharide &{0};-{1}. '.format(anomeric, sugar_name)
	L_sugar_name = sugar_name.replace('D-', 'L-')
	question_text += 'Which one of the following Haworth projections is of the monosaccharide &{0};-{1}?</p> '.format(anomeric, L_sugar_name)
	enantiomer_code = sugar_codes_cls.get_enantiomer_code_from_code(sugar_code)
	answer_code = enantiomer_code

	choice_codes = [(answer_code, anomeric), ]
	if anomeric == 'alpha':
		other_anomeric = 'beta'
	elif anomeric == 'beta':
		other_anomeric = 'alpha'
	choice_codes += [(answer_code, other_anomeric), ]

	extra_choices = []
	for position in range(2, len(sugar_code)):
		if sugar_code[position-1] == "K":
			continue
		wrong = sugar_codes_cls.flip_position(sugar_code, position)
		extra_choices.append((wrong, anomeric))
		extra_choices.append((wrong, other_anomeric))

		wrong = sugar_codes_cls.flip_position(enantiomer_code, position)
		extra_choices.append((wrong, anomeric))
		extra_choices.append((wrong, other_anomeric))

	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)
	while len(choice_codes) < num_choices:
		choice_codes.append(extra_choices.pop(0))
		random.shuffle(extra_choices)

	prelen = len(choice_codes)
	choice_codes = list(set(choice_codes))
	postlen = len(choice_codes)
	if prelen != postlen:
		raise ValueError(f"Lost some choices {prelen} -> {postlen}")

	# Build full HTML content for the question
	sugar_name_line = f"<p>&{anomeric};-{sugar_name}</p>"
	full_question_content = sugar_name_line + haworth + question_text

	html_choices_list = []
	random.shuffle(choice_codes)
	for s, a in choice_codes:
		my_sugar_struct = sugarlib.SugarStructure(s)
		my_haworth = my_sugar_struct.Haworth_projection_html(ring=ring, anomeric=a)
		if my_haworth is None:
			return None
		html_choices_list.append(my_haworth)
		if s == answer_code:
			html_answer_text = my_haworth

	# Format the question for Blackboard
	complete_question = bptools.formatBB_MC_Question(
		N, full_question_content, html_choices_list, html_answer_text
	)
	return complete_question


def get_sugar_codes(sugar_codes_cls):
	sugar_names_list = []
	sugar_names_list += sugar_codes_cls.get_sugar_names(5, 'D', 'aldo')
	sugar_names_list += sugar_codes_cls.get_sugar_names(6, 'D', 'keto')
	sugar_names_list += sugar_codes_cls.get_sugar_names(6, 'D', 'aldo')
	sugar_names_list += sugar_codes_cls.get_sugar_names(7, 'D', 'keto')
	sugar_names_list.remove('D-fructose')
	sugar_names_list.remove('D-glucose')
	sugar_names_list = list(set(sugar_names_list))
	print(f"Retrieved {len(sugar_names_list)} from the sugar library")
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
		description="Generate D/L Haworth configuration questions.",
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
	parser.set_defaults(duplicates=1)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	sugar_codes_cls = sugarlib.SugarCodes()
	sugar_names_list = get_sugar_codes(sugar_codes_cls)

	args.sugar_codes_cls = sugar_codes_cls
	args.sugar_names_list = sugar_names_list

	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(
		None,
		args.question_type.upper(),
		hint_mode,
		f"{args.num_choices}_choices"
	)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
