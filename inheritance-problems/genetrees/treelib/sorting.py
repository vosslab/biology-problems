
import math

try:
	from treelib import tools
except ImportError:
	import tools

### ONLY ALLOWED TO IMPORT tools NOT OTHER TREELIB FILES

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

	if map1 == map2:
		return 1.0

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
	taxa_distance_map1 = tools.generate_taxa_distance_map(tree_code1)
	taxa_distance_map2 = tools.generate_taxa_distance_map(tree_code2)
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
	answer_distance_map = tools.generate_taxa_distance_map(answer_code)

	# Compute similarity scores for each tree
	tree_scores = []
	for tree_code in tree_codes:
		tree_distance_map = tools.generate_taxa_distance_map(tree_code)
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
	import definitions
	all_codes = list(definitions.code_library.values())
	tree_code = random.choice(all_codes)
	print(f"tree_code = {tree_code}")
	taxa_distance_map = tools.generate_taxa_distance_map(tree_code)
	pprint.pprint(taxa_distance_map)
	compare_tree_codes('(((a1b)3c)4(d2e))', '(((a2b)3c)4(d1e))')
	compare_tree_codes('((((a1b)2c)3d)4e)', '(((a2b)3c)4(d1e))')
