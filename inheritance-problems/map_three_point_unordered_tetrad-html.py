#!/usr/bin/env python3

import os
import sys
import math
import random
import argparse
from itertools import combinations


import bptools
import genemaplib as gml
#import tetradlib

debug = True

def tetradSetToString(tetradSet):
	return '\t'.join(tetradSet)

def invertType(genotype, basetype):
	return gml.invert_genotype(genotype, basetype)

def flipGene(genotype, gene, basetype):
	return gml.flip_gene_by_letter(genotype, gene, basetype)

def set_gene_order(gene_letters_str):
	return gml.get_random_gene_order(gene_letters_str)

#=====================
def makeProgenyHtmlTable(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'
	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 400px; height: 220px;">'
	table += '<tr>'
	table += '  <th {0}>Set #</th>'.format(td_extra)
	table += '  <th colspan="4" {0}>Tetrad Genotypes</th>'.format(td_extra)
	table += '  <th {0}>Progeny<br/>Count</th>'.format(td_extra)
	table += '</tr>'
	for i,type in enumerate(alltypes):
		interheader = '</span></td><td {0}>{1}'.format(td_extra, span)
		html_type = type.strip().replace('\t', interheader)
		table += '<tr>'
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, i+1)
		table += ' <td {0}>{1}{2}</span></td>'.format(td_extra, span, html_type)
		table += ' <td {0}>{1}{2:d}</span></td>'.format(td_extra.replace('center', 'right'), span, typemap[type])
		table += '</tr>'
	table += '<tr>'
	table += '  <th colspan="5" {0}">TOTAL =</th>'.format(td_extra.replace('center', 'right'))
	table += '  <td {0}>{1:d}</td>'.format(td_extra.replace('center', 'right'), progeny_size)
	table += '</tr>'
	table += '</table>'
	return table

#=====================
def makeProgenyAsciiTable(progeny_tetrads_count_dict, progeny_size):
	alltypes = sorted(progeny_tetrads_count_dict.keys())
	table = ''
	for type in alltypes:
		table += ("{0}\t".format(type))
		table += ("{0:d}\t".format(progeny_tetrads_count_dict[type]))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table

#=====================
def construct_progeny_counts(gene_letters_str, gene_order_str, distances, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s - %d - %s"
		%(gene_order_str[0], distances[0], gene_order_str[1], distances[1], gene_order_str[2]))
	print(answerString)
	if debug is True: print("------------")

	if debug is True: print("determine double crossovers")
	doublecross = distances[0]*distances[1]/100.
	if debug is True: print("doublecross", doublecross*10, 'per 1000')

	if debug is True: print("determine parental type")
	types = ['++'+gene_letters_str[2], '+'+gene_letters_str[1]+'+', '+'+gene_letters_str[1]+gene_letters_str[2]]
	parental = random.choice(types)

	progeny_tetrads_count_dict = generateTypeCounts(parental, gene_order_str, distances, progeny_size, gene_letters_str)
	return progeny_tetrads_count_dict

#=====================
#=====================
def get_double_counts(distance_tuple, progeny_size_int):
	"""
	Calculates the counts of double crossover events for three gene distances.

	For a given progeny size and genetic distances between three pairs of genes, this function
	calculates the expected counts of double crossovers (DCOs) involving each gene pair, with
	an adjustment for the third distance to ensure consistent modeling of genetic linkage.

	Args:
		distance_tuple (tuple): Genetic distances between three gene pairs (e.g., (10, 20, 15)).
		progeny_size_int (int): Total number of progeny in the experiment.

	Returns:
		tuple: A tuple (dcount1, dcount2, dcount3) representing the counts of double crossovers
		for each gene pair.
	"""

	# Step 1: Estimate the initial double crossover count (DCO) between the first two gene pairs
	# Calculate the probability of a double crossover occurring between the first two genes.
	# `doublecross_prob` represents this probability, calculated by multiplying the probabilities
	# of individual crossovers between the first two gene pairs.
	doublecross_prob = (distance_tuple[0] / 100.0) * (distance_tuple[1] / 100.0)

	# Calculate the initial double crossover count as an integer, rounded from the expected float value.
	doublecount_float = doublecross_prob * progeny_size_int
	doublecount = int(round(doublecount_float + 1e-7))  # Adding a small epsilon to ensure correct rounding
	print(f"double counts = round({doublecount_float:.3f}) = {doublecount}")

	# Ensure the double crossover count is reasonable by setting a minimum threshold.
	# This avoids issues in calculations when the double crossover count is too low.
	if doublecount <= 4:
		print("Error: double crossover count is too small")
		raise ValueError("Double crossover count is too small for accurate calculation")
	if debug:
		print("Initial double crossover count:", doublecount)

	# Step 2: Determine dcount3 based on the third distance in `distance_tuple`
	# `dcount3` is calculated to ensure the third distance aligns with observed double crossovers.
	# This is derived from rearranging the formula for distance3:
	#   distance3 approx. (distance1 + distance2) - (6 * dcount3 / progeny_size * 100)
	# Solving for dcount3:
	dcount3 = ((distance_tuple[0] + distance_tuple[1] - distance_tuple[2]) * progeny_size_int) / 600
	dcount3 = int(dcount3)  # Convert to an integer for use in the final counts
	if debug:
		print("Final dcount3:", dcount3)

	# Step 3: Calculate counts for dcount1 and dcount2 based on random sampling ratios
	# Here, we distribute the remaining double crossovers (after accounting for dcount3)
	# between the first two gene pairs using squared distances as weights.

	# Calculate the squared distances for the first two gene pairs as a basis for probabilities.
	d00 = distance_tuple[0] ** 2  # Squared distance for the first gene pair
	d11 = distance_tuple[1] ** 2  # Squared distance for the second gene pair

	# Calculate the probabilities for dcount1 and dcount2 based on these squared distances
	total_cross_distance = float(d00 + d11)
	prob_dcount1 = d00 / total_cross_distance  # Probability of dcount1 events

	if debug:
		print(f"Probability of dcount1 = {prob_dcount1:.6f}")
		prob_dcount2 = d11 / total_cross_distance  # Probability of dcount2 events
		print(f"Probability of dcount2 = {prob_dcount2:.6f}")

	# Calculate dcount1 and dcount2 based on the total double crossover count minus dcount3.
	# This uses the calculated probabilities to partition the remaining double crossovers.
	dcount1 = int(round(prob_dcount1 * (doublecount - dcount3)))
	# Ensure that dcount1 + dcount2 + dcount3 = doublecount
	dcount2 = doublecount - dcount3 - dcount1

	if debug:
		print("Final double crossover counts - dcount1:", dcount1, "dcount2:", dcount2, "dcount3:", dcount3)

	return dcount1, dcount2, dcount3

def make_ditype_from_genotype_str(genotype_str, gene_letters_str):
	invert_str = gml.invert_genotype(genotype_str, gene_letters_str)
	ditype_tetrad = sorted([genotype_str, genotype_str, invert_str, invert_str])
	return '\t'.join(ditype_tetrad)
	return tuple(ditype_tetrad)

def make_tetratype_from_genotype_strings(genotype_str1, genotype_str2, gene_letters_str):
	invert_str1 = gml.invert_genotype(genotype_str1, gene_letters_str)
	invert_str2 = gml.invert_genotype(genotype_str2, gene_letters_str)
	tetratype_tetrad = sorted([genotype_str1, genotype_str2, invert_str1, invert_str2])
	return '\t'.join(tetratype_tetrad)
	return tuple(tetratype_tetrad)

#=====================
#===========================================================
def generateTypeCounts(parental_genotype_str, gene_order_str, distance_tuple, progeny_size_int, gene_letters_str):
	"""
	Generates counts for different types of tetrads based on genetic distances.

	This function calculates the expected numbers of each type of tetrad:
	Parental Ditype (PD), Non-Parental Ditype (NPD), and Tetratype (TT).
	The calculations are based on given crossover distances and total progeny size.

	Args:
		parental_genotype_str (str): The parental genotype as a string (e.g., '++' or 'ab').
		gene_order_str (str): The order of genes as a string (e.g., 'abc').
		distance_tuple (tuple): A tuple of genetic distances between gene pairs (e.g., (5, 10, 15)).
		progeny_size_int (int): The total number of progeny.
		gene_letters_str (str): A string containing gene letters for generating inverted types (e.g., 'ab').

	Returns:
		dict: A dictionary with tetrad configurations as keys and their counts as values.

	Example Output:
		{
			'PD': 450,
			'TT': 300,
			'NPD1': 50,
			'NPD2': 50,
			'NPD3': 50
		}

	Notes:
		- PD: Parental Ditype
		- TT: Tetratype (single crossover)
		- NPD: Non-Parental Ditype (double crossover)
	"""

	# Step 1: Calculate counts for double crossovers based on distances and progeny size
	# dcount1, dcount2, and dcount3 represent the number of double crossovers for each gene pair.
	dcount1, dcount2, dcount3 = get_double_counts(distance_tuple, progeny_size_int)
	double_count_total = dcount1 + dcount2 + dcount3  # Total double crossover events

	# Step 2: Calculate counts for single crossovers involving the first and second genes
	# Each single crossover count is derived from the genetic distance for each gene pair.
	# The formula adjusts for the fact that double crossovers also impact these counts.
	firstcount = 2 * (int(round(distance_tuple[0] * progeny_size_int / 100.)) - 3 * (dcount1 + dcount3))
	secondcount = 2 * (int(round(distance_tuple[1] * progeny_size_int / 100.)) - 3 * (dcount2 + dcount3))

	# Calculate the count of parental types by subtracting the counts of crossovers from total progeny
	parentcount = progeny_size_int - double_count_total - firstcount - secondcount

	# Step 3: Adjust the third distance to fit the calculated progeny counts
	# This recalculation ensures that the observed counts are consistent with the genetic model.
	calc_distance3 = 0.5 * (firstcount + secondcount + 6 * (double_count_total - dcount3))
	calc_distance3 = round(calc_distance3 / progeny_size_int * 100, 4)  # Convert to percentage

	# Step 4: Validation checks to ensure calculated counts are within expected ranges
	if debug:
		print(f"Expected   DISTANCE 3: {distance_tuple[2]:d}")
		print(f"Calculated DISTANCE 3: {calc_distance3:.5f}")
	# Check if calculated distance3 is close to the expected distance3 within tolerance
	if not math.isclose(distance_tuple[2], calc_distance3, abs_tol=1e-6):
		raise ValueError("Calculated distance is not close to the expected distance.")
	if firstcount <= 0 or secondcount <= 0:
		print("Error: Negative or zero single crossover counts due to too many double crossovers.")
		return None
	if firstcount >= parentcount:
		print("Error: Tetratype count is larger than Parental Type count.")
		return None
	if secondcount >= parentcount:
		print("Error: Tetratype count is larger than Parental Type count.")
		return None

	# Step 5: Initialize dictionary to store tetrad configurations and their counts
	progeny_tetrads_count_dict = {}

	# Step 6: Create and add the Parental Ditype (PD) tetrad to the count dictionary
	parental_tetrad = make_ditype_from_genotype_str(parental_genotype_str, gene_letters_str)
	progeny_tetrads_count_dict[parental_tetrad] = parentcount
	if debug:
		print("Parental Tetrad:", parental_tetrad)

	# Step 7: Generate Tetratype (TT) and Non-Parental Ditype (NPD) based on the first gene flip
	# Flip the first gene in gene_order to generate a single crossover configuration
	first_flip = flipGene(parental_genotype_str, gene_order_str[0], gene_letters_str)

	# Tetratype (TT) tetrad for first flip
	tt_tetrad = make_tetratype_from_genotype_strings(first_flip, parental_genotype_str, gene_letters_str)
	progeny_tetrads_count_dict[tt_tetrad] = firstcount

	# Non-Parental Ditype (NPD) for first flip
	npd_tetrad_1 = make_ditype_from_genotype_str(first_flip, gene_letters_str)
	progeny_tetrads_count_dict[npd_tetrad_1] = dcount1

	# Step 8: Generate Tetratype (TT) and Non-Parental Ditype (NPD) based on the second gene flip
	# Flip the second gene in gene_order to generate another single crossover configuration
	second_flip = flipGene(parental_genotype_str, gene_order_str[2], gene_letters_str)

	# Tetratype (TT) tetrad for second flip
	tt_tetrad_2 = make_tetratype_from_genotype_strings(second_flip, parental_genotype_str, gene_letters_str)
	progeny_tetrads_count_dict[tt_tetrad_2] = secondcount

	# Non-Parental Ditype (NPD) for second flip
	npd_tetrad_2 = make_ditype_from_genotype_str(second_flip, gene_letters_str)
	progeny_tetrads_count_dict[npd_tetrad_2] = dcount2

	# Step 9: Generate Non-Parental Ditype (NPD) based on both first and second gene flips
	# Flip both the middle gene to simulate a double crossover configuration
	double_flip = flipGene(parental_genotype_str, gene_order_str[1], gene_letters_str)

	# Non-Parental Ditype (NPD) for double flip: [double_flip, inverted(double_flip), double_flip, inverted(double_flip)]
	npd_double_flip_tetrad = make_ditype_from_genotype_str(double_flip, gene_letters_str)
	progeny_tetrads_count_dict[npd_double_flip_tetrad] = dcount3

	# Final validation: Ensure we have exactly 6 unique tetrad configurations
	if len(progeny_tetrads_count_dict) != 6:
		raise ValueError("Expected 6 unique tetrad configurations, but got a different number.")

	return progeny_tetrads_count_dict


#=====================
def questionText(gene_letters_str):
	question_string = '<h6>Unordered Tetrad Three Gene Mapping</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among three genes. '
	question_string += '<p>Using the table, determine the order of the genes and the distances between them. '
	question_string += 'Once calculated, fill in the following four blanks: </p><ul>'
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(gene_letters_str[0].upper(),gene_letters_str[1].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(gene_letters_str[0].upper(),gene_letters_str[2].upper())
	question_string += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(gene_letters_str[1].upper(),gene_letters_str[2].upper())
	question_string += '<li>From this the correct order of the genes is [geneorder] (gene order).</li></ul>'
	question_string += '<p><i>Hint 1:</i> ALL gene distances will be whole numbers, '
	question_string += ' do NOT enter a decimal; if you have a decimal your calculations are wrong.</p>'
	question_string += '<p><i>Hint 2:</i> enter your answer in the blank using only letters or numbers '
	question_string += ' with no spaces or commas. Also, do NOT add units, e.g. cM or m.u.</p>'
	question_string += '<ul>'
	question_string += '<li>Step 1: Find the Row for the Parental Type for all three genes.</li>'
	question_string += '<li>Step 2: Pick any two genes and assign PD, NPD, TT</li>'
	question_string += '<li>Step 3: Determine if the two genes are linked.</li>'
	question_string += '<ul><li>PD >> NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	question_string += '<li>Step 4: Determine the map distance between the two genes</li>'
	question_string += '<ul><li>D = &half; (TT + 6 NPD)/total = (3 NPD + &half;TT)/total</li></ul>'
	question_string += '<li>Step 5: Go to Step 2 and pick a new pair of genes until all pairs are complete.</li>'
	question_string += '</ul>'

	return question_string

#=====================
def create_pair_variable(gene1, gene2):
	"""Helper function to create a variable name from two genes in alphabetical order."""
	return f"{min(gene1, gene2).upper()}{max(gene1, gene2).upper()}"

#=====================
def make_answer_map(gene_order_str, distances):
	"""
	Creates a mapping of variable names to their associated distances and gene order.

	For a given gene order and a list of distances, this function generates a dictionary where:
	- Each pairwise combination of genes (in alphabetical order) is mapped to a distance.
	- The full gene order is mapped to both its original and reversed versions.

	Args:
		gene_order_str (str): A string of gene letters, e.g., 'abc'.
		distances (list): A list of distances between each pair of genes, e.g., [5, 10, 15].

	Returns:
		dict: A dictionary with variable names as keys and distance or gene order as values.

	Example:
		>>> make_answer_map('abc', [5, 10, 15])
		{
			'AB': [5],
			'BC': [10],
			'AC': [15],
			'geneorder': ['abc', 'cba']
		}
	"""
	# Initialize answer map with pairwise gene combinations
	answer_map = {
		create_pair_variable(gene_order_str[0], gene_order_str[1]): [distances[0]],
		create_pair_variable(gene_order_str[1], gene_order_str[2]): [distances[1]],
		create_pair_variable(gene_order_str[0], gene_order_str[2]): [distances[2]],
	}
	# Add the full gene order and its reverse as a separate entry
	answer_map['geneorder'] = [gene_order_str, gene_order_str[::-1]]
	return answer_map

#=====================
def get_question_header():
	"""
	Returns the introductory context of the problem for unordered tetrad three-gene mapping.
	"""
	header = '<h5>Unordered Tetrad Three Gene Mapping</h5>'
	header += '<p>In this problem, you will use unordered tetrads to determine the order of three genes '
	header += 'and calculate the distances between them. The yeast <i>Saccharomyces cerevisiae</i> is used in this study. '
	header += 'A cross has been performed to study the linkage relationships among three genes, and the resulting genotypes are summarized in the table below.</p>'
	return header

#=====================
def get_question_setup(gene_letters_str):
	"""
	Generates the specific part of the question that depends on gene letters.

	Args:
		gene_letters_str (str): String containing gene letters, e.g., "akn".

	Returns:
		str: HTML formatted string with the dynamic question setup.
	"""
	setup = '<h6>Enter Your Answers Here</h6>'
	setup += '<p>Using the table, determine the order of the genes and the distances between them. '
	setup += 'Once calculated, fill in the following four blanks: </p><ul>'
	setup += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(
		gene_letters_str[0].upper(), gene_letters_str[1].upper())
	setup += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(
		gene_letters_str[0].upper(), gene_letters_str[2].upper())
	setup += '<li>The distance between genes {0} and {1} is [{0}{1}] cM ({0}{1})</li>'.format(
		gene_letters_str[1].upper(), gene_letters_str[2].upper())
	setup += '<li>From this, the correct order of the genes is [geneorder] (gene order).</li></ul>'
	return setup

#=====================
def get_question_footer_tips():
	"""
	Returns the HTML formatted hints for solving the problem.

	Returns:
		str: HTML formatted string with hints.
	"""
	tips = '<h6>Hints</h6>'
	tips += '<p><ul>'
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
	tips += '</ul></p>'
	return tips

#=====================
def get_question_footer_steps():
	"""
	Returns the HTML formatted step-by-step instructions for solving the problem.

	Returns:
		str: HTML formatted string with step-by-step instructions.
	"""
	steps = '<h6>Step-by-Step Instructions</h6>'
	steps += '<ul>'
	steps += '<li>Step 1: Find the row for the Parental Type for all three genes.</li>'
	steps += '<li>Step 2: Pick any two genes and assign PD, NPD, TT.</li>'
	steps += '<li>Step 3: Determine if the two genes are linked.</li>'
	steps += '<ul><li>PD &gt;&gt; NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	steps += '<li>Step 4: Determine the map distance between the two genes.</li>'
	steps += '<ul><li>D = &half; (TT + 6 NPD) / total = (3 NPD + &half; TT) / total</li></ul>'
	steps += '<li>Step 5: Go back to Step 2 and pick a new pair of genes until all pairs are complete.</li>'
	steps += '</ul>'
	return steps

#=====================
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='number of duplicate runs to do', default=1)
	args = parser.parse_args()

	# Load the distance triplets and question headers
	distance_triplet_list = gml.get_all_distance_triplets(msg=debug)
	question_header = get_question_header()
	footer_steps = get_question_footer_steps()
	footer_tips = get_question_footer_tips()

	# Define output file name
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('Writing to file:', outfile)
	f = open(outfile, 'w')
	N = 1

	for i in range(args.duplicates):
		gene_letters_str = gml.get_gene_letters(3)
		question_setup = get_question_setup(gene_letters_str)
		phenotype_info_str = gml.get_phenotype_info(gene_letters_str, organism="S. cerevisiae")

		gene_order_str = set_gene_order(gene_letters_str)

		distances = sorted(random.choice(distance_triplet_list))
		while distances[1] > 26 and len(set(distances)) == 3:
			distances = sorted(random.choice(distance_triplet_list))
		if debug: print(f"Distances: {distances}")

		progeny_size = gml.get_general_progeny_size(distances) * 3

		progeny_tetrads_count_dict = construct_progeny_counts(gene_letters_str, gene_order_str, distances, progeny_size)
		if progeny_tetrads_count_dict is None:
			print("Question generation failed")
			print(f"Distances: {distances}")
			continue

		ascii_table = makeProgenyAsciiTable(progeny_tetrads_count_dict, progeny_size)
		print(ascii_table)
		html_table = makeProgenyHtmlTable(progeny_tetrads_count_dict, progeny_size)
		answer_map = make_answer_map(gene_order_str, distances)

		# Combine all parts of the question into a single HTML string
		complete_question = question_header + phenotype_info_str + html_table + question_setup + footer_steps + footer_tips
		final_question = bptools.formatBB_FIB_PLUS_Question(N, complete_question, answer_map)

		if final_question is not None:
			N += 1
			f.write(final_question)
		else:
			print("Question generation failed")

	f.close()

if __name__ == "__main__":
	main()
