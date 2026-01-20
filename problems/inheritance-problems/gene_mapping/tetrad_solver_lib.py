
import itertools

import genemaplib as gml

debug = False

#====================================
#====================================
def infer_gene_letters_str(progeny_tetrads_count_dict: dict) -> str:
	if progeny_tetrads_count_dict is None or len(progeny_tetrads_count_dict) == 0:
		raise ValueError("Missing progeny tetrads count dictionary.")
	first_tetrad = next(iter(progeny_tetrads_count_dict))
	if len(first_tetrad) == 0:
		raise ValueError("Empty tetrad tuple.")
	genotype_len = len(first_tetrad[0])
	gene_letters = [""] * genotype_len
	for tetrad_tuple in progeny_tetrads_count_dict.keys():
		for genotype_str in tetrad_tuple:
			if len(genotype_str) != genotype_len:
				raise ValueError("Genotype lengths are not consistent.")
			for index, allele in enumerate(genotype_str):
				if allele == "+":
					continue
				if gene_letters[index] == "":
					gene_letters[index] = allele
				elif gene_letters[index] != allele:
					raise ValueError("Conflicting gene letters for position.")
	if "" in gene_letters:
		raise ValueError("Could not determine gene letters for all positions.")
	return "".join(gene_letters)

#====================================
#====================================
def get_pair_genotypes_from_tetrad(tetrad_tuple: tuple, gene_index_pair: tuple) -> list:
	i, j = gene_index_pair
	pair_genotypes = []
	for genotype_str in tetrad_tuple:
		if len(genotype_str) <= max(i, j):
			raise ValueError("Genotype string shorter than gene index.")
		pair_genotypes.append(genotype_str[i] + genotype_str[j])
	return pair_genotypes

#====================================
#====================================
def classify_pair_tetrad(pair_genotypes: list) -> tuple:
	genotype_counts = {}
	for genotype_str in pair_genotypes:
		genotype_counts[genotype_str] = genotype_counts.get(genotype_str, 0) + 1
	unique_count = len(genotype_counts)
	if unique_count == 2 and sorted(genotype_counts.values()) == [2, 2]:
		ditype_key = tuple(sorted(genotype_counts.keys()))
		return "ditype", ditype_key
	if unique_count == 4:
		return "tetratype", None
	raise ValueError("Unexpected tetrad pattern for gene pair.")

#====================================
#====================================
def get_pair_tetrad_counts(progeny_tetrads_count_dict: dict, gene_index_pair: tuple) -> tuple:
	tt_count = 0
	ditype_counts = {}
	for tetrad_tuple, tetrad_count in progeny_tetrads_count_dict.items():
		pair_genotypes = get_pair_genotypes_from_tetrad(tetrad_tuple, gene_index_pair)
		tetrad_type, ditype_key = classify_pair_tetrad(pair_genotypes)
		if tetrad_type == "tetratype":
			tt_count += tetrad_count
			continue
		ditype_counts[ditype_key] = ditype_counts.get(ditype_key, 0) + tetrad_count
	if len(ditype_counts) != 2:
		raise ValueError("Expected exactly two ditype classes for a gene pair.")
	ditype_values = sorted(ditype_counts.values())
	npd_count = ditype_values[0]
	pd_count = ditype_values[1]
	return tt_count, npd_count, pd_count, ditype_counts

#====================================
#====================================
def calculate_distance_from_counts(tt_count: int, npd_count: int, total_tetrads: int) -> float:
	distance = (0.5 * tt_count + 3 * npd_count) / float(total_tetrads) * 100.0
	if gml.is_almost_integer(distance):
		return int(round(distance))
	return distance

#====================================
#====================================
def get_gene_order_from_distances(distance_map: dict) -> str:
	if len(distance_map) != 3:
		raise ValueError("Expected exactly three distances for gene order.")
	if len(set(distance_map.values())) != len(distance_map.values()):
		all_letters = sorted(set("".join(distance_map.keys())))
		return "".join(all_letters)
	sorted_distances = sorted(distance_map.items(), key=lambda x: x[1], reverse=True)
	furthest_pair = sorted_distances[0][0]
	closest_pair = sorted_distances[-1][0]
	common_letter = set(furthest_pair).intersection(closest_pair).pop()
	other_furthest = (set(furthest_pair) - {common_letter}).pop()
	other_closest = (set(closest_pair) - {common_letter}).pop()
	gene_order = common_letter + other_closest + other_furthest
	return gene_order.lower()

#====================================
#====================================
def solve_unordered_tetrad_three_gene(progeny_tetrads_count_dict: dict, gene_letters_str: str=None) -> tuple:
	if gene_letters_str is None:
		gene_letters_str = infer_gene_letters_str(progeny_tetrads_count_dict)
	gene_letters_str = gene_letters_str.lower()
	total_tetrads = sum(progeny_tetrads_count_dict.values())
	if total_tetrads <= 0:
		raise ValueError("Total tetrad count must be positive.")
	pair_distance_map = {}
	pair_details = {}
	for gene_index_pair in itertools.combinations(range(len(gene_letters_str)), 2):
		tt_count, npd_count, pd_count, ditype_counts = get_pair_tetrad_counts(
			progeny_tetrads_count_dict, gene_index_pair
		)
		distance = calculate_distance_from_counts(tt_count, npd_count, total_tetrads)
		gene1 = gene_letters_str[gene_index_pair[0]]
		gene2 = gene_letters_str[gene_index_pair[1]]
		pair_key = "".join(sorted((gene1, gene2))).upper()
		pair_distance_map[pair_key] = distance
		pair_details[pair_key] = {
			"tt": tt_count,
			"npd": npd_count,
			"pd": pd_count,
			"ditype_counts": ditype_counts,
		}
	if debug:
		print(f"pair_distance_map={pair_distance_map}")
		print(f"pair_details={pair_details}")
	gene_order_str = get_gene_order_from_distances(pair_distance_map)
	return pair_distance_map, gene_order_str, pair_details

