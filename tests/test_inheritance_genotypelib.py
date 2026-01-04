#!/usr/bin/env python3

from lib_test_utils import import_from_repo_path


def test_genotypelib_cross_counts():
	genotypelib = import_from_repo_path("inheritance-problems/genotypelib.py")
	assert genotypelib.deconstructPowerOfNumber(72) == (3, 2)

	cross = genotypelib.crossGenotypes(("A", "a"), ("A", "a"))
	assert sorted(cross) == ["AA", "Aa", "aa"]

	phenos = genotypelib.crossPhenotypes(("A", "a"), ("A", "a"))
	assert sorted(phenos) == ["A", "a"]

	gene_list = [("A", "a"), ("B", "b")]
	assert genotypelib.countGenotypesForCross(gene_list, gene_list) == 9
	assert genotypelib.countPhenotypesForCross(gene_list, gene_list) == 4
