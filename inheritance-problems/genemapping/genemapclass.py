#!/usr/bin/env python3

#Built-in libraries
import copy
import math
import random
import itertools

#local libraries
import bptools
import genemaplib as gml
import phenotypes_for_flies

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
#===========================================================
#===========================================================
class GeneMappingClass:
	"""
	The GeneMappingClass simulates a genetic map for a set of genes and their associated traits.

	This class is designed to generate genetic mapping data, including distances between genes,
	interference patterns, and crossover events for a configurable number of genes (2 to 4).
	Each instance of the class can simulate progeny outcomes from genetic crosses and
	provide detailed information for test cross problems, either as multiple choice (`mc`)
	or numerical questions (`num`). The class includes methods to set gene distances,
	interference ratios, and progeny counts, and it can generate ASCII or HTML tables
	for visualization.

	Main functionalities include:
	- Setting up gene letters and gene order.
	- Generating random distances between genes, considering interference.
	- Calculating progeny counts and groupings based on crossover events.
	- Producing visual representations of the generated genetic map.
	"""
	# Class-level variable to cache distance triplets across instances
	_distance_triplet_list_cache = None

	#===========================================================
	def __init__(self, num_genes_int: int, question_count: int = 1, debug: bool = False) -> None:
		"""
		Initializes a GeneMappingClass object with specified attributes for gene mapping.

		Args:
			num_genes_int (int): The number of genes to include in the map.
			question_count (int): The number of questions to generate (default is 1).
			debug (bool): Enables debug mode to print data after initialization.

		Raises:
			ValueError: If `num_genes_int` is less than 2 or greater than 4.
		"""
		# Set debug flag
		self.debug = debug

		# Ensure that the number of genes is within the supported range (2 to 4)
		if num_genes_int < 2:
			raise ValueError("Too few genes, num_genes_int must be at least 2")
		if num_genes_int > 4:
			raise ValueError("Too many genes, num_genes_int cannot be more than 4")
		self.num_genes_int = num_genes_int

		# Basic configuration for gene mapping
		self.question_type = 'num'  # Default question type is numerical
		self.max_gene_distance = 40  # Max allowed distance between genes
		self.question_count_int = question_count  # Total questions to generate

		# Set gene labels and order
		self.set_gene_letters()  # Initializes `self.gene_letters_str` with gene symbols
		self.set_gene_order()  # Randomizes `self.gene_order_str` based on gene letters

		# Set color schemes for light and dark gene labels
		self.light_colors, self.dark_colors = bptools.light_and_dark_color_wheel(
			self.num_genes_int,
			light_color_wheel=bptools.extra_light_color_wheel
		)

		# Initialize attributes for genetic distances, progeny, and interference
		self.interference_dict = None
		self.distances_dict = None
		self.progeny_count_int = -1
		self.multiplier = 100  # Scaling factor for calculating distances

		# Initialize data structures for genotype pairs and progeny counts
		self.all_genotype_tuple_pairs_list = None
		self.progeny_groups_count_dict = None
		self.parental_genotypes_tuple = None
		self.genotype_counts = None
		self.interference_mode = False  # Default interference mode

		self.phenotype_dict = phenotypes_for_flies.phenotype_dict

		# Print initial data if debug mode is enabled
		if self.debug is True:
			self.print_gene_map_data()


	#===========================================================
	#===========================================================
	def print_gene_map_data(self) -> None:
		"""
		Prints the internal data of the gene map for debugging and analysis.

		Displays details such as gene count, gene order, distances, interference patterns,
		progeny counts, genotype pair lists, and individual genotype counts.
		"""
		print('================================')
		print(f'self.num_genes_int = {self.num_genes_int}')
		print(f'self.gene_letters_str = {self.gene_letters_str}')
		print(f'self.gene_order_str = {self.gene_order_str}')

		# Print distances between genes
		if self.distances_dict is not None:
			print('self.distances_dict = {')
			for key, value in self.distances_dict.items():
				print(f'  {key}: {value} # gene '
					+f'{self.gene_order_str[key[0]-1].upper()} and '
					+f'{self.gene_order_str[key[1]-1].upper()} '
				)
			print('}')

		# Print interference values
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

		# Print progeny count and grouping details
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

		# Print genotype pair lists and counts
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
	def set_gene_letters(self) -> None:
		"""
		Sets the gene letters (symbols) for the gene map, stored in `self.gene_letters_str`.

		Uses a function from `genemaplib` to obtain a string of unique letters representing genes.
		"""
		self.gene_letters_str = gml.get_gene_letters(self.num_genes_int)

	#===========================================================
	#===========================================================
	def set_gene_order(self) -> None:
		"""
		Sets the order of genes within the map by randomly shuffling `gene_letters_str`.
		"""
		self.gene_order_str = gml.get_random_gene_order(self.gene_letters_str)

	#===========================================================
	#===========================================================
	def setup_question(self):
		"""
		Prepares the gene map for a question by setting distances, progeny counts, and genotype lists.

		This method calls several helper functions to initialize various properties required
		for a genetic question, including distances, progeny group counts, and genotype pairs.
		"""
		self.set_gene_distances()               # Sets genetic distances between gene pairs
		self.set_progeny_count()                # Sets the total progeny count for the map
		self.set_progeny_groups_counts()        # Sets counts for different progeny groups
		self.set_all_genotype_tuple_pairs_list()  # Sets pairs of genotypes for the map
		self.set_parental_genotypes()           # Chooses parental genotypes for the map
		self.set_genotype_counts()              # Sets counts for each genotype

	#===========================================================
	#===========================================================
	def map_gene_order_to_alphabetical(self, gene_order_index) -> int:
		"""
		Maps a given gene order index to the alphabetical index in the gene letters string.

		Args:
			gene_order_index (int): The position of the gene in `gene_order_str`.

		Returns:
			int: The 1-based index of the gene in `gene_letters_str`.

		Raises:
			ValueError: If `gene_order_index` is out of bounds.
		"""
		# Ensure the index is within valid range
		if gene_order_index < 1 or gene_order_index > self.num_genes_int:
			raise ValueError(f'gene order index must be 1 <= {gene_order_index} <= {self.num_genes_int}')

		# Get the gene letter from the gene order string
		gene_letter = self.gene_order_str[gene_order_index - 1]

		# Find the position of the gene letter in `gene_letters_str` and return it as a 1-based index
		gene_alphabet_index = self.gene_letters_str.find(gene_letter) + 1
		return gene_alphabet_index

	#===========================================================
	#===========================================================
	def map_gene_order_pair_to_alphabetical_pair(self, gene_order_index1, gene_order_index2) -> tuple:
		"""
		Maps a pair of gene order indices to their alphabetical indices in the gene letters string.

		Args:
			gene_order_index1 (int): The first gene position in `gene_order_str`.
			gene_order_index2 (int): The second gene position in `gene_order_str`.

		Returns:
			tuple: A tuple containing the alphabetical indices of the two genes, in ascending order.
		"""
		# Map each gene order index to its alphabetical index
		gene_alphabet_index1 = self.map_gene_order_to_alphabetical(gene_order_index1)
		gene_alphabet_index2 = self.map_gene_order_to_alphabetical(gene_order_index2)

		# Return the pair in ascending order
		if gene_alphabet_index1 < gene_alphabet_index2:
			return gene_alphabet_index1, gene_alphabet_index2
		else:
			return gene_alphabet_index2, gene_alphabet_index1

	#===========================================================
	#===========================================================
	def set_gene_distances(self, min_distance=2) -> None:
		"""
		Sets the genetic distances between gene pairs.

		Args:
			min_distance (int): The minimum possible distance between gene pairs (default is 2).

		Chooses different methods for setting distances based on the question type (`mc` or `num`).
		Prints the data if debug mode is enabled.
		"""
		if self.question_type == 'mc':
			self.set_gene_distances_mc(min_distance)
		else:
			self.set_gene_distances_int(min_distance)

		# Print updated gene map data if in debug mode
		if self.debug is True:
			self.print_gene_map_data()

	#===========================================================
	#===========================================================
	def get_two_decimal_rand(self, min_value: int = 9, multiplier: int = None) -> float:
		"""
		Generates a random float with two decimal places within a specified range.

		Args:
			min_value (int): The minimum value for the random number generation (default is 9).
			multiplier (int): Scaling factor for decimal precision (default is `self.multiplier`).

		Returns:
			float: A randomly generated number with two decimal places within the range.
		"""
		# Use the class-level multiplier if none is provided
		if multiplier is None:
			multiplier = self.multiplier

		# Generate a random integer within the scaled range and then divide to get two decimal places
		two_decimal_rand = random.randint(min_value * multiplier, self.max_gene_distance * multiplier)
		return two_decimal_rand / float(multiplier)

	#===========================================================
	#===========================================================
	def set_gene_distances_mc(self, min_distance=2) -> None:
		"""
		Sets genetic distances for multiple-choice questions, with specific interference calculations.

		Args:
			min_distance (int): The minimum possible distance between gene pairs (default is 2).

		Raises:
			NotImplementedError: If `num_genes_int` is greater than 3.
		"""
		if self.num_genes_int == 2:
			# For two genes, set a single distance
			distance = self.get_two_decimal_rand(min_value=9)
			self.distances_dict = {(1, 2): distance}

		elif self.num_genes_int == 3:
			# For three genes, set distances with interference for the third gene
			self.distances_dict = {}
			distance_pair = [
				self.get_two_decimal_rand(min_value=3),
				self.get_two_decimal_rand(min_value=3)
			]

			# Randomly assign the pair to (1,2) and (2,3)
			if random.random() < 0.5:
				self.distances_dict[(1, 2)] = distance_pair[0]
				self.distances_dict[(2, 3)] = distance_pair[1]
			else:
				self.distances_dict[(1, 2)] = distance_pair[1]
				self.distances_dict[(2, 3)] = distance_pair[0]

			# Set interference between non-adjacent genes
			interference_tuple = (
				random.randint(1, 7),
				random.randint(8, 12)
			)
			distance3 = gml.calculate_third_distance(distance_pair[0], distance_pair[1], interference_tuple)
			self.distances_dict[(1, 3)] = distance3
			self.interference_dict = {(1, 3): interference_tuple}

		elif self.num_genes_int >= 4:
			# Not implemented for four or more genes in multiple-choice format
			raise NotImplementedError

	#===========================================================
	#===========================================================
	def set_gene_distances_int(self, min_distance=2) -> None:
		"""
		Sets genetic distances for numerical questions without interference constraints.

		Args:
			min_distance (int): The minimum possible distance between gene pairs (default is 2).

		Uses different setups depending on the number of genes (2 to 4). For three genes,
		calculates a third distance and interference ratio using a helper function. For four genes,
		sets hardcoded distances and interference ratios.

		Raises:
			NotImplementedError: If `num_genes_int` is 5 or more.
		"""
		if self.num_genes_int == 2:
			# For two genes, set a single random distance
			distance = random.randint(min_distance, self.max_gene_distance)
			self.distances_dict = {(1, 2): distance}

		elif self.num_genes_int == 3:
			# For three genes, generate three distances, using a distance triplet
			self.distances_dict = {}
			distance_triplet = self.get_one_distance_triplet(
				max_gene_distance=self.max_gene_distance,
				interference_mode=self.interference_mode
			)
			# Randomly assign the first two distances
			if random.random() < 0.5:
				self.distances_dict[(1, 2)] = distance_triplet[0]
				self.distances_dict[(2, 3)] = distance_triplet[1]
			else:
				self.distances_dict[(1, 2)] = distance_triplet[1]
				self.distances_dict[(2, 3)] = distance_triplet[0]

			# Set the distance for non-adjacent genes and calculate interference
			self.distances_dict[(1, 3)] = distance_triplet[2]
			interference_tuple = gml.calculate_interference_from_three_distances(*distance_triplet)
			self.interference_dict = {(1, 3): interference_tuple}

		elif self.num_genes_int == 4:
			# Hardcoded distances and interference for four genes
			self.distances_dict = {
				(1, 2): 5,
				(2, 3): 10,
				(3, 4): 15,
				(1, 3): 15,
				(2, 4): 25,
				(1, 4): 30,
			}
			self.interference_dict = {
				(1, 3): (1, 1),
				(2, 4): (1, 1),
				(1, 4): (1, 1),
			}

		elif self.num_genes_int >= 5:
			# Not implemented for five or more genes
			raise NotImplementedError

	#====================================
	#====================================
	@classmethod
	def get_one_distance_triplet(cls, max_fraction_int: int = 12, max_gene_distance: int = 40, interference_mode: bool = False) -> list:
		"""
		Fetches a single distance triplet for three-gene scenarios, optionally considering interference.

		Args:
			max_fraction_int (int): The maximum allowable fraction for interference calculations.
			max_gene_distance (int): The maximum distance between genes.
			interference_mode (bool): Whether to use interference-based triplet generation.

		Returns:
			list: A list of three distances between genes.

		If the distance triplet list has already been cached, it randomly selects a triplet from the cache.
		If interference mode is enabled, it uses a different function to generate triplets.

		interference_mode = True:
			Generates a list of unique distance triplets based on interference fractions,
			with a fixed denominator of 100 for each fraction.
			interference is always a whole number when multiplied by 100

		interference_mode = False:
			uses a tuple representing the interference fraction (a, b).
			interference is a rational value or fraction value
		"""
		# Return cached triplet list if it exists
		if cls._distance_triplet_list_cache is not None:
			return random.choice(cls._distance_triplet_list_cache)

		# Generate triplet list based on interference mode
		if interference_mode:
			max_fraction_int = 99
			distance_triplet_list = gml.get_all_distance_triplets_INTERFERENCE(max_fraction_int, max_gene_distance)
		else:
			distance_triplet_list = gml.get_all_distance_triplets(max_fraction_int, max_gene_distance)

		# Cache the triplet list and return a random choice
		cls._distance_triplet_list_cache = distance_triplet_list
		return random.choice(distance_triplet_list)

	#====================================
	#====================================
	def set_progeny_count(self) -> None:
		"""
		Sets the total progeny count for the gene map based on question type and distances.

		For multiple-choice (`mc`) questions, distances are floats, so progeny count calculation
		is done with scaling and rounding to ensure an integer result. For numerical questions,
		it uses a general progeny size function from `genemaplib`.

		Raises:
			ValueError: If the calculated progeny count is not an integer.
		"""
		# Progeny count calculation varies by question type
		if self.question_type == 'mc':
			# DISTANCES ARE FLOATS
			values = [100]
			for val in self.distances_dict.values():
				values.append(int(round(val * 100)))
			gcd = math.gcd(*values)
			progeny_count = random.randint(2, 29) * 10000 / gcd

			# Check if progeny count is almost an integer
			if not gml.is_almost_integer(progeny_count):
				self.print_gene_map_data()
				raise ValueError(f"progeny count error: {progeny_count:.8f}")
			self.progeny_count_int = int(round(progeny_count))

		else:
			# For numerical questions, calculate progeny size directly
			self.progeny_count_int = gml.get_general_progeny_size(tuple(self.distances_dict.values()))

		# Print the updated progeny count if in debug mode
		if self.debug:
			self.print_gene_map_data()

	#====================================
	#====================================
	def calculate_triple_crossovers(self, gene_pair: tuple) -> int:
		"""
		Calculates the number of triple crossovers (TCO) between two non-adjacent genes.

		Args:
			gene_pair (tuple): A tuple representing a non-adjacent gene pair (e.g., (1,3)).

		Returns:
			int: The calculated number of triple crossovers.

		Raises:
			ValueError: If the gene pair is not a valid triple crossover pair or if the result is not an integer.
		"""
		# Ensure gene pair represents a triple crossover (non-adjacent)
		if gene_pair[1] - gene_pair[0] != 3:
			raise ValueError(f"gene pair is not a triple crossover, {gene_pair}")

		# Calculate triple crossover without interference
		no_interference_TCO = self.progeny_count_int
		for x in range(gene_pair[0], gene_pair[1]):
			no_interference_TCO *= self.distances_dict[(x, x + 1)] / 100
		if self.debug:
			print(f'no_interference_TCO={no_interference_TCO:.3f}')

		# Apply interference correction
		interference_tuple = self.interference_dict[gene_pair]
		Interference_TCO = no_interference_TCO * (interference_tuple[1] - interference_tuple[0]) / interference_tuple[1]
		if not gml.is_almost_integer(Interference_TCO):
			raise ValueError(f'Interference_TCO={Interference_TCO:.5f} is NOT an integer')

		Interference_TCO = int(round(Interference_TCO))
		if self.debug:
			print(f'Interference_TCO for {gene_pair}={Interference_TCO:d}')
		return Interference_TCO

	#====================================
	#====================================
	def calculate_double_crossovers(self, gene_pair: tuple) -> int:
		"""
		Calculates the number of double crossovers (DCO) between two adjacent genes.

		Args:
			gene_pair (tuple): A tuple representing a gene pair for double crossover (e.g., (1,3) for three genes).

		Returns:
			int: The calculated number of double crossovers.

		Raises:
			ValueError: If the gene pair is not valid for double crossover or if the calculated value is not an integer.
		"""
		# Ensure gene pair represents a double crossover (the genes should be separated by one other gene)
		if gene_pair[1] - gene_pair[0] != 2:
			raise ValueError(f"gene pair is not a double crossover, {gene_pair}")

		# Calculate the expected double crossover without interference
		no_interference_DCO = self.progeny_count_int
		for x in range(gene_pair[0], gene_pair[1]):
			no_interference_DCO *= self.distances_dict[(x, x + 1)] / 100
		if self.debug:
			print(f'no_interference_DCO={no_interference_DCO:.3f}')

		# Apply interference correction using interference ratios from `self.interference_dict`
		interference_tuple = self.interference_dict[gene_pair]
		Interference_DCO = no_interference_DCO * (interference_tuple[1] - interference_tuple[0]) / interference_tuple[1]

		# Ensure the result is an integer, if not raise an error
		if self.question_type != 'mc' and not gml.is_almost_integer(Interference_DCO):
			raise ValueError(f'Interference_DCO={Interference_DCO:.5f} is NOT an integer')

		# Round and convert to integer for the final count
		Interference_DCO = int(round(Interference_DCO))
		if self.debug:
			print(f'Interference_DCO for {gene_pair}={Interference_DCO:d}')
		return Interference_DCO

	#====================================
	#====================================
	def calculate_single_crossover(self, gene_pair: tuple) -> int:
		"""
		Calculates the number of single crossovers (SCO) between two adjacent genes.

		Args:
			gene_pair (tuple): A tuple representing an adjacent gene pair (e.g., (1,2)).

		Returns:
			int: The calculated number of single crossover progeny.

		Raises:
			ValueError: If the gene pair is not valid for single crossover or if the result is not an integer.
		"""
		# Ensure gene pair represents a single crossover (adjacent genes)
		if gene_pair[1] - gene_pair[0] != 1:
			raise ValueError(f"gene pair is not a single crossover, {gene_pair}")

		# Calculate the single crossover progeny count based on distance and total progeny
		sco_progeny = self.progeny_count_int * self.distances_dict[gene_pair] / 100

		# Check that the result is an integer
		if not gml.is_almost_integer(sco_progeny):
			raise ValueError(f'sco_progeny for {gene_pair}={sco_progeny:.5f} is NOT an integer')

		# Convert to integer and return the final count
		sco_progeny = int(round(sco_progeny))
		if self.debug:
			print(f'sco_progeny for {gene_pair}={sco_progeny:d}')
		return sco_progeny

	#====================================
	#====================================
	def set_progeny_groups_counts(self):
		"""
		Calculates and sets progeny group counts for single, double, and triple crossovers.

		This method:
		1. Determines gene pairs based on their distance (single, double, or triple crossovers).
		2. Calculates raw counts for each crossover type (SCO, DCO, TCO) based on the gene pairs.
		3. Adjusts SCO counts by subtracting DCO counts that overlap with each SCO.
		4. Sets the remaining progeny count as the parental type.

		Raises:
			ValueError: If the total count of all progeny groups does not match the total progeny count.
		"""
		"""
		Example gene map layout:
		A - x - B - y - C
		A - z - C

		Where:
		- `A`, `B`, and `C` represent three genes.
		- `x`, `y`, and `z` represent distances in centiMorgans (cM) between these genes.
		- `x` is the distance between genes A and B.
		- `y` is the distance between genes B and C.
		- `z` is the direct distance between genes A and C, where z >= x + y

		Steps to calculate crossover events for progeny groups:

		1. Determine the `interference_tuple` for each gene pair.
			- The `interference_tuple` is typically represented as a pair of numbers (a, b).
			- Interference is the phenomenon where the occurrence of one crossover event reduces (or enhances) the probability of another crossover happening nearby.
			- The `interference_tuple` modifies the expected crossover frequencies and must be applied to adjust DCO (double crossover) counts accordingly.

		2. Calculate DCO (double crossovers) for relevant gene pairs.
			- `DCO from A-B`: Calculate the double crossovers between genes A and B.
			- `DCO from A-C`: Calculate the double crossovers between genes A and C.
			- Use the `interference_tuple` in these calculations to account for interference effects.

		3. Ensure that DCO counts are integers.
			- Since crossover counts represent actual progeny numbers, they must be integers.
			- After calculating DCO counts, round them and check to ensure they are integers.

		4. Calculate SCO (single crossovers) for adjacent gene pairs and adjust for overlapping DCOs.
			- `determine SCO(x) for A-B genotype pairs, subtract DCO`: Calculate the single crossover count for the distance `x` (between genes A and B).
				- Then subtract any overlapping DCO contributions to avoid double-counting.
			- `determine SCO(y) for B-C genotype pairs, subtract DCO`: Similarly, calculate the single crossover count for the distance `y` (between genes B and C) and adjust by removing overlapping DCO contributions.

		5. Assign remaining progeny counts to the "parental" genotype group.
			- After accounting for all crossover types (SCO, DCO, TCO), any remaining progeny counts are assigned to the parental genotype group, which represents progeny with no crossovers.

		Formula Breakdown (specific to a three-gene scenario):

		For three genes (A, B, and C) with distances `x` and `y`:

		- `dco = Xc * Yc * N * (b - a) / b`
			- `dco`: The expected number of double crossovers between A and C.
			- `Xc` and `Yc`: These are crossover frequencies (proportional to distances x and y, respectively) for A-B and B-C.
			- `N`: Total progeny count.
			- `(b - a) / b`: Interference adjustment factor, where `a` and `b` come from the `interference_tuple`. This factor reduces the expected DCO count based on the level of interference.

		- `sx = N * Xc - dco`
			- `sx`: The adjusted count for single crossovers between genes A and B.
			- This is calculated as the expected count of crossovers based on distance `x` (i.e., `N * Xc`), minus any DCO contributions that overlap with this region.

		- `sy = N * Yc - dco`
			- `sy`: The adjusted count for single crossovers between genes B and C.
			- Similarly, this is the expected count of crossovers based on distance `y` (i.e., `N * Yc`), minus overlapping DCO contributions.

		Terminology:
		- `DCO`: Double Crossover - where two crossovers occur within a single progeny between non-adjacent genes (e.g., A and C).
		- `SCO`: Single Crossover - where a single crossover occurs between adjacent genes (e.g., A-B or B-C).
		- `sx`: The SCO count for the gene pair separated by distance `x`.
		"""

		# Create a dictionary to categorize gene pairs based on their separation (distance)
		# This categorization allows us to separately handle triple crossovers (distance of 3),
		# double crossovers (distance of 2), and single crossovers (distance of 1).
		gene_diff_pairs = {}
		for gene1 in range(1, self.num_genes_int):
			for gene2 in range(gene1 + 1, self.num_genes_int + 1):
				diff = gene2 - gene1
				# Add gene pair to the appropriate list in the dictionary based on their distance
				gene_diff_pairs[diff] = gene_diff_pairs.get(diff, []) + [(gene1, gene2)]

		if self.debug:
			print(f'gene_diff_pairs={gene_diff_pairs}')

		# Initialize dictionary to store progeny counts for each crossover type
		self.progeny_groups_count_dict = {}

		# Calculate triple crossovers (TCO) for gene pairs separated by two other genes
		for gene_pair in gene_diff_pairs.get(3, []):
			# Example: (1, 4) in a four-gene map would be a triple crossover
			self.progeny_groups_count_dict[gene_pair] = self.calculate_triple_crossovers(gene_pair)

		# Calculate double crossovers (DCO) for gene pairs separated by one other gene
		for gene_pair in gene_diff_pairs.get(2, []):
			# Example: (1, 3) in a three-gene map would be a double crossover
			self.progeny_groups_count_dict[gene_pair] = self.calculate_double_crossovers(gene_pair)

		# Calculate single crossovers (SCO) for adjacent gene pairs
		for gene_pair in gene_diff_pairs.get(1, []):
			# Example: (1, 2) or (2, 3) in a three-gene map would be single crossovers
			self.progeny_groups_count_dict[gene_pair] = self.calculate_single_crossover(gene_pair)

		# Adjust SCO counts by subtracting overlapping DCO counts
		# Since DCO events contribute to both SCO events on either side, we must remove this overlap.
		for gene_pair in gene_diff_pairs.get(1, []):
			# For each SCO pair, subtract DCO counts associated with the neighboring gene pairs
			# Example: For the SCO pair (1,2), subtract DCO counts from pairs like (1,3) and (2,4)
			for gene_index in gene_pair:
				# Check if the gene index can form a DCO with a gene two positions away
				if gene_index + 2 <= self.num_genes_int:
					new_gene_pair = (gene_index, gene_index + 2)
					self.progeny_groups_count_dict[gene_pair] -= self.progeny_groups_count_dict[new_gene_pair]
				elif gene_index - 2 >= 1:
					new_gene_pair = (gene_index - 2, gene_index)
					self.progeny_groups_count_dict[gene_pair] -= self.progeny_groups_count_dict[new_gene_pair]

		# Print warning if gene count exceeds three, as functionality is not fully implemented for larger numbers
		if self.num_genes_int > 3:
			print('MORE THAN 3 genes WARNING NOT IMPLEMENTED YET')

		"""
		three gene:
		dco = Xc * Yc * N * (b - a) / b
		sx = N * Xc - dco
		sy = N * Yc - dco
		"""
		# Calculate the count for parental genotypes as the remainder after accounting for all crossovers
		# The parental count is the remaining progeny count after accounting for single, double, and triple crossovers.
		parent_count_int = self.progeny_count_int - sum(self.progeny_groups_count_dict.values())
		self.progeny_groups_count_dict['parental'] = parent_count_int

		# Verify that the total progeny counts match the expected progeny count
		total_count = sum(self.progeny_groups_count_dict.values())
		if total_count != self.progeny_count_int:
			raise ValueError(f'counts do not add up {total_count} vs expected {self.progeny_count_int}')

	#====================================
	#====================================
	def set_all_genotype_tuple_pairs_list(self):
		"""
		Generates all possible genotype pairs and stores them as a list of unique pairs.

		This function uses the gene letters to create all possible genotypes, then pairs each genotype with its "inverted" version
		(e.g., `"+a"` paired with `"a+"` for a two-gene system). Each pair is sorted and stored in a set to ensure uniqueness,
		then converted back to a list for further use in the class.

		Raises:
			ValueError: If the number of unique genotype pairs does not match the expected half of total genotypes.
		"""
		# Generate all possible genotypes based on the gene letters
		all_genotypes = gml.generate_genotypes(self.gene_letters_str)
		self.all_genotype_tuple_pairs_list = []
		genotype_tuple_pairs_set = set()

		# Iterate over each genotype to find its inverted pair and add both as a sorted tuple to the set
		for genotype in all_genotypes:
			# Get the "inverted" genotype (e.g., `"+a"` becomes `"a+"` if `gene_letters_str` is "ab")
			inverted = gml.invert_genotype(genotype, self.gene_letters_str)
			# Sort the pair to ensure consistency (e.g., `("a+", "+a")` always becomes `("+a", "a+")`)
			pair = sorted([genotype, inverted])
			genotype_tuple_pairs_set.add(tuple(pair))

		# Validate the number of unique pairs is as expected (half of all genotypes)
		if len(genotype_tuple_pairs_set) != len(all_genotypes) // 2:
			print(genotype_tuple_pairs_set)
			print(all_genotypes)
			raise ValueError(f'len(genotype_tuple_pairs_set) {len(genotype_tuple_pairs_set)} != '
					+f'len(all_genotypes)//2 {len(all_genotypes)}//2')

		# Convert the set of unique pairs into a list for further use in the class
		self.all_genotype_tuple_pairs_list = list(genotype_tuple_pairs_set)

	#====================================
	#====================================
	def set_parental_genotypes(self):
		"""
		Randomly selects a pair of genotypes to represent the parental genotypes.

		This function chooses a random genotype pair from `self.all_genotype_tuple_pairs_list` and assigns it as the
		`parental_genotypes_tuple`, which will be used to identify the parental types in the progeny.

		If debugging is enabled, it also prints the gene map data.
		"""
		# Randomly choose one pair of genotypes as the parental genotypes
		self.parental_genotypes_tuple = random.choice(self.all_genotype_tuple_pairs_list)

		# If debugging is enabled, print the current gene map data
		if self.debug is True:
			self.print_gene_map_data()

	#====================================
	#====================================
	def set_genotype_counts(self) -> dict:
		"""
		Assigns counts to each genotype based on crossover events and progeny distribution.

		This function distributes progeny counts across various genotypes by:
		1. Splitting the parental count between the two parental genotypes.
		2. Iteratively assigning counts to each crossover type (SCO, DCO) based on gene pairs and adjusting for crossovers.

		Raises:
			ValueError: If the total count of all genotypes does not match the expected progeny count.

		Returns:
			dict: A dictionary with genotypes as keys and their assigned progeny counts as values.
		"""
		"""self.progeny_groups_count_dict = {
			'parental': parent_count_int,
			'dco': reduced_DCO,
			'sco': {
				'(1,2)': sy,
				'(2,3)': sx,
			},
		}"""
		self.genotype_counts = {}

		# Split parental count between the two parental genotypes
		p_genotype1, p_genotype2 = self.parental_genotypes_tuple
		p_count1, p_count2 = gml.split_number_in_two(self.progeny_groups_count_dict['parental'])
		self.genotype_counts[p_genotype1] = p_count1
		self.genotype_counts[p_genotype2] = p_count2

		# Assign counts for crossover events based on each gene pair
		for gene_index1 in range(1, self.num_genes_int):
			for gene_index2 in range(gene_index1 + 1, self.num_genes_int + 1):
				gene_pair = (gene_index1, gene_index2)

				# Split progeny count for this gene pair between two genotypes
				progeny_count1, progeny_count2 = gml.split_number_in_two(self.progeny_groups_count_dict[gene_pair])
				geno_type_1, geno_type_2 = copy.copy((p_genotype1, p_genotype2))

				# Apply crossovers to generate new genotypes from parental genotypes
				for crossover_index in range(gene_index1, gene_index2):
					geno_type_1 = gml.crossover_after_index(geno_type_1, crossover_index, self.gene_order_str)
					geno_type_2 = gml.crossover_after_index(geno_type_2, crossover_index, self.gene_order_str)

				# Store the generated genotypes with their corresponding counts
				self.genotype_counts[geno_type_1] = progeny_count1
				self.genotype_counts[geno_type_2] = progeny_count2

		# Verify that the total count matches the expected progeny count
		total_count = sum(self.genotype_counts.values())
		if total_count != self.progeny_count_int:
			raise ValueError(f'counts do not add up {total_count} vs expected {self.progeny_count_int}')

		# Print gene map data if debugging is enabled
		if self.debug is True:
			self.print_gene_map_data()

	#====================================
	#====================================
	def values_to_text(self, values: tuple) -> str:
		"""
		Converts a tuple of values into a formatted HTML string representing the genetic distance.

		This function takes a list of progeny counts for a gene pair and:
		1. Sums the values to get the total count of recombinants.
		2. Formats these counts as a fraction of the total progeny count, then converts it to centiMorgans (cM).

		Args:
			values (tuple): A tuple containing counts for one or more genotypes.

		Returns:
			str: A formatted HTML string showing the calculated genetic distance in cM.
		"""
		# Sum recombinant counts
		val_sum = sum(values)

		# Build numerator text: either a sum (e.g., 3,100 + 2,400) or the single value
		if len(values) > 1:
			numerator_str = '(' + ' + '.join(f'{v:,d}' for v in sorted(values)) + ')'
		else:
			numerator_str = f'{val_sum:,d}'

		# Start with the fraction using proper <sup>/<sub> pairing
		total_str = f'{self.progeny_count_int:,d}'
		choice_text = (
			f'<sup>{numerator_str}</sup>/<sub>{total_str}</sub> = '
		)

		# Add the total recombinant count to the numerator and format the fraction
		choice_text += f'<sup>{val_sum:,d}</sup>/<sub>{self.progeny_count_int:,d}</sub> = '

		# Calculate the fraction as a decimal and convert to centiMorgans (cM)
		float_val = val_sum / float(self.progeny_count_int)
		choice_text += f'{float_val:.4f} = '  # Show the fraction as a decimal

		# Display the final genetic distance in cM
		choice_text += f'<strong>{float_val*100:.2f} cM</strong>'

		return choice_text

	#====================================
	#====================================
	def get_all_recombinants_for_gene_pair(self, gene_pair: tuple) -> list:
		"""
		Identifies all recombinant genotypes for a specified gene pair.

		Recombinants are genotypes where one gene in the pair matches the parental type,
		while the other does not, indicating a crossover event. This function:
		1. Finds the indices of the two genes in the `gene_pair`.
		2. Iterates over all genotypes and checks if each genotype is recombinant for the gene pair.

		Args:
			gene_pair (tuple): A tuple representing the gene pair (e.g., ('A', 'B')).

		Returns:
			list: A list of recombinant genotypes for the specified gene pair.
		"""
		recombinants = []
		gene_index1 = self.gene_letters_str.find(gene_pair[0])  # Index of the first gene in the gene pair
		gene_index2 = self.gene_letters_str.find(gene_pair[1])  # Index of the second gene in the gene pair

		# Iterate through each genotype and identify recombinant genotypes
		for genotype in self.genotype_counts.keys():
			for ptype in self.parental_genotypes_tuple:
				# A recombinant genotype has one gene matching the parental type and the other differing
				if genotype[gene_index1] == ptype[gene_index1] and genotype[gene_index2] != ptype[gene_index2]:
					recombinants.append(genotype)
		return recombinants

	#====================================
	#====================================
	def get_counts_from_genotype_list(self, genotype_list: list) -> list:
		"""
		Returns the progeny counts for a specified list of genotypes.

		This function iterates through the provided genotypes and retrieves their counts from `self.genotype_counts`,
		accumulating them into a list.

		Args:
			genotype_list (list): A list of genotypes for which counts are to be retrieved.

		Returns:
			list: A list of progeny counts corresponding to each genotype in `genotype_list`.
		"""
		counts = []
		for genotype in genotype_list:
			count = self.genotype_counts[genotype]  # Retrieve count for each genotype
			counts.append(count)  # Append the count to the result list
		return counts

	#=====================
	#=====================
	def add_combinations(self, k: int, choices_set: set, max_choices: int = None):
		"""
		Helper for make_choices().
		Add combinations of genotypes of length k as distractors, preferring
		a diverse spread of fractions when max_choices is set.

		Args:
			k (int): Size of genotype combination (2, 3, 4, etc.).
			choices_set (set): Existing set of genotype tuples to avoid duplicates.
			max_choices (int, optional): Cap on number of new choices to return.

		Returns:
			set: New HTML-formatted choices generated in this call.

		Modifies: choices_set
		"""
		candidates = []
		all_genotypes = list(self.genotype_counts.keys())

		for combo in itertools.combinations(all_genotypes, k):
			combo_tuple = tuple(sorted(combo))
			if combo_tuple in choices_set:
				continue
			values_list = [self.genotype_counts[gt] for gt in combo_tuple]
			frac = sum(values_list) / float(self.progeny_count_int)
			if frac > 0.51:
				continue
			candidates.append((frac, combo_tuple, values_list))

		# Nothing to add
		if not candidates:
			return set()

		# If no cap, return all
		if max_choices is None or max_choices >= len(candidates):
			new_texts = set()
			for frac, combo_tuple, values_list in candidates:
				choices_set.add(combo_tuple)
				new_texts.add(self.values_to_text(values_list))
			return new_texts

		# Greedy diverse selection on fraction space
		candidates.sort(key=lambda x: x[0])  # sort by frac
		selected = []

		# seed with extremes
		selected.append(candidates[0])
		if len(selected) < max_choices and len(candidates) > 1:
			selected.append(candidates[-1])

		# pick next items maximizing min distance to selected set
		def min_dist_to_selected(f):
			return min(abs(f - s[0]) for s in selected)

		while len(selected) < max_choices and len(selected) < len(candidates):
			best = max(
				(c for c in candidates if c not in selected),
				key=lambda c: min_dist_to_selected(c[0])
			)
			selected.append(best)

		# Emit results
		new_texts = set()
		for frac, combo_tuple, values_list in selected:
			choices_set.add(combo_tuple)
			new_texts.add(self.values_to_text(values_list))
		return new_texts

	#=====================
	#=====================
	def make_choices(self, gene_pair: tuple = None, num_choices: int = 6):
		"""
		Generates a list of possible answer choices for the genetic distance question.

		This function:
		1. Identifies the correct answer by calculating the recombinant fraction for the specified gene pair.
		2. Generates random incorrect choices by selecting random genotype counts and calculating their fractions.
		3. Ensures each choice is formatted as a genetic distance in centiMorgans (cM).

		This emphasizes distractors that sum the same count of genotypes
		as the true recombinant numerator by swapping items in and out.

		Args:
			gene_pair (tuple, optional): A tuple specifying the gene pair for which choices are generated.
			If `self.num_genes_int` is 2, defaults to the entire gene order.

		Returns:
			list, str: A list of formatted choices in HTML and the correct answer as a string.

		Raises:
			NotImplementedError: If the function is called with more than three genes.
			ValueError: If `gene_pair` is not provided for three-gene setups.
		"""
		# Ensure the function is only called for two or three genes
		if self.num_genes_int > 3:
			raise NotImplementedError('This function was only designed for three genes or fewer')

		# Set the default gene pair for two-gene setups
		if gene_pair is None and self.num_genes_int == 2:
			gene_pair = tuple(self.gene_order_str)
		elif gene_pair is None:
			raise ValueError('Need input gene_pair')

		choices_text_set = set()  # Use a set to ensure unique choices
		choices_set = set()  # Use a set to ensure unique choices

		# Calculate the correct answer based on recombinant genotypes
		recomb_genotypes = self.get_all_recombinants_for_gene_pair(gene_pair)
		recomb_set = set(recomb_genotypes)
		recomb_counts = self.get_counts_from_genotype_list(recomb_genotypes)
		answer_text = self.values_to_text(recomb_counts)
		print(f'answer_text={answer_text}')
		choices_set.add(tuple(sorted(recomb_set)))
		choices_text_set.add(answer_text)

		# Calculate the parental fraction and add as an incorrect distractor choice
		parent_values = self.get_counts_from_genotype_list(self.parental_genotypes_tuple)
		parent_text = self.values_to_text(parent_values)
		print(f'parent_text={parent_text}')
		choices_set.add(tuple(sorted(self.parental_genotypes_tuple)))
		choices_text_set.add(parent_text)

		# Generate random incorrect choices
		if self.num_genes_int == 2:
			# All 2-item pairs of genotypes
			needed_choices = num_choices - len(choices_text_set)
			choices_text_set |= self.add_combinations(2, choices_set, needed_choices)
			# If still short, add singles with small fractions
			if len(choices_text_set) < num_choices:
				needed_choices = num_choices - len(choices_text_set)
				choices_text_set |= self.add_combinations(1, choices_set, needed_choices)
		elif self.num_genes_int == 3:
			# All 2-item pairs of genotypes
			needed_choices = num_choices - len(choices_text_set)
			choices_text_set |= self.add_combinations(4, choices_set, needed_choices)
			# If still short, add triples with small fractions
			if len(choices_text_set) < num_choices:
				needed_choices = num_choices - len(choices_text_set)
				choices_text_set |= self.add_combinations(3, choices_set, needed_choices)
			# If still short, add pairs with small fractions
			if len(choices_text_set) < num_choices:
				needed_choices = num_choices - len(choices_text_set)
				choices_text_set |= self.add_combinations(2, choices_set, needed_choices)

		return sorted(choices_text_set), answer_text

	#====================================
	#====================================
	def is_valid_html(self, html_text) -> bool:
		"""
		Validates the given HTML text.

		This function checks if the provided HTML text is valid by calling `gml.is_valid_html()`.
		It acts as a wrapper around the HTML validation function, which likely checks for syntax
		and structural correctness of the HTML content.

		Args:
			html_text (str): The HTML text to validate.

		Returns:
			bool: True if the HTML text is valid, False otherwise.
		"""
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
			phenotype_string = gml.get_phenotype_name_for_genotype(genotype, self.phenotype_dict)
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
			phenotype_string = gml.get_phenotype_name_for_genotype(genotype, self.phenotype_dict)

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
		#table += '<p>The resulting phenotypes are summarized in the table above.</p> '

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
		return gml.get_phenotype_info(self.gene_letters_str, self.phenotype_dict, self.dark_colors)

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
	print(a.get_question_header())
	print(a.get_progeny_ascii_table())

	#for i in range(200):
	"""
	a = GeneMappingClass(4, 1)
	a.debug = False
	a.setup_question()
	a.print_gene_map_data()
	"""
