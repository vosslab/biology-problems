"""Authored YAML and bounded procedural family sources."""

# Standard Library
import random
import pathlib
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
def _union_plan(rng: random.Random, seeds: int, count: int, generations: int,
		children: tuple[int, int], roots: tuple[int, int], max_people: int) -> tuple | None:
	"""Plan unions using child-slot references, reserving room before creating people."""
	parents = [(None, None) for _ in range(seeds)]
	ranks = [0] * seeds
	used = [0] * seeds
	# Adjacent founding families join through distinct children in generation two.
	for index in range(seeds - 1):
		pair = [(index, used[index]), (index + 1, used[index + 1])]
		used[index] += 1
		used[index + 1] += 1
		rng.shuffle(pair)
		parents.append(tuple(pair))
		ranks.append(1)
		used.append(0)

	def minimum_sizes() -> list[int]:
		result = [max(used[i], roots[0] if i < seeds else children[0])
			for i in range(len(parents))]
		return result

	if any(used[i] > roots[1] for i in range(seeds)):
		return None

	def grow() -> bool:
		remaining = count - len(parents)
		minimum = count + 1 + sum(minimum_sizes()) + remaining * children[0]
		if minimum > max_people:
			return False
		if remaining == 0:
			complete = max(ranks) == generations - 2
			return complete
		needed = generations - 2 - max(ranks)
		candidates = [i for i, rank in enumerate(ranks)
			if rank < generations - 2 and used[i] < (roots[1] if i < seeds else children[1])
			and (remaining > needed or rank == max(ranks))]
		rng.shuffle(candidates)
		for index in candidates:
			pair = [(index, used[index]), None]
			rng.shuffle(pair)
			used[index] += 1
			parents.append(tuple(pair))
			ranks.append(ranks[index] + 1)
			used.append(0)
			if grow():
				return True
			used.pop()
			ranks.pop()
			parents.pop()
			used[index] -= 1
		return False

	if not grow():
		return None
	result = (parents, minimum_sizes())
	return result


#============================================
def minimum_couples(generations: int, seed_couples: int) -> int:
	"""Minimum unions needed to join founding families and reach the requested depth."""
	result = generations - 1 if seed_couples == 1 else 2 * seed_couples + generations - 4
	return result


#============================================
def procedural_family(rng: random.Random, min_people: int = 11,
		max_people: int = 16, generations: int = 4, *, seed_couples: int = 1,
		couples: tuple[int, int] | None = None, children: tuple[int, int] = (1, 4),
		root_children: tuple[int, int] | None = None) -> family_model.Family:
	"""Construct one connected family within inclusive structural bounds.

	Seed couples start in generation one; their children join the founding families
	without consanguinity. Total couples includes seed, joining, and marrying-in
	unions. Child bounds apply per union, with separate bounds for seed unions.
	Relationships and feasible sibship sizes are planned before people are created.
	Infeasible combinations raise ValueError; no relatives are pruned afterward.
	"""
	if generations not in (3, 4, 5):
		raise ValueError('Generation count must be three, four, or five')
	if type(seed_couples) is not int or seed_couples < 1:
		raise ValueError('Seed couple count must be a positive integer')
	if root_children is None:
		root_children = (2, 6 if generations == 3 else 4)
	minimum = minimum_couples(generations, seed_couples)
	if couples is None:
		couples = (minimum, max(minimum, 5,
			1 + (max_people - 2 - root_children[1] + 4) // 5))
	for bounds in ((min_people, max_people), couples, children, root_children):
		if len(bounds) != 2 or any(type(n) is not int for n in bounds) or not 1 <= bounds[0] <= bounds[1]:
			raise ValueError('Construction bounds must be ordered positive integer pairs')
	counts = [n for n in range(max(couples[0], minimum), couples[1] + 1)
		if n + 1 + seed_couples * root_children[0] + (n - seed_couples) * children[0] <= max_people
		and n + 1 + seed_couples * root_children[1] + (n - seed_couples) * children[1] >= min_people]
	rng.shuffle(counts)
	plan = None
	for count in counts:
		plan = _union_plan(rng, seed_couples, count, generations, children, root_children, max_people)
		if plan is not None:
			break
	if plan is None:
		raise ValueError('Size bounds and couple/child counts cannot hold a supported teaching family')
	parents, sizes = plan
	upper = [root_children[1] if i < seed_couples else children[1] for i in range(len(parents))]
	# Joining seed families uses two existing children instead of a new spouse.
	# With seeds-1 joining unions, total people = total couples + 1 + all children.
	remaining = rng.randint(max(sum(sizes), min_people - len(parents) - 1),
		min(sum(upper), max_people - len(parents) - 1)) - sum(sizes)
	order = list(range(len(sizes)))
	rng.shuffle(order)
	for position, index in enumerate(order):
		capacity_after = sum(upper[i] - sizes[i] for i in order[position + 1:])
		added = rng.randint(max(0, remaining - capacity_after), min(remaining, upper[index] - sizes[index]))
		sizes[index] += added
		remaining -= added

	# Sex follows the planned parental role for marrying children; all others are random.
	sex_by_slot = {slot: sex for pair in parents
		for slot, sex in zip(pair, ('male', 'female')) if slot is not None}
	people, unions, slots = [], [], {}

	def add_person(sex: str) -> str:
		pid = f'p{len(people) + 1}'
		people.append(family_model.Person(pid, sex))
		return pid

	for index, pair in enumerate(parents):
		father, mother = [slots[slot] if slot is not None else add_person(sex)
			for slot, sex in zip(pair, ('male', 'female'))]
		offspring = []
		for child in range(sizes[index]):
			slot = (index, child)
			sex = sex_by_slot[slot] if slot in sex_by_slot else rng.choice(('male', 'female'))
			slots[slot] = add_person(sex)
			offspring.append(slots[slot])
		rng.shuffle(offspring)
		unions.append(family_model.Union(father, mother, tuple(offspring)))
	result = family_model.Family(tuple(people), tuple(unions))
	result.generations()
	return result


#============================================
def simulate_case(mode: str, rng: random.Random, min_people: int = 11,
		max_people: int = 16, show_carriers: bool = False, generations: int = 4, *,
		seed_couples: int = 1, couples: tuple[int, int] | None = None,
		children: tuple[int, int] = (1, 4), root_children: tuple[int, int] | None = None) -> Case:
	"""Enrich informative founder crosses, then transmit genotypes normally.

	Args:
		mode: One of inheritance.MODES.
		rng: Shared generator for family and genotype choices.
		min_people: Inclusive minimum size.
		max_people: Inclusive maximum size.
		generations: Required depth, from three to five.
		show_carriers: Reveal unaffected heterozygotes when true.
		seed_couples: Number of founding couples in generation one.
		couples: Inclusive bounds on total unions, including joining unions.
		children: Inclusive offspring bounds for non-seed unions.
		root_children: Inclusive offspring bounds for seed unions; None uses depth defaults.

	Returns:
		Simulated case awaiting biological, teaching, and layout acceptance.

	Raises:
		ValueError: Invalid mode or infeasible bounds.
	"""
	if mode not in inheritance.MODES:
		raise ValueError(f'Unknown mode: {mode}')
	family = procedural_family(rng, min_people, max_people, generations, seed_couples=seed_couples,
		couples=couples, children=children, root_children=root_children)
	parents = family.parentage()
	later_spouses = family_model.later_spouses(family)
	founders = {}
	for person in family.people:
		if person.id not in parents:
			founders[person.id] = inheritance.genotype_domain(mode, person.sex)[0]
	# A founder may marry into a later generation. Seed an allele where it can
	# reach grandchildren, without prescribing their sexes or transmitted alleles.
	parent_ids = {pid for union in family.unions for pid in (union.father, union.mother)}
	crosses = [union for union in family.unions
		if any(pid in parent_ids for pid in union.children)
		and (union.father in founders or union.mother in founders)]
	if mode in ('x-linked dominant', 'x-linked recessive', 'y-linked'):
		crosses = [union for union in crosses if union.father in founders]
	cross = rng.choice(crosses)
	if mode == 'autosomal dominant':
		candidates = [pid for pid in (cross.father, cross.mother) if pid in founders]
		founders[rng.choice(candidates)] = (0, 1)
	elif mode == 'autosomal recessive':
		for pid in founders:
			if pid in later_spouses:
				# Enrich teaching examples with affected spouses, never unaffected carriers.
				founders[pid] = (1, 1) if rng.random() < 0.1 else (0, 0)
			else:
				founders[pid] = (0, 1)
	elif mode == 'x-linked dominant':
		founders[cross.father] = (1,)
	elif mode == 'x-linked recessive':
		founders[cross.father] = (1,)
		if cross.mother in founders and cross.mother not in later_spouses:
			founders[cross.mother] = rng.choice(((0, 0), (0, 1)))
	else:
		founders[cross.father] = (1,)
	genotypes = inheritance.simulate(family, mode, rng, founders)
	observations = inheritance.observe(family, mode, genotypes, show_carriers)
	result = Case(family, observations, genotypes)
	return result
