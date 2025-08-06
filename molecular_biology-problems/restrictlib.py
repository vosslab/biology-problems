#python library of restriction enzymes

import os
import re
import sys
import time
import yaml
import json
import random
import requests
from Bio import Restriction
from bs4 import BeautifulSoup

"""
'all_suppliers', 'buffers', 'catalyse', 'catalyze', 'charac', 'characteristic', 'compatible_end', 'compsite', 'cut_once', 'cut_twice', 'dna', 'elucidate', 'equischizomers', 'freq', 'frequency', 'fst3', 'fst5', 'inact_temp', 'is_3overhang', 'is_5overhang', 'is_ambiguous', 'is_blunt', 'is_comm', 'is_defined', 'is_equischizomer', 'is_isoschizomer', 'is_methylable', 'is_neoschizomer', 'is_palindromic', 'is_unknown', 'isoschizomers', 'mro', 'neoschizomers', 'opt_temp', 'overhang', 'ovhg', 'ovhgseq', 'results', 'scd3', 'scd5', 'search', 'site', 'size', 'substrat', 'suppl', 'supplier_list', 'suppliers'
"""

"""
Useful attributes:
. cut_once - True if the enzyme cut the sequence one time on each strand.
. cut_twice - True if the enzyme cut the sequence twice on each strand.
. elucidate - Return a representation of the site with the cut on the (+) strand
		represented as '^' and the cut on the (-) strand as '_'.
. fst5 -> first 5' cut ((current strand) or None
. fst3 -> first 3' cut (complementary strand) or None
. is_palindromic - Return if the enzyme has a palindromic recoginition site.
. is_3overhang - True if the enzyme produces 3' overhang sticky end.
. is_5overhang - True if the enzyme produces 5' overhang sticky end.
. is_blunt - True if the enzyme produces blunt end.
. is_ambiguous - True if the sequence recognised and cut is ambiguous,
		i.e. the recognition site is degenerated AND/OR the enzyme cut outside the site.
. is_defined - the recognition site is not degenerated AND the enzyme cut inside the site.
. is_unknown - True if the sequence is unknown, has not been characterised yet.
. overhang - Can be "3' overhang", "5' overhang", "blunt", "unknown".
. ovhgseq
. site -> recognition site
"""
#============================
def save_cache(cache_data):
	if len(cache_data) == 0:
		return
	print('==== SAVE CACHE ====')
	t0 = time.time()
	cache_name = 'enzyme_names_cache'
	cache_format = 'yml'
	file_name = cache_name+'.'+cache_format
	if len(cache_data) > 0:
		if cache_format == 'json':
			json.dump( cache_data, open( file_name, 'w') )
		elif cache_format == 'yml':
			yaml.dump( cache_data, open( file_name, 'w') )
		else:
			print("UNKNOWN CACHE FORMAT: ", cache_data)
			sys.exit(1)
		print('.. wrote {0} entires to {1} in {2:,d} usec'.format(
			len(cache_data), file_name, int((time.time()-t0)*1e6)))
	print('==== END SAVE CACHE ====')

#============================
def load_cache():
	cache_name = 'enzyme_names_cache'
	cache_format = 'yml'
	file_name = cache_name+'.'+cache_format
	print('==== LOAD CACHE ====')
	if os.path.isfile(file_name):
		try:
			t0 = time.time()
			if cache_format == 'json':
				cache_data = json.load( open(file_name, 'r') )
			elif cache_format == 'yml':
				cache_data =  yaml.safe_load( open(file_name, 'r') )
			else:
				print("UNKNOWN CACHE FORMAT: ", cache_data)
				sys.exit(1)
			print('.. loaded {0} entires from {1} in {2:,d} usec'.format(
				len(cache_data), file_name, int((time.time()-t0)*1e6)))
		except IOError:
			cache_data = {}
	else:
		cache_data = {}
	print('==== END LOAD CACHE ====')
	return cache_data

#============================
def get_web_data(enzyme_class):
	uri = enzyme_class.uri
	#print(f"URI: {uri}")
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'}
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(uri, headers=headers)
	#print(f"HTTP Response: {response.status_code}")
	if response.status_code != 200:
		print("Failed to fetch data")
		return {}
	time.sleep(random.random())

	soup = BeautifulSoup(response.content, 'html.parser')

	# Create a dictionary to store the data
	enzyme_data = {'uri': uri,}
	# Iterate through each <b> tag that has the field name
	for field in soup.find_all('b'):
		field_name = field.text.replace(":", "").strip()
		next_tag = field.find_next()
		if next_tag and next_tag.name == 'a':
			field_value = next_tag.text
		elif next_tag and next_tag.name == 'font':
			continue  # Skip, as this doesn't seem to hold data of interest
		else:
			next_sibling = field.find_next_sibling(text=True)
			field_value = next_sibling.strip() if next_sibling else ""

		# Only add the field if it has a name and value
		if field_name and field_value and field_name.startswith("Organism"):
			enzyme_data[field_name] = field_value.strip()

	#print(f"Enzyme data: {enzyme_data}")
	return enzyme_data


#========================================
def check_for_good_ending(item: str) -> bool:
	"""
	Check if the given string ends with a good suffix.

	Good suffixes include Roman numerals or mutation markers like '_mut1' or '_3'.
	"""
	if item.endswith("I"):
		return True
	if item.endswith("V"):
		return True
	if item.endswith("X"):
		return True
	# Match strings ending in _mut followed by a single digit (e.g., '_mut3')
	if re.search(r"_mut[0-9]$", item):
		return True
	# Match strings ending in underscore + digit (e.g., '_1')
	if re.search(r"_[0-9]$", item):
		return True
	return False


#========================================
def has_strict_sequence(enzyme_class) -> bool:
	"""
	Check if the enzyme has a strict recognition site and elucidation pattern.

	Returns:
		bool: True if both site and elucidate() match strict ACGT rules.
	"""
	# Match sequences that only contain A, C, G, or T (strict DNA bases)
	if not re.search(r'^[ACGT]+$', enzyme_class.site):
		return False

	# Elucidated cut site must also contain only ACGT and optional underscore or caret
	if not re.search(r'^[ACGT_\^]+$', enzyme_class.elucidate()):
		return False

	return True

#========================================
def get_enzyme_list() -> list:
	"""
	Build a filtered list of enzymes that are:
	- Properly named (starts with [A-Z][a-z][a-z])
	- Palindromic
	- Cut once
	- Non-ambiguous
	- Known
	- Have a strict recognition sequence

	Returns:
		list: List of valid enzyme names
	"""
	dir_result = dir(Restriction)
	enzymes = []

	for item in dir_result:
		# Match enzyme names like 'Eco', 'Bam', etc.
		if not re.match(r"^[A-Z][a-z][a-z]", item):
			continue

		enzyme_class = enzyme_name_to_class(item)

		if not hasattr(enzyme_class, 'site'):
			continue

		if enzyme_class.is_palindromic() is False:
			continue

		if enzyme_class.cut_once() is False:
			continue

		if enzyme_class.is_ambiguous() is True:
			continue

		if enzyme_class.is_unknown() is True:
			continue

		if enzyme_class.fst3 == 0:
			continue

		if has_strict_sequence(enzyme_class) is False:
			continue

		enzymes.append(item)

	#print("Found {0:d} enzymes".format(len(enzymes)))
	for enzyme in enzymes:
		#print(enzyme)
		pass
	return enzymes

#========================================
def enzyme_name_to_class(enzyme_name):
	enzyme_class = getattr(Restriction, enzyme_name)
	return enzyme_class

#========================================
def random_enzyme(enzymes=None):
	if enzymes is None:
		enzymes = get_enzyme_list()
	enzyme_name = random.choice(enzymes)
	enzyme_class = enzyme_name_to_class(enzyme_name)
	return enzyme_class

#========================================
def random_enzyme_one_end(enzymes=None, badletter="."):
	if enzymes is None:
		enzymes = get_enzyme_list()
	enzyme_name = "x"
	while (len(enzyme_name) != 4
			or not enzyme_name.endswith("I")
			or enzyme_name.startswith(badletter)):
		enzyme_name = random.choice(enzymes)
	enzyme_class = enzyme_name_to_class(enzyme_name)
	return enzyme_class

#========================================
def random_enzyme_with_overhang(enzymes=None):
	if enzymes is None:
		enzymes = get_enzyme_list()
	has_overhang = False
	while has_overhang is False:
		enzyme_name = random.choice(enzymes)
		enzyme_class = enzyme_name_to_class(enzyme_name)
		overhang = enzyme_class.overhang()
		has_overhang = overhang.endswith('overhang')
	return enzyme_class

#========================================
def format_enzyme(enzyme_class):
	elucidate_str = enzyme_class.elucidate()
	elucidate_str = elucidate_str.replace("^", "|")
	elucidate_str = elucidate_str.replace("_", "")
	final_str = "5'-{0}-3'".format(elucidate_str)
	return final_str

#========================================
def html_monospace(txt):
	return f"<code>{txt}</code>"
	#return f"<span style='font-family: 'andale mono', 'courier new', courier, monospace;'>{txt}</span>"

#========================================
#========================================
if __name__ == '__main__':
	enzymes = get_enzyme_list()
	print("Found {0:d} enzymes".format(len(enzymes)))
	enzyme_class = random_enzyme_with_overhang(enzymes)
	print(enzyme_class.__name__)
	print(enzyme_class.site)
	print(format_enzyme(enzyme_class))

