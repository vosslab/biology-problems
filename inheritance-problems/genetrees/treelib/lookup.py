import os
import random
from collections import defaultdict

# Attempt to import tools and definitions from treelib, fallback to local versions for testing
try:
	from treelib import tools
	from treelib import definitions
except ImportError:
	import tools
	import definitions

### ONLY ALLOWED TO IMPORT definitions and tools NOT OTHER TREELIB FILES

#==============================
# Initialization
#==============================
# A dictionary mapping the number of leaves to a list of tree codes
num_leaves_to_tree_set = defaultdict(list)
# A dictionary mapping tree codes to their common names
tree_code_to_name = {}
# Count the total number of tree codes processed
count = 0
# Populate num_leaves_to_tree_set and tree_code_to_name using the definitions from code_library
for name, tree_code in definitions.code_library.items():
	tools.validate_tree_code(tree_code, base=True)
	count += 1
	if tree_code in tree_code_to_name:
		old_name = tree_code_to_name[tree_code]
		print(f"tree_code={tree_code} already used: current name={name} used by {old_name}")
	tree_code_to_name[tree_code] = name  # Map tree code to its name
	num_leaves = tools.code_to_number_of_taxa(tree_code)  # Determine number of leaves in the tree
	num_leaves_to_tree_set[num_leaves].append(tree_code)  # Group tree codes by number of leaves
# Print a summary of the script's initialization
output = f"{os.path.basename(__file__).title()}: "
output += f"Processed {len(tree_code_to_name)} of {count} trees codes "
output += f"with max leaves of {max(list(num_leaves_to_tree_set.keys()))}"
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
