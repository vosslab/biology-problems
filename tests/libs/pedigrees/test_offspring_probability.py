"""Protect cross-specific probabilities and small-sibship tail semantics."""

import numpy
import pytest

import pedigree_lib.family as family_model
import pedigree_lib.offspring_probability as offspring_probability
import pedigree_lib.inheritance as inheritance
import pedigree_lib.questions as questions
import pedigree_lib.sources as sources


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


@pytest.mark.parametrize('affected,expected', [(0, 148 / 256), (1, 1),
	(2, 148 / 256), (3, 13 / 256), (4, 1 / 256)])
def test_exact_carrier_cross_tail_includes_equally_extreme_counts(affected, expected):
	assert offspring_probability.affected_count_tail('autosomal recessive',
		(0, 1), (0, 1), ('male', 'male', 'female', 'female'), affected) == expected


def test_exact_tail_conditions_on_sex_and_handles_deterministic_crosses():
	# Carrier mother: four unaffected daughters contribute no random affected outcomes.
	assert offspring_probability.affected_count_tail('x-linked recessive', (0,), (0, 1),
		('male',) * 6 + ('female',) * 4, 6) == 2 / 64
	# All six daughters of this father must be affected; their count is not surprising.
	assert offspring_probability.affected_count_tail('x-linked dominant', (1,), (0, 0),
		('female',) * 6, 6) == 1
	assert offspring_probability.affected_count_tail('y-linked', (1,), (),
		('male', 'female'), 0) == 0


@pytest.mark.parametrize('sexes,affected_ids', [
	(('male', 'male', 'female', 'female'), ('c0', 'c1', 'c2', 'c3')),
	# Four of six affected has p = 154/4096: below 5% but above 1%.
	(('male', 'male', 'female', 'female', 'male', 'female'), ('c0', 'c1', 'c2', 'c3')),
])
def test_classroom_gate_rejects_extreme_sibship_without_changing_genotypes(sexes, affected_ids):
	children = tuple(f'c{i}' for i in range(len(sexes)))
	family = family_model.Family((family_model.Person('f', 'male'),
		family_model.Person('m', 'female')) + tuple(family_model.Person(pid,
		sexes[i]) for i, pid in enumerate(children)),
		(family_model.Union('f', 'm', children),))
	genotypes = {'f': (0, 1), 'm': (0, 1),
		**{pid: (1, 1) if pid in affected_ids else (0, 0) for pid in children}}
	observations = inheritance.observe(family, 'autosomal recessive', genotypes)
	case = sources.Case(family, observations, genotypes)
	accepted, reasons = questions.evaluate(case)
	assert accepted is None
	assert 'affected-count tail' in reasons[0]
	assert all(case.genotypes[pid] == (1, 1) for pid in affected_ids)
	# Ordinary variation remains eligible, without changing the family structure.
	genotypes = dict(genotypes, c1=(0, 1), c3=(0, 0))
	observations = inheritance.observe(family, 'autosomal recessive', genotypes)
	accepted, reasons = questions.evaluate(sources.Case(family, observations, genotypes))
	assert accepted is not None, reasons
