"""Diagnostic Pearson tails for fixed parental crosses, never an acceptance gate."""

import numpy

import pedigree_lib.family as family_model
import pedigree_lib.inheritance as inheritance

CATEGORIES = (('male', False), ('male', True), ('female', False), ('female', True))


#============================================
def probabilities(mode: str, father: tuple, mother: tuple) -> list[float]:
	"""Return sex x phenotype probabilities with equally likely offspring sexes."""
	result = []
	for sex, affected in CATEGORIES:
		outcomes = inheritance.transmissions(mode, father, mother, sex)
		count = sum(inheritance.phenotype(mode, genotype) == affected for genotype in outcomes)
		result.append(0.5 * count / len(outcomes))
	return result


#============================================
def _pearson(counts, expected):
	"""Exclude structural zeros; callers handle impossible observations separately."""
	positive = expected > 0
	result = numpy.sum((counts[..., positive] - expected[positive]) ** 2 / expected[positive], axis=-1)
	return result


#============================================
def _tail(simulated, observed: float) -> float:
	# Count numerical ties in the upper tail, including multinomial permutations.
	count = numpy.count_nonzero((simulated >= observed) | numpy.isclose(
		simulated, observed, rtol=1e-12, atol=1e-12))
	result = float((count + 1) / (len(simulated) + 1))
	return result


#============================================
def diagnose(family: family_model.Family, mode: str, genotypes: dict[str, tuple],
		rng: numpy.random.Generator, simulations: int = 9999) -> dict:
	"""Compare each sibship to its actual parental cross using Monte Carlo tails.

	The reference draws independent sibships with observed parents and sizes fixed.
	It does not resimulate ancestry or condition on teaching/selection filters.
	Original sampled genotypes are required; inferred witnesses change the null.
	An impossible transmission has p=0 and a null statistic (not JSON Infinity).
	Individual p-values are unadjusted; the smallest is a descriptive warning.
	"""
	family.generations()
	if type(simulations) is not int or simulations < 1:
		raise ValueError('simulations must be a positive integer')
	if set(genotypes) != set(family.members()):
		raise ValueError('Supply the original genotype of every person')
	for person in family.people:
		if genotypes[person.id] not in inheritance.genotype_domain(mode, person.sex):
			raise ValueError(f'Invalid genotype for {person.id}')
	people = family.members()
	total_simulated = numpy.zeros(simulations)
	total_observed = 0.0
	sibships = []
	impossible = []
	for index, union in enumerate(family.unions):
		if not union.children:
			continue
		father, mother = genotypes[union.father], genotypes[union.mother]
		probs = numpy.array(probabilities(mode, father, mother))
		expected = len(union.children) * probs
		observed = numpy.zeros(len(CATEGORIES), dtype=int)
		invalid = []
		for child in union.children:
			sex, genotype = people[child].sex, genotypes[child]
			observed[CATEGORIES.index((sex, inheritance.phenotype(mode, genotype)))] += 1
			if genotype not in inheritance.transmissions(mode, father, mother, sex):
				invalid.append(child)
		statistic = float(_pearson(observed, expected))
		sampled = rng.multinomial(len(union.children), probs, size=simulations)
		simulated = _pearson(sampled, expected)
		pvalue = 0.0 if invalid else _tail(simulated, statistic)
		sibships.append(dict(union_index=index, father=union.father, mother=union.mother,
			children=list(union.children), probabilities=probs.tolist(),
			observed=observed.tolist(), expected=expected.tolist(),
			statistic=None if invalid else statistic, pvalue=pvalue, impossible_children=invalid))
		impossible.extend(invalid)
		total_observed += statistic
		total_simulated += simulated
	if not sibships:
		raise ValueError('At least one nonempty sibship is required')
	worst = min(sibships, key=lambda row: row['pvalue'])
	result = dict(mode=mode, reference='independent fixed parental crosses',
		categories=[f'{sex} {"affected" if affected else "unaffected"}' for sex, affected in CATEGORIES],
		simulations=simulations, statistic=None if impossible else total_observed,
		pvalue=0.0 if impossible else _tail(total_simulated, total_observed),
		impossible_children=impossible, worst_union_index=worst['union_index'],
		worst_sibship_pvalue=worst['pvalue'], sibships=sibships)
	return result
