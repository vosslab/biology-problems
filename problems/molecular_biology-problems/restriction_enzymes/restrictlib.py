#python library of restriction enzymes

import os
import re
import time
import datetime
import yaml
import random
import requests
from Bio import Restriction
from bs4 import BeautifulSoup

import bptools


WEB_DATA_CACHE_PATH = bptools.get_repo_data_path('restriction_enzyme_web_data.yml')
WEB_DATA_CACHE_MAX_AGE = datetime.timedelta(days=183)
WEB_DATA_REQUEST_TIMEOUT = 20
WEB_DATA_CACHE = None

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
def _new_web_data_cache() -> dict:
	cache_data = {
		'schema_version': 1,
		'max_age_days': WEB_DATA_CACHE_MAX_AGE.days,
		'enzymes': {},
	}
	return cache_data


#============================
def load_web_data_cache() -> dict:
	global WEB_DATA_CACHE
	if WEB_DATA_CACHE is not None:
		return WEB_DATA_CACHE
	if os.path.isfile(WEB_DATA_CACHE_PATH):
		with open(WEB_DATA_CACHE_PATH, 'r', encoding='utf-8') as cache_file:
			WEB_DATA_CACHE = yaml.safe_load(cache_file)
	else:
		WEB_DATA_CACHE = _new_web_data_cache()
	return WEB_DATA_CACHE


#============================
def save_web_data_cache() -> None:
	cache_data = load_web_data_cache()
	with open(WEB_DATA_CACHE_PATH, 'w', encoding='utf-8') as cache_file:
		yaml.safe_dump(cache_data, cache_file, sort_keys=True, allow_unicode=False)


#============================
def _utc_now() -> datetime.datetime:
	now = datetime.datetime.now(datetime.timezone.utc)
	return now


#============================
def _cache_entry_is_fresh(cache_entry: dict) -> bool:
	fetched_at = datetime.datetime.fromisoformat(cache_entry['fetched_at'])
	age = _utc_now() - fetched_at
	is_fresh = age <= WEB_DATA_CACHE_MAX_AGE
	return is_fresh


#============================
def _field_value(field) -> str:
	value_parts = []
	for sibling in field.next_siblings:
		if getattr(sibling, 'name', None) == 'br':
			break
		if hasattr(sibling, 'get_text'):
			value_parts.append(sibling.get_text(' ', strip=True))
		else:
			value_parts.append(str(sibling).strip())
	value = ' '.join(part for part in value_parts if len(part) > 0)
	return value.strip()


#============================
def _parse_web_data(response_content: bytes, uri: str) -> dict:
	soup = BeautifulSoup(response_content, 'html.parser')
	enzyme_data = {'uri': uri}
	for field in soup.find_all('b'):
		field_name = field.get_text(' ', strip=True).rstrip(':').strip()
		if not field.get_text(' ', strip=True).endswith(':'):
			continue
		field_value = _field_value(field)
		if len(field_name) > 0 and len(field_value) > 0:
			enzyme_data[field_name] = field_value
	return enzyme_data


#============================
def fetch_web_data(enzyme_class) -> dict:
	uri = enzyme_class.uri
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(uri, headers=headers, timeout=WEB_DATA_REQUEST_TIMEOUT)
	response.raise_for_status()
	time.sleep(random.random())
	enzyme_data = _parse_web_data(response.content, uri)
	return enzyme_data


#============================
def get_web_data(enzyme_class, force_refresh: bool=False, save: bool=True) -> dict:
	cache_data = load_web_data_cache()
	enzyme_name = enzyme_class.__name__
	cache_entry = cache_data['enzymes'].get(enzyme_name)
	if not force_refresh and cache_entry is not None and _cache_entry_is_fresh(cache_entry):
		return cache_entry['data']

	enzyme_data = fetch_web_data(enzyme_class)
	cache_data['enzymes'][enzyme_name] = {
		'fetched_at': _utc_now().isoformat(timespec='seconds'),
		'data': enzyme_data,
	}
	if save:
		save_web_data_cache()
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
def get_enzyme_list(include_blunt=True) -> list:
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

		if include_blunt is False and not enzyme_class.overhang().endswith('overhang'):
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
