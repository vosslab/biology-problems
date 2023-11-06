#!/usr/bin/env python3

import os
import math
import argparse

import bptools
import genemapclass as gmc

debug = False

#=====================
#=====================
def get_question_text(gene_order_str):
	question_string = ''

	question_string += '<p>In genetic studies, interference refers to the phenomenon where the '
	question_string += 'occurrence of a crossover in one region of a chromosome inhibits the occurrence'
	question_string += 'of another crossover nearby, affecting the expected genetic ratios.</p> '

	question_string += '<h6>Question</h6> '
	question_string += '<p>Based on the traits expressed in the offspring, '
	question_string += '<strong>calculate the percentage of interference</strong> '
	question_string += f'between genes {gene_order_str[0]} and {gene_order_str[-1]}.</p> '


	question_string += '<p><ul> '
	question_string += '<li><i>Important Tip 1:</i> '
	question_string +=   'Your calculated interfence between each pair of gene should be a whole number. '
	question_string +=   'Finding a decimal in your answer, such as 0.055 (which is 5.5%), suggests a mistake was made. '
	question_string +=   'Please provide your answer as a complete number without fractions or decimals.</li>'
	question_string += '<li><i>Important Tip 2:</i> '
	question_string +=   'Your answer should be written as a numerical value only, '
	question_string +=   'no spaces, commas, or symbols such as "&percnt;". '
	question_string +=   'For example, if the interference is 0.31 = 31%, simply write "31". </li> '
	question_string += '</ul></p> '

	return question_string

#=====================
def describe_gene_map(GMC):
	describe_gene_map_string = ''
	up_genes = GMC.gene_order_str.upper()
	distances_dict = GMC.distances_dict

	describe_gene_map_string += '<p>The resulting phenotypes are summarized in the table above.</p> '

	describe_gene_map_string += '<p><ul> '
	describe_gene_map_string += '<li>The distance between genes '
	describe_gene_map_string += f'{up_genes[0]} and {up_genes[1]} is {distances_dict[(1,2)]} cM</li>'
	describe_gene_map_string += '<li>The distance between genes '
	describe_gene_map_string += f'{up_genes[0]} and {up_genes[2]} is {distances_dict[(1,3)]} cM</li>'
	describe_gene_map_string += '<li>The distance between genes '
	describe_gene_map_string += f'{up_genes[1]} and {up_genes[2]} is {distances_dict[(2,3)]} cM</li>'
	describe_gene_map_string += f'<li>The correct gene order determined from these distances is {up_genes}</li>'
	describe_gene_map_string += '</ul></p> '
	return describe_gene_map_string

#=====================
#=====================
def make_choice_text_from_fraction(a,b):
	"""gcd = math.gcd(a,b)
	a //= gcd
	b //= gcd"""
	decimal = a/float(b)
	percent = (100*a)/float(b)
	percent = int(round(percent))
	text = f'{a}/{b} = {decimal:.4f} = {percent:d}%'
	return text, percent

#=====================
#=====================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	question_group = parser.add_mutually_exclusive_group()
	# Add question type argument with choices
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	outfile = ('bbq-' + os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicates):
		N += 1
		# Gene Mapping Class
		GMC = gmc.GeneMappingClass(3, N)
		GMC.interference_mode = False
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

		choices_list = [ 'no interference, 0%', ]

		a,b = GMC.interference_dict[(1,3)]
		if (a,b) == (1,2):
			continue
		choices_dict = {
			100: 'complete interference, 100%',
			 50: '1/2 = 0.500 = 50%',
			  0: 'no interference, 0%',
		}
		answer_text, ans_percent = make_choice_text_from_fraction(a, b)
		choices_dict[ans_percent] = answer_text
		wrong_text, wrong_percent = make_choice_text_from_fraction(b-a, b)
		choices_dict[wrong_percent] = wrong_text

		if b < 8:
			for i in range(1, b):
				another_text, another_percent = make_choice_text_from_fraction(i, b)
				choices_dict[another_percent] = another_text
		else:
			for i in range(1, b, 2):
				another_text, another_percent = make_choice_text_from_fraction(i, b)
				choices_dict[another_percent] = another_text

		choices_list = [value for (key, value) in sorted(choices_dict.items(), key=lambda x: x[0])]
		print(choices_list)

		describe_gene_map_string = describe_gene_map(GMC)
		question_string = get_question_text(GMC.gene_order_str.upper())
		full_question = header + phenotype_info_text + html_table + describe_gene_map_string + question_string
		GMC.is_valid_html(full_question)
		final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)

		f.write(final_question)
	f.close()
	bptools.print_histogram()

#THE END
