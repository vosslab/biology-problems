#!/usr/bin/env python3


# Built-in libraries
import sys
import copy
import math
import random

# Local libraries
import bptools
import genemaplib as gml
import genemapclass as gmc
import tetradlib

#===========================================================
class TetradMappingClass(gmc.GeneMappingClass):
	"""
	An extension of the GeneMappingClass for tetrad analysis.

	This class expands upon the base GeneMappingClass to include functionality specific
	to tetrad analysis, which might involve additional calculations or data structures
	for handling tetrad-based gene mapping problems.
	"""
	# Class-level variable to cache distance triplets across instances
	_distance_triplet_list_cache = None

	def __init__(self, num_genes_int: int, question_count: int = 1, debug: bool = True) -> None:
		"""
		Initialize a TetradMappingClass instance.

		Args:
			num_genes_int (int): The number of genes involved in the mapping.
			question_count (int, optional): The number of questions to generate. Defaults to 1.
			debug (bool, optional): If True, enables debug output. Defaults to False.

		Additional Attributes:
			Any attributes specific to tetrad analysis can be added here.
		"""
		# Call the superclass initializer with required arguments
		self.list_of_all_tetrads = []
		self.parental_tetrad = None
		self.unlinked = False
		super().__init__(num_genes_int, question_count, debug)

	#===========================================================
	#===========================================================
	def setup_question(self):
		"""
		Prepares the gene map for a question by setting distances, progeny counts, and genotype lists.

		This method calls several helper functions to initialize various properties required
		for a genetic question, including distances, progeny group counts, and genotype pairs.
		"""
		# Sets genetic distances between gene pairs
		self.set_gene_distances()
		# Sets the total progeny count for the map
		self.set_progeny_count()
		# Sets counts for different progeny groups
		self.set_progeny_groups_counts()

		# Set the tetrad groups, ditypes and tetratypes
		self.setup_tetrad_lists()
		# Assign progeny
		self.set_tetrad_counts()
		# Chooses parental genotypes for the map
		if self.debug is True:
			self.print_gene_map_data()
		sys.exit(1)

		self.set_all_genotype_tuple_pairs_list()  # Sets pairs of genotypes for the map
		self.set_genotype_counts()              # Sets counts for each genotype

	#===========================================================
	#===========================================================
	def set_gene_distances(self, min_distance=2) -> None:
		"""
		Sets the genetic distances between gene pairs.

		Args:
			min_distance (int): The minimum possible distance between gene pairs (default is 2).

		Chooses different methods for setting distances based on the question type (`mc` or `num`).
		Prints the data if debug mode is enabled.
		"""
		if self.unlinked is True and self.num_genes_int == 2:
			self.distances_dict = {(1, 2): 49}
		elif self.question_type == 'mc':
			self.set_gene_distances_mc(min_distance)
		else:
			self.set_gene_distances_int(min_distance)

		# Print updated gene map data if in debug mode
		if self.debug is True:
			self.print_gene_map_data()

	#====================================
	#====================================
	def setup_tetrad_lists(self):
		self.list_of_ditypes = tetradlib.get_all_ditype_tetrads(self.gene_letters_str)
		self.list_of_tetratypes = tetradlib.get_all_tetratype_tetrads(self.gene_letters_str)
		self.list_of_all_tetrads = sorted(self.list_of_ditypes + self.list_of_tetratypes)
		if self.debug:
			print(f"Generated {len(self.list_of_all_tetrads)} unique tetrads")

	#===========================================================
	#===========================================================
	def print_gene_map_data(self) -> None:
		"""
		Prints the internal data of the gene map for debugging and analysis.

		Displays details such as gene count, gene order, distances, interference patterns,
		progeny counts, genotype pair lists, and individual genotype counts.
		"""
		print('================================')
		print('================================')

		print(self.get_progeny_ascii_table())

		print('================================')
		print(f'self.num_genes_int = {self.num_genes_int}')
		print(f'self.gene_letters_str = {self.gene_letters_str}')
		print(f'self.gene_order_str = {self.gene_order_str}')

		if len(self.list_of_all_tetrads) > 0:
			print(f"there are {len(self.list_of_ditypes)} di-type tetrads")
			print(f"there are {len(self.list_of_tetratypes)} tetra-type tetrads")
			print(f"there are {len(self.list_of_all_tetrads)} unique tetrads")


		# Print distances between genes
		if self.distances_dict is not None:
			print('self.distances_dict = {')
			for key, value in self.distances_dict.items():
				print(f'  {key}: {value} # gene '
					+f'{self.gene_order_str[key[0]-1].upper()} and '
					+f'{self.gene_order_str[key[1]-1].upper()} '
				)
			print('}')

		# Print interference values
		if self.interference_dict is not None:
			print('self.interference_dict = {')
			for key in self.distances_dict.keys():
				value = self.interference_dict.get(key)
				if value is None:
					print(f'  {key}: {value} # adjacent genes '
						+f'{self.gene_order_str[key[0]-1].upper()} and '
						+f'{self.gene_order_str[key[1]-1].upper()} '
					)
				else:
					print(f'  {key}: {value} # interference btw '
						+f'{self.gene_order_str[key[0]-1].upper()} and '
						+f'{self.gene_order_str[key[1]-1].upper()} '
					)
			print('}')

		# Print progeny count and grouping details
		if self.progeny_count_int > 0:
			print(f'self.progeny_count_int = {self.progeny_count_int}')
		if self.progeny_groups_count_dict is not None:
			print('self.progeny_groups_count_dict = {')
			for key, value in self.progeny_groups_count_dict.items():
				if isinstance(key, tuple):
					print(f'  {key}: {value:02d} # gene '
						+f'{self.gene_order_str[key[0]-1].upper()} and '
						+f'{self.gene_order_str[key[1]-1].upper()} '
					)
				else:
					print(f'  {key}: {value:02d} # parental')
			print('}')

		# Print genotype pair lists and counts
		if self.all_genotype_tuple_pairs_list is not None:
			print(f'self.all_genotype_tuple_pairs_list = {self.all_genotype_tuple_pairs_list}')
		if self.parental_genotypes_tuple is not None:
			print(f'self.parental_genotypes_tuple = {self.parental_genotypes_tuple}')
		if self.genotype_counts is not None:
			print('self.genotype_counts = {')
			for genotype, count in self.genotype_counts.items():
				print(f'  {genotype}: {count:d}')
			print('}')
		print('================================')

	#====================================
	#====================================
	#====================================
	#====================================
	def get_progeny_ascii_table(self) -> str:
		"""
		Generates an ASCII table with Unicode borders displaying progeny data in a tetrad format.

		Each row represents a tetrad set, with columns for the tetrad set number, spore genotypes,
		and the count of tetrads. Borders are made using Unicode box-drawing characters.

		Returns:
			str: A formatted string displaying tetrad information with Unicode borders.
		"""
		html_table = tetradlib.get_progeny_ascii_table(self.num_genes_int, self.progeny_tetrads_count_dict, self.progeny_count_int)
		return html_table

	#====================================
	#====================================
	#====================================
	#====================================
	def make_progeny_html_table(self):
		"""
		Generates an HTML table to display progeny data in Blackboard format.

		Args:
			typemap (dict): Dictionary mapping tetrad genotypes to their counts.
			progeny_size (int): Total progeny size to display as the table's total.

		Returns:
			str: An HTML string without newlines representing the progeny table.
		"""

		# Define common CSS styles
		styles = {
			'table': 'border-collapse: collapse; border: 2px solid black; width: 400px; height: 220px;',
			'th': 'border: 1px solid black; text-align: center;',
			'td': 'border: 1px solid black; text-align: center;',
			'td_right': 'border: 1px solid black; text-align: right; background: gray; ',
		}

		# Sort the genotype keys
		all_types = sorted(typemap.keys())

		# Build the HTML table with a list to avoid repeated `+=`
		html_output = [
			f'<table style="{styles["table"]}">',
			'  <tr>',
			f'    <th style="{styles["th"]}">Set #</th>',
			f'    <th colspan="4" style="{styles["th"]}">Tetrad Genotypes</th>',
			f'    <th style="{styles["th"]}">Progeny<br/>Count</th>',
			'  </tr>'
		]

		# Sort all genotype pairs (tetrads) for display
		all_tetrads_tuples = sorted(self.list_of_all_tetrads, reverse=True)

		# Initialize tetrad set counter and overall total counter
		total_tetrad_count = 0

		# Loop through sorted genotype pairs to fill the table with tetrads
		for tetrad_set_num, tetrad_tuple in enumerate(all_tetrads_tuples, start=1):
			# Split and format genotype into separate cells if needed
			genotype_cells = " ".join([
				f'<td style="{styles["td"]}">{genotype_part}</td>'
				for genotype_part in genotype.strip().split('\t')
			])

			html_output.append('  <tr>')
			html_output.append(f'    <td style="{styles["td"]}">{tetrad_set_num}</td>')
			html_output.append(f'    {genotype_cells}')
			html_output.append(f'    <td style="{styles["td_right"]}">{typemap[genotype]:,}</td>')
			html_output.append('  </tr>')

		# Add the total row
		html_output.extend([
			'  <tr>',
			f'    <th colspan="5" style="{styles["td_right"]}">TOTAL =</th>',
			f'    <td style="{styles["td_right"]}">{progeny_size:,}</td>',
			'  </tr>',
			'</table>'
		])

		# Join list into a single HTML string with no newlines and return
		return " ".join(html_output)


	#====================================
	#====================================
	def set_progeny_groups_counts(self):
		"""
		Calculates and sets progeny group counts for single, double, and triple crossovers.

		This method:
		1. Determines gene pairs based on their distance (single, double, or triple crossovers).
		2. Calculates raw counts for each crossover type (SCO, DCO, TCO) based on the gene pairs.
		3. Adjusts SCO counts by subtracting DCO counts that overlap with each SCO.
		4. Sets the remaining progeny count as the parental type.

		Raises:
			ValueError: If the total count of all progeny groups does not match the total progeny count.
		"""
		"""
		Example gene map layout:
		A - x - B - y - C
		A - z - C

		Where:
		- `A`, `B`, and `C` represent three genes.
		- `x`, `y`, and `z` represent distances in centiMorgans (cM) between these genes.
		- `x` is the distance between genes A and B.
		- `y` is the distance between genes B and C.
		- `z` is the direct distance between genes A and C, where z >= x + y

		Steps to calculate crossover events for progeny groups:

		1. Determine the `interference_tuple` for each gene pair.
			- The `interference_tuple` is typically represented as a pair of numbers (a, b).
			- Interference is the phenomenon where the occurrence of one crossover event reduces (or enhances) the probability of another crossover happening nearby.
			- The `interference_tuple` modifies the expected crossover frequencies and must be applied to adjust DCO (double crossover) counts accordingly.

		2. Calculate DCO (double crossovers) for relevant gene pairs.
			- `DCO from A-B`: Calculate the double crossovers between genes A and B.
			- `DCO from A-C`: Calculate the double crossovers between genes A and C.
			- Use the `interference_tuple` in these calculations to account for interference effects.

		3. Ensure that DCO counts are integers.
			- Since crossover counts represent actual progeny numbers, they must be integers.
			- After calculating DCO counts, round them and check to ensure they are integers.

		4. Calculate SCO (single crossovers) for adjacent gene pairs and adjust for overlapping DCOs.
			- `determine SCO(x) for A-B genotype pairs, subtract DCO`: Calculate the single crossover count for the distance `x` (between genes A and B).
				- Then subtract any overlapping DCO contributions to avoid double-counting.
			- `determine SCO(y) for B-C genotype pairs, subtract DCO`: Similarly, calculate the single crossover count for the distance `y` (between genes B and C) and adjust by removing overlapping DCO contributions.

		5. Assign remaining progeny counts to the "parental" genotype group.
			- After accounting for all crossover types (SCO, DCO, TCO), any remaining progeny counts are assigned to the parental genotype group, which represents progeny with no crossovers.

		Formula Breakdown (specific to a three-gene scenario):

		For three genes (A, B, and C) with distances `x` and `y`:

		- `dco = Xc * Yc * N * (b - a) / b`
			- `dco`: The expected number of double crossovers between A and C.
			- `Xc` and `Yc`: These are crossover frequencies (proportional to distances x and y, respectively) for A-B and B-C.
			- `N`: Total progeny count.
			- `(b - a) / b`: Interference adjustment factor, where `a` and `b` come from the `interference_tuple`. This factor reduces the expected DCO count based on the level of interference.

		- `sx = N * Xc - dco`
			- `sx`: The adjusted count for single crossovers between genes A and B.
			- This is calculated as the expected count of crossovers based on distance `x` (i.e., `N * Xc`), minus any DCO contributions that overlap with this region.

		- `sy = N * Yc - dco`
			- `sy`: The adjusted count for single crossovers between genes B and C.
			- Similarly, this is the expected count of crossovers based on distance `y` (i.e., `N * Yc`), minus overlapping DCO contributions.

		Terminology:
		- `DCO`: Double Crossover - where two crossovers occur within a single progeny between non-adjacent genes (e.g., A and C).
		- `SCO`: Single Crossover - where a single crossover occurs between adjacent genes (e.g., A-B or B-C).
		- `sx`: The SCO count for the gene pair separated by distance `x`.
		"""

		# Create a dictionary to categorize gene pairs based on their separation (distance)
		# This categorization allows us to separately handle triple crossovers (distance of 3),
		# double crossovers (distance of 2), and single crossovers (distance of 1).

		# Print warning if gene count exceeds three, as functionality is not fully implemented for larger numbers
		if self.num_genes_int > 3:
			print('MORE THAN 3 genes WARNING NOT IMPLEMENTED YET')

		gene_diff_pairs = {}
		for gene1 in range(1, self.num_genes_int):
			for gene2 in range(gene1 + 1, self.num_genes_int + 1):
				diff = gene2 - gene1
				# Add gene pair to the appropriate list in the dictionary based on their distance
				gene_diff_pairs[diff] = gene_diff_pairs.get(diff, []) + [(gene1, gene2)]

		if self.debug:
			print(f'gene_diff_pairs={gene_diff_pairs}')

		# Initialize dictionary to store progeny counts for each crossover type
		self.progeny_groups_count_dict = {}

		# Calculate double crossovers (DCO) for gene pairs separated by one other gene
		for gene_pair in gene_diff_pairs.get(2, []):
			# Example: (1, 3) in a three-gene map would be a double crossover
			self.progeny_groups_count_dict[gene_pair] = self.calculate_double_crossovers(gene_pair)

		# Calculate single crossovers (SCO) for adjacent gene pairs
		for gene_pair in gene_diff_pairs.get(1, []):
			# Example: (1, 2) or (2, 3) in a three-gene map would be single crossovers
			self.progeny_groups_count_dict[gene_pair] = self.calculate_single_crossover(gene_pair)

		# Adjust SCO counts by subtracting overlapping DCO counts
		# Since DCO events contribute to both SCO events on either side, we must remove this overlap.
		for gene_pair in gene_diff_pairs.get(1, []):
			# For each SCO pair, subtract DCO counts associated with the neighboring gene pairs
			# Example: For the SCO pair (1,2), subtract DCO counts from pairs like (1,3) and (2,4)
			for gene_index in gene_pair:
				# Check if the gene index can form a DCO with a gene two positions away
				if gene_index + 2 <= self.num_genes_int:
					new_gene_pair = (gene_index, gene_index + 2)
					self.progeny_groups_count_dict[gene_pair] -= self.progeny_groups_count_dict[new_gene_pair]
				elif gene_index - 2 >= 1:
					new_gene_pair = (gene_index - 2, gene_index)
					self.progeny_groups_count_dict[gene_pair] -= self.progeny_groups_count_dict[new_gene_pair]
		"""
		three gene:
		dco = Xc * Yc * N * (b - a) / b
		sx = N * Xc - dco
		sy = N * Yc - dco
		"""
		import pprint
		pprint.pprint(self.progeny_groups_count_dict)

		#sys.exit(1)
		# Calculate the count for parental genotypes as the remainder after accounting for all crossovers
		# The parental count is the remaining progeny count after accounting for single, double, and triple crossovers.
		parent_count_int = self.progeny_count_int - sum(self.progeny_groups_count_dict.values())
		self.progeny_groups_count_dict['parental'] = parent_count_int

		# Verify that the total progeny counts match the expected progeny count
		total_count = sum(self.progeny_groups_count_dict.values())
		if total_count != self.progeny_count_int:
			raise ValueError(f'counts do not add up {total_count} vs expected {self.progeny_count_int}')

		pprint.pprint(self.progeny_groups_count_dict)
		return


	#====================================
	#====================================
	def set_tetrad_counts(self):
		self.progeny_tetrads_count_dict = {}

		self.parental_tetrad = random.choice(self.list_of_ditypes)
		#keep this while loop as an alternate system to consider...
		#while len(self.list_of_ditypes) > 3 and set(self.parental_tetrad[0]) == {'+'}:
		if set(self.parental_tetrad[0]) == {'+'}:
			#make it less likely to have all three '+'
			self.parental_tetrad = random.choice(self.list_of_ditypes)
		if self.debug is True:
			print(f"parental_tetrad = {self.parental_tetrad}")
		self.progeny_tetrads_count_dict[self.parental_tetrad] = self.progeny_groups_count_dict['parental']

		#question 1: which tetratypes are SCO from the parental???
		list_of_sco_tetratypes = tetradlib.get_all_single_crossovers_for_ditype_tetrad(self.parental_tetrad, self.gene_letters_str)
		print(list_of_sco_tetratypes)

#===========================================================
#===========================================================
#===========================================================
#===========================================================
#===========================================================

if __name__ == '__main__':
	# Testing the TetradMappingClass with various numbers of genes
	a = TetradMappingClass(2, 1)
	a.unlinked = True
	a.debug = True
	a.setup_question()
	a.print_gene_map_data()

	# Testing with 3 genes
	a = TetradMappingClass(3, 1)
	a.debug = True
	a.setup_question()
	a.print_gene_map_data()
	print(a.get_question_header())
	print(a.get_progeny_ascii_table())

	# Testing with 4 genes
	a = TetradMappingClass(4, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()


