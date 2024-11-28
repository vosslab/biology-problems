#!/usr/bin/env python3

import sys
import copy
import time
import random

from treelib import tools
from treelib import treecodes

### TODO
# add background colors to gene labels
# add font colors to gene labels
# test new function sort_codes_by_closeness()

class GeneTreeManip(object):
	#==================================
	def __init__(self):
		self.code = None
		self.num_leaves = None

		self._load_code_library()
		self._check_tree_count_theory()
		self.make_all_cache = {}

	#==================================
	def _load_code_library(self):
		self.num_leaves_to_tree_set = {}
		self.max_leaves = 0
		self.code_to_name = {}
		count = 0
		for name, code in treecodes.code_library.items():
			count += 1
			self.code_to_name[code] = name
			num_leaves = tools.code_to_number_of_taxa(code)
			self.max_leaves = max(self.max_leaves, num_leaves)
			self.num_leaves_to_tree_set[num_leaves] = self.num_leaves_to_tree_set.get(num_leaves, []) + [code,]
		print("Processed {0} codes into {1} different sets with max leaves of {2}".format(
			count, len(self.num_leaves_to_tree_set), self.max_leaves))
		#print(list(self.num_leaves_to_tree_set.keys()))
		return

	#==================================
	def _check_tree_count_theory(self):
		return
		keys = list(self.num_leaves_to_tree_set.keys())
		keys.sort()
		for key in keys:
			print("leaves=", key, ": trees=", len(self.num_leaves_to_tree_set[key]))
		return

	#==================================
	def get_tree_name_from_code(self, code):
		return self.code_to_name[code]

	#==================================
	def get_random_gene_tree_code_for_leaf_count(self, num_leaves):
		if num_leaves > self.max_leaves:
			print("too many leaves requested {0} > max {1}".format(num_leaves, self.max_leaves))
			sys.exit(1)
		good_codes = self.num_leaves_to_tree_set[num_leaves]
		return random.choice(good_codes)

	#==================================
	def get_all_gene_tree_codes_for_leaf_count(self, num_leaves):
		return self.num_leaves_to_tree_set[num_leaves]

	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================

	#==================================
	def flip_tree_code(self, code: str) -> str:
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
	def get_left_of_node(self, code, node_loc):
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
	def get_right_of_node(self, code, node_loc):
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
	def _flip_node_in_code(self, code, node_number):
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

		left_text = self.get_left_of_node(code, node_loc)
		right_text = self.get_right_of_node(code, node_loc)

		start = node_loc-len(left_text)
		end = node_loc+len(right_text)+1
		subcode = code[start:end]
		flip_subcode = self.flip_tree_code(subcode)
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
	def permute_code_by_node(self, code, node_number=None):
		#rotates tree about a single node, but preserves connections
		max_nodes = tools.code_to_number_of_internal_nodes(code)
		if node_number is None:
			node_number = random.randint(1, max_nodes)
		elif node_number == 0:
			return copy.copy(code)
		elif node_number > max_nodes:
			print("error: node_number {0} > max_nodes {1}".format(node_number, max_nodes))
			sys.exit(1)

		new_code = self._flip_node_in_code(code, node_number)
		return new_code

	#==================================
	def get_all_code_permutations(self, code):
		max_nodes = tools.code_to_number_of_internal_nodes(code)
		code_permutations = []
		for node_binary in range(2**max_nodes):
			node_binary_list = self.convert_int_to_binary_list(node_binary)
			new_code = self._permute_code_by_node_binary(code, node_binary_list)
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
	def _permute_code_by_node_binary(self, code, node_binary_list):
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
				new_code = self.permute_code_by_node(new_code, node_number)
		return new_code

	#==================================
	def get_all_alpha_sorted_code_rotation_permutations(self, code):
		original_code_permutations = self.get_all_code_permutations(code)
		alpha_sorted_code_permutations = []
		for code in original_code_permutations:
			new_code = tools.sort_alpha_for_gene_tree(code)
			alpha_sorted_code_permutations.append(new_code)
		code_permutations = list(set(alpha_sorted_code_permutations))
		return code_permutations

	#===========================================
	def make_all_gene_trees_for_leaf_count(self, num_leaves, sorted_taxa):
		if num_leaves > 7:
			print("generating the 88,200 trees for 7 leaves takes 5 seconds, 8 leaves takes over 2 minutes to make 1.3M trees")
			print("too many leaves requested, try a different method for generating trees")
			sys.exit(1)

		t0 = time.time()
		all_taxa_permutations = tools.get_comb_safe_taxa_permutations(sorted_taxa)
		print("len(all_taxa_permutations)=", len(all_taxa_permutations))
	
		sorted_gene_tree_codes = self.get_all_gene_tree_codes_for_leaf_count(num_leaves)
		print("len(sorted_gene_tree_codes)=", len(sorted_gene_tree_codes))
		
		### ASSEMBLE CODE LIST
		code_choice_list = []
	
		for sorted_code in sorted_gene_tree_codes:
			all_permute_codes = self.get_all_code_permutations(sorted_code)
			for permuted_code in all_permute_codes:
				for permuted_nodes in all_taxa_permutations:
					final_code = self.replace_gene_letters(permuted_code, permuted_nodes)
					if tools.is_gene_tree_alpha_sorted(final_code) is True:
						code_choice_list.append(final_code)
		#purge some other duplicates
		code_choice_list = list(set(code_choice_list))
		print("Created all trees ({0} in total) for {1} leaves in {2:.3f} seconds".format(
			len(code_choice_list), num_leaves, time.time() - t0))
		print("")
		return code_choice_list

	#===========================================
	def sort_codes_by_closeness(self, code_list, answer_code):
		"""
		has not been thoroughly tested
		"""
		# Validate that `answer_code` is a code and not a profile
		if '(' not in answer_code:
			raise ValueError(f"Invalid `answer_code`: {answer_code}. Expected a gene tree code.")
		# Calculate similarity scores and sort the codes by score in descending order
		sorted_codes = sorted(
			code_list,
			key=lambda code: tools.string_match(code, answer_code),
			reverse=True
		)
		return sorted_codes

	#==================================
	def get_random_code_permutation(self, code):
		max_nodes = tools.code_to_number_of_internal_nodes(code)
		node_binary = random.randint(0, 2**max_nodes)
		node_binary_list = self.convert_int_to_binary_list(node_binary)
		new_code = self._permute_code_by_node_binary(code, node_binary_list)
		return new_code

	#==================================
	def get_random_even_code_permutation(self, code):
		max_nodes = tools.code_to_number_of_internal_nodes(code)
		node_binary = random.randint(0, 2**(max_nodes-1))*2
		node_binary_list = self.convert_int_to_binary_list(node_binary)
		new_code = self._permute_code_by_node_binary(code, node_binary_list)
		return new_code

	#==================================
	def convert_int_to_binary_list(self, integer):
		binary_list = [int(x) for x in list('{0:0b}'.format(integer))]
		#print(integer, '->', binary_list)
		return binary_list
