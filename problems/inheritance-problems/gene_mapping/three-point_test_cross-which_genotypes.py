#!/usr/bin/env python3

import os
import random
import argparse

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
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	question_group = parser.add_mutually_exclusive_group(required=True)
	# Add question type argument with choices
	question_group.add_argument('-t', '--type', dest='question_type', type=str,
		choices=('parental', 'double', 'genes'), help='Set the question type: accept or reject')
	question_group.add_argument('-p', '--parental', dest='question_type', action='store_const',
		const='parental',)
	question_group.add_argument('-D', '--double', dest='question_type', action='store_const',
		const='double',)
	question_group.add_argument('-g', '--genes', dest='question_type', action='store_const',
		const='genes',)
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ f'-{args.question_type.upper()}'
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicates):
		N += 1
		# Gene Mapping Class
		GMC = gmc.GeneMappingClass(3, N)
		GMC.setup_question()
		print(GMC.get_progeny_ascii_table())
		header = GMC.get_question_header()
		html_table = GMC.get_progeny_html_table()
		phenotype_info_text = GMC.get_phenotype_info()

		#typemap, type_categories = makeQuestion(basetype, geneorder, distances, progeny_size)

		sorted_genotype_counts = sorted(GMC.genotype_counts.items(), key=lambda x: x[1], reverse=True)
		parental_genotypes_tuple = tuple(sorted((sorted_genotype_counts[0][0], sorted_genotype_counts[1][0])))
		if parental_genotypes_tuple != GMC.parental_genotypes_tuple:
			raise ValueError(f'parental_genotypes_tuple: {parental_genotypes_tuple} != {GMC.parental_genotypes_tuple}')
		double_cross_genotypes_tuple = (sorted_genotype_counts[-1][0], sorted_genotype_counts[-2][0])

		choices_list = sorted(GMC.genotype_counts.keys(), reverse=True)
		gene_pair = None
		if args.question_type == 'parental':
			answers_list = list(GMC.parental_genotypes_tuple)
		elif args.question_type == 'double':
			answers_list = list(double_cross_genotypes_tuple)
		elif args.question_type == 'genes':
			genes_list = list(GMC.gene_letters_str)
			random.shuffle(genes_list)
			gene_pair = tuple(genes_list[0:2])
			answers_list = GMC.get_all_recombinants_for_gene_pair(gene_pair)
		else:
			raise ValueError(f'unknown question type: {args.question_type}')

		question_string = get_question_text(args.question_type, gene_pair)
		full_question = header + phenotype_info_text + html_table + question_string
		GMC.is_valid_html(full_question)
		final_question = bptools.formatBB_MA_Question(N, full_question, choices_list, answers_list)

		f.write(final_question)
	f.close()
	bptools.print_histogram()

#THE END
