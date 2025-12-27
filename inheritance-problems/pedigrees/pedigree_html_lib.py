#!/usr/bin/env python3

# Local repo modules
import pedigree_code_lib
import pedigree_label_lib


#===============================
def makeCharacterTD_Cell(character_name):
	character_unicode = pedigree_code_lib.character_unicodes[character_name]
	fontsize = pedigree_code_lib.character_sizes[character_name]
	html_text = makeTD_Cell(character_name, character_unicode, fontsize)
	return html_text


#===============================
def makeTD_Cell(comment_text, character_unicode, fontsize, line_height="0px"):
	html_text = ''
	if comment_text is not None:
		html_text += f'<!-- {comment_text} --> '
	html_text += '<td align="center" style="'
	if fontsize is not None:
		html_text += f'font-size: {fontsize:d}pt; '
	html_text += (
		f'padding: 0; margin: 0; line-height: {line_height}; vertical-align: middle; '
		f'width: {pedigree_code_lib.table_cell_dimension}px; '
		f'height: {pedigree_code_lib.table_cell_dimension}px;">'
	)
	html_text += f'{character_unicode}</td>'
	return html_text


#===============================
def _make_person_span(shape_name, label_text):
	cell_size = pedigree_code_lib.table_cell_dimension
	border_width = 2
	font_size = max(8, int(cell_size * 0.6))
	label = label_text if label_text else '&nbsp;'
	is_circle = shape_name.endswith('CIRCLE')
	is_black = shape_name.startswith('BLACK')
	is_left_half = shape_name.startswith('LEFT-HALF')
	is_right_half = shape_name.startswith('RIGHT-HALF')

	outer_styles = [
		'display: inline-block',
		'position: relative',
		f'width: {cell_size}px',
		f'height: {cell_size}px',
		f'line-height: {cell_size}px',
		'text-align: center',
		'font-weight: bold',
		f'font-size: {font_size}px',
		f'border: {border_width}px solid #000',
		'box-sizing: border-box',
		'overflow: hidden',
	]
	if is_circle:
		outer_styles.append('border-radius: 50%')

	text_color = '#000000'
	background_color = '#ffffff'
	if is_black:
		background_color = '#000000'
		text_color = '#ffffff'

	if not (is_left_half or is_right_half):
		outer_styles.append(f'background-color: {background_color}')
		outer_styles.append(f'color: {text_color}')
		return (
			f"<span style=\"{' ; '.join(outer_styles)}\">"
			f"<span style='position: relative; z-index: 1;'>{label}</span>"
			"</span>"
		)

	outer_styles.append('color: #000000')
	half_left_color = '#000000' if is_left_half else '#ffffff'
	half_right_color = '#000000' if is_right_half else '#ffffff'
	return (
		f"<span style=\"{' ; '.join(outer_styles)}\">"
		f"<span style='position: absolute; left: 0; top: 0; width: 50%; height: 100%; background: {half_left_color};'></span>"
		f"<span style='position: absolute; right: 0; top: 0; width: 50%; height: 100%; background: {half_right_color};'></span>"
		f"<span style='position: relative; z-index: 1;'>{label}</span>"
		"</span>"
	)


#===============================
def makePersonTD_Cell(shape_name, label_text):
	html_text = ''
	html_text += f'<!-- {shape_name} --> '
	html_text += '<td align="center" style="'
	html_text += (
		'padding: 0; margin: 0; vertical-align: middle; '
		f'width: {pedigree_code_lib.table_cell_dimension}px; '
		f'height: {pedigree_code_lib.table_cell_dimension}px;">'
	)
	html_text += _make_person_span(shape_name, label_text)
	html_text += '</td>'
	return html_text


#===============================
def tabelEdgeTD_Cell(location_binary, edge_binary):
	# location_binary: 00 top left, 01 top right, 10 bottom left, 11 bottom right
	# edge_binary: up-down-left-right
	td_cell_text = (
		'<td style="padding: 0; margin: 0; line-height: 0px; font-size: 1px;'
	)
	if location_binary == '00': # top-left
		if edge_binary[0] == '1': # up
			td_cell_text += 'border-right: 3px solid #000000; '
		if edge_binary[2] == '1': # left
			td_cell_text += 'border-bottom: 3px solid #000000; '
		elif edge_binary[2] == '2': # left
			td_cell_text += 'border-bottom: 9px double #000000; '
	elif location_binary == '01': # top-right
		if edge_binary[0] == '1': # up
			td_cell_text += 'border-left: 3px solid #000000; '
		if edge_binary[3] == '1': # right
			td_cell_text += 'border-bottom: 3px solid #000000; '
		elif edge_binary[3] == '2': # right
			td_cell_text += 'border-bottom: 9px double #000000; '
	elif location_binary == '10': # bottom-left
		if edge_binary[1] == '1': # down
			td_cell_text += 'border-right: 3px solid #000000; '
		if edge_binary[2] == '1': # left
			td_cell_text += 'border-top: 3px solid #000000; '
		elif edge_binary[2] == '2': # left
			td_cell_text += 'border-top: 9px double #000000; '
	elif location_binary == '11': # bottom-right
		if edge_binary[1] == '1': # down
			td_cell_text += 'border-left: 3px solid #000000; '
		if edge_binary[3] == '1': # right
			td_cell_text += 'border-top: 3px solid #000000; '
		elif edge_binary[3] == '2': # right
			td_cell_text += 'border-top: 9px double #000000; '
	td_cell_text += '">&nbsp;</td> '
	return td_cell_text


#===============================
def makeShapeNameTableTD_Cell(shape_name):
	binary_edges = pedigree_code_lib.shape_binary_edges[shape_name]
	shape_html_text = ''
	shape_html_text += f'<!-- START {shape_name} -->'
	shape_html_text += '<td align="center" style="vertical-align: middle; padding: 0; margin: 0; line-height: 0px; "> '
	shape_html_text += '<table border="0" cellpadding="0" cellspacing="0" '
	shape_html_text += (
		' style="padding: 0; margin: 0; '
		f'width: {pedigree_code_lib.table_cell_dimension}px; '
		f'height: {pedigree_code_lib.table_cell_dimension}px; '
		'border-collapse: collapse; border-style: hidden;"> '
	)
	shape_html_text += '<tbody><tr> '
	shape_html_text += tabelEdgeTD_Cell('00', binary_edges)
	shape_html_text += tabelEdgeTD_Cell('01', binary_edges)
	shape_html_text += '</tr><tr> '
	shape_html_text += tabelEdgeTD_Cell('10', binary_edges)
	shape_html_text += tabelEdgeTD_Cell('11', binary_edges)
	shape_html_text += '</tr></tbody></table></td> '
	shape_html_text += f'<!-- END {shape_name} -->'
	return shape_html_text


#===============================
def translateCode(code_string, label_string=None):
	max_num_col = 0
	num_row = 0
	num_col = 0
	html_code = ''
	if not code_string.endswith('%'):
		code_string += '%'
	label_chars = None
	if label_string is not None:
		if not label_string.endswith('%'):
			label_string += '%'
		label_chars = list(label_string)

	for idx, char in enumerate(list(code_string)):
		if char != '%':
			num_col += 1
		char_name = pedigree_code_lib.short_hand_lookup[char]
		if char_name.endswith('SHAPE'):
			html_code += makeShapeNameTableTD_Cell(char_name)
		elif char_name.endswith('CIRCLE') or char_name.endswith('SQUARE'):
			label_text = ''
			if label_chars is not None and idx < len(label_chars):
				label_candidate = label_chars[idx]
				if label_candidate != '.':
					label_text = label_candidate
			html_code += makePersonTD_Cell(char_name, label_text)
		elif char_name == 'SPACE':
			html_code += makeTD_Cell(None, '&nbsp;', 1)
		elif char_name == 'NEW LINE':
			num_row += 1
			max_num_col = max(max_num_col, num_col)
			num_col = 0
			html_code += '</tr><tr>'
	html_text = (
		'<p><table cellpadding="0" cellspacing="0" style='
		+ '"padding: 0; margin: 0; border-collapse: collapse; border: 3px solid silver; '
		+ f'width: {max_num_col * pedigree_code_lib.table_cell_dimension}px; '
		+ f'height: {num_row * pedigree_code_lib.table_cell_dimension}px"'
		+ '><tr>'
		+ html_code
		+ '</tr></table></p><p>&nbsp;</p>'
	)
	return html_text


#===============================
def make_pedigree_html(code_string: str, label_string: str | None = None) -> str:
	"""
	Translate a pedigree code string into HTML markup.

	Args:
		code_string (str): Pedigree code string.
		label_string (str | None): Optional label string aligned to code_string.

	Returns:
		str: HTML table markup.
	"""
	if label_string is not None:
		errors = pedigree_label_lib.validate_label_string(label_string, code_string)
		if errors:
			raise ValueError("Invalid label string: " + "; ".join(errors))
	html_text = translateCode(code_string, label_string)
	return html_text


#===============================
#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	print(make_pedigree_html(sample_code))

## THE END
