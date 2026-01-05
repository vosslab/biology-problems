#!/usr/bin/env python3

# Standard Library
import dataclasses

# Local repo modules
import pedigree_code_lib
import pedigree_validate_lib


#===============================
@dataclasses.dataclass
class Individual:
	id: str
	sex: str
	phenotype: str
	generation: int
	row: int
	col: int
	father_id: str | None = None
	mother_id: str | None = None


#===============================
@dataclasses.dataclass
class Couple:
	id: str
	partner_a: str
	partner_b: str
	row: int
	col_left: int
	col_right: int
	children: list[str]


#===============================
def _is_individual_shape(shape_name: str) -> bool:
	is_individual = shape_name.endswith('CIRCLE') or shape_name.endswith('SQUARE')
	return is_individual


#===============================
def _phenotype_from_shape(shape_name: str) -> str:
	if shape_name.startswith('BLACK'):
		return 'affected'
	if shape_name.startswith('LEFT-HALF') or shape_name.startswith('RIGHT-HALF'):
		return 'carrier'
	return 'unaffected'


#===============================
def _sex_from_shape(shape_name: str) -> str:
	if shape_name.endswith('SQUARE'):
		return 'male'
	return 'female'


#===============================
def _build_grid(code_string: str) -> tuple[list[list[str]], int, int]:
	rows = pedigree_code_lib.get_code_rows(code_string)
	if not rows:
		raise ValueError("Empty pedigree code string.")
	max_cols = max(len(row) for row in rows)
	grid = []
	for row in rows:
		row_chars = list(row.ljust(max_cols, '.'))
		grid.append(row_chars)
	num_rows = len(grid)
	return grid, num_rows, max_cols


#===============================
def _find_individual_rows(grid: list[list[str]]) -> list[int]:
	individual_rows = []
	for row_index, row in enumerate(grid):
		for char in row:
			shape_name = pedigree_code_lib.short_hand_lookup.get(char, None)
			if shape_name is None:
				continue
			if _is_individual_shape(shape_name):
				individual_rows.append(row_index)
				break
	return individual_rows


#===============================
def _build_individuals(grid: list[list[str]], individual_rows: list[int]) -> dict[str, Individual]:
	row_to_generation = {row: idx + 1 for idx, row in enumerate(individual_rows)}
	individuals: dict[str, Individual] = {}
	for row_index in individual_rows:
		for col_index, char in enumerate(grid[row_index]):
			shape_name = pedigree_code_lib.short_hand_lookup.get(char, None)
			if shape_name is None or not _is_individual_shape(shape_name):
				continue
			sex = _sex_from_shape(shape_name)
			phenotype = _phenotype_from_shape(shape_name)
			generation = row_to_generation[row_index]
			ind_id = f"r{row_index}_c{col_index}"
			individuals[ind_id] = Individual(
				id=ind_id,
				sex=sex,
				phenotype=phenotype,
				generation=generation,
				row=row_index,
				col=col_index,
			)
	return individuals


#===============================
def _connectors_have_horizontal(shape_name: str) -> bool:
	edges = pedigree_code_lib.shape_binary_edges[shape_name]
	has_left = edges[2] in ('1', '2')
	has_right = edges[3] in ('1', '2')
	return has_left and has_right


#===============================
def _connectors_have_down(shape_name: str) -> bool:
	edges = pedigree_code_lib.shape_binary_edges[shape_name]
	has_down = edges[1] in ('1', '2')
	return has_down


#===============================
def _find_couples(grid: list[list[str]], individuals: dict[str, Individual], individual_rows: list[int]) -> list[Couple]:
	couples: list[Couple] = []
	used = set()
	for row_index in individual_rows:
		row = grid[row_index]
		ind_positions = [ind.col for ind in individuals.values() if ind.row == row_index]
		ind_positions.sort()
		for idx, col_left in enumerate(ind_positions):
			left_id = f"r{row_index}_c{col_left}"
			if left_id in used:
				continue
			for col_right in ind_positions[idx + 1:]:
				right_id = f"r{row_index}_c{col_right}"
				if right_id in used:
					continue
				if col_right - col_left <= 1:
					continue
				valid = True
				for col_mid in range(col_left + 1, col_right):
					char = row[col_mid]
					shape_name = pedigree_code_lib.short_hand_lookup.get(char, None)
					if shape_name is None or not shape_name.endswith('SHAPE'):
						valid = False
						break
					if not _connectors_have_horizontal(shape_name):
						valid = False
						break
				if not valid:
					continue
				couple_id = f"couple_{row_index}_{col_left}_{col_right}"
				couples.append(Couple(
					id=couple_id,
					partner_a=left_id,
					partner_b=right_id,
					row=row_index,
					col_left=col_left,
					col_right=col_right,
					children=[],
				))
				used.add(left_id)
				used.add(right_id)
				break
	return couples


#===============================
def _build_adjacency(grid: list[list[str]]) -> dict[tuple[int, int], list[tuple[int, int]]]:
	adjacency: dict[tuple[int, int], list[tuple[int, int]]] = {}
	num_rows = len(grid)
	num_cols = len(grid[0])
	for row_index in range(num_rows):
		for col_index in range(num_cols):
			char = grid[row_index][col_index]
			shape_name = pedigree_code_lib.short_hand_lookup.get(char, None)
			if shape_name is None or not shape_name.endswith('SHAPE'):
				continue
			edges = pedigree_code_lib.shape_binary_edges[shape_name]
			pos = (row_index, col_index)
			for direction, offset in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
				if edges[direction] not in ('1', '2'):
					continue
				neighbor_row = row_index + offset[0]
				neighbor_col = col_index + offset[1]
				if neighbor_row < 0 or neighbor_row >= num_rows:
					continue
				if neighbor_col < 0 or neighbor_col >= num_cols:
					continue
				neighbor_char = grid[neighbor_row][neighbor_col]
				neighbor_shape = pedigree_code_lib.short_hand_lookup.get(neighbor_char, None)
				if neighbor_shape is None or neighbor_shape == 'SPACE':
					continue
				adjacency.setdefault(pos, []).append((neighbor_row, neighbor_col))
				adjacency.setdefault((neighbor_row, neighbor_col), []).append(pos)
	return adjacency


#===============================
def _find_children(
	grid: list[list[str]],
	adjacency: dict[tuple[int, int], list[tuple[int, int]]],
	individuals: dict[str, Individual],
	couple: Couple,
	child_row: int,
) -> list[str]:
	children: list[str] = []
	row = couple.row
	for col_index in range(couple.col_left, couple.col_right + 1):
		char = grid[row][col_index]
		shape_name = pedigree_code_lib.short_hand_lookup.get(char, None)
		if shape_name is None or not shape_name.endswith('SHAPE'):
			continue
		if not _connectors_have_down(shape_name):
			continue
		start = (row, col_index)
		queue = [start]
		visited = {start}
		while queue:
			current = queue.pop(0)
			for neighbor in adjacency.get(current, []):
				if neighbor in visited:
					continue
				if neighbor[0] <= row or neighbor[0] > child_row:
					continue
				neighbor_char = grid[neighbor[0]][neighbor[1]]
				neighbor_shape = pedigree_code_lib.short_hand_lookup.get(neighbor_char, None)
				if neighbor_shape is None or neighbor_shape == 'SPACE':
					continue
				if _is_individual_shape(neighbor_shape) and neighbor[0] == child_row:
					child_id = f"r{neighbor[0]}_c{neighbor[1]}"
					if child_id in individuals:
						children.append(child_id)
					continue
				visited.add(neighbor)
				queue.append(neighbor)
	children = list(dict.fromkeys(children))
	return children


#===============================
def parse_pedigree_graph(code_string: str) -> tuple[dict[str, Individual], list[Couple], bool]:
	"""
	Parse a pedigree code string into individuals and couples.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		tuple: (individuals, couples, carriers_visible).
	"""
	grid, _, _ = _build_grid(code_string)
	individual_rows = _find_individual_rows(grid)
	individuals = _build_individuals(grid, individual_rows)
	couples = _find_couples(grid, individuals, individual_rows)
	adjacency = _build_adjacency(grid)

	individual_rows_sorted = sorted(individual_rows)
	row_to_next = {}
	for idx, row_index in enumerate(individual_rows_sorted[:-1]):
		row_to_next[row_index] = individual_rows_sorted[idx + 1]

	for couple in couples:
		child_row = row_to_next.get(couple.row, None)
		if child_row is None:
			continue
		children = _find_children(grid, adjacency, individuals, couple, child_row)
		couple.children = children
		partner_a = individuals.get(couple.partner_a)
		partner_b = individuals.get(couple.partner_b)
		if partner_a is None or partner_b is None:
			continue
		if partner_a.sex == 'male':
			father_id = partner_a.id
			mother_id = partner_b.id if partner_b.sex == 'female' else None
		elif partner_b.sex == 'male':
			father_id = partner_b.id
			mother_id = partner_a.id if partner_a.sex == 'female' else None
		else:
			father_id = None
			mother_id = None
		for child_id in children:
			child = individuals.get(child_id, None)
			if child is None:
				continue
			if child.father_id is None:
				child.father_id = father_id
			if child.mother_id is None:
				child.mother_id = mother_id

	carriers_visible = any(ind.phenotype == 'carrier' for ind in individuals.values())
	return individuals, couples, carriers_visible


#===============================
def validate_mode(
	individuals: dict[str, Individual],
	mode: str,
	allow_de_novo: bool = False,
	carriers_visible: bool = False,
) -> list[str]:
	"""
	Validate inheritance constraints for a pedigree graph.

	Args:
		individuals (dict[str, Individual]): Parsed individuals.
		mode (str): Inheritance mode.
		allow_de_novo (bool): Allow de novo events for AD.
		carriers_visible (bool): Whether carrier state is explicitly shown.

	Returns:
		list[str]: Validation errors.
	"""
	errors: list[str] = []
	mode_value = mode.strip().lower()

	children_by_father: dict[str, list[Individual]] = {}
	for ind in individuals.values():
		if ind.father_id:
			children_by_father.setdefault(ind.father_id, []).append(ind)

	if mode_value in ('autosomal dominant', 'ad'):
		for ind in individuals.values():
			if ind.phenotype != 'affected':
				continue
			if ind.father_id is None and ind.mother_id is None:
				continue
			father = individuals.get(ind.father_id, None)
			mother = individuals.get(ind.mother_id, None)
			if allow_de_novo:
				continue
			if father is None and mother is None:
				continue
			father_ok = father is not None and father.phenotype == 'affected'
			mother_ok = mother is not None and mother.phenotype == 'affected'
			if not father_ok and not mother_ok:
				errors.append(f"{ind.id}: affected without affected parent (AD).")

	if mode_value in ('autosomal recessive', 'ar'):
		for ind in individuals.values():
			if ind.phenotype != 'affected':
				continue
			if ind.father_id is None and ind.mother_id is None:
				continue
			father = individuals.get(ind.father_id, None)
			mother = individuals.get(ind.mother_id, None)
			if not carriers_visible:
				continue
			for parent in (father, mother):
				if parent is None:
					continue
				if parent.phenotype not in ('affected', 'carrier'):
					errors.append(f"{ind.id}: affected child with non-carrier parent (AR).")

	if mode_value in ('x-linked recessive', 'xr'):
		for ind in individuals.values():
			if ind.phenotype != 'affected':
				continue
			father = individuals.get(ind.father_id, None)
			mother = individuals.get(ind.mother_id, None)
			if ind.sex == 'female':
				if father is not None and father.phenotype != 'affected':
					errors.append(f"{ind.id}: affected female with unaffected father (XR).")
				if carriers_visible and mother is not None:
					if mother.phenotype not in ('affected', 'carrier'):
						errors.append(f"{ind.id}: affected female with non-carrier mother (XR).")
			else:
				if father is not None and father.phenotype == 'affected':
					errors.append(f"{ind.id}: affected male with affected father (XR).")
				if carriers_visible and mother is not None:
					if mother.phenotype not in ('affected', 'carrier'):
						errors.append(f"{ind.id}: affected male with non-carrier mother (XR).")

	if mode_value in ('y-linked', 'yl'):
		for ind in individuals.values():
			if ind.phenotype == 'affected' and ind.sex != 'male':
				errors.append(f"{ind.id}: affected female in Y-linked mode.")
		for father_id, children in children_by_father.items():
			father = individuals.get(father_id, None)
			if father is None or father.phenotype != 'affected':
				continue
			for child in children:
				if child.sex == 'male' and child.phenotype != 'affected':
					errors.append(f"{child.id}: unaffected son of affected father (YL).")

	return errors


#===============================
def validate_mode_from_code(
	code_string: str,
	mode: str,
	allow_de_novo: bool = False,
	carriers_visible: bool | None = None,
) -> list[str]:
	"""
	Validate a code string under a specific inheritance mode.

	Args:
		code_string (str): Pedigree code string.
		mode (str): Inheritance mode.
		allow_de_novo (bool): Allow de novo events for AD.
		carriers_visible (bool | None): Override carrier visibility detection.

	Returns:
		list[str]: Validation errors.
	"""
	errors = pedigree_validate_lib.validate_code_string(code_string)
	if errors:
		return errors
	individuals, _, detected_carriers = parse_pedigree_graph(code_string)
	carrier_flag = detected_carriers if carriers_visible is None else carriers_visible
	mode_errors = validate_mode(
		individuals,
		mode,
		allow_de_novo=allow_de_novo,
		carriers_visible=carrier_flag,
	)
	return mode_errors


#===============================
#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	mode_errors = validate_mode_from_code(sample_code, 'y-linked')
	assert isinstance(mode_errors, list)

## THE END
