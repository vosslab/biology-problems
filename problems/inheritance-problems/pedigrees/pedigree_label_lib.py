#!/usr/bin/env python3

# Standard Library
import string

# Local repo modules
import pedigree_code_lib


#===============================
def make_label_string(code_string: str, label_positions: dict[tuple[int, int], str]) -> str:
	"""
	Build a label string aligned to the code string grid.

	Args:
		code_string (str): Pedigree code string.
		label_positions (dict[(row, col), str]): Label characters keyed by grid position.

	Returns:
		str: Label string with identical row structure to code_string.
	"""
	code_rows = pedigree_code_lib.get_code_rows(code_string)
	if not code_rows:
		raise ValueError('Empty pedigree code string.')
	max_cols = max(len(row) for row in code_rows)

	label_grid = [['.' for _ in range(max_cols)] for _ in range(len(code_rows))]
	for (row, col), label in label_positions.items():
		if row < 0 or row >= len(code_rows):
			continue
		if col < 0 or col >= max_cols:
			continue
		label_grid[row][col] = label

	label_rows: list[str] = []
	for row_index, code_row in enumerate(code_rows):
		row_len = len(code_row)
		if row_len <= 0:
			label_rows.append('.')
			continue
		line = ''.join(label_grid[row_index])[:row_len]
		if len(line) < row_len:
			line = line.ljust(row_len, '.')
		label_rows.append(line)
	return '%'.join(label_rows)


#===============================
def assign_labels(label_count: int) -> list[str]:
	"""
	Assign deterministic labels (A-Z then a-z) for a given count.

	Args:
		label_count (int): Number of labels needed.

	Returns:
		list[str]: Label characters.
	"""
	alphabet = list(string.ascii_uppercase) + list(string.ascii_lowercase)
	if label_count > len(alphabet):
		raise ValueError('Too many labels for available alphabet.')
	return alphabet[:label_count]


#===============================
def validate_label_string(label_string: str, code_string: str) -> list[str]:
	"""
	Validate label string structure against a code string.

	Args:
		label_string (str): Label string.
		code_string (str): Pedigree code string.

	Returns:
		list[str]: Validation error messages.
	"""
	errors: list[str] = []
	code_rows = pedigree_code_lib.get_code_rows(code_string)
	label_rows = pedigree_code_lib.get_code_rows(label_string)

	if len(code_rows) != len(label_rows):
		errors.append('Label rows must match code string row count.')
		return errors

	labels_seen: set[str] = set()
	for row_index, (code_row, label_row) in enumerate(zip(code_rows, label_rows)):
		if len(code_row) != len(label_row):
			errors.append(
				f"Row {row_index + 1} length mismatch: code={len(code_row)} label={len(label_row)}."
			)
			continue
		for col_index, (code_char, label_char) in enumerate(zip(code_row, label_row)):
			if label_char == '.':
				continue
			if not label_char.isalpha() or len(label_char) != 1:
				errors.append(
					f"Invalid label '{label_char}' at row {row_index + 1}, col {col_index + 1}."
				)
				continue
			name = pedigree_code_lib.short_hand_lookup.get(code_char, '')
			if 'SQUARE' not in name and 'CIRCLE' not in name:
				errors.append(
					f"Label '{label_char}' must align with a person cell at row {row_index + 1}, col {col_index + 1}."
				)
			if label_char in labels_seen:
				errors.append(f"Duplicate label '{label_char}'.")
			labels_seen.add(label_char)

	return errors


#===============================
if __name__ == '__main__':
	sample_code = "#To%r^d%#.o"
	positions = {(0, 0): 'A', (0, 2): 'B', (2, 0): 'C', (2, 2): 'D'}
	print(make_label_string(sample_code, positions))

## THE END
