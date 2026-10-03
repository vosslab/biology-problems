"""Protect cross-specific probabilities and small-sibship tail semantics."""

import numpy
import pytest

import pedigree_lib.family as family_model
import pedigree_lib.offspring_probability as offspring_probability


@pytest.mark.parametrize('mode,father,mother,expected', [
	('autosomal dominant', (0, 1), (0, 1), [0.125, 0.375, 0.125, 0.375]),
	('autosomal recessive', (0, 1), (0, 1), [0.375, 0.125, 0.375, 0.125]),
	('x-linked dominant', (1,), (0, 0), [0.5, 0, 0, 0.5]),
	('x-linked recessive', (1,), (0, 0), [0.5, 0, 0.5, 0]),
	('y-linked', (1,), (), [0, 0.5, 0.5, 0]),
])
def test_parental_cross_preserves_sex_and_mendelian_weights(mode, father, mother, expected):
	assert offspring_probability.probabilities(mode, father, mother) == expected


def test_small_sibship_tail_includes_ties_and_impossible_children():
	# Four children from aa x aa: all male has exact sex tail 2/16.
	children = tuple(f'c{i}' for i in range(4))
	family = family_model.Family((family_model.Person('f', 'male'),
		family_model.Person('m', 'female')) + tuple(family_model.Person(c, 'male') for c in children),
		(family_model.Union('f', 'm', children),))
	genotypes = {p.id: (0, 0) for p in family.people}
	report = offspring_probability.diagnose(family, 'autosomal recessive', genotypes,
		numpy.random.default_rng(17))
	assert report['pvalue'] == pytest.approx(0.125, abs=0.015)
	assert report['sibships'][0]['expected'] == [2, 0, 2, 0]
	# A heterozygote is impossible here even though its phenotype is unaffected.
	genotypes['c0'] = (0, 1)
	report = offspring_probability.diagnose(family, 'autosomal recessive', genotypes,
		numpy.random.default_rng(17))
	assert report['pvalue'] == 0
	assert report['impossible_children'] == ['c0']
