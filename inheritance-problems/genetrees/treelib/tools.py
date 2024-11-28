#!/usr/bin/env python3

import re
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
def code_to_taxa_list(code):
	# Split the code by non-alphabetic characters using regex
	re_list = re.split("[^a-zA-Z]+", code)
	# Filter out empty strings caused by consecutive non-alphabetic characters
	taxa_list = list(filter(None, re_list))
	return taxa_list
assert code_to_taxa_list('(((a2b)3c)4(d1e))') == list('abcde')

#===========================================
#===========================================
def code_to_number_of_taxa(code):
	# Extract the alphabetic nodes and return their count
	return len(code_to_taxa_list(code))
assert code_to_number_of_taxa('(((a2b)3c)5((d1e)4f))') == 6

#===========================================
#===========================================
def code_to_internal_node_list(code):
	# Split the code by non-numeric characters using regex
	re_list = re.split("[^0-9]+", code)
	# Filter out empty strings caused by consecutive non-numeric characters
	internal_node_list = list(filter(None, re_list))
	return internal_node_list
assert code_to_internal_node_list('((((a1b)2c)4(d3e))5f)') == list('12435')

#===========================================
#===========================================
def code_to_number_of_internal_nodes(code):
	# Extract the numeric internal nodes and return their count
	return len(code_to_internal_node_list(code))
assert code_to_number_of_internal_nodes('((((a1b)2c)4(d3e))7((f5g)6h))') == 7

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


