"""Fully penetrant Mendelian inheritance, without new mutations.

Alleles are 0 (ordinary) and 1 (trait); X/Y hemizygotes have one allele.
The same transmission function powers simulation and constraint solving.
"""

# Standard Library
import random
import functools
import itertools
import dataclasses

# local repo modules
import pedigree_lib.family as family_model

MODES = ('autosomal dominant', 'autosomal recessive', 'x-linked dominant',
	'x-linked recessive', 'y-linked')


#============================================
def genotype_domain(mode: str, sex: str) -> tuple[tuple[int, ...], ...]:
	"""List genotypes allowed by mode and sex.

	Args:
		mode: One of MODES.
		sex: male or female.

	Returns:
		Allele tuples; females have an empty genotype in Y-linked mode.

	Raises:
		ValueError: Unknown mode or sex.
	"""
	if mode not in MODES:
		raise ValueError(f'Unknown inheritance mode: {mode}')
	if sex not in ('male', 'female'):
		raise ValueError(f'Unknown sex: {sex}')
	if mode == 'y-linked':
		return ((0,), (1,)) if sex == 'male' else ((),)
	if mode.startswith('x-linked') and sex == 'male':
		return ((0,), (1,))
	return ((0, 0), (0, 1), (1, 1))


#============================================
def phenotype(mode: str, genotype: tuple[int, ...]) -> bool:
	"""Derive affected status under complete penetrance.

	Args:
		mode: One of MODES.
		genotype: A genotype from genotype_domain for the relevant sex.

	Returns:
		Whether the genotype expresses the trait.

	Raises:
		ValueError: Unknown mode.
	"""
	if mode not in MODES:
		raise ValueError(f'Unknown inheritance mode: {mode}')
	if mode.endswith('recessive'):
		result = bool(genotype) and all(genotype)
	else:
		result = any(genotype)
	return result


#============================================
@functools.lru_cache(maxsize=None)
def transmissions(mode: str, father: tuple, mother: tuple, sex: str) -> tuple:
	"""Enumerate equally probable gamete combinations.

	Args:
		mode: One of MODES.
		father: Paternal genotype.
		mother: Maternal genotype.
		sex: Offspring sex.

	Returns:
		Offspring genotypes, retaining repeats to preserve Mendelian probabilities.

	Raises:
		ValueError: Invalid mode, sex, or parental genotype.
	"""
	if father not in genotype_domain(mode, 'male') or mother not in genotype_domain(mode, 'female'):
		raise ValueError('Invalid parental genotypes')
	genotype_domain(mode, sex)
	if mode == 'y-linked':
		return (father,) if sex == 'male' else ((),)
	if mode.startswith('x-linked') and sex == 'male':
		result = tuple((allele,) for allele in mother)
	else:
		result = tuple(tuple(sorted((a, b))) for a in father for b in mother)
	return result


#============================================
@dataclasses.dataclass(frozen=True)
class Compatibility:
	mode: str
	compatible: bool
	witness: dict[str, tuple]


#============================================
def _propagate(family: family_model.Family, mode: str, domains: dict) -> bool:
	people = family.members()
	changed = True
	while changed:
		changed = False
		for union in family.unions:
			for child in union.children:
				ids = (union.father, union.mother, child)
				supports = [set(), set(), set()]
				for father, mother in itertools.product(domains[ids[0]], domains[ids[1]]):
					possible = set(transmissions(mode, father, mother, people[child].sex))
					for genotype in domains[child] & possible:
						supports[0].add(father)
						supports[1].add(mother)
						supports[2].add(genotype)
				for pid, supported in zip(ids, supports):
					if not supported:
						return False
					if supported != domains[pid]:
						domains[pid] = supported
						changed = True
	return True


#============================================
def _solve(family: family_model.Family, mode: str, domains: dict) -> dict | None:
	if any(not values for values in domains.values()) or not _propagate(family, mode, domains):
		return None
	unsolved = [pid for pid in domains if len(domains[pid]) > 1]
	if not unsolved:
		result = {pid: next(iter(values)) for pid, values in domains.items()}
		return result
	pid = min(unsolved, key=lambda key: len(domains[key]))
	for genotype in sorted(domains[pid]):
		branch = {key: set(values) for key, values in domains.items()}
		branch[pid] = {genotype}
		result = _solve(family, mode, branch)
		if result is not None:
			return result
	return None


#============================================
def analyze(family: family_model.Family, observations: dict, mode: str) -> Compatibility:
	"""Solve every family using only visible information.

	Args:
		family: People and unions to analyze.
		observations: Person-ID mapping of visible phenotypes and carrier markings.
		mode: One of MODES.

	Returns:
		Compatibility result with a genotype witness when a solution exists.

	Raises:
		ValueError: Invalid family, observations, or mode.
	"""
	family_model.validate_observations(family, observations)
	domains = {}
	for person in family.people:
		observation = observations[person.id]
		values = genotype_domain(mode, person.sex)
		domains[person.id] = {
			g for g in values
			if (observation.affected is None or phenotype(mode, g) == observation.affected)
			and (not observation.carrier or (mode.endswith('recessive') and g == (0, 1)))
		}
	witness = _solve(family, mode, domains)
	result = Compatibility(mode, witness is not None, {} if witness is None else witness)
	return result


#============================================
def simulate(family: family_model.Family, mode: str, rng: random.Random,
		founders: dict[str, tuple] | None = None) -> dict[str, tuple]:
	"""Transmit actual parental genotypes to every child.

	Args:
		family: People and unions to simulate.
		mode: One of MODES.
		rng: Explicit random-number generator shared by the pipeline.
		founders: Optional founder-ID genotype overrides; others are sampled.

	Returns:
		Genotypes keyed by person ID.

	Raises:
		ValueError: Invalid structure, mode, founder IDs, or genotype overrides.
	"""
	ranks = family.generations()
	parents = family.parentage()
	founders = {} if founders is None else founders
	if set(founders) - (set(ranks) - set(parents)):
		raise ValueError('Only founders can have supplied simulation genotypes')
	genotypes = {}
	for person in sorted(family.people, key=lambda p: ranks[p.id]):
		if person.id in parents:
			union = parents[person.id]
			values = transmissions(mode, genotypes[union.father],
				genotypes[union.mother], person.sex)
		else:
			values = genotype_domain(mode, person.sex)
		if person.id in founders:
			genotype = founders[person.id]
			if genotype not in values:
				raise ValueError(f'Invalid genotype for {person.id}: {genotype}')
		else:
			genotype = rng.choice(values)
		genotypes[person.id] = genotype
	return genotypes


#============================================
def observe(family: family_model.Family, mode: str, genotypes: dict,
		show_carriers: bool = False) -> dict[str, family_model.Observation]:
	"""Create visible observations without changing genotypes.

	Args:
		family: Family corresponding to the genotype map.
		mode: One of MODES.
		genotypes: Simulated genotypes keyed by person ID.
		show_carriers: Reveal unaffected heterozygotes when true.

	Returns:
		New observations keyed by person ID.
	"""
	if set(genotypes) != set(family.members()):
		raise ValueError('Genotypes must identify every person exactly once')
	result = {}
	for person in family.people:
		genotype = genotypes[person.id]
		if genotype not in genotype_domain(mode, person.sex):
			raise ValueError(f'Invalid genotype for {person.id}')
		carrier = show_carriers and mode.endswith('recessive') and genotype == (0, 1)
		result[person.id] = family_model.Observation(phenotype(mode, genotype), carrier)
	return result
