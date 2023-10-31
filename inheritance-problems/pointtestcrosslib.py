
import math
import numpy
import random
import itertools
from bs4 import BeautifulSoup

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


#=============================
#=============================
def is_valid_html_table(html_str: str) -> bool:
	"""
		Check if the given HTML string represents a valid HTML table.

		Parameters
		----------
		html_str : str
			The HTML string to check.

		Returns
		-------
		bool
			True if the string represents a valid HTML table, False otherwise.
	"""
	# Parse the HTML string using BeautifulSoup
	soup = BeautifulSoup(html_str, 'html.parser')

	# Search for the first 'table' tag
	table = soup.find('table')

	# If there is no 'table' tag, it's not a valid HTML table
	if not table:
		return False

	# Check for 'tr', 'td', and 'th' tags within the table
	rows = table.find_all('tr')
	for row in rows:
		cells = row.find_all(['td', 'th'])
		if not cells:
			return False

	# If the code reaches here, the HTML contains a well-structured table
	return True

# Simple assertion test for the function: 'is_valid_html_table'
assert is_valid_html_table('<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>') == True
assert is_valid_html_table('<p>This is not a table</p>') == False

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
def get_distance():
	#integers
	return random.randint(2,45)

#====================================
def get_progeny_size(distance):
	if debug is True: print("determine progeny size")
	gcdfinal = math.gcd(distance, 100)
	if debug is True: print("Final GCD", gcdfinal)
	progenybase = 100/gcdfinal
	minprogeny =  900/progenybase
	maxprogeny = 6000/progenybase
	progs = numpy.arange(minprogeny, maxprogeny+1, 1, dtype=numpy.float64)*progenybase
	#print(progs)
	numpy.random.shuffle(progs)
	#print(progs)
	bases = progs * distance * distance / 1e4
	#print(bases)
	devs = (bases - numpy.around(bases, 0))**2
	#print(devs)
	argmin = numpy.argmin(devs)
	progeny_size = int(progs[argmin])
	if debug is True: print(("total progeny: %d\n"%(progeny_size)))
	return progeny_size


#=============================
#=============================
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

	if is_valid_html_table(table) is False:
		sys.exit(1)
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
def make_progeny_ascii_table(typemap, progeny_size):
	alltypes = list(typemap.keys())
	alltypes.sort()
	table = ''
	for genotype in alltypes:
		phenotype_string = get_phenotype_name(genotype)
		for gene in genotype:
			table += f"{gene}\t"
		table += ("{0:d}\t".format(typemap[genotype]))
		table += ("{0}\t".format(phenotype_string))
		table += "\n"
	table +=  "\t\t\t-----\n"
	table +=  "\t\tTOTAL\t%d\n\n"%(progeny_size)
	return table

#====================================
def generate_type_counts(parental_type, basetype, progeny_size, distance, geneorder):
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


