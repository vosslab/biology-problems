#!/usr/bin/env python3

import os
import argparse
import itertools

import bptools
import genemapclass as gmc

#===========================================================
#===========================================================
def get_question_text(gene_letters: str) -> str:
	up_genes = gene_letters.upper()
	question_string = ''
	question_string += '<p>The resulting phenotypes are summarized in the table above.</p> '
	question_string += '<h6>Question</h6> '
	question_string += '<p>Using the table above, determine the order of the genes and the distances between them. '
	question_string += 'Once you have calculated them, fill in the following four blanks: </p>'

	question_string += '<p><ul> '
	question_string += '<li>The distance between genes '
	#question_string += f'{up_genes[0]} and {up_genes[1]} is {} cM</li>'
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(up_genes[0], up_genes[1])
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(up_genes[0], up_genes[2])
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(up_genes[1], up_genes[2])
	question_string += '<li>From this the correct order of the genes is [geneorder] (gene order).</li>'
	question_string += '</ul></p> '

	question_string += '<p><ul> '
	question_string += '<li><i>Important Tip 1:</i> '
	question_string +=   'Your calculated distances between each pair of gene should be a whole number. '
	question_string +=   'Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
	question_string +=   'Please provide your answer as a complete number without fractions or decimals.</li>'
	question_string += '<li><i>Important Tip 2:</i> '
	question_string +=   'Your answer should be written as a numerical value only, '
	question_string +=   'no spaces, commas, or units such as "cM" or "map units". '
	question_string +=   'For example, if the distance is fifty one centimorgans, simply write "51". </li> '
	question_string += '</ul></p> '

	return question_string

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
		answer_map[gene_letter_pair_str] = [distance,]
	return answer_map
assert get_answer_mapping('ab', {(1,2): 3,}) == {'geneorder': ['ab', 'ba'], 'AB': [3]}

#===========================================================
#===========================================================
def formatBB_FIB_PLUS_Question(N: int, question: str, answer_map: dict) -> str:
	crc16 = bptools.getCrc16_FromString(question)

	#FIB_PLUS TAB question text TAB variable1 TAB answer1 TAB answer2 TAB TAB variable2 TAB answer3
	bb_question = f'FIB_PLUS\t<p>{crc16}</p> {question}'
	pretty_question = bptools.makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	keys_list = sorted(answer_map.keys())
	for key in keys_list:
		value_list = answer_map[key]
		bb_question += f'\t{key}'
		for value in value_list:
			bb_question += f'\t{value}'
		bb_question += '\t'
	bb_question += '\n'
	return bb_question

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
		final_question = formatBB_FIB_PLUS_Question(N, full_question, answer_map)
		#print(final_question)
		f.write(final_question)
		print('\n\n')
	f.close()
#THE END
