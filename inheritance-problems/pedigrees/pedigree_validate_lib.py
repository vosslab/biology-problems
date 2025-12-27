#!/usr/bin/env python3

# Local repo modules
import pedigree_code_lib


#===============================
def validate_code_string(code_string: str, strict: bool = False) -> list[str]:
	"""
	Validate a pedigree code string for allowed characters and structure.

	Args:
		code_string (str): Pedigree code string.
		strict (bool): When True, require consistent row lengths.

	Returns:
		list[str]: Validation error messages. Empty list means valid.
	"""
	errors: list[str] = []
	if not code_string:
		errors.append("Code string is empty.")
		return errors

	rows = [row for row in code_string.split('%') if row]
	if not rows:
		errors.append("Code string contains no rows.")
		return errors

	allowed_chars = set(pedigree_code_lib.short_hand_lookup.keys())
	for row_index, row in enumerate(rows, start=1):
		for col_index, char in enumerate(row, start=1):
			if char not in allowed_chars:
				errors.append(f"Unknown character '{char}' at row {row_index}, col {col_index}.")

	if strict:
		row_lengths = {len(row) for row in rows}
		if len(row_lengths) > 1:
			errors.append("Row lengths are inconsistent.")

	return errors


#===============================
def _get_connection_mask(char: str) -> list[bool] | None:
	"""
	Return [up, down, left, right] connectivity for connector glyphs.

	Args:
		char (str): Pedigree code character.

	Returns:
		list[bool] | None: Connectivity mask or None if not a connector glyph.
	"""
	name = pedigree_code_lib.short_hand_lookup.get(char)
	if name is None:
		return None

	binary_edges = pedigree_code_lib.shape_binary_edges.get(name)
	if binary_edges is None:
		return None

	mask = [edge != '0' for edge in binary_edges]
	return mask


#===============================
def _is_person_cell(char: str) -> bool:
	"""
	Check whether a character represents a person glyph.

	Args:
		char (str): Pedigree code character.

	Returns:
		bool: True if a person glyph, otherwise False.
	"""
	name = pedigree_code_lib.short_hand_lookup.get(char, '')
	is_person = 'SQUARE' in name or 'CIRCLE' in name
	return is_person


#===============================
def _get_code_grid(code_string: str) -> list[str]:
	"""
	Return code rows, excluding empty rows.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		list[str]: Code rows.
	"""
	rows = pedigree_code_lib.get_code_rows(code_string)
	return rows


#===============================
def validate_connector_adjacency(code_string: str) -> list[str]:
	"""
	Validate connector glyphs for required adjacency.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		list[str]: Validation error messages.
	"""
	errors: list[str] = []
	rows = _get_code_grid(code_string)
	if not rows:
		errors.append("Code string contains no rows.")
		return errors

	max_len = max(len(row) for row in rows)
	padded_rows = [row.ljust(max_len, '.') for row in rows]
	row_count = len(padded_rows)
	col_count = max_len

	for row_index, row in enumerate(padded_rows):
		for col_index, char in enumerate(row):
			mask = _get_connection_mask(char)
			if mask is None:
				continue

			for direction, requires in enumerate(mask):
				if not requires:
					continue

				neighbor_row = row_index + (-1 if direction == 0 else 1 if direction == 1 else 0)
				neighbor_col = col_index + (-1 if direction == 2 else 1 if direction == 3 else 0)

				if neighbor_row < 0 or neighbor_row >= row_count:
					errors.append(f"Dangling connector at row {row_index + 1}, col {col_index + 1}.")
					continue
				if neighbor_col < 0 or neighbor_col >= col_count:
					errors.append(f"Dangling connector at row {row_index + 1}, col {col_index + 1}.")
					continue

				neighbor_char = padded_rows[neighbor_row][neighbor_col]
				neighbor_mask = _get_connection_mask(neighbor_char)
				if neighbor_mask is not None:
					opposite = 1 if direction == 0 else 0 if direction == 1 else 3 if direction == 2 else 2
					if not neighbor_mask[opposite]:
						errors.append(
							f"Connector mismatch at row {row_index + 1}, col {col_index + 1}."
						)
				elif not _is_person_cell(neighbor_char):
					errors.append(f"Connector does not terminate on a person at row {row_index + 1}, col {col_index + 1}.")

	return errors


#===============================
def validate_connector_components(code_string: str) -> list[str]:
	"""
	Validate that connector components terminate on people.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		list[str]: Validation error messages.
	"""
	errors: list[str] = []
	rows = _get_code_grid(code_string)
	if not rows:
		errors.append("Code string contains no rows.")
		return errors

	max_len = max(len(row) for row in rows)
	padded_rows = [row.ljust(max_len, '.') for row in rows]
	row_count = len(padded_rows)
	col_count = max_len
	visited: set[tuple[int, int]] = set()

	for row_index in range(row_count):
		for col_index in range(col_count):
			if (row_index, col_index) in visited:
				continue
			mask = _get_connection_mask(padded_rows[row_index][col_index])
			if mask is None:
				continue

			stack = [(row_index, col_index)]
			component_cells: list[tuple[int, int]] = []
			component_terminals: set[tuple[int, int]] = set()
			visited.add((row_index, col_index))

			while stack:
				cell_row, cell_col = stack.pop()
				component_cells.append((cell_row, cell_col))
				for delta_row, delta_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
					neighbor_row = cell_row + delta_row
					neighbor_col = cell_col + delta_col
					if neighbor_row < 0 or neighbor_row >= row_count:
						continue
					if neighbor_col < 0 or neighbor_col >= col_count:
						continue

					neighbor_char = padded_rows[neighbor_row][neighbor_col]
					if _is_person_cell(neighbor_char):
						component_terminals.add((neighbor_row, neighbor_col))
						continue

					neighbor_mask = _get_connection_mask(neighbor_char)
					if neighbor_mask is None:
						continue
					if (neighbor_row, neighbor_col) in visited:
						continue
					visited.add((neighbor_row, neighbor_col))
					stack.append((neighbor_row, neighbor_col))

			if len(component_terminals) < 2:
				row_label = component_cells[0][0] + 1
				col_label = component_cells[0][1] + 1
				errors.append(
					f"Connector component near row {row_label}, col {col_label} touches fewer than 2 people."
				)

	return errors


#===============================
def validate_bounding_box(code_string: str, max_width_cells: int | None, max_height_cells: int | None) -> list[str]:
	"""
	Validate the bounding box of non-empty cells.

	Args:
		code_string (str): Pedigree code string.
		max_width_cells (int | None): Optional maximum width.
		max_height_cells (int | None): Optional maximum height.

	Returns:
		list[str]: Validation error messages.
	"""
	errors: list[str] = []
	rows = _get_code_grid(code_string)
	if not rows:
		errors.append("Code string contains no rows.")
		return errors

	max_len = max(len(row) for row in rows)
	padded_rows = [row.ljust(max_len, '.') for row in rows]

	min_row = None
	max_row = None
	min_col = None
	max_col = None

	for row_index, row in enumerate(padded_rows):
		for col_index, char in enumerate(row):
			if char == '.':
				continue
			if min_row is None:
				min_row = row_index
				max_row = row_index
				min_col = col_index
				max_col = col_index
				continue
			min_row = min(min_row, row_index)
			max_row = max(max_row, row_index)
			min_col = min(min_col, col_index)
			max_col = max(max_col, col_index)

	if min_row is None:
		errors.append("Code string contains no non-empty cells.")
		return errors

	width_cells = max_col - min_col + 1
	height_cells = max_row - min_row + 1

	if max_width_cells is not None and width_cells > max_width_cells:
		errors.append(f"Bounding box width {width_cells} exceeds {max_width_cells} cells.")
	if max_height_cells is not None and height_cells > max_height_cells:
		errors.append(f"Bounding box height {height_cells} exceeds {max_height_cells} cells.")

	return errors


#===============================
def validate_code_string_strict(
	code_string: str,
	max_width_cells: int | None = None,
	max_height_cells: int | None = None
) -> list[str]:
	"""
	Run strict validation with adjacency and bounding-box checks.

	Args:
		code_string (str): Pedigree code string.
		max_width_cells (int | None): Optional maximum width.
		max_height_cells (int | None): Optional maximum height.

	Returns:
		list[str]: Validation error messages.
	"""
	errors = validate_code_string(code_string, strict=False)
	if errors:
		return errors

	semantics_errors = validate_row_parity_semantics(code_string)
	errors.extend(semantics_errors)
	if errors:
		return errors

	box_errors = validate_bounding_box(code_string, max_width_cells, max_height_cells)
	errors.extend(box_errors)

	return errors


#===============================
def validate_row_parity_semantics(code_string: str) -> list[str]:
	"""
	Validate row parity semantics for people vs connector rows.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		list[str]: Validation error messages.
	"""
	errors: list[str] = []
	rows = _get_code_grid(code_string)
	if not rows:
		errors.append("Code string contains no rows.")
		return errors

	people_row_connectors = {'-', 'T', '='}
	for row_index, row in enumerate(rows):
		row_is_people = row_index % 2 == 0
		for col_index, char in enumerate(row):
			if char == '.':
				continue
			if row_is_people and _get_connection_mask(char) is not None:
				if char not in people_row_connectors:
					errors.append(
						f"Connector symbol '{char}' on people row {row_index + 1}, col {col_index + 1}."
					)
				else:
					left_ok = col_index > 0 and _is_person_cell(row[col_index - 1])
					right_ok = col_index + 1 < len(row) and _is_person_cell(row[col_index + 1])
					if not (left_ok and right_ok):
						errors.append(
							f"Connector '{char}' on people row {row_index + 1}, col {col_index + 1} must sit between two people."
						)
			if (not row_is_people) and _is_person_cell(char):
				errors.append(
					f"Person symbol '{char}' on connector row {row_index + 1}, col {col_index + 1}."
				)

	for row_index in range(1, len(rows), 2):
		connector_row = rows[row_index]
		has_vertical = '|' in connector_row or '^' in connector_row
		if not has_vertical:
			continue
		if row_index - 1 >= 0:
			upper_row = rows[row_index - 1]
			if 'T' in upper_row:
				errors.append(
					f"Vertical descent at connector row {row_index + 1} must terminate on a person, not a couple midpoint in row {row_index}."
				)
		if row_index + 1 < len(rows):
			lower_row = rows[row_index + 1]
			if 'T' in lower_row:
				errors.append(
					f"Vertical descent at connector row {row_index + 1} must terminate on a person, not a couple midpoint in row {row_index + 2}."
				)

	return errors


#===============================
def is_valid_code_string(code_string: str, strict: bool = False) -> bool:
	"""
	Check whether a pedigree code string is valid.

	Args:
		code_string (str): Pedigree code string.
		strict (bool): When True, require consistent row lengths.

	Returns:
		bool: True if valid, otherwise False.
	"""
	errors = validate_code_string(code_string, strict)
	is_valid = len(errors) == 0
	return is_valid


#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	assert is_valid_code_string(sample_code)

## THE END
