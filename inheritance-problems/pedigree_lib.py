#!/usr/bin/env python

table_cell_dimension = 65
### TODO
# add roman numerals to the beginning and ending of each generation
# better generation of pedigrees
# ability to add names to pedigree
# add incest

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
	#up-down-left-right
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
def makeCharacterTD_Cell(character_name):
	character_unicode = character_unicodes[character_name]
	fontsize = character_sizes[character_name]
	html_text = makeTD_Cell(character_name, character_unicode, fontsize)
	return html_text

#===============================
def makeTD_Cell(comment_text, character_unicode, fontsize):
	html_text = ''
	if comment_text is not None:
		html_text += '<!--- {0} ---> '.format(comment_text)
	html_text += '<td align="center" style="'
	if fontsize is not None:
		html_text += 'font-size: {0:d}pt; '.format(fontsize)
	html_text += 'padding: 0; margin: 0; line-height: 0px; vertical-align: middle; width: {0}px; height: {0}px;">'.format(table_cell_dimension)
	html_text += '{0}</td>'.format(character_unicode)
	return html_text

#===============================
def tabelEdgeTD_Cell(location_binary, edge_binary):
	#location_binary: 00 top left, 01 top right, 10 bottom left, 11 bottom right
	#edge_binary: up-down-left-right
	td_cell_text = '<td style="padding: 0; margin: 0; line-height: 0px; font-size: 1px;'
	#print(location_binary, edge_binary)	
	if location_binary == '00': #top-left
		if edge_binary[0] == '1': #up
			td_cell_text += 'border-right: 3px solid #000000; '
		if edge_binary[2] == '1': #left
			td_cell_text += 'border-bottom: 3px solid #000000; '
		elif edge_binary[2] == '2': #left
			td_cell_text += 'border-bottom: 9px double #000000; '
	elif location_binary == '01': #top-right
		if edge_binary[0] == '1': #up
			td_cell_text += 'border-left: 3px solid #000000; '
		if edge_binary[3] == '1': #right
			td_cell_text += 'border-bottom: 3px solid #000000; '
		elif edge_binary[3] == '2': #right
			td_cell_text += 'border-bottom: 9px double #000000; '
	elif location_binary == '10': #bottom-left
		if edge_binary[1] == '1': #down
			td_cell_text += 'border-right: 3px solid #000000; '
		if edge_binary[2] == '1': #left
			td_cell_text += 'border-top: 3px solid #000000; '
		elif edge_binary[2] == '2': #left
			td_cell_text += 'border-top: 9px double #000000; '
	elif location_binary == '11': #bottom-right
		if edge_binary[1] == '1': #down
			td_cell_text += 'border-left: 3px solid #000000; '
		if edge_binary[3] == '1': #right
			td_cell_text += 'border-top: 3px solid #000000; '
		elif edge_binary[3] == '2': #right
			td_cell_text += 'border-top: 9px double #000000; '
	td_cell_text += '">&nbsp;</td> '
	#print(td_cell_text)
	return td_cell_text

#===============================
def makeShapeNameTableTD_Cell(shape_name):
	binary_edges = shape_binary_edges[shape_name]
	shape_html_text = ''
	shape_html_text += '<! --- START {0} --->'.format(shape_name)
	shape_html_text += '<td align="center" style="vertical-align: middle; padding: 0; margin: 0; line-height: 0px; "> '
	shape_html_text += '<table border="0" cellpadding="0" cellspacing="0" '
	shape_html_text += ' style="padding: 0; margin: 0; width: {0}px; height: {0}px; border-collapse: collapse; border-style: hidden;"> '.format(table_cell_dimension)
	shape_html_text += '<tbody><tr> '
	shape_html_text += tabelEdgeTD_Cell('00', binary_edges)
	shape_html_text += tabelEdgeTD_Cell('01', binary_edges)
	shape_html_text += '</tr><tr> '
	shape_html_text += tabelEdgeTD_Cell('10', binary_edges)
	shape_html_text += tabelEdgeTD_Cell('11', binary_edges)
	shape_html_text += '</tr></tbody></table></td> '
	shape_html_text += '<! --- END {0} --->'.format(shape_name)
	return shape_html_text

#===============================
def mirrorPedigree(code_string):
	code_lines = code_string.split('%')
	mirror_code_lines = []
	for code_line in code_lines:
		mirror_code_line = code_line[::-1]
		#u <-> L
		mirror_code_line = mirror_code_line.replace('u', '@')
		mirror_code_line = mirror_code_line.replace('L', 'u')
		mirror_code_line = mirror_code_line.replace('@', 'L')
		#r <-> d
		mirror_code_line = mirror_code_line.replace('r', '@')
		mirror_code_line = mirror_code_line.replace('d', 'r')
		mirror_code_line = mirror_code_line.replace('@', 'd')

		mirror_code_lines.append(mirror_code_line)
	mirror_code_string = '%'.join(mirror_code_lines)
	return mirror_code_string

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
		char_name = short_hand_lookup[char]
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
	html_code = ('<p><table cellpadding="0" cellspacing="0" style='
		+ '"padding: 0; margin: 0; border-collapse: collapse; border: 3px solid silver; '
		+ 'width: {0}px; height: {1}px"'.format(max_num_col * table_cell_dimension, num_row * table_cell_dimension,)
		+ '><tr>'
		+ html_code
		+ '</tr></table></p><p>&nbsp;</p>'
	)
	return html_code


#===============================
#===============================
#===============================
#===============================
if __name__ == '__main__':
	code_string = (	 "#To..#To%"
					+"r^d...|.%"
					+"x.*-T-#.%"
					+"....|...%"
					+"....x..."
				)
	#x-linked recessive
	code_string = (	 "#To..xTo%"
					+"r^d...|.%"
					+"#.x-T-*.%"
					+"r-T-+-d.%"
					+"x.o.x.x."
				)
	code_string = (	 "#To..#To....%"
					+".|.r-T^T-d..%"
					+".|.x.*.|.#To%"
					+".x--T--o..|.%"
					+"...r^d....|.%"
					+".o-x.xTo..o.%"
					+".r^d..|.....%"
					+".x.*..*.....%"
				)
	code_string = (	 "#To.#To.#To.#To%"
					+"r^d.r^d.r^d.r^d%"
					+"#.oT#.oT#.oT#.o%"
					+"..r^d.r^d.r^d..%"
					+"oT#.oT#.oT#.oT#%"
					+"r^d.r^d.r^d.r^d%"
					+"#.o.#.o.#.o.#.o%"
				)
	code_string = (	 "#To.#To.#To.#To%"
					+"r^d.r^d.r^d.r^d%"
					+"o.oT#.o.#.oT#.#%"
					+"..r^d.....r^d..%"
					+"oT#.o--T--#.oT#%"
					+"r^d...r^d...r^d%"
					+"#.o...o.#...#.o%"
				)
	code_string = (	 "#To.#To.#To.#To%"
					+"r^d.r^d.r^d.r^d%"
					+"o.*T#.o.#.oTx.#%"
					+"..r^d.....r^d..%"
					+"oT#.o--T--#.oT#%"
					+"r^d...r^d...r^d%"
					+"#.*...o.x...#.o%"
				)
	code_string = 	("#To.#To.#To.xTo%"
	+"r^d.r^d.r^d.r^d%"
	+"o.oT#.o.#.oTx.x%"
	+"..r^d.....r^d..%"
	+"oT#.o--T--x.oT#%"
	+"r^d.r-T^T-d.r^d%"
	+"#.o.o.x.o.x.#.o%"
	)
	code = '<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;"><tr>'
	for name in character_sizes.keys():
		code += makeCharacterTD_Cell(name)
	code += '</tr></table>'
	#print(code)
	code = translateCode(code_string)
	print(code)

#THE END
