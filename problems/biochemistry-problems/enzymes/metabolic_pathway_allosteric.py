#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools
import metaboliclib

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""Create an MC question about which enzyme is most likely allosteric.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted MC question string.
	"""
	# Randomly pick pathway length for variety between questions
	num_letters = random.randint(4, 7)
	# Generate metabolite data once, use for both diagram and choices
	metabolites = metaboliclib.get_metabolite_data(num_letters, N)
	metabolic_table = metaboliclib.generate_metabolic_pathway(metabolites)

	# Build question stem with pathway diagram
	question_text = '<p>A series of enzymes catalyze the reactions in the following metabolic pathway:</p>'
	question_text += metabolic_table
	question_text += '<p>In a typical metabolic pathway, an allosteric enzyme is sensitive to changes in concentration of specific molecules and can regulate the rate of reactions.</p>'
	question_text += '<p>Which one of the enzymes in the metabolic pathway above is most likely to be an allosteric enzyme?</p>'

	# Build choices using colored text from the same metabolite data
	choices_list = []
	for i in range(len(metabolites) - 1):
		substrate = metaboliclib.color_text(metabolites[i][0], metabolites[i][1])
		product = metaboliclib.color_text(metabolites[i+1][0], metabolites[i+1][1])
		choice_str = f'<strong>enzyme {i+1}</strong> '
		choice_str += f'that catalyzes the reaction from substrate {substrate} to product {product}'
		choices_list.append(choice_str)
	answer_text = choices_list[0]

	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#============================================
#============================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate questions about metabolic pathways.")
	args = parser.parse_args()
	return args

#============================================
#============================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
#============================================
if __name__ == '__main__':
	main()

## THE END
