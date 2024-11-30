#!/usr/bin/env python3

import re
import copy
import itertools
import xml.etree.ElementTree as ET

### NOT ALLOWED TO IMPORT OTHER TREELIB FILES

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

#==================================
def reset_sort_taxa_in_code(original_tree_code: str) -> str:
	"""
	Resets and sorts the taxa in a tree code alphabetically.
	"""
	# Step 1: Extract the list of taxa in the original tree code
	original_taxa_list = code_to_taxa_list(original_tree_code)
	# Step 2: Create a sorted version of the taxa
	sorted_taxa_list = "abcdefghijklmnop"[:len(original_taxa_list)]
	# Step 3: Create intermediate placeholders for replacements
	placeholders = [f"@PL{i}$" for i in range(len(original_taxa_list))]
	# Step 4: Replace original taxa with placeholders to avoid collisions
	placeholder_tree_code = copy.copy(original_tree_code)
	for taxon, placeholder in zip(original_taxa_list, placeholders):
		placeholder_tree_code = placeholder_tree_code.replace(taxon, placeholder)

	# Step 5: Replace placeholders with sorted taxa
	sorted_tree_code = copy.copy(placeholder_tree_code)
	for placeholder, sorted_taxon in zip(placeholders, sorted_taxa_list):
		sorted_tree_code = sorted_tree_code.replace(placeholder, sorted_taxon)
	return sorted_tree_code
assert reset_sort_taxa_in_code('(((a2b)3c)4(d1e))') == '(((a2b)3c)4(d1e))'
assert reset_sort_taxa_in_code('(((e2c)3a)4(d1b))') == '(((a2b)3c)4(d1e))'
assert reset_sort_taxa_in_code('(((Y2Z)4(W3X))5(U1V))') == '(((a2b)4(c3d))5(e1f))'

#===========================================
#===========================================
def code_to_internal_node_list(tree_code: str):
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
def check_matching_parens(tree_code: str) -> bool:
	"""
	Checks that parentheses in the tree code are balanced and properly nested.
	"""
	open_parens = 0
	for char in tree_code:
		if char == '(':
			open_parens += 1
		elif char == ')':
			if not open_parens:
				raise ValueError(f"Unmatched closing parenthesis in tree_code {tree_code}")
			open_parens -= 1
	if open_parens:
		raise ValueError(f"Unmatched opening parenthesis in tree_code {tree_code}")
	return True
assert check_matching_parens("((()())())") == True

#===========================================
#===========================================
def validate_tree_code_by_reduction(tree_code: str) -> bool:
	"""
	Validates a tree code by iteratively reducing valid subtrees to a placeholder.

	Args:
		tree_code (str): The tree code to validate.

	Returns:
		bool: True if the tree code is valid, otherwise raises ValueError.

	Raises:
		ValueError: If the tree code is invalid or cannot be fully reduced.
	"""
	if not tree_code or not isinstance(tree_code, str):
		raise ValueError("Invalid input: tree_code must be a non-empty string.")
	# Create a mutable copy
	reduced_tree_code = copy.copy(tree_code)
	# Placeholder for valid subtrees
	placeholder = 'Z'
	# Extract and sort the internal node numerical characters
	node_list = sorted(code_to_internal_node_list(tree_code))
	# Iteratively replace valid subtrees with the placeholder
	for node_num_char in node_list:
		node_index = reduced_tree_code.find(node_num_char)
		sub_tree_str = reduced_tree_code[node_index-2:node_index+3]
		# Debug output for tracking the reduction process
		#print(f'sub_tree_str = {sub_tree_str}')
		# Match and replace valid subtrees
		if not re.fullmatch(r'\([a-zA-Z]\d[a-zA-Z]\)', sub_tree_str):
			raise ValueError(f"Invalid subtree structure: {sub_tree_str} of {reduced_tree_code}")
		reduced_tree_code = reduced_tree_code.replace(sub_tree_str, placeholder)
	# Final check: reduced tree code should collapse to a single placeholder
	if len(reduced_tree_code) > 1 and reduced_tree_code != placeholder:
		raise ValueError(f"Invalid tree_code did not reduce: {reduced_tree_code}")
	return True
assert validate_tree_code_by_reduction("(a1b)") == True  # Minimal structure
assert validate_tree_code_by_reduction("(((a2b)3c)4(d1e))") == True
assert validate_tree_code_by_reduction('(((((a1b)3c)5d)7(e6(f4(g2h))))8i)') == True

#===========================================
#===========================================
def validate_tree_code(tree_code: str, base: bool = False, replacement: bool = False) -> bool:
	"""
	Validates the structure and contents of a tree code.

	Args:
		tree_code (str): The tree code to validate.
		replacement (bool): Indicates if validation allows uppercase and non-consecutive taxa.

	Returns:
		bool: True if the tree code passes all validation checks.

	Raises:
		ValueError: If the tree code fails any validation check.
	"""
	# Step 0: Basic input validation
	if not tree_code:
		raise ValueError("Tree code is empty.")
	if not isinstance(tree_code, str):
		raise ValueError("Tree code is not a string.")
	# Minimum valid structure is "(a1b)"
	if len(tree_code) < 5:
		raise ValueError(f"Tree code is too short: {tree_code}")
	if base and replacement:
		raise ValueError(f"replacement {replacement} overrides base {base}, only one can be true")

	# Step 1: Check for valid characters
	if not replacement and not re.fullmatch(r'[a-z0-9()]+', tree_code):
		raise ValueError(f"Tree code contains invalid characters: {tree_code}")
	if replacement and not re.fullmatch(r'[a-zA-Z0-9()]+', tree_code):
		raise ValueError(f"Tree code contains invalid characters: {tree_code}")

	# Step 2: Check for balanced parentheses
	if tree_code.count('(') != tree_code.count(')'):
		raise ValueError(f"Unmatched parentheses in tree_code {tree_code}")
	check_matching_parens(tree_code)

	# Step 3: Extract taxa and internal node lists
	taxa_list = code_to_taxa_list(tree_code)
	node_list = code_to_internal_node_list(tree_code)

	# Step 4: Check the relationship between the number of taxa and internal nodes
	num_taxa = len(taxa_list)
	num_nodes = len(node_list)
	if num_taxa != num_nodes + 1:
		raise ValueError(f"Unmatched taxa {num_taxa} != nodes {num_nodes} + 1 in tree_code {tree_code}")

	# Step 5: Check for duplicate taxa
	if len(set(taxa_list)) != len(taxa_list):
		raise ValueError(f"Duplicate taxa found: {taxa_list} in tree_code {tree_code}")

	# Step 6: Validate taxa (lowercase or uppercase in replacement mode)
	if not replacement:
		# Ensure all taxa are lowercase and consecutive
		if not all(taxon.islower() and taxon.isalpha() for taxon in taxa_list):
			raise ValueError(f"Taxa not all lowercase alphabetic characters: {taxa_list} in tree_code {tree_code}")
		if sorted(taxa_list) != list('abcdefghijklmn')[:num_taxa]:
			raise ValueError(f"Taxa are not consecutive: {taxa_list} in tree_code {tree_code} in non-replacement mode")
		if base and taxa_list != list('abcdefghijklmn')[:num_taxa]:
			raise ValueError(f"Unsorted Taxa are not consecutive: {taxa_list} in base tree_code {tree_code} in base mode")
	else:
		# Ensure all taxa are alphabetic (uppercase or lowercase allowed in replacement mode)
		if not all(taxon.isalpha() for taxon in taxa_list):
			raise ValueError(f"Taxa not all alphabetic characters: {taxa_list} in tree_code {tree_code} in replacement mode")

	# Step 7: Check for duplicate internal nodes
	if len(set(node_list)) != len(node_list):
		raise ValueError(f"Duplicate numbers found: {node_list} in tree_code {tree_code}")

	# Step 8: Validate nodes (numeric and consecutive)
	if not all(node.isdigit() for node in node_list):
		raise ValueError(f"Nodes not all numeric: {node_list} in tree_code {tree_code}")
	if sorted(node_list) != list('123456789')[:num_nodes]:
		raise ValueError(f"Nodes are not consecutive: {node_list} in tree_code {tree_code}")

	#Validates a tree code by iteratively reducing valid subtrees to a placeholder.
	validate_tree_code_by_reduction(tree_code)

	# If all checks pass, the tree code is valid
	return True
# Valid tree codes
assert validate_tree_code("(a1b)") == True  # Minimal structure
assert validate_tree_code("(((a1b)2c)3d)") == True
assert validate_tree_code("(((a1b)3(c2d))5(e4f))") == True
# Valid tree codes in replacement mode
assert validate_tree_code("(((X1Y)2z)3F)", replacement=True) == True
# Check base modes
assert validate_tree_code("(((a1b)2c)3d)", base=True) == True
assert validate_tree_code("(((a1d)2b)3c)", base=False) == True


#===========================================
#===========================================
def is_valid_html(html_str: str, debug: bool=True) -> bool:
	"""
	Validates if the input HTML string is well-formed by removing entities
	and wrapping the content in a root element for XML parsing.

	Args:
		html_str (str): The HTML string to validate.

	Returns:
		bool: True if the HTML is well-formed, False otherwise.
	"""
	if '\n' in html_str:
		raise ValueError("Blackboard upload does not support newlines in the HTML code.")
	html_str = html_str.replace('<', '\n<')  # Optional: format the input HTML string for better readability on error
	try:
		# Remove HTML entities by finding '&' followed by alphanumerics or '#' and a semicolon
		cleaned_html = re.sub(r'&[#a-zA-Z0-9]+;', '', html_str)
		# Wrap in a root tag for XML parsing as XML requires a single root element
		wrapped_html = f"<root>{cleaned_html}</root>"
		# Parse the cleaned and wrapped HTML with XML parser
		ET.fromstring(wrapped_html)
		return True
	except ET.ParseError as e:
		# Print detailed error information for debugging
		if debug: print(f"Parse error: {e}")

		# Optional: Print a snippet of the HTML around the error
		error_index = e.position[1] if hasattr(e, 'position') else 0
		snippet = cleaned_html[max(0, error_index - 40): error_index + 40]
		if debug: print(f"Snippet around error (40 chars before and after):\n{snippet}")

		# Optional: Print the entire cleaned HTML if debugging further
		if debug: print("Full cleaned HTML (wrapped in root):")
		if debug: print(wrapped_html)

		return False

# Simple assertion test for the function: 'is_valid_html'
assert is_valid_html("<p>This is a paragraph.</p>") == True
assert is_valid_html("<p>This is a<br/>paragraph.</p>") == True
assert is_valid_html("<p>This is&nbsp;a paragraph.</p>") == True
assert is_valid_html("<p>This is a paragraph.</html>", debug=False) == False
assert is_valid_html("<span style='no closing quote>This is a paragraph.</span>", debug=False) == False

#===========================================
#===========================================
if __name__ == '__main__':
	import random
	import definitions
	all_codes = list(definitions.code_library.values())
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
	reset_code = reset_sort_taxa_in_code(replaced_code)
	print(f"reset_code = {reset_code}")
