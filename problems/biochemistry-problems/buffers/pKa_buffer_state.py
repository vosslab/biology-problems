#!/usr/bin/env python3

import random

import bptools
import bufferslib

#============================
#============================
#============================
def get_pH_values(pKa_list):
	min_pH_diff = 0.51
	max_pH_diff = 1.9
	all_pH_list = [
		0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
		5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0,
		10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0,
	]
	pH_list = []
	for pH in all_pH_list:
		#print(pH, pH - max(pKa_list), min(pKa_list) - pH)
		good_value = True
		for pKa in pKa_list:
			if abs(pKa-pH) < min_pH_diff:
				good_value = False
		if pH - max(pKa_list) > max_pH_diff:
			good_value = False
		elif min(pKa_list) - pH > max_pH_diff:
			good_value = False
		if good_value is True:
			pH_list.append(pH)
	return pH_list

#============================
#============================
#============================
def write_question_text(buffer_dict, pH_value):
	question_text = ''
	question_text += ('<p><strong>' + buffer_dict['acid_name'].capitalize()
		+ '</strong> and its conjugate base, ' + buffer_dict['base_name']
		+ ', ' + buffer_dict['description'] + '.</p> ')
	question_text += ('<p>' + buffer_dict['acid_name'].capitalize() + ' is ' + buffer_dict['protic_name']
		+ ' with '+bufferslib.pKa_list_to_words(buffer_dict['pKa_list'])+'.</p> ')
	num_states = len(buffer_dict['state_list'])
	question_text += ('<p>' + buffer_dict['acid_name'].capitalize() + ' has ' + bptools.number_to_cardinal(num_states)
		+' possible protonation states in the choices below.</p> ')
	question_text += ('<p>Which one of the following protonation states is the most abundant at <strong>pH '
		+ f"{pH_value:.1f}" + '</strong>?</p> ')
	return question_text


#============================
#============================
#============================
def make_complete_question(N, buffer_dict, pH_value):
	question_text = write_question_text(buffer_dict, pH_value)
	choices_list = buffer_dict['formula_list']
	if random.random() < 0.5:
		choices_list.reverse()
	answer_formula = bufferslib.get_protonation_formula(buffer_dict, pH_value)
	bbformat = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_formula)
	return bbformat


#=====================
def get_buffer_list(proton_count):
	"""
	Return the list of buffers for the requested proton count.
	"""
	if proton_count == 1:
		return list(bufferslib.monoprotic.values())
	if proton_count == 2:
		return list(bufferslib.diprotic.values())
	if proton_count == 3:
		return list(bufferslib.triprotic.values())
	if proton_count == 4:
		return list(bufferslib.tetraprotic.values())
	raise ValueError("Invalid proton_count value.")

#=====================
def write_question(N: int, args) -> str:
	"""
	Create a single buffer protonation question.
	"""
	buffer_list = get_buffer_list(args.proton_count)
	buffer_dict = bufferslib.expand_buffer_dict(random.choice(buffer_list))
	pH_list = get_pH_values(buffer_dict['pKa_list'])
	pH_value = random.choice(pH_list)
	return make_complete_question(N, buffer_dict, pH_value)

#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = bptools.make_arg_parser(
		description='Generate questions related to buffer protonation states.',
	)
	parser.add_argument('-p', '--protons', '--proton-count', dest='proton_count',
		type=int, metavar='#',
		help='Number of removable protons in a buffer (1, 2, 3, 4)',
		default=2)

	args = parser.parse_args()
	return args


#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Define output file name
	outfile = bptools.make_outfile(None, f"{args.proton_count}_protons")
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
