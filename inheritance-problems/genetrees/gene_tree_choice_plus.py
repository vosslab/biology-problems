#!/usr/bin/env python3

import os
import sys
import copy
import random
import argparse
import colorsys

#local
import bptools
import phylolib2
bptools.use_add_no_click_div = False

debug = False

# make a gene tree table with 4 leaves, ask students to choose correct one

#===========================================
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

#===========================================
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
	rgb1 = colorsys.hsv_to_rgb(angle, 0.20, 0.999)

	# Convert the RGB values to a hexadecimal HTML color.
	html_hex = rgb_to_hex(rgb1)

	# Return the hexadecimal color string for use in HTML.
	return html_hex

#===========================================
def makeRandDistanceList(num_distances):
	###num_distances = math.comb(len(ordered_taxa), 2)//2 <- WRONG?
	distances = []
	multiplier = 2
	while len(distances) < num_distances:
		r = random.randint(2, num_distances*multiplier)
		r *= 2
		skip = False
		for d in distances:
			if abs(r - d) <= 7:
				skip = True
		if skip is False:
			distances.append(r)
			multiplier += 2
	distances.sort()
	return distances

#==================================
def get_taxa_pair_node(code, taxa1, taxa2):
	## assumes existing taxa are alphabetical, also assumes ordered taxa lag
	index1 = code.find(taxa1)
	index2 = code.find(taxa2)
	min_index = min(index1, index2)
	max_index = max(index1, index2)
	substring = code[min_index+1:max_index]
	#print("substring=", taxa1, substring, taxa2)
	sublist = list(substring)
	max_node = -1
	for s in sublist:
		if s.isdigit():
			s_int = int(s)
			max_node = max(max_node, s_int)
	#print("max_node=", max_node)
	return max_node

#===========================================
def makeDistancePairs(ordered_taxa, distance_list, answer_code):
	# A-1-B -2-C -3-D
	distance_dict = {}
	for i, taxa1 in enumerate(ordered_taxa):
		if i == 0:
			continue
		for j, taxa2 in enumerate(ordered_taxa):
			if i <= j:
				continue
			# i > j OR j < i
			max_node = get_taxa_pair_node(answer_code, taxa1, taxa2)
			distance_index = max_node - 1
			distance_dict[(taxa1, taxa2)] = distance_list[distance_index]
			distance_dict[(taxa2, taxa1)] = distance_list[distance_index]
	return distance_dict

#===========================================
def addDistancePairShifts(distance_dict, ordered_taxa, answer_code):
	shift_list = [-2,2]
	for n in range(len(ordered_taxa)-2):
		shift_list.append(0)
	shift_list.sort()
	#print("shift_list=", shift_list)
	for i,taxa1 in enumerate(ordered_taxa):
		for j,taxa2 in enumerate(ordered_taxa):
			if i == j:
				continue
			for k,taxa3 in enumerate(ordered_taxa):
				if j == k or i == k:
					continue
				# i > j > k OR k < j < i
				max_node_1_2 = get_taxa_pair_node(answer_code, taxa1, taxa2)
				max_node_2_3 = get_taxa_pair_node(answer_code, taxa2, taxa3)
				max_node_1_3 = get_taxa_pair_node(answer_code, taxa1, taxa3)

				if max_node_2_3 == max_node_1_3 and max_node_1_2 < max_node_1_3:
					# do something
					#print("genes (", taxa1, taxa2, ")", taxa3)
					#print("max_node", max_node_1_2, max_node_2_3, max_node_1_3)
					#print("DO SOMETHING")
					#shift = random.randint(-1, 1) * 2
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
	header = f"{vertical_line}{' ' * column_width}"  # Empty top-left corner
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
				cell_value = "---"  # Self-distance marked with 'x'
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

#===========================================
def generate_html_distance_table(ordered_taxa, distance_dict, distance_list):
	"""
	Generate an HTML table for a distance matrix with genes as rows and columns.

	Args:
		ordered_taxa (list): Ordered list of gene names.
		distance_dict (dict): A dictionary mapping gene pairs to distances.
		distance_list (list): List of distances used for color mapping.

	Returns:
		str: An HTML string representing the distance matrix as a table.
	"""
	sorted_taxa = sorted(ordered_taxa)  # Sort the taxa names alphabetically
	td_extra = 'align="center" style="border: 1px solid black; background-color: xxxxxx;"'
	span = '<span style="font-size: medium;">'

	# Start the table and add the header row
	table = (
		'<table style="border-collapse: collapse; border: 2px solid black; width: 460px; height: 150px">'
		'<tr>'
		f'<td {td_extra.replace("xxxxxx", "white")}>taxa</td>'
	)
	for g in sorted_taxa:
		table += f'<th {td_extra}>{span}{g}</span></th>'
	table += '</tr>'

	# Add rows for each taxa
	for taxa1 in sorted_taxa:
		table += '<tr>'
		table += f'<th {td_extra}>{span}{taxa1}</span></th>'
		for taxa2 in sorted_taxa:
			if taxa1 == taxa2:
				# Self-distance is represented by gray cells
				my_td_extra = td_extra.replace('xxxxxx', 'gray')
				table += f'<td {my_td_extra}>&times;</td>'
			else:
				# Use distance to calculate color and add the value
				distance = distance_dict[(taxa1, taxa2)]
				hex_color = distance_to_html_color(distance, distance_list)
				my_td_extra = td_extra.replace('xxxxxx', hex_color)
				table += f'<td {my_td_extra}>{span}{distance}</span></td>'
		table += '</tr>'

	# Close the table
	table += '</table>'
	return table

#===========================================
def getGoodGenePermutation(gene_permutations, ordered_taxa, answer_code):
	one_index = answer_code.find('1')
	first_letter = answer_code[one_index-1]
	second_letter = answer_code[one_index+1]
	first_letter_index_pair = (ordered_taxa.index(first_letter),  ordered_taxa.index(second_letter))
	random.shuffle(gene_permutations)
	for permuted_genes in gene_permutations:
		if permuted_genes == ordered_taxa:
			continue
		if permuted_genes.index(first_letter) not in first_letter_index_pair:
			continue
		if permuted_genes.index(second_letter) not in first_letter_index_pair:
			continue
		#print("PERMUTE", permuted_genes, ordered_taxa, first_letter, second_letter)
		return permuted_genes

#===========================================
def make_question(N: int, num_leaves: int, num_choices: int) -> str:
	"""
	Generate a multiple-choice question about gene trees based on a distance matrix.

	Args:
		N (int): A unique identifier for the question.
		num_leaves (int): The number of leaves (genes) in the gene tree.
		num_choices (int): The total number of answer choices, including the correct one.

	Returns:
		str: A formatted HTML multiple-choice question that includes a species distance matrix
		     and a list of possible gene tree answers.
	"""
	# Generate node names (letters) with "clear" letters (excluding ambiguous ones like 'o' or 'i')
	taxa_letters_str = bptools.generate_gene_letters(num_leaves, clear=True).upper()
	# Sort the node letters alphabetically
	sorted_taxa = sorted(taxa_letters_str)

	# The number of taxa in the gene tree equals the number of leaves minus one
	# ^^ this makes no sense to me!!!
	num_taxa = num_leaves - 1
	genetree = phylolib2.GeneTree()  # Initialize the GeneTree object for tree generation and manipulation

	#===========================================
	# FIND A PARTICULAR ORDER FOR THE GENES
	#===========================================
	# Get all permutations of the sorted node letters and shuffle them randomly
	all_taxa_permutations = phylolib2.get_comb_safe_taxa_permutations(sorted_taxa)
	random.shuffle(all_taxa_permutations)

	# Select one node order for constructing the distance matrix
	ordered_taxa = all_taxa_permutations.pop()
	if debug: print('ordered_taxa=', ordered_taxa)

	#===========================================
	# GET ALL POSSIBLE GENE TREES
	#===========================================
	# Generate all possible gene tree encodings for the given number of leaves
	code_choice_list = genetree.make_all_gene_trees_for_leaf_count(num_leaves, sorted_taxa)
	random.shuffle(code_choice_list)  # Shuffle the tree encodings to randomize selection

	# Select one tree encoding as the correct answer
	answer_code = code_choice_list.pop()
	if debug: print("answer_code=", answer_code)

	#===========================================
	# CREATE RANDOM DISTANCES AND PAIRS
	#===========================================
	# Generate a random list of distances for the internal nodes of the tree
	distance_list = makeRandDistanceList(num_taxa)
	if debug: print("distance_list=", distance_list)

	# Create a distance dictionary mapping node pairs to distances based on the answer tree
	distance_dict = makeDistancePairs(ordered_taxa, distance_list, answer_code)

	# Generate and display an ASCII version of the distance matrix table
	if debug: print("original distance matrix")
	print_ascii_distance_table(ordered_taxa, distance_dict)

	# Modify the distance dictionary to include shifts (random offsets for added complexity)
	addDistancePairShifts(distance_dict, ordered_taxa, answer_code)

	# Display the updated distance dictionary as an ASCII table
	if debug: print("adjusted distance matrix")
	print_ascii_distance_table(ordered_taxa, distance_dict)

	#===========================================
	# REMOVE CHOICES WITH IDENTICAL PROFILES
	#===========================================
	# Generate the "profile" (a structural representation) of the correct answer tree
	answer_profile = genetree.gene_tree_code_to_profile(answer_code, num_taxa)

	# Group all tree encodings by their profiles
	profile_groups = genetree.group_gene_trees_by_profile(code_choice_list, num_taxa)

	# Remove any trees with profiles that match the correct answer's profile
	if profile_groups.get(answer_profile) is not None:
		del profile_groups[answer_profile]

	#===========================================
	# PRIORITIZE MORE SIMILAR TREES FOR CHOICES
	#===========================================
	# Sort the remaining profile groups by how similar they are to the correct answer
	sorted_profile_group_keys = list(profile_groups.keys())
	if len(profile_groups) > num_choices:
		sorted_profile_group_keys = genetree.sort_profiles_by_closeness(profile_groups, answer_profile)

	# Generate the HTML answer choices for the question
	html_choices_list = []
	if debug:
		print(answer_profile)
		print("sorted profiles=", sorted_profile_group_keys[:6])

	for key in sorted_profile_group_keys:
		# Randomly select one tree encoding from the profile group
		profile_code_list = profile_groups[key]
		code_choice = random.choice(profile_code_list)

		# Convert the tree encoding into an HTML representation and add it to the choices
		html_choice = genetree.get_html_from_code(code_choice)
		html_choices_list.append(html_choice)

		# Stop when we have enough incorrect choices
		if len(html_choices_list) >= num_choices - 1:
			break

	# Add the correct answer as an HTML choice
	answer_html_choice = genetree.get_html_from_code(answer_code)
	html_choices_list.append(answer_html_choice)

	# Shuffle the answer choices to randomize their order
	random.shuffle(html_choices_list)

	#===========================================
	# WRITE THE QUESTION
	#===========================================
	# Create the HTML table representation of the distance matrix
	distance_html_table = generate_html_distance_table(ordered_taxa, distance_dict, distance_list)

	# Add the descriptive question statement
	tax1 = sorted_taxa[0]
	tax2 = sorted_taxa[1]
	tax3 = sorted_taxa[2]
	problem_statement = (
		"<p>The table above represents a distance matrix for the following genes: "
		f"{', '.join(f'<b>{taxa}</b>' for taxa in sorted_taxa)}. "
		"The values in the matrix correspond to the genetic distances "
		"between pairs of genes.</p> "
		"<p>For example, "
		f"{taxa_text(tax1, tax2, distance_dict)}. "
		"Distances are symmetric, meaning that both "
		f"{taxa_text(tax2, tax3, distance_dict)} and "
		f"{taxa_text(tax3, tax2, distance_dict)}.</p>"
		"<p>Using this distance matrix, determine the most appropriate gene tree that "
		"accurately reflects the relationships and distances between these genes.</p>"
	)

	if debug is True:
		# Uncomment to debug: write question and choices to a temporary HTML file
		f = open('temp.html', 'w')
		f.write(answer_html_choice + '<br/>')
		f.write(distance_html_table + '<br/>')
		for hc in html_choices_list:
			f.write(hc + '<br/>')
		f.write(''.join(ordered_taxa))
		f.close()

	# Format the question for multiple-choice display and return it
	# Format and return the complete question
	full_question = distance_html_table + problem_statement
	complete = bptools.formatBB_MC_Question(N, full_question, html_choices_list, answer_html_choice)
	return complete

#======================================
#======================================
def taxa_text(tax1, tax2, distance_dict):
	gene_string = (
		f"the distance between <b>taxa {tax1}</b> and "
		f"<b>taxa {tax2}</b> is "
		f"<b>{distance_dict[(tax1, tax2)]}</b>"
	)
	return gene_string

#=====================
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
		help='number of leaves in gene trees', default=5)

	args = parser.parse_args()

	if args.num_leaves < 3:
		raise ValueError("Program requires a minimum of three (3) genes to work")

	return args

#======================================
#======================================
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
		f'-{args.num_leaves}_leaves'
		'-questions.txt'
	)
	print(f'Writing to file: {outfile}')
	N = 0

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			complete_question = make_question(N, args.num_leaves, args.num_choices)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram
	print(f"wrote {N} questions to the file {outfile}")
	bptools.print_histogram()

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
