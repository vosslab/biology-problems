#!/usr/bin/env python3

# external python/pip modules
import os
import random
import argparse
# local repo modules
import bptools
import metaboliclib

#==========================
def generateQuestionText(letters: list, metabolic_table: str, question_type_id: int) -> str:
	"""
	Construct the question text based on input letters and metabolic table.

	Parameters
	----------
	letters : list
	    Sequence of letters representing metabolites in the pathway.
	metabolic_table : str
	    Formatted string of the metabolic reactions.
	question_type_id : int
	    Identifier that indicates the type of question to generate.

	Returns
	-------
	str
	    Formatted question text segment.
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

#==========================
def generateChoices(letters: list, question_type_id: int) -> (list, str):
	"""
	Create a list of answer choices and identify the correct answer.

	Parameters
	----------
	letters : list
	    Sequence of letters representing metabolites in the pathway.
	question_type_id : int
	    Identifier to select the type of question and its corresponding answer.

	Returns
	-------
	list
	    A shuffled list of possible answer choices.
	str
	    The correct answer for the question.
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

#==========================
def writeQuestion(N: int, num_letters: int, course_name: str) -> str:
	"""
	Create a metabolic pathway question.

	Parameters
	----------
	N : int
	    Identifier for the question.
	num_letters : int
	    Total letters representing metabolites in the pathway.

	Returns
	-------
	str
	    Fully formatted question for display.
	"""
	if course_name == 'bchm355':
		# BCHM 355/455
		question_type_id = (N-1)%4 #random.randint(0, 3)
	else:
		# BIOL 301
		question_type_id = (N-1)%2 #random.randint(0, 3)

	letters = metaboliclib.get_letters(num_letters, N)
	metabolic_table = metaboliclib.generate_metabolic_pathway(num_letters, N)

	# Add more to the question based on the given letters
	question_text = generateQuestionText(letters, metabolic_table, question_type_id)

	# Choices and answers
	new_choices_list, answer_text = generateChoices(letters, question_type_id)

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, new_choices_list, answer_text)
	return complete_question

#======================================
#======================================
#======================================
#======================================
if __name__ == '__main__':
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions about metabolic pathways.")
	parser.add_argument('-d', '--duplicates', type=int, default=99, help="Number of questions to create.")
	parser.add_argument('-n', '--num_letters', type=int, default=5, help="Number of letters in the metabolic pathway.")

	# Create a mutually exclusive group for question types
	course_group = parser.add_mutually_exclusive_group(required=True)
	# Add question type argument with choices
	course_group.add_argument('-c', '--course', dest='course', type=str,
		choices=('biol301', 'bchm355'),
		help='Set the course: biol301 or bchm355.')
	# Add flags for multiple-choice and fill-in-the-blank question types
	course_group.add_argument('--biol301', dest='course', action='store_const', const='biol301',
		help='Set question type to BIOL 301.')
	course_group.add_argument('--bchm355', dest='course', action='store_const', const='bchm355',
		help='Set question type to BCHM 355/455.')

	args = parser.parse_args()

	# Generate the output file name based on the script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{args.course.upper()}'
		f'-{script_name}'  # Add the script name to the file name
		'-questions.txt'  # Add the file extension
	)

	print(f'writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0
		# Generate the specified number of questions
		for _ in range(args.duplicates):
			# Generate the complete formatted question
			complete_question = writeQuestion(N+1, args.num_letters, args.course)
			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)
	bptools.print_histogram()
	# Print a message indicating how many questions were saved
	print(f'saved {N} questions to {outfile}')
