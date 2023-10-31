
import random
import itertools

debug = False

#====================================
phenotype_dict = {
	'a': 'amber',
	'b': 'bald',
	'c': 'conehead',
	'd': 'dumpy',
	'e': 'eyeless',
	'f': 'forked',
	'g': 'garnet',
	'h': 'hook',
	'i': 'indy',
	'j': 'jagged',
	'k': 'kidney',
	'l': 'lyra',
	'm': 'marula',
	'n': 'notch',
	'o': 'okra',
	'p': 'prickly',
	'q': 'quick',
	'r': 'rosy',
	's': 'scute',
	't': 'taxi',
	'u': 'upturned',
	'v': 'vestigial',
	'w': 'white',
	'x': 'xray',
	'y': 'yellow',
	'z': 'zipper',
}

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
