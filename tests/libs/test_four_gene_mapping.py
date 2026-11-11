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
