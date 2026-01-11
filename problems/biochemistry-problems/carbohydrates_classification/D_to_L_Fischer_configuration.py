#!/usr/bin/env python3

import random

import bptools
import sugarlib

def write_question(N, d_sugar_name, sugar_codes_cls, num_choices):
	d_sugar_code = sugar_codes_cls.sugar_name_to_code[d_sugar_name]
	d_sugar_structure = sugarlib.SugarStructure(d_sugar_code)
	fischer_html = d_sugar_structure.Fischer_projection_html()

	# Build the question prompt
	L_sugar_name = d_sugar_name.replace('D-', 'L-')
	question_text = ''
	question_text += f'<p>Above is a Fischer projection of the monosaccharide {d_sugar_name}. '
	question_text += f'Which one of the following Fischer projections is of the monosaccharide {L_sugar_name}?</p> '

	# Get correct answer
	L_sugar_code = sugar_codes_cls.get_enantiomer_code_from_code(d_sugar_code)
	correct_answer_code = L_sugar_code
	if len(d_sugar_code) != len(L_sugar_code):
		raise ValueError("L and D sugars are different lengths")

	# Generate choice pool
	choice_codes = [correct_answer_code]

	all_distractor_codes = []
	for position in range(2, len(d_sugar_code)):
		if d_sugar_code[position-1] == "K":
			#print("skipping")
			continue
		flipped_d_code = sugar_codes_cls.flip_position(d_sugar_code, position)
		#print(f"position = {position}; orig={d_sugar_code}; flipped={flipped_d_code}")
		all_distractor_codes.append(flipped_d_code)

		flipped_l_code = sugar_codes_cls.flip_position(L_sugar_code, position)
		#print(f"position = {position}; orig={L_sugar_code}; flipped={flipped_l_code}")
		all_distractor_codes.append(flipped_l_code)
		#print(all_distractor_codes)

	all_distractor_codes = list(set(all_distractor_codes))
	random.shuffle(all_distractor_codes)

	while len(choice_codes) < num_choices:
		choice_codes.append(all_distractor_codes.pop(0))
		random.shuffle(all_distractor_codes)

	# Sanity check: no duplicates in choices
	pre_dedup_count = len(choice_codes)
	choice_codes = list(set(choice_codes))
	post_dedup_count = len(choice_codes)
	if pre_dedup_count != post_dedup_count:
		raise ValueError("duplicate choice added...")

	# Build full HTML content for the question
	sugar_name_line = f"<p>{d_sugar_name}&xrarr;{L_sugar_name}</p>"
	full_question_content = sugar_name_line + fischer_html + question_text

	# Shuffle and render HTML Fischer projections for choices
	html_fischer_choices = []
	random.shuffle(choice_codes)
	for code in choice_codes:
		struct = sugarlib.SugarStructure(code)
		struct_html = struct.Fischer_projection_html()
		html_fischer_choices.append(struct_html)
		if code == correct_answer_code:
			correct_html_answer = struct_html

	# Format the question for Blackboard
	complete_question = bptools.formatBB_MC_Question(
		N, full_question_content, html_fischer_choices, correct_html_answer
	)
	return complete_question

def write_question2(N, sugar_name):
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
	for i in range(first_stereocarbon, len(sugar_code)):
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
		raise ValueError("duplicate choice added...")

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

def get_sugar_codes(sugar_codes_cls):
	sugar_names_list = []
	sugar_names_list += sugar_codes_cls.get_sugar_names(5, configuration='D', types='aldo')
	sugar_names_list += sugar_codes_cls.get_sugar_names(6, configuration='D')
	sugar_names_list += sugar_codes_cls.get_sugar_names(7, configuration='D')
	sugar_names_list = list(set(sugar_names_list))

	#sugar_names_list.remove('D-ribose')
	sugar_names_list.remove('D-fructose')
	sugar_names_list.remove('D-glucose')
	sugar_names_list.remove('D-galactose')
	sugar_names_list.remove('D-idose')
	print(f"Retrieved {len(sugar_names_list)} from the sugar library")
	return sugar_names_list

#======================================
#======================================
def write_question_batch(start_num: int, args) -> list:
	questions = []
	N = start_num
	for sugar_name in args.sugar_names_list:
		complete_question = write_question(N, sugar_name, args.sugar_codes_cls, args.num_choices)
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
		description="Generate D/L Fischer configuration questions.",
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
	outfile = bptools.make_outfile(args.question_type.upper(),
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
