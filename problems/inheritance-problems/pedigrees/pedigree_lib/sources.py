"""Authored YAML and bounded procedural family sources."""

# Standard Library
import random
import pathlib
import itertools
import dataclasses

# PIP3 modules
import yaml

# local repo modules
import pedigree_lib.family as family_model
import pedigree_lib.inheritance as inheritance


#============================================
@dataclasses.dataclass(frozen=True)
class Case:
	family: family_model.Family
	observations: dict[str, family_model.Observation]
	genotypes: dict[str, tuple] = dataclasses.field(default_factory=dict)
	metadata: dict = dataclasses.field(default_factory=dict)
	ordered_unions: tuple[int, ...] = ()


#============================================
def load_cases(path: str | pathlib.Path) -> list[Case]:
	"""Load a YAML bank; explicit sibling_order hints prevent later shuffling.

	Args:
		path: Path to the people-and-unions YAML document.

	Returns:
		Structurally validated cases; bare children order is only an initial order.

	Raises:
		ValueError: Invalid relationships, observations, or sibling-order hints.
	"""
	# ASVS 1.5.2: YAML contains plain data, never executable Python objects.
	with open(path, encoding='utf-8') as stream:
		document = yaml.safe_load(stream)
	result = []
	for entry in document['cases']:
		people = []
		observations = {}
		for row in entry['people']:
			person = family_model.Person(row['id'], row['sex'], row.get('label', ''))
			if person.id in observations:
				raise ValueError(f'Duplicate person: {person.id}')
			people.append(person)
			observations[person.id] = family_model.Observation(row['affected'], row.get('carrier', False))
		unions = []
		ordered_unions = []
		for index, row in enumerate(entry['unions']):
			children = row['children']
			order = row.get('sibling_order', children)
			if len(order) != len(children) or set(order) != set(children):
				raise ValueError('Sibling order must contain each child exactly once')
			unions.append(family_model.Union(row['father'], row['mother'], tuple(order)))
			if 'sibling_order' in row:
				ordered_unions.append(index)
		family = family_model.Family(tuple(people), tuple(unions))
		family_model.validate_observations(family, observations)
		result.append(Case(family, observations, metadata=entry.get('metadata', {}),
			ordered_unions=tuple(ordered_unions)))
	return result


#============================================
def procedural_family(rng: random.Random, min_people: int = 11,
		max_people: int = 16) -> family_model.Family:
	"""Choose feasible sibships, then grow branches from unmarried descendants.

	Args:
		rng: Shared generator for topology and sex choices.
		min_people: Inclusive minimum size.
		max_people: Inclusive maximum size.

	Returns:
		Family with three or four generations; no people are truncated to meet bounds.

	Raises:
		ValueError: No supported topology fits the requested size bounds.
	"""
	# Each descendant union adds one spouse and its children. Choose all sizes
	# before adding people, so even narrow bounds never require pruning relatives.
	configurations = [sizes for branches in range(1, 4)
		for sizes in itertools.product(range(1, 5), repeat=branches + 1)
		if sizes[0] >= 2 and min_people <= 2 + branches + sum(sizes) <= max_people]
	if not configurations:
		raise ValueError('Size bounds cannot hold a supported teaching family')
	sizes = rng.choice(configurations)
	people = [family_model.Person('p1', 'male'), family_model.Person('p2', 'female')]
	unions = []

	def add_person(sex: str | None = None) -> str:
		pid = f'p{len(people) + 1}'
		if sex is None:
			sex = rng.choice(('male', 'female'))
		people.append(family_model.Person(pid, sex))
		return pid

	children = tuple(add_person() for _ in range(sizes[0]))
	unions.append(family_model.Union('p1', 'p2', children))
	available = list(children)
	ranks = {child: 1 for child in children}
	for offspring_count in sizes[1:]:
		child = rng.choice(available)
		available.remove(child)
		sex = next(person.sex for person in people if person.id == child)
		spouse = add_person('female' if sex == 'male' else 'male')
		father, mother = (child, spouse) if sex == 'male' else (spouse, child)
		offspring = tuple(add_person() for _ in range(offspring_count))
		unions.append(family_model.Union(father, mother, offspring))
		for pid in offspring:
			ranks[pid] = ranks[child] + 1
			if ranks[pid] < 3:
				available.append(pid)
	result = family_model.Family(tuple(people), tuple(unions))
	result.generations()
	return result


#============================================
def simulate_case(mode: str, rng: random.Random, min_people: int = 11,
		max_people: int = 16, show_carriers: bool = False) -> Case:
	"""Enrich informative founder crosses, then transmit genotypes normally.

	Args:
		mode: One of inheritance.MODES.
		rng: Shared generator for family and genotype choices.
		min_people: Inclusive minimum size.
		max_people: Inclusive maximum size.
		show_carriers: Reveal unaffected heterozygotes when true.

	Returns:
		Simulated case awaiting biological, teaching, and layout acceptance.

	Raises:
		ValueError: Invalid mode or infeasible bounds.
	"""
	if mode not in inheritance.MODES:
		raise ValueError(f'Unknown mode: {mode}')
	family = procedural_family(rng, min_people, max_people)
	parents = family.parentage()
	founders = {}
	for person in family.people:
		if person.id not in parents:
			founders[person.id] = inheritance.genotype_domain(mode, person.sex)[0]
	# A founder may marry into a later generation. Seed an allele where it can
	# reach grandchildren, without prescribing their sexes or transmitted alleles.
	parent_ids = {pid for union in family.unions for pid in (union.father, union.mother)}
	crosses = [union for union in family.unions
		if any(pid in parent_ids for pid in union.children)]
	if mode in ('x-linked dominant', 'x-linked recessive', 'y-linked'):
		crosses = [union for union in crosses if union.father in founders]
	cross = rng.choice(crosses)
	if mode == 'autosomal dominant':
		candidates = [pid for pid in (cross.father, cross.mother) if pid in founders]
		founders[rng.choice(candidates)] = (0, 1)
	elif mode == 'autosomal recessive':
		founders = {pid: (0, 1) for pid in founders}
	elif mode == 'x-linked dominant':
		founders[cross.father] = (1,)
	elif mode == 'x-linked recessive':
		founders[cross.father] = (1,)
		if cross.mother in founders:
			founders[cross.mother] = rng.choice(((0, 0), (0, 1)))
	else:
		founders[cross.father] = (1,)
	genotypes = inheritance.simulate(family, mode, rng, founders)
	observations = inheritance.observe(family, mode, genotypes, show_carriers)
	result = Case(family, observations, genotypes)
	return result
