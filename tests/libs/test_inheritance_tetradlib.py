
from lib_test_utils import import_from_repo_path

import lxml.etree


def test_ascus_table_preserves_genotypes_counts_and_gene_colors():
	tetradlib = import_from_repo_path('problems/inheritance-problems/gene_mapping/tetradlib.py')
	colors = ['003FFF', '007A00', 'A719DB']
	for genes in ('dx', 'dnx'):
		tetrads = tetradlib.get_all_possible_tetrads(genes)
		counts = {tetrad: (index + 1) * 100 for index, tetrad in enumerate(tetrads)}
		total = sum(counts.values())
		markup = tetradlib.make_progeny_html_table(counts, total, colors[:len(genes)])
		document = lxml.etree.fromstring(('<root>' + markup + '</root>').encode())
		rows = document.xpath('.//table[@class="tetrad-visual"]/tr[position() > 1]')
		assert len(rows) == len(counts)
		for row, tetrad in zip(rows, sorted(counts)):
			spores = row.xpath('.//*[@class="spore"]')
			assert sorted(node.get('data-genotype') for node in spores) == sorted(tetrad)
			assert ''.join(row[-1].itertext()) == f'{counts[tetrad]:,d}'
			for spore in spores:
				features = spore.xpath('.//*[@class="gene-color"]')
				assert [node.get('data-gene') for node in features] == [
					allele for allele in spore.get('data-genotype') if allele != '+']
				for node in features:
					assert node.get('fill') == '#' + colors[genes.index(node.get('data-gene'))]
		calculation = document.xpath('.//table[@class="tetrad-calculation"]')[0]
		assert len(calculation.xpath('./tr')) == len(counts) + 3
		assert len(calculation.xpath('.//td[@class="tetrad-classification"]')) == len(counts) * len(genes) * (len(genes) - 1) // 2
		assert calculation.xpath('./tr[last()]/td')[0].text == f'{total:,d}'
		for gene_index, gene in enumerate(genes):
			colored = calculation.xpath(f'./tr[2]/th/span[text()="{gene.upper()}"]')
			assert len(colored) == 4
			assert all(node.get('style').find('#' + colors[gene_index]) >= 0 for node in colored)


def test_tetradlib_ditype_and_tetratype_helpers():
	tetradlib = import_from_repo_path("problems/inheritance-problems/gene_mapping/tetradlib.py")
	tetradlib.debug = False

	ditype = tetradlib.make_ditype_from_genotype_str("++", "ab")
	assert ditype == ("++", "++", "ab", "ab")

	tetratype = tetradlib.make_tetratype_from_genotype_strings("++", "+b", "ab")
	assert set(tetratype) == {"++", "+b", "a+", "ab"}


def test_tetradlib_all_ditypes_small():
	tetradlib = import_from_repo_path("problems/inheritance-problems/gene_mapping/tetradlib.py")
	tetradlib.debug = False
	all_ditypes = tetradlib.get_all_ditype_tetrads("ab")
	assert len(all_ditypes) == 2
