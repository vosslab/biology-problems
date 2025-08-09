#!/usr/bin/env python3

import os
import re
import sys
import copy
import time
import random
import argparse
import colorsys

#local
import bptools
bptools.use_add_no_click_div = False
bptools.use_insert_hidden_terms = False

from treelib import tools
from treelib import lookup

debug = True

cache_all_treecode_cls_list = []

#===========================================================
#===========================================================
def rgb_to_hex(rgb1):
	"""
	Convert an RGB color (in float format) to a hexadecimal color string.

	Args:
		rgb1 (tuple): A tuple of three floats (R, G, B) where each value is in the range [0, 1].

	Returns:
		str: A hexadecimal string representing the RGB color, in the format `#RRGGBB`.
	"""
	# Scale the RGB values from the range [0, 1] to [0, 255].
	rgb256 = tuple([int(i * 255) for i in rgb1])

	# Convert the scaled RGB values to a hexadecimal color string.
	return '#%02x%02x%02x' % rgb256

#===========================================================
#===========================================================
def distance_to_html_color(distance, distance_list):
	"""
	Map a distance value to an HTML color, transitioning from one color to another based on the range of distances.

	Args:
		distance (float): The specific distance value to map to a color.
		distance_list (list): A list of all distance values, used to determine the range (min and max distances).

	Returns:
		str: A hexadecimal string representing the HTML color corresponding to the distance value.
	"""
	# Extract the minimum and maximum distances from the sorted distance list.
	min_dist = distance_list[0]
	max_dist = distance_list[-1]

	# Calculate the fraction of the distance range that the current distance represents.
	# A smaller distance will correspond to a higher fraction_diff.
	fraction_diff = (max_dist - distance) / float(max_dist - min_dist)

	# Divide the fraction_diff by 3.0 to determine the color angle in the HSV color space.
	# This restricts the color range (e.g., hue) for better visualization.
	angle = fraction_diff / 3.0

	# Convert the HSV color (angle, saturation, value) to RGB.
	# Hue is determined by the angle, saturation is 0.20 for a pastel effect, and value is near 1.0 for brightness.
	rgb1 = colorsys.hsv_to_rgb(angle, 0.05, 1.0)

	# Convert the RGB values to a hexadecimal HTML color.
	html_hex = rgb_to_hex(rgb1)

	# Return the hexadecimal color string for use in HTML.
	return html_hex

#===========================================================
#===========================================================
def make_random_distance_list(num_distances: int) -> list:
	"""
	Generates a sorted list of unique random distances.
	The function creates a list of random even integers such that:
	- Each distance is at least 8 units apart from any other.
	- The random distances are bounded by `2` and `num_distances * multiplier`.
	"""
	# Initialize the list of distances
	distances = []
	# Define the bounds for random number generation
	lower_bound = 2
	upper_bound = 12
	common_divisor = 2
	while len(distances) < num_distances:
		# Generate a random even number within the current bounds
		scaled_lower_bound = lower_bound // common_divisor
		scaled_upper_bound = upper_bound // common_divisor
		random_distance = random.randint(scaled_lower_bound, scaled_upper_bound) * common_divisor
		# Append the new distance
		#print(f"LB={lower_bound}, UB={upper_bound}, R={random_distance}")
		distances.append(random_distance)
		# Update bounds based on the latest valid distance
		lower_bound = max(distances) + 8
		upper_bound = lower_bound + 10
	# Return the sorted list of distances
	return sorted(distances)

#===========================================================
#===========================================================
def get_highest_number(substring):
	"""
	Extracts the highest number from a string of alphanumeric and parenthesis characters.
	"""
	# Use a regex to find all numeric substrings
	numbers = re.findall(r'\d+', substring)
	# Convert the matches to integers
	int_numbers = list(map(int, numbers))
	# Return the maximum number, or -1 if the list is empty
	return max(int_numbers, default=-1)

#===========================================================
#===========================================================
def map_taxon_distances(ordered_taxa, distance_list, treecode_cls):
	"""
	Maps distances between taxon pairs using their positions in the tree.

	This function computes distances between all pairs of taxa based on their
	connecting internal node numbers (derived from the tree structure). It uses
	the provided distance list to determine the distance for each node.

	Args:
		ordered_taxa (list): A list of taxa in the order they appear in the tree.
		distance_list (list): A list of distances corresponding to internal nodes.
		tree_code_str (str): A string representing the tree structure, where taxa
			are represented by alphabetic characters and internal nodes by numbers.

	Returns:
		dict: A dictionary mapping tuples of taxon pairs to their corresponding
			distances, with keys as `(taxon1, taxon2)` and `(taxon2, taxon1)`.
	"""
	# Initialize a dictionary to store distances between taxon pairs
	treecode_distance_map = treecode_cls.distance_map
	#print(treecode_cls.tree_code_str)
	#print(treecode_distance_map)
	taxa_distance_map = {}
	# Loop through all pairs of taxa
	for pair_tuple, distance_int in treecode_distance_map.items():
		swap_tuple = (pair_tuple[1], pair_tuple[0])
		distance_index = distance_int - 1
		taxa_distance_map[pair_tuple] = distance_list[distance_index]
		taxa_distance_map[swap_tuple] = distance_list[distance_index]
	#print(taxa_distance_map)
	return taxa_distance_map

#===========================================================
#===========================================================
def add_distance_pair_shifts(distance_dict, ordered_taxa, answer_treecode_cls):
	answer_code = answer_treecode_cls.tree_code_str
	shift_list = [-2,2]
	for n in range(len(ordered_taxa)-2):
		shift_list.append(0)
	shift_list.sort()
	for i,taxa1 in enumerate(ordered_taxa):
		for j,taxa2 in enumerate(ordered_taxa):
			if i == j:
				continue
			for k,taxa3 in enumerate(ordered_taxa):
				if j == k or i == k:
					continue
				# i > j > k OR k < j < i
				max_node_1_2 = tools.find_node_number_for_taxa_pair(answer_code, taxa1, taxa2)
				max_node_2_3 = tools.find_node_number_for_taxa_pair(answer_code, taxa2, taxa3)
				max_node_1_3 = tools.find_node_number_for_taxa_pair(answer_code, taxa1, taxa3)

				if max_node_2_3 == max_node_1_3 and max_node_1_2 < max_node_1_3:
					shift = random.choice(shift_list)
					distance_dict[(taxa1, taxa3)] += shift
					distance_dict[(taxa3, taxa1)] += shift
					distance_dict[(taxa2, taxa3)] -= shift
					distance_dict[(taxa3, taxa2)] -= shift
	return distance_dict

#===========================================================
#===========================================================
def print_ascii_distance_table(ordered_taxa, distance_dict):
	"""
	Print a formatted ASCII table with Unicode borders for the taxa distance matrix.

	Args:
		ordered_taxa (list): The ordered list of taxa names.
		distance_dict (dict): A dictionary mapping taxa pairs to distances.
	"""
	# Sort the taxa names for consistent row/column order
	sorted_taxa = list(copy.copy(ordered_taxa))
	sorted_taxa.sort()

	# Calculate the column width dynamically for consistent alignment
	column_width = 5

	# Unicode characters for table borders
	horizontal_line = "\u2500"
	vertical_line = "\u2502"
	top_left_corner = "\u250C"
	top_right_corner = "\u2510"
	bottom_left_corner = "\u2514"
	bottom_right_corner = "\u2518"
	middle_top = "\u252C"
	middle_bottom = "\u2534"
	middle_left = "\u251C"
	middle_right = "\u2524"
	center_cross = "\u253C"

	# Create the table borders
	# Top border with column headers
	top_border = f"{top_left_corner}{horizontal_line * column_width}"
	for _ in sorted_taxa:
		top_border += f"{middle_top}{horizontal_line * column_width}"
	top_border += f"{top_right_corner}\n"

	# Separator for headers and rows
	separator = f"{middle_left}{horizontal_line * column_width}"
	for _ in sorted_taxa:
		separator += f"{center_cross}{horizontal_line * column_width}"
	separator += f"{middle_right}\n"

	# Bottom border
	bottom_border = f"{bottom_left_corner}{horizontal_line * column_width}"
	for _ in sorted_taxa:
		bottom_border += f"{middle_bottom}{horizontal_line * column_width}"
	bottom_border += f"{bottom_right_corner}\n"

	# Generate the table header
	header = f"{vertical_line}{' ' * column_width}" # Empty top-left corner
	for taxa in sorted_taxa:
		header += f"{vertical_line}  {taxa}  "
	header += f"{vertical_line}\n"

	# Start assembling the ASCII table
	ascii_table = top_border + header + separator

	# Generate the rows
	for taxa1 in sorted_taxa:
		# Row label
		row = f"{vertical_line}  {taxa1}  "
		for taxa2 in sorted_taxa:
			if taxa1 == taxa2:
				cell_value = "---" # Self-distance marked with 'x'
			else:
				# Retrieve the distance value
				distance = distance_dict.get((taxa1, taxa2), 0)
				cell_value = f"{distance}"
			# Add the cell value, centered in the column
			row += f"{vertical_line} {cell_value.rjust(column_width-2)} "
		row += f"{vertical_line}\n"
		ascii_table += row + separator

	# Replace the last separator with the bottom border
	ascii_table = ascii_table[:-len(separator)] + bottom_border

	# Print the final table to stderr
	sys.stderr.write(ascii_table)

#===========================================================
#===========================================================
def generate_html_distance_table(sorted_taxa, distance_dict, answer_treecode_cls):
	"""
	Generate an HTML table for a distance matrix with taxa as rows and columns.

	Args:
		sorted_taxa (list): alphabetically sorted list of taxa names.
		distance_dict (dict): A dictionary mapping taxa pairs to distances.

	Returns:
		str: An HTML string representing the distance matrix as a table.
	"""
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: large;">'

	font_colors = answer_treecode_cls.output_cls.font_colors
	background_colors = answer_treecode_cls.output_cls.background_colors
	taxa_name_map = answer_treecode_cls.output_cls.taxa_name_map

	# Start the table and add the header row
	width = 120 * (len(sorted_taxa) + 1) + 10
	height = 45 * (len(sorted_taxa) + 1) + 10
	htmL_table = '<table style="border-collapse: collapse; border: 2px solid black; '
	htmL_table += f'width: {width}px; height: {height}px">'
	htmL_table +=  (
		'<caption style="caption-side:bottom">'
		f'{len(sorted_taxa)} taxa &times; {len(sorted_taxa)} taxa distance matrix'
		'</caption>'
	)
	for _ in range(len(sorted_taxa) + 1):
		htmL_table += '<colgroup width="100"/>'
	htmL_table += '<tr>'
	htmL_table += f'<td {td_extra}>taxa</td>'
	for taxon in sorted_taxa:
		font_color = font_colors.get(taxon.lower(), 'black')
		bg_color = background_colors.get(taxon.lower(), '#f3f3f3')
		taxon_name = taxa_name_map.get(taxon.lower(), taxon)
		th_extra = td_extra + f' bgcolor="{bg_color}"'
		taxon_span = f'<span style="font-size: large; color: {font_color};">'
		htmL_table += f'<th {th_extra}>{taxon_span}{taxon_name}</span></th>'
	htmL_table += '</tr>'

	distance_list = sorted(distance_dict.values())
	# Add rows for each taxa
	for taxa1 in sorted_taxa:
		htmL_table += '<tr>'
		font_color = font_colors.get(taxa1.lower(), 'black')
		bg_color = background_colors.get(taxa1.lower(), '#f3f3f3')
		taxon_name = taxa_name_map.get(taxa1.lower(), taxa1)
		taxon_span = f'<span style="font-size: large; color: {font_color};">'
		htmL_table += f'<th bgcolor="{bg_color}" {td_extra} >{taxon_span}{taxon_name}</span></th>'
		for taxa2 in sorted_taxa:
			if taxa1 == taxa2:
				# Self-distance is represented by gray cells
				my_td_extra = td_extra + ' bgcolor="DarkGray"'
				htmL_table += f'<td {my_td_extra}>&times;</td>'
			else:
				# Use distance to calculate color and add the value
				distance = distance_dict[(taxa1, taxa2)]
				hex_color = distance_to_html_color(distance, distance_list)
				my_td_extra = td_extra + f' bgcolor="{hex_color}"'
				htmL_table += f'<td {my_td_extra}>{span}{distance}</span></td>'
		htmL_table += '</tr>'

	# Close the table
	htmL_table += '</table>'
	tools.is_valid_html(htmL_table)
	return htmL_table

#===========================================================
#===========================================================
def get_problem_statement(sorted_taxa, distance_dict, answer_treecode_cls):
	font_colors = answer_treecode_cls.output_cls.font_colors
	#background_colors = answer_treecode_cls.output_cls.background_colors
	taxa_name_map = answer_treecode_cls.output_cls.taxa_name_map

	#named_taxa = [taxa_name_map.get(taxon.lower(), taxon) for taxon in sorted_taxa]
	colored_taxa = [f'<span style="color: {font_colors.get(taxon.lower(), "black")};">{taxa_name_map.get(taxon.lower(), taxon)}</span>' for taxon in sorted_taxa]

	# Add the descriptive question statement
	taxon1 = sorted_taxa[0]
	taxon2 = sorted_taxa[1]
	taxon3 = sorted_taxa[2]
	problem_statement = (
		"<p><span style='font-size: large;'>"
		"The table above represents a distance matrix for the following taxa: "
		f"{', '.join(f'<b>{taxon_name}</b>' for taxon_name in colored_taxa)}. "
		"The values in the matrix correspond to the genetic distances "
		"between pairs of taxa.</span></p> "
		"<p><span style='font-size: large;'>For example, "
		f"{taxa_text(taxon1, taxon2, distance_dict, taxa_name_map, font_colors)}. "
		"Distances are symmetric, meaning that both "
		f"{taxa_text(taxon2, taxon3, distance_dict, taxa_name_map, font_colors)} and "
		f"{taxa_text(taxon3, taxon2, distance_dict, taxa_name_map, font_colors)}.</span></p>"
		"<p><span style='font-size: large;'>Using this distance matrix, determine the most appropriate gene tree that "
		"accurately reflects the relationships and distances between these taxa.</span></p>"
	)
	tools.is_valid_html(problem_statement)
	return problem_statement

#===========================================================
#===========================================================
def taxa_text(taxon1, taxon2, distance_dict, taxa_name_map, font_colors):
	span1 = f'<span style="color: {font_colors.get(taxon1.lower(), "black")};">'
	span2 = f'<span style="color: {font_colors.get(taxon2.lower(), "black")};">'
	taxon1_formatted = f'{span1}<b>taxon {taxa_name_map.get(taxon1.lower(), taxon1)}</b></span>'
	taxon2_formatted = f'{span2}<b>taxon {taxa_name_map.get(taxon2.lower(), taxon2)}</b></span>'

	taxa_string = (
		f"the distance between {taxon1_formatted} and "
		f"{taxon2_formatted} is "
		f"<b>{distance_dict[(taxon1, taxon2)]}</b>"
	)
	return taxa_string

#===========================================================
#===========================================================
def get_multiple_choices(ordered_taxa, num_choices):
	num_leaves = len(ordered_taxa)
	#===========================================
	# GET ALL POSSIBLE GENE TREES
	#===========================================
	if debug: print("starting get_multiple_choices()")
	base_treecode_cls = lookup.get_random_base_tree_code_for_leaf_count(num_leaves)
	pre_answer_treecode_cls = lookup.get_random_inner_node_permutation_from_tree_code(base_treecode_cls)
	if debug: pre_answer_treecode_cls.print_ascii_tree()

	global cache_all_treecode_cls_list
	if len(cache_all_treecode_cls_list) == 0:
		if debug: print("calculating all_permuted_tree_codes")
		all_treecode_cls_list = lookup.get_all_taxa_permuted_tree_codes_for_leaf_count(num_leaves)
		if debug: print("shuffling all_permuted_tree_codes")
		random.shuffle(all_treecode_cls_list)
		purge_start = time.time()
		if debug: print("purgine duplicates")
		unique_treecode_cls_list = list(set(all_treecode_cls_list))
		if time.time() - purge_start > 10:
			if debug: print(f"done purging duplicates in {time.time() - purge_start:.1f} seconds")
			if debug: print(f"unique {len(unique_treecode_cls_list)} treecodes, down from all {len(all_treecode_cls_list)}")
		cache_all_treecode_cls_list = copy.copy(unique_treecode_cls_list)
	else:
		if debug: print("loading unique_treecode_cls_list")
		unique_treecode_cls_list = copy.copy(cache_all_treecode_cls_list)

	sorted_treecode_cls_list = lookup.sort_treecodes_by_taxa_distances(unique_treecode_cls_list, pre_answer_treecode_cls)
	if debug: print(f"sorted {len(sorted_treecode_cls_list)} treecodes, down from unique {len(unique_treecode_cls_list)}")

	replaced_treecode_cls_list = []
	for treecode_cls in sorted_treecode_cls_list[:num_choices-1]:
		permuted_treecode_cls = lookup.get_random_inner_node_permutation_from_tree_code(treecode_cls)
		replaced_treecode_cls = lookup.replace_taxa_letters(permuted_treecode_cls, ordered_taxa)
		replaced_treecode_cls_list.append(replaced_treecode_cls)

	answer_treecode_cls = lookup.replace_taxa_letters(pre_answer_treecode_cls, ordered_taxa)
	if debug:
		print(f"answer_treecode = {answer_treecode_cls.tree_code_str}")
		answer_treecode_cls.print_ascii_tree()

	return replaced_treecode_cls_list, answer_treecode_cls

#===========================================================
#===========================================================
def make_question(N: int, num_leaves: int, num_choices: int) -> str:
	"""
	Generate a multiple-choice question about gene trees based on a distance matrix.

	Args:
		N (int): A unique identifier for the question.
		num_leaves (int): The number of leaves (taxa) in the gene tree.
		num_choices (int): The total number of answer choices, including the correct one.

	Returns:
		str: A formatted HTML multiple-choice question that includes a species distance matrix
			and a list of possible gene tree answers.
	"""
	# Initialize the GeneTree object for tree generation and manipulation

	# Generate taxa names (letters) with "clear" letters (excluding ambiguous ones like 'o' or 'i')
	taxa_letters_str = bptools.generate_gene_letters(num_leaves, clear=True)
	# Sort the taxa letters alphabetically
	sorted_taxa = sorted(taxa_letters_str)

	#===========================================
	# FIND A PARTICULAR ORDER FOR THE TAXA
	#===========================================
	# Get all permutations of the sorted taxa letters and shuffle them randomly
	all_taxa_permutations = tools.get_comb_safe_taxa_permutations(sorted_taxa)
	random.shuffle(all_taxa_permutations)

	# Select one taxa order for constructing the distance matrix
	ordered_taxa = all_taxa_permutations.pop()
	if debug: print('ordered_taxa=', ordered_taxa)

	#===========================================
	# GENERATE DISTRACTOR CHOICES
	#===========================================

	## get the choices and answer
	treecode_cls_list, answer_treecode_cls = get_multiple_choices(ordered_taxa, num_choices)

	html_choices_list = []
	for treecode_cls in treecode_cls_list:
		html_treecode_table = treecode_cls.get_html_table()
		html_choices_list.append(html_treecode_table)
	html_choices_list = html_choices_list[:num_choices]
	answer_html_table = answer_treecode_cls.get_html_table()
	html_choices_list.append(answer_html_table)
	html_choices_list = list(set(html_choices_list))
	random.shuffle(html_choices_list)
	if len(html_choices_list) < 3:
		return None

	#===========================================
	# CREATE RANDOM DISTANCES AND PAIRS
	#===========================================

	# Generate a random list of distances for the taxa of the tree
	distance_list = make_random_distance_list(len(sorted_taxa) - 1)
	if debug: print(f"distance_list = {distance_list}")

	# Create a distance dictionary mapping taxa pairs to distances based on the answer tree
	distance_dict = map_taxon_distances(ordered_taxa, distance_list, answer_treecode_cls)

	# Generate and display an ASCII version of the distance matrix table
	if debug:
		print("original distance matrix")
		print_ascii_distance_table(ordered_taxa, distance_dict)

	# Modify the distance dictionary to include shifts (random offsets for added complexity)
	add_distance_pair_shifts(distance_dict, ordered_taxa, answer_treecode_cls)

	# Display the updated distance dictionary as an ASCII table
	if debug:
		print("adjusted distance matrix")
		print_ascii_distance_table(ordered_taxa, distance_dict)

	#===========================================
	# WRITE THE QUESTION
	#===========================================
	# Create the HTML table representation of the distance matrix
	distance_html_table = generate_html_distance_table(sorted_taxa, distance_dict, answer_treecode_cls)

	# Add the descriptive question statement
	problem_statement = get_problem_statement(sorted_taxa, distance_dict, answer_treecode_cls)

	# Format the question for multiple-choice display and return it
	full_question = distance_html_table + problem_statement
	complete = bptools.formatBB_MC_Question(N, full_question, html_choices_list, answer_html_table)
	return complete

#===========================================================
#===========================================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create', default=1
	)
	parser.add_argument(
		'-c', '--num_choices', type=int, default=5, dest='num_choices',
		help="Number of choices to create."
	)
	parser.add_argument(
		'-l', '--leaves', '--num_leaves', type=int, dest='num_leaves',
		help='number of leaves in the gene tree', default=5)

	args = parser.parse_args()

	# DIFFICULTY: easy < medium < rigorous
	# Use one argument with choices, plus optional shortcuts if you want
	parser.add_argument("-d", "--difficulty", dest="difficulty", type=str,
		choices=("easy", "medium", "rigorous"), default="medium",
		help="Difficulty: easy, medium, or rigorous")

	# Optional difficulty shortcuts
	diff_group = parser.add_mutually_exclusive_group()
	diff_group.add_argument("-E", "--easy",      dest="difficulty", action="store_const", const="easy",
		help="Set difficulty to easy")
	diff_group.add_argument("-M", "--medium",    dest="difficulty", action="store_const", const="medium",
		help="Set difficulty to medium")
	diff_group.add_argument("-R", "--rigorous",  dest="difficulty", action="store_const", const="rigorous",
		help="Set difficulty to rigorous")

	if args.num_leaves < 3:
		raise ValueError("Program requires a minimum of three (3) leaves to work")

	return args

#===========================================================
#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Define output file name
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'
		f'-{bptools.number_to_cardinal(args.num_leaves).upper()}_leaves'
		f'-{args.difficulty.upper()}'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1 # Question number counter
		for _ in range(args.duplicates):
			complete_question = make_question(N, args.num_leaves, args.num_choices)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram
	print(f"wrote {N-1} questions to the file {outfile}")
	bptools.print_histogram()

#===========================================================
#===========================================================
if __name__ == '__main__':
	main()

## THE END
