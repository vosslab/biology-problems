#!/usr/bin/env python3

import sys
import random

try:
	from treelib import tools
	from treelib import treecodes
except ImportError:
	import tools
	import treecodes

class GeneTreeLookup(object):
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
