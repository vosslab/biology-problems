#!/usr/bin/env python3

import copy
import random
import genemaplib as gml


#===========================================================
#===========================================================
"""
# Two gene example
self.num_genes_int = 2
self.gene_letters_str = gk
self.gene_order_str = gk
self.distances_dict = {
  (1, 2): 19 # gene G and K
}
self.progeny_count_int = 2600
self.progeny_groups_count_dict = {
  (1, 2): 494 # gene G and K
  parental: 2106 # parental
}
self.all_genotype_tuple_pairs_list = [('++', 'gk'), ('+k', 'g+')]
self.parental_genotypes_tuple = ('+k', 'g+')
self.genotype_counts = {
  +k: 1047
  g+: 1059
  ++: 246
  gk: 248
}
#===========================================================
#===========================================================
# Three gene example
self.num_genes_int = 3
self.gene_letters_str = cgp
self.gene_order_str = gcp
self.distances_dict = {
  (1, 2): 16 # gene G and C
  (2, 3): 25 # gene C and P
  (1, 3): 36 # gene G and P
}
self.interference_dict = {
  (1, 2): None # adjacent genes G and C
  (2, 3): None # adjacent genes C and P
  (1, 3): (3, 8) # interference btw G and P
}
self.progeny_count_int = 4000
self.progeny_groups_count_dict = {
  (1, 3): 100 # gene G and P
  (1, 2): 640 # gene G and C
  (2, 3): 1000 # gene C and P
  parental: 2260 # parental
}
self.all_genotype_tuple_pairs_list = [('+gp', 'c++'), ('+g+', 'c+p'), ('+++', 'cgp'), ('++p', 'cg+')]
self.parental_genotypes_tuple = ('+gp', 'c++')
self.genotype_counts = {
  +gp: 1106
  c++: 1154
  cg+: 308
  ++p: 332
  cgp: 48
  +++: 52
  +g+: 500
  c+p: 500
}

self.num_genes_int = 3
#===========================================================
#===========================================================
# Four gene example
self.num_genes_int = 4
self.gene_letters_str = ajnu
self.gene_order_str = aujn
self.distances_dict = {
  (1, 2): 05 # gene A and U
  (2, 3): 10 # gene U and J
  (3, 4): 15 # gene J and N
  (1, 3): 15 # gene A and J
  (2, 4): 25 # gene U and N
  (1, 4): 30 # gene A and N
}
self.interference_dict = {
  (1, 2): None # adjacent genes A and U
  (2, 3): None # adjacent genes U and J
  (3, 4): None # adjacent genes J and N
  (1, 3): (1, 1) # interference btw A and J
  (2, 4): (1, 1) # interference btw U and N
  (1, 4): (1, 1) # interference btw A and N
}
self.progeny_count_int = 7200
self.progeny_groups_count_dict = {
  (1, 4): 00 # gene A and N
  (1, 3): 00 # gene A and J
  (2, 4): 00 # gene U and N
  (1, 2): 360 # gene A and U
  (2, 3): 720 # gene U and J
  (3, 4): 1080 # gene J and N
  parental: 5040 # parental
}
self.all_genotype_tuple_pairs_list = [('++n+', 'aj+u'), ('+j+u', 'a+n+'), ('+jnu', 'a+++'), ('++++', 'ajnu'), ('++nu', 'aj++'), ('+++u', 'ajn+'), ('+j++', 'a+nu'), ('+jn+', 'a++u')]
self.parental_genotypes_tuple = ('+j++', 'a+nu')
self.genotype_counts = {
  +j++: 2510
  a+nu: 2530
  ++nu: 186
  aj++: 174
  +j+u: 0
  a+n+: 0
  +jnu: 0
  a+++: 0
  ++n+: 355
  aj+u: 365
  ++++: 0
  ajnu: 0
  +jn+: 537
  a++u: 543
}
"""

#===========================================================
#===========================================================
class GeneMappingClass:
	#global cls variable
	_distance_triplet_list_cache = None

	#===========================================================
	#===========================================================
	def print_gene_map_data(self) -> None:
		print('================================')
		print(f'self.num_genes_int = {self.num_genes_int}')
		print(f'self.gene_letters_str = {self.gene_letters_str}')
		print(f'self.gene_order_str = {self.gene_order_str}')
		if self.distances_dict is not None:
			print('self.distances_dict = {')
			for key, value in self.distances_dict.items():
				print(f'  {key}: {value:02d} # gene '
					+f'{self.gene_order_str[key[0]-1].upper()} and '
					+f'{self.gene_order_str[key[1]-1].upper()} '
				)
			print('}')
		if self.interference_dict is not None:
			print('self.interference_dict = {')
			for key in self.distances_dict.keys():
				value = self.interference_dict.get(key)
				if value is None:
					print(f'  {key}: {value} # adjacent genes '
						+f'{self.gene_order_str[key[0]-1].upper()} and '
						+f'{self.gene_order_str[key[1]-1].upper()} '
					)
				else:
					print(f'  {key}: {value} # interference btw '
						+f'{self.gene_order_str[key[0]-1].upper()} and '
						+f'{self.gene_order_str[key[1]-1].upper()} '
					)
			print('}')
		if self.progeny_count_int > 0:
			print(f'self.progeny_count_int = {self.progeny_count_int}')
		if self.progeny_groups_count_dict is not None:
			print('self.progeny_groups_count_dict = {')
			for key, value in self.progeny_groups_count_dict.items():
				if isinstance(key, tuple):
					print(f'  {key}: {value:02d} # gene '
						+f'{self.gene_order_str[key[0]-1].upper()} and '
						+f'{self.gene_order_str[key[1]-1].upper()} '
					)
				else:
					print(f'  {key}: {value:02d} # parental')
			print('}')
		if self.all_genotype_tuple_pairs_list is not None:
			print(f'self.all_genotype_tuple_pairs_list = {self.all_genotype_tuple_pairs_list}')
		if self.parental_genotypes_tuple is not None:
			print(f'self.parental_genotypes_tuple = {self.parental_genotypes_tuple}')
		if self.genotype_counts is not None:
			print('self.genotype_counts = {')
			for genotype, count in self.genotype_counts.items():
				print(f'  {genotype}: {count:d}')
			print('}')
		print('================================')

	#===========================================================
	#===========================================================
	def __init__(self, num_genes_int: int, question_count: int=1, debug: bool=False) -> None:
		self.debug = debug
		if num_genes_int < 2:
			raise ValueError("Too few genes, num_genes_int must be at least 2")
		if num_genes_int > 4:
			raise ValueError("Too many genes, num_genes_int cannot be more than 4")
		self.num_genes_int = num_genes_int
		self.question_count_int = question_count
		self.set_gene_letters()  # This will set self.gene_letters_str
		self.set_gene_order()

		self.distance_triplet_tuple = None
		self.interference_dict = None
		self.distances_dict = None
		self.progeny_count_int = -1
		self.all_genotype_tuple_pairs_list = None
		self.progeny_groups_count_dict = None
		self.parental_genotypes_tuple = None
		self.genotype_counts = None
		if self.debug is True:
			self.print_gene_map_data()

	#===========================================================
	#===========================================================
	def set_gene_letters(self) -> None:
		self.gene_letters_str = gml.get_gene_letters(self.num_genes_int)

	#===========================================================
	#===========================================================
	def set_gene_order(self) -> None:
		gene_order_list = list(self.gene_letters_str)
		random.shuffle(gene_order_list)
		gene_order_list = min(gene_order_list, gene_order_list[::-1])
		self.gene_order_str = ''.join(gene_order_list)

	#===========================================================
	#===========================================================
	def setup_question(self):
		self.set_gene_distances()
		self.set_progeny_count()
		self.set_progeny_groups_counts()
		self.set_all_genotype_tuple_pairs_list()
		self.set_parental_genotypes()
		self.set_genotype_counts()

	#===========================================================
	#===========================================================
	def map_gene_order_to_alphabetical(self, gene_order_index) -> None:
		if gene_order_index < 1 or gene_order_index > self.num_genes_int:
			raise ValueError(f'gene order index must be 1 <= {gene_order_index} <= {self.num_genes_int}')
		gene_letter = self.gene_order_str[gene_order_index-1]
		gene_alphabet_index = self.gene_letters_str.find(gene_letter) + 1
		return gene_alphabet_index

	#===========================================================
	#===========================================================
	def map_gene_order_pair_to_alphabetical_pair(self, gene_order_index1, gene_order_index2) -> None:
		gene_alphabet_index1 = self.map_gene_order_to_alphabetical(gene_order_index1)
		gene_alphabet_index2 = self.map_gene_order_to_alphabetical(gene_order_index2)
		if gene_alphabet_index1 < gene_alphabet_index2:
			return gene_alphabet_index1, gene_alphabet_index2
		else:
			return gene_alphabet_index2, gene_alphabet_index1

	#===========================================================
	#===========================================================
	def set_gene_distances(self, min_distance=2, max_distance=48) -> None:
		if self.num_genes_int == 2:
			distance = random.randint(min_distance, max_distance)
			self.distances_dict = { (1,2): distance, }
		elif self.num_genes_int == 3:
			self.distances_dict = {}
			self.distance_triplet_tuple = self.get_one_distance_triplet()
			if random.random() < 0.5:
				self.distances_dict[(1,2)] = self.distance_triplet_tuple[0]
				self.distances_dict[(2,3)] = self.distance_triplet_tuple[1]
			else:
				self.distances_dict[(1,2)] = self.distance_triplet_tuple[1]
				self.distances_dict[(2,3)] = self.distance_triplet_tuple[0]
			self.distances_dict[(1,3)] = self.distance_triplet_tuple[2]
			interference_tuple = gml.calculate_interference_from_three_distances(*self.distance_triplet_tuple)
			self.interference_dict = {
				(1,3): interference_tuple,
				}
		elif self.num_genes_int == 4:
			self.distances_dict = {
				(1,2): 5,
				(2,3): 10,
				(3,4): 15,
				(1,3): 15,
				(2,4): 25,
				(1,4): 30,
			}
			self.interference_dict = {
				(1,3): (1,1),
				(2,4): (1,1),
				(1,4): (1,1),
			}
		if self.debug is True:
			self.print_gene_map_data()

	#====================================
	#====================================
	@classmethod
	def get_one_distance_triplet(cls, max_fraction_int: int=12, max_distance: int=40) -> list:
		if cls._distance_triplet_list_cache is not None:
			return random.choice(cls._distance_triplet_list_cache)
		distance_triplet_list = gml.get_all_distance_triplets(max_fraction_int, max_distance)
		cls._distance_triplet_list_cache = distance_triplet_list
		return random.choice(distance_triplet_list)

	#====================================
	#====================================
	def set_progeny_count(self):
		#self.progeny_base_int = minN(self.distance_triplet_tuple[0], self.distance_triplet_tuple[1])
		self.progeny_count_int = gml.get_general_progeny_size(tuple(self.distances_dict.values()))
		if self.debug is True:
			self.print_gene_map_data()

	#====================================
	#====================================
	def calculate_triple_crossovers(self, gene_pair):
		#gene_pair = (1,3)
		if gene_pair[1] - gene_pair[0] != 3:
			raise ValueError(f"gene pair is not a triple crossover, {gene_pair}")
		no_interference_TCO = self.progeny_count_int
		for x in range(gene_pair[0], gene_pair[1]):
			no_interference_TCO *= self.distances_dict[(x,x+1)] / 100
		if self.debug is True:
			print(f'no_interference_TCO={no_interference_TCO:.3f}')
		interference_tuple= self.interference_dict[gene_pair]
		Interference_TCO = no_interference_TCO * (interference_tuple[1] - interference_tuple[0]) / interference_tuple[1]
		if not gml.is_almost_integer(Interference_TCO):
			raise ValueError(f'Interference_TCO={Interference_TCO:.5f} is NOT an integer')
		Interference_TCO = int(round(Interference_TCO))
		if self.debug is True:
			print(f'Interference_TCO for {gene_pair}={Interference_TCO:d}')
		return Interference_TCO

	#====================================
	#====================================
	def calculate_double_crossovers(self, gene_pair):
		#gene_pair = (1,3)
		if gene_pair[1] - gene_pair[0] != 2:
			raise ValueError(f"gene pair is not a double crossover, {gene_pair}")
		no_interference_DCO = self.progeny_count_int
		for x in range(gene_pair[0], gene_pair[1]):
			no_interference_DCO *= self.distances_dict[(x,x+1)] / 100
		if self.debug is True:
			print(f'no_interference_DCO={no_interference_DCO:.3f}')
		interference_tuple = self.interference_dict[gene_pair]
		Interference_DCO = no_interference_DCO * (interference_tuple[1] - interference_tuple[0]) / interference_tuple[1]
		if not gml.is_almost_integer(Interference_DCO):
			raise ValueError(f'Interference_DCO={Interference_DCO:.5f} is NOT an integer')
		Interference_DCO = int(round(Interference_DCO))
		if self.debug is True:
			print(f'Interference_DCO for {gene_pair}={Interference_DCO:d}')
		return Interference_DCO

	#====================================
	#====================================
	def calculate_single_crossover(self, gene_pair):
		#gene_pair = (1,3)
		if gene_pair[1] - gene_pair[0] != 1:
			raise ValueError(f"gene pair is not a single crossover, {gene_pair}")
		sco_progeny = self.progeny_count_int * self.distances_dict[gene_pair] / 100
		if not gml.is_almost_integer(sco_progeny):
			raise ValueError(f'sco_progeny for {gene_pair}={sco_progeny:.5f} is NOT an integer')
		sco_progeny = int(round(sco_progeny))
		if self.debug is True:
			print(f'sco_progeny for {gene_pair}={sco_progeny:d}')
		return sco_progeny

	#====================================
	#====================================
	def set_progeny_groups_counts(self):
		"""
		A - x - B - y - C
		A - z - C
		determine interference_tuple

		determine DCO from A-B
		determine DCO from A-C
		get interference_tuple?

		make sure DCO is an integer

		determine SCO(x) for A-B genotype pairs, subtract DCO
		determine SCO(y) for B-C genotype pairs, subtract DCO

		leftover is for Parental genotype pairs
		"""

		gene_diff_pairs = {}
		for gene1 in range(1, self.num_genes_int):
			for gene2 in range(gene1+1, self.num_genes_int+1):
				diff = gene2 - gene1
				# Concatenate the current pair as a new list to the existing list of pairs
				gene_diff_pairs[diff] = gene_diff_pairs.get(diff, []) + [(gene1, gene2),]
		if self.debug is True:
			print(f'gene_diff_pairs={gene_diff_pairs}')
		self.progeny_groups_count_dict = {}
		# GET RAW COUNTS
		for gene_pair in gene_diff_pairs.get(3, []):
			#triple crossovers (TCO)
			self.progeny_groups_count_dict[gene_pair] = self.calculate_triple_crossovers(gene_pair)
		for gene_pair in gene_diff_pairs.get(2, []):
			#double crossovers (DCO)
			self.progeny_groups_count_dict[gene_pair] = self.calculate_double_crossovers(gene_pair)
		for gene_pair in gene_diff_pairs.get(1, []):
			#single crossovers (SCO)
			self.progeny_groups_count_dict[gene_pair] = self.calculate_single_crossover(gene_pair)

		# SUBTRACT DCO from SCO
		for gene_pair in gene_diff_pairs.get(1, []):
			#single crossovers (SCO)
			# if (1,2) subtract (1,3) and (2,4)
			# if (2,3) subtract (1,3) and (2,4)
			# if (3,4) subtract (2,4)
			for gene_index in gene_pair:
				if gene_index + 2 <= self.num_genes_int:
					new_gene_pair = (gene_index, gene_index+2)
					self.progeny_groups_count_dict[gene_pair] -= self.progeny_groups_count_dict[new_gene_pair]
				elif gene_index - 2 >= 1:
					new_gene_pair = (gene_index - 2, gene_index)
					self.progeny_groups_count_dict[gene_pair] -= self.progeny_groups_count_dict[new_gene_pair]
		if self.num_genes_int > 3:
			print('MORE THAN 3 genes WARNING NOT IMPLEMENTED YET')

		"""
		three gene:
		dco = Xc * Yc * N * (b -a)/b
		sx = N * Xc - dco
		sy = N * Yc - dco
		"""
		parent_count_int = self.progeny_count_int - sum(self.progeny_groups_count_dict.values())
		self.progeny_groups_count_dict['parental'] = parent_count_int
		total_count = sum(self.progeny_groups_count_dict.values())
		if total_count != self.progeny_count_int:
			raise ValueError(f'counts do not add up {total_count} vs expected {self.progeny_count_int}')

	#====================================
	def set_all_genotype_tuple_pairs_list(self):
		all_genotypes = gml.generate_genotypes(self.gene_letters_str)
		self.all_genotype_tuple_pairs_list = []
		genotype_tuple_pairs_set = set()
		for genotype in all_genotypes:
			inverted = gml.invert_genotype(genotype, self.gene_letters_str)
			pair = sorted([genotype, inverted])
			genotype_tuple_pairs_set.add(tuple(pair))
		if len(genotype_tuple_pairs_set) != len(all_genotypes)//2:
			print(genotype_tuple_pairs_set)
			print(all_genotypes)
			raise ValueError(f'len(genotype_tuple_pairs_set) {len(genotype_tuple_pairs_set)} != '
					+f'len(all_genotypes)//2 {len(all_genotypes)}//2')
		self.all_genotype_tuple_pairs_list = list(genotype_tuple_pairs_set)

	#====================================
	def set_parental_genotypes(self):
		self.parental_genotypes_tuple = random.choice(self.all_genotype_tuple_pairs_list)
		if self.debug is True:
			self.print_gene_map_data()

	#====================================
	def set_genotype_counts(self) -> dict:
		"""self.progeny_groups_count_dict = {
			'parental': parent_count_int,
			'dco': reduced_DCO,
			'sco': {
				'(1,2)': sy,
				'(2,3)': sx,
			},
		}"""
		self.genotype_counts = {}
		#okay this stage is easy
		p_genotype1, p_genotype2 = self.parental_genotypes_tuple
		p_count1, p_count2 = gml.split_number_in_two(self.progeny_groups_count_dict['parental'])
		self.genotype_counts[p_genotype1] = p_count1
		self.genotype_counts[p_genotype2] = p_count2

		for gene_index1 in range(1, self.num_genes_int):
			for gene_index2 in range(gene_index1+1, self.num_genes_int+1):
				gene_pair = (gene_index1, gene_index2)
				#print(gene_pair)
				progeny_count1, progeny_count2 = gml.split_number_in_two(self.progeny_groups_count_dict[gene_pair])
				geno_type_1, geno_type_2 = copy.copy((p_genotype1, p_genotype2))
				for crossover_index in range(gene_index1, gene_index2):
					geno_type_1 = gml.crossover_after_index(geno_type_1, crossover_index, self.gene_order_str)
					geno_type_2 = gml.crossover_after_index(geno_type_2, crossover_index, self.gene_order_str)
				self.genotype_counts[geno_type_1] = progeny_count1
				self.genotype_counts[geno_type_2] = progeny_count2
		total_count = sum(self.genotype_counts.values())
		if total_count != self.progeny_count_int:
			raise ValueError(f'counts do not add up {total_count} vs expected {self.progeny_count_int}')
		if self.debug is True:
			self.print_gene_map_data()

#===========================================================
#===========================================================
#===========================================================
#===========================================================
#===========================================================

if __name__ == '__main__':
	#print("HELLO")
	a = GeneMappingClass(2, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()

	#for i in range(200):
	a = GeneMappingClass(3, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()

	#for i in range(200):
	a = GeneMappingClass(4, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()

