
import random
import string

import lxml.etree

from lib_test_utils import import_from_repo_path


def test_fly_gene_descriptions_use_question_colors_for_all_phenotypes():
	gml = import_from_repo_path('problems/inheritance-problems/gene_mapping/genemaplib.py')
	flies = import_from_repo_path('problems/inheritance-problems/gene_mapping/phenotypes_for_flies.py')
	colors = ['003FFF', '007A00', 'A719DB']
	for gene in string.ascii_lowercase:
		portraits = []
		for color in colors:
			markup = gml.get_phenotype_info(gene, flies.phenotype_dict, [color])
			assert '<metadata>' not in markup
			assert 'creativecommons.org' not in markup
			document = lxml.etree.fromstring(('<root>' + markup + '</root>').encode())
			portrait, = document.xpath('//*[@data-phenotype]')
			assert portrait.get('data-phenotype') == flies.phenotype_dict[gene]
			assert portrait.get('data-gene-color') == '#' + color
			assert flies.phenotype_dict[flies.phenotype_dict[gene]] in ''.join(document.itertext())
			portraits.append(portrait)
		heads = [node.xpath('.//*[@data-part="face"]')[0][0].get('fill') for node in portraits]
		assert len(set(heads)) == 1
		wings = [lxml.etree.tostring(node.xpath('.//*[@data-part="wings"]')[0]) for node in portraits]
		assert len(set(wings)) == 3


def test_genemaplib_small_pure_helpers():
	genemaplib = import_from_repo_path("problems/inheritance-problems/gene_mapping/genemaplib.py")
	assert genemaplib.is_almost_integer(5.0000001) is True
	assert genemaplib.is_almost_integer(5.001) is False

	random.seed(0)
	a, b = genemaplib.split_number_in_two(100, 0.5)
	assert a + b == 100
	assert 0 <= a <= 100
	assert 0 <= b <= 100

	assert genemaplib.invert_genotype("+b+d", "abcd") == "a+c+"
	assert genemaplib.flip_gene_by_letter("+b+d", "b", "abcd") == "+++d"
	assert genemaplib.flip_gene_by_index("+b+d", 2, "abcd") == "+++d"
	assert genemaplib.crossover_after_index("++++", 2, "adcb") == "+bc+"


def test_two_point_choices_avoid_distance_giveaway():
	import re
	gmc = import_from_repo_path("problems/inheritance-problems/gene_mapping/gene_map_class_lib.py")
	mapping = gmc.GeneMappingClass.__new__(gmc.GeneMappingClass)
	mapping.num_genes_int = 2
	mapping.gene_letters_str = "dx"
	mapping.gene_order_str = "dx"
	mapping.parental_genotypes_tuple = ("dx", "++")
	mapping.progeny_count_int = 28000
	for counts in [(12290, 12322, 1666, 1722), (12290, 12322, 1694, 1694)]:
		mapping.genotype_counts = dict(zip(("dx", "++", "d+", "+x"), counts))
		for count in (4, 6, 10):
			choices, answer = mapping.make_choices(num_choices=count)
			values = [float(re.search(r"([0-9.]+) cM", choice)[1]) for choice in choices]
			assert choices.count(answer) == 1
			assert "12.10 cM" in answer
			assert values == sorted(set(values))
			assert min(values) < 12.10 < max(values)
			assert 2 * sum(v >= 49 for v in values) <= len(values) - 1
			if count <= 6:
				assert len(choices) == count


def test_three_point_distractors_prefer_single_genotype_swaps():
	gmc = import_from_repo_path('problems/inheritance-problems/gene_mapping/gene_map_class_lib.py')
	mapping = gmc.GeneMappingClass.__new__(gmc.GeneMappingClass)
	mapping.genotype_counts = dict(zip('abcdefgh', (1, 2, 4, 8, 16, 32, 64, 128)))
	mapping.progeny_count_int = 1000
	preferred = set('abcd')
	used = {tuple(sorted(preferred))}
	choices = mapping.add_combinations(4, used, 3, preferred)
	assert len(choices) == 3
	assert all(len(set(combo) & preferred) == 3 for combo in used if set(combo) != preferred)
