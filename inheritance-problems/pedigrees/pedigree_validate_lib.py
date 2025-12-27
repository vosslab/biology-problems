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
