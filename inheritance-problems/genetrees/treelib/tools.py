#!/usr/bin/env python3

import re
import copy
import itertools

#===========================================
#===========================================
def get_comb_safe_taxa_permutations(taxa):
	# Sort the items to generate consistent permutations
	taxa_list = sorted(taxa)
	# Generate all permutations of the items
	permuations_list = list(itertools.permutations(taxa_list, len(taxa_list)))
	# Initialize a list to store combination-safe permutations
	comb_safe_permutations_list = []
	# Iterate through all permutations
	for p in permuations_list:
		# Create a swapped version of the first two elements
		swapped = (p[1], p[0]) + p[2:]
		# Check if the swapped version is not already in the list
		if swapped not in comb_safe_permutations_list:
			# Add the original permutation if it is combination-safe
			comb_safe_permutations_list.append(p)
	return comb_safe_permutations_list
result = get_comb_safe_taxa_permutations('abc')
assert len(result) == 3, "Test failed: Expected 3 safe permutations"
assert ("a", "b", "c") in result, "Test failed: ('a', 'b', 'c') should be in the result"
assert ("b", "a", "c") not in result, "Test failed: ('b', 'a', 'c') should NOT be in the result"

#===========================================
#===========================================
def code_to_taxa_list(tree_code):
	# Split the tree_code by non-alphabetic characters using regex
	re_list = re.split("[^a-zA-Z]+", tree_code)
	# Filter out empty strings caused by consecutive non-alphabetic characters
	taxa_list = list(filter(None, re_list))
	return taxa_list
assert code_to_taxa_list('(((a2b)3c)4(d1e))') == list('abcde')

#===========================================
#===========================================
def code_to_number_of_taxa(tree_code):
	# Extract the alphabetic nodes and return their count
	return len(code_to_taxa_list(tree_code))
assert code_to_number_of_taxa('(((a2b)3c)5((d1e)4f))') == 6

#===========================================
#===========================================
def code_to_internal_node_list(tree_code):
	# Split the tree_code by non-numeric characters using regex
	re_list = re.split("[^0-9]+", tree_code)
	# Filter out empty strings caused by consecutive non-numeric characters
	internal_node_list = list(filter(None, re_list))
	return internal_node_list
assert code_to_internal_node_list('((((a1b)2c)4(d3e))5f)') == list('12435')

#===========================================
#===========================================
def code_to_number_of_internal_nodes(tree_code):
	# Extract the numeric internal nodes and return their count
	return len(code_to_internal_node_list(tree_code))
assert code_to_number_of_internal_nodes('((((a1b)2c)4(d3e))7((f5g)6h))') == 7

#===========================================
#===========================================
def is_gene_tree_alpha_sorted(tree_code):
	internal_nodes_list = code_to_internal_node_list(tree_code)
	for internal_node_num in internal_nodes_list:
		internal_node_index = tree_code.find(str(internal_node_num))
		before_char = tree_code[internal_node_index-1]
		if not before_char.isalpha():
			continue
		after_char = tree_code[internal_node_index+1]
		if not after_char.isalpha():
			continue
		if before_char >= after_char:
			return False
	return True
assert is_gene_tree_alpha_sorted('((((a1b)2c)3d)5(e4f))') == True
assert is_gene_tree_alpha_sorted('(((a1b)2c)5((e3d)4f))') == False

#===========================================
#===========================================
def sort_alpha_for_gene_tree(tree_code):
	# Validate num_nodes
	internal_nodes_list = code_to_internal_node_list(tree_code)

	# Convert code into a mutable list for manipulation
	new_code_list = list(tree_code)

	for internal_node_num in internal_nodes_list:
		internal_node_index = tree_code.find(str(internal_node_num))  # Find the position of the node in the string
		if internal_node_index == -1:
			raise ValueError(f"{internal_node_num} not in {tree_code}")

		before_char = tree_code[internal_node_index-1]
		if not before_char.isalpha():
			continue
		after_char = tree_code[internal_node_index+1]
		if not after_char.isalpha():
			continue
		if before_char >= after_char:
			# Swap positions in the new_code_list
			new_code_list[internal_node_index-1] = after_char
			new_code_list[internal_node_index+1] = before_char

	# Reconstruct and return the updated string
	new_code_str = ''.join(new_code_list)
	return new_code_str
assert sort_alpha_for_gene_tree('((b1a)3(d2c))') == '((a1b)3(c2d))'

#===========================================
#===========================================
def replace_gene_letters(tree_code, ordered_taxa):
	# Get the number of leaves in the tree
	num_leaves = code_to_number_of_taxa(tree_code)

	# Validate input
	if num_leaves != len(ordered_taxa):
		raise ValueError(f"Mismatch: {num_leaves} leaves in tree_code but {len(ordered_taxa)} taxa provided.")

	# Extract default gene labels from the tree tree_code
	default_gene_labels = code_to_taxa_list(tree_code)

	# Create mappings for old labels to placeholders and placeholders to final labels
	old_to_placeholder_map = {}
	placeholder_to_new_map = {}
	for i, (old_label, new_label) in enumerate(zip(default_gene_labels, ordered_taxa)):
		placeholder_str = f"__PLACEHOLDER_{i}__"  # Unique placeholder for each old label
		# Add delimiters for multi-character gene names
		final_new_label = f"|{new_label}|" if len(new_label) > 1 else new_label
		#print(f"Mapping {old_label} -> {new_label} with placeholder {placeholder_str}")
		old_to_placeholder_map[old_label] = placeholder_str
		placeholder_to_new_map[placeholder_str] = final_new_label

	# Step 1: Replace old labels with placeholders
	new_code = copy.copy(tree_code)
	for old_label, placeholder in old_to_placeholder_map.items():
		new_code = new_code.replace(old_label, placeholder)

	# Step 2: Replace placeholders with final new labels
	for placeholder, new_label in placeholder_to_new_map.items():
		new_code = new_code.replace(placeholder, new_label)

	# Sort the gene tree for consistency
	new_code = sort_alpha_for_gene_tree(new_code)

	return new_code
assert replace_gene_letters('(((a1b)2c)4(d3e))', 'ZYXWV') == '(((Y1Z)2X)4(V3W))'

#===========================================
#===========================================
if __name__ == '__main__':
	import random
	import treecodes
	all_codes = list(treecodes.code_library.values())
	tree_code = random.choice(all_codes)
	print(f"tree_code = {tree_code}")
	num_taxa = code_to_number_of_taxa(tree_code)
	print(f"num_taxa = {num_taxa}")
	taxa_list = code_to_taxa_list(tree_code)
	print(f"taxa_list = {taxa_list}")
	num_internal_nodes = code_to_number_of_internal_nodes(tree_code)
	print(f"num_internal_nodes = {num_internal_nodes}")
	internal_node_list = code_to_internal_node_list(tree_code)
	print(f"internal_node_list = {internal_node_list}")
	is_sorted = is_gene_tree_alpha_sorted(tree_code)
	print(f"is_gene_tree_alpha_sorted = {is_sorted}")
	sorted_code = sort_alpha_for_gene_tree(tree_code)
	print(f"sorted should be same = {sorted_code == tree_code}")
	replaced_code = replace_gene_letters(tree_code, 'ZYXWVUTSR'[:num_taxa])
	print(f"replaced_code = {replaced_code}")

