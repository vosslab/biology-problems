#!/usr/bin/env python3

import copy
import time
import random

try:
	from treelib import tools
except:
	import tools

### ONLY ALLOWED TO IMPORT tools NOT OTHER TREELIB FILES

#==================================
def _flip_tree_code(code: str) -> str:
	"""
	Reverses the tree code and flips parentheses.
	Args:
		code (str): A string representing the tree code.
	Returns:
		str: The reversed and flipped tree code as a string.
	"""
	# Reverse the code string
	flip_code = code[::-1]
	# Safely flip parentheses using a placeholder
	flip_code = flip_code.replace('(', '@')
	flip_code = flip_code.replace(')', '(')
	flip_code = flip_code.replace('@', ')')
	return flip_code

#==================================
def _get_left_of_node(code: str, node_loc):
	left_count = node_loc
	if code[node_loc-1].isalpha():
		return code[node_loc-1]
	if code[node_loc-1] == ')':
		parendiff = 1
		for i in range(2, left_count):
			if code[node_loc-i] == ')':
				parendiff += 1
			elif code[node_loc-i] == '(':
				parendiff -= 1
			if parendiff == 0:
				return code[node_loc-i:node_loc]
	return code[node_loc-1:node_loc]

#==================================
def _get_right_of_node(code: str, node_loc):
	right_count = len(code) - node_loc
	if code[node_loc+1].isalpha():
		return code[node_loc+1]
	if code[node_loc+1] == '(':
		parendiff = 1
		for i in range(2, right_count):
			if code[node_loc+i] == '(':
				parendiff += 1
			elif code[node_loc+i] == ')':
				parendiff -= 1
			if parendiff == 0:
				return code[node_loc+1:node_loc+1+i]
	return code[node_loc+1:node_loc+2]

#==================================
def _flip_node_in_code(code: str, node_number: int) -> str:
	"""
	Flips a specific node in a tree structure represented by the code.

	Args:
		code (str): The tree code.
		node_number (int): The internal node number to flip.

	Returns:
		str: The updated tree code with the specified node flipped.

	Raises:
		ValueError: If the resulting tree code has mismatched parentheses.
	"""
	node_loc = code.find(str(node_number))

	if node_loc == -1:
		raise ValueError(f"Node number {node_number} not found in the code.")

	left_text = _get_left_of_node(code, node_loc)
	right_text = _get_right_of_node(code, node_loc)

	start = node_loc-len(left_text)
	end = node_loc+len(right_text)+1
	subcode = code[start:end]
	flip_subcode = _flip_tree_code(subcode)
	new_code = code[:start] + flip_subcode + code[end:]

	debug_message = (
		f"Flipping node={node_number}\n"
		f"Node: {node_number}\n"
		f"node location={node_loc}\n"
		f"Left subtree: {left_text}\n"
		f"Right subtree: {right_text}\n"
		f"subcode: {subcode} <-subcode\n"
		f"Flipped subcode: {flip_subcode} <-flip_subcode\n"
		f"Original code: {code} <-code\n"
		f"New code: {new_code} <-new_code\n"
	)

	if len(new_code) != len(code):
		print(debug_message)
		raise ValueError("ERROR: Length of code changed.")

	if new_code.count('(') !=new_code.count(')'):
		print(debug_message)
		raise ValueError("ERROR: Unmatched parentheses.")

	if not new_code.startswith('(') or not new_code.endswith(')'):
		print(debug_message)
		raise ValueError("ERROR: Missing end parentheses.")

	return new_code

#==================================
def _permute_code_by_node(code: str, node_number=None) -> str:
	#rotates tree about a single node, but preserves connections
	max_nodes = tools.code_to_number_of_internal_nodes(code)
	if node_number is None:
		node_number = random.randint(1, max_nodes)
	elif node_number == 0:
		return copy.copy(code)
	elif node_number > max_nodes:
		raise ValueError(f"error: node_number {node_number} > max_nodes {max_nodes}")
	new_code = _flip_node_in_code(code, node_number)
	return new_code

#==================================
def _permute_code_by_node_binary(code, node_binary_list: list) -> str:
	max_nodes = tools.code_to_number_of_internal_nodes(code)
	new_code = copy.copy(code)
	reverse_binary_list = node_binary_list[::-1]
	for node_number_index in range(max_nodes):
		node_number = node_number_index + 1
		# power of two, essentually a binary number
		#if (node_binary // 2**node_number_less_one) % 2 == 1:
		if node_number_index >= len(reverse_binary_list):
			continue
		if reverse_binary_list[node_number_index] == 1:
			new_code = _permute_code_by_node(new_code, node_number)
	return new_code

#==================================
def _convert_int_to_binary_list(integer: int) -> list:
	binary_list = [int(x) for x in list('{0:0b}'.format(integer))]
	#print(integer, '->', binary_list)
	return binary_list


#====================================================================
#====================================================================
#====================================================================
#====================================================================
#====================================================================
#====================================================================
#====================================================================
#====================================================================

#=====================================================
# Permute Functions that return List of tree_code_str
#=====================================================

#===========================================
def get_all_permuted_tree_codes_from_tree_code_list(base_tree_code_str_list: list) -> list:
	t0 = time.time()
	sorted_taxa = sorted(tools.code_to_taxa_list(base_tree_code_str_list[0]))
	num_leaves = len(sorted_taxa)
	#print(f"__ len(base_tree_code_str_list)= {len(base_tree_code_str_list)}")
	all_taxa_permutations = tools.get_comb_safe_taxa_permutations(sorted_taxa)
	#print(f"__ len(all_taxa_permutations)= {len(all_taxa_permutations)}")
	#print(f"__ num_leaves = {num_leaves}")
	if num_leaves > 7:
		print("generating the 88,200 trees for 7 leaves takes 5 seconds, 8 leaves takes over 2 minutes to make 1.3M trees")
		#raise ValueError(f"too many leaves requested ({num_leaves}), try a different method for generating trees")
	### ASSEMBLE CODE LIST
	tree_code_str_list = []
	for i, base_tree_code_str in enumerate(base_tree_code_str_list):
		#print(f"__ tree code {i+1} of {len(base_tree_code_str_list)} -> {base_tree_code_str}")
		all_inner_node_permutated_tree_codes = get_all_inner_node_permutations_from_tree_code(base_tree_code_str)
		#print(f"__ processing inner node {len(all_inner_node_permutated_tree_codes)} tree codes and {len(all_taxa_permutations)} taxa orders")
		#loop_time = time.time()
		for permuted_code in all_inner_node_permutated_tree_codes:
			for permuted_taxa in all_taxa_permutations:
				final_code = tools.replace_taxa_letters(permuted_code, permuted_taxa)
				if tools.is_gene_tree_alpha_sorted(final_code) is True:
					tree_code_str_list.append(final_code)
		#print(f"__ current {len(tree_code_str_list)} permuted tree codes loop time {time.time()-loop_time:.6f} seconds.")

	#purge some other duplicates
	tree_code_str_list = list(set(tree_code_str_list))
	print("## created all trees ({0:,d} in total) for {1} leaves in {2:.3f} seconds.\n".format(
		len(tree_code_str_list), num_leaves, time.time() - t0))
	return tree_code_str_list

#==================================
def get_all_alpha_sorted_code_rotation_permutations(tree_code_str: str) -> list:
	if not isinstance(tree_code_str, str):
		raise ValueError('permute functions only take string tree_code_str as input')
	original_code_permutations = get_all_permutations_from_tree_code(tree_code_str)
	alpha_sorted_tree_code_permutations = []
	for permuted_tree_code_str in original_code_permutations:
		alpha_sorted_tree_code_str = tools.sort_alpha_for_gene_tree(permuted_tree_code_str)
		alpha_sorted_tree_code_permutations.append(alpha_sorted_tree_code_str)
	tree_code_permutations_list = list(set(alpha_sorted_tree_code_permutations))
	return tree_code_permutations_list

#==================================
def get_all_inner_node_permutations_from_tree_code(tree_code_str: str) -> list:
	if not isinstance(tree_code_str, str):
		raise ValueError('permute functions only take string tree_code_str as input')
	max_nodes = tools.code_to_number_of_internal_nodes(tree_code_str)
	alpha_sorted_tree_code_permutations = set()
	all_tree_code_permutations = []
	# even numbers only removes the (a1b) -> (b1a) permuation
	for node_binary in range(0, 2**max_nodes, 2):
		node_binary_list = _convert_int_to_binary_list(node_binary)
		permuted_tree_code_str = _permute_code_by_node_binary(tree_code_str, node_binary_list)
		if permuted_tree_code_str in all_tree_code_permutations:
			raise ValueError
		all_tree_code_permutations.append(permuted_tree_code_str)
		alpha_sorted_tree_code_str = tools.sort_alpha_for_gene_tree(permuted_tree_code_str)
		alpha_sorted_tree_code_permutations.add(alpha_sorted_tree_code_str)
	#print(f"len(all_tree_code_permutations) = {len(all_tree_code_permutations)}")
	#print(f"len(alpha_sorted_tree_code_permutations) = {len(alpha_sorted_tree_code_permutations)}")
	return alpha_sorted_tree_code_permutations

#==================================
def get_all_permutations_from_tree_code(tree_code_str: str) -> list:
	print(f".. .. running get_all_permutations_from_tree_code(tree_code={tree_code_str})")
	t0 = time.time()
	num_leaves = tools.code_to_number_of_taxa(tree_code_str)
	if num_leaves > 8:
		print("generating the 71,400 trees for 8 leaves takes ~8 seconds, 9 leaves takes too long")
		raise ValueError(f"too many leaves requested ({num_leaves}), try a different method for generating trees")
	sorted_taxa = sorted(tools.code_to_taxa_list(tree_code_str))
	all_taxa_permutations = tools.get_comb_safe_taxa_permutations(sorted_taxa)
	#print("^^ ^^ len(all_taxa_permutations)=", len(all_taxa_permutations))

	### ASSEMBLE CODE LIST
	tree_code_str_list = []
	all_inner_node_permutated_tree_codes = get_all_inner_node_permutations_from_tree_code(tree_code_str)
	#print("^^ ^^ len(all_inner_node_permutated_tree_codes)=", len(all_inner_node_permutated_tree_codes))
	#print(f"__ processing inner node {len(all_inner_node_permutated_tree_codes)} tree codes and {len(all_taxa_permutations)} taxa orders")
	for permuted_tree_code in all_inner_node_permutated_tree_codes:
		for permuted_taxa in all_taxa_permutations:
			final_code = tools.replace_gene_letters(permuted_tree_code, permuted_taxa)
			if tools.is_gene_tree_alpha_sorted(final_code) is True:
				tree_code_str_list.append(final_code)
	#purge some other duplicates
	tree_code_str_list = list(set(tree_code_str_list))
	print("** ** created {0:,d} tree code permutations for {1} leaves in {2:.3f} seconds".format(
		len(tree_code_str_list), num_leaves, time.time() - t0))
	return tree_code_str_list

#=====================================================
# Permute Functions that return tree_code_str String
#=====================================================

#==================================
def get_random_inner_node_permutation_from_tree_code(tree_code_str: str) -> str:
	if not isinstance(tree_code_str, str):
		raise ValueError('permute functions only take string tree_code_str as input')
	max_nodes = tools.code_to_number_of_internal_nodes(tree_code_str)
	# even numbers only removes the (a1b) -> (b1a) permuation
	node_binary = random.randint(0, 2**(max_nodes-1))*2
	node_binary_list = _convert_int_to_binary_list(node_binary)
	permuted_tree_code_str = _permute_code_by_node_binary(tree_code_str, node_binary_list)
	alpha_sorted_tree_code_str = tools.sort_alpha_for_gene_tree(permuted_tree_code_str)
	return alpha_sorted_tree_code_str

if __name__ == '__main__':
	import definitions

	def time_function(func, *args, **kwargs):
		"""
		Times the execution of a function and prints the result and elapsed time.

		Args:
			func (callable): The function to time.
			*args: Positional arguments to pass to the function.
			**kwargs: Keyword arguments to pass to the function.
		"""
		print(f"\n======function name:\n{func.__name__}()\n======")
		start_time = time.time()
		result = func(*args, **kwargs)
		elapsed_time = time.time() - start_time
		print(f"{func.__name__} took {elapsed_time:.6f} seconds.")
		return result

	# Select a random tree code for testing
	all_tree_code_str_list = list(definitions.code_library.values())
	len_6_tree_codes = []
	for tree_code_str in all_tree_code_str_list:
		taxa_list = sorted(tools.code_to_taxa_list(tree_code_str))
		if len(taxa_list) == 6:
			len_6_tree_codes.append(tree_code_str)
	tree_code_str = random.choice(len_6_tree_codes)
	taxa_list = sorted(tools.code_to_taxa_list(tree_code_str))
	while len(taxa_list) != 6:
		tree_code_str = random.choice(len_6_tree_codes)
		taxa_list = sorted(tools.code_to_taxa_list(tree_code_str))

	print(f"Testing with tree_code_str: {tree_code_str}")

	# Use a sorted list of taxa from the tree code
	print(f"Taxa list: {taxa_list}")

	# Time each function
	print("\nTiming functions:\n")

	# Time get_all_alpha_sorted_code_rotation_permutations
	alpha_sorted_permutations = time_function(
		get_all_alpha_sorted_code_rotation_permutations, tree_code_str
	)

	# Time get_all_inner_node_permutations_from_tree_code
	inner_node_permutations = time_function(
		get_all_inner_node_permutations_from_tree_code, tree_code_str
	)

	# Time get_all_permutations_from_tree_code
	all_permutations = time_function(
		get_all_permutations_from_tree_code, tree_code_str
	)

	# Time get_random_inner_node_permutation_from_tree_code
	random_inner_node_permutation = time_function(
		get_random_inner_node_permutation_from_tree_code, tree_code_str
	)

	base_tree_code_str_list = [tree_code_str,]
	base_tree_code_str_list = len_6_tree_codes
	# Time get_all_permuted_tree_codes_from_tree_code_list
	permuted_tree_codes1 = time_function(
		get_all_permuted_tree_codes_from_tree_code_list, base_tree_code_str_list
	)

	# Summary of results
	print("\nFunction outputs:")
	print(f"get_all_alpha_sorted_code_rotation_permutations: {len(alpha_sorted_permutations)} permutations generated.")
	print(f"get_all_inner_node_permutations_from_tree_code: {len(inner_node_permutations)} permutations generated.")
	print(f"get_all_permutations_from_tree_code: {len(all_permutations)} permutations generated.")
	print(f"get_random_inner_node_permutation_from_tree_code: {random_inner_node_permutation}")
	print(f"get_all_permuted_tree_codes_from_tree_code_list: {len(permuted_tree_codes1)} permutations generated.")
