#!/usr/bin/env python3

# Standard Library
import dataclasses
import random




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
def _make_founder_couples(starting_couples: int, rng: random.Random) -> tuple[dict[str, Individual], list[Couple]]:
	individuals: dict[str, Individual] = {}
	couples: list[Couple] = []
	person_counter = 1
	couple_counter = 1
	for _ in range(starting_couples):
		male_id = _new_id('M', person_counter)
		person_counter += 1
		female_id = _new_id('F', person_counter)
		person_counter += 1
		individuals[male_id] = Individual(
			id=male_id,
			sex='male',
			phenotype='unaffected',
			generation=1,
		)
		individuals[female_id] = Individual(
			id=female_id,
			sex='female',
			phenotype='unaffected',
			generation=1,
		)
		couple_id = _new_id('C', couple_counter)
		couple_counter += 1
		couples.append(Couple(
			id=couple_id,
			partner_a=male_id,
			partner_b=female_id,
			generation=1,
			children=[],
		))
	return individuals, couples


#===============================
def _add_children(
	individuals: dict[str, Individual],
	couples: list[Couple],
	generation: int,
	person_counter: int,
	rng: random.Random,
	min_children: int,
	max_children: int,
) -> tuple[list[str], int]:
	children_ids: list[str] = []
	for couple in [c for c in couples if c.generation == generation]:
		num_children = rng.randint(min_children, max_children)
		for _ in range(num_children):
			sex = rng.choice(['male', 'female'])
			child_id = _new_id('P', person_counter)
			person_counter += 1
			individuals[child_id] = Individual(
				id=child_id,
				sex=sex,
				phenotype='unaffected',
				generation=generation + 1,
				father_id=couple.partner_a,
				mother_id=couple.partner_b,
			)
			couple.children.append(child_id)
			children_ids.append(child_id)
	return children_ids, person_counter


#===============================
def _pair_children(
	individuals: dict[str, Individual],
	children_ids: list[str],
	generation: int,
	person_counter: int,
	couple_counter: int,
	rng: random.Random,
	marry_in_rate: float,
) -> tuple[list[Couple], int, int]:
	new_couples: list[Couple] = []
	for child_id in children_ids:
		if rng.random() > marry_in_rate:
			continue
		child = individuals[child_id]
		spouse_sex = 'female' if child.sex == 'male' else 'male'
		spouse_id = _new_id('S', person_counter)
		person_counter += 1
		individuals[spouse_id] = Individual(
			id=spouse_id,
			sex=spouse_sex,
			phenotype='unaffected',
			generation=generation,
		)
		couple_id = _new_id('C', couple_counter)
		couple_counter += 1
		if child.sex == 'male':
			partner_a = child_id
			partner_b = spouse_id
		else:
			partner_a = spouse_id
			partner_b = child_id
		new_couples.append(Couple(
			id=couple_id,
			partner_a=partner_a,
			partner_b=partner_b,
			generation=generation,
			children=[],
		))
	return new_couples, person_counter, couple_counter


#===============================
def _assign_autosomal_dominant(graph: PedigreeGraph, rng: random.Random) -> None:
	founders = [ind for ind in graph.individuals.values() if ind.generation == 1]
	affected_founder = rng.choice(founders)
	affected_founder.phenotype = 'affected'
	for couple in graph.couples:
		parent_a = graph.individuals[couple.partner_a]
		parent_b = graph.individuals[couple.partner_b]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			inherit_a = parent_a.phenotype == 'affected' and rng.random() < 0.5
			inherit_b = parent_b.phenotype == 'affected' and rng.random() < 0.5
			child.phenotype = 'affected' if (inherit_a or inherit_b) else 'unaffected'


#===============================
def _assign_autosomal_recessive(graph: PedigreeGraph, rng: random.Random, show_carriers: bool) -> None:
	for ind in graph.individuals.values():
		if ind.generation == 1:
			if rng.random() < 0.6:
				ind.phenotype = 'carrier' if show_carriers else 'unaffected'
			else:
				ind.phenotype = 'unaffected'
	for couple in graph.couples:
		parent_a = graph.individuals[couple.partner_a]
		parent_b = graph.individuals[couple.partner_b]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			parent_a_carrier = parent_a.phenotype in ('carrier', 'affected')
			parent_b_carrier = parent_b.phenotype in ('carrier', 'affected')
			if parent_a_carrier and parent_b_carrier and rng.random() < 0.25:
				child.phenotype = 'affected'
			elif parent_a_carrier or parent_b_carrier:
				child.phenotype = 'carrier' if show_carriers else 'unaffected'
			else:
				child.phenotype = 'unaffected'


#===============================
def _assign_x_linked_recessive(graph: PedigreeGraph, rng: random.Random, show_carriers: bool) -> None:
	for ind in graph.individuals.values():
		if ind.generation == 1:
			if ind.sex == 'female' and rng.random() < 0.4:
				ind.phenotype = 'carrier' if show_carriers else 'unaffected'
			elif ind.sex == 'male' and rng.random() < 0.2:
				ind.phenotype = 'affected'
	for couple in graph.couples:
		mother = graph.individuals[couple.partner_b]
		father = graph.individuals[couple.partner_a]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			if child.sex == 'male':
				if mother.phenotype in ('carrier', 'affected') and rng.random() < 0.5:
					child.phenotype = 'affected'
				else:
					child.phenotype = 'unaffected'
			else:
				if father.phenotype == 'affected' and mother.phenotype in ('carrier', 'affected'):
					child.phenotype = 'affected' if rng.random() < 0.5 else ('carrier' if show_carriers else 'unaffected')
				elif mother.phenotype in ('carrier', 'affected') and rng.random() < 0.5:
					child.phenotype = 'carrier' if show_carriers else 'unaffected'
				else:
					child.phenotype = 'unaffected'


#===============================
def _assign_y_linked(graph: PedigreeGraph, rng: random.Random) -> None:
	founder_males = [ind for ind in graph.individuals.values() if ind.generation == 1 and ind.sex == 'male']
	if founder_males:
		rng.choice(founder_males).phenotype = 'affected'
	for couple in graph.couples:
		father = graph.individuals[couple.partner_a]
		for child_id in couple.children:
			child = graph.individuals[child_id]
			if child.sex == 'male' and father.phenotype == 'affected':
				child.phenotype = 'affected'


#===============================
def assign_phenotypes(graph: PedigreeGraph, mode: str, rng: random.Random, show_carriers: bool) -> None:
	mode_value = mode.strip().lower()
	if mode_value in ('autosomal dominant', 'ad'):
		_assign_autosomal_dominant(graph, rng)
	elif mode_value in ('autosomal recessive', 'ar'):
		_assign_autosomal_recessive(graph, rng, show_carriers)
	elif mode_value in ('x-linked recessive', 'xr'):
		_assign_x_linked_recessive(graph, rng, show_carriers)
	elif mode_value in ('y-linked', 'yl'):
		_assign_y_linked(graph, rng)


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
	individuals, couples = _make_founder_couples(starting_couples, rng)
	person_counter = len(individuals) + 1
	couple_counter = len(couples) + 1
	for gen in range(1, generations):
		children_ids, person_counter = _add_children(
			individuals,
			couples,
			gen,
			person_counter,
			rng,
			min_children,
			max_children,
		)
		if gen + 1 > generations:
			continue
		new_couples, person_counter, couple_counter = _pair_children(
			individuals,
			children_ids,
			gen + 1,
			person_counter,
			couple_counter,
			rng,
			marry_in_rate,
		)
		couples.extend(new_couples)
	graph = PedigreeGraph(
		individuals=individuals,
		couples=couples,
		generations=generations,
		starting_couples=starting_couples,
	)
	assign_phenotypes(graph, mode, rng, show_carriers)
	return graph


#===============================
def _assign_slots(graph: PedigreeGraph) -> int:
	max_slots = 0
	for gen in range(1, graph.generations + 1):
		gen_couples = [c for c in graph.couples if c.generation == gen]
		gen_individuals = [i for i in graph.individuals.values() if i.generation == gen]
		couple_ids = {c.partner_a for c in gen_couples} | {c.partner_b for c in gen_couples}
		unpaired = [i for i in gen_individuals if i.id not in couple_ids]
		unpaired.sort(key=_sort_by_id)
		slot_cursor = 0
		for couple in gen_couples:
			graph.individuals[couple.partner_a].slot = slot_cursor
			graph.individuals[couple.partner_b].slot = slot_cursor + 1
			slot_cursor += 3
		for single in unpaired:
			graph.individuals[single.id].slot = slot_cursor
			slot_cursor += 2
		max_slots = max(max_slots, slot_cursor)
	return max_slots


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
	max_slots = _assign_slots(graph)
	num_rows = graph.generations * 2 - 1
	num_cols = max(3, max_slots * 2 - 1)

	grid = [['.' for _ in range(num_cols)] for _ in range(num_rows)]
	edge_cells: dict[tuple[int, int], dict[str, bool]] = {}

	for ind in graph.individuals.values():
		row = (ind.generation - 1) * 2
		col = (ind.slot or 0) * 2
		grid[row][col] = _phenotype_to_char(ind, show_carriers)

	for couple in graph.couples:
		partner_a = graph.individuals[couple.partner_a]
		partner_b = graph.individuals[couple.partner_b]
		row = (couple.generation - 1) * 2
		col_left = min(partner_a.slot or 0, partner_b.slot or 0) * 2
		col_right = max(partner_a.slot or 0, partner_b.slot or 0) * 2
		mid_col = (col_left + col_right) // 2
		if col_left + 1 <= col_right - 1:
			for col in range(col_left + 1, col_right):
				edge_cells.setdefault((row, col), {}).update({'l': True, 'r': True})

		if not couple.children:
			continue
		child_row = row + 2
		connector_row = row + 1
		child_cols = []
		for child_id in couple.children:
			child = graph.individuals[child_id]
			child_cols.append((child.slot or 0) * 2)
		if not child_cols:
			continue
		min_col = min(child_cols)
		max_col = max(child_cols)
		for col in range(min_col, max_col + 1):
			if col % 2 == 1 or col == min_col or col == max_col:
				edge_cells.setdefault((connector_row, col), {}).update({'l': True, 'r': True})
		edge_cells.setdefault((connector_row, mid_col), {}).update({'u': True, 'd': True})
		for col in child_cols:
			edge_cells.setdefault((connector_row, col), {}).update({'u': True, 'd': True})
			if child_row < num_rows:
				edge_cells.setdefault((child_row - 1, col), {}).update({'u': True, 'd': True})

	for (row, col), edges in edge_cells.items():
		if row < 0 or row >= num_rows or col < 0 or col >= num_cols:
			continue
		if grid[row][col] == '.':
			grid[row][col] = _edges_to_char(edges)

	code_lines = [''.join(row).rstrip('.') for row in grid]
	code_string = '%'.join(line for line in code_lines if line)
	return code_string


#===============================
def generate_pedigree_code(
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
	Generate a pedigree code string from a graph-based generator.
	"""
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
	code_string = render_graph_to_code(graph, show_carriers=show_carriers)
	return code_string


#===============================
#===============================
if __name__ == '__main__':
	default_rng = random.Random(7)
	code_string = generate_pedigree_code('autosomal recessive', rng=default_rng)
	print(code_string)

## THE END
