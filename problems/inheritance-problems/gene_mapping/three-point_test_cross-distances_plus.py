#!/usr/bin/env python3

import os
import argparse
import itertools

import bptools
import gene_map_class_lib as gmc

#===========================================================
#===========================================================
def get_question_text(gene_letters: str) -> str:
	question_string = ''
	question_string += '<h6>Question</h6> '
	question_string += '<p>Using the table above, determine the order of the genes and the distances between them. '
	question_string += 'Once calculated, fill in the following four blanks: </p><ul>'

	# FIXED: removed the illegal <p><ul> nesting and stray <li>
	# question_string += '<ul>'  # REMOVE THIS LINE
	#the gene letters ARE sorted, so this okay since it is not the gene order
	for gene1, gene2 in itertools.combinations(gene_letters.upper(), 2):
		question_string += f'<li>The distance between genes {gene1} and {gene2} is '
		question_string += f'[{gene1}{gene2}] cM ({gene1}{gene2})</li>'
	question_string += '<li>From this the correct order of the genes is [geneorder] (gene order).</li>'
	question_string += '</ul>'

	question_string += get_question_footer_tips()
	return question_string

#===========================================================
#===========================================================
def get_question_footer_tips():
	"""
	Returns the HTML formatted hints for solving the problem.

	Returns:
		str: HTML formatted string with hints.
	"""
	tips = '<h6>Hints</h6>'
	tips += '<ul>'
	tips += '<li><i>Important Tip 1:</i> '
	tips += 'Your calculated distances between each pair of genes should be a whole number. '
	tips += 'Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
	tips += 'Please provide your answer as a complete number without fractions or decimals.</li>'
	tips += '<li><i>Important Tip 2:</i> '
	tips += 'Your answer should be written as a numerical value only, '
	tips += 'with no spaces, commas, or units such as "cM" or "map units". '
	tips += 'For example, if the distance is fifty one centimorgans, simply write "51".</li>'
	tips += '<li><i>Important Tip 3:</i> '
	tips += 'Your gene order answer should be written as three letters only, '
	tips += 'with no spaces, commas, hyphens, or other characters allowed. '
	tips += 'For example, if the gene order is B - A - C, simply write "bac" or "cab".</li>'
	tips += '</ul>'
	return tips

#===========================================================
#===========================================================
def get_answer_mapping(gene_order: str, distances_dict: dict) -> list:
	# Generate all combinations of 2 genes, and sort each combination alphabetically
	answer_map = { 'geneorder': [gene_order, gene_order[::-1]], }
	for gene_index_pair in itertools.combinations(range(1,len(gene_order)+1), 2):
		print(gene_index_pair)
		gene_pair = (gene_order[gene_index_pair[0]-1], gene_order[gene_index_pair[1]-1])
		gene_letter_pair_str = ''.join(sorted(gene_pair)).upper()
		distance = distances_dict[tuple(gene_index_pair)]
		answer_map[gene_letter_pair_str] = [str(distance),]
	return answer_map
assert get_answer_mapping('ab', {(1,2): 3,}) == {'geneorder': ['ab', 'ba'], 'AB': ['3']}

#=====================
#=====================
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	lowercase = "abcdefghijklmnpqrsuvwxyz"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	j = -1
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

		question_string = get_question_text(GMC.gene_letters_str)
		full_question = header + phenotype_info_text + html_table + question_string
		answer_map = get_answer_mapping(GMC.gene_order_str, GMC.distances_dict)
		print(answer_map)
		final_question = bptools.formatBB_FIB_PLUS_Question(N, full_question, answer_map)
		#print(final_question)
		f.write(final_question)
		print('\n\n')
	f.close()
#THE END
