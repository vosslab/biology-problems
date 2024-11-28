
import re
import math

try:
	from treelib import tools
except ImportError:
	import tools

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
assert get_highest_number('))4((g8h)7') == 8

#===========================================================
#===========================================================
def find_node_number_for_taxa_pair(tree_code, taxon1, taxon2):
	"""
	Finds the connecting internal node number (LCA) between two taxa in a tree structure.

	In this representation, the connecting internal node (lowest common ancestor, LCA)
	is identified as the highest internal node number found between the two specified
	taxa. The tree structure is provided as a string, where:
	  - Taxa (leaves) are represented by alphabetic characters.
	  - Internal nodes are denoted by numeric labels.

	Args:
		tree_code (str): A string representing the tree structure, where alphabetic
			characters represent taxa (leaves) and numeric characters represent
			internal nodes.
		taxon1 (str): The first taxon (leaf) to analyze.
		taxon2 (str): The second taxon (leaf) to analyze.

	Returns:
		int: The connecting internal node number (LCA) between the two taxa, or -1 if no
			internal node is found between them.
	"""

	# Locate the positions of the two taxa in the tree string
	index1 = tree_code.find(taxon1)
	index2 = tree_code.find(taxon2)

	# Ensure both taxa are found in the string
	if index1 == -1 or index2 == -1:
		raise ValueError(f"One or both taxa not found in the tree_code: {taxon1}, {taxon2}")

	# Determine the substring between the two taxa
	min_index = min(index1, index2)
	max_index = max(index1, index2)
	substring = tree_code[min_index + 1:max_index]

	# Extract the highest internal node number from the substring
	max_internal_node = get_highest_number(substring)

	return max_internal_node
assert find_node_number_for_taxa_pair("((a1b)2c)", "a", "c") == 2

#===========================================================
#===========================================================
def generate_taxa_distance_map(tree_code: str) -> dict:
	"""
	Generates a map of distances between all pairs of taxa in a tree.

	Args:
		tree_code (str): The tree code.

	Returns:
		dict: A dictionary where keys are taxon pairs (tuples), and values are distances.
	"""
	# Extract ordered taxa from the tree code
	ordered_taxa = tools.code_to_taxa_list(tree_code)

	# Initialize a dictionary to store distances between taxon pairs
	taxa_distance_map = {}

	# Loop through all pairs of taxa
	for i, taxon1 in enumerate(ordered_taxa):
		for j, taxon2 in enumerate(ordered_taxa):
			# Only consider pairs where taxon1 comes after taxon2
			if taxon1 <= taxon2:
				continue

			# Find the internal node connecting the two taxa
			internal_node_number = find_node_number_for_taxa_pair(tree_code, taxon1, taxon2)

			# Retrieve the distance from the list and store it in both pair directions
			taxa_distance_map[(taxon2, taxon1)] = internal_node_number

	return taxa_distance_map
assert generate_taxa_distance_map('(a1b)') == {('a', 'b'): 1}

#===========================================================
#===========================================================
def compare_taxa_distance_maps(map1: dict, map2: dict) -> float:
	"""
	Compares two taxa distance maps and calculates a closeness score.

	Args:
		map1 (dict): The first taxa distance map.
		map2 (dict): The second taxa distance map.

	Returns:
		float: A closeness score, where higher values indicate greater similarity.
	"""
	# Ensure both maps cover the same taxon pairs
	if set(map1.keys()) != set(map2.keys()):
		raise ValueError("The two distance maps must have the same taxon pairs.")

	score = 0
	for pair in map1:
		# Calculate the absolute difference in distances for each taxon pair
		diff = abs(map1[pair] - map2[pair])
		score += 1 / (1 + diff)  # Inverse weighting: closer distances contribute more

	# Normalize the score
	final_score = score / len(map1)

	# Ensure the score is within the valid range
	if not (0 <= final_score <= 1):
		raise ValueError(f"Invalid similarity score: {final_score}. Expected a value between 0 and 1.")

	return  final_score

#===========================================================
#===========================================================
def compare_tree_codes(tree_code1: str, tree_code2: str) -> float:
	taxa_distance_map1 = generate_taxa_distance_map(tree_code1)
	taxa_distance_map2 = generate_taxa_distance_map(tree_code2)
	#print(f"taxa_distance_map1 = {taxa_distance_map1}")
	#print(f"taxa_distance_map2 = {taxa_distance_map2}")
	score = compare_taxa_distance_maps(taxa_distance_map1, taxa_distance_map2)
	#print(f"score = {score}")
	return score
assert compare_tree_codes('(((a1b)3c)4(d2e))', '(((a2b)3c)4(d1e))') == 0.9
assert compare_tree_codes('((((a1b)2c)3d)4e)', '(((a2b)3c)4(d1e))') == 0.625

#===========================================================
#===========================================================
def tree_codes_match(tree_code1: str, tree_code2: str) -> bool:
	"""
	Determines if two tree codes are identical based on their similarity score.
	"""
	score = compare_tree_codes(tree_code1, tree_code2)
	return math.isclose(score, 1.0, abs_tol=1e-6)
assert tree_codes_match('((a1b)2c)', '(c2(a1b))') is True

#===========================================================
#===========================================================
def sort_tree_codes_by_taxa_distances(tree_codes: list, answer_code: str) -> list:
	"""
	Sorts a list of tree codes by their closeness to an answer tree code.

	Args:
		tree_codes (list): A list of tree codes to compare.
		answer_code (str): The reference tree code.

	Returns:
		list: The tree codes sorted by closeness to the answer code.
	"""
	# Generate the distance map for the answer code
	answer_distance_map = generate_taxa_distance_map(answer_code)

	# Compute similarity scores for each tree
	tree_scores = []
	for tree_code in tree_codes:
		tree_distance_map = generate_taxa_distance_map(tree_code)
		score = compare_taxa_distance_maps(answer_distance_map, tree_distance_map)
		tree_scores.append((tree_code, score))

	# Sort by scores in descending order
	tree_scores.sort(key=lambda x: x[1], reverse=True)

	# Return the sorted tree codes
	return [tree for tree, score in tree_scores]

#===========================================
#===========================================
if __name__ == '__main__':
	import random
	import pprint
	import treecodes
	all_codes = list(treecodes.code_library.values())
	tree_code = random.choice(all_codes)
	print(f"tree_code = {tree_code}")
	taxa_distance_map = generate_taxa_distance_map(tree_code)
	pprint.pprint(taxa_distance_map)
	compare_tree_codes('(((a1b)3c)4(d2e))', '(((a2b)3c)4(d1e))')
	compare_tree_codes('((((a1b)2c)3d)4e)', '(((a2b)3c)4(d1e))')
