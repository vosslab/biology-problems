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

SCENARIOS: list[tuple[str, str]] = []

#=======================
def write_question(N: int, code_string: str, answer: str) -> str:
	choices_list = [
		'autosomal dominant',
		'autosomal recessive',
		'x-linked dominant',
		'x-linked recessive',
		'y-linked',
	]
	question_text = (
		"<p>Examine the pedigree above. "
		"Which one of the following patterns of inheritance is most likely demonstrated "
		"in the above pedigree inheritance?</p> "
	)

	if random.random() < 0.5:
		code_string = pedigree_lib.code_definitions.mirror_pedigree(code_string)
	html_code = pedigree_lib.html_output.translateCode(code_string)
	return bptools.formatBB_MC_Question(N, html_code + question_text, choices_list, answer)


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
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser(description="Generate questions.", batch=True)
	parser = bptools.add_scenario_args(parser)


	# Parse the provided command-line arguments and return them
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

	global SCENARIOS
	SCENARIOS = []
	for code_string in pedigree_lib.code_templates.autosomal_dominant:
		SCENARIOS.append((code_string, 'autosomal dominant'))
	for code_string in pedigree_lib.code_templates.autosomal_recessive:
		SCENARIOS.append((code_string, 'autosomal recessive'))
	for code_string in pedigree_lib.code_templates.x_linked_dominant:
		SCENARIOS.append((code_string, 'x-linked dominant'))
	for code_string in pedigree_lib.code_templates.x_linked_recessive:
		SCENARIOS.append((code_string, 'x-linked recessive'))
	for code_string in pedigree_lib.code_templates.y_linked:
		SCENARIOS.append((code_string, 'y-linked'))

	if args.scenario_order == 'sorted':
		SCENARIOS.sort(key=lambda x: (x[1], x[0]))
	else:
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)

	outfile = bptools.make_outfile()
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#===========================================================
def write_question_batch(start_num: int, args) -> list:
	if len(SCENARIOS) == 0:
		return []

	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return []

	batch_size = len(SCENARIOS) if remaining is None else min(len(SCENARIOS), remaining)
	questions = []
	for offset in range(batch_size):
		N = start_num + offset
		idx = (N - 1) % len(SCENARIOS)
		code_string, answer = SCENARIOS[idx]
		questions.append(write_question(N, code_string, answer))
	return questions

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
