#!/usr/bin/env python3


# Standard Library
import os
import sys
import argparse

# Local repo modules
import bptools
import genemapclass as gmc

debug = False

#===========================
def get_question_text(question_type):
	"""
	Generates the question text based on the question type.

	Args:
		question_type (str): Type of question ('num' or 'mc').

	Returns:
		str: The formatted question text.
	"""
	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>With the progeny data from the table, '
	question_string += '<strong>calculate the genetic distance between the two genes,</strong> '
	question_string += 'expressing your answer in centimorgans (cM)</p> '
	if question_type == 'num':
		question_string += '<ul> '
		question_string += '<li><i>Important Tip 1:</i> '
		question_string +=   'Your calculated distance between the genes should be a whole number. '
		question_string +=   'Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
		question_string +=   'Please provide your answer as a complete number without fractions or decimals.</li>'
		question_string += '<li><i>Important Tip 2:</i> '
		question_string +=   'Your answer should be written as a numerical value only, '
		question_string +=   'no spaces, commas, or units such as "cM" or "map units". '
		question_string +=   'For example, if the distance is fifty one centimorgans, simply write "51". </li> '
		question_string += '</ul> '
	return question_string


#===========================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		Namespace: Parsed arguments with attributes `question_type` and `duplicates`.
	"""
	parser = argparse.ArgumentParser(description='Process some integers.')
	question_group = parser.add_mutually_exclusive_group(required=True)

	# Add question type argument with choices
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('num', 'mc'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)
	question_group.add_argument(
		'-n', '--num', dest='question_type', action='store_const', const='num',
		help='Set question type to numeric'
	)

	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do', default=1
	)

	return parser.parse_args()

#===========================
def generate_question(N: int, question_type: str) -> str:
	"""
	Generates a formatted question string based on the type.

	Args:
		N (int): Question number.
		question_type (str): Type of question ('num' or 'mc').

	Returns:
		str: The formatted question string ready to be written to the file.
	"""
	# Initialize Gene Mapping Class instance
	GMC = gmc.GeneMappingClass(2, N)
	global debug
	GMC.debug = debug
	GMC.question_type = question_type
	GMC.setup_question()

	# Retrieve question data
	header = GMC.get_question_header()
	phenotype_info_text = GMC.get_phenotype_info()
	html_table = GMC.get_progeny_html_table()
	question_string = get_question_text(question_type)

	# Assemble full question content
	full_question = header + phenotype_info_text + html_table + question_string

	# Format question based on type
	if question_type == 'num':
		distance = GMC.distances_dict[(1, 2)]
		return bptools.formatBB_NUM_Question(N, full_question, distance, 0.1, tol_message=False)
	elif question_type == 'mc':
		choices_list, answer_text = GMC.make_choices()
		return bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
	else:
		print("Error: Invalid question type in generate_question.")
		sys.exit(1)

#===========================
def main():
	"""
	Main function that handles generating questions and writing them to an output file.
	"""
	args = parse_arguments()

	# Setup output file
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile =  f'bbq-{script_name}-{args.question_type.upper()}-questions.txt'
	print(f'Writing to file: {outfile}')

	# Open file and write questions
	with open(outfile, 'w') as f:
		for i in range(args.duplicates):
			N = i + 1  # Question number
			final_question = generate_question(N, args.question_type)
			f.write(final_question)
	if args.question_type == "mc":
		bptools.print_histogram()

if __name__ == "__main__":
	main()

#THE END
