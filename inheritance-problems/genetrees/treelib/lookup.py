import os
import time
import random
from collections import defaultdict

# Attempt to import tools and definitions from treelib, fallback to local versions for testing
try:
	from treelib import tools
	from treelib import permute
	from treelib import sorting
	from treelib import definitions
	from treelib import treecodeclass
except ImportError:
	import tools
	import permute
	import sorting
	import definitions
	import treecodeclass

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

def get_common_name_from_tree_code(tree_code) -> str:
	"""
	Returns the common name for a given tree code. If the tree code does not
	directly match, it attempts to reset and sort the taxa in the tree code
	before looking it up.
	"""
	if isinstance(tree_code, treecodeclass.TreeCode):
		tree_code_str = tree_code.tree_code_str
	elif isinstance(tree_code, str):
		tree_code_str = tree_code
	if tree_code in tree_code_to_name:
		return tree_code_to_name[tree_code_str]
	# Try resetting and sorting the taxa in the tree code
	reset_tree_code_str = tools.reset_sort_taxa_in_code(tree_code_str)
	if reset_tree_code_str in tree_code_to_name:
		return tree_code_to_name[reset_tree_code_str]
	if isinstance(tree_code, treecodeclass.TreeCode):
		# this might be None
		return tree_code.tree_common_name
	return None

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
	sized_tree_codes = num_leaves_to_tree_set[num_leaves]
	# Return a random choice
	tree_code_str = random.choice(sized_tree_codes)
	treecode_cls = treecodeclass.TreeCode(tree_code_str)
	return treecode_cls

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
	tree_code_str_list = num_leaves_to_tree_set[num_leaves]
	treecode_cls_list = []
	for tree_code_str in tree_code_str_list:
		treecode_cls = treecodeclass.TreeCode(tree_code_str)
		treecode_cls_list.append(treecode_cls)
	return treecode_cls_list

#===========================================
# Ported Permute Functions that return List of tree_code_str
#===========================================

#===========================================
def get_all_permuted_tree_codes_for_leaf_count(num_leaves: int) -> list:
	print(f".. running get_all_permuted_tree_codes_for_leaf_count(num_leaves={num_leaves})")
	if num_leaves > 7:
		print("generating the 88,200 trees for 7 leaves takes 5 seconds, 8 leaves takes over 2 minutes to make 1.3M trees")
		#raise ValueError("too many leaves requested, try a different method for generating trees")
	base_tree_code_cls_list = get_all_base_tree_codes_for_leaf_count(num_leaves)
	base_tree_code_str_list = []
	for base_tree_code_cls in base_tree_code_cls_list:
		base_tree_code_str_list.append(base_tree_code_cls.tree_code_str)
	tree_code_str_list = permute.get_all_permuted_tree_codes_from_tree_code_list(base_tree_code_str_list)
	start_time = time.time()
	treecode_cls_list = []
	for tree_code_str in tree_code_str_list:
		treecode_cls = treecodeclass.TreeCode(tree_code_str)
		treecode_cls_list.append(treecode_cls)
	print(f"get_all_permuted_tree_codes_for_leaf_count() took {time.time() - start_time:.6f} seconds.")
	return treecode_cls_list

#==================================
def get_all_alpha_sorted_code_rotation_permutations(tree_code) -> list:
	if isinstance(tree_code, treecodeclass.TreeCode):
		tree_code_str = tree_code.tree_code_str
	elif isinstance(tree_code, str):
		tree_code_str = tree_code
	tree_code_str_list = permute.get_all_alpha_sorted_code_rotation_permutations(tree_code_str)
	start_time = time.time()
	treecode_cls_list = []
	for tree_code_str in tree_code_str_list:
		treecode_cls = treecodeclass.TreeCode(tree_code_str)
		treecode_cls_list.append(treecode_cls)
	print(f"get_all_alpha_sorted_code_rotation_permutations() took {time.time() - start_time:.6f} seconds.")
	return treecode_cls_list

#==================================
def get_all_inner_node_permutations_from_tree_code(tree_code) -> list:
	if isinstance(tree_code, treecodeclass.TreeCode):
		tree_code_str = tree_code.tree_code_str
	elif isinstance(tree_code, str):
		tree_code_str = tree_code
	tree_code_str_list = permute.get_all_tree_code_inner_node_permutations(tree_code_str)
	start_time = time.time()
	treecode_cls_list = []
	for tree_code_str in tree_code_str_list:
		treecode_cls = treecodeclass.TreeCode(tree_code_str)
		treecode_cls_list.append(treecode_cls)
	print(f"get_all_inner_node_permutations_from_tree_code() took {time.time() - start_time:.6f} seconds.")
	return treecode_cls_list

#===========================================
def get_all_permutations_from_tree_code(tree_code) -> list:
	if isinstance(tree_code, treecodeclass.TreeCode):
		tree_code_str = tree_code.tree_code_str
	elif isinstance(tree_code, str):
		tree_code_str = tree_code
	tree_code_str_list = permute.get_all_permutations_from_tree_code(tree_code_str)
	start_time = time.time()
	treecode_cls_list = []
	for tree_code_str in tree_code_str_list:
		treecode_cls = treecodeclass.TreeCode(tree_code_str)
		treecode_cls_list.append(treecode_cls)
	print(f"get_all_permutations_from_tree_code() took {time.time() - start_time:.6f} seconds.")
	return treecode_cls_list

#===========================================
# Ported Permute Functions that return tree_code_str
#===========================================

#==================================
def get_random_inner_node_permutation_from_tree_code(tree_code):
	if isinstance(tree_code, treecodeclass.TreeCode):
		tree_code_str = tree_code.tree_code_str
	elif isinstance(tree_code, str):
		tree_code_str = tree_code
	permute_tree_code_str = permute.get_random_inner_node_permutation_from_tree_code(tree_code_str)
	permute_treecode_cls = treecodeclass.TreeCode(permute_tree_code_str)
	return permute_treecode_cls

#===========================================
# Ported Tools Functions that return tree_code_str
#===========================================

def replace_taxa_letters(tree_code, ordered_taxa: list):
	if isinstance(tree_code, treecodeclass.TreeCode):
		tree_code_str = tree_code.tree_code_str
	elif isinstance(tree_code, str):
		tree_code_str = tree_code
	ordered_tree_str = tools.replace_taxa_letters(tree_code_str, ordered_taxa)
	#print(f"replace_taxa_letters {tree_code_str} -> {ordered_tree_str}")
	ordered_treecode_cls = treecodeclass.TreeCode(ordered_tree_str, ordered_taxa)
	return ordered_treecode_cls

#===========================================
# Ported Sorting Functions that return List of tree_code_str
#===========================================

def sort_treecodes_by_taxa_distances(treecode_cls_list: list, answer_treecode_cls: str) -> list:
	"""
	Sorts a list of TreeCode objects by their similarity to an answer TreeCode.
	"""
	# Verify the type of the answer_treecode_cls
	if not isinstance(answer_treecode_cls, treecodeclass.TreeCode):
		raise TypeError("this function requires treecodeclass.TreeCode")
	# Get the distance map for the answer tree code
	answer_distance_map = answer_treecode_cls.distance_map
	# Initialize a list to store valid TreeCode objects with scores
	good_treecode_cls_list = []
	# Compute similarity scores for each tree in the input list
	for treecode_cls in treecode_cls_list:
		# Compare the distance maps of the current tree and the answer tree
		answer_score = sorting.compare_taxa_distance_maps(answer_distance_map, treecode_cls.distance_map)
		#print(f"answer_score = {answer_score:.3f} for a={answer_treecode_cls.tree_code_str}, t={treecode_cls.tree_code_str}")
		# Filter out exact matches (score = 1.0) and non-matches (score = 0.0)
		if answer_score < 0.999:
			# Assign the similarity score to the current TreeCode object
			treecode_cls.answer_score = answer_score
			# Add the TreeCode object to the list of valid comparisons
			good_treecode_cls_list.append(treecode_cls)
	# Sort the valid TreeCode objects by similarity score in descending order
	good_treecode_cls_list.sort(key=lambda x: x.answer_score, reverse=True)
	# Return the sorted list of TreeCode objects
	return good_treecode_cls_list

#==============================
# Test Block
#==============================
if __name__ == "__main__":
	# Test `get_common_name_from_tree_code`
	tree_code_str = random.choice(list(tree_code_to_name.keys()))
	common_name = get_common_name_from_tree_code(tree_code_str)
	print(f"Tree code: {tree_code_str}")
	print(f"Common name: {common_name}")

	# Test `get_tree_code_from_common_name`
	try:
		tree_code_from_name = get_tree_code_from_common_name(common_name)
		print(f"Tree code for common name '{common_name}': {tree_code_from_name}")
	except ValueError:
		pass

	print("\n.. Test `get_random_tree_code_for_leaf_count`")
	num_leaves = random.choice(list(num_leaves_to_tree_set.keys()))
	random_tree_code_cls = get_random_base_tree_code_for_leaf_count(num_leaves)
	tree_code = random_tree_code_cls.tree_code_str
	print(f"Random tree code for {num_leaves} leaves: {tree_code}")

	print("\n.. Test `get_all_permutations_from_tree_code`")
	treecode_cls_list = get_all_permutations_from_tree_code(random_tree_code_cls)
	print("\n.. Test `get_all_permutations_from_tree_code (again)`")
	treecode_cls_list = get_all_permutations_from_tree_code(random_tree_code_cls.tree_code_str)
	if len(treecode_cls_list) > 5:
		print(f"Permuted tree codes for {tree_code}: {len(treecode_cls_list)} different tree_codes")
	else:
		print(f"Permuted tree codes for {tree_code}: {[code.tree_code_str for code in treecode_cls_list]}")

	print("\n.. Test `get_all_base_tree_codes_for_leaf_count`")
	treecode_cls_list = get_all_base_tree_codes_for_leaf_count(num_leaves)
	if len(treecode_cls_list) > 5:
		print(f"All tree codes for {num_leaves} leaves: {len(treecode_cls_list)} different tree_codes")
	else:
		print(f"All tree codes for {num_leaves} leaves: {[code.tree_code_str for code in treecode_cls_list]}")

	if num_leaves >= 7:
		num_leaves = 6
	start_time = time.time()
	all_codes = get_all_permuted_tree_codes_for_leaf_count(num_leaves)
	if len(all_codes) > 10:
		print(f"All permuted tree codes for {num_leaves} leaves: {len(all_codes)} different tree_codes")
	else:
		print(f"All permuted tree codes for {num_leaves} leaves: {all_codes}")
	print(f"## get_all_permutations_from_tree_code() took {time.time() - start_time:.6f} seconds.")


