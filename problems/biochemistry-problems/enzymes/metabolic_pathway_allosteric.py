#!/usr/bin/env python3

import bptools
import metaboliclib

#======================================
#======================================
# Generate a multiple-choice question about metabolic pathways
def write_question(N, args):
	# Create the question stem and generate the metabolic pathway table
	question_text = '<p>A series of enzymes catalyze the reactions in the following metabolic pathway:</p>'
	metabolic_table = metaboliclib.generate_metabolic_pathway(args.num_letters, N)
	letters = metaboliclib.get_letters(args.num_letters, N)
	#print(metabolic_table)

	# Add the generated metabolic table to the question
	question_text += metabolic_table

	question_text += '<p>In a typical metabolic pathway, an allosteric enzyme is sensitive to changes in concentration of specific molecules and can regulate the rate of reactions.</p>'

	question_text += '<p>Which one of the enzymes in the metabolic pathway above is most likely to be an allosteric enzyme?</p>'

	choices_list = []
	for i in range(args.num_letters - 1):
		choice_str = f'<strong>enzyme {i+1}</strong> '
		choice_str += f'that catalyzes the reaction from substrate {letters[i]} to product {letters[i+1]}'
		choices_list.append(choice_str)
	answer_text = choices_list[0]

	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#======================================
#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate questions about metabolic pathways.")
	parser.add_argument(
		'-n', '--num-letters', type=int, default=6, dest='num_letters',
		help="Number of letters in the metabolic pathway."
	)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	main()

## THE END
