import random

from lib_test_utils import import_from_repo_path

BASE = 'problems/inheritance-problems/gene_mapping/'


def test_four_gene_tetrads_preserve_distances_and_order():
	mod = import_from_repo_path(BASE + 'tetrad_unordered_4_gene-distances_plus.py')
	pool = mod.gml.get_four_gene_distance_pool()
	for key in random.Random(17).sample(list(pool), 20):
		rows = mod.construct_tetrads('abcd', 'cadb', '+b+d', pool[key][0])
		assert len(rows) == 16 and min(rows.values()) > 0
		assert sum(rows.values()) == 12000
		for tetrad in rows:
			assert all(sum(spore[i] == '+' for spore in tetrad) == 2 for i in range(4))
		divisor = mod.math.gcd(*rows.values())
		for scale in (1, 4):
			scaled = {tetrad: n // divisor * scale for tetrad, n in rows.items()}
			answers = mod.get_answer_mapping(scaled, 'abcd')
			assert set(answers['geneorder']) == {'cadb', 'bdac'}
			for (i, j), expected in zip(mod.PAIR_POSITIONS, key):
				pair = ''.join(sorted(('cadb'[i], 'cadb'[j]))).upper()
				assert answers[pair][0] == f'{expected / 10:.1f}'
