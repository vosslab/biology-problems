#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import pedigree_lib.html_output
import pedigree_lib.code_definitions
import pedigree_lib.code_templates

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
	bb_output_format_list = []
	question_text = "<p>Match the following pedigrees to their most likely inheritance type.</p> "
	question_text += "<p>Note: <i>each inheritance type will only be used ONCE.</i></p> "
	choices_list = ['autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked']
	N = start_num - 1
	for ad in pedigree_lib.code_templates.autosomal_dominant:
		for ar in pedigree_lib.code_templates.autosomal_recessive:			
			for xd in pedigree_lib.code_templates.x_linked_dominant:
				for xr in pedigree_lib.code_templates.x_linked_recessive:
					for yl in pedigree_lib.code_templates.y_linked:
						if max_questions is not None and N >= max_questions:
							return bb_output_format_list
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
						N += 1
						bb_output_format = bptools.formatBB_MAT_Question(N, question_text, prompts_list, choices_list)
						bb_output_format_list.append(bb_output_format)

	return bb_output_format_list

#=======================
def write_question_batch(N: int, args) -> list[str]:
	return matchingQuestionSet(N, args.max_questions)


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
