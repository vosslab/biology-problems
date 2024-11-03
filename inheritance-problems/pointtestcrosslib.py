
import sys
import copy
import math
import random
import itertools
from bs4 import BeautifulSoup

debug = False

"""
===========================================
WARNING: THIS FILE IS DEPRECATED
===========================================

Please use the following files instead:

- genemapclass.py
- genemaplib.py

This file will no longer be maintained and may be removed in future versions.
"""

import genemaplib as gml

# Prompt the user for confirmation of the deprecation warning
print("WARNING: This file is deprecated. ")
print("Please use 'genemapclass.py' and 'genemaplib.py' instead.")
response = input("Do you acknowledge this warning? (y/n): ")
# If the user does not acknowledge, exit the program
if not response.lower().startswith('y'):
	print("Exiting due to lack of acknowledgment of deprecation warning.")
	raise RuntimeError("Acknowledgment of deprecation warning required to continue.")

#====================================
#====================================
# Dictionary to describe hypothetical fruit fly phenotypes
phenotype_description_dict = gml.phenotype_description_dict
phenotype_dict = gml.phenotype_dict

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
	def __init__(self, num_genes_int: int, question_count: int) -> None:
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
		self.print_gene_map_data()

	#===========================================================
	#===========================================================
	def set_gene_letters(self) -> None:
		self.gene_letters_str = get_gene_letters(self.num_genes_int)

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
			self.distances_dict[(1,2)] = self.distance_triplet_tuple[0]
			self.distances_dict[(2,3)] = self.distance_triplet_tuple[1]
			self.distances_dict[(1,3)] = self.distance_triplet_tuple[2]
			interference_tuple = calculate_interference_from_three_distances(*self.distance_triplet_tuple)
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
		self.print_gene_map_data()

	#====================================
	#====================================
	@classmethod
	def get_one_distance_triplet(cls, max_fraction_int: int=12, max_distance: int=40) -> list:
		if cls._distance_triplet_list_cache is not None:
			return random.choice(cls._distance_triplet_list_cache)
		distance_triplet_list = get_all_distance_triplets(max_fraction_int, max_distance)
		cls._distance_triplet_list_cache = distance_triplet_list
		return random.choice(distance_triplet_list)

	#====================================
	#====================================
	def set_progeny_count(self):
		#self.progeny_base_int = minN(self.distance_triplet_tuple[0], self.distance_triplet_tuple[1])
		self.progeny_count_int = get_general_progeny_size(tuple(self.distances_dict.values()))
		self.print_gene_map_data()

	#====================================
	#====================================
	def calculate_triple_crossovers(self, gene_pair):
		#gene_pair = (1,3)
		if gene_pair[1] - gene_pair[0] != 3:
			raise ValueError(f"gene pair is not a triple crossover, {gene_pair}")
		x1, x4 = gene_pair
		x2 = x1 + 1
		x3 = x1 + 2
		no_interference_TCO = self.progeny_count_int
		for x in range(gene_pair[0], gene_pair[1]):
			no_interference_TCO *= self.distances_dict[(x,x+1)] / 100
		print(f'no_interference_TCO={no_interference_TCO:.3f}')
		interference_tuple= self.interference_dict[gene_pair]
		Interference_TCO = no_interference_TCO * (interference_tuple[1] - interference_tuple[0]) / interference_tuple[1]
		if not is_almost_integer(Interference_TCO):
			raise ValueError(f'Interference_TCO={Interference_TCO:.5f} is NOT an integer')
		Interference_TCO = int(round(Interference_TCO))
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
		print(f'no_interference_DCO={no_interference_DCO:.3f}')
		interference_tuple= self.interference_dict[gene_pair]
		Interference_DCO = no_interference_DCO * (interference_tuple[1] - interference_tuple[0]) / interference_tuple[1]
		if not is_almost_integer(Interference_DCO):
			raise ValueError(f'Interference_DCO={Interference_DCO:.5f} is NOT an integer')
		Interference_DCO = int(round(Interference_DCO))
		print(f'Interference_DCO for {gene_pair}={Interference_DCO:d}')
		return Interference_DCO

	#====================================
	#====================================
	def calculate_single_crossover(self, gene_pair):
		#gene_pair = (1,3)
		if gene_pair[1] - gene_pair[0] != 1:
			raise ValueError(f"gene pair is not a single crossover, {gene_pair}")
		sco_progeny = self.progeny_count_int * self.distances_dict[gene_pair] / 100
		if not is_almost_integer(sco_progeny):
			raise ValueError(f'sco_progeny for {gene_pair}={sco_progeny:.5f} is NOT an integer')
		sco_progeny = int(round(sco_progeny))
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
		print(f'gene_diff_pairs={gene_diff_pairs}')
		self.progeny_groups_count_dict = {}
		for gene_pair in gene_diff_pairs.get(3, []):
			#triple crossovers (TCO)
			self.progeny_groups_count_dict[gene_pair] = self.calculate_triple_crossovers(gene_pair)
		for gene_pair in gene_diff_pairs.get(2, []):
			#double crossovers (DCO)
			self.progeny_groups_count_dict[gene_pair] = self.calculate_double_crossovers(gene_pair)
		for gene_pair in gene_diff_pairs.get(1, []):
			#single crossovers (SCO)
			self.progeny_groups_count_dict[gene_pair] = self.calculate_single_crossover(gene_pair)
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
		all_genotypes = generate_genotypes(self.gene_letters_str)
		self.all_genotype_tuple_pairs_list = []
		genotype_tuple_pairs_set = set()
		for genotype in all_genotypes:
			inverted = invert_genotype(genotype, self.gene_letters_str)
			pair = sorted([genotype, inverted])
			print(pair)
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
		p_count1, p_count2 = split_number_in_two(self.progeny_groups_count_dict['parental'])
		self.genotype_counts[p_genotype1] = p_count1
		self.genotype_counts[p_genotype2] = p_count2

		for gene_index1 in range(1, self.num_genes_int):
			for gene_index2 in range(gene_index1+1, self.num_genes_int+1):
				gene_pair = (gene_index1, gene_index2)
				print(gene_pair)
				progeny_count1, progeny_count2 = split_number_in_two(self.progeny_groups_count_dict[gene_pair])
				geno_type_1, geno_type_2 = copy.copy((p_genotype1, p_genotype2))
				for crossover_index in range(gene_index1, gene_index2):
					geno_type_1 = crossover_after_index(geno_type_1, crossover_index, self.gene_order_str)
					geno_type_2 = crossover_after_index(geno_type_2, crossover_index, self.gene_order_str)
				self.genotype_counts[geno_type_1] = progeny_count1
				self.genotype_counts[geno_type_2] = progeny_count2
		total_count = sum(self.genotype_counts.values())
		if total_count != self.progeny_count_int:
			raise ValueError(f'counts do not add up {total_count} vs expected {self.progeny_count_int}')
		self.print_gene_map_data()

#===========================================================
#===========================================================
#===========================================================
#===========================================================
#===========================================================
#===========================================================
def get_gene_letters(num_genes_int: int) -> str:
	return gml.get_gene_letters(num_genes_int)

#===========================================================
#===========================================================
def generate_genotypes(gene_letters: str) -> list:
	return gml.generate_genotypes(gene_letters)

#===========================================================
#===========================================================
def split_number_in_two(number: int) -> tuple:
	return gml.split_number_in_two(number)

#===========================================================
#===========================================================
def is_almost_integer(num: float, epsilon: float = 1e-6) -> bool:
	"""
	Checks if a float number is close to an integer within a given epsilon.

	Parameters
	----------
	num : float
		The number to check.
	epsilon : float, optional
		The tolerance level for being close to an integer. Default is 1e-6.

	Returns
	-------
	bool
		True if the number is close to an integer, False otherwise.
	"""
	# Calculate the absolute difference between the number and its nearest integer
	# Check if the difference is within the given epsilon and return the result
	difference = abs(num - round(num))
	return difference < epsilon
# Simple assertion tests for the function: 'is_almost_integer'
assert is_almost_integer(5.0000001)  == True
assert is_almost_integer(5.001)      == False

#===========================================================
#===========================================================
def get_phenotype_name(genotype: str) -> str:
	"""
	Gets the phenotype from a genotype.

	Parameters
	----------
	genotype : str
		The genotype to find the phenotype for.

	Returns
	-------
	str
		The phenotype in string format.
	"""
	# Check if all characters in genotype are '+'
	if all(char == '+' for char in genotype):
		return '<i>wildtype</i>'

	# Initialize an empty list to collect phenotype components
	phenotype_list = []

	# Iterate through the genotype to extract phenotypes
	for allele in genotype:
		if allele == '+':
			continue
		phenotype = phenotype_dict.get(allele)
		phenotype_list.append(phenotype)

	# Convert the list to a comma-separated string
	phenotype_string = ', '.join(phenotype_list)

	# Return the phenotype string
	return phenotype_string.strip()

# Simple assertion tests for the function: 'get_phenotype_name'
assert get_phenotype_name('++++') == '<i>wildtype</i>'
assert get_phenotype_name('+++') == '<i>wildtype</i>'
assert get_phenotype_name('++') == '<i>wildtype</i>'

#===========================================================
#===========================================================
import xml.etree.ElementTree as ET

def is_valid_html(html_str: str) -> bool:
	"""
	Validates if the input HTML string is well-formed.

	Args:
	html_str (str): The HTML string to validate.

	Returns:
	bool: True if the HTML is well-formed, False otherwise.
	"""
	try:
		# Wrapping the HTML string with a root tag, because `ET.fromstring`
		# requires a single root element, and typical HTML snippets might not have one.
		wrapped_html = f"<root>{html_str}</root>"
		ET.fromstring(wrapped_html)
		return True
	except ET.ParseError:
		return False

# Simple assertion test for the function: 'is_valid_html'
assert is_valid_html("<p>This is a paragraph.</p>") == True
assert is_valid_html("<p>This is a paragraph.</html>") == False
assert is_valid_html("<span style='no closing quote>This is a paragraph.</span>") == False

#===========================================================
#===========================================================
def min_difference(numbers: list) -> int:
	"""
	Find the minimum difference between any two consecutive integers in a sorted list.

	Parameters
	----------
	numbers : list
		A list of integers.

	Returns
	-------
	int
		The smallest difference found between any two consecutive integers.
	"""
	if isinstance(numbers, tuple):
		numbers = list(numbers)
	# Sort the list in place
	numbers.sort()
	# Calculate differences using list comprehension
	differences = [numbers[i+1] - numbers[i] for i in range(len(numbers) - 1)]
	# Return the smallest difference
	return min(differences)
assert min_difference([40, 41]) == 1
assert min_difference([30, 15, 36]) == 6
assert min_difference([84, 25, 24, 37]) == 1
assert min_difference([84, 30, 30, 42, 56, 72]) == 0

def minN(x: int, y: int, a: int, b: int) -> int:
	"""
	Calculate the smallest integer N that satisfies the given genetic linkage conditions.

	The function computes the minimum integer N such that for genetic linkage ratios x and y
	(expressed in centiMorgans, cM), the number of single crossover offspring (dsx and dsy)
	and double crossover offspring (dco) are maximized and still maintain whole numbers of offspring.

	Parameters
	----------
	x : int
		Recombination frequency between the first pair of genes in centiMorgans (cM).
	y : int
		Recombination frequency between the second pair of genes in centiMorgans (cM).
	a : int
		A parameter used in the equation for double crossovers (must be less than b).
	b : int
		A parameter used in the equation for double crossovers.

	Returns
	-------
	int
		The smallest integer N that satisfies the linkage conditions for genetic cross.

	Examples
	--------
	>>> minN(2, 3, 1, 2)
	10000

	Notes
	-----
	The function ensures that the total number of offspring, N, when multiplied by the
	recombination frequencies (in centiMorgans), results in whole numbers of single and
	double crossover offspring. It involves finding the greatest common divisor (gcd) of
	the potential maximum values of dsx, dsy, and dco, which in turn ensures the maximization
	of observable recombinants and the accuracy of linkage estimation.

	"""
	# The base multiplier for N is set to 10000 times b. This value ensures whole number counts
	# for single and double crossovers when N is divided by the recombination frequencies (x and y)
	# and the double crossover correction factor ((b - a) / b).

	# These are the desired integers for which we want N to guarantee whole numbers:
	# dsx = 100 * b * x (single crossovers for gene pair x)
	# dsy = 100 * b * y (single crossovers for gene pair y)
	# dco = x * y * (b - a) (double crossovers adjusted for (b - a) and b)
	# Finding the gcd of these terms gives the smallest factor by which 10000 * b can be
	# divided to still ensure integer values for dsx, dsy, and dco, hence satisfying the
	# genetic linkage conditions.
	final_gcd = math.gcd(100 * b * x, 100 * b * y, x * y * (b - a), 10000 * b)
	N = 10000 * b // final_gcd
	return N
assert minN(2, 3, 1, 2) == 10000
assert minN(5, 22, 6, 11) == 200


#====================================
#====================================
def get_distance():
	#integers
	return random.randint(2,45)

#====================================
#====================================
def calculate_third_distance(x: int, y: int, interference_tuple: tuple=(0,1)) -> float:
	"""
	Calculates the recombination distance between two outer genes (A and C)
	given the recombination distances between inner gene pairs (A-B and B-C)
	and a specified level of interference.

	Parameters:
	- x: float, recombination distance between genes A and B. 0 < x < 0.5.
	- y: float, recombination distance between genes B and C. x < y < 0.5.
	- interference: float, the interference value, typically between 0 and 1.

	Returns:
	- float, recombination distance between genes A and C.

	Derivation and Assumptions:
	- The number of expected double crossovers is calculated as dco = x * y * (1 - interference).
	- Single crossovers for A-B and B-C are derived as sco(x) = x - dco and
	  sco(y) = y - dco, respectively.
	- The distance z between A and C is calculated as z = x + y - 2 * dco,
	  where dco contributes to both x and y but cancels out for z.

	interference:
	- Incorporates the level of interference in the calculation.
	- In genetics, "interference" is defined as the degree to which one
	  crossover event interferes with additional crossovers in the same region.
	  If interference = 1, it means complete interference (no double crossovers occur).
	  If interference = 0, it means no interference (double crossovers occur as expected).
	"""

	# Validate the input constraints: 1 < x < 50, 1 < y < 50, and 0 <= interference <= 1
	if x < 1 or x >= 50 or y < 1 or y >= 50:
		raise ValueError("Invalid input values. Make sure 1 < x < 50 and 1 < y < 50.")
	a = interference_tuple[0]
	b = interference_tuple[1]
	interference_float = a/float(b)
	if interference_float < 0 or interference_float > 1:
		raise ValueError("Invalid input values. Make sure 0 <= interference <= 1.")
	# Calculate the number of expected double crossovers with interference
	# 1 - a/b == (b-a)/b
	dco = x * y * (b - a) / 100. / b
	if not is_almost_integer(2*dco):
		#print(f'x={x}; y={y}; interference={a}/{b}')
		#print(f'double crossovers is NOT integer!!! {dco:.4f}')
		#raise ValueError(f'double crossovers is NOT integer!!! {dco:.4f}')
		#return -1
		pass
	# Calculate the distance z between genes A and C
	z = x + y - 2 * dco
	if is_almost_integer(z):
		z = int(round(z))
	return z
assert calculate_third_distance(25, 22, (7, 11)) == 43
assert calculate_third_distance(20, 28, (3, 8)) == 41


#====================================
#====================================
def calculate_fourth_distance(x: int, y: int, z: int) -> float:
	# Validate the input constraints: 1 < x < 50, 1 < y < 50, and 0 <= z <= 50
	if x < 1 or x >= 50 or y < 1 or y >= 50 or z < 1 or z >= 50:
		raise ValueError("Invalid input values. Make sure 1 < x < 50 and 1 < y < 50 and 1 < z < 50.")
	t = x + y + z - 2 * (x*y/100 + y*z/100) + 3 * (x*y*z/100/100)
	if is_almost_integer(t):
		t = int(round(t))
	return t
#assert calculate_fourth_distance(25, 22, (7, 11)) == 43
#assert calculate_fourth_distance(20, 28, (3, 8)) == 41

#====================================
#====================================
def calculate_interference_from_three_distances(x: int, y: int, z: int) -> tuple:
	"""
	Calculate the interference based on three distances.

	Parameters
	----------
	x : int
		The first distance value, must be between 1 and 50.
	y : int
		The second distance value, must be between 1 and 50.
	z : int
		The third distance value, must be greater than x and y but less than 50.

	Returns
	-------
	tuple
		A tuple containing the interference ratio (a, b) as integers.
	"""
	# Validate the input constraints for x and y
	if not 1 < x < 50 or not 1 < y < 50:
		raise ValueError(f"Invalid input values for x and y. Ensure 1 < x < 50 and 1 < y < 50; got x={x}, y={y}.")

	# Validate the input constraints for z
	if not x < z < 50 or not y < z < 50:
		raise ValueError(f"Invalid input values for z. Ensure z > x, z > y, and z < 50; got x={x}, y={y}, z={z}.")

	# Begin with the third distance equation:
	# z = x + y - 2 * x * y * (b-a)/b / 100
	# This equation calculates the third distance z, which is altered by interference
	# in double crossover events. The term (2 * x * y * (b-a)/b) / 100 quantifies the interference impact on z.

	# To isolate the interference term (b-a)/b, we rearrange the equation:
	# 2 * x * y * (b - a)/b / 100 = x + y - z
	# Multiply through by 100 to remove the division by 100:
	# 2 * x * y * (b - a)/b = 100 * (x + y - z)

	# Now, to express (b - a)/b directly, divide both sides by 2 * x * y:
	# (b - a)/b = 50 * (x + y - z) / (x * y)

	# We are seeking integer values for a and b that represent the interference as a ratio.
	# To find b (the denominator of the interference ratio), we set b equal to the product of x and y:
	b = x * y

	# To find a (the numerator of the interference ratio), we isolate a from the term (b - a):
	# Solving for a, given (b - a) is equivalent to 50 * (x + y - z):
	# -a = -b + 50 * (x + y - z) <=> a = b + 50 * (z - x - y)
	a = b + 50 * (z - x - y)

	# Note that a and b may not be in their simplest form.
	# To reduce them to the simplest form, we calculate the greatest common divisor (GCD) of a and b
	# then divide both a anb b by their GCD.
	gcd1 = math.gcd(a, b)
	a //= gcd1
	b //= gcd1

	# Return the simplified ratio representing interference.
	return (a, b)
# Assert statement for testing the function with an example
assert calculate_interference_from_three_distances(5, 22, 26) == (6, 11)
assert calculate_interference_from_three_distances(30, 15, 38) == (2, 9)

# ==============================
# ==============================
def distance_triplet_generator(interference_tuple: tuple=(0,1), max_dist: int=40) -> list:
	"""
	Generate a list of distance triplets (y, x, z) within a given maximum distance.

	The function calculates the third distance z based on the given interference tuple and checks if z
	is an almost integer and within the range. The distance triplet is then validated for minimum
	difference and added to the list if it meets criteria.

	Parameters
	----------
	interference_tuple : tuple, optional
		A tuple representing the interference ratio (default is (0,1) which means no interference).
	max_dist : int, optional
		The maximum distance for x and y (default is 47).

	Returns
	-------
	list
		A list of valid distance triplets sorted in ascending order.

	Notes
	-----
	- Assumes that `calculate_third_distance`, `is_almost_integer`, and `min_difference`
	functions are already defined.
	- Potential error: `is_almost_integer` needs to be defined. If it's meant to check if `z`
	is close to an integer, the standard library function `math.isclose` or a custom definition
	might be needed.

	Examples
	--------
	>>> distance_triplet_generator()
	[(1, 1, 1), (2, 1, 2), ...]
	"""

	# Initialize an empty list to store valid distance triplets
	distance_triplet_list = []

	# Iterate over possible values of x
	for x in range(1, max_dist):
		# Iterate over possible values of y starting from current x to avoid duplicates
		for y in range(x, max_dist):
			# Calculate the third distance z using the provided interference tuple
			(a, b) = interference_tuple
			N = minN(x, y, a, b)
			if N < 10000:
				z = calculate_third_distance(x, y, interference_tuple)
				# Check if z is an almost integer, within the valid range, and the min difference criteria is met
				if y < z < max_dist and is_almost_integer(z):
					distance_tuple =(y,x,int(z))
					if min_difference(distance_tuple) > 1:
						# Add the valid triplet to the list
						distance_triplet_list.append(distance_tuple)
	# Sort the list of distance triplets in ascending order before returning
	distance_triplet_list.sort()
	return distance_triplet_list
# Example assertion for simple function validation (assuming other functions are defined)
assert distance_triplet_generator((9,11), 36) == [(25, 11, 35)]

#====================================
#====================================
def get_all_distance_triplets(max_fraction_int: int=12, max_distance: int=40) -> list:
	used_values = {}
	distance_triplet_list = []
	for numerator_prime  in range(1, max_fraction_int):
		for denominator_prime in range(numerator_prime+1,max_fraction_int+1):
			gcd_prime = math.gcd(numerator_prime ,denominator_prime )
			numerator = numerator_prime // gcd_prime
			denominator= denominator_prime // gcd_prime
			if used_values.get((numerator,denominator)) is None:
				used_values[(numerator,denominator)] = True
				new_distance_triplet_list = distance_triplet_generator((numerator,denominator), max_distance)
				if new_distance_triplet_list is not None:
					distance_triplet_list += new_distance_triplet_list
	print(f'found {len(distance_triplet_list)} distance tuples '+
		f'with max distance {max_distance} '+
		f'from all interference fractions up to denominator {max_fraction_int}')
	return distance_triplet_list

#====================================
#====================================
def get_general_progeny_size(distances: tuple) -> int:
	"""
	Calculate a suitable progeny size based on genetic distances.

	Parameters
	----------
	distances : list
		A tuple of genetic distances between genes.

	Returns
	-------
	int
		A calculated progeny size that factors in the provided genetic distances.

	"""
	# lazy method 1: just use 200
	if len(distances) == 3:
		a, b = calculate_interference_from_three_distances(distances[0], distances[1], distances[2])
		progeny_base = minN(distances[0], distances[1], a, b)
	else:
		progeny_base = 200
	multiplier = random.randint(900//progeny_base+1, 9900//progeny_base-1)
	return multiplier * progeny_base
	# more unique progeny numbers, GCD method 2
	# goal is to get the smallest progeny_base for set of distances
	# smallest progeny_base possible is 20
	# Calculate the greatest common divisor of the distances
	gcdf1 = math.gcd(*distances)
	# Why GCD with 40?
	# prime factors of 200 = 2^3 x 5^2
	# 200 / 3 and 200 / 7 are not integers, so must be multiple of 2 and 5
	# for each d in distances, d must be in range 1 < d < 49 = the max
	# 2^3= 8:  8,16,24 is GOOD
	# 2^4=16: 16,32,48 is too big <- also 200/16 is not int.
	# 5^1= 5:  5,10,15 is GOOD
	# 5^2=25: 25,50,75 is too big
	# Calculate the GCD with 40 = 2^3 x 5^1 to find a common scale factor
	gcdfinal = math.gcd(40, gcdf1)
	# Determine the base progeny size by dividing 200 by the final GCD
	progeny_base = 200 // gcdfinal
	# Compute the minimum progeny multiplier by dividing 900 by progeny base and adding 1
	min_progeny_multiplier = 900 // progeny_base + 1
	# Compute the maximum progeny multiplier by dividing 9900 by progeny base and subtracting 1
	max_progeny_multiplier = 9900 // progeny_base - 1
	# Generate a random multiplier between the min and max progeny multiplier
	multiplier = random.randint(min_progeny_multiplier, max_progeny_multiplier)
	# Return the final calculated progeny size
	return multiplier * progeny_base
#assert get_general_progeny_size([2, 3, 7]) % 200 == 0
#assert get_general_progeny_size([10, 20, 30]) % 20 == 0

#====================================
#====================================
def get_progeny_size(distance: int) -> int:
	return get_general_progeny_size([distance,])
assert get_progeny_size(10) % 200 == 0

#====================================
#====================================
def make_progeny_html_table(typemap: dict, progeny_size: int) -> str:
	"""
		Create an HTML table representation of progeny data.

		Parameters
		----------
		typemap : dict
			A dictionary containing genotype to progeny count mappings.
		progeny_size : int
			The total size of the progeny.

		Returns
		-------
		str
			The HTML table as a string.
	"""
	# Sort all genotype keys
	alltypes = list(typemap.keys())
	alltypes.sort()

	# Define common HTML attributes for table cells
	td_extra = 'align="center" style="border: 1px solid black;"'
	span = '<span style="font-size: medium;">'

	# Initialize the HTML table
	table = '<table style="border-collapse: collapse; border: 2px solid black; width: 460px; height: 280px">'

	# Add header row to the table
	table += f'<tr><th {td_extra}>{span}Phenotype</span></th>'
	table += f'<th colspan="{len(alltypes)}" {td_extra}>{span}Genotypes</span></th>'
	table += f'<th {td_extra}>{span}Progeny<br/>Count</span></th></tr>'

	# Loop through each genotype and add a row to the table
	for genotype in alltypes:
		# Fetch the phenotype string based on the genotype
		phenotype_string = get_phenotype_name(genotype)

		table += f'<tr><td {td_extra.replace("center", "left")}>&nbsp;{span}{phenotype_string}</span></td>'
		for i in range(len(genotype)):
			table += f'<td {td_extra}>{span}{genotype[i]}</span></td>'
		table += f'<td {td_extra.replace("center", "right")}>{span}{typemap[genotype]:d}</span></td></tr>'

	# Add total progeny size at the end of the table
	table += f'<tr><th colspan="{len(alltypes)+1}" {td_extra.replace("center", "right")}">{span}TOTAL =</span></th>'
	table += f'<td {td_extra.replace("center", "right")}>{span}{progeny_size:d}</span></td></tr>'
	table += '</table>'

	return table

# Simple assertion test for the function: 'make_progeny_html_table'
# Example dictionary and progeny size for testing
example_typemap = {'++': 10, '+b': 15, 'a+': 5, 'ab': 5}
example_progeny_size = 35
result = make_progeny_html_table(example_typemap, example_progeny_size)
# Since the return type is an HTML string, we are not asserting its exact content
# Instead, we assert that it contains an expected substring
assert 'TOTAL =' in result
assert f'{example_progeny_size:d}' in result

#====================================
#====================================
def right_justify_int(num: int, length: int) -> str:
	my_str = f'{num:d}'
	while len(my_str) < length:
		my_str = ' ' + my_str
	return my_str
assert right_justify_int(7,5) == "    7"

#====================================
#====================================
def make_progeny_ascii_table(typemap: dict, progeny_size: int) -> str:
	"""
	Numpydoc Comment
	----------------
	Parameters:
		typemap : dict
			Dictionary mapping genotypes to their corresponding counts
		progeny_size : int
			The total number of progenies

	Returns:
		str
			The ASCII table representing the genotype and phenotype counts
	"""

	# Initialize an empty string to hold the table
	table = '\n'

	# Sort all types from the typemap keys
	all_genotypes = list(typemap.keys())
	all_genotypes.sort()
	genes = all_genotypes[-1]

	for gene in genes:
		table += " -----"
	table += " --------- ------------------"
	table += "\n"
	table += "|"
	for gene in genes:
		table += f"  {gene}  |"
	table += "  count  | phenotype"
	table += "\n"
	for gene in genes:
		table += " -----"
	table += " --------- ------------------"
	table += "\n"

	# Loop through sorted genotypes to fill the table
	for genotype in all_genotypes:
		# Fetch the phenotype name based on the genotype
		phenotype_string = get_phenotype_name(genotype)
		table += "|"
		# Add genotype to the table
		for gene in genotype:
			table += f"  {gene}  |"

		# Add genotype count and phenotype name
		table += f"{right_justify_int(typemap[genotype],7)}  |"
		table += f" {phenotype_string}\t"

		# Add newline to complete the row
		table += "\n"

	for i in range(len(genes)):
		table += " -----"
	# Add delimiter and total progeny size at the end
	table += " --------- ------------------"
	table += "\n"
	for i in range(len(genes)-1):
		table += "      "
	table += f"  TOTAL{right_justify_int(progeny_size,7)}\n\n"

	# Return the completed table
	return table

#====================================
#====================================
def get_gene_distance(parental_types: tuple, gene_pair: tuple, typemap: dict, basetype: str, progeny_size: int) -> float:
	# Identify which genes are NOT in the pair (i.e., unused genes)
	unused_genes = [g for g in basetype if g not in gene_pair]

	# Start with the parental types and flip one of the two genes in the pair
	recomb1 = flip_gene_by_letter(parental_types[0], gene_pair[0], basetype)
	recomb2 = flip_gene_by_letter(parental_types[1], gene_pair[0], basetype)

	# Add them to the list of recombinants
	recombinants = [recomb1, recomb2]

	# Create new recombinants by flipping each unused gene in the recombinants generated so far
	for unused_gene in unused_genes:
		new_recombinants = [flip_gene_by_letter(recombinant, unused_gene, basetype) for recombinant in recombinants]
		recombinants += new_recombinants

	sum_progeny = 0
	for recomb in recombinants:
		sum_progeny += typemap[recomb]
	distance = sum_progeny/float(progeny_size)*100.0
	return distance

#====================================
#====================================
def gene_map_solver(typemap: dict, basetype: str, progeny_size: int) -> str:
	"""
	Find recombinants based on typemap, basetype, and progeny_size.

	Parameters
	----------
	typemap : dict
		Dictionary containing genotype frequencies.
	basetype : str
		String containing the basic genotype.
	progeny_size : int
		Total number of progenies.

	Returns
	-------
	str
		Description of recombinants.
	"""
	#all_genotypes = list(typemap.keys())
	sorted_typemap = sorted(typemap.items(), key=lambda x: x[1], reverse=True)
	parental_types = (sorted_typemap[0][0], sorted_typemap[1][0])
	observed_double_crossovers = sorted_typemap[-1][1] + sorted_typemap[-2][1]
	#print(f'parental_types = {parental_types}')
	#print(f'double_crossovers = {double_crossovers}')

	# Generate all unique combinations of two genes
	gene_pairs = list(itertools.combinations(basetype, 2))

	distances_dict = {}
	distances_list = []
	for gene_pair in gene_pairs:
		distance = get_gene_distance(parental_types, gene_pair, typemap, basetype, progeny_size)
		distances_dict[gene_pair] = distance
		distances_list.append(distance)

	#gene_pair_keys = list(distances_dict.keys())
	#print(distances_tuples_list)

	distances_list.sort()
	predict_dist = calculate_third_distance(distances_list[1], distances_list[0])
	expected_double_crossovers = distances_list[0]*distances_list[1]*progeny_size/10000.
	print(f'distances=({distances_list[1]:.0f}, {distances_list[0]:.0f}) and {distances_list[2]:.3f} vs {predict_dist:.1f})')
	if abs(expected_double_crossovers - observed_double_crossovers) > 1e-6:
		interference = 1.0 - observed_double_crossovers/expected_double_crossovers
		print(f'Expected DCO: {expected_double_crossovers} vs Observed DCO: {observed_double_crossovers}; Interference {interference}')
		sys.exit(1)

	"""
	distances_tuples_list = sorted(distances_dict.items(), key=lambda x: x[1], reverse=False)
	for gene_pair, distance in distances_tuples_list:
		if abs(distance - round(distance)) > 1e-6:
			dist_text = f'{distance:.4f}'
		else:
			dist_text = f'{distance:.2f}'
		print(f'\t{gene_pair[0]} and {gene_pair[1]}: {dist_text}')
	"""


#====================================
#====================================
def generate_genotype_counts(parental_type: str, basetype: str, progeny_size: int, distances: tuple, geneorder: str) -> dict:
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
	pass

def generate_three_gene_type_map(types: list, type_counts: dict, basetype: str) -> dict:
	if debug is True: print("\n\ngenerate progeny data")
	typemap = {}
	for t in types:
		n = ptcl.invert_genotype(t, basetype)
		#rand = random.gauss(0.5, 0.01)
		try:
			count = type_counts[t]
		except KeyError:
			count = type_counts[n]
		tcount = 0
		ncount = 0
		for i in range(count):
			if random.random() > 0.5:
				tcount += 1
			else:
				ncount += 1
		#sys.stderr.write(".")
		#typemap[t] = int(rand * count)
		#typemap[n] = count - typemap[t]
		typemap[t] = tcount
		typemap[n] = ncount
	sys.stderr.write("\n")
	return typemap

def generate_three_gene_type_counts(parental: str, doublecross: str, basetype: str, progeny_size: int, geneorder: str) -> dict:
	type_counts = {}
	if debug is True: print("determine double type")
	doubletype = ptcl.flip_gene_by_letter(parental, geneorder[1], basetype)
	doublecount = int(round(doublecross*progeny_size/100.))
	if debug is True: print("  ", doubletype, ptcl.invert_genotype(doubletype, basetype), doublecount)
	type_counts[doubletype] = doublecount

	if debug is True: print("determine first flip")
	firsttype = ptcl.flip_gene_by_letter(parental, geneorder[0], basetype)
	firstcount = int(round(distances[0]*progeny_size/100.)) - doublecount
	if debug is True: print("  ", firsttype, ptcl.invert_genotype(firsttype, basetype), firstcount)
	type_counts[firsttype] = firstcount

	if debug is True: print("determine second flip")
	secondtype = ptcl.flip_gene_by_letter(parental, geneorder[2], basetype)
	secondcount = int(round(distances[1]*progeny_size/100.)) - doublecount
	if debug is True: print("  ", secondtype, ptcl.invert_genotype(secondtype, basetype), secondcount)
	type_counts[secondtype] = secondcount

	if debug is True: print("determine parental type count")
	parentcount = progeny_size - doublecount - firstcount - secondcount
	if debug is True: print("  ", parental, ptcl.invert_genotype(parental, basetype), parentcount)
	type_counts[parental] = parentcount

	return type_counts

#====================================
#====================================
def generate_two_gene_type_counts(parental_type: str, basetype: str, progeny_size: int, distance: int, geneorder: str) -> dict:
	type_counts = {}
	recombinant_type_1 = flip_gene_by_letter(parental_type, geneorder[0], basetype)
	if debug is True: print("recombinant type 1=", recombinant_type_1)
	recombinant_type_2 = invert_genotype(recombinant_type_1, basetype)
	if debug is True: print("recombinant type 2=", recombinant_type_2)

	if debug is True: print("determine recombinant type counts")
	total_recombinant_count = int(round(distance*progeny_size/100.))
	recombinant_count_1 = 0
	recombinant_count_2 = 0
	for i in range(total_recombinant_count):
		if random.random() < 0.5:
			recombinant_count_1 += 1
		else:
			recombinant_count_2 += 1
	if recombinant_count_1 == recombinant_count_2:
		shift = random.randint(1,4)
		recombinant_count_1 += shift
		recombinant_count_2 -= shift

	type_counts[recombinant_type_1] = recombinant_count_1
	if debug is True: print("recombinant count_1=", recombinant_count_1)
	type_counts[recombinant_type_2] = recombinant_count_2
	if debug is True: print("recombinant count_2=", recombinant_count_2)

	if debug is True: print("determine parental type count")
	total_parent_count = progeny_size - total_recombinant_count
	if debug is True: print("  ", parental_type, invert_genotype(parental_type, basetype), total_parent_count)
	parent_count_1 = 0
	parent_count_2 = 0
	for i in range(total_parent_count):
		if random.random() < 0.5:
			parent_count_1 += 1
		else:
			parent_count_2 += 1
	if parent_count_1 == parent_count_2:
		shift = random.randint(1,4)
		parent_count_1 += shift
		parent_count_2 -= shift

	type_counts[parental_type] = parent_count_1
	if debug is True: print("parental count_1=", parent_count_1)
	type_counts[invert_genotype(parental_type, basetype)] = parent_count_2
	if debug is True: print("parental count_2=", parent_count_2)
	return type_counts

#====================================
#====================================
def invert_genotype(genotype: str, basetype: str) -> str:
	"""
	Inverts the type of a genotype based on a given basetype.

	Parameters
	----------
	genotype : str
		The original genotype.
	basetype : str
		The basic type used as a reference for inverting the genotype.

	Returns
	-------
	str
		The new genotype after inversion.
	"""
	# Initialize an empty string to store the new genotype
	newtype = ''

	# Iterate through the length of the genotype to perform the inversion
	for i in range(len(genotype)):
		if genotype[i] == '+':
			newtype += basetype[i]
		else:
			newtype += '+'

	# Return the new inverted genotype
	return newtype
# Simple assertion test for the function: 'invert_genotype'
assert invert_genotype('+b+d', 'abcd') == 'a+c+'
assert invert_genotype('+b+', 'abc') == 'a+c'
assert invert_genotype('+b', 'ab') == 'a+'

#====================================
#====================================
def flip_gene_by_letter(genotype: str, gene_letter: str, basetype: str) -> str:
	"""
	Flips a specified gene in the genotype.

	Parameters
	----------
	genotype : str
		The original genotype.
	gene : str
		The gene to flip.
	basetype : str
		The basic type used as a reference for flipping the gene.

	Returns
	-------
	str
		The new genotype after the gene has been flipped.
	"""
	# Convert genotype string to a list for easier manipulation
	newlist = list(genotype)

	# Iterate through the genotype to find and flip the specified gene
	for i in range(len(genotype)):
		if basetype[i] == gene_letter:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'

	# Join the list back into a string to form the new genotype
	newtype = ''.join(newlist)

	# Return the new genotype
	return newtype

# Simple assertion tests for the function: 'flip_gene_by_letter'
assert flip_gene_by_letter('+b+d', 'b', 'abcd') == '+++d'
assert flip_gene_by_letter('+b+', 'c', 'abc') == '+bc'
assert flip_gene_by_letter('+b', 'a', 'ab') == 'ab'

#====================================
#====================================
def flip_gene_by_index(genotype: str, gene_index: int, basetype: str) -> str:
	"""
	Flips a specified gene in the genotype.

	Parameters
	----------
	genotype : str
		The original genotype.
	gene_index : int
		The gene number to flip. starts at 1.
	basetype : str
		The basic type used as a reference for flipping the gene.

	Returns
	-------
	str
		The new genotype after the gene has been flipped.
	"""
	# Convert genotype string to a list for easier manipulation
	newlist = list(genotype)
	gene_letter = basetype[gene_index-1]
	# Iterate through the genotype to find and flip the specified gene
	for i in range(len(genotype)):
		if basetype[i] == gene_letter:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'

	# Join the list back into a string to form the new genotype
	newtype = ''.join(newlist)

	# Return the new genotype
	return newtype

# Simple assertion tests for the function: 'flip_gene_by_letter'
assert flip_gene_by_index('+b+d', 2, 'abcd') == '+++d'
assert flip_gene_by_index('+b+', 3, 'abc') == '+bc'
assert flip_gene_by_index('+b', 1, 'ab') == 'ab'

#====================================
#====================================
def crossover_after_index(genotype: str, gene_index: str, gene_order: str) -> str:
	"""
	Flips a specified gene in the genotype.

	parent genotypes: ++++, abcd
	index 1: +bcd, a+++
	index 2: ++cd, ab++
	index 3: +++d, abc+

	Parameters
	----------
	genotype : str
		The original genotype.
	gene : str
		The gene to flip.
	gene_order : str
		The basic type used as a reference for flipping the gene.
	"""
	sorted_genes = ''.join(sorted(list(gene_order)))

	new_genotype = copy.copy(genotype)
	# Iterate through the genotype to find and flip the specified gene
	for i in range(len(genotype)):
		if i >= gene_index:
			gene_letter = gene_order[i]
			new_genotype = flip_gene_by_letter(new_genotype, gene_letter, sorted_genes)
	# Return the new genotype
	return new_genotype
assert crossover_after_index('++++', 1, 'abcd') == '+bcd'
assert crossover_after_index('++++', 2, 'abcd') == '++cd'
assert crossover_after_index('++++', 3, 'abcd') == '+++d'
assert crossover_after_index('++++', 2, 'adcb') == '+bc+'

#====================================
#====================================
def get_random_gene_order(basetype: str) -> str:
	"""
	Generates a random gene order based on all unique unordered permutations
	of the characters in the string 'basetype'.

	Parameters
	----------
	basetype : str
		The original gene order.

	Returns
	-------
	str
		A randomly chosen gene order from all unique unordered permutations.
	"""
	# Generate all permutations of the 'basetype' string
	all_permutations = set(itertools.permutations(basetype))

	# Initialize a set to store unique permutations
	unique_permutations = set()

	# Filter out reverse duplicates by only adding the lexicographically smallest of each pair
	for perm in all_permutations:
		perm_str = ''.join(perm)
		rev_perm_str = ''.join(reversed(perm))
		unique_permutations.add(min(perm_str, rev_perm_str))

	# Convert set to list
	unique_permutations = list(unique_permutations)

	# Debugging: Print information on gene order selection
	if debug is True:
		print("selecting gene order...")
		print(f'from: {unique_permutations}')

	# Randomly select a gene order from the unique permutations
	geneorder = random.choice(unique_permutations)

	# Debugging: Print the selected gene order
	if debug is True:
		print(geneorder)

	# Return the randomly selected gene order
	return geneorder

# Simple assertion test for the function: 'get_random_gene_order'
# Hard to assert due to random output, but you can test by running the function multiple times
assert get_random_gene_order('de') == 'de'
assert get_random_gene_order('abc') in ('abc', 'acb', 'bac')

if __name__ == '__main__':
	"""triplets = [(28, 20, 41), (25, 22, 43), (25, 7, 29), (22, 5, 26), (22, 10, 30), (30, 8, 35),]
	for triplet in triplets:
		print(triplet)
		a, b = calculate_interference_from_three_distances(*triplet)
		print(f'interference = {a}/{b}')
		dist = calculate_third_distance(triplet[0], triplet[1], (a, b))
		print(dist, triplet[2])"""
	print("start")

	#print(distance_triplet_generator((9,11), 45))
	a = GeneMappingClass(2, 1)
	a.setup_question()

	#for i in range(200):
	a = GeneMappingClass(3, 1)
	a.setup_question()

	#for i in range(200):
	a = GeneMappingClass(4, 1)
	a.setup_question()
