#!/usr/bin/env python3

import sys
import copy
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
def _get_left_of_node(code, node_loc):
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
def _get_right_of_node(code, node_loc):
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
def _flip_node_in_code(code, node_number):
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
def _permute_code_by_node(code, node_number=None):
	#rotates tree about a single node, but preserves connections
	max_nodes = tools.code_to_number_of_internal_nodes(code)
	if node_number is None:
		node_number = random.randint(1, max_nodes)
	elif node_number == 0:
		return copy.copy(code)
	elif node_number > max_nodes:
		print("error: node_number {0} > max_nodes {1}".format(node_number, max_nodes))
		sys.exit(1)

	new_code = _flip_node_in_code(code, node_number)
	return new_code

#==================================
def _permute_code_by_node_binary(code, node_binary_list):
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
def _convert_int_to_binary_list(integer):
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

#==================================
def get_all_alpha_sorted_code_rotation_permutations(code):
	original_code_permutations = get_all_code_permutations(code)
	alpha_sorted_code_permutations = []
	for code in original_code_permutations:
		new_code = tools.sort_alpha_for_gene_tree(code)
		alpha_sorted_code_permutations.append(new_code)
	code_permutations = list(set(alpha_sorted_code_permutations))
	return code_permutations



#==================================
def get_all_code_permutations(code):
	max_nodes = tools.code_to_number_of_internal_nodes(code)
	code_permutations = []
	for node_binary in range(2**max_nodes):
		node_binary_list = _convert_int_to_binary_list(node_binary)
		new_code = _permute_code_by_node_binary(code, node_binary_list)
		#print(node_binary, code, '->', new_code)
		if new_code in code_permutations:
			sys.exit(1)
		code_permutations.append(new_code)
	prelen = len(code_permutations)
	unique_code_permutations = list(set(code_permutations))
	postlen = len(unique_code_permutations)
	if prelen != postlen and max_nodes >= 4:
		dupes = [x for n, x in enumerate(code_permutations) if x in code_permutations[:n]]
		print(dupes)
		print("some code rotation permuation were duplicates")
		print("prelen=", prelen, "postlen=", postlen)
		sys.exit(1)
	return unique_code_permutations

#==================================
def get_random_code_permutation(code):
	max_nodes = tools.code_to_number_of_internal_nodes(code)
	node_binary = random.randint(0, 2**max_nodes)
	node_binary_list = _convert_int_to_binary_list(node_binary)
	new_code = _permute_code_by_node_binary(code, node_binary_list)
	return new_code

#==================================
def get_random_even_code_permutation(code):
	max_nodes = tools.code_to_number_of_internal_nodes(code)
	node_binary = random.randint(0, 2**(max_nodes-1))*2
	node_binary_list = _convert_int_to_binary_list(node_binary)
	new_code = _permute_code_by_node_binary(code, node_binary_list)
	return new_code
