#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools
import metaboliclib

#============================================
#============================================
def generate_question_text(letters: list, metabolic_table: str, question_type_id: int) -> str:
	"""Construct the question text based on input letters and metabolic table.

	Args:
		letters (list): Sequence of letters representing metabolites in the pathway.
		metabolic_table (str): Formatted string of the metabolic reactions.
		question_type_id (int): Identifier that indicates the type of question to generate.

	Returns:
		str: Formatted question text segment.
	"""
	# Initialize the question text
	question_text = '<p>A series of enzymes catalyze the reactions in the following metabolic pathway:</p>'

	# Generate letters and metabolic table
	question_text += metabolic_table

	question_text += '<p>Understanding the type of enzyme inhibition or activation '
	question_text += 'is crucial for developing effective drugs and understanding metabolic regulation.</p>'

	question_text += f'<strong>enzyme 1</strong> converts substrate {letters[0]} into product {letters[1]}. '

	question_text += f'<p>The end product {letters[-1]} of this pathway binds to <strong>enzyme 1</strong>'

	# Define possible question endings
	question_types_text_list = [
		'in its active site blocking the substrate.</p>',  #comp. inhibitor
		'at a location far away from its active site.</p>', #non-comp. inhibitor
		'and its substrate in the active site at the same time.</p>', #un-comp. inhibitor
		'at a location far away from its active site.</p>' #activator
		]
	question_text += question_types_text_list[question_type_id]

	# Determine if the binding increases or decreases the activity
	if question_type_id == 3:
		activity_adjective = '<strong><span style="color: seagreen">increases</span></strong> '
	else:
		activity_adjective = '<strong><span style="color: brown">decreases</span></strong>'

	question_text += f'<p>This binding {activity_adjective} the activity of the enzyme.</p>'

	question_text += '<p>Determine the type of enzyme inhibition or activation described:</p>'

	return question_text

#============================================
#============================================
def generate_choices(question_type_id: int) -> tuple:
	"""Create a list of answer choices and identify the correct answer.

	Args:
		question_type_id (int): Identifier to select the type of question and its answer.

	Returns:
		tuple: (shuffled choices list, correct answer string).
	"""

	# Define possible choices and wrong choices
	choices_list = [
		'competitive inhibitor',
		'non-competitive inhibitor',
		'un-competitive inhibitor',
		'enzyme activator',
		]
	answer_text = choices_list[question_type_id]
	wrong_choices_list = [
		'molecular stopper',
		'metabolic blocker',
		'enzyme suppressor',
		'substrate displacer',
		'catalytic converter',
		'enzyme enhancer',
		'biochemical brake',
		'proteomic pothole',
		]
	random.shuffle(wrong_choices_list)
	choices_list.extend(wrong_choices_list[:1])

	# Shuffle choices for presentation
	random.shuffle(choices_list)

	return choices_list, answer_text

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""Create a metabolic pathway question about enzyme inhibition types.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: Fully formatted question for display.
	"""
	if args.course == 'bchm355':
		# BCHM 355/455: all four types
		question_type_id = random.randint(0, 3)
	else:
		# BIOL 301: competitive and non-competitive only
		question_type_id = random.randint(0, 1)

	# Randomly pick pathway length for variety between questions
	num_letters = random.randint(4, 7)
	# Generate metabolite data once, use for both diagram and question text
	metabolites = metaboliclib.get_metabolite_data(num_letters, N)
	metabolic_table = metaboliclib.generate_metabolic_pathway(metabolites)

	# Format colored text for use in question prose
	letters = [metaboliclib.color_text(m[0], m[1]) for m in metabolites]

	# Add more to the question based on the given letters
	question_text = generate_question_text(letters, metabolic_table, question_type_id)

	# Choices and answers
	new_choices_list, answer_text = generate_choices(question_type_id)

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, new_choices_list, answer_text)
	return complete_question

#============================================
#============================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate questions about metabolic pathways.")
	course_group = parser.add_mutually_exclusive_group(required=False)
	course_group.add_argument(
		'-c', '--course', dest='course', type=str,
		choices=('biol301', 'bchm355'),
		help='Set the course: biol301 or bchm355.'
	)
	course_group.add_argument(
		'--biol301', dest='course', action='store_const', const='biol301',
		help='Set question type to BIOL 301.'
	)
	course_group.add_argument(
		'--bchm355', dest='course', action='store_const', const='bchm355',
		help='Set question type to BCHM 355/455.'
	)
	parser.set_defaults(course='biol301')
	args = parser.parse_args()
	return args

#============================================
#============================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(args.course.upper())
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
#============================================
if __name__ == '__main__':
	main()
