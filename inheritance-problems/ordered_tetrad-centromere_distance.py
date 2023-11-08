#!/usr/bin/env python3

import os
import math
import random
import argparse

import bptools
debug = False

#=====================
#=====================
patterns = (
	"++++aaaa",
	"++aa++aa",
	"++aaaa++",
	"aa++++aa",
	"aa++aa++",
	"aaaa++++",
)


def get_background_context():
	background_text = ''
	background_text += "<h3>Ordered Tetrads in <i>Neurospora crassa</i></h3>"
	background_text += "<h6>Background Information</h6>"
	background_text += "<p><strong><i>Neurospora crassa</i></strong> is an organism that has significantly contributed to the understanding of genetics. This fungus exhibits a distinctive genetic feature: the formation of ordered tetrads. These ordered tetrads result from the typical two rounds of meiotic divisions followed by a single round of mitotic division within an ascus, resulting in eight ascospores arranged in a predictable sequence. The position of each ascospore reflects the series of genetic events during cell division, providing a snapshot of the meiotic process.</p>"
	background_text += "<p>The analysis of these ordered tetrads in <i>Neurospora crassa</i> allows for the classification of ascospores based on their allele arrangements into different segregation patterns.</p>"
	background_text += "<p>The central principle in this analysis is the distinction between first-division and second-division segregation, which is based on the behavior of alleles in the presence or absence of crossover between a gene and its centromere. When alleles separate during the first meiotic division, it indicates first-division segregation. Conversely, if alleles separate during the second division, this suggests that a crossover event has occurred, leading to second-division segregation.</p>"
	background_text += "<p>Counting the frequency of second-division segregation events within these ordered tetrads can provide an estimate of the genetic distance between a gene and its centromere. This frequency, reflective of the crossover events during meiosis, is used to calculate the recombination frequency. Such estimates are crucial for constructing genetic maps, which serve as a guide to the genetic landscape of Neurospora crassa, enhancing our understanding of genetic linkage and the location of genes relative to centromeres.</p>"
	return background_text

#=====================
#=====================
def get_formula():
	formula = ''
	formula += "<h6>Distance Formula</h6>"
	formula += ( ''
		+ '<table border="0" style="border-collapse: collapse">'
		+ '<tr><td rowspan="2" style="; vertical-align: middle; text-align: right;">'
		+ 'distance between a gene<br/>and its centromere</td>'
		+ '<td rowspan="2" style="; vertical-align: middle; padding: 10px;">=</td>'
		+ '<td style="border-bottom: 1px solid black; text-align: center">'
		+ '&half; &times; (asci with second-division segregation patterns)'
		+ '</td></tr><tr><td style="border-top: 1px solid black; text-align: center">'
		+ 'total number of asci'
		+ '</td></tr></table>'
	)
	return formula


#=====================
#=====================
def split_counts_into_bins(count, bins=2):
	bin_list = [0 for i in range(bins)]
	for i in range(count):
		bin_num = int(math.floor(random.random()*bins))
		bin_list[bin_num] += 1
	print(bin_list)
	return bin_list

#=====================
#=====================
def get_asci_counts(distance):
	"""
	d = count / N / 2 * 100
	count/N = 2 * d/100
	count = d/50 * N
	"""
	parental_patterns = ('++++aaaa', 'aaaa++++')
	total_count = random.randint(3, 199) * 50
	recombinant_count = total_count * distance // 50
	parental_count = total_count - recombinant_count
	parent_counts = split_counts_into_bins(parental_count, 2)
	recon_counts = split_counts_into_bins(recombinant_count, 4)
	asci_count_dict = {}
	for i, pattern in enumerate(parental_patterns):
		asci_count_dict[pattern] = parent_counts[i]
	recon_patterns = set(patterns)
	recon_patterns -= set(parental_patterns)
	for i, pattern in enumerate(recon_patterns):
		asci_count_dict[pattern] = recon_counts[i]
	check_count = sum(asci_count_dict.values())
	if check_count != total_count:
		raise ValueError
	return asci_count_dict

#=====================
#=====================
def generate_html_for_pattern(pattern, color_dominant, color_recessive):
	"""
	Generate an HTML string for a given genetic pattern.

	Args:
	- pattern (str): The pattern of '+' and 'a' representing genetic outcomes.
	- color_dominant (str): The color representing '+'.
	- color_recessive (str): The color representing 'a'.

	Returns:
	- str: An HTML string representing the pattern.
	"""
	html_output = ''
	html_output += '<table border="0" style="padding: 10px;"> <tr>'
	# Create table cells based on the pattern
	for char in pattern:
		bgcolor = color_dominant if char == char.upper() or char == '+' else color_recessive
		html_output += f'<td width="40" height="40" bgcolor="{bgcolor}" '
		html_output += 'style="border-radius:  15% 50% 30%; '
		html_output += 'text-align: center; vertical-align: middle; '
		html_output += 'color: #f0f0f0; font-size: 25px;"> '
		html_output += f'{char} </td> '
	html_output += '</tr></table> '
	bptools.is_valid_html(html_output)
	return html_output

#=====================
#=====================
def get_octads_table(asci_count_dict, gene_letter):
	color_dominant, color_recessive = bptools.default_color_wheel(2)
	octads_table = ''
	octads_table += "<h6>Experimental Data</h6>"
	octads_table += "<p>In the table below, the six different patterns of ordered asci in <i>Neurospora crassa</i> are listed along with the counts found in an experiment.</p>"
	octads_table += '<table style="border: 1px solid black; border-collapse: collapse;">'
	octads_table += '<tr><th style="padding: 10px; border: 1px solid gray; background-color: lightgray;">'
	octads_table += 'Octad'
	octads_table += '</th>'
	octads_table += '<th style="padding: 10px; border: 1px solid gray; background-color: lightgray;">'
	octads_table += 'Asci<br/>Count'
	octads_table += '</th></tr>'
	# Generate and print the HTML for each pattern
	for i, pattern in enumerate(patterns, start=1):
		new_pattern = pattern.replace('a', gene_letter)
		octads_table += '<tr><td style="padding: 10px; spacing: 20px; border: 1px solid gray; '
		octads_table += 'border-radius: 30%; background-color: #d2f9d2;">'
		html_for_pattern = generate_html_for_pattern(new_pattern, color_dominant, color_recessive)
		octads_table += html_for_pattern
		octads_table += '</td><td style="padding: 10px; border: 1px solid gray; text-align: right">'
		octads_table += f'{asci_count_dict[pattern]:,d}&nbsp;'
		octads_table += '</td></tr>'
	octads_table += '<tr><td style="padding: 10px; spacing: 20px; border: 1px solid gray; '
	octads_table += 'background-color: lightgray; text-align: right;">'
	octads_table += "<strong>TOTAL</strong>"
	octads_table += '</td><td style="padding: 10px; border: 1px solid gray; text-align: center">'
	total_asci_count = sum(asci_count_dict.values())
	octads_table += f'{total_asci_count:,d}'
	octads_table += '</td></tr>'
	octads_table += '</table>'
	bptools.is_valid_html(octads_table)
	return octads_table

#=====================
#=====================
def get_question_text(gene_letter):
	question_text = ''
	question_text += "<h6>Question</h6>"
	question_text += (
		'<p>Using the numbers of asci for each pattern shown in the table above, '
		+ f'<strong>determine the genetic distance between gene {gene_letter.upper()} and its centromere.</strong></p>'
		)
	return question_text

#=====================
#=====================
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
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
		gene_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
		distance = random.randint(2, 29)
		asci_count_dict = get_asci_counts(distance)

		background_text = get_background_context()
		formula = get_formula()
		octads_table = get_octads_table(asci_count_dict, gene_letter)
		question_text = get_question_text(gene_letter)

		full_question = background_text + octads_table + formula + question_text
		"""g = open('circle.html', 'w')
		g.write(full_question)
		g.close()
		print("open circle.html")"""
		bb_question = bptools.formatBB_NUM_Question(N, full_question, distance, 0.1, tol_message=False)
		f.write(bb_question)
	f.close()
	bptools.print_histogram()
