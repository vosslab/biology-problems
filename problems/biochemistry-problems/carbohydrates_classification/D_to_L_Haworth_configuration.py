#!/usr/bin/env python3

import random

import bptools
import sugarlib

#======================================
SUGAR_CODES_CLS = None
SUGAR_NAMES_LIST = None
SCENARIOS = None


#======================================
def _get_ring_for_sugar_code(sugar_code: str) -> str:
	if len(sugar_code) == 5 and sugar_code[0] == 'A':
		# aldo pentose
		return 'furan'
	if len(sugar_code) == 6 and sugar_code[0] == 'M':
		# keto hexose
		return 'furan'
	if len(sugar_code) == 6 and sugar_code[0] == 'A':
		# aldo hexose
		return 'pyran'
	if len(sugar_code) == 7 and sugar_code[0] == 'M':
		# keto heptose
		return 'pyran'
	raise ValueError(f"not sure how to cyclize this sugar code {sugar_code}")


#======================================
def write_haworth_question(N, sugar_name, anomeric, sugar_codes_cls, num_choices):
	sugar_code = sugar_codes_cls.sugar_name_to_code[sugar_name]
	ring = _get_ring_for_sugar_code(sugar_code)

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
def _build_scenarios(sugar_names_list: list, sugar_codes_cls) -> list:
	scenarios: list[tuple[str, str]] = []
	for anomeric in ('alpha', 'beta'):
		for sugar_name in sorted(sugar_names_list):
			sugar_code = sugar_codes_cls.sugar_name_to_code[sugar_name]
			ring = _get_ring_for_sugar_code(sugar_code)
			sugar_struct = sugarlib.SugarStructure(sugar_code)
			haworth = sugar_struct.Haworth_projection_html(ring=ring, anomeric=anomeric)
			if haworth is None:
				continue
			scenarios.append((sugar_name, anomeric))
	return scenarios


#======================================
def write_question(N: int, args) -> str:
	if SUGAR_CODES_CLS is None or SCENARIOS is None:
		raise ValueError("Sugar globals not initialized; run main().")
	idx = (N - 1) % len(SCENARIOS)
	sugar_name, anomeric = SCENARIOS[idx]
	return write_haworth_question(
		N,
		sugar_name,
		anomeric,
		SUGAR_CODES_CLS,
		args.num_choices
	)

#======================================
#======================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = bptools.make_arg_parser(
		description="Generate D/L Haworth configuration questions.",
	)
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_scenario_args(parser)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc'],
		required=False,
		default='mc'
	)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	global SUGAR_CODES_CLS
	global SUGAR_NAMES_LIST
	global SCENARIOS
	SUGAR_CODES_CLS = sugarlib.SugarCodes()
	SUGAR_NAMES_LIST = get_sugar_codes(SUGAR_CODES_CLS)

	SCENARIOS = _build_scenarios(SUGAR_NAMES_LIST, SUGAR_CODES_CLS)
	if args.scenario_order == 'random':
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)
	print(f"Using {len(SCENARIOS)} scenarios")
	if len(SCENARIOS) == 0:
		raise ValueError("No valid Haworth scenarios were generated.")

	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(args.question_type.upper(),
		hint_mode,
		f"{args.num_choices}_choices"
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
