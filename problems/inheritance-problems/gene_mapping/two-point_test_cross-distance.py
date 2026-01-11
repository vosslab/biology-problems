#!/usr/bin/env python3

# Local repo modules
import bptools
import gene_map_class_lib as gmc

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
	parser = bptools.make_arg_parser(
		description="Generate two-point test cross distance questions."
	)
	parser = bptools.add_choice_args(parser, default=6)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc', 'num'],
		required=True
	)
	parser.set_defaults(duplicates=1)
	return parser.parse_args()

#===========================
def generate_question(N: int, args) -> str:
	"""
	Generates a formatted question string based on the type.

	Args:
		N (int): Question number.
		args (argparse.Namespace): Parsed arguments with question settings.

	Returns:
		str: The formatted question string ready to be written to the file.
	"""
	# Initialize Gene Mapping Class instance
	GMC = gmc.GeneMappingClass(2, N)
	GMC.question_type = args.question_type
	GMC.setup_question()

	# Retrieve question data
	header = GMC.get_question_header()
	phenotype_info_text = GMC.get_phenotype_info()
	html_table = GMC.get_progeny_html_table()
	question_string = get_question_text(args.question_type)

	# Assemble full question content
	full_question = header + phenotype_info_text + html_table + question_string

	# Format question based on type
	if args.question_type == 'num':
		distance = GMC.distances_dict[(1, 2)]
		return bptools.formatBB_NUM_Question(N, full_question, distance, 0.1, tol_message=False)
	elif args.question_type == 'mc':
		choices_list, answer_text = GMC.make_choices(num_choices=args.num_choices)
		return bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
	else:
		raise ValueError("Error: Invalid question type in generate_question.")

#===========================
def main():
	"""
	Main function that handles generating questions and writing them to an output file.
	"""
	args = parse_arguments()

	hint_mode = 'with_hint' if args.hint else 'no_hint'
	suffix = f"{args.num_choices}_choices" if args.question_type == "mc" else None
	outfile = bptools.make_outfile(args.question_type.upper(),
		hint_mode,
		suffix
	)
	bptools.collect_and_write_questions(generate_question, args, outfile)

if __name__ == "__main__":
	main()

#THE END
