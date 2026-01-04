#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
import copy
import random

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import hybridcrosslib as crossinglib

#===================
#===================
def questionContent(gene_id):
	question = ''
	question += '<p>Above are the phenotypic results from a dihybrid cross and double heterozygote test cross. '
	question += 'The phenotypes were '
	ratio = crossinglib.gene_type_ratios[gene_id]
	counts = ratio.split(':')
	for count in counts:
		question += '{0} to '.format(crossinglib.num2word[int(count)])
	question = question[:-4]
	question += ' ({0}).</p>'.format(ratio)
	question += '<p><strong>What type of gene interaction is being shown?</strong></p>'
	#print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	assigned_colors = crossinglib.dihybridAssignColorsOriginal(gene_id, color_set)
	dihybrid_table = crossinglib.createDiHybridTable(letter1, letter2, assigned_colors)
	testcross_table = crossinglib.createTestCrossTable(letter1, letter2, assigned_colors)

	# write the question content
	question = questionContent(gene_id)

	complete_question = '<table style="border: 0px solid white; border-collapse: collapse; ">'
	complete_question += ' <tr><td> '
	complete_question += dihybrid_table
	complete_question += ' </td><td> '
	complete_question += '&nbsp;'
	complete_question += ' </td><td> '
	complete_question += testcross_table
	complete_question += '</td></tr></table> '

	complete_question += " <br/> "
	complete_question += question

	#print(complete_question)
	return complete_question


#===================
#===================
def gene_id_to_choice_text(gene_id: str) -> str:
	"""
	Converts a gene interaction ID to a formatted choice text.

	Args:
		gene_id (str): The gene interaction identifier.

	Returns:
		str: Formatted choice text string.
	"""
	name = crossinglib.gene_interaction_names[gene_id]
	description = crossinglib.gene_type_description[gene_id]
	choice_text = f"These two genes show <strong>{name}</strong> {description}."
	return choice_text

#===================
#===================
def build_question(N: int, answer_gene_id: str, color_set: list, num_choices: int) -> str:
	"""
	Creates a formatted MC question about gene interaction types.

	Args:
		N (int): Question number
		answer_gene_id (str): The correct gene interaction type ID
		color_set (list): List of colors involved in the genetic scenario

	Returns:
		str: Complete formatted Blackboard question string
	"""
	# Select and sort two gene letters for use in question table
	letter_pool = copy.copy(crossinglib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = sorted([letter_pool.pop(), letter_pool.pop()])

	# Create the main question text
	question_text = makeQuestion(answer_gene_id, color_set, two_letters[0], two_letters[1])

	# Build answer and choices
	answer_text = gene_id_to_choice_text(answer_gene_id)

	all_gene_ids = set(crossinglib.gene_interaction_names.keys())
	if len(all_gene_ids) > num_choices:
		# Exclude the correct answer first using a set
		available_distractors = list(all_gene_ids - {answer_gene_id})
		# Sample random distractors
		distractors = set(random.sample(available_distractors, num_choices - 1))
		# Add the correct answer
		all_gene_ids = distractors | {answer_gene_id}

	choices_list = []
	for sub_gene_id in all_gene_ids:
		choice_text = gene_id_to_choice_text(sub_gene_id)
		choices_list.append(choice_text)

	random.shuffle(choices_list)
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return complete_question

#===================
#===================
def write_question(N: int, args) -> str:
	all_gene_ids = list(crossinglib.gene_interaction_names.keys())
	all_color_sets = crossinglib.get_four_color_sets()
	gene_id = all_gene_ids[(N - 1) % len(all_gene_ids)]
	color_set = random.choice(all_color_sets)
	complete_question = build_question(N, gene_id, color_set, args.num_choices)
	return complete_question

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with base args and `num_choices`.
	"""
	parser = bptools.make_arg_parser(description="Generate epistatic gene interaction questions.")
	parser = bptools.add_choice_args(parser, default=4)
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile(f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
