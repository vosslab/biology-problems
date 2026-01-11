#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random
import os
import sys

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

# Add pedigree_lib to path for local imports used inside pedigree_lib modules
pedigree_lib_path = os.path.join(os.path.dirname(__file__), 'pedigree_lib')
if pedigree_lib_path not in sys.path:
	sys.path.insert(0, pedigree_lib_path)

import pedigree_lib.html_output
import pedigree_lib.code_definitions
import pedigree_lib.code_templates

AUTOSOMAL_DOMINANT: list[str] = []
AUTOSOMAL_RECESSIVE: list[str] = []
X_LINKED_DOMINANT: list[str] = []
X_LINKED_RECESSIVE: list[str] = []
Y_LINKED: list[str] = []

QUESTION_TEXT = "<p>Match the following pedigrees to their most likely inheritance type.</p> <p>Note: <i>each inheritance type will only be used ONCE.</i></p> "
CHOICES_LIST = ['autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked']

#=======================
def bbFormatMatchingQuestion(N, question_text, prompts_list, choices_list, max_choices=5):
	complete_question = question_text
	num_items = min(len(prompts_list), len(choices_list))
	indices = list(range(num_items))
	random.shuffle(indices)
	indices = indices[:max_choices]
	indices.sort()
	for i in indices:
		complete_question += '\t' + prompts_list[i] + '\t' + choices_list[i]
	crc16_value = bptools.getCrc16_FromString(complete_question)
	#MAT TAB question_text TAB answer_text TAB matching text TAB answer two text TAB matching two text
	bb_output_format = "MAT\t<p>{0:03d}. {1}</p> {2}\n".format(N, crc16_value, complete_question)
	return bb_output_format

#=======================
def matchingQuestionSet(start_num=1, max_questions=None):
	if len(AUTOSOMAL_DOMINANT) == 0:
		return []

	len_ad = len(AUTOSOMAL_DOMINANT)
	len_ar = len(AUTOSOMAL_RECESSIVE)
	len_xd = len(X_LINKED_DOMINANT)
	len_xr = len(X_LINKED_RECESSIVE)
	len_yl = len(Y_LINKED)
	total = len_ad * len_ar * len_xd * len_xr * len_yl

	remaining = None
	if max_questions is not None:
		remaining = max_questions - (start_num - 1)
		if remaining <= 0:
			return []
	batch_size = total if remaining is None else min(total, remaining)

	bb_output_format_list: list[str] = []
	for offset in range(batch_size):
		q_num = start_num + offset
		idx = (q_num - 1) % total

		# Mixed-radix decode: pick one pedigree template from each list.
		idx, i_yl = divmod(idx, len_yl)
		idx, i_xr = divmod(idx, len_xr)
		idx, i_xd = divmod(idx, len_xd)
		idx, i_ar = divmod(idx, len_ar)
		_, i_ad = divmod(idx, len_ad)

		ad = AUTOSOMAL_DOMINANT[i_ad]
		ar = AUTOSOMAL_RECESSIVE[i_ar]
		xd = X_LINKED_DOMINANT[i_xd]
		xr = X_LINKED_RECESSIVE[i_xr]
		yl = Y_LINKED[i_yl]

		if random.random() < 0.5:
			ad = pedigree_lib.code_definitions.mirror_pedigree(ad)
		adc = pedigree_lib.html_output.translateCode(ad)
		if random.random() < 0.5:
			ar = pedigree_lib.code_definitions.mirror_pedigree(ar)
		arc = pedigree_lib.html_output.translateCode(ar)
		if random.random() < 0.5:
			xd = pedigree_lib.code_definitions.mirror_pedigree(xd)
		xdc = pedigree_lib.html_output.translateCode(xd)
		if random.random() < 0.5:
			xr = pedigree_lib.code_definitions.mirror_pedigree(xr)
		xrc = pedigree_lib.html_output.translateCode(xr)
		if random.random() < 0.5:
			yl = pedigree_lib.code_definitions.mirror_pedigree(yl)
		ylc = pedigree_lib.html_output.translateCode(yl)

		prompts_list = [adc, arc, xdc, xrc, ylc]
		bb_output_format_list.append(bptools.formatBB_MAT_Question(q_num, QUESTION_TEXT, prompts_list, CHOICES_LIST))

	return bb_output_format_list

#=======================
def write_question_batch(N: int, args) -> list[str]:
	if len(AUTOSOMAL_DOMINANT) == 0:
		return []

	len_ad = len(AUTOSOMAL_DOMINANT)
	len_ar = len(AUTOSOMAL_RECESSIVE)
	len_xd = len(X_LINKED_DOMINANT)
	len_xr = len(X_LINKED_RECESSIVE)
	len_yl = len(Y_LINKED)
	total = len_ad * len_ar * len_xd * len_xr * len_yl

	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (N - 1)
		if remaining <= 0:
			return []
	batch_size = total if remaining is None else min(total, remaining)

	questions: list[str] = []
	for offset in range(batch_size):
		q_num = N + offset
		idx = (q_num - 1) % total

		# Mixed-radix decode: pick one pedigree template from each list.
		idx, i_yl = divmod(idx, len_yl)
		idx, i_xr = divmod(idx, len_xr)
		idx, i_xd = divmod(idx, len_xd)
		idx, i_ar = divmod(idx, len_ar)
		_, i_ad = divmod(idx, len_ad)

		ad = AUTOSOMAL_DOMINANT[i_ad]
		ar = AUTOSOMAL_RECESSIVE[i_ar]
		xd = X_LINKED_DOMINANT[i_xd]
		xr = X_LINKED_RECESSIVE[i_xr]
		yl = Y_LINKED[i_yl]

		if random.random() < 0.5:
			ad = pedigree_lib.code_definitions.mirror_pedigree(ad)
		adc = pedigree_lib.html_output.translateCode(ad)
		if random.random() < 0.5:
			ar = pedigree_lib.code_definitions.mirror_pedigree(ar)
		arc = pedigree_lib.html_output.translateCode(ar)
		if random.random() < 0.5:
			xd = pedigree_lib.code_definitions.mirror_pedigree(xd)
		xdc = pedigree_lib.html_output.translateCode(xd)
		if random.random() < 0.5:
			xr = pedigree_lib.code_definitions.mirror_pedigree(xr)
		xrc = pedigree_lib.html_output.translateCode(xr)
		if random.random() < 0.5:
			yl = pedigree_lib.code_definitions.mirror_pedigree(yl)
		ylc = pedigree_lib.html_output.translateCode(yl)

		prompts_list = [adc, arc, xdc, xrc, ylc]
		questions.append(bptools.formatBB_MAT_Question(q_num, QUESTION_TEXT, prompts_list, CHOICES_LIST))

	return questions


#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = bptools.make_arg_parser(description="Generate pedigree matching questions.", batch=True)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using write_question().
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	global AUTOSOMAL_DOMINANT
	global AUTOSOMAL_RECESSIVE
	global X_LINKED_DOMINANT
	global X_LINKED_RECESSIVE
	global Y_LINKED

	AUTOSOMAL_DOMINANT = list(pedigree_lib.code_templates.autosomal_dominant)
	AUTOSOMAL_RECESSIVE = list(pedigree_lib.code_templates.autosomal_recessive)
	X_LINKED_DOMINANT = list(pedigree_lib.code_templates.x_linked_dominant)
	X_LINKED_RECESSIVE = list(pedigree_lib.code_templates.x_linked_recessive)
	Y_LINKED = list(pedigree_lib.code_templates.y_linked)

	if args.scenario_order == 'sorted':
		AUTOSOMAL_DOMINANT.sort()
		AUTOSOMAL_RECESSIVE.sort()
		X_LINKED_DOMINANT.sort()
		X_LINKED_RECESSIVE.sort()
		Y_LINKED.sort()
	else:
		random.shuffle(AUTOSOMAL_DOMINANT)
		random.shuffle(AUTOSOMAL_RECESSIVE)
		random.shuffle(X_LINKED_DOMINANT)
		random.shuffle(X_LINKED_RECESSIVE)
		random.shuffle(Y_LINKED)

	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
