import re
import math

try:
	from treelib import tools
	from treelib import lookup
	from treelib import output
	from treelib import sorting
except ImportError:
	import tools
	import lookup
	import output
	import sorting

### ALLOWED TO IMPORT ALL OTHER TREELIB FILES

lookup_cls = lookup.GeneTreeLookup()

class TreeCode:
	def __init__(self, tree_code_str: str):
		"""
		Initializes a TreeCode object.

		Args:
			tree_code_str (str): The tree_code string.
		"""
		self.tree_code_str = tools.sort_alpha_for_gene_tree(tree_code_str)
		self.tree_common_name = lookup_cls.get_tree_name_from_code(self.tree_code_str)
		self.distance_map = sorting.generate_taxa_distance_map(self.tree_code_str)
		self.num_leaves = tools.code_to_number_of_taxa(self.tree_code_str)
		comb_name = f"{self.num_leaves}comb"
		self.base_tree_code_str = definitions.code_library[comb_name]
		self.base_similarity_score = self._compute_similarity_to_base()
		self.output_cls = output.GeneTreeOutput()

	def _compute_similarity_to_base(self) -> float:
		"""
		Computes the similarity score to the canonical base tree for the number of leaves.

		Returns:
			float: The similarity score to the base comb tree.
		"""
		# If the tree is the same as the base tree, similarity is perfect
		if self.base_tree_code_str == self.tree_code_str:
			return 1.0

		# Compute the distance map for the base tree directly
		base_distance_map = sorting.generate_taxa_distance_map(self.base_tree_code_str)

		# Compare the current tree's distance map to the base tree's distance map
		return sorting.compare_taxa_distance_maps(self.distance_map, base_distance_map)

	def compare_to(self, other_tree) -> float:
		"""
		Compares this TreeCode to another TreeCode and returns a similarity score.

		Args:
			other (TreeCode): The other TreeCode to compare against.

		Returns:
			float: A similarity score between 0 and 1.
		"""
		# Trees with different numbers of leaves are not comparable
		if self.num_leaves != other_tree.num_leaves:
			return 0.0
		if self.tree_code_str == other_tree.tree_code_str:
			return 1.0
		score = sorting.compare_taxa_distance_maps(self.distance_map, other_tree.distance_map)
		return score

	def __lt__(self, other_tree) -> bool:
		"""
		Defines the less-than comparison for sorting TreeCode objects.

		Args:
			other_tree (TreeCode): The other TreeCode to compare.

		Returns:
			bool: True if this TreeCode is "less than" the other for sorting.
		"""
		# Sort by lowest tree size first
		# Trees with different numbers of leaves are not comparable
		if self.num_leaves != other_tree.num_leaves:
			return self.num_leaves < other_tree.num_leaves

		# Sort by similarity to the base comb tree
		if self.base_similarity_score != other_tree.base_similarity_score:
			# use greater than because closer to base comb tree comes first
			return self.base_similarity_score > other_tree.base_similarity_score
		# Sort by string representation for tie-breaking
		return self.tree_code_str < other_tree.tree_code_str

	def __eq__(self, other_tree) -> bool:
		"""
		Checks equality between two TreeCode objects based on their string representation.

		Args:
			other (TreeCode): The other TreeCode to compare.

		Returns:
			bool: True if the tree_codes are identical.
		"""
		# faster than comparing distance maps
		if self.num_leaves != other_tree.num_leaves:
			return False
		return self.distance_map == other_tree.distance_map

	def get_html_tree(self):
		return self.output_cls.get_html_from_tree_code(self.tree_code_str)

	def print_ascii_tree(self):
		return self.output_cls.print_ascii_tree(self.tree_code_str)

if __name__ == '__main__':
	import random

	# Step 1: Select a random tree_code from the library
	all_tree_codes = list(definitions.code_library.values())
	tree_code_str = random.choice(all_tree_codes)
	print(f"Randomly selected tree_code = {tree_code_str}")

	# Step 2: Create a TreeCode object
	tree_code_obj = TreeCode(tree_code_str)
	tree_code_obj.print_ascii_tree()
	print(f"TreeCode object created: {tree_code_obj.tree_code_str}")
	print(f"Number of leaves: {tree_code_obj.num_leaves}")
	print(f"Base similarity score: {tree_code_obj.base_similarity_score:.5f}")

	# Step 3: Compare the tree_code to its base comb tree
	base_tree_code_str = tree_code_obj.base_tree_code_str
	base_tree_code_obj = TreeCode(base_tree_code_str)
	similarity_score = tree_code_obj.compare_to(base_tree_code_obj)
	print(f"Similarity to base tree: {similarity_score:.5f}")

	# Step 4: Test sorting functionality with multiple TreeCode objects
	test_tree_codes = random.sample(all_tree_codes, 9)
	tree_objects = [TreeCode(tree_code) for tree_code in test_tree_codes]
	sorted_trees = sorted(tree_objects)
	print("Sorted tree_codes based on similarity to base trees:")
	for i, tree in enumerate(sorted_trees):
		print(f".. {i+1} Leaves: {tree.num_leaves} Base Score: {tree.base_similarity_score:.3f}, Code: {tree.tree_code_str}, ")

	# Step 5: Verify equality comparison
	if tree_objects[0] == tree_objects[0]:
		print(f"Tree {tree_objects[0].tree_code_str} is equal to itself.")
	if tree_objects[0] != tree_objects[1]:
		print(f"Tree {tree_objects[0].tree_code_str} is not equal to {tree_objects[1].tree_code_str}.")
	if tree_objects[2] > tree_objects[3]:
		print(f"Tree {tree_objects[0].tree_code_str} is greater than {tree_objects[1].tree_code_str}.")
	elif tree_objects[2] < tree_objects[3]:
		print(f"Tree {tree_objects[0].tree_code_str} is less than {tree_objects[1].tree_code_str}.")
