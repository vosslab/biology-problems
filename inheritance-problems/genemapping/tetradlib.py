
# Standard Library Imports
import sys
import copy
import math
import random

# Local Repository Modules
import bptools
import genemaplib as gml

# Global debug flag
debug = True

light_colors, dark_colors = bptools.light_and_dark_color_wheel(3)

#===========================================================
#===========================================================
def mini_genotype_table(genotype_str):
	table = '<div style="padding-left: 5px; padding-right: 5px;">'
	table += '<table style="border-collapse: collapse; border: 0px; padding-left: 50px; padding-right: 50px;">'
	table += '<tr>'
	td_extra = 'align="center" style="border: 0px;"'
	span = '<span style="font-size: large; font-family: monospace;">'
	for i, allele in enumerate(list(genotype_str)):
		if allele == '+':
			color_span = f'<span style="font-size: large; font-family: monospace; color: #{dark_colors[i]};">'
			table += f' <td {td_extra}>{color_span}{allele}</span></td>'
		else:
			color_td = f'align="center" style="border: 0px; background-color: #{light_colors[i]}"'
			table += f' <td {color_td}>{span}{allele}</span></td>'
	table += '</tr>'
	table += '</table>'
	table += '</div>'

	if gml.is_valid_html(table) is False:
		print(table)
		raise ValueError("Generated HTML is not valid.")
	return table

#===========================================================
#===========================================================
def make_progeny_html_table(progeny_tetrads_count_dict, progeny_size):
	list_of_tetrads = sorted(list(progeny_tetrads_count_dict.keys()))
	td_extra_center = 'align="center" style="border: 1px solid black;"'
	td_extra_right = 'align="right" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'
	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 400px; height: 220px;">'
	table += '<tr>'
	table += f'  <th {td_extra_center}>Set #</th>'
	table += f'  <th colspan="4" {td_extra_center}>Tetrad Genotypes</th>'
	table += f'  <th {td_extra_center}>Progeny<br/>Count</th>'
	table += '</tr>'
	for i, tetrad_tuple in enumerate(list_of_tetrads):
		table += '<tr>'
		table += f' <td {td_extra_center}>{span}{i+1}</span></td>'
		for genotype_str in tetrad_tuple:
			genotype_table = mini_genotype_table(genotype_str)
			table += f' <td {td_extra_center}>{span}{genotype_table}</span></td>'
		counts = progeny_tetrads_count_dict[tetrad_tuple]
		table += f' <td {td_extra_right}>{span}{counts:,d}</span></td>'
		table += '</tr>'
	table += '<tr>'
	table += f'  <th colspan="5" {td_extra_right}>TOTAL =</th>'
	table += f'  <td {td_extra_right}>{progeny_size:,d}</td>'
	table += '</tr>'
	table += '</table>'
	table += '<p>The resulting phenotypes are summarized in the table above.</p> '
	if gml.is_valid_html(table) is False:
		print(table)
		raise ValueError
	return table

#===========================================================
#===========================================================
def make_ditype_from_genotype_str(genotype_str, gene_letters_str):
	invert_str = gml.invert_genotype(genotype_str, gene_letters_str)
	ditype_tetrad = sorted([genotype_str, genotype_str, invert_str, invert_str])
	#return '\t'.join(ditype_tetrad)
	return tuple(ditype_tetrad)

#===========================================================
#===========================================================
def make_tetratype_from_genotype_strings(genotype_str1, genotype_str2, gene_letters_str):
	invert_str1 = gml.invert_genotype(genotype_str1, gene_letters_str)
	invert_str2 = gml.invert_genotype(genotype_str2, gene_letters_str)
	tetratype_tetrad = sorted([genotype_str1, genotype_str2, invert_str1, invert_str2])
	#return '\t'.join(tetratype_tetrad)
	return tuple(tetratype_tetrad)

#======================================
def get_all_ditype_tetrads(gene_letters_str):
	"""
	Generates all possible ditype tetrads for the given genes.
	A ditype tetrad consists of two identical pairs of alleles.

	Args:
		gene_letters_str (str): String containing gene symbols (e.g., 'ab' or 'def').

	Returns:
		list: A sorted list of unique ditype tetrads.
	"""
	list_of_all_genotypes = gml.generate_genotypes(gene_letters_str)

	if debug:
		print(f"{len(list_of_all_genotypes)} possible genotypes")

	# Initialize a set to store unique ditypes as tuples
	set_of_ditypes = set()

	# Generate ditypes by pairing each genotype with its inverted form
	for genotype in list_of_all_genotypes:
		inverted_genotype = gml.invert_genotype(genotype, gene_letters_str)
		ditype_tetrad = sorted([genotype, genotype, inverted_genotype, inverted_genotype])
		set_of_ditypes.add(tuple(ditype_tetrad))  # Use a tuple for hashable elements in the set

	if debug:
		print(f"Generated {len(set_of_ditypes)} unique ditypes")

	return sorted(set_of_ditypes)

#======================================
def get_all_tetratype_tetrads(gene_letters_str):
	"""
	Generates all possible tetratype tetrads for the given genes.
	A tetratype tetrad consists of four unique alleles.

	Args:
		gene_letters_str (str): String containing gene symbols (e.g., 'ab' or 'def').

	Returns:
		list: A sorted list of unique tetratype tetrads.
	"""
	list_of_all_genotypes = gml.generate_genotypes(gene_letters_str)

	if debug:
		print(f"{len(list_of_all_genotypes)} possible genotypes")

	# Initialize a set to store unique tetratypes as tuples
	set_of_tetratypes = set()

	# Generate tetratypes by combining each genotype with other unique genotypes
	for genotype1 in list_of_all_genotypes:
		inverted_genotype1 = gml.invert_genotype(genotype1, gene_letters_str)
		for genotype2 in list_of_all_genotypes:
			if genotype1 == genotype2 or inverted_genotype1 == genotype2:
				continue  # Avoid pairing a genotype with itself for tetratypes
			inverted_genotype2 = gml.invert_genotype(genotype2, gene_letters_str)
			tetratype_tetrad = sorted([genotype1, genotype2, inverted_genotype1, inverted_genotype2])
			if len(set(tetratype_tetrad)) != 4:
				raise ValueError
			set_of_tetratypes.add(tuple(tetratype_tetrad))

	if debug:
		print(f"Generated {len(set_of_tetratypes)} unique tetratypes")

	return sorted(set_of_tetratypes)

#======================================
def get_all_possible_tetrads(gene_letters_str):
	"""
	Generates all possible tetrads (arrangements of gene alleles in spores) for the given genes.

	For 2 genes:
		- Generates cis and trans ditypes, as well as tetratypes.
	For 3 genes:
		- Currently not implemented.

	Args:
		gene_letters_str (str): String containing gene symbols (e.g., 'ab' or 'def').

	Returns:
		list: A sorted list of all possible tetrad arrangements.
	"""

	# Generate all ditypes and tetratypes
	list_of_ditypes = get_all_ditype_tetrads(gene_letters_str)
	list_of_tetratypes = get_all_tetratype_tetrads(gene_letters_str)

	# Combine ditypes and tetratypes into a single list and sort for consistent output
	list_of_all_tetrads = sorted(list_of_ditypes + list_of_tetratypes)

	if debug:
		print(f"Generated {len(list_of_all_tetrads)} unique tetrads")

	return list_of_all_tetrads

#======================================
def is_ditype(tetrad_tuple):
	if len(set(tetrad_tuple)) == 2:
		return True
	if len(set(tetrad_tuple)) == 4:
		return False
	raise ValueError

#====================================
#====================================
def get_all_single_crossovers_for_ditype_tetrad(tetrad_tuple, gene_letters_str):
	if not is_ditype(tetrad_tuple):
		sys.exit(1)
	num_genes_int = len(gene_letters_str)

	genotype_pair = list(set(tetrad_tuple))
	print(f"genotype_pair = {genotype_pair}")
	set_of_tetratypes = set()
	for i in range(num_genes_int):
		index = i+1
		tetratype_tetrad = copy.copy(genotype_pair)
		for genotype in genotype_pair:
			print(genotype, index, gene_letters_str)
			flipped_genotype = gml.flip_gene_by_index(genotype, index, gene_letters_str)
			tetratype_tetrad.append(flipped_genotype)
		tetratype_tetrad = sorted(tetratype_tetrad)
		if len(set(tetratype_tetrad)) != 4:
			raise ValueError
		set_of_tetratypes.add(tuple(tetratype_tetrad))
	return set_of_tetratypes


#===========================================================
#===========================================================
def get_progeny_ascii_table(num_genes_int, progeny_tetrads_count_dict, progeny_count_int) -> str:
	"""
	Generates an ASCII table with Unicode borders displaying progeny data in a tetrad format.

	Each row represents a tetrad set, with columns for the tetrad set number, spore genotypes,
	and the count of tetrads. Borders are made using Unicode box-drawing characters.

	Returns:
		str: A formatted string displaying tetrad information with Unicode borders.
	"""
	# Column 1: fixed 8 characters wide
	# Column 2: variable width based on the number of genes
	# Column 3: fixed 9 characters wide

	# Calculate the dynamic width for the "Genotypes of Spore in Tetrads" column
	genotypes_col_width = 4 * num_genes_int + 3*3 + 2  # 4 characters per genotype plus 5 spaces between

	# Unicode characters for borders
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

	# Define table borders
	top_border = (
		f"{top_left_corner}{horizontal_line * 8}{middle_top}"
		f"{horizontal_line * genotypes_col_width}{middle_top}"
		f"{horizontal_line * 9}{top_right_corner}\n"
	)
	separator = (
		f"{middle_left}{horizontal_line * 8}{center_cross}"
		f"{horizontal_line * genotypes_col_width}{center_cross}"
		f"{horizontal_line * 9}{middle_right}\n"
	)
	bottom_border = (
		f"{bottom_left_corner}{horizontal_line * 8}{middle_bottom}"
		f"{horizontal_line * genotypes_col_width}{middle_bottom}"
		f"{horizontal_line * 9}{bottom_right_corner}\n"
	)

	# Header and alignment for columns
	header = (
		f"{vertical_line} Tetrad {vertical_line} Genotypes of {' ' * (genotypes_col_width - 14)}{vertical_line}  # of   {vertical_line}\n"
		f"{vertical_line}  Set # {vertical_line} Tetrad Spores{' ' * (genotypes_col_width - 14)}{vertical_line} Tetrads {vertical_line}\n"
	)

	# Initialize table with headers and top border
	ascii_table = top_border + header + separator

	list_of_all_tetrads = sorted(list(progeny_tetrads_count_dict.keys()))

	# Sort all genotype pairs (tetrads) for display
	all_tetrads_tuples = sorted(list_of_all_tetrads, reverse=False)

	# Initialize tetrad set counter and overall total counter
	total_tetrad_count = 0

	# Loop through sorted genotype pairs to fill the table with tetrads
	for tetrad_set_num, tetrad_tuple in enumerate(all_tetrads_tuples, start=1):
		# Each tetrad has four spores: two of genotype1 and two of genotype2

		genotypes_str = f" {vertical_line} ".join(tetrad_tuple)

		# Calculate tetrad count and add to total
		tetrad_count = progeny_tetrads_count_dict.get(tetrad_tuple,0)
		total_tetrad_count += tetrad_count

		# Format columns with appropriate alignment
		# Centered tetrad set number, by rule number is a single digit
		tetrad_set_str = f"    {tetrad_set_num}   "
		# Right-aligned with thousands comma
		tetrad_count_str = gml.right_justify_int(tetrad_count, 8)

		# Add row to the table
		ascii_table += f"{vertical_line}{tetrad_set_str}{vertical_line} "
		ascii_table += f"{genotypes_str:<{genotypes_col_width-2}} "
		ascii_table += f"{vertical_line}{tetrad_count_str} {vertical_line}\n"

	if total_tetrad_count != progeny_count_int:
		#double check the counts
		print("WARNING COUNTS ARE OFF")
		#raise ValueError

	# Add bottom separator and total row
	ascii_table += separator
	total_str = gml.right_justify_int(progeny_count_int, 8)
	ascii_table += f"{vertical_line}{'TOTAL':^8}{vertical_line}{' ' * genotypes_col_width}{vertical_line}{total_str} {vertical_line}\n"
	ascii_table += bottom_border

	return ascii_table


#===========================================================
#===========================================================
def construct_progeny_counts(gene_letters_str, gene_order_str, distances, progeny_size):
	if debug is True: print("------------")
	answerString = ("%s - %d - %s - %d - %s"
		%(gene_order_str[0], distances[0], gene_order_str[1], distances[1], gene_order_str[2]))
	print(answerString)
	if debug is True: print("------------")

	if debug is True: print("determine parental type")
	possible_genotypes = ['++'+gene_letters_str[2], '+'+gene_letters_str[1]+'+', '+'+gene_letters_str[1]+gene_letters_str[2]]
	parental_genotype_str = random.choice(possible_genotypes)

	progeny_tetrads_count_dict = generate_progeny_counts(parental_genotype_str, gene_order_str, distances, progeny_size, gene_letters_str)
	return progeny_tetrads_count_dict

#===========================================================
#===========================================================
def generate_progeny_counts(parental_genotype_str, gene_order_str, distance_tuple, progeny_size_int, gene_letters_str):
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
	first_flip = gml.flip_gene_by_letter(parental_genotype_str, gene_order_str[0], gene_letters_str)

	# Tetratype (TT) tetrad for first flip
	tt_tetrad = make_tetratype_from_genotype_strings(first_flip, parental_genotype_str, gene_letters_str)
	progeny_tetrads_count_dict[tt_tetrad] = firstcount

	# Non-Parental Ditype (NPD) for first flip
	npd_tetrad_1 = make_ditype_from_genotype_str(first_flip, gene_letters_str)
	progeny_tetrads_count_dict[npd_tetrad_1] = dcount1

	# Step 8: Generate Tetratype (TT) and Non-Parental Ditype (NPD) based on the second gene flip
	# Flip the second gene in gene_order to generate another single crossover configuration
	second_flip = gml.flip_gene_by_letter(parental_genotype_str, gene_order_str[2], gene_letters_str)

	# Tetratype (TT) tetrad for second flip
	tt_tetrad_2 = make_tetratype_from_genotype_strings(second_flip, parental_genotype_str, gene_letters_str)
	progeny_tetrads_count_dict[tt_tetrad_2] = secondcount

	# Non-Parental Ditype (NPD) for second flip
	npd_tetrad_2 = make_ditype_from_genotype_str(second_flip, gene_letters_str)
	progeny_tetrads_count_dict[npd_tetrad_2] = dcount2

	# Step 9: Generate Non-Parental Ditype (NPD) based on both first and second gene flips
	# Flip both the middle gene to simulate a double crossover configuration
	double_flip = gml.flip_gene_by_letter(parental_genotype_str, gene_order_str[1], gene_letters_str)

	# Non-Parental Ditype (NPD) for double flip: [double_flip, inverted(double_flip), double_flip, inverted(double_flip)]
	npd_double_flip_tetrad = make_ditype_from_genotype_str(double_flip, gene_letters_str)
	progeny_tetrads_count_dict[npd_double_flip_tetrad] = dcount3

	# Final validation: Ensure we have exactly 6 unique tetrad configurations
	if len(progeny_tetrads_count_dict) != 6:
		raise ValueError("Expected 6 unique tetrad configurations, but got a different number.")

	return progeny_tetrads_count_dict


#===========================================================
#===========================================================
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

#===========================================================
#===========================================================
def tetrad_calculation_string(tt_values, npd_values, total) -> str:
	"""
	Generates an HTML-formatted string representing the genetic distance calculation in centiMorgans (cM).

	This function takes tuples of counts for tetratypes (TT) and non-parental ditypes (NPD), and:
	1. Sums these counts to get the total recombinant counts for TT and NPD.
	2. Uses the formula (1/2 * TT + 3 * NPD) / total to compute the recombinant fraction.
	3. Converts this fraction to centiMorgans (cM) and formats the calculation as an HTML string,
	   including each intermediate step in the calculation.

	Args:
		tt_values (tuple): A tuple of integers representing the count of TT genotypes.
		npd_values (tuple): A tuple of integers representing the count of NPD genotypes.
		total (int): The total progeny count, used as the denominator in the calculation.

	Returns:
		str: A formatted HTML string showing the detailed genetic distance calculation and final result in cM.

	Raises:
		ValueError: If the generated HTML is not valid (detected by `gml.is_valid_html`).
	"""
	# Step 1: Sum the recombinant counts for TT and NPD
	tt_val_sum = sum(tt_values)
	npd_val_sum = sum(npd_values)

	# Step 2: Start constructing the HTML string for the genetic distance formula
	# Display the formula: distance = (1/2 * TT + 3 * NPD) / total
	choice_text = 'distance = '
	#choice_text += gml.format_fraction('&half;TT + 3&times;NPD', 'total') + ' = '

	# Step 3: Construct the numerator with each TT and NPD count formatted as a sum
	tt_list = sorted(tt_values)
	formatted_tt_values = ' + '.join(f'{val:,d}' for val in tt_list)
	npd_list = sorted(npd_values)
	formatted_npd_values = ' + '.join(f'{val:,d}' for val in npd_list)

	numerator = f'&half;({formatted_tt_values}) + 3&times;({formatted_npd_values})'
	choice_text += gml.format_fraction(f'{numerator}', f'{total:,d}') + ' = '

	# Step 4: Substitute the total sums for TT and NPD into the formula
	numerator = f'&half;&times;{tt_val_sum:,d} + 3&times;{npd_val_sum:,d}'
	#choice_text += gml.format_fraction(f'{numerator}', f'{total:,d}') + ' = '

	# Step 5: Evaluate the fractional TT term (half of TT sum)
	# Handle even and odd TT counts differently for consistent formatting
	if tt_val_sum % 2 == 0:
		numerator = f'{tt_val_sum // 2:,d} + {3 * npd_val_sum:,d}'
	else:
		numerator = f'{tt_val_sum / 2:.1f} + {3 * npd_val_sum:,d}'
	choice_text += gml.format_fraction(f'{numerator}', f'{total:,d}') + ' = '

	# Step 6: Combine the TT and NPD contributions into a single recombinant count
	# Handle integer vs. float formatting for the combined count
	if tt_val_sum % 2 == 0:
		numerator = f'{(tt_val_sum // 2 + 3 * npd_val_sum):,d}'
	else:
		numerator = f'{(tt_val_sum / 2.0 + 3 * npd_val_sum):.1f}'
	choice_text += gml.format_fraction(f'{numerator}', f'{total:,d}') + ' = '

	# Step 7: Calculate the recombinant fraction as a decimal
	val_sum = tt_val_sum / 2.0 + 3 * npd_val_sum
	distance_float_val = val_sum / float(total)
	choice_text += f'{distance_float_val:.4f} = '  # Display the fraction as a decimal (4 decimal places)

	# Step 8: Convert the fraction to centiMorgans (cM) and display the final result
	# Round the result if it's close to an integer, otherwise keep 2 decimal places
	if math.isclose(distance_float_val * 100, round(distance_float_val * 100)):
		choice_text += f'<strong>{round(distance_float_val * 100 + 1e-6):d} cM</strong>'
	else:
		choice_text += f'<strong>{distance_float_val * 100:.2f} cM</strong>'

	# Step 9: Validate the generated HTML string and raise an error if invalid
	if gml.is_valid_html(choice_text) is False:
		print(choice_text)
		raise ValueError("Generated HTML is not well-formed.")

	return choice_text, distance_float_val

#======================================
#======================================
def check_if_progeny_counts_are_valid(progeny_tetrads_count_dict):
	"""
	Checks if the provided progeny tetrads count dictionary is valid for use in a genetics question.

	This function performs the following checks:
	1. Ensures that `progeny_tetrads_count_dict` is not `None`.
	2. Confirms that each tetrad has exactly 4 genotypes, as required for this type of question.
	3. Checks that the number of distinct tetrad counts matches the expected number for the given number of genes.
	   - For two genes, we expect 3 unique tetrad types: PD, NPD, TT.
	   - For three genes, we expect 6 unique tetrad types.
	4. Verifies that each tetrad count has a minimum threshold (at least 2), ensuring that there are enough tetrads for each type.

	Args:
		progeny_tetrads_count_dict (dict): Dictionary where each key represents a tetrad genotype
										   (a tuple of 4 elements), and each value represents the count of that genotype.

	Returns:
		bool: True if `progeny_tetrads_count_dict` is valid, False otherwise. If validation fails,
			  error messages are printed to indicate the specific issue.
	"""
	# Check 1: Ensure the dictionary is not `None`
	if progeny_tetrads_count_dict is None:
		print("Question generation failed: No progeny tetrads count dictionary provided.")
		return False

	# Check 2: Confirm that each tetrad is composed of exactly 4 genotypes
	single_key = next(iter(progeny_tetrads_count_dict))  # Get an arbitrary key from the dictionary
	if len(single_key) != 4:
		print("Question generation failed: Each tetrad should be composed of 4 genotypes.")
		print(f"Tetrad keys provided: {progeny_tetrads_count_dict.keys()}")
		return False

	# Determine the number of genes by checking the length of each genotype in the tetrad key
	num_genes_int = len(single_key[0])

	# Define the expected number of unique tetrad types based on the number of genes
	expected_tetrads = {2: 3, 3: 6}  # 3 for 2 genes (PD, NPD, TT), 6 for 3 genes

	# Check 3: Verify that the number of unique tetrad counts matches the expected number for the given gene count
	if len(set(progeny_tetrads_count_dict.values())) != expected_tetrads[num_genes_int]:
		print("Question generation failed: Incorrect number of distinct tetrad counts.")
		print(f"Tetrad counts provided: {progeny_tetrads_count_dict.values()}")
		return False

	# Check 4: Ensure each tetrad count has at least a minimum threshold (2 in this case)
	if min(progeny_tetrads_count_dict.values()) < 2:
		print("Question generation failed: Not enough tetrads for at least one of the types.")
		print(f"Tetrad counts provided: {progeny_tetrads_count_dict.values()}")
		return False

	# If all checks pass, the dictionary is valid
	return True

#======================================
def main():
	"""Main function for testing get_all_possible_tetrads with different gene inputs."""
	# Test cases for 2-gene and 3-gene systems
	print('=' * 80)
	tetrads_2_genes = get_all_possible_tetrads('ab')
	print("Tetrads for 'ab':", tetrads_2_genes)

	print('=' * 80)
	tetrads_3_genes = get_all_possible_tetrads('def')
	print("Tetrads for 'def':", tetrads_3_genes)

	print('=' * 80)

#======================================
if __name__ == '__main__':
	main()
