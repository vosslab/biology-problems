#!/usr/bin/env python3

import bptools
import gene_map_class_lib as gmc

#====================================
def get_question_text():
	question_string = ''
	question_string += '<p>The phenotype counts resulting from the cross are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>Using the data presented in the table to determine the configuration '
	question_string += 'of the alleles on the parental chromosomes. '
	question_string += 'Determine whether the alleles for the two genes are in a '
	question_string += '<strong><i>cis</i></strong> (on the same chromosome) or '
	question_string += '<strong><i>trans</i></strong> (on different chromosomes) configuration.</p> '

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

	choices_list = ['cis', 'trans']
	extra_choices = ['both', 'neither', 'cannot be determined']
	choices_list += extra_choices[:3]
	if '++' in GMC.parental_genotypes_tuple:
		answer = 'cis'
	else:
		answer = 'trans'

	question_string = get_question_text()
	full_question = header + phenotype_info_text + html_table + question_string
	final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer)
	return final_question

#====================================
#====================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate two-point test cross cis/trans questions."
	)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc'],
		required=False,
		default='mc'
	)
	args = parser.parse_args()
	return args

#====================================
#====================================
def main():
	args = parse_arguments()
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(args.question_type.upper(),
		hint_mode
	)
	bptools.collect_and_write_questions(write_question, args, outfile)

#====================================
#====================================
if __name__ == "__main__":
	main()

#THE END
