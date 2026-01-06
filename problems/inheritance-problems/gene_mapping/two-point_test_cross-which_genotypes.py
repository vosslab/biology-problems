#!/usr/bin/env python3

import bptools
import gene_map_class_lib as gmc

#====================================
#====================================
def get_question_text(question_type='parental'):
	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>Review the phenotype counts shown in the table. '
	question_string += 'Based on the traits expressed in the offspring, identify the possible '
	question_string += f'<strong>{question_type} genotype combinations</strong>. '
	if question_type == 'parental':
		question_string += 'These are the allele combinations that the parent fruit flies originally carried. '
	else:  # Assuming the alternative is 'recombinant'
		question_string += 'These allele combinations have occurred due to genetic crossover. '
	question_string += 'More than one combination will be correct. '
	question_string += 'Select all that apply.</p> '
	return question_string

#====================================
#====================================
def write_question(N: int, args) -> str:
	# Gene Mapping Class
	GMC = gmc.GeneMappingClass(2, N)
	GMC.setup_question()
	print(GMC.get_progeny_ascii_table())
	header = GMC.get_question_header()
	html_table = GMC.get_progeny_html_table()
	phenotype_info_text = GMC.get_phenotype_info()

	choices_list = sorted(GMC.genotype_counts.keys(), reverse=True)
	if args.genotype_type == 'parental':
		answers_list = list(GMC.parental_genotypes_tuple)
	elif args.genotype_type == 'recombinant':
		answers_list = [item for item in choices_list if item not in GMC.parental_genotypes_tuple]
	else:
		raise ValueError(f"unknown question type {args.genotype_type}")

	question_string = get_question_text(args.genotype_type)
	full_question = header + phenotype_info_text + html_table + question_string
	final_question = bptools.formatBB_MA_Question(N, full_question, choices_list, answers_list)
	return final_question

#====================================
#====================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate two-point test cross genotype questions."
	)
	parser = bptools.add_hint_args(parser)

	# Create a mutually exclusive group for question types
	question_group = parser.add_mutually_exclusive_group(required=True)
	# Add question type argument with choices
	question_group.add_argument(
		'-t', '--type', dest='genotype_type', type=str,
		choices=('parental', 'recombinant'),
		help='Set the question type: parental or recombinant'
	)
	question_group.add_argument(
		'-p', '--parental', dest='genotype_type', action='store_const',
		const='parental',
	)
	question_group.add_argument(
		'-r', '--recombinant', dest='genotype_type', action='store_const',
		const='recombinant',
	)
	parser.set_defaults(duplicates=1)
	args = parser.parse_args()
	return args

#====================================
#====================================
def main():
	args = parse_arguments()
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(
		None,
		"MA",
		hint_mode,
		args.genotype_type.upper()
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

#====================================
#====================================
if __name__ == "__main__":
	main()

#THE END
