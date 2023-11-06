
import re
import copy
import math
import random
import itertools

debug = False


#====================================
#====================================
# Dictionary to describe hypothetical fruit fly phenotypes
phenotype_description_dict = {
	'artsy':   'has wings that are colorful and distinctive patterns.',
	'bumpy':   'has a skin texture that is not smooth, but rough with small bumps all over.',
	'chummy':  'shows behavior where it always maintains a close distance to other flies.',
	'dewy':    'appears moist, with its body covered in tiny droplets of water.',
	'eery':    'appears to have something off, crooked limbs and other twisted appendages.',
	'fuzzy':   'is covered in a dense layer of hairs, giving it a soft appearance.',
	'gooey':   'is coated with a thick, sticky substance, suggestive of a viscous bodily secretion.',
	'horsey':  'is quite big and strong-looking, much larger than your typical fruit fly.',
	'icy':     'has a frosted appearance, with a sheen like a layer of frost.',
	'jerky':   'moves in rapid and sudden movements, displaying an unpredictable flight pattern.',
	'kidney':  'has a body shape that is curved, similar to a kidney bean.',
	'leafy':   'has wings that resemble the shape and pattern of leaves.',
	'mushy':   'feels soft to the touch and unusually squishy, unlike the usual firmness.',
	'nerdy':   'has large, prominent eyes that stand out, much like thick-rimmed glasses.',
	'okra':    'features a long, slender body, resembling the shape of an okra pod.',
	'prickly': 'is covered with sharp bristles, giving it a spiky texture.',
	'quacky':  'emits sounds that oddly mimic the quack of a duck.',
	'rusty':   'has a reddish-brown color, much like rusted iron metal.',
	'spicy':   'has chemical defense giving a tingling sensation, similar to spicy food.',
	'tipsy':   'moves in an erratic path, suggesting a lack of coordination, as if intoxicated.',
	'ugly':    'has dull colors and uneven features different from the typical fruit fly.',
	'valley':  'shows deep grooves along its body, creating a landscape of peaks and troughs.',
	'waxy':    'has a thick protective layer that is water resistant and opague.',
	'xanthic': 'has a fluorescent bright yellow coloring.',
	'yucky':   'gives off an unpleasant odor and has a generally unappealing look.',
	'zippy':   'zooms around quickly, darting from one place to another.',
}

#====================================
#====================================
phenotype_names = list(phenotype_description_dict.keys())
random.shuffle(phenotype_names)
phenotype_dict = {}
for name in phenotype_names:
	phenotype_dict[name[0]] = name
del phenotype_names

#===========================================================
def get_gene_letters(num_genes_int: int) -> str:
	lowercase = "abcdefghijklmnpqrsuvwxyz"  # Make sure this has the letters you want
	gene_letters_set = set()
	while len(gene_letters_set) < num_genes_int:
		gene_letters_set.update(random.choice(lowercase))  # Add a randomly chosen letter

	# Sort after the set has the correct number of elements
	gene_letters_list = sorted(gene_letters_set)
	gene_letters_str = ''.join(gene_letters_list)  # Create string from sorted list
	return gene_letters_str
assert len(get_gene_letters(5)) == 5

#===========================================================
#===========================================================
def generate_genotypes(gene_letters: str) -> list:
	"""
	Generate all possible genotypes for a given string of gene letters.

	Parameters
	----------
	gene_letters : str
		A string containing gene letter identifiers.

	Returns
	-------
	list
		A list of tuples, each containing a pair representing the genotype.

	Examples
	--------
	>>> generate_genotypes('abc')
	['+++', '++c', '+b+', '+bc', 'a++', 'a+c', 'ab+', 'abc']
	"""
	genotypes = []
	num_genes = len(gene_letters)
	for i in range(2**num_genes):
		# Generate a binary representation of i, then pad it with zeros
		binary_repr = bin(i)[2:].zfill(num_genes)
		genotype = ''.join(gene_letters[j] if bit == '1' else '+' for j, bit in enumerate(binary_repr))
		genotypes.append(genotype)
	return genotypes
# Use this function to generate genotypes for 'abc'
assert len(generate_genotypes('abc')) == 8
assert len(generate_genotypes('qrst')) == 16

#===========================================================
#===========================================================
def split_number_in_two(number: int) -> tuple:
	a = 0
	b = 0
	for i in range(number):
		if random.random() < 0.5:
			a += 1
		else:
			b += 1
	return (a,b)
assert sum(split_number_in_two(100)) == 100

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
def get_phenotype_name_for_genotype(genotype: str) -> str:
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
assert get_phenotype_name_for_genotype('++++') == '<i>wildtype</i>'
assert get_phenotype_name_for_genotype('+++') == '<i>wildtype</i>'
assert get_phenotype_name_for_genotype('++') == '<i>wildtype</i>'

#===========================================================
#===========================================================

import xml.etree.ElementTree as ET

def is_valid_html(html_str: str) -> bool:
	"""
	Validates if the input HTML string is well-formed by removing entities
	and wrapping the content in a root element for XML parsing.

	Args:
	html_str (str): The HTML string to validate.

	Returns:
	bool: True if the HTML is well-formed, False otherwise.
	"""
	html_str = html_str.replace('<', '\n<')
	try:
		# Remove HTML entities by finding '&' followed by alphanumerics or '#' and a semicolon
		cleaned_html = re.sub(r'&[#a-zA-Z0-9]+;', '', html_str)
		# Wrap in a root tag for XML parsing as XML requires a single root element
		wrapped_html = f"<root>{cleaned_html}</root>"
		# Parse the cleaned and wrapped HTML with XML parser
		ET.fromstring(wrapped_html)
		return True
	except ET.ParseError as e:
		# Print the error message for debugging
		if len(html_str) > 80:
			print(f"Parse error: {e}")
		#print(html_str)
		return False


# Simple assertion test for the function: 'is_valid_html'
assert is_valid_html("<p>This is a paragraph.</p>") == True
assert is_valid_html("<p>This is a<br/>paragraph.</p>") == True
assert is_valid_html("<p>This is&nbsp;a paragraph.</p>") == True
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
def right_justify_int(num: int, length: int) -> str:
	my_str = f'{num:d}'
	while len(my_str) < length:
		my_str = ' ' + my_str
	return my_str
assert right_justify_int(7,5) == "    7"

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
