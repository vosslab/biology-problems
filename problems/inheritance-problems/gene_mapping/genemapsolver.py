#!/usr/bin/env python3

import math
import itertools
import genemaplib as gml

debug = False

#====================================
#====================================
def get_gene_distance(gene_pair: tuple, parental_types: tuple, genotype_counts: dict, gene_letters: str, progeny_size: int) -> float:
	# Identify which genes are NOT in the pair (i.e., unused genes)
	gene_index1 = gene_letters.find(gene_pair[0])
	gene_index2 = gene_letters.find(gene_pair[1])

	# Add them to the list of recombinants
	recombinants = []
	for genotype in genotype_counts.keys():
		for ptype in parental_types:
			if genotype[gene_index1] == ptype[gene_index1] and genotype[gene_index2] != ptype[gene_index2]:
				recombinants.append(genotype)

	sum_progeny = 0
	for recomb in recombinants:
		sum_progeny += genotype_counts[recomb]
	if debug is True:
		print(f'sum_progeny = {sum_progeny} over {progeny_size}')
	distance = sum_progeny*100.0/float(progeny_size)
	if gml.is_almost_integer(distance):
		distance = int(round(distance))
	if debug is True:
		print(f'distance = {distance} for {gene_pair}')
	return distance

#====================================
#====================================
def get_gene_order(distances_dict: dict) -> str:
	sorted_distances = sorted(distances_dict.items(), key=lambda x: x[1], reverse=True)
	if len(sorted_distances) == 1:
		return ''.join(sorted(sorted_distances[0][0]))
	further_gene_letters = sorted_distances[0][0]
	closest_gene_letters = sorted_distances[-1][0]
	common_letter = set(further_gene_letters).intersection(closest_gene_letters).pop()
	other_further_gene_letter = (set(further_gene_letters) - {common_letter}).pop()
	other_closest_gene_letter = (set(closest_gene_letters) - {common_letter}).pop()
	if len(sorted_distances) == 3:
		gene_order = common_letter + other_closest_gene_letter + other_further_gene_letter
	return gene_order

#====================================
#====================================
def gene_map_solver(genotype_counts: dict) -> str:
	"""
	Find recombinants based on genotype_counts.

	Parameters
	----------
	genotype_counts : dict
		Dictionary containing genotype (keys) and their progeny counts (values).
	"""
	# progeny_size = Total number of progenies: int
	progeny_size = sum(genotype_counts.values())
	if debug is True:
		print(f'progeny_size = {progeny_size}')

	# gene_letters String containing all of the gene letters.
	sorted_genotype_names = sorted(genotype_counts.keys(), reverse=True)
	gene_letters = ''.join(sorted_genotype_names[0])
	if debug is True:
		print(f'gene_letters = {gene_letters}')
	if '+' in gene_letters:
		raise ValueError(f'Cound not find true gene_leters, {gene_letters}')

	sorted_genotype_counts = sorted(genotype_counts.items(), key=lambda x: x[1], reverse=True)
	if debug is True:
		print(f'sorted_genotype_counts = {sorted_genotype_counts}')
	parental_types = (sorted_genotype_counts[0][0], sorted_genotype_counts[1][0])
	if debug is True:
		print(f'parental_types = {parental_types}')
	observed_dco = (sorted_genotype_counts[-1][1] + sorted_genotype_counts[-2][1])
	if debug is True:
		print(f'observed_double_crossovers = {observed_dco}')

	# Generate all unique combinations of two genes
	gene_pairs = list(itertools.combinations(gene_letters, 2))
	if debug is True:
		print(f'gene_pairs = {gene_pairs}')

	distances_dict = {}
	distances_list = []
	for gene_pair in gene_pairs:
		distance = get_gene_distance(gene_pair, parental_types, genotype_counts, gene_letters, progeny_size)
		distances_dict[gene_pair] = distance
		distances_list.append(distance)
	if debug is True:
		print(f'distances_dict = {distances_dict}')

	oberserved_gene_order = get_gene_order(distances_dict)
	if debug is True:
		print(f'oberserved_gene_order = {oberserved_gene_order}')

	if len(gene_letters) == 2:
		observed_interference_tuple = None
	elif len(gene_letters) == 3:
		distances_list.sort()
		calc_interference_tuple = gml.calculate_interference_from_three_distances(*distances_list)
		predict_dist = gml.calculate_third_distance(distances_list[0], distances_list[1], calc_interference_tuple)
		expected_dco = distances_list[0]*distances_list[1]*progeny_size/10000.
		if debug is True:
			print(f'expected_double_crossovers = {expected_dco}')
			print(f'distances=({distances_list[1]:.0f}, {distances_list[0]:.0f}) and {distances_list[2]:.3f} vs {predict_dist:.1f})')
		if abs(distances_list[2] - predict_dist) > 1e-6:
			print(f'distances=({distances_list[1]:.0f}, {distances_list[0]:.0f}) and {distances_list[2]:.3f} vs {predict_dist:.1f})')
			raise ValueError("Distance values are off?!?")
		observed_dco_star = int(round(observed_dco*100))
		expected_dco_star = int(round(expected_dco*100))
		gcd = math.gcd((expected_dco_star-observed_dco_star), expected_dco_star)
		observed_interference_tuple = ((expected_dco_star-observed_dco_star)//gcd, expected_dco_star//gcd)
		if debug is True:
			print(f'observed_interference_tuple = {observed_interference_tuple}')
			print(f'calc_interference_tuple = {calc_interference_tuple}')
		if observed_interference_tuple != calc_interference_tuple:
			print(f'observed_interference_tuple = {observed_interference_tuple}')
			print(f'calc_interference_tuple = {calc_interference_tuple}')
			raise ValueError("interferences values are off?!?")
	else:
		observed_interference_tuple = None
	return distances_list, observed_interference_tuple, oberserved_gene_order

#====================================
#====================================
def test_two_genes():
	import genemapclass as gmc
	# two genes
	a = gmc.GeneMappingClass(2, debug=debug)
	gml.debug = debug
	a.setup_question()
	if debug is True:
		a.print_gene_map_data()
	observed_distances_list, observed_interference_tuple, oberserved_gene_order = gene_map_solver(a.genotype_counts)
	original_distances_list = list(a.distances_dict.values())
	original_distances_list.sort()
	if  observed_distances_list != original_distances_list:
		print(observed_distances_list, original_distances_list)
		raise ValueError
	if  observed_interference_tuple != None:
		print(observed_interference_tuple)
		raise ValueError
	original_gene_order = a.gene_order_str
	if sorted(original_gene_order) != sorted(oberserved_gene_order):
		print(original_gene_order, oberserved_gene_order)
		raise ValueError

#====================================
#====================================
def test_three_genes():
	import genemapclass as gmc
	# three genes
	a = gmc.GeneMappingClass(3, debug=debug)
	gml.debug = debug
	a.setup_question()
	if debug is True:
		a.print_gene_map_data()
	observed_distances_list, observed_interference_tuple, oberserved_gene_order = gene_map_solver(a.genotype_counts)
	original_distances_list = list(a.distances_dict.values())
	original_distances_list.sort()
	if  observed_distances_list != original_distances_list:
		print(observed_distances_list, original_distances_list)
		raise ValueError
	original_interference_tuple = a.interference_dict[(1,3)]
	if  observed_interference_tuple != original_interference_tuple:
		print(observed_interference_tuple, original_interference_tuple)
		raise ValueError
	original_gene_order = a.gene_order_str
	if sorted(original_gene_order) != sorted(oberserved_gene_order):
		print(original_gene_order, oberserved_gene_order)
		raise ValueError

if __name__ == '__main__':
	num_tests = 1000
	for i in range(num_tests):
		test_two_genes()
	for i in range(num_tests):
		test_three_genes()

