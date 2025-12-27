#!/usr/bin/env python3

# Local repo modules
import pedigree_code_lib


#===============================
def makeCharacterTD_Cell(character_name):
	character_unicode = pedigree_code_lib.character_unicodes[character_name]
	fontsize = pedigree_code_lib.character_sizes[character_name]
	html_text = makeTD_Cell(character_name, character_unicode, fontsize)
	return html_text


#===============================
def makeTD_Cell(comment_text, character_unicode, fontsize):
	html_text = ''
	if comment_text is not None:
		html_text += f'<!-- {comment_text} --> '
	html_text += '<td align="center" style="'
	if fontsize is not None:
		html_text += f'font-size: {fontsize:d}pt; '
	html_text += (
		'padding: 0; margin: 0; line-height: 0px; vertical-align: middle; '
		f'width: {pedigree_code_lib.table_cell_dimension}px; '
		f'height: {pedigree_code_lib.table_cell_dimension}px;">'
	)
	html_text += f'{character_unicode}</td>'
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
def translateCode(code_string):
	max_num_col = 0
	num_row = 0
	num_col = 0
	html_code = ''
	if not code_string.endswith('%'):
		code_string += '%'
	for char in list(code_string):
		if char != '%':
			num_col += 1
		char_name = pedigree_code_lib.short_hand_lookup[char]
		if char_name.endswith('SHAPE'):
			html_code += makeShapeNameTableTD_Cell(char_name)
		elif char_name.endswith('CIRCLE') or char_name.endswith('SQUARE'):
			html_code += makeCharacterTD_Cell(char_name)
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
def make_pedigree_html(code_string: str) -> str:
	"""
	Translate a pedigree code string into HTML markup.

	Args:
		code_string (str): Pedigree code string.

	Returns:
		str: HTML table markup.
	"""
	html_text = translateCode(code_string)
	return html_text


#===============================
#===============================
if __name__ == '__main__':
	sample_code = "#To..#To%r^d...|.%x.*-T-#.%....|...%....x..."
	print(make_pedigree_html(sample_code))

## THE END
