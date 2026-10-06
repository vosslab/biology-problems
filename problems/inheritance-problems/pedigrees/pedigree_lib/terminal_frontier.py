"""Plan terminal breadth before people exist; keep designation out of biology."""

import random

import pedigree_lib.family as family_model
import pedigree_lib.layout as layout


#============================================
class Rejected(ValueError):
	"""An expected capacity or geometry rejection of a sampled frontier."""


#============================================
def _layers(rng: random.Random, seeds: int, count: int, depth: int,
		root_max: int, child_max: int, terminal_count: int) -> list[int] | None:
	"""Reserve the final layer and fill intervening union counts with bounded search."""
	dead = set()

	def fill(rank: int, previous: int, remaining: int) -> list[int] | None:
		key = (rank, previous, remaining)
		if key in dead:
			return None
		joins = seeds - 1 if rank == 1 else 0
		capacity = previous * (root_max if rank == 1 else child_max) - joins
		if rank == depth - 2:
			if remaining == terminal_count and joins <= terminal_count <= capacity:
				return [terminal_count]
			return None
		# At least one union per intervening rank, plus all reserved terminal unions.
		after = depth - 3 - rank
		upper = min(capacity, remaining - terminal_count - after)
		options = list(range(max(1, joins), upper + 1))
		rng.shuffle(options)
		for number in options:
			if number * child_max ** (depth - 2 - rank) < terminal_count:
				continue
			suffix = fill(rank + 1, number, remaining - number)
			if suffix is not None:
				return [number] + suffix
		dead.add(key)
		return None

	result = fill(1, seeds, count - seeds)
	if result is not None:
		result = [seeds] + result
	return result


#============================================
def plan(rng: random.Random, generations: int, seeds: int, couples: tuple[int, int],
		children: tuple[int, int], roots: tuple[int, int], people: tuple[int, int],
		frontier_count: int) -> tuple | None:
	"""Return parent-slot pairs, minimum sibship sizes, and ordered terminal unions.

	Foundation lines join through distinct generation-II children. Other unions
	use one earlier child and one unrelated spouse. Each rank distributes these
	connections across available parental sibships before reusing a branch.
	All counts are checked before any Person objects or biological state exist.
	"""
	# ASVS 2.2.1: validate counts and their combined capacity at the construction boundary.
	if type(generations) is not int or generations not in range(3, 8):
		raise ValueError('Generation count must be between three and seven')
	if type(seeds) is not int or seeds < 1:
		raise ValueError('Seed couple count must be a positive integer')
	if type(frontier_count) is not int or frontier_count < 2:
		raise ValueError('Frontier count must be an integer of at least two')
	for bounds in (couples, children, roots, people):
		if len(bounds) != 2 or any(type(n) is not int for n in bounds) or not 1 <= bounds[0] <= bounds[1]:
			raise ValueError('Construction bounds must be ordered positive integer pairs')
	if seeds > 2 and roots[1] < 2:
		return None
	counts = list(range(max(couples[0], seeds + frontier_count), couples[1] + 1))
	rng.shuffle(counts)
	for count in counts:
		if count + 1 + seeds * roots[0] + (count - seeds) * children[0] > people[1]:
			continue
		if count + 1 + seeds * roots[1] + (count - seeds) * children[1] < people[0]:
			continue
		layers = _layers(rng, seeds, count, generations, roots[1], children[1], frontier_count)
		if layers is None:
			continue
		parents, used = _connect(rng, layers, roots[1], children[1])
		sizes = [max(used[i], roots[0] if i < seeds else children[0]) for i in range(count)]
		if count + 1 + sum(sizes) > people[1]:
			continue
		terminals = tuple(range(count - frontier_count, count))
		return parents, sizes, terminals
	return None


#============================================
def _connect(rng: random.Random, layers: list[int], root_max: int,
		child_max: int) -> tuple[list, list[int]]:
	"""Connect reserved layers using each child slot as a partner at most once."""
	seeds = layers[0]
	parents = [(None, None) for _ in range(seeds)]
	used = [0] * seeds
	previous = list(range(seeds))
	for rank, number in enumerate(layers[1:], 1):
		pairs = []
		limit = root_max if rank == 1 else child_max
		if rank == 1:
			for index in range(seeds - 1):
				pairs.append([(index, used[index]), (index + 1, used[index + 1])])
				used[index] += 1
				used[index + 1] += 1
		while len(pairs) < number:
			available = [i for i in previous if used[i] < limit]
			least = min(used[i] for i in available)
			index = rng.choice([i for i in available if used[i] == least])
			pairs.append([(index, used[index]), None])
			used[index] += 1

		def pair_key(pair: list) -> float:
			# Order by relationship slots, independent of drawing coordinates.
			keys = [slot[0] * (limit + 1) + slot[1] for slot in pair if slot is not None]
			result = sum(keys) / len(keys)
			return result

		pairs.sort(key=pair_key)
		previous = list(range(len(parents), len(parents) + number))
		for pair in pairs:
			rng.shuffle(pair)
			parents.append(tuple(pair))
			used.append(0)
	return parents, used


#============================================
def endpoints_match(diagram: layout.Diagram, designated: tuple[str, ...]) -> bool:
	"""Check the actual deepest-row extremes, including reflected diagrams."""
	last_y = max(symbol.y for symbol in diagram.symbols)
	row = [symbol for symbol in diagram.symbols if symbol.y == last_y]
	left = min(row, key=lambda symbol: symbol.x).person
	right = max(row, key=lambda symbol: symbol.x).person
	result = left in designated and right in designated
	return result


#============================================
def validate_layout(family: family_model.Family, designated: tuple[str, ...]) -> None:
	"""Reject unreadable ordering before simulation; structural defects propagate."""
	family.generations()
	try:
		diagram = layout.lay_out(family)
	except layout.AlignmentFailure as error:
		raise Rejected('Frontier layout cannot align this ordering') from error
	errors = layout.layout_errors(diagram)
	if errors:
		raise Rejected('Frontier layout: ' + '; '.join(errors))
	if not endpoints_match(diagram, designated):
		raise Rejected('Frontier endpoints are not the final-row extremes')
