#!/usr/bin/env python3

import os
import sys
import copy
import math
import random
import argparse
import itertools

import bptools
import tetradlib
import genemaplib as gml
import phenotypes_for_yeast

debug = True

#=====================
#=====================

#===========================================================
#===========================================================
def get_question_header():
	"""
	Returns the introductory context of the problem for unordered tetrad three-gene mapping.
	"""
	header = '<h5>Unordered Tetrad Three Gene Mapping</h5>'
	header += '<p>In this problem, you will use unordered tetrads to determine the between a single pair of genes '
	header += 'and calculate the distances between them. The yeast <i>Saccharomyces cerevisiae</i> is used in this study. '
	header += 'A cross has been performed to study the linkage relationships among three genes, '
	header += 'and the resulting genotypes are summarized in the table below.</p>'
	if gml.is_valid_html(header) is False:
		print(header)
		raise ValueError
	return header

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
	tips += '  Your calculated distance between the pair of genes should be a whole number. '
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

#===========================================================
#===========================================================
def get_question_footer_steps():
	"""
	Returns the HTML formatted step-by-step instructions for solving the problem.

	Returns:
		str: HTML formatted string with step-by-step instructions.
	"""
	steps = '<h6>Step-by-Step Instructions</h6>'
	steps += '<ul>'
	steps += ' <li>Step 1: Find the row for the Parental Type for all three genes.</li>'
	steps += ' <li>Step 2: Looking at only your two genes, assign PD, NPD, TT.</li>'
	steps += ' <li>Step 3: Determine if the two genes are linked.</li>'
	steps += '   <ul><li>PD &gt;&gt; NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	steps += ' <li>Step 4: Determine the map distance between the two genes.</li>'
	steps += '   <ul><li>D = &half; (TT + 6 NPD) / total = (3 NPD + &half; TT) / total</li></ul>'
	steps += '</ul>'
	if gml.is_valid_html(steps) is False:
		print(steps)
		raise ValueError
	return steps

#===========================================================
#===========================================================
def create_pair_variable(gene1, gene2):
	"""Helper function to create a variable name from two genes in alphabetical order."""
	return f"{min(gene1, gene2).upper()}{max(gene1, gene2).upper()}"

#===========================================================
#===========================================================
def make_answer_map(gene_order_str, distances):
	# Initialize answer map with pairwise gene combinations
	answer_map = {
		create_pair_variable(gene_order_str[0], gene_order_str[1]): [distances[0]],
		create_pair_variable(gene_order_str[1], gene_order_str[2]): [distances[1]],
		create_pair_variable(gene_order_str[0], gene_order_str[2]): [distances[2]],
	}
	return answer_map

#===========================================================
#===========================================================
def get_all_non_empty_subsets(input_list):
	# Generate all combinations of sizes 1 through len(input_list)
	all_subsets = []
	for r in range(1, len(input_list) + 1):
		all_subsets.extend(itertools.combinations(input_list, r))
	return all_subsets

#===========================================================
#===========================================================
#===========================================================
#===========================================================
def make_choices(progeny_tetrads_count_dict, gene_pair_distance, num_choices):
	"""
	Generates a list of possible answer choices for the genetic distance question.

	This function:
	1. Identifies the correct answer by calculating the recombinant fraction for the specified gene pair.
	2. Categorizes incorrect choices based on their rounding characteristics (integer, half-integer, fraction).
	3. Prioritizes integer choices first, then half-integers, and finally fraction choices to fill up the required number.

	Args:
		progeny_tetrads_count_dict (dict): Dictionary with genotype counts for different tetrad types.
		gene_pair_distance (float): The correct genetic distance for the gene pair, used to identify the correct answer.
		num_choices (int): Total number of choices to generate, including the correct answer.

	Returns:
		list: A list of formatted choices in HTML, including the correct answer.
		str: The correct answer as a formatted HTML string.

	Raises:
		ValueError: If the correct answer cannot be generated or if there are insufficient choices.
	"""

	# Calculate the total progeny count as the sum of all tetrad counts
	total_progeny_count = sum(progeny_tetrads_count_dict.values())

	# Organize progeny counts into Tetratype (TT) and Non-Parental Ditype (NPD) based on sorting.
	progeny_counts = sorted(progeny_tetrads_count_dict.values())
	tetratype_counts = progeny_counts[3:5]  # Middle two values for Tetratype (TT) counts
	npd_counts = progeny_counts[0:3]        # First three values for Non-Parental Ditype (NPD) counts

	# Dictionary to store categorized choices
	all_choices_map = {
		"int": {},         # Choices that round to integer centiMorgan values
		"tenth-int": {},    # Choices that round to half-integer centiMorgan values (e.g., 0.5, 1.5, etc.)
		"fraction": {}     # Choices that are fractional centiMorgan values
	}

	answer_text = None

	# Generate all non-empty subsets for Tetratype (TT) and Non-Parental Ditype (NPD) counts
	tt_subsets = get_all_non_empty_subsets(tetratype_counts)
	npd_subsets = get_all_non_empty_subsets(npd_counts)

	# Loop through all combinations of TT and NPD subsets to generate possible choices
	for tt_subset in tt_subsets:
		for npd_subset in npd_subsets:
			# Calculate the genetic distance and format it as an HTML string
			choice_text, decimal_distance = tetradlib.tetrad_calculation_string(
				list(tt_subset), list(npd_subset), total_progeny_count
			)

			# Convert distance to a bigger integer representing thousandths of a centiMorgan
			rounded_distance_key = int(round(decimal_distance * 10000 + 1e-6))

			# Check if this choice is the correct answer (within tolerance)
			if math.isclose(rounded_distance_key, gene_pair_distance * 100, abs_tol=0.0001):
				if answer_text is None:
					answer_text = choice_text
				else:
					print("Duplicate answer detected; this is unexpected.")
					return None, None
			else:
				# Classify the choice based on rounding characteristics
				if gml.is_almost_integer(decimal_distance * 100):
					all_choices_map["int"][rounded_distance_key] = choice_text
				elif gml.is_almost_integer(decimal_distance * 1000):
					all_choices_map["tenth-int"][rounded_distance_key] = choice_text
				else:
					all_choices_map["fraction"][rounded_distance_key] = choice_text

	# Ensure the correct answer was identified
	if answer_text is None:
		print(f"gene_pair_distance = {gene_pair_distance}")
		print(f"possible values = {list(all_choices_map['int'].keys())}")
		raise ValueError("Correct answer not found; this is unexpected.")

	# Debugging output to verify the distribution of choices
	print(f"Generated {len(all_choices_map['int'])} integer choices")
	print(f"Generated {len(all_choices_map['tenth-int'])} tenth-integer choices")
	print(f"Generated {len(all_choices_map['fraction'])} fractional choices")

	# Prioritize integer choices, then tenth-integer choices, and finally fraction choices
	remaining_choices_needed = num_choices - 1  # Subtract 1 for the correct answer

	# Step 1: Add integer choices
	if len(all_choices_map["int"]) >= remaining_choices_needed:
		choices_list = random.sample(list(all_choices_map["int"].values()), remaining_choices_needed)
	else:
		choices_list = list(all_choices_map["int"].values())
	remaining_choices_needed = num_choices - len(choices_list)  - 1

	# Step 2: Add tenth-integer choices if needed
	if remaining_choices_needed > 0:
		if len(all_choices_map["tenth-int"]) >= remaining_choices_needed:
			choices_list += random.sample(list(all_choices_map["tenth-int"].values()), remaining_choices_needed)
		else:
			choices_list += list(all_choices_map["tenth-int"].values())
	remaining_choices_needed = num_choices - len(choices_list)  - 1

	# Step 3: Add fraction choices if still needed
	if remaining_choices_needed > 0:
		if len(all_choices_map["fraction"]) >= remaining_choices_needed:
			choices_list += random.sample(list(all_choices_map["fraction"].values()), remaining_choices_needed)
		else:
			choices_list += list(all_choices_map["fraction"].values())
			# If there are still not enough choices, raise an error
			if len(choices_list) < num_choices - 1:
				raise ValueError("Insufficient choices to generate the required number of answers.")

	# Add the correct answer as the last item in the list
	choices_list.append(answer_text)
	random.shuffle(choices_list)

	return choices_list, answer_text

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

	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of choices to choose from in the question', default=5)

	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do', default=1
	)

	args = parser.parse_args()

	return args

#=====================
#=====================
def main():
	args = parse_arguments()

	# Load the distance triplets and question headers
	distance_triplet_list = gml.get_all_distance_triplets(msg=debug)
	question_header = get_question_header()
	footer_steps = get_question_footer_steps()
	fib_important_tips = get_important_tips()
	phenotype_dict = phenotypes_for_yeast.phenotype_dict

	# Define output file name
	outfile = (
		'bbq-' +
		os.path.splitext(os.path.basename(__file__))[0] +
		'-' +
		args.question_type.upper() +
		'-questions.txt'
		)
	print('Writing to file:', outfile)
	f = open(outfile, 'w')
	N = 1
	for _ in range(args.duplicates):
		gene_letters_str = gml.get_gene_letters(3)
		phenotype_info_str = gml.get_phenotype_info(gene_letters_str, phenotype_dict)

		gene_order_str = gml.get_random_gene_order(gene_letters_str)

		distances = sorted(random.choice(distance_triplet_list))
		while distances[1] > 26 and len(set(distances)) == 3:
			distances = sorted(random.choice(distance_triplet_list))
		if debug: print(f"Distances: {distances}")

		progeny_size = gml.get_general_progeny_size(distances) * 3

		progeny_tetrads_count_dict = tetradlib.construct_progeny_counts(gene_letters_str, gene_order_str, distances, progeny_size)
		if progeny_tetrads_count_dict is None:
			print("Question generation failed")
			print(f"Distances: {distances}")
			continue

		if len(set(progeny_tetrads_count_dict.values())) != 6:
			print("Question generation failed")
			print(f"Distances: {progeny_tetrads_count_dict.values()}")
			continue


		ascii_table = tetradlib.get_progeny_ascii_table(3, progeny_tetrads_count_dict, progeny_size)
		print(ascii_table)
		html_table = tetradlib.make_progeny_html_table(progeny_tetrads_count_dict, progeny_size)

		answer_map = make_answer_map(gene_order_str, distances)
		gene_pair_str, gene_pair_distances = random.choice(list(answer_map.items()))
		gene_pair_distance = gene_pair_distances[0]
		statement = f"<h5>Determine the distance between the two genes {gene_pair_str[0].upper()} and {gene_pair_str[1].upper()}</h5>"

		# Combine all parts of the question into a single HTML string
		full_question = question_header + phenotype_info_str + html_table + footer_steps
		# Format question based on type
		if args.question_type == 'mc':
			full_question = full_question + statement
			choices_list, answer_text = make_choices(progeny_tetrads_count_dict, gene_pair_distance, args.num_choices)
			if choices_list is None:
				continue
			final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
		else:
			full_question = full_question + fib_important_tips + statement
			print(f"gene_pair_distance = {gene_pair_distance}")
			final_question = bptools.formatBB_NUM_Question(N, full_question, gene_pair_distance, 0.1, tol_message=False)

		if final_question is not None:
			N += 1
			f.write(final_question)
		else:
			print("Question generation failed")
	f.close()

	# Display histogram if question type is multiple choice
	if args.question_type == "mc":
		bptools.print_histogram()


#===========================================================
#===========================================================
if __name__ == "__main__":
	main()
