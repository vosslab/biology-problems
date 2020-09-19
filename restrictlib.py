#python library of restriction enzymes

import re
import random
from Bio import Restriction

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

#========================================
def check_for_good_ending(item):
	#not used / not useful
	if item.endswith("I"):
		return True
	if item.endswith("V"):
		return True
	if item.endswith("X"):
		return True
	if re.search("_mut[0-9]$", item):
		return True
	if re.search("_[0-9]$", item):
		return True
	return False

#========================================
def has_strict_sequence(enzyme_class):
	m = re.search('^[ACGT]+$', enzyme_class.site)
	if not m:
		return False
	return True
	# not needed use enzyme_class.fst3 == 0:
	if enzyme_class.fst3 == 0:
		return False
	m = re.search('^[ACGT_\^]+$', enzyme_class.elucidate())
	if not m:
		return False
	return True

#========================================
def get_enzyme_list():
	dir_result = dir(Restriction)
	enzymes = []
	for item in dir_result:
		if not re.match("^[A-Z][a-z][a-z]", item):
			#print(item)
			continue
		enzyme_class = enzyme_name_to_class(item)
		if not hasattr(enzyme_class, 'site'):
			#print(item)
			continue
		if enzyme_class.is_palindromic() is False:
			#print("{0} - {1}".format(item, enzyme_class.site))
			continue
		if enzyme_class.cut_once() is False:
			#print("{0} - {1}".format(item, enzyme_class.elucidate()))
			continue
		if enzyme_class.is_ambiguous() is True:
			#print("{0} - {1}".format(item, enzyme_class.elucidate()))
			continue
		if enzyme_class.is_unknown() is True:
			#print("{0} - {1}".format(item, enzyme_class.elucidate()))
			continue
		if enzyme_class.fst3 == 0:
			#print("{0} - {1}".format(item, enzyme_class.elucidate()))
			continue
		if has_strict_sequence(enzyme_class) is False:
			#print("{0} - {1}".format(item, enzyme_class.site))
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
	return "<span style='font-family: 'andale mono', 'courier new', courier, monospace;'>{0}</span>".format(txt)

#========================================
#========================================
if __name__ == '__main__':
	enzymes = get_enzyme_list()
	print("Found {0:d} enzymes".format(len(enzymes)))
	enzyme_class = random_enzyme_with_overhang(enzymes)
	print(enzyme_class.__name__)
	print(enzyme_class.site)
	print(format_enzyme(enzyme_class))

