#!/usr/bin/env python3

import random

import bptools
import gene_map_class_lib as gmc

debug = False

#=====================
#=====================
def get_question_text(question_type='parental', gene_pair=None):
	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>Based on the traits expressed in the offspring, identify the '
	if question_type == 'parental':
		question_string += '<span style="color: DarkRed;"><strong>'
		question_string +=   f'{question_type} genotype combinations</strong></span>. '
		question_string +=   'These are the allele combinations that the parent fruit flies originally carried.</p> '
	elif question_type == 'double':
		question_string += '<span style="color: DarkGreen;"><strong>'
		question_string +=   f'{question_type} crossover genotype combinations</strong></span>. '
		question_string +=   'These allele combinations are a result of two genetic crossover events.</p> '
	elif question_type == 'genes' and gene_pair is not None:
		gene_pair_text =   f'genes <b>{gene_pair[0].upper()}</b> and <b>{gene_pair[1].upper()}</b>'
		question_string += '<span style="color: DarkBlue;"><strong>'
		question_string +=   f'all recombinant genotypes</strong></span> for {gene_pair_text}. '
		question_string += f'These genotypes result from crossover events that occur between the two {gene_pair_text} during meiosis.</p> '
	else:
		print('failed question type')
		raise ValueError
	question_string += '<p>More than one genotype will be correct. '
	question_string += 'Select all that apply.</p> '
	return question_string

#=====================
#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate three-point test cross genotype identification (MA) questions."
	)
	question_group = parser.add_mutually_exclusive_group(required=True)
	question_group.add_argument(
		'-t', '--type', dest='mode', type=str,
		choices=('parental', 'double', 'genes'),
		help='Select which genotype set students must identify.'
	)
	question_group.add_argument(
		'-p', '--parental', dest='mode', action='store_const', const='parental',
		help='Identify parental genotype combinations.'
	)
	question_group.add_argument(
		'-D', '--double', dest='mode', action='store_const', const='double',
		help='Identify double crossover genotype combinations.'
	)
	question_group.add_argument(
		'-g', '--genes', dest='mode', action='store_const', const='genes',
		help='Identify all recombinant genotypes for a gene pair.'
	)
	args = parser.parse_args()
	return args

#=====================
def write_question(N: int, args) -> str | None:
	GMC = gmc.GeneMappingClass(3, N)
	GMC.setup_question()
	if debug:
		print(GMC.get_progeny_ascii_table())
	header = GMC.get_question_header()
	html_table = GMC.get_progeny_html_table()
	phenotype_info_text = GMC.get_phenotype_info()

	sorted_genotype_counts = sorted(GMC.genotype_counts.items(), key=lambda x: x[1], reverse=True)
	parental_genotypes_tuple = tuple(sorted((sorted_genotype_counts[0][0], sorted_genotype_counts[1][0])))
	if parental_genotypes_tuple != GMC.parental_genotypes_tuple:
		raise ValueError(f'parental_genotypes_tuple: {parental_genotypes_tuple} != {GMC.parental_genotypes_tuple}')
	double_cross_genotypes_tuple = (sorted_genotype_counts[-1][0], sorted_genotype_counts[-2][0])

	choices_list = sorted(GMC.genotype_counts.keys(), reverse=True)
	gene_pair = None
	if args.mode == 'parental':
		answers_list = list(GMC.parental_genotypes_tuple)
	elif args.mode == 'double':
		answers_list = list(double_cross_genotypes_tuple)
	elif args.mode == 'genes':
		genes_list = list(GMC.gene_letters_str)
		random.shuffle(genes_list)
		gene_pair = tuple(genes_list[0:2])
		answers_list = GMC.get_all_recombinants_for_gene_pair(gene_pair)
	else:
		raise ValueError(f'unknown mode: {args.mode}')

	question_string = get_question_text(args.mode, gene_pair)
	full_question = header + phenotype_info_text + html_table + question_string
	GMC.is_valid_html(full_question)
	return bptools.formatBB_MA_Question(N, full_question, choices_list, answers_list)

#=====================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(args.mode.upper())
	bptools.collect_and_write_questions(write_question, args, outfile)

#=====================
if __name__ == "__main__":
	main()
