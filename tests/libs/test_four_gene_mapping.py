import itertools
import random

import pytest

from lib_test_utils import import_from_repo_path

BASE = 'problems/inheritance-problems/gene_mapping/'


def test_four_gene_pool_keys_recover_from_offspring():
	gmc = import_from_repo_path(BASE + 'gene_map_class_lib.py')
	gml = gmc.gml
	solver = import_from_repo_path(BASE + 'gene_map_solver_lib.py')
	pairs = ((1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (1, 4))
	for key, vectors in gml.get_four_gene_distance_pool().items():
		for counts in vectors:
			rows = {}
			for mask, n in zip(gml.FOUR_GENE_MASKS, counts):
				bits = [0]
				for bit in mask:
					bits.append(bits[-1] ^ int(bit))
				genotype = ''.join(g if b else '+' for g, b in zip('abcd', bits))
				rows[genotype] = n // 2
				rows[gml.invert_genotype(genotype, 'abcd')] = n - n // 2
			assert len(rows) == 16 and min(rows.values()) > 0
			assert sum(rows.values()) == 2000
			observed = {}
			for i, j in pairs:
				numerator = sum(n for genotype, n in rows.items()
					if (genotype[i-1] == '+') != (genotype[j-1] == '+'))
				assert numerator % 2 == 0
				observed[('abcd'[i-1], 'abcd'[j-1])] = numerator // 2
			assert tuple(observed.values()) == key
			assert solver.get_gene_order(observed) in ('abcd', 'dcba')


def test_four_gene_questions_have_correct_blanks_tables_and_keys():
	mod = import_from_repo_path(BASE + 'four_point_test-cross_gene_map-distances_plus.py')
	for seed in range(12):
		random.seed(seed)
		mapping = mod.gmc.GeneMappingClass(4)
		mapping.setup_question()
		distances, _, order = mod.solver.gene_map_solver(mapping.genotype_counts)
		assert order in (mapping.gene_order_str, mapping.gene_order_str[::-1])
		assert sorted(round(d, 1) for d in distances) == sorted(mapping.distances_dict.values())
		assert len(mapping.genotype_counts) == 16
		assert sum(mapping.genotype_counts.values()) == mapping.progeny_count_int
		html = mapping.get_progeny_html_table()
		assert html.count('Progeny<br/>Count') == 2
		assert html.count('Combined total progeny:') == 1
		answers = mod.get_answer_mapping(mapping)
		for i, j in itertools.combinations(range(1, 5), 2):
			pair = ''.join(sorted((mapping.gene_order_str[i-1], mapping.gene_order_str[j-1]))).upper()
			assert answers[pair][0] == f'{mapping.distances_dict[(i, j)]:.1f}'
		assert mapping.gene_order_str[::-1].upper() in answers['geneorder']
	with pytest.raises(ValueError, match='unique order'):
		mod.solver.get_gene_order({pair: 10 for pair in itertools.combinations('abcd', 2)})
