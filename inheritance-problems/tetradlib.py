
# Standard Library Imports
import re
import sys
import copy
import math
import random
import random

# Local Repository Modules
import genemaplib as gml

# Global debug flag
debug = True

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
