#!/usr/bin/env python3

#===============================
table_cell_dimension = 65
hide_carriers = True

#===============================
character_sizes = {
	'LEFT-HALF BLACK SQUARE': 42,
	'RIGHT-HALF BLACK SQUARE': 42,
	'BLACK SQUARE': 48,
	'WHITE SQUARE': 48,
	'LEFT-HALF BLACK CIRCLE': 32,
	'RIGHT-HALF BLACK CIRCLE': 32,
	'BLACK CIRCLE': 26,
	'WHITE CIRCLE': 28,
}

#===============================
character_unicodes = {
	'LEFT-HALF BLACK SQUARE': '&#x25E7;',
	'RIGHT-HALF BLACK SQUARE': '&#x25E8;',
	'BLACK SQUARE': '&#x25FC;',
	'WHITE SQUARE': '&#x25FB;',
	'LEFT-HALF BLACK CIRCLE': '&#x25D0;',
	'RIGHT-HALF BLACK CIRCLE': '&#x25D1;',
	'BLACK CIRCLE': '&#x2B24;',
	'WHITE CIRCLE': '&xcirc;',
}

#===============================
shape_binary_edges = {
	# up-down-left-right
	'HORIZONTAL LINE SHAPE': '0011',
	'DOWN-RIGHT ELBOW SHAPE': '0101',
	'DOWN-LEFT ELBOW SHAPE': '0110',
	'T SHAPE': '0111',
	'INCEST T SHAPE': '0122',
	'UP-RIGHT ELBOW SHAPE': '1001',
	'UP-LEFT ELBOW SHAPE': '1010',
	'PERPENDICULAR TENT SHAPE': '1011',
	'VERTICAL LINE SHAPE': '1100',
	'PLUS SHAPE': '1111',
}

#===============================
if hide_carriers is False:
	short_hand_lookup = {
		'.': 'SPACE',
		'%': 'NEW LINE',
		'x': 'BLACK SQUARE',
		'#': 'WHITE SQUARE',
		'[': 'LEFT-HALF BLACK SQUARE',
		']': 'RIGHT-HALF BLACK SQUARE',
		'*': 'BLACK CIRCLE',
		'o': 'WHITE CIRCLE',
		'(': 'LEFT-HALF BLACK CIRCLE',
		')': 'RIGHT-HALF BLACK CIRCLE',
		'T': 'T SHAPE',
		'=': 'INCEST T SHAPE',
		'|': 'VERTICAL LINE SHAPE',
		'^': 'PERPENDICULAR TENT SHAPE',
		'+': 'PLUS SHAPE',
		'-': 'HORIZONTAL LINE SHAPE',
		'L': 'UP-RIGHT ELBOW SHAPE',
		'u': 'UP-LEFT ELBOW SHAPE',
		'r': 'DOWN-RIGHT ELBOW SHAPE',
		'd': 'DOWN-LEFT ELBOW SHAPE',
	}
else:
	short_hand_lookup = {
		'.': 'SPACE',
		'%': 'NEW LINE',
		'x': 'BLACK SQUARE',
		'#': 'WHITE SQUARE',
		'[': 'WHITE SQUARE',
		']': 'WHITE SQUARE',
		'*': 'BLACK CIRCLE',
		'o': 'WHITE CIRCLE',
		'(': 'WHITE CIRCLE',
		')': 'WHITE CIRCLE',
		'T': 'T SHAPE',
		'=': 'INCEST T SHAPE',
		'|': 'VERTICAL LINE SHAPE',
		'^': 'PERPENDICULAR TENT SHAPE',
		'+': 'PLUS SHAPE',
		'-': 'HORIZONTAL LINE SHAPE',
		'L': 'UP-RIGHT ELBOW SHAPE',
		'u': 'UP-LEFT ELBOW SHAPE',
		'r': 'DOWN-RIGHT ELBOW SHAPE',
		'd': 'DOWN-LEFT ELBOW SHAPE',
	}


#===============================
def get_code_rows(code_string: str) -> list[str]:
	"""
	Split a code string into rows, skipping empty rows.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		list[str]: Non-empty rows.
	"""
	rows = [row for row in code_string.split('%') if row]
	return rows


#===============================
def count_generations(code_string: str) -> int:
	"""
	Estimate the number of generations represented in a code string.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		int: Estimated number of generations.
	"""
	rows = get_code_rows(code_string)
	if not rows:
		raise ValueError("Empty pedigree code string.")
	generations = (len(rows) + 1) // 2
	return generations


#===============================
def mirror_pedigree(code_string: str) -> str:
	"""
	Mirror a pedigree code string horizontally.

	Rows are first padded to equal length before mirroring to preserve
	vertical alignment of connectors.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		str: Mirrored code string.
	"""
	code_lines = code_string.split('%')

	# Pad all rows to the same length before mirroring
	# This preserves vertical alignment of connectors
	max_len = max(len(line) for line in code_lines) if code_lines else 0
	padded_lines = [line.ljust(max_len, '.') for line in code_lines]

	mirror_code_lines = []
	for code_line in padded_lines:
		mirror_code_line = code_line[::-1]
		# u <-> L
		mirror_code_line = mirror_code_line.replace('u', '@')
		mirror_code_line = mirror_code_line.replace('L', 'u')
		mirror_code_line = mirror_code_line.replace('@', 'L')
		# r <-> d
		mirror_code_line = mirror_code_line.replace('r', '@')
		mirror_code_line = mirror_code_line.replace('d', 'r')
		mirror_code_line = mirror_code_line.replace('@', 'd')

		# Strip trailing dots to match original format
		mirror_code_line = mirror_code_line.rstrip('.')
		if not mirror_code_line:
			mirror_code_line = '.'

		mirror_code_lines.append(mirror_code_line)
	mirror_code_string = '%'.join(mirror_code_lines)
	return mirror_code_string


#===============================
def mirrorPedigree(code_string: str) -> str:
	"""
	Legacy alias for mirror_pedigree.
	"""
	mirrored = mirror_pedigree(code_string)
	return mirrored


#===============================
#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	assert count_generations(sample_code) == 3
	assert mirror_pedigree(sample_code).count('%') == sample_code.count('%')

## THE END
