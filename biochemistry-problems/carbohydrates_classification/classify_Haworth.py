#!/usr/bin/env python3

import os
import time
import argparse

import bptools
import sugarlib


def write_question(N, sugar_name, anomeric, ring_type):
	"""
	Creates a multiple-choice question for classifying a sugar based on its Haworth projection.
	Args:
		N (int): Question number.
		sugar_name (str): Name of the sugar to classify.
		anomeric (str): Anomeric configuration ('alpha' or 'beta').
	"""
	sugar_codes_class = sugarlib.SugarCodes()
	sugar_code = sugar_codes_class.sugar_name_to_code[sugar_name]
	sugar_struct = sugarlib.SugarStructure(sugar_code)

	# Generate Haworth projection diagram
	haworth_projection_html_str = sugar_struct.Haworth_projection_html(ring=ring_type, anomeric=anomeric)

	# HTML question introduction and instructions
	question = (
		'<p>The diagram above shows a <strong>Haworth projection</strong> of an unnamed monosaccharide.</p>'
		'<p>Your task is to classify the sugar based on the provided categorizations below. '
		'Carefully analyze the structure and check the <strong>five categorizations that apply</strong>.</p>'
		'<p><strong>Instructions:</strong></p>'
		'<ul>'
		'<li>You are required to select exactly <strong>five (5) boxes</strong>.</li>'
		'<li>Selecting fewer or more than five boxes will be marked as <strong>incorrect</strong>.</li>'
		'<li><strong>No partial credit</strong> will be awarded.</li>'
		'</ul>'
	)

	# Define answer choices
	choices_list = [
		'pentose (5)',
		'hexose (6)',
		'septose (7)',
		'D-configuration',
		'L-configuration',
		'aldose',
		'ketose',
		'furanose',
		'pyranose',
		'&alpha;-anomer',
		'&beta;-anomer',
	]

	# Determine correct answers
	answers_dict = {}

	# Classify based on sugar length
	if len(sugar_code) == 5:
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

	# Assign aldose/ketose classifications
	if sugar_code.startswith('MK'):
		answers_dict['ketose'] = True
	elif sugar_code.startswith('A'):
		answers_dict['aldose'] = True

	# Assign ring structure classification
	if ring_type == 'furan':
		answers_dict['furanose'] = True
	elif ring_type == 'pyran':
		answers_dict['pyranose'] = True

	# Assign anomeric configuration
	if anomeric == 'alpha':
		answers_dict['&alpha;-anomer'] = True
	elif anomeric == 'beta':
		answers_dict['&beta;-anomer'] = True

	# Get the list of correct answers
	answers_list = list(answers_dict.keys())

	# Apply colors to choices and answers using the shared helper function
	colored_choices_list = sugarlib.color_question_choices(choices_list)
	colored_answers_list = sugarlib.color_question_choices(answers_list)

	# Assemble the final question content
	question_content = '<p>Haworth classification problem</p>'
	question_content += haworth_projection_html_str  # Add Haworth projection diagram
	question_content += question  # Add question description and instructions

	# Format the question for Blackboard
	complete_question = bptools.formatBB_MA_Question(
		N, question_content, colored_choices_list, colored_answers_list
	)

	return complete_question

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
def get_sugar_codes(ring_type):
	sugar_codes_class = sugarlib.SugarCodes()
	sugar_names_list = []
	#rings need to have exactly one extra carbon off the end, so D/L can easily be determined.
	# Furanose-forming sugars (both D/L types))
	if ring_type == 'furan':
		sub_sugar_names_list = sugar_codes_class.get_sugar_names(5, "all", 'aldo')  # Aldopentoses
		print(f"Retrieved {len(sub_sugar_names_list)} Aldopentoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
		sub_sugar_names_list = sugar_codes_class.get_sugar_names(6, "all", 'keto')  # Ketohexoses
		print(f"Retrieved {len(sub_sugar_names_list)} Ketohexoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
	elif ring_type == 'pyran':
		sub_sugar_names_list = sugar_codes_class.get_sugar_names(6, "all", 'aldo')  # Aldohexoses
		print(f"Retrieved {len(sub_sugar_names_list)} Aldohexoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
		sub_sugar_names_list = sugar_codes_class.get_sugar_names(7, "all", 'keto')  # Ketoheptoses
		print(f"Retrieved {len(sub_sugar_names_list)} Ketoheptoses sugars from the sugar library.")
		sugar_names_list += sub_sugar_names_list
	# better be no duplicates
	if len(sugar_names_list) != len(list(set(sugar_names_list))):
		raise ValueError

	#sugar_names_list += sugar_codes_class.get_sugar_names(6, None, 'aldo')
	print(f"Retrieved {len(sugar_names_list)} sugars for the ring type '{ring_type}' from the sugar library.")
	time.sleep(0.5)
	return sugar_names_list

#======================================
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

	sugar_names_list = get_sugar_codes(args.ring_type)

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for anomeric in ('alpha', 'beta'):
			for sugar_name in sugar_names_list:
				complete_question = write_question(N, sugar_name, anomeric, args.ring_type)
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

