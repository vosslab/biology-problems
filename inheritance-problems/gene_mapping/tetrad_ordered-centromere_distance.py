#!/usr/bin/env python3

# Standard Library
import os
import math
import random
import argparse

# Local repo modules
import bptools
import genemaplib as gml

# Global debug flag
debug = False

# Constants
patterns = (
	"++++aaaa",
	"++aa++aa",
	"++aaaa++",
	"aa++++aa",
	"aa++aa++",
	"aaaa++++",
)

parental_patterns = ('++++aaaa', 'aaaa++++')

#=====================
#=====================
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

#===========================================================
#===========================================================
def get_important_tips():
	"""
	Returns the HTML formatted hints for solving the problem.

	Returns:
		str: HTML formatted string with hints.
	"""
	tips = '<h6>Important Answer Guidelines</h6>'
	tips += '<p><ul>'
	tips += '<li><i>Important Tip 1:</i> '
	tips += '  Your calculated distances between each pair of genes should be a whole number. '
	tips += '  Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
	tips += '  Please provide your answer as a complete number without fractions or decimals.</li>'
	tips += '<li><i>Important Tip 2:</i> '
	tips += '  Your answer should be written as a numerical value only, '
	tips += '  with no spaces, commas, or units such as "cM" or "map units". '
	tips += '  For example, if the distance is fifty one centimorgans, simply write "51".</li>'
	tips += '</ul></p>'
	if gml.is_valid_html(tips) is False:
		print(tips)
		raise ValueError
	return tips

#=====================
#=====================
def split_counts_into_bins(count: int, bins: int = 2) -> list:
	"""Splits a count into random bins and returns a list of counts."""
	bin_list = [0 for _ in range(bins)]
	for _ in range(count):
		bin_num = random.randint(0, bins - 1)
		bin_list[bin_num] += 1
	return bin_list

#=====================
#=====================
def get_asci_counts(distance: float) -> dict:
	"""
	d = count / N / 2 * 100
	count/N = 2 * d/100
	count = d/50 * N
	"""
	gcd = math.gcd(50, int(round(distance*100)))
	total_count = random.randint(3, 29) * 5000 / gcd
	recombinant_count = int(round(total_count * distance // 50))
	if abs(recombinant_count*50/total_count - distance) > 1e-6:
		print(recombinant_count, total_count, recombinant_count/total_count/2, distance)
		return None
	parental_count = int(round(total_count - recombinant_count))
	parent_counts = split_counts_into_bins(parental_count, 2)
	recon_counts = split_counts_into_bins(recombinant_count, 4)
	asci_count_dict = {}
	for i, pattern in enumerate(parental_patterns):
		asci_count_dict[pattern] = int(round(parent_counts[i]))
	recon_patterns = set(patterns)
	recon_patterns -= set(parental_patterns)
	for i, pattern in enumerate(recon_patterns):
		asci_count_dict[pattern] = int(round(recon_counts[i]))
	check_count = sum(asci_count_dict.values())
	if check_count != total_count:
		raise ValueError
	print(asci_count_dict)
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
def values_to_text(values: tuple, total_count:int):
	choice_text = '<sup>&half;&times;('
	val_sum = 0
	val_list = sorted(values)
	for val in val_list:
		choice_text += f'{val:,d} + '
		val_sum += val
	choice_text = choice_text[:-3]
	choice_text += f')</sup>/<sub>{total_count:,d}</sub> = '
	choice_text += f'<sup>&half;&times;{val_sum:,d}</sup>/<sub>{total_count:,d}</sub> = '
	float_val = val_sum/float(total_count)/2
	choice_text += f'{float_val:.4f} = '
	choice_text += f'{float_val*100:.2f} cM<br/>'

	return choice_text

#=====================
#=====================
def make_choices(asci_count_dict):
	choices_set = set()

	total_count = sum(asci_count_dict.values())
	answer_values = []
	for key in asci_count_dict.keys():
		if key not in parental_patterns:
			answer_values.append(asci_count_dict[key])
	answer_text = values_to_text(answer_values, total_count)
	print(f'answer_text={answer_text}')
	choices_set.add(answer_text)

	parent_values = []
	for key in asci_count_dict.keys():
		if key in parental_patterns:
			parent_values.append(asci_count_dict[key])
	parent_text = values_to_text(parent_values, total_count)
	print(f'parent_text={parent_text}')
	choices_set.add(parent_text)

	all_keys = list(asci_count_dict.keys())

	while(len(choices_set) < 6):
		num_items = random.randint(2, 4)
		keys_set = set()
		while(len(keys_set) < num_items):
			key = random.choice(all_keys)
			keys_set.add(key)
		values_list = []
		for key in keys_set:
			values_list.append(asci_count_dict[key])
		float_val = sum(values_list)/float(total_count)/2
		if float_val > 0.46:
			continue
		choice_text = values_to_text(values_list, total_count)
		choices_set.add(choice_text)
	return list(choices_set), answer_text

#=====================
def generate_question(N: int, question_type: str) -> str:
	"""Generates a formatted question string based on the question type and question number."""
	# Set up the genetic distance and calculate asci counts
	# Set precision step based on question type
	precision_step = 0.05 if question_type == 'mc' else 1.0
	base_range = (9, 29)
	# Generate a random distance within the base range and round it to the nearest precision step.
	raw_distance = random.uniform(base_range[0], base_range[1])
	distance = round(raw_distance / precision_step) * precision_step

	asci_count_dict = get_asci_counts(distance)
	if asci_count_dict is None:
		return None  # Skip this question if asci counts are invalid

	# Assemble question components
	background_text = get_background_context()
	formula = get_formula()
	gene_letter = gml.get_gene_letters(1)
	#print(f"GENE LETTER = {gene_letter}")
	octads_table = get_octads_table(asci_count_dict, gene_letter)
	question_text = get_question_text(gene_letter)
	full_question = background_text + octads_table + formula + question_text

	# Format question based on type
	if question_type == 'mc':
		choices_list, answer_text = make_choices(asci_count_dict)
		random.shuffle(choices_list)
		return bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
	else:
		important_tip_text = get_important_tips()
		return bptools.formatBB_NUM_Question(N, full_question + important_tip_text, distance, 0.1, tol_message=False)

#=====================
def parse_arguments():
	"""Parses command-line arguments for the script."""
	parser = argparse.ArgumentParser(description="Generate Neurospora genetics questions.")
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

	args = parser.parse_args()

	return args


#=====================
def main():
	"""Main function that handles argument parsing, question generation, and file writing."""
	args = parse_arguments()

	outfile = f'bbq-{os.path.splitext(os.path.basename(__file__))[0]}-{args.question_type.upper()}-questions.txt'
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			final_question = generate_question(N, args.question_type)
			if final_question:
				N += 1
				f.write(final_question)
	f.close()

	# Display histogram if question type is multiple choice
	if args.question_type == "mc":
		bptools.print_histogram()


#===========================================================
#===========================================================
if __name__ == "__main__":
	main()

#THE END
