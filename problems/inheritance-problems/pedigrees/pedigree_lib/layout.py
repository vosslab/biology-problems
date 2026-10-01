"""Layered family geometry shared by HTML and editable SVG renderers."""

# Standard Library
import itertools
import dataclasses

# PIP3 modules
import scipy.optimize

# local repo modules
import pedigree_lib.family as family_model
import pedigree_lib.graphs as graphs

# Output size is independent of the coordinates used for layout and validation.
DISPLAY_SCALE = 0.75
RADIUS = 16
SIBLING_GAP = 26
FAMILY_GAP = 48
GENERATION_GAP = 96


#============================================
@dataclasses.dataclass(frozen=True)
class Symbol:
	person: str
	x: float
	y: float
	sex: str
	label: str


#============================================
@dataclasses.dataclass(frozen=True)
class Segment:
	x1: float
	y1: float
	x2: float
	y2: float
	union: int


#============================================
@dataclasses.dataclass(frozen=True)
class Diagram:
	symbols: tuple[Symbol, ...]
	segments: tuple[Segment, ...]
	width: float
	height: float


#============================================
def _half_width(person: family_model.Person) -> float:
	result = max(RADIUS, len(person.label) * 4.5)
	return result


#============================================
def _gap(left: list, right: list, parents: dict) -> int:
	shared = any(a in parents and b in parents and parents[a] == parents[b]
		for a in left for b in right)
	return SIBLING_GAP if shared else FAMILY_GAP


#============================================
def _positions(family: family_model.Family, component: set, ranks: dict) -> dict:
	"""Order couple blocks by ancestry, then align the complete connected family."""
	people = family.members()
	parents = family.parentage()
	partners = {}
	for union in family.unions:
		partners[union.father] = union.mother
		partners[union.mother] = union.father
	rows = []
	x = {}
	for generation in range(max(ranks[pid] for pid in component) + 1):
		members = [p.id for p in family.people if p.id in component and ranks[p.id] == generation]
		keys = {}
		for index, pid in enumerate(members):
			if pid in parents:
				union = parents[pid]
				keys[pid] = (x[union.father] + x[union.mother]) / 2 + union.children.index(pid) / 10
			else:
				keys[pid] = index * 100
		blocks = []
		seen = set()
		for pid in members:
			if pid in seen:
				continue
			block = [pid]
			if pid in partners:
				block.append(partners[pid])
			seen.update(block)
			inherited = [keys[p] for p in block if p in parents]
			key = sum(inherited) / len(inherited) if inherited else keys[pid]
			# Start spouses outward; related partners follow their parent groups.
			if len(block) == 2:
				if all(p in parents for p in block):
					block.sort(key=lambda p: keys[p])
				elif len(inherited) == 1:
					child = next(p for p in block if p in parents)
					u = parents[child]
					left_half = u.children.index(child) < (len(u.children) - 1) / 2
					block = [partners[child], child] if left_half else [child, partners[child]]
			blocks.append((key, block))
		blocks.sort(key=lambda item: item[0])
		row = [block for _, block in blocks]
		rows.append(row)
		cursor = 0
		for index, block in enumerate(row):
			for pid in block:
				cursor += _half_width(people[pid])
				x[pid] = cursor
				cursor += _half_width(people[pid]) + SIBLING_GAP
			if index + 1 < len(row):
				cursor += _gap(block, row[index + 1], parents) - SIBLING_GAP
	x = _align_family(family, rows, people, parents)
	x = _compact_spouses(family, rows, people, parents, ranks, x)
	return x


#============================================
def _compact_spouses(family: family_model.Family, rows: list, people: dict,
		parents: dict, ranks: dict, x: dict) -> dict:
	"""Keep spouse reversals that reduce width or row spans without collisions."""
	component = family_model.Family(tuple(people[pid] for pid in x),
		tuple(union for union in family.unions if union.father in x))
	blocks = [block for row in rows for block in row
		if len(block) == 2 and sum(pid in parents for pid in block) == 1]

	def width(positions: dict) -> float:
		result = max(positions[p] + _half_width(people[p]) for p in positions)
		result -= min(positions[p] - _half_width(people[p]) for p in positions)
		return result

	def extent(positions: dict) -> tuple:
		spans = sum(max(positions[p] for block in row for p in block)
			- min(positions[p] for block in row for p in block) for row in rows)
		spans += sum(abs(positions[u.father] - positions[u.mother])
			for u in component.unions)
		return round(width(positions), 6), round(spans, 6)

	changed = True
	while changed:
		changed = False
		for block in blocks:
			block.reverse()
			candidate = _align_family(family, rows, people, parents)
			if extent(candidate) < extent(x):
				symbols = {pid: Symbol(pid, candidate[pid], ranks[pid] * GENERATION_GAP,
					people[pid].sex, people[pid].label) for pid in candidate}
				diagram = Diagram(tuple(symbols.values()), _segments(component, symbols),
					width(candidate), (max(ranks[p] for p in candidate) + 1) * GENERATION_GAP)
				if not layout_errors(diagram):
					x = candidate
					changed = True
					continue
			block.reverse()
	return x


#============================================
def _align_family(family: family_model.Family, rows: list, people: dict,
		parents: dict) -> dict:
	"""Place generations together with centered descent and compact rows and couples."""
	ids = [pid for row in rows for block in row for pid in block]
	indices = {pid: index for index, pid in enumerate(ids)}
	objective = [0.0] * len(ids)
	separations, distances, equalities = [], [], []
	for row in rows:
		ordered = [pid for block in row for pid in block]
		blocks = {pid: block for block in row for pid in block}
		objective[indices[ordered[0]]] -= 1
		objective[indices[ordered[-1]]] += 1
		for left, right in zip(ordered, ordered[1:]):
			constraint = [0.0] * len(ids)
			constraint[indices[left]], constraint[indices[right]] = 1, -1
			partners = blocks[left] == blocks[right]
			if partners:
				# Penalize stretched marriage lines as well as wide rows.
				objective[indices[left]] -= 1
				objective[indices[right]] += 1
			gap = SIBLING_GAP if partners else _gap(blocks[left], blocks[right], parents)
			separations.append(constraint)
			distances.append(-(_half_width(people[left]) + _half_width(people[right]) + gap))
	for union in family.unions:
		if union.father not in indices or not union.children:
			continue
		# Use the outer children's positions, not spouses or the sibship's mean.
		children = sorted(union.children, key=indices.__getitem__)
		constraint = [0.0] * len(ids)
		for pid in (union.father, union.mother):
			constraint[indices[pid]] += 1
		for pid in (children[0], children[-1]):
			constraint[indices[pid]] -= 1
		equalities.append(constraint)
	# Keep drawing coordinates nonnegative; no coordinates enter the family model.
	solution = scipy.optimize.linprog(objective,
		A_ub=separations or None, b_ub=distances or None,
		A_eq=equalities or None, b_eq=[0.0] * len(equalities) or None,
		method='highs')
	if not solution.success:
		raise ValueError(f'Cannot align this family order: {solution.message}')
	result = {pid: round(float(solution.x[index]), 8) for pid, index in indices.items()}
	return result


#============================================
def _segments(family: family_model.Family, symbols: dict) -> tuple[Segment, ...]:
	lines = []

	def add(x1: float, y1: float, x2: float, y2: float, index: int) -> None:
		if (x1, y1) != (x2, y2):
			lines.append(Segment(x1, y1, x2, y2, index))

	for index, union in enumerate(family.unions):
		a, b = sorted((symbols[union.father], symbols[union.mother]), key=lambda p: p.x)
		midpoint = (a.x + b.x) / 2
		consanguineous = bool(family.ancestors(a.person) & family.ancestors(b.person))
		for offset in (-3, 3) if consanguineous else (0,):
			add(a.x + RADIUS, a.y + offset, b.x - RADIUS, b.y + offset, index)
		if not union.children:
			continue
		children = [symbols[pid] for pid in union.children]
		center = (min(child.x for child in children) + max(child.x for child in children)) / 2
		# Permit only subpixel solver noise, never a visibly shifted descent line.
		if len(children) <= 2 and abs(center - midpoint) > 1e-6:
			raise ValueError('Offspring must be centered below the marriage midpoint')
		if len(children) == 1:
			child = children[0]
			add(midpoint, a.y + (3 if consanguineous else 0),
				midpoint, child.y - RADIUS, index)
			continue
		# Leave room below parent labels and a short, clear drop to each child.
		bar_y = children[0].y - 36
		add(midpoint, a.y + (3 if consanguineous else 0), midpoint, bar_y, index)
		left = min(midpoint, *(p.x for p in children))
		right = max(midpoint, *(p.x for p in children))
		add(left, bar_y, right, bar_y, index)
		for child in children:
			add(child.x, bar_y, child.x, child.y - RADIUS, index)
	return tuple(lines)


#============================================
def lay_out(family: family_model.Family, mirror: bool = False) -> Diagram:
	"""Place each person once, including shared descendants and separate families.

	Args:
		family: People and unions with optional child ordering.
		mirror: Reflect all X coordinates without changing relationships.

	Returns:
		Geometry for both renderers; layout_errors must still check readability.

	Raises:
		ValueError: Invalid family structure or an order that cannot be aligned.
	"""
	ranks = family.generations()
	people = family.members()
	symbols = {}
	cursor = 28
	for component in graphs.components(family):
		x = _positions(family, component, ranks)
		left = min(x[pid] - _half_width(people[pid]) for pid in component)
		for pid in component:
			person = people[pid]
			symbols[pid] = Symbol(pid, x[pid] - left + cursor,
				28 + ranks[pid] * GENERATION_GAP, person.sex, person.label)
		cursor += max(x[pid] + _half_width(people[pid]) for pid in component) - left + 80
	width = cursor - 52
	if mirror:
		symbols = {pid: dataclasses.replace(p, x=width - p.x) for pid, p in symbols.items()}
	ordered = tuple(symbols[person.id] for person in family.people)
	result = Diagram(ordered, _segments(family, symbols), width,
		max(p.y + (48 if p.label else 28) for p in ordered))
	return result


#============================================
def _intersection(a: Segment, b: Segment) -> bool:
	"""Axis-aligned inclusive intersection, including collinear overlaps."""
	x_overlap = max(min(a.x1, a.x2), min(b.x1, b.x2)) <= min(max(a.x1, a.x2), max(b.x1, b.x2))
	y_overlap = max(min(a.y1, a.y2), min(b.y1, b.y2)) <= min(max(a.y1, a.y2), max(b.y1, b.y2))
	return x_overlap and y_overlap


#============================================
def layout_errors(diagram: Diagram) -> tuple[str, ...]:
	"""Check geometry for obscured people, labels, or ambiguous connectors.

	Args:
		diagram: Positioned symbols and relationship segments.

	Returns:
		Readability failures, or an empty tuple for acceptable geometry.
	"""
	errors = []
	for a, b in itertools.combinations(diagram.symbols, 2):
		aw = max(RADIUS, len(a.label) * 4.5)
		bw = max(RADIUS, len(b.label) * 4.5)
		if abs(a.x - b.x) < aw + bw + 8 and abs(a.y - b.y) < 54:
			errors.append(f'Overlapping people or labels: {a.person}, {b.person}')
	for a, b in itertools.combinations(diagram.segments, 2):
		if a.union != b.union and _intersection(a, b):
			errors.append(f'Ambiguous relationship intersection: {a.union}, {b.union}')
	for line in diagram.segments:
		for person in diagram.symbols:
			# Open symbol bounds permit intended relationship endpoints at their edges.
			if (max(line.x1, line.x2) > person.x - RADIUS + 0.1
				and min(line.x1, line.x2) < person.x + RADIUS - 0.1
				and max(line.y1, line.y2) > person.y - RADIUS + 0.1
				and min(line.y1, line.y2) < person.y + RADIUS - 0.1):
				errors.append(f'Line passes through person: {person.person}')
			if person.label:
				if (max(line.x1, line.x2) > person.x - len(person.label) * 4.5
					and min(line.x1, line.x2) < person.x + len(person.label) * 4.5
					and max(line.y1, line.y2) > person.y + 20
					and min(line.y1, line.y2) < person.y + 38):
					errors.append(f'Line passes through label: {person.person}')
	return tuple(dict.fromkeys(errors))
