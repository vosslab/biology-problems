#!/usr/bin/env python3

import random
import itertools

import bptools
import tetradlib
import genemaplib as gml
import phenotypes_for_yeast
import tetrad_solver_lib as tusl

#need this so students can add info to the box
bptools.allow_no_click_div = False
debug = False

DISTANCE_TRIPLETS: list[tuple[int, int, int]] = []
QUESTION_HEADER = ""
FOOTER_STEPS = ""
IMPORTANT_TIPS = ""
PHENOTYPE_DICT: dict = {}

#===========================================================
#===========================================================
def get_question_header():
	"""
	Returns the introductory context of the problem for unordered tetrad three-gene mapping.
	"""
	header = '<h5>Unordered Tetrad Three Gene Mapping</h5>'
	header += '<p>In this problem, you will use unordered tetrads to determine the order of three genes '
	header += 'and calculate the distances between them. The yeast <i>Saccharomyces cerevisiae</i> is used in this study. '
	header += 'A cross has been performed to study the linkage relationships among three genes, '
	header += 'and the resulting genotypes are summarized in the table below.</p>'
	if gml.is_valid_html(header) is False:
		print(header)
		raise ValueError
	return header

#===========================================================
#===========================================================
def get_question_setup(gene_letters_str):
	"""
	Generates the specific part of the question that depends on gene letters.

	Args:
		gene_letters_str (str): String containing gene letters, e.g., "akn".

	Returns:
		str: HTML formatted string with the dynamic question setup.
	"""
	setup = '<h6>Question</h6> '
	setup += '<p>Using the table above, determine the order of the genes and the distances between them. '
	setup += 'Once calculated, fill in the following four blanks: </p><ul>'
	#the gene letters ARE sorted, so this okay since it is not the gene order
	for gene1, gene2 in itertools.combinations(gene_letters_str.upper(), 2):
		setup += f'<li>The distance between genes {gene1} and {gene2} is [{gene1}{gene2}] cM ({gene1}{gene2})</li>'
	setup += '<li>From this, the correct order of the genes is [geneorder] (gene order).</li></ul>'
	if gml.is_valid_html(setup) is False:
		print(setup)
		raise ValueError
	return setup

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
	tips += '<li><i>Important Tip 3:</i> '
	tips += '  Your gene order answer should be written as three letters only, '
	tips += '  with no spaces, commas, hyphens, or other characters allowed. '
	tips += '  For example, if the gene order is B - A - C, simply write "bac" or "cab".</li>'
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
	steps += ' <li>Step 2: Pick any two genes and assign PD, NPD, TT.</li>'
	steps += ' <li>Step 3: Determine if the two genes are linked.</li>'
	steps += '  <ul><li>PD &gt;&gt; NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	steps += ' <li>Step 4: Determine the map distance between the two genes.</li>'
	steps += '  <ul><li>D = &half; (TT + 6 NPD) / total = (3 NPD + &half; TT) / total</li></ul>'
	steps += ' <li>Step 5: Go back to Step 2 and pick a new pair of genes until all pairs are complete.</li>'
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
def make_answer_map(gene_order_str, pair_distance_map):
	"""
	Creates a mapping of variable names to their associated distances and gene order.

	For a given gene order and a distance map, this function generates a dictionary where:
	- Each pairwise combination of genes (in alphabetical order) is mapped to a distance.
	- The full gene order is mapped to both its original and reversed versions.

	Args:
		gene_order_str (str): A string of gene letters, e.g., 'abc'.
		pair_distance_map (dict): A map like {'AB': 5, 'BC': 10, 'AC': 15}.

	Returns:
		dict: A dictionary with variable names as keys and distance or gene order as values.

	Example:
		>>> make_answer_map('abc', {'AB': 5, 'BC': 10, 'AC': 15})
		{
			'AB': [5],
			'BC': [10],
			'AC': [15],
			'geneorder': ['abc', 'cba']
		}
	"""
	# Initialize answer map with pairwise gene combinations
	answer_map = {
		create_pair_variable(gene_order_str[0], gene_order_str[1]): [
			str(pair_distance_map[create_pair_variable(gene_order_str[0], gene_order_str[1])])
		],
		create_pair_variable(gene_order_str[1], gene_order_str[2]): [
			str(pair_distance_map[create_pair_variable(gene_order_str[1], gene_order_str[2])])
		],
		create_pair_variable(gene_order_str[0], gene_order_str[2]): [
			str(pair_distance_map[create_pair_variable(gene_order_str[0], gene_order_str[2])])
		],
	}
	# Add the full gene order and its reverse as a separate entry
	answer_map['geneorder'] = [gene_order_str, gene_order_str[::-1]]
	return answer_map


#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate unordered tetrad three-gene mapping (distances + order) FIB+ questions."
	)
	args = parser.parse_args()
	return args

#=====================
def write_question(N: int, args) -> str | None:
	gene_letters_str = gml.get_gene_letters(3)
	question_setup = get_question_setup(gene_letters_str)
	phenotype_info_str = gml.get_phenotype_info(gene_letters_str, PHENOTYPE_DICT)

	gene_order_str = gml.get_random_gene_order(gene_letters_str)

	distances = sorted(random.choice(DISTANCE_TRIPLETS))
	while distances[1] > 26 and len(set(distances)) == 3:
		distances = sorted(random.choice(DISTANCE_TRIPLETS))
	if debug:
		print(f"Distances: {distances}")

	progeny_size = gml.get_general_progeny_size(distances) * 3

	progeny_tetrads_count_dict = tetradlib.construct_progeny_counts(
		gene_letters_str,
		gene_order_str,
		distances,
		progeny_size,
	)
	#Check if progeny_tetrads_count_dict are valid
	if tetradlib.check_if_progeny_counts_are_valid(progeny_tetrads_count_dict) is False:
		return None

	if debug:
		ascii_table = tetradlib.get_progeny_ascii_table(3, progeny_tetrads_count_dict, progeny_size)
		print(ascii_table)

	html_table = tetradlib.make_progeny_html_table(progeny_tetrads_count_dict, progeny_size)
	pair_distance_map, solved_gene_order_str, pair_details = (
		tusl.solve_unordered_tetrad_three_gene(progeny_tetrads_count_dict, gene_letters_str)
	)
	if debug:
		print(pair_details)

	observed_distances_sorted = sorted(pair_distance_map.values())
	expected_distances_sorted = sorted(distances)
	if observed_distances_sorted != expected_distances_sorted:
		if debug:
			print("Observed distances do not match expected distances.")
			print(f"observed={observed_distances_sorted} expected={expected_distances_sorted}")
		return None
	answer_map = make_answer_map(solved_gene_order_str, pair_distance_map)

	complete_question = QUESTION_HEADER + phenotype_info_str + html_table + question_setup
	complete_question += FOOTER_STEPS + IMPORTANT_TIPS
	return bptools.formatBB_FIB_PLUS_Question(N, complete_question, answer_map)

#=====================
#=====================
def main():
	args = parse_arguments()

	global DISTANCE_TRIPLETS
	global QUESTION_HEADER
	global FOOTER_STEPS
	global IMPORTANT_TIPS
	global PHENOTYPE_DICT

	DISTANCE_TRIPLETS = gml.get_all_distance_triplets(msg=debug)
	QUESTION_HEADER = get_question_header()
	FOOTER_STEPS = get_question_footer_steps()
	IMPORTANT_TIPS = get_important_tips()
	PHENOTYPE_DICT = phenotypes_for_yeast.phenotype_dict

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile, print_histogram_flag=False)

#===========================================================
#===========================================================
if __name__ == "__main__":
	main()
