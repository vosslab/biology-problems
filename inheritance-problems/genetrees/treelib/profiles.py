import sys
import random
from collections import defaultdict

import tools

#===========================================
def gene_tree_code_to_profile(code: str, num_nodes: int = None):
	"""
	Generates a profile for a gene tree code.

	This method creates a profile string to compare tree structures efficiently.
	If two trees have different profiles, they are guaranteed to be different.
	If two trees have the same profile, they might be the same or different
	(since the profile is not a unique identifier for tree topology).

	Args:
		code (str): The gene tree code representing the tree structure.
		num_nodes (int, optional): The number of internal nodes in the tree.
			If not provided, it is calculated using `code_to_number_of_internal_nodes`.

	Returns:
		str: The profile string of the tree.
	"""
	# Determine the number of internal nodes if not provided
	if num_nodes is None:
		num_nodes = tools.code_to_number_of_internal_nodes(code)

	# Build a mapping of internal nodes to their associated taxa
	code_dict = defaultdict(list)  # Default value for new keys is an empty list
	for i in range(num_nodes):
		node_num = i + 1
		node_index = code.find(str(node_num))

		# Check preceding and following characters for associated taxa
		if code[node_index - 1].isalpha():
			code_dict[node_num].append(code[node_index - 1])
		if code[node_index + 1].isalpha():
			code_dict[node_num].append(code[node_index + 1])

	# Generate the profile string
	profile = ""
	keys = sorted(code_dict.keys())
	for key in keys:
		profile += str(key)
		values = sorted(code_dict[key])
		profile += ''.join(values)

	# Debugging: Uncomment to see the intermediate results
	# print(f"Code: {code}, Code Dict: {code_dict}, Profile: {profile}")
	return profile

#===========================================
def group_gene_trees_by_profile(gene_tree_codes, num_nodes):
	if num_nodes is None:
		num_nodes = tools.code_to_number_of_internal_nodes(gene_tree_codes[0])
	gene_tree_profile_groups = {}
	for code in gene_tree_codes:
		profile = gene_tree_code_to_profile(code, num_nodes)
		gene_tree_profile_groups[profile] = gene_tree_profile_groups.get(profile, []) + [code,]
	print(f"{len(gene_tree_profile_groups)} profile groups were formed")
	return gene_tree_profile_groups

#===========================================
def sort_profiles_by_closeness(profile_groups, answer_profile):
	similar_scores = {}
	if '(' in answer_profile:
		print("ERROR: wanted profile, but received code")
		print(answer_profile)
		sys.exit(1)
	profile_group_keys = list(profile_groups.keys())
	random.shuffle(profile_group_keys)
	for profile in profile_groups.keys():
		score = string_match(profile, answer_profile)
		similar_scores[profile] = score
	sorted_profile_group_keys = [k for k in sorted(similar_scores.keys(), key=similar_scores.get, reverse=True)]
	return sorted_profile_group_keys

#===========================================
def sort_codes_by_closeness(code_list, answer_code):
	"""
	has not been thoroughly tested
	"""
	similar_scores = {}
	if not '(' in answer_code:
		print("ERROR: wanted code, but received profile")
		print(answer_code)
		sys.exit(1)
	for code in code_list:
		score = string_match(code, answer_code)
		similar_scores[code] = score
	sorted_codes = [k for k in sorted(code_list, key=similar_scores.get, reverse=True)]
	return sorted_codes

#===========================================
def string_match(str1, str2):
	minlen = min(len(str1), len(str2))
	count = 0
	count_step = 10
	list1 = list(str1)
	list2 = list(str2)
	for i in range(minlen):
		if list1[i] != list2[i]:
			count_step = 1
		count += count_step
	return count

if __name__ == '__main__':
	import treecodes
	all_codes = list(treecodes.code_library.values())
	tree_code = random.choice(all_codes)
	print(f"tree_code = {tree_code}")
	profile = gene_tree_code_to_profile(tree_code)
	print(f"profile = {profile}")
