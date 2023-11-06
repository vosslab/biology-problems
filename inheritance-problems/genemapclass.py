#!/usr/bin/env python3

import copy
import random

import bptools
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
		self.max_gene_distance = 40
		self.question_count_int = question_count
		self.set_gene_letters()  # This will set self.gene_letters_str
		self.set_gene_order()
		self.light_colors, self.dark_colors = bptools.light_and_dark_color_wheel(self.num_genes_int, extra_light=True)

		# set None and empty values
		self.distance_triplet_tuple = None
		self.interference_dict = None
		self.distances_dict = None
		self.progeny_count_int = -1
		self.all_genotype_tuple_pairs_list = None
		self.progeny_groups_count_dict = None
		self.parental_genotypes_tuple = None
		self.genotype_counts = None
		self.interference_mode = False

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
	def set_gene_distances(self, min_distance=2) -> None:
		if self.num_genes_int == 2:
			distance = random.randint(min_distance, self.max_gene_distance)
			self.distances_dict = { (1,2): distance, }
		elif self.num_genes_int == 3:
			self.distances_dict = {}
			self.distance_triplet_tuple = self.get_one_distance_triplet(max_gene_distance=self.max_gene_distance, interference_mode=self.interference_mode)
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
	def get_one_distance_triplet(cls, max_fraction_int: int=12, max_gene_distance: int=40, interference_mode: bool=False) -> list:
		if cls._distance_triplet_list_cache is not None:
			return random.choice(cls._distance_triplet_list_cache)
		if interference_mode is True:
			max_fraction_int = 99
			distance_triplet_list = gml.get_all_distance_triplets_INTERFERENCE(max_fraction_int, max_gene_distance)
		else:
			distance_triplet_list = gml.get_all_distance_triplets(max_fraction_int, max_gene_distance)
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

	#====================================
	#====================================
	def get_all_recombinants_for_gene_letter(self, gene_pair: tuple) -> list:
		recombinants = []
		gene_index1 = self.gene_letters_str.find(gene_pair[0])
		gene_index2 = self.gene_letters_str.find(gene_pair[1])

		# Add them to the list of recombinants
		recombinants = []
		for genotype in self.genotype_counts.keys():
			for ptype in self.parental_genotypes_tuple:
				if genotype[gene_index1] == ptype[gene_index1] and genotype[gene_index2] != ptype[gene_index2]:
					recombinants.append(genotype)
		return recombinants

	#====================================
	#====================================
	def is_valid_html(self, html_text) -> bool:
		return gml.is_valid_html(html_text)

	#====================================
	#====================================
	def get_progeny_ascii_table(self) -> str:
		# Initialize an empty string to hold the table
		table = '\n'

		# Sort all types from the typemap keys
		all_genotypes = sorted(self.genotype_counts.keys(), reverse=True)

		spacer_line = ''
		for gene in range(self.num_genes_int):
			spacer_line += " -----"
		spacer_line += " --------- -----------------------\n"

		table += spacer_line
		table += "|"
		for gene in self.gene_letters_str:
			table += f"  {gene.upper()}  |"
		table += "  count  | phenotype"
		table += "\n"

		# Loop through sorted genotypes to fill the table
		for i, genotype in enumerate(all_genotypes):
			if i % 4 == 0:
				table += spacer_line
			# Fetch the phenotype name based on the genotype
			phenotype_string = gml.get_phenotype_name_for_genotype(genotype)
			table += "|"
			# Add genotype to the table
			for gene in genotype:
				table += f"  {gene}  |"

			# Add genotype count and phenotype name
			table += f"{gml.right_justify_int(self.genotype_counts[genotype],7)}  |"
			table += f" {phenotype_string}\t"

			# Add newline to complete the row
			table += "\n"

		table += spacer_line
		for gene in range(self.num_genes_int-1):
			table += "      "
		table += f"  TOTAL{gml.right_justify_int(self.progeny_count_int,7)}\n\n"

		# Return the completed table
		return table

	#====================================
	#====================================
	def get_progeny_html_table(self) -> str:
		"""
		Create an HTML table representation of progeny data.
		"""
		# Sort all genotype keys
		all_genotypes = sorted(self.genotype_counts.keys(), reverse=True)

		# Define common HTML attributes for table cells
		th_extra = 'align="center" style="border: 1px solid black; background-color: #cccccc; padding: 10px;"'
		td_extra = 'align="center" style="border: 1px solid black; background-color: #ffffff; padding: 5px;"'
		span = '<span style="font-size: medium; color: #000000;">'

		# Initialize the HTML table
		# width: 460px; height: 280px
		table = '<table style="border-collapse: collapse; border: 2px solid black;">'

		# Add header row to the table
		table += f'<tr><th {th_extra}>{span}Phenotype</span></th>'
		table += f'<th colspan="{self.num_genes_int}" {th_extra}>{span}Genotypes</span></th>'
		table += f'<th {th_extra}>{span}Progeny<br/>Count</span></th></tr>'

		# Loop through each genotype and add a row to the table
		for genotype in all_genotypes:
			# Fetch the phenotype string based on the genotype
			phenotype_string = gml.get_phenotype_name_for_genotype(genotype)

			table += f'<tr><td {td_extra.replace("center", "left")}>&nbsp;{span}{phenotype_string}</span></td>'
			for i in range(self.num_genes_int):
				local_span = copy.copy(span)
				local_td_extra = copy.copy(td_extra)
				allele = genotype[i]
				if allele == '+':
					local_span = local_span.replace('000000', self.dark_colors[i])
					local_span = local_span.replace('medium', 'large')
					local_td_extra = local_td_extra.replace('ffffff', 'f8f8f8')
				else:
					local_span = local_span.replace('medium', 'large')
					local_td_extra = local_td_extra.replace('ffffff', self.light_colors[i])
				table += f'<td {local_td_extra}>{local_span}{allele}</span></td>'
			table += f'<td {td_extra.replace("center", "right")}>{span}{self.genotype_counts[genotype]:,d}</span></td></tr>'

		# Add total progeny size at the end of the table
		table += f'<tr><th colspan="{self.num_genes_int+1}" {th_extra.replace("center", "right")}>{span}TOTAL =</span></th>'
		table += f'<td {td_extra.replace("center", "right")}>{span}{self.progeny_count_int:,d}</span></td></tr>'
		table += '</table>'

		if self.is_valid_html(table) is False:
			print(table)
			raise ValueError
		return table

	#====================================
	#====================================
	def get_question_header(self) -> str:
		cardinal_text = bptools.number_to_cardinal(self.num_genes_int)
		header_text = f'<h4>{cardinal_text.capitalize()}-Point Test Cross Problem</h4>'

		header_text += '<p>A test cross is a way to explore the relationship between genes and their respective alleles. '
		header_text += 'It is a useful tool for genetic mapping and deciphering the inheritance of traits. '
		header_text += f'Specifically, a {cardinal_text}-point test cross examines {cardinal_text} ({self.num_genes_int}) genes '
		header_text += 'at the same time to learn about their assortment in gamete formation.</p>'

		if self.num_genes_int == 2:
			count_str = 'both'
		else:
			count_str = f'all {cardinal_text}'
		header_text += f'<p>A standard {cardinal_text}-point test cross involves crossing '

		header_text += f'a heterozygous organism for {count_str} genes '
		header_text += f'with an organism that is homozygous recessive for {count_str} genes</p> '

		header_text += '<p>For this problem, a test cross using a fruit fly (<i>Drosophila melanogaster</i>) '
		header_text += f'heterozygous for {cardinal_text} genes was conducted to understand their genetic interactions.</p>'

		if self.is_valid_html(header_text) is False:
			print(header_text)
			raise ValueError
		return header_text

	#====================================
	#====================================
	def get_phenotype_info(self) -> str:
		phenotype_info_text = ''
		phenotype_info_text += '<h6>Characteristics of Recessive Phenotypes</h6>'

		linking_words = ('linked with', 'associated with', 'related to',
			'connected with', 'analogous to', 'affiliated with', 'correlated with',)
		phenotype_info_text += '<p><ul>'
		for i, gene_letter in enumerate(self.gene_letters_str):
			# Fetch the phenotype string based on the genotype
			phenotype_name = gml.phenotype_dict[gene_letter]
			phenotype_description = gml.phenotype_description_dict[phenotype_name]
			gene_span = f'<span style="color: #{self.dark_colors[i]};">'
			phenotype_info_text += f"<li><strong>{gene_span}Gene {gene_letter.upper()}</span></strong> is "
			phenotype_info_text += f'{random.choice(linking_words)} '
			phenotype_info_text += f"the '{gene_span}<i>{phenotype_name}</i></span>' phenotype. "
			phenotype_info_text += f'A fruit fly that is homozygous recessive for {gene_span}Gene {gene_letter.upper()}</span> '
			phenotype_info_text += f'{phenotype_description}</li> '
		phenotype_info_text += '</ul></p>'
		if self.is_valid_html(phenotype_info_text) is False:
			print(phenotype_info_text)
			raise ValueError
		return phenotype_info_text

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
	a = GeneMappingClass(4, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()

	#for i in range(200):
	a = GeneMappingClass(3, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()
	print(a.get_question_header())
	print(a.get_progeny_ascii_table())
