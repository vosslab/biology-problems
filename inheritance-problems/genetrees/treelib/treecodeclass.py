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

class TreeCode:
	def __init__(self, tree_code_str: str, ordered_taxa_tuple: tuple = None):
		"""
		Initializes a TreeCode object.

		Args:
			tree_code_str (str): The tree_code string.
		"""
		self.tree_code_str = tools.sort_alpha_for_gene_tree(tree_code_str)
		self.num_leaves = tools.code_to_number_of_taxa(self.tree_code_str)
		if ordered_taxa_tuple is not None:
			self.taxa_replaced = True
			if isinstance(ordered_taxa_tuple, list):
				ordered_taxa_tuple = tuple(ordered_taxa_tuple)
			elif not isinstance(ordered_taxa_tuple, tuple):
				raise ValueError(f"ordered_taxa_tuple must be a tuple, not a {type(ordered_taxa_tuple)}")
			self.ordered_taxa_tuple = ordered_taxa_tuple
			self.ordered_taxa_str = ''.join(ordered_taxa_tuple)
		else:
			self.taxa_replaced = False
			self.ordered_taxa_str = 'abcdefghijklm'[:self.num_leaves]
		self.tree_common_name = lookup.get_common_name_from_tree_code(self.tree_code_str)
		self.distance_map = tools.generate_taxa_distance_map(self.tree_code_str)
		#self.frozen_map = frozenset(sorted(self.distance_map.items()))
		self.frozen_map = frozenset(sorted(self.distance_map.items()))
		comb_name = f"{self.num_leaves}comb"
		self.base_comb_tree_code_str = lookup.get_tree_code_from_common_name(comb_name)
		if self.base_comb_tree_code_str is None:
			raise ValueError(f"could not find {comb_name} in definitions")
		if self.taxa_replaced is True:
			self.base_comb_tree_code_str = tools.replace_taxa_letters(self.base_comb_tree_code_str, self.ordered_taxa_tuple)
		self.base_comb_similarity_score = self._compute_similarity_to_base_comb()
		self.output_cls = output.GeneTreeOutput()

	def _compute_similarity_to_base_comb(self) -> float:
		"""
		Computes the similarity score to the canonical base tree for the number of leaves.

		Returns:
			float: The similarity score to the base comb tree.
		"""
		# If the tree is the same as the base comb tree, similarity is perfect
		if self.base_comb_tree_code_str == self.tree_code_str:
			return 1.0

		# Compute the distance map for the base comb tree directly
		base_distance_map = tools.generate_taxa_distance_map(self.base_comb_tree_code_str)

		# Compare the current tree's distance map to the base comb tree's distance map
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
		if self.base_comb_similarity_score != other_tree.base_comb_similarity_score:
			# use greater than because closer to base comb tree comes first
			return self.base_comb_similarity_score > other_tree.base_comb_similarity_score
		# Sort by string representation for tie-breaking
		return self.tree_code_str < other_tree.tree_code_str

	def _key(self):
		"""
		Generates a tuple of attributes that uniquely identify this TreeCode object.
		This is used for both hashing and equality checks.
		"""
		return (
			self.num_leaves,
			self.taxa_replaced,
			self.ordered_taxa_str,
			int(round(self.base_comb_similarity_score * 1000)),
			self.frozen_map,
		)

	def __hash__(self) -> int:
		"""
		Computes a hash value for the TreeCode object based on its key attributes.
		"""
		return hash(self._key())

	def __eq__(self, other_tree) -> bool:
		"""
		Checks equality between two TreeCode objects based on their key attributes.
		"""
		if not isinstance(other_tree, TreeCode):
			return False
		return self._key() == other_tree._key()

	def __eq__old(self, other_tree) -> bool:
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
		# faster than comparing distance maps
		if not math.isclose(self.base_comb_similarity_score, other_tree.base_comb_similarity_score, abs_tol=1e-6):
			return False
		return self.frozen_map == other_tree.frozen_map

	def get_html_table(self):
		return self.output_cls.get_html_from_tree_code(self.tree_code_str)

	def print_ascii_tree(self):
		return self.output_cls.print_ascii_tree(self.tree_code_str)

if __name__ == '__main__':
	import random
	import definitions
	# Step 1: Select a random tree_code from the library
	all_tree_codes = list(definitions.code_library.values())
	tree_code_str = random.choice(all_tree_codes)
	print(f"Randomly selected tree_code = {tree_code_str}")

	# Step 2: Create a TreeCode object
	tree_code_obj = TreeCode(tree_code_str)
	tree_code_obj.print_ascii_tree()
	print(f"TreeCode object created: {tree_code_obj.tree_code_str}")
	print(f"Number of leaves: {tree_code_obj.num_leaves}")
	print(f"Base comb similarity score: {tree_code_obj.base_comb_similarity_score:.5f}")

	# Step 3: Compare the tree_code to its base comb tree
	base_comb_tree_code_str = tree_code_obj.base_comb_tree_code_str
	base_comb_tree_code_obj = TreeCode(base_comb_tree_code_str)
	base_comb_similarity_score = tree_code_obj.compare_to(base_comb_tree_code_obj)
	print(f"Similarity to base comb tree: {base_comb_similarity_score:.5f}")

	# Step 4: Test sorting functionality with multiple TreeCode objects
	test_tree_codes = random.sample(all_tree_codes, 9)
	tree_objects = [TreeCode(tree_code) for tree_code in test_tree_codes]
	sorted_trees = sorted(tree_objects)
	print("Sorted tree_codes based on similarity to base trees:")
	for i, tree in enumerate(sorted_trees):
		print(f".. {i+1} Leaves: {tree.num_leaves} Base Score: {tree.base_comb_similarity_score:.3f}, Code: {tree.tree_code_str}, ")

	# Step 5: Verify equality comparison
	if tree_objects[0] == tree_objects[0]:
		print(f"Tree {tree_objects[0].tree_code_str} is equal to itself.")
	if tree_objects[0] != tree_objects[1]:
		print(f"Tree {tree_objects[0].tree_code_str} is not equal to {tree_objects[1].tree_code_str}.")
	if tree_objects[2] > tree_objects[3]:
		print(f"Tree {tree_objects[0].tree_code_str} is greater than {tree_objects[1].tree_code_str}.")
	elif tree_objects[2] < tree_objects[3]:
		print(f"Tree {tree_objects[0].tree_code_str} is less than {tree_objects[1].tree_code_str}.")
