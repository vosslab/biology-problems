
import re
import sys
import copy
import math
import random

import bptools

debug = False

#===========================================================
# Function to generate a unique set of gene letters
#===========================================================

def get_gene_letters(num_genes_int: int) -> str:
	"""
	Generates a unique string of lowercase letters representing gene symbols.

	Args:
		num_genes_int (int): The number of unique gene letters to generate.

	Returns:
		str: A string containing `num_genes_int` unique, sorted letters chosen randomly.
	"""

	# Define the set of lowercase letters to choose from.
	# This set excludes certain letters (like 'o' and 't') which might have specific reasons for exclusion.
	lowercase = "abcdefghijklmnpqrsuvwxyz"

	# Initialize an empty set to store unique gene letters.
	gene_letters_set = set()

	# Continuously add random letters to the set until it contains `num_genes_int` unique letters.
	while len(gene_letters_set) < num_genes_int:
		# Randomly select a letter from `lowercase` and add it to `gene_letters_set`.
		# Since sets do not allow duplicates, any repeated letter will be ignored.
		gene_letters_set.update(random.choice(lowercase))

	# Convert the set of letters to a sorted list.
	gene_letters_list = sorted(gene_letters_set)

	# Join the sorted list of letters into a single string.
	gene_letters_str = ''.join(gene_letters_list)

	# Return the resulting string of unique, sorted gene letters.
	return gene_letters_str

# Test the function with an assertion to ensure it generates the correct number of letters.
# This checks that the length of the result is equal to the requested number of genes.
assert len(get_gene_letters(5)) == 5

#===========================================================
#===========================================================
def get_phenotype_info(gene_letters_str, phenotype_dict, dark_colors=None) -> str:
	organism = phenotype_dict['common name']
	phenotype_info_text = ''
	phenotype_info_text += '<h6>Characteristics of Recessive Phenotypes</h6>'

	linking_words = ('linked with', 'associated with', 'related to',
		'connected with', 'analogous to', 'affiliated with', 'correlated with',)
	phenotype_info_text += '<p><ul>'
	if dark_colors is None:
		num_genes_int = len(gene_letters_str)
		light_colors, dark_colors = bptools.light_and_dark_color_wheel(num_genes_int)
	for i, gene_letter in enumerate(gene_letters_str):
		# Fetch the phenotype string based on the genotype
		phenotype_name = phenotype_dict[gene_letter]
		phenotype_description = phenotype_dict[phenotype_name]
		gene_span = f'<span style="color: #{dark_colors[i]};">'
		phenotype_info_text += f"<li><strong>{gene_span}Gene {gene_letter.upper()}</span></strong> is "
		phenotype_info_text += f'{random.choice(linking_words)} '
		phenotype_info_text += f"the '{gene_span}<i>{phenotype_name}</i></span>' phenotype. "
		phenotype_info_text += f'A {organism} that is homozygous recessive for {gene_span}Gene {gene_letter.upper()}</span> '
		phenotype_info_text += f'{phenotype_description}</li> '
	phenotype_info_text += '</ul></p>'
	if is_valid_html(phenotype_info_text) is False:
		print(phenotype_info_text)
		raise ValueError
	return phenotype_info_text

#===========================================================
#===========================================================
def get_random_gene_order(gene_letters_str: str) -> str:
	"""
	Sets the order of genes within the map by randomly shuffling `gene_letters_str`.

	The order is minimized lexicographically, ensuring consistency in order representation.
	"""
	# Convert the gene letters into a list and shuffle them
	gene_order_list = list(gene_letters_str)
	random.shuffle(gene_order_list)

	# Set gene order to the lexicographically smaller of the shuffled order and its reverse
	gene_order_list = min(gene_order_list, gene_order_list[::-1])

	# Join the list back into a string and assign to `gene_order_str`
	gene_order_str = ''.join(gene_order_list)

	if debug is True: print(f"gene_order_str = {gene_order_str}")
	return gene_order_str
assert ''.join(sorted(get_random_gene_order('abcdefg'))) == 'abcdefg'
assert get_random_gene_order('ab') in ('ab', 'ba')


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
def split_number_in_two(number: int, probability: float = 0.5) -> tuple:
	"""
	Splits a given integer `number` randomly into two parts (a, b) such that a + b = number.

	This function uses a binomial distribution to approximate a random split based on the given probability.
	- If Python 3.12 or newer is available, it uses `random.binomialvariate` for a direct binomial distribution.
	- For older versions of Python, it falls back to a loop-based approximation.

	Args:
		number (int): The integer to split. Must be a non-negative integer.
		probability (float): The probability of "success" for each trial. Defaults to 0.5 (50%).

	Returns:
		tuple: A tuple (a, b) where a and b are non-negative integers that sum up to `number`.

	Example:
		>>> split_number_in_two(10, 0.5)
		(5, 5) or another random split such as (6, 4).
	"""

	# Input validation: ensure `number` is non-negative
	if number < 2:
		raise ValueError("`number` must be a non-negative integer greater than 2.")

	# Check if Python version is 3.12 or newer
	if sys.version_info >= (3, 12):
		# Use `random.binomialvariate` for a direct binomial distribution.
		# `a` is the count of "successes" out of `number` trials with a given `probability`
		a = random.binomialvariate(number, probability)
	else:
		# Fallback for Python versions older than 3.12 that do not have `random.binomialvariate`.
		# Manually simulate a binomial distribution by iterating `number` times and counting "successes"
		a = 0  # Initialize the count for the first part of the split
		# Loop `number` times, simulating `number` coin flips
		for _ in range(number):
			if random.random() < probability:
				a += 1

	# Calculate `b` as the remainder of the split
	b = number - a

	# Return the two parts as a tuple (a, b). Note that a + b should equal the original `number`.
	return (a, b)

# Test to ensure the function's output always sums to the input `number`.
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
	# Use math.isclose to check if num is close to the nearest integer within epsilon
	return math.isclose(num, round(num), abs_tol=epsilon)
# Simple assertion tests for the function: 'is_almost_integer'
assert is_almost_integer(5.0000001)  == True
assert is_almost_integer(5.001)      == False

#===========================================================
#===========================================================
def get_phenotype_name_for_genotype(genotype: str, phenotype_dict: dict) -> str:
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
assert get_phenotype_name_for_genotype('++++', None) == '<i>wildtype</i>'
assert get_phenotype_name_for_genotype('+++', None) == '<i>wildtype</i>'
assert get_phenotype_name_for_genotype('++', None) == '<i>wildtype</i>'

#===========================================================
#===========================================================

import xml.etree.ElementTree as ET

def is_valid_html(html_str: str, debug: bool=True) -> bool:
	"""
	Validates if the input HTML string is well-formed by removing entities
	and wrapping the content in a root element for XML parsing.

	Args:
		html_str (str): The HTML string to validate.

	Returns:
		bool: True if the HTML is well-formed, False otherwise.
	"""
	if '\n' in html_str:
		raise ValueError("Blackboard upload does not support newlines in the HTML code.")
	html_str = html_str.replace('<', '\n<')  # Optional: format the input HTML string for better readability on error
	try:
		# Remove HTML entities by finding '&' followed by alphanumerics or '#' and a semicolon
		cleaned_html = re.sub(r'&[#a-zA-Z0-9]+;', '', html_str)
		# Wrap in a root tag for XML parsing as XML requires a single root element
		wrapped_html = f"<root>{cleaned_html}</root>"
		# Parse the cleaned and wrapped HTML with XML parser
		ET.fromstring(wrapped_html)
		return True
	except ET.ParseError as e:
		# Print detailed error information for debugging
		if debug: print(f"Parse error: {e}")

		# Optional: Print a snippet of the HTML around the error
		error_index = e.position[1] if hasattr(e, 'position') else 0
		snippet = cleaned_html[max(0, error_index - 40): error_index + 40]
		if debug: print(f"Snippet around error (40 chars before and after):\n{snippet}")

		# Optional: Print the entire cleaned HTML if debugging further
		if debug: print("Full cleaned HTML (wrapped in root):")
		if debug: print(wrapped_html)

		return False

# Simple assertion test for the function: 'is_valid_html'
assert is_valid_html("<p>This is a paragraph.</p>") == True
assert is_valid_html("<p>This is a<br/>paragraph.</p>") == True
assert is_valid_html("<p>This is&nbsp;a paragraph.</p>") == True
assert is_valid_html("<p>This is a paragraph.</html>", debug=False) == False
assert is_valid_html("<span style='no closing quote>This is a paragraph.</span>", debug=False) == False

#===========================================================
#===========================================================
def format_fraction(numerator: str, denominator: str) -> str:
	"""
	Formats the given numerator and denominator as a fraction displayed in a two-cell HTML table.

	Args:
		numerator (str): The numerator to display in the top cell.
		denominator (str): The denominator to display in the bottom cell.

	Returns:
		str: HTML string representing the fraction in a table format.
	"""
	# Construct the fraction as a two-row HTML table
	html_table = (
		f'<table style="border-collapse: collapse; display: inline-table; vertical-align: middle;">'
		f'  <tr><td style="border-bottom: 1px solid black; text-align: center;">{numerator}</td></tr>'
		f'  <tr><td style="text-align: center;">{denominator}</td></tr>'
		f'</table>'
	)

	# Optional: Validate the HTML format and raise an error if invalid
	if is_valid_html(html_table) is False:
		print(html_table)
		raise ValueError("Generated HTML is not well-formed.")

	return html_table

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


#===========================================================
def minN_INTERFERENCE(x: int, y: int, a: int, b: int) -> int:
	"""
	Calculates the minimum value of N needed for certain genetic interference calculations.

	Args:
		x (int): First distance or parameter in the interference calculation.
		y (int): Second distance or parameter in the interference calculation.
		a (int): Numerator of interference ratio.
		b (int): Denominator of interference ratio.

	Returns:
		int: The minimum value of N, scaled by the greatest common divisor of the given terms.
	"""
	# Calculate the greatest common divisor (GCD) of multiple terms involving x, y, a, and b.
	# This GCD represents the greatest common factor in the interference calculations.
	final_gcd = math.gcd(b * x * y, 100 * b * x, 100 * b * y, x * y * (b - a), 10000 * b)

	# Divide 10000 * b by the calculated GCD to get the minimum interference value N.
	N = 10000 * b // final_gcd
	return N

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
def get_all_distance_triplets(max_fraction_int: int=12, max_distance: int=40, msg: bool=True) -> list:
	"""
	Generates a list of unique distance triplets based on interference fractions and maximum distance.

	Args:
		max_fraction_int (int): The maximum integer for the fraction's numerator and denominator.
		max_distance (int): The maximum allowable distance in each distance triplet.
		msg (bool): If True, prints a message about the number of distance triplets found.

	Returns:
		list: A list of valid distance triplets generated by `distance_triplet_generator`.
	"""
	# Dictionary to keep track of used numerator/denominator pairs to avoid duplicates.
	used_values = {}

	# List to store all generated distance triplets.
	distance_triplet_list = []

	# Iterate over possible values for the numerator and denominator within max_fraction_int.
	for numerator_prime in range(1, max_fraction_int):
		for denominator_prime in range(numerator_prime + 1, max_fraction_int + 1):
			# Calculate the GCD to reduce the fraction (numerator_prime/denominator_prime) to its simplest form.
			gcd_prime = math.gcd(numerator_prime, denominator_prime)
			numerator = numerator_prime // gcd_prime
			denominator = denominator_prime // gcd_prime

			# Check if the fraction (numerator, denominator) has been used already.
			if used_values.get((numerator, denominator)) is None:
				# Mark this fraction as used.
				used_values[(numerator, denominator)] = True

				# Generate distance triplets for the current fraction.
				new_distance_triplet_list = distance_triplet_generator((numerator, denominator), max_distance)

				# If valid triplets were generated, add them to the main list.
				if new_distance_triplet_list is not None:
					distance_triplet_list += new_distance_triplet_list

	# If msg is True, print the number of distance triplets found and other parameters.
	if msg is True:
		print(f'found {len(distance_triplet_list)} distance tuples '+
			f'with max distance {max_distance} '+
			f'from all interference fractions up to denominator {max_fraction_int}')

	# Return the complete list of distance triplets.
	return distance_triplet_list

# ==============================
def distance_triplet_generator_INTERFERENCE(interference_tuple: tuple=(0,1), max_dist: int=40) -> list:
	"""
	Generates a list of distance triplets based on interference conditions.

	Args:
		interference_tuple (tuple): A tuple representing the interference fraction (a, b).
		max_dist (int): The maximum allowable distance for each distance in the triplet.

	Returns:
		list: A list of valid distance triplets that meet the interference conditions.
	"""
	# Initialize an empty list to store valid distance triplets.
	distance_triplet_list = []

	# Iterate over possible values of x (the first distance in the triplet).
	for x in range(1, max_dist):
		# Iterate over possible values of y (the second distance), starting from x to avoid duplicates.
		for y in range(x, max_dist):
			# Calculate the minimum N value for interference based on x, y, and interference_tuple (a, b).
			(a, b) = interference_tuple
			N = minN_INTERFERENCE(x, y, a, b)

			# Only proceed if N is less than 10000 (a predefined threshold).
			if N < 10000:
				# Calculate the expected double crossover occurrence.
				expected_dco = N * x * y / 10000

				# Skip to the next iteration if expected_dco is not an integer (or close to one).
				if not is_almost_integer(expected_dco):
					continue

				# Calculate the third distance z using the provided interference parameters.
				z = calculate_third_distance(x, y, interference_tuple)

				# Validate z: it should be almost an integer, within range, and meet minimum difference criteria.
				if y < z < max_dist and is_almost_integer(z):
					distance_tuple = (y, x, int(z))
					if min_difference(distance_tuple) > 1:
						# Add the valid triplet to the list.
						distance_triplet_list.append(distance_tuple)

	# Sort the list of distance triplets in ascending order before returning.
	distance_triplet_list.sort()
	return distance_triplet_list

#====================================
#====================================
def get_all_distance_triplets_INTERFERENCE(max_fraction_int: int=99, max_distance: int=40, msg: bool=True) -> list:
	"""
	Generates a list of unique distance triplets based on interference fractions,
	with a fixed denominator of 100 for each fraction.

	Args:
		max_fraction_int (int): The maximum integer for the numerator of the fraction.
		max_distance (int): The maximum allowable distance in each distance triplet.
		msg (bool): If True, prints a message about the number of distance triplets found.

	Returns:
		list: A list of valid distance triplets generated by `distance_triplet_generator`.
	"""
	# Dictionary to keep track of used numerator/denominator pairs to avoid duplicates.
	used_values = {}

	# List to store all generated distance triplets.
	distance_triplet_list = []

	# Iterate over possible values for the numerator within the range specified by `max_fraction_int`.
	for numerator_prime in range(1, max_fraction_int):
		# Fixed denominator of 100 for all fractions in this function.
		denominator_prime = 100

		# Calculate the GCD to reduce the fraction (numerator_prime/denominator_prime) to its simplest form.
		gcd_prime = math.gcd(numerator_prime, denominator_prime)
		numerator = numerator_prime // gcd_prime
		denominator = denominator_prime // gcd_prime

		# Check if the fraction (numerator, denominator) has been used already.
		if used_values.get((numerator, denominator)) is None:
			# Mark this fraction as used.
			used_values[(numerator, denominator)] = True

			# Generate distance triplets for the current fraction.
			new_distance_triplet_list = distance_triplet_generator((numerator, denominator), max_distance)

			# If valid triplets were generated, add them to the main list.
			if new_distance_triplet_list is not None:
				distance_triplet_list += new_distance_triplet_list

	# If `msg` is True, print the number of distance triplets found and other parameters.
	if msg is True:
		print(f'found {len(distance_triplet_list)} distance tuples ' +
		      f'with max distance {max_distance} ' +
		      f'from all interference fractions up to numerator {max_fraction_int}')

	# Return the complete list of distance triplets.
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
def get_progeny_size(distance: int) -> int:
	"""
	Calculates the progeny size based on a single distance value.

	Args:
		distance (int): The genetic distance for which to calculate progeny size.

	Returns:
		int: The calculated progeny size.
	"""
	# Calls an external function `get_general_progeny_size` with a list containing `distance`.
	# Returns the progeny size based on the distance.
	return get_general_progeny_size([distance, ])

# Assertion to verify that progeny size is a multiple of 200 for a given distance.
assert get_progeny_size(7) % 200 == 0
assert get_progeny_size(11) % 200 == 0
assert get_progeny_size(13) % 200 == 0

#====================================
def right_justify_int(num: int, length: int) -> str:
	"""
	Right-justifies an integer within a string of specified length by padding with spaces.

	Args:
		num (int): The integer to right-justify.
		length (int): The total length of the resulting string, including padding.

	Returns:
		str: A string representation of `num`, right-justified within the specified `length`.
	"""
	# Convert the integer `num` to a string.
	my_str = f'{num:,d}'

	# Add spaces to the left of `my_str` until it reaches the desired `length`.
	while len(my_str) < length:
		my_str = ' ' + my_str  # Prepend a space to right-align the integer.

	# Return the right-justified string.
	return my_str

# Test to ensure that the function correctly pads the integer to the specified length.
# For example, right_justify_int(7,5) should return "    7" (with four leading spaces).
assert right_justify_int(7, 5) == "    7"
assert right_justify_int(1007, 6) == " 1,007"


#====================================
#====================================
def invert_genotype(genotype: str, gene_letters: str) -> str:
	"""
	Inverts the type of a genotype based on a given gene_letters.

	Parameters
	----------
	genotype : str
		The original genotype.
	gene_letters : str
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
			newtype += gene_letters[i]
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
def flip_gene_by_letter(genotype: str, gene_letter: str, gene_letters: str) -> str:
	"""
	Flips a specified gene in the genotype.

	Parameters
	----------
	genotype : str
		The original genotype.
	gene : str
		The gene to flip.
	gene_letters : str
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
		if gene_letters[i] == gene_letter:
			if genotype[i] == '+':
				newlist[i] = gene_letters[i]
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
def flip_gene_by_index(genotype: str, gene_index: int, gene_letters: str) -> str:
	"""
	Flips a specified gene in the genotype.

	Parameters
	----------
	genotype : str
		The original genotype.
	gene_index : int
		The gene number to flip. starts at 1.
	gene_letters : str
		The basic type used as a reference for flipping the gene.

	Returns
	-------
	str
		The new genotype after the gene has been flipped.
	"""
	# Convert genotype string to a list for easier manipulation
	newlist = list(genotype)
	gene_letter = gene_letters[gene_index-1]
	# Iterate through the genotype to find and flip the specified gene
	for i in range(len(genotype)):
		if gene_letters[i] == gene_letter:
			if genotype[i] == '+':
				newlist[i] = gene_letters[i]
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

if __name__ == "__main__":
	print("DONE")

