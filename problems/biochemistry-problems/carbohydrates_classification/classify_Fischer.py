#!/usr/bin/env python3

import bptools
import sugarlib

def write_question(N, sugar_name, sugar_codes_class):
	"""
	Creates a multiple-choice question for classifying a sugar based on its Fischer projection.
	"""
	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	sugar_struct = sugarlib.SugarStructure(sugar_code)

	# Generate Fischer projection diagram
	fischer_projection_html_str = sugar_struct.Fischer_projection_html()

	# HTML question introduction and instructions
	question = ''
	question += '<p>The diagram above shows a <strong>Fischer projection</strong> of an unnamed monosaccharide.</p>'
	question += '<p>Your task is to classify the sugar based on the provided categorizations below. '
	question += 'Carefully analyze the structure and check the <strong>three categorizations that apply</strong>.</p>'
	question += '<p><strong>Instructions:</strong></p>'
	question += '<ul>'
	question += '<li>You are required to select exactly <strong>three (3) boxes</strong>.</li>'
	question += '<li>Selecting fewer or more than three boxes will be marked as <strong>incorrect</strong>.</li>'
	question += '<li>No partial credit will be awarded.</li>'
	question += '</ul>'


	# Define answer choices
	choices_list = [
		'triose (3)',
		'tetrose (4)',
		'pentose (5)',
		'hexose (6)',
		'D-configuration',
		'L-configuration',
		'aldose',
		'ketose',
		'3-ketose',
	]

	# Determine correct answers
	answers_dict = {}

	# Classify based on sugar length
	if len(sugar_code) == 3:
		answers_dict['triose (3)'] = True
	elif len(sugar_code) == 4:
		answers_dict['tetrose (4)'] = True
	elif len(sugar_code) == 5:
		answers_dict['pentose (5)'] = True
	elif len(sugar_code) == 6:
		answers_dict['hexose (6)'] = True
	elif len(sugar_code) == 7:
		answers_dict['septose (7)'] = True

	# Assign D/L configuration
	if sugar_code[-2] == 'D':
		answers_dict['D-configuration'] = True
	elif sugar_code[-2] == 'L':
		answers_dict['L-configuration'] = True

	# Assign aldose/ketose and specific ketose classifications
	if sugar_code.startswith('MK'):
		answers_dict['ketose'] = True
	elif sugar_code.startswith('A'):
		answers_dict['aldose'] = True
	elif sugar_code.startswith('M') and sugar_code[2] == 'K':
		answers_dict['3-ketose'] = True

	# Get the list of correct answers
	answers_list = list(answers_dict.keys())

	# Apply colors to choices and answers using the shared helper function
	colored_choices_list = sugarlib.color_question_choices(choices_list)
	colored_answers_list = sugarlib.color_question_choices(answers_list)

	# Assemble the final question content
	question_content = '<p>Fischer classification problem</p>'
	question_content += fischer_projection_html_str  # Add Fischer projection diagram
	question_content += question  # Add question description and instructions

	if len(colored_answers_list) != 3:
		raise ValueError("must be exactly three answers")

	# Format the question for Blackboard
	complete_question = bptools.formatBB_MA_Question(
		N, question_content, colored_choices_list, colored_answers_list
	)

	return complete_question

def get_sugar_codes(sugar_codes_class):
	sugar_names_list = []
	sugar_names_list += sugar_codes_class.get_sugar_names(4, 'D', None)
	sugar_names_list += sugar_codes_class.get_sugar_names(4, 'L', None)
	sugar_names_list += sugar_codes_class.get_sugar_names(5, 'D', None)
	sugar_names_list += sugar_codes_class.get_sugar_names(5, 'L', None)
	sugar_names_list += sugar_codes_class.get_sugar_names(6, None, 'aldo')
	sugar_names_list += sugar_codes_class.get_sugar_names(6, None, 'keto')
	#print(sugar_names_list)
	sugar_names_list.remove('D-ribose')
	sugar_names_list.remove('D-fructose')
	sugar_names_list.remove('D-glucose')
	sugar_names_list.remove('D-galactose')
	sugar_names_list.remove('D-idose')
	#sugar_names_list.remove('D-tagatose')
	print(f"Retrieved {len(sugar_names_list)} from the sugar library")
	return sugar_names_list

#======================================
#======================================
def write_question_batch(start_num: int, args) -> list:
	questions = []
	N = start_num
	for sugar_name in args.sugar_names_list:
		complete_question = write_question(N, sugar_name, args.sugar_codes_class)
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
		description="Generate Fischer classification questions.",
		batch=True
	)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['ma'],
		required=False,
		default='ma'
	)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	sugar_codes_class = sugarlib.SugarCodes()
	sugar_names_list = get_sugar_codes(sugar_codes_class)

	args.sugar_codes_class = sugar_codes_class
	args.sugar_names_list = sugar_names_list

	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(args.question_type.upper(),
		hint_mode
	)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
