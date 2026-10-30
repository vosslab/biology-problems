
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
		top_tables = document.xpath('.//table[not(ancestor::table)]')
		visual_tables = [
			table for table in top_tables if table.xpath('./tr[1]/th')[1].text == 'Tetrad Genotypes'
		]
		rows = [row for table in visual_tables for row in table.xpath('./tr[position() > 1]')]
		assert len(rows) == len(counts)
		for row, tetrad in zip(rows, sorted(counts)):
			spores = row.xpath('.//*[@data-genotype]')
			assert sorted(node.get('data-genotype') for node in spores) == sorted(tetrad)
			assert ''.join(row[-1].itertext()) == f'{counts[tetrad]:,d}'
			for spore in spores:
				features = spore.xpath('.//*[@data-gene]')
				assert [node.get('data-gene') for node in features] == [
					allele for allele in spore.get('data-genotype') if allele != '+']
				for node in features:
					assert node.get('fill') == '#' + colors[genes.index(node.get('data-gene'))]
		calculation, = [
			table for table in top_tables if table.xpath('./tr[1]/th')[1].text == 'Spore 1'
		]
		assert len(calculation.xpath('./tr')) == len(counts) + 3
		spore_rows = calculation.xpath('./tr[position() > 2 and position() < last()]')
		for row, tetrad in zip(spore_rows, sorted(counts)):
			spore_texts = [
				''.join(spore.itertext()) for spore in row.xpath('./td[div/table]')
			]
			assert sorted(spore_texts) == sorted(tetrad)
		assert len(calculation.xpath('.//td[@data-pair]')) == len(counts) * len(genes) * (len(genes) - 1) // 2
		assert calculation.xpath('./tr[last()]/td')[0].text == f'{total:,d}'
		for gene_index, gene in enumerate(genes):
			colored = calculation.xpath(f'./tr[2]/th/table//span[text()="{gene.upper()}"]')
			assert len(colored) == 4
			assert all(node.get('style').find('#' + colors[gene_index]) >= 0 for node in colored)
		assert 'class=' not in markup


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
