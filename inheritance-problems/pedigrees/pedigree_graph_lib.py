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
	import pedigree_inheritance_lib
	import pedigree_skeleton_lib
	graph = pedigree_skeleton_lib.generate_skeleton_graph(
		generations=generations,
		starting_couples=starting_couples,
		rng=rng,
		min_children=min_children,
		max_children=max_children,
		marry_in_rate=marry_in_rate,
	)
	pedigree_inheritance_lib.assign_phenotypes(graph, mode, rng, show_carriers)
	return graph


#===============================
def _assign_slots(graph: PedigreeGraph) -> int:
	max_slots = 0
	parent_index: dict[str, int] = {}
	for gen in range(1, graph.generations + 1):
		gen_couples = [c for c in graph.couples if c.generation == gen]
		def couple_key(couple: Couple) -> tuple[int, str]:
			index_a = parent_index.get(couple.partner_a, 0)
			index_b = parent_index.get(couple.partner_b, 0)
			return (min(index_a, index_b), couple.id)

		gen_couples.sort(key=couple_key)
		gen_individuals = [i for i in graph.individuals.values() if i.generation == gen]
		couple_ids = {c.partner_a for c in gen_couples} | {c.partner_b for c in gen_couples}
		unpaired = [i for i in gen_individuals if i.id not in couple_ids]
		unpaired.sort(key=lambda ind: (parent_index.get(ind.id, 0), ind.id))

		units: list[tuple[tuple[int, str], str, Individual | Couple]] = []
		for couple in gen_couples:
			units.append((couple_key(couple), 'couple', couple))
		for single in unpaired:
			units.append(((parent_index.get(single.id, 0), single.id), 'single', single))
		units.sort(key=lambda item: item[0])

		slot_cursor = 0
		for _, unit_type, payload in units:
			if unit_type == 'couple':
				couple = payload
				graph.individuals[couple.partner_a].slot = slot_cursor
				graph.individuals[couple.partner_b].slot = slot_cursor + 1
				slot_cursor += 3
			else:
				single = payload
				graph.individuals[single.id].slot = slot_cursor
				slot_cursor += 2
		max_slots = max(max_slots, slot_cursor)

		for index, couple in enumerate(gen_couples):
			for child_id in couple.children:
				parent_index[child_id] = index
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
