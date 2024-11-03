#!/usr/bin/env python3


# Built-in libraries
import copy
import math
import random

# Local libraries
import bptools
import genemaplib as gml
import genemapclass as gmc

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

	def __init__(self, num_genes_int: int, question_count: int = 1, debug: bool = False) -> None:
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
		super().__init__(num_genes_int, question_count, debug)

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
		# Column 1: fixed 8 characters wide
		# Column 2: variable width based on the number of genes
		# Column 3: fixed 9 characters wide

		# Calculate the dynamic width for the "Genotypes of Spore in Tetrads" column
		genotypes_col_width = 4 * self.num_genes_int + 5  # 4 characters per genotype plus 5 spaces between them
		if genotypes_col_width < 14:
			genotypes_col_width = 14

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
		table = top_border + header + separator

		# Sort all genotype pairs (tetrads) for display
		all_genotype_pairs = sorted(self.all_genotype_tuple_pairs_list, reverse=True)

		# Initialize tetrad set counter and overall total counter
		total_tetrad_count = 0

		# Loop through sorted genotype pairs to fill the table with tetrads
		for tetrad_set_num, (genotype1, genotype2) in enumerate(all_genotype_pairs, start=1):
			# Each tetrad has four spores: two of genotype1 and two of genotype2
			spores = [genotype1, genotype1, genotype2, genotype2]
			genotypes_str = " ".join(spores)

			# Calculate tetrad count and add to total
			tetrad_count = self.genotype_counts[genotype1] + self.genotype_counts[genotype2]
			total_tetrad_count += tetrad_count

			# Format columns with appropriate alignment
			tetrad_set_str = f"    {tetrad_set_num}   "  # Centered tetrad set number, by rule number is a single digit
			tetrad_count_str = gml.right_justify_int(tetrad_count, 8)  # Right-aligned with thousands comma

			# Add row to the table
			table += f"{vertical_line}{tetrad_set_str}{vertical_line} {genotypes_str:<{genotypes_col_width-2}} {vertical_line}{tetrad_count_str} {vertical_line}\n"

		# Add bottom separator and total row
		table += separator
		total_str = gml.right_justify_int(total_tetrad_count, 8)
		table += f"{vertical_line}{'TOTAL':^8}{vertical_line}{' ' * genotypes_col_width}{vertical_line}{total_str} {vertical_line}\n"
		table += bottom_border

		return table

#===========================================================
#===========================================================
#===========================================================
#===========================================================
#===========================================================

if __name__ == '__main__':
	# Testing the TetradMappingClass with various numbers of genes
	a = TetradMappingClass(2, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()

	# Testing with 4 genes
	a = TetradMappingClass(4, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()

	# Testing with 3 genes
	a = TetradMappingClass(3, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()
	print(a.get_question_header())
	print(a.get_progeny_ascii_table())
