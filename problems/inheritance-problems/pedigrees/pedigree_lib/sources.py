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
import pedigree_lib.terminal_frontier as terminal_frontier


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
	if generations not in (3, 4, 5, 6, 7):
		raise ValueError('Generation count must be between three and seven')
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
	result, _ = _instantiate(rng, parents, sizes, seed_couples, root_children, children,
		min_people, max_people)
	return result


#============================================
def _instantiate(rng: random.Random, parents: list, sizes: list[int], seeds: int,
		roots: tuple[int, int], children: tuple[int, int], min_people: int, max_people: int,
		terminal_unions: tuple[int, ...] = ()) -> tuple[family_model.Family, tuple[str, ...]]:
	"""Allocate complete sibships and instantiate either relationship plan once."""
	upper = [roots[1] if i < seeds else children[1] for i in range(len(parents))]
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

	# Designation belongs to planning slots, before any Person is created.
	designated_slots = {}
	for position, index in enumerate(terminal_unions):
		if position == 0:
			child_index = 0
		elif position == len(terminal_unions) - 1:
			child_index = sizes[index] - 1
		else:
			child_index = rng.randrange(sizes[index])
		designated_slots[index] = (index, child_index)

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
		if not terminal_unions:
			rng.shuffle(offspring)
		unions.append(family_model.Union(father, mother, tuple(offspring)))
	result = family_model.Family(tuple(people), tuple(unions))
	result.generations()
	designated = tuple(slots[slot] for slot in designated_slots.values())
	return result, designated


#============================================
def frontier_family(rng: random.Random, min_people: int, max_people: int,
		generations: int, *, seed_couples: int, couples: tuple[int, int],
		children: tuple[int, int], root_children: tuple[int, int],
		frontier_count: int) -> tuple[family_model.Family, tuple[str, ...]]:
	"""Construct a checked frontier, returning transient designated person IDs.

	Raises:
		ValueError: Invalid construction inputs.
		terminal_frontier.Rejected: This sampled shape or layout cannot realize the frontier.
	"""
	plan = terminal_frontier.plan(rng, generations, seed_couples, couples,
		children, root_children, (min_people, max_people), frontier_count)
	if plan is None:
		raise terminal_frontier.Rejected('Frontier capacity cannot fit the sampled shape')
	parents, sizes, terminals = plan
	family, designated = _instantiate(rng, parents, sizes, seed_couples,
		root_children, children, min_people, max_people, terminals)
	terminal_frontier.validate_layout(family, designated)
	return family, designated


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
		generations: Required depth, from three to seven.
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
	result = simulate_family(family, mode, rng, show_carriers)
	return result


#============================================
def simulate_family(family: family_model.Family, mode: str, rng: random.Random,
		show_carriers: bool = False) -> Case:
	"""Apply existing founder policy and Mendelian simulation to a completed family.

	Construction provenance is deliberately absent from this interface.
	"""
	if mode not in inheritance.MODES:
		raise ValueError(f'Unknown mode: {mode}')
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
