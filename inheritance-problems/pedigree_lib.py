#!/usr/bin/env python

import numpy
import itertools

space = " "
dash = '_'
bar = '|'

#https://arxiv.org/pdf/1902.03321.pdf

def makeCharacterTD_Cell(character_name):
	character_unicode = character_unicodes[character_name]
	fontsize = character_sizes[character_name]
	html_text = makeTD_Cell(character_name, character_unicode, fontsize)
	return html_text

def makeTD_Cell(comment_text, character_unicode, fontsize):
	character_unicode = character_unicodes[character_name]
	fontsize = character_sizes[character_name]
	html_text = ''
	if comment_name is not None:
		html_text += '<!--- {0} ---> '.format(comment_text)
	html_text += '<td align="center" style="'
	if fontsize is not None:
		'font-size: {0:d}pt; '.format(fontsize)
	html_text += 'vertical-align: middle; width: 80px; height: 80px;">'
	html_text += '{0}</td>'.format(character_unicode)
	return html_text


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

character_unicodes = {
	'LEFT-HALF BLACK SQUARE': '&#x25E7;',
	'RIGHT-HALF BLACK SQUARE': '&#x25E8;',
	'BLACK SQUARE': '&#x25FB;',
	'WHITE SQUARE': '&#x25FC;',
	'LEFT-HALF BLACK CIRCLE': '&#x25D0;',
	'RIGHT-HALF BLACK CIRCLE': '&#x25D1;',
	'BLACK CIRCLE': '&#x2B24;',
	'WHITE CIRCLE': '&xcirc;',
}

short_hand_lookup = {
	'.': 'SPACE',
	'x': 'BLACK SQUARE',
	'#': 'WHITE SQUARE',
	'*': 'BLACK CIRCLE',
	'o': 'WHITE CIRCLE',
	'T': 'T SHAPE',
	'|': 'VERTICAL LINE SHAPE',
	'^': 'PERPENDICULAR TENT SHAPE',
	'+': 'PLUS SHAPE',
	'-': 'HORIZONTAL LINE SHAPE',
	'L': 'UP-RIGHT ELBOW SHAPE',
	'u': 'UP-LEFT ELBOW SHAPE',
	'r': 'DOWN-RIGHT ELBOW SHAPE',
	'd': 'DOWN-LEFT ELBOW SHAPE',
}


def makeShapeNameTableTD_Cell(shape_name):
	pass

#===============================

def translateCode(code_string):
	html_code = '<table><tr>'
	for char in List(code_string):
		char_name = short_hand_lookup[char]
		if char_name.endswith('SHAPE'):
			html_code += makeShapeNameTableTD_Cell(char)
		elif char_name.endswith('CIRCLE') or char_name.endswith('SQUARE'):
			html_code += makeCharacterTD_Cell(char_name)
		elif char_name == 'SPACE':
			html_code += makeTD_Cell(None, '&nbsp;', None)
	return html_code

if __name__ == '__main__':
	code_string = (	 "#To..#To"
					+"d^r...|."
					+"x.*-T-#."
					+"....|..."
					+"....x..."
				)
	code = '<table><tr>'
	for name in character_sizes.keys():
		code += makeCharacterTD_Cell(name)
	code += '</tr></table>'
	print(code)

#THE END
