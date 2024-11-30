import os
import time
import random
from collections import defaultdict

# Attempt to import tools and definitions from treelib, fallback to local versions for testing
try:
	from treelib import tools
	from treelib import permute
	from treelib import definitions
except ImportError:
	import tools
	import permute
	import definitions

### ONLY ALLOWED TO IMPORT definitions, permute, and tools NOT OTHER TREELIB FILES

#==============================
# Initialization
#==============================
# A dictionary mapping the number of leaves to a list of corresponding tree codes.
num_leaves_to_tree_set = defaultdict(list)
# A dictionary mapping tree codes to their common (human-readable) names.
tree_code_to_name = {}
# Counter to track the total number of tree codes processed.
count = 0
# Populate the `num_leaves_to_tree_set` and `tree_code_to_name` dictionaries
# using the tree definitions provided in `definitions.code_library`.
for name, tree_code in definitions.code_library.items():
	# Validate each tree code to ensure it adheres to the expected "base" format.
	tools.validate_tree_code(tree_code, base=True)
	# Increment the count of processed tree codes.
	count += 1
	# Check if the tree code is already mapped to a name.
	if tree_code in tree_code_to_name:
		# If duplicate found, print a warning with details.
		old_name = tree_code_to_name[tree_code]
		print(f"tree_code={tree_code} already used: current name={name} used by {old_name}")
	# Map the tree code to its common name.
	tree_code_to_name[tree_code] = name
	# Determine the number of leaves in the tree code.
	num_leaves = tools.code_to_number_of_taxa(tree_code)
	# Add the tree code to the list of tree codes for the corresponding leaf count.
	num_leaves_to_tree_set[num_leaves].append(tree_code)
# Validate that the number of tree codes matches the expected count for each leaf count.
for num_leaves in num_leaves_to_tree_set:
	# Get the total number of tree codes for the current leaf count.
	num_tree_codes = len(num_leaves_to_tree_set[num_leaves])
	# Determine the expected number of tree codes.
	if num_leaves <= 6:
		# For smaller trees, use the larger expected number of edge-labeled trees.
		num_expected = tools.expected_number_of_edge_labeled_trees_for_leaf_count(num_leaves)
	else:
		# For larger trees, use the smaller expected number of tree types.
		num_expected = tools.expected_number_of_tree_types_for_leaf_count(num_leaves)
	# If the actual and expected counts do not match, raise an error.
	if num_tree_codes != num_expected:
		raise ValueError(f"num_leaves={num_leaves}, num_codes={num_tree_codes}, expected_codes={num_expected}")
# Generate and print a summary of the script's initialization process.
output = f"{os.path.basename(__file__).title()}: "  # Add the script name.
output += f"Processed {len(tree_code_to_name)} of {count} trees codes "  # Include processed count.
output += f"with max leaves of {max(list(num_leaves_to_tree_set.keys()))}"  # Include the maximum leaf count.
print(output)

#==================================

def get_common_name_from_tree_code(tree_code: str) -> str:
	"""
	Returns the common name for a given tree code. If the tree code does not
	directly match, it attempts to reset and sort the taxa in the tree code
	before looking it up.
	"""
	if tree_code in tree_code_to_name:
		return tree_code_to_name[tree_code]
	# Try resetting and sorting the taxa in the tree code
	reset_tree_code = tools.reset_sort_taxa_in_code(tree_code)
	if reset_tree_code in tree_code_to_name:
		return tree_code_to_name[reset_tree_code]
	# Raise an error if no match is found
	raise ValueError(f"Cannot find a common name for this tree code: {tree_code}")

#==================================
def get_tree_code_from_common_name(common_name: str) -> str:
	"""
	Returns the tree code associated with a given common name.
	"""
	if common_name in definitions.code_library:
		return definitions.code_library[common_name]
	# Raise an error if no match is found
	raise ValueError(f"Cannot find a tree code for this common name: {common_name}")

#==================================
def get_random_base_tree_code_for_leaf_count(num_leaves: int) -> str:
	"""
	Returns a random tree code with the specified number of leaves.
	"""
	if num_leaves < 2:
		raise ValueError(f"You need at least two leaves for a tree not: {num_leaves}")
	max_leaves = max(list(num_leaves_to_tree_set.keys()))
	if num_leaves > max_leaves:
		raise ValueError(f"Too many leaves requested: {num_leaves} > max {max_leaves}")
	# Get all tree codes for the given number of leaves
	good_codes = num_leaves_to_tree_set[num_leaves]
	# Return a random choice
	return random.choice(good_codes)

#==================================
def get_all_base_tree_codes_for_leaf_count(num_leaves: int) -> list:
	"""
	Returns all tree codes with the specified number of leaves.
	"""
	if num_leaves < 2:
		raise ValueError(f"You need at least two leaves for a tree not: {num_leaves}")
	max_leaves = max(list(num_leaves_to_tree_set.keys()))
	if num_leaves > max_leaves:
		raise ValueError(f"Too many leaves requested: {num_leaves} > max {max_leaves}")
	return num_leaves_to_tree_set[num_leaves]

#===========================================
def get_all_permuted_tree_codes_for_leaf_count(num_leaves, sorted_taxa):
	print(f".. running get_all_permuted_tree_codes_for_leaf_count(num_leaves={num_leaves})")
	if num_leaves > 7:
		print("generating the 88,200 trees for 7 leaves takes 5 seconds, 8 leaves takes over 2 minutes to make 1.3M trees")
		raise ValueError("too many leaves requested, try a different method for generating trees")

	t0 = time.time()
	all_taxa_permutations = tools.get_comb_safe_taxa_permutations(sorted_taxa)
	print("len(all_taxa_permutations)=", len(all_taxa_permutations))

	base_tree_codes = get_all_base_tree_codes_for_leaf_count(num_leaves)
	print("len(base_tree_codes)=", len(base_tree_codes))

	### ASSEMBLE CODE LIST
	code_choice_list = []

	for base_code in base_tree_codes:
		all_permute_codes = permute.get_all_code_permutations(base_code)
		for permuted_code in all_permute_codes:
			for permuted_nodes in all_taxa_permutations:
				final_code = tools.replace_gene_letters(permuted_code, permuted_nodes)
				if tools.is_gene_tree_alpha_sorted(final_code) is True:
					code_choice_list.append(final_code)
	#purge some other duplicates
	code_choice_list = list(set(code_choice_list))
	print("Created all trees ({0} in total) for {1} leaves in {2:.3f} seconds".format(
		len(code_choice_list), num_leaves, time.time() - t0))
	return code_choice_list

#==============================
# Test Block
#==============================
if __name__ == "__main__":
	# Test `get_common_name_from_tree_code`
	tree_code = random.choice(list(tree_code_to_name.keys()))
	common_name = get_common_name_from_tree_code(tree_code)
	print(f"Tree code: {tree_code}")
	print(f"Common name: {common_name}")

	# Test `get_tree_code_from_common_name`
	try:
		tree_code_from_name = get_tree_code_from_common_name(common_name)
		print(f"Tree code for common name '{common_name}': {tree_code_from_name}")
	except ValueError as e:
		print(e)

	# Test `get_random_tree_code_for_leaf_count`
	num_leaves = random.choice(list(num_leaves_to_tree_set.keys()))
	random_tree_code = get_random_base_tree_code_for_leaf_count(num_leaves)
	print(f"Random tree code for {num_leaves} leaves: {random_tree_code}")

	# Test `get_all_base_tree_codes_for_leaf_count`
	all_codes = get_all_base_tree_codes_for_leaf_count(num_leaves)
	if len(all_codes) > 5:
		print(f"All tree codes for {num_leaves} leaves: {len(all_codes)} different tree_codes")
	else:
		print(f"All tree codes for {num_leaves} leaves: {all_codes}")

	if num_leaves >= 7:
		num_leaves = 6
	sorted_taxa = "abcdefg"[:num_leaves]
	all_codes = get_all_permuted_tree_codes_for_leaf_count(num_leaves, sorted_taxa)
	if len(all_codes) > 10:
		print(f"All permuted tree codes for {num_leaves} leaves: {len(all_codes)} different tree_codes")
	else:
		print(f"All permuted tree codes for {num_leaves} leaves: {all_codes}")
