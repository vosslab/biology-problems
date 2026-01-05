#!/usr/bin/env python3

# Standard Library
import dataclasses
import random

# Local repo modules
import graph_spec




#===============================
@dataclasses.dataclass
class Individual:
	id: str
	sex: str
	phenotype: str
	generation: int
	father_id: str | None = None
	mother_id: str | None = None
	slot: int | None = None


#===============================
@dataclasses.dataclass
class Couple:
	id: str
	partner_a: str
	partner_b: str
	generation: int
	children: list[str]


#===============================
@dataclasses.dataclass
class PedigreeGraph:
	individuals: dict[str, Individual]
	couples: list[Couple]
	generations: int
	starting_couples: int


#===============================
def _new_id(prefix: str, counter: int) -> str:
	identifier = f"{prefix}{counter:03d}"
	return identifier


#===============================
def generate_pedigree_graph(
	mode: str,
	generations: int = 4,
	starting_couples: int = 1,
	rng: random.Random | None = None,
	min_children: int = 2,
	max_children: int = 4,
	marry_in_rate: float = 0.7,
	show_carriers: bool = False,
) -> PedigreeGraph:
	"""
	Generate a pedigree graph with randomized structure.
	"""
	if rng is None:
		rng = random.Random()
	import inheritance_assign
	import skeleton
	graph = skeleton.generate_skeleton_graph(
		generations=generations,
		starting_couples=starting_couples,
		rng=rng,
		min_children=min_children,
		max_children=max_children,
		marry_in_rate=marry_in_rate,
	)
	inheritance_assign.assign_phenotypes(graph, mode, rng, show_carriers)
	return graph


#===============================
def _trim_graph_to_limit(graph: PedigreeGraph, max_people: int) -> PedigreeGraph:
	ordered = sorted(graph.individuals.values(), key=lambda ind: (ind.generation, ind.id))
	keep_ids = {ind.id for ind in ordered[:max_people]}
	if len(keep_ids) == len(graph.individuals):
		return graph

	individuals = {pid: ind for pid, ind in graph.individuals.items() if pid in keep_ids}
	couples: list[Couple] = []
	for couple in graph.couples:
		if couple.partner_a not in keep_ids or couple.partner_b not in keep_ids:
			continue
		children = [child_id for child_id in couple.children if child_id in keep_ids]
		couples.append(Couple(
			id=couple.id,
			partner_a=couple.partner_a,
			partner_b=couple.partner_b,
			generation=couple.generation,
			children=children,
		))

	for person_id, person in individuals.items():
		if person.father_id and person.father_id not in keep_ids:
			person.father_id = None
		if person.mother_id and person.mother_id not in keep_ids:
			person.mother_id = None

	graph = PedigreeGraph(
		individuals=individuals,
		couples=couples,
		generations=graph.generations,
		starting_couples=graph.starting_couples,
	)
	return graph


#===============================
def _assign_slots(graph: PedigreeGraph) -> int:
	SIB_GAP = 1
	COMPONENT_GUTTER = 3

	couples_by_id = {couple.id: couple for couple in graph.couples}
	partner_to_couple: dict[str, str] = {}
	for couple in graph.couples:
		partner_to_couple[couple.partner_a] = couple.id
		partner_to_couple[couple.partner_b] = couple.id

	width_cache: dict[str, int] = {}

	def _measure_child_width(child_id: str) -> int:
		couple_id = partner_to_couple.get(child_id)
		if couple_id is None:
			return 1
		return _measure_couple_width(couple_id)

	def _measure_couple_width(couple_id: str) -> int:
		if couple_id in width_cache:
			return width_cache[couple_id]
		couple = couples_by_id[couple_id]
		children = list(couple.children)
		if not children:
			width_cache[couple_id] = 3
			return 3
		child_widths = [_measure_child_width(child_id) for child_id in children]
		child_block_width = sum(child_widths) + SIB_GAP * (len(child_widths) - 1)
		width_cache[couple_id] = max(3, child_block_width)
		return width_cache[couple_id]

	placed_couples: set[str] = set()

	def _place_couple(couple_id: str, left_slot: int) -> None:
		if couple_id in placed_couples:
			return
		placed_couples.add(couple_id)
		couple = couples_by_id[couple_id]
		children = list(couple.children)
		couple_width = width_cache.get(couple_id, 2)
		if children:
			child_widths = [_measure_child_width(child_id) for child_id in children]
			child_block_width = sum(child_widths) + SIB_GAP * (len(child_widths) - 1)
			block_left = left_slot + (couple_width - child_block_width) // 2
			cursor = block_left
			for child_id, child_width in zip(children, child_widths):
				child_couple_id = partner_to_couple.get(child_id)
				if child_couple_id is None:
					graph.individuals[child_id].slot = cursor
				else:
					_place_couple(child_couple_id, cursor)
				cursor += child_width + SIB_GAP
			child_slots = [
				graph.individuals[child_id].slot
				for child_id in children
				if graph.individuals[child_id].slot is not None
			]
			if child_slots:
				mid_slot = (min(child_slots) + max(child_slots)) // 2
			else:
				mid_slot = block_left + child_block_width // 2
		else:
			mid_slot = left_slot + couple_width // 2

		partner_a = graph.individuals[couple.partner_a]
		partner_b = graph.individuals[couple.partner_b]
		left_id = couple.partner_a
		right_id = couple.partner_b
		if partner_a.sex == 'female' and partner_b.sex == 'male':
			left_id, right_id = right_id, left_id
		graph.individuals[left_id].slot = mid_slot - 1
		graph.individuals[right_id].slot = mid_slot + 1

	root_couples = [c for c in graph.couples if c.generation == 1]
	root_couples.sort(key=lambda couple: (couple.partner_a, couple.partner_b))
	for couple in root_couples:
		_measure_couple_width(couple.id)

	left_cursor = 0
	for couple in root_couples:
		_place_couple(couple.id, left_cursor)
		left_cursor += width_cache[couple.id] + COMPONENT_GUTTER

	max_slot = 0
	for ind in graph.individuals.values():
		if ind.slot is None:
			continue
		max_slot = max(max_slot, ind.slot)
	return max_slot


#===============================
def _phenotype_to_char(ind: Individual, show_carriers: bool) -> str:
	if ind.phenotype == 'affected':
		return 'x' if ind.sex == 'male' else '*'
	if ind.phenotype == 'carrier' and show_carriers:
		return '[' if ind.sex == 'male' else '('
	return '#' if ind.sex == 'male' else 'o'


#===============================
def _sort_by_id(item: Individual) -> str:
	return item.id


#===============================
def _slot_to_col(slot: int, col_shift: int) -> int:
	col = slot + col_shift
	return col


#===============================
def _compute_col_shift(graph: PedigreeGraph, min_slot: int, max_slot: int) -> int:
	top_couples = [c for c in graph.couples if c.generation == 1]
	if not top_couples:
		return 0
	top_couples.sort(key=lambda couple: couple.id)
	top_couple = top_couples[0]
	partner_a = graph.individuals[top_couple.partner_a]
	partner_b = graph.individuals[top_couple.partner_b]
	top_mid_col = ((partner_a.slot or 0) + (partner_b.slot or 0)) // 2
	col_min = min_slot
	col_max = max_slot
	current_center = (col_min + col_max) // 2
	col_shift = current_center - top_mid_col
	min_shifted = col_min + col_shift
	if min_shifted < 0:
		col_shift += -min_shifted
	return col_shift


#===============================
def _edges_to_char(edges: dict[str, bool]) -> str:
	key = ''.join(['1' if edges.get(k, False) else '0' for k in ['u', 'd', 'l', 'r']])
	edge_map = {
		'0011': '-',
		'1100': '|',
		'0111': 'T',
		'1011': '^',
		'0101': 'r',
		'0110': 'd',
		'1001': 'L',
		'1010': 'u',
		'1111': '+',
	}
	char = edge_map.get(key, '+')
	return char


#===============================
def render_graph_to_code(graph: PedigreeGraph, show_carriers: bool = False) -> str:
	_assign_slots(graph)
	min_slot = min(ind.slot for ind in graph.individuals.values() if ind.slot is not None)
	max_slot = max(ind.slot for ind in graph.individuals.values() if ind.slot is not None)
	col_shift = _compute_col_shift(graph, min_slot, max_slot)
	num_rows = graph.generations * 2 - 1
	num_cols = max(3, max_slot + col_shift + 1)

	grid = [['.' for _ in range(num_cols)] for _ in range(num_rows)]
	edge_cells: dict[tuple[int, int], dict[str, bool]] = {}

	for ind in graph.individuals.values():
		row = (ind.generation - 1) * 2
		col = _slot_to_col(ind.slot or 0, col_shift)
		grid[row][col] = _phenotype_to_char(ind, show_carriers)

	for couple in graph.couples:
		partner_a = graph.individuals[couple.partner_a]
		partner_b = graph.individuals[couple.partner_b]
		row = (couple.generation - 1) * 2
		col_left = _slot_to_col(min(partner_a.slot or 0, partner_b.slot or 0), col_shift)
		col_right = _slot_to_col(max(partner_a.slot or 0, partner_b.slot or 0), col_shift)
		mid_col = (col_left + col_right) // 2
		if col_left + 1 <= col_right - 1:
			for col in range(col_left + 1, col_right):
				edge_cells.setdefault((row, col), {}).update({'l': True, 'r': True})
		if 0 <= row < num_rows and 0 <= mid_col < num_cols:
			grid[row][mid_col] = 'T'

		if not couple.children:
			continue
		edge_cells.setdefault((row, mid_col), {}).update({'l': True, 'r': True, 'd': True})
		connector_row = row + 1
		child_cols = []
		for child_id in couple.children:
			child = graph.individuals[child_id]
			child_cols.append(_slot_to_col(child.slot or 0, col_shift))
		if not child_cols:
			continue
		min_col = min(child_cols)
		max_col = max(child_cols)
		if len(child_cols) > 1:
			for col in range(min_col, max_col + 1):
				edges: dict[str, bool] = {}
				if col == min_col:
					edges['r'] = True
				elif col == max_col:
					edges['l'] = True
				else:
					edges['l'] = True
					edges['r'] = True
				edge_cells.setdefault((connector_row, col), {}).update(edges)
		edge_cells.setdefault((connector_row, mid_col), {}).update({'u': True})
		for col in child_cols:
			edge_cells.setdefault((connector_row, col), {}).update({'d': True})
			if col == mid_col:
				edge_cells.setdefault((connector_row, col), {}).update({'u': True})

	for (row, col), edges in edge_cells.items():
		if row < 0 or row >= num_rows or col < 0 or col >= num_cols:
			continue
		if grid[row][col] == '.':
			grid[row][col] = _edges_to_char(edges)

	code_lines: list[str] = []
	for row in grid:
		line = ''.join(row).rstrip('.')
		if not line:
			line = '.'
		code_lines.append(line)
	code_string = '%'.join(code_lines)
	return code_string


#===============================
def _graph_to_graph_spec(graph: PedigreeGraph, include_carriers: bool) -> graph_spec.PedigreeGraphSpec:
	people: dict[str, graph_spec.IndividualIR] = {}
	unions: list[graph_spec.UnionIR] = []

	main_couple_ids: tuple[str, str] | None = None
	main_couple_people: tuple[str, str] | None = None
	if graph.starting_couples == 1:
		founder_couples = [c for c in graph.couples if c.generation == 1]
		if founder_couples:
			founder_couples.sort(key=lambda couple: couple.id)
			founder = founder_couples[0]
			partner_a = graph.individuals[founder.partner_a]
			partner_b = graph.individuals[founder.partner_b]
			if partner_a.sex == 'female':
				female = partner_a
				male = partner_b
			else:
				female = partner_b
				male = partner_a
			main_couple_ids = ('A', 'B')
			main_couple_people = (female.id, male.id)

	referenced_ids: set[str] = set()
	for couple in graph.couples:
		if not couple.children:
			continue
		referenced_ids.add(couple.partner_a)
		referenced_ids.add(couple.partner_b)
		referenced_ids.update(couple.children)
	if main_couple_people is not None:
		referenced_ids.update(main_couple_people)

	individuals_sorted = sorted(
		[ind for ind in graph.individuals.values() if ind.id in referenced_ids],
		key=lambda ind: (ind.generation, ind.id),
	)
	if len(individuals_sorted) > 26:
		raise ValueError("Graph spec supports up to 26 individuals (single-letter IDs).")
	letter_ids = [chr(ord('A') + idx) for idx in range(len(individuals_sorted))]
	id_map: dict[str, str] = {}
	if main_couple_people is not None:
		id_map[main_couple_people[0]] = 'A'
		id_map[main_couple_people[1]] = 'B'

	next_letter_index = 0
	for letter in letter_ids:
		if letter in ('A', 'B') and graph.starting_couples == 1:
			continue
		while next_letter_index < len(individuals_sorted) and individuals_sorted[next_letter_index].id in id_map:
			next_letter_index += 1
		if next_letter_index >= len(individuals_sorted):
			break
		id_map[individuals_sorted[next_letter_index].id] = letter
		next_letter_index += 1

	for individual in individuals_sorted:
		status = None
		if individual.phenotype == 'affected':
			status = 'infected'
		elif individual.phenotype == 'carrier' and include_carriers:
			status = 'carrier'
		people[id_map[individual.id]] = graph_spec.IndividualIR(
			person_id=id_map[individual.id],
			sex=individual.sex,
			status=status,
		)

	for couple in graph.couples:
		if not couple.children:
			continue
		unions.append(graph_spec.UnionIR(
			partner_a=id_map[couple.partner_a],
			partner_b=id_map[couple.partner_b],
			children=[id_map[child_id] for child_id in couple.children],
		))

	return graph_spec.PedigreeGraphSpec(people=people, unions=unions, main_couple=main_couple_ids)


#===============================
def generate_pedigree_graph_spec(
	mode: str,
	generations: int = 4,
	starting_couples: int = 1,
	rng: random.Random | None = None,
	min_children: int = 2,
	max_children: int = 4,
	marry_in_rate: float = 0.7,
	show_carriers: bool = False,
) -> str:
	"""
	Generate a pedigree graph spec string from a graph-based generator.
	"""
	max_people = 26
	graph = generate_pedigree_graph(
		mode,
		generations=generations,
		starting_couples=starting_couples,
		rng=rng,
		min_children=min_children,
		max_children=max_children,
		marry_in_rate=marry_in_rate,
		show_carriers=show_carriers,
	)
	graph = _trim_graph_to_limit(graph, max_people)
	spec = _graph_to_graph_spec(graph, include_carriers=show_carriers)
	return graph_spec.format_pedigree_graph_spec(spec)


#===============================
def _assign_generations_from_unions(spec: graph_spec.PedigreeGraphSpec) -> dict[str, int]:
	child_ids = set()
	partner_ids = set()
	for union in spec.unions:
		child_ids.update(union.children)
		partner_ids.add(union.partner_a)
		partner_ids.add(union.partner_b)
	generations: dict[str, int] = {}

	for union in spec.unions:
		if union.partner_a in child_ids or union.partner_b in child_ids:
			continue
		generations[union.partner_a] = 1
		generations[union.partner_b] = 1

	for person_id in spec.people:
		if person_id in child_ids:
			continue
		if person_id in partner_ids:
			continue
		generations[person_id] = 1

	if not generations:
		raise ValueError('No founders detected in graph spec.')

	progress = True
	while progress:
		progress = False
		for union in spec.unions:
			parent_a = union.partner_a
			parent_b = union.partner_b
			if parent_a in generations and parent_b not in generations:
				generations[parent_b] = generations[parent_a]
				progress = True
			if parent_b in generations and parent_a not in generations:
				generations[parent_a] = generations[parent_b]
				progress = True
			if parent_a not in generations or parent_b not in generations:
				continue
			parent_gen = max(generations[parent_a], generations[parent_b])
			for child_id in union.children:
				child_gen = parent_gen + 1
				if child_id in generations and generations[child_id] != child_gen:
					raise ValueError(f"Inconsistent generation for '{child_id}'.")
				if child_id not in generations:
					generations[child_id] = child_gen
					progress = True

	missing = [pid for pid in spec.people if pid not in generations]
	if missing:
		raise ValueError(f"Unassigned generations for: {', '.join(sorted(missing))}.")
	return generations


#===============================
def parse_graph_spec_to_graph(spec_string: str) -> PedigreeGraph:
	"""
	Parse a pedigree graph spec string into an internal PedigreeGraph.
	"""
	spec = graph_spec.parse_pedigree_graph_spec(spec_string)
	generations = _assign_generations_from_unions(spec)

	individuals: dict[str, Individual] = {}
	for person_id, person in spec.people.items():
		phenotype = 'unaffected'
		if person.status == 'infected':
			phenotype = 'affected'
		elif person.status == 'carrier':
			phenotype = 'carrier'
		individuals[person_id] = Individual(
			id=person_id,
			sex=person.sex or 'unknown',
			phenotype=phenotype,
			generation=generations[person_id],
		)

	couples: list[Couple] = []
	for union in spec.unions:
		partner_a = individuals[union.partner_a]
		partner_b = individuals[union.partner_b]
		if partner_a.sex == partner_b.sex:
			raise ValueError(f"Union partners must be opposite sex: {union.partner_a}-{union.partner_b}")
		if partner_a.sex == 'female' and partner_b.sex == 'male':
			partner_a_id = union.partner_b
			partner_b_id = union.partner_a
		else:
			partner_a_id = union.partner_a
			partner_b_id = union.partner_b
		couple = Couple(
			id=f"C_{partner_a_id}_{partner_b_id}",
			partner_a=partner_a_id,
			partner_b=partner_b_id,
			generation=generations[partner_a_id],
			children=list(union.children),
		)
		for child_id in union.children:
			individuals[child_id].father_id = couple.partner_a
			individuals[child_id].mother_id = couple.partner_b
		couples.append(couple)

	graph = PedigreeGraph(
		individuals=individuals,
		couples=couples,
		generations=max(generations.values()),
		starting_couples=0,
	)
	return graph


#===============================
def compile_graph_spec_to_code(spec_string: str, show_carriers: bool = True) -> str:
	"""
	Compile a pedigree graph spec string to a pedigree code string.
	"""
	graph = parse_graph_spec_to_graph(spec_string)
	code_string = render_graph_to_code(graph, show_carriers=show_carriers)
	return code_string


#===============================
#===============================
if __name__ == '__main__':
	default_rng = random.Random(7)
	spec_string = generate_pedigree_graph_spec('autosomal recessive', rng=default_rng)
	print(spec_string)

## THE END
