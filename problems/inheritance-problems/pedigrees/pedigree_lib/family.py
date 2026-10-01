"""Family relationships, independent of inheritance and drawing coordinates."""

# Standard Library
import dataclasses


#============================================
@dataclasses.dataclass(frozen=True)
class Person:
	id: str
	sex: str
	label: str = ''


#============================================
@dataclasses.dataclass(frozen=True)
class Union:
	father: str
	mother: str
	children: tuple[str, ...]


#============================================
@dataclasses.dataclass(frozen=True)
class Observation:
	affected: bool | None
	carrier: bool = False


#============================================
@dataclasses.dataclass(frozen=True)
class Family:
	people: tuple[Person, ...]
	unions: tuple[Union, ...]

	def members(self) -> dict[str, Person]:
		"""Index people by their stable identifiers.

		Returns:
			Person objects keyed by ID; call generations() first to validate uniqueness.
		"""
		result = {person.id: person for person in self.people}
		return result

	def parentage(self) -> dict[str, Union]:
		"""Derive parentage from the union child lists.

		Returns:
			The parental union for each nonfounder; requires validated structure.
		"""
		result = {child: union for union in self.unions for child in union.children}
		return result

	def generations(self) -> dict[str, int]:
		"""Validate structure and solve relative generation constraints.

		Returns:
			Person IDs mapped to generation ranks, starting at zero per component.

		Raises:
			ValueError: Invalid relationships, people, cycles, or generation constraints.
		"""
		people = self.members()
		if not people or len(people) != len(self.people):
			raise ValueError('People must have unique identifiers and family must not be empty')
		for person in self.people:
			if not isinstance(person.id, str) or not person.id or person.sex not in ('male', 'female'):
				raise ValueError(f'Invalid person: {person}')
			if not isinstance(person.label, str) or len(person.label) > 12:
				raise ValueError('Labels must be text of at most 12 characters')
		links = {pid: [] for pid in people}
		partners = set()
		children = set()
		for union in self.unions:
			refs = (union.father, union.mother, *union.children)
			if any(pid not in people for pid in refs):
				raise ValueError(f'Missing person reference in {union}')
			if people[union.father].sex != 'male' or people[union.mother].sex != 'female':
				raise ValueError('Each union requires one father and one mother')
			if union.father in partners or union.mother in partners:
				raise ValueError('Multiple unions per person are not supported')
			partners.update((union.father, union.mother))
			links[union.father].append((union.mother, 0))
			links[union.mother].append((union.father, 0))
			for child in union.children:
				if child in children:
					raise ValueError(f'Duplicate parentage: {child}')
				children.add(child)
				for parent in (union.father, union.mother):
					links[parent].append((child, 1))
					links[child].append((parent, -1))
		# A single constraint solve detects ancestry cycles and incompatible generations.
		ranks = {}
		for pid in people:
			if pid in ranks:
				continue
			ranks[pid] = 0
			component = [pid]
			for current in component:
				for neighbor, delta in links[current]:
					wanted = ranks[current] + delta
					if neighbor in ranks:
						if ranks[neighbor] != wanted:
							raise ValueError('Ancestry cycle or inconsistent generations')
					else:
						ranks[neighbor] = wanted
						component.append(neighbor)
			minimum = min(ranks[member] for member in component)
			for member in component:
				ranks[member] -= minimum
		return ranks

	def ancestors(self, pid: str) -> set[str]:
		"""Collect ancestors without duplicating shared relatives.

		Args:
			pid: Person identifier whose ancestors are requested.

		Returns:
			Ancestor IDs; empty when no parentage is recorded for pid.

		Raises:
			ValueError: The family structure is invalid.
		"""
		self.generations()
		parents = self.parentage()
		result = set()
		pending = [pid]
		while pending:
			current = pending.pop()
			if current in parents:
				union = parents[current]
				for parent in (union.father, union.mother):
					if parent not in result:
						result.add(parent)
						pending.append(parent)
		return result


#============================================
def validate_observations(family: Family, observations: dict[str, Observation]) -> None:
	"""Validate one visible observation per person.

	Args:
		family: Family whose structure and observations will be checked.
		observations: ID-keyed observations; None affected status means unknown.

	Raises:
		ValueError: Invalid structure, missing observations, or contradictory markings.
	"""
	family.generations()
	if set(observations) != set(family.members()):
		raise ValueError('Observations must identify every person exactly once')
	for observation in observations.values():
		if observation.affected is not None and type(observation.affected) is not bool:
			raise ValueError('Affected observations must be boolean or None')
		if type(observation.carrier) is not bool or (observation.carrier and observation.affected):
			raise ValueError('A carrier marking denotes an unaffected heterozygote')
