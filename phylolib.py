#!/usr/bin/env python

import itertools

space = " "
dash = '_'
bar = '|'

#https://arxiv.org/pdf/1902.03321.pdf

white_border = 'border: 0px solid white; '
black_bottom = 'border-bottom: 3px solid black; '
black_top = 'border-bottom: 3px solid black; '
black_left = 'border-left: 3px solid black; '
black_right = 'border-right: 3px solid black; '
middle = 'vertical-align: middle; '

def comb_safe_permutations(genes):
	complete_set = itertools.permutations(genes, len(genes))
	comb_safe_set = list(complete_set)
	for p in comb_safe_set:
		#swap first two elements
		q = list(p)
		q[0], q[1] = q[1], q[0]
		r = tuple(q)
		comb_safe_set.remove(r)
	#print(comb_safe_set)
	return comb_safe_set

def comb_fail_permutations(genes):
	complete_set = list(itertools.permutations(genes, len(genes)))
	comb_fail_set = []
	first_two = (complete_set[0][0], complete_set[0][1])
	for p in complete_set:
		if p[0] not in first_two:
			continue
		if p[1] not in first_two:
			continue
		comb_fail_set.append(p)
	#print(comb_fail_set)
	return comb_fail_set


def td_cell(code):
	line = ' 3px solid black; '
	td_cell = ' <td style="border: 0px solid white; '
	if '|' in code:
		td_cell += 'border-right:'+line
	if '_' in code:
		td_cell += 'border-bottom:'+line
	td_cell += '"></td>' # third line
	return td_cell

def td_cell_old(left, right, top, bottom):
	line = ' 3px solid black; '
	td_cell = ' <td style="border: 0px solid white; '
	if left == 1 or left == True:
		td_cell += 'border-left:'+line
	if right == 1 or right == True:
		td_cell += 'border-right:'+line
	if top == 1 or top == True:
		td_cell += 'border-top:'+line
	if bottom == 1 or bottom == True:
		td_cell += 'border-bottom:'+line
	td_cell += '"></td>' # third line
	return td_cell

def letter_cell(text):
	white_border = 'border: 0px solid white; '
	middle = 'vertical-align: middle; '
	alignspan = ' align="left" rowspan="2" '
	td_cell = ' <td style="'+white_border+middle+'"'+alignspan+'>'
	td_cell += '&nbsp;<span style="font-size: x-large;">'
	td_cell += '{0}</span></td>'.format(text) # value
	return td_cell

def comb_tree_3_leaves_ascii(values, distances=None):
	# values = ['a','b','c']
	# distances = [2, 3]; 3 >2
	# format = (a,b),c
	# 5 rows are needed
	if distances is None:
		distances = (2, 3)
	if distances[0] >= distances[1]:
		return None

	#row1 = "         ____ a"
	#row2 = "    ____|     "
	#row3 = "   |    |____ b"
	#row4 = " __|          "
	#row5 = "   |_________ c"
	diffdistance = distances[1] - distances[0]
	row1 = ''
	row1 += space * int(4 + 2*diffdistance + 1)
	row1 += dash * int(2 * distances[0])
	row1 += space
	row1 += values[0]
	#===============
	row2 = ''
	row2 += space * 4
	row2 += dash * int(2 * diffdistance)
	row2 += bar
	row2 += space * int(2 * distances[0] + 1)
	row2 += '.'
	#===============
	row3 = ''
	row3 += space * 3
	row3 += bar
	row3 += space * int(2 * diffdistance)
	row3 += bar
	row3 += dash * int(2 * distances[0])
	row3 += space
	row3 += values[1]
	#===============
	row4 = ''
	row4 += space
	row4 += dash * 2
	row4 += bar
	row4 += space * int(2 * distances[1] + 2)
	row4 += '.'
	#===============
	row5 = ''
	row5 += space * 3
	row5 += bar
	row5 += dash * int(2 * distances[1] + 1)
	row5 += space
	row5 += values[2]
	#===============
	tree = row1 + '\n' + row2 + '\n'  + row3 + '\n' + row4 + '\n' + row5 + '\n'
	return tree


def comb_tree_3_leaves_html(values, distances=None):
	# values = ['a','b','c']
	# distances = [2, 3]; 3 >2
	# format = (a,b),c
	# 5 rows are needed
	if distances is None:
		distances = (2, 3)
	if distances[0] >= distances[1]:
		return None
	#row1 = "         ____ a"
	#row2 = "    ____|      "
	#row3 = "   |    |____ b"
	#row4 = " __|           "
	#row5 = "   |_________ c"
	diffdistance = distances[1] - distances[0]
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format(diffdistance*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'

	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def comb_tree_3_leaves_alternate_ascii(values, distances=None):
	# values = ['a','b','c']
	# distances = [2, 3]; 3 >2
	# format = (a,b),c
	# 5 rows are needed
	if distances is None:
		distances = (2, 3)
	if distances[0] >= distances[1]:
		return None

	#row1 = "    _________ a"
	#row4 = "   |           "
	#row1 = " --|     ____ b"
	#row2 = "   |____|      "
	#row3 = "        |____ c"
	diffdistance = distances[1] - distances[0]
	row1 = ''
	row1 += space * 4
	row1 += dash * int(2 * distances[1] + 1)
	row1 += space
	row1 += values[0]
	#===============
	row2 = ''
	row2 += space * 3
	row2 += bar
	row2 += space * int(2 * distances[1] + 2)
	row2 += '.'
	#===============
	row3 = ''
	row3 += space
	row3 += dash * 2
	row3 += bar
	row3 += space * int(2*diffdistance + 1)
	row3 += dash * int(2 * distances[0])
	row3 += space
	row3 += values[1]
	#===============
	row4 = ''
	row4 += space * 3
	row4 += bar
	row4 += dash * int(2 * diffdistance)
	row4 += bar
	row4 += space * int(2 * distances[0] + 1)
	row4 += '.'
	#===============
	row5 = ''
	row5 += space * int(2 * diffdistance + 4)
	row5 += bar
	row5 += dash * int(2 * distances[0])
	row5 += space
	row5 += values[2]
	#===============
	tree = row1 + '\n' + row2 + '\n'  + row3 + '\n' + row4 + '\n' + row5 + '\n'
	return tree


def comb_tree_3_leaves_alternate_html(values, distances=None):
	# values = ['a','b','c']
	# distances = [2, 3]; 3 >2
	# format = (a,b),c
	# 5 rows are needed
	if distances is None:
		distances = (2, 3)
	if distances[0] >= distances[1]:
		return None

	#row1 = "    _________ c"
	#row4 = "   |           "
	#row1 = " --|     ____ a"
	#row2 = "   |____|      "
	#row3 = "        |____ b"
	diffdistance = distances[1] - distances[0]
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format(diffdistance*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('|_')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def balanced_tree_3_leaves_ascii(values, distances=None):
	# values = ['a','b','c']
	# distances = [2,];
	# format = (a,b,c)
	# 5 rows are needed
	if distances is None:
		distances = [2,]

	#row1 = "    ____ a"
	#row2 = "   |      "
	#row3 = " --|____ b"
	#row4 = "   |      "
	#row5 = "   |____ c"
	row1 = ''
	row1 += space * 4
	row1 += dash * int(2 * distances[0])
	row1 += space
	row1 += values[0]
	#===============
	row2 = ''
	row2 += space * 3
	row2 += bar
	row2 += space * int(2 * distances[0] + 1)
	row2 += '.'
	#===============
	row3 = ''
	row3 += space
	row3 += dash * 2
	row3 += bar
	row3 += dash * int(2 * distances[0])
	row3 += space
	row3 += values[1]
	#===============
	row4 = ''
	row4 += space * 3
	row4 += bar
	row4 += space * int(2 * distances[0] + 1)
	row4 += '.'
	#===============
	row5 = ''
	row5 += space * 3
	row5 += bar
	row5 += dash * int(2 * distances[0])
	row5 += space
	row5 += values[2]
	#===============
	tree = row1 + '\n' + row2 + '\n'  + row3 + '\n' + row4 + '\n' + row5 + '\n'
	return tree


def balanced_tree_3_leaves_html(values, distances=None):
	# values = ['a','b','c']
	# distances = [2,];
	# format = (a,b,c)
	# 5 rows are needed
	if distances is None:
		distances = [2,]

	#row1 = "    ____ a"
	#row2 = "   |      "
	#row3 = " --|____ b"
	#row4 = "   |      "
	#row5 = "   |____ c"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table



def comb_tree_4_leaves_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row1 = "           ____ a"
	#row2 = "      ____|     "
	#row3 = "     |    |____ b"
	#row4 = "   __|          "
	#row5 = "  |  |_________ c"
	#row6 = "__|              "
	#row6 = "  |____________ d"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def comb_tree_4_leaves_alternate_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row6 = "   ____________ d"
	#row6 = "  |              "
	#row1 = "__|        ____ a"
	#row2 = "  |   ____|      "
	#row3 = "  |  |    |____ b"
	#row4 = "  |__|           "
	#row5 = "     |_________ c"

	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table


def balanced_tree_4_leaves_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row1 = "           ____ a"
	#row2 = "      ____|     "
	#row3 = "     |    |____ b"
	#row4 = "   __|          "
	#row5 = "     |   ______ c"
	#row6 = "     |__|        "
	#row6 = "        |______ d"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('__')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table


def giraffe_tree_5_leaves_html(values, distances=None):
	# values = ['a','b','c', 'd', 'e']
	# distances = [2, 3, 4, 5]; 3 > 2; 4 > 3; 5 > 4
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4,5]
	#row1 = "           ____ a"
	#row2 = "      ____|     "
	#row3 = "     |    |____ b"
	#row4 = "   __|          "
	#row5 = "  |  |   ______ c"
	#row6 = "  |  |__|        "
	#row7 = "__|     |______ d"
	#row8 = "  |              "
	#row9 = "  |____________ e"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('__')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('  ')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell('  ')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[4])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def comb_tree_5_leaves_html(values, distances=None):
	# values = ['a','b','c', 'd', 'e']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4,5]
	#row1 = "              ____ a"
	#row2 = "         ____|     "
	#row3 = "        |    |____ b"
	#row4 = "      __|          "
	#row5 = "     |  |_________ c"
	#row6 = "   __|              "
	#row7 = "  |  |____________ d"
	#row8 = "__|                 "
	#row9 = "  |_______________ e"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell(' |')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[4])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def balanced_tree_5_leaves_type_1_html(values, distances=None):
	# values = ['a','b','c', 'd', 'e']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4,5]
	#row1 = "              ____ a"
	#row2 = "         ____|     "
	#row3 = "        |    |____ b"
	#row4 = "   _____|          "
	#row5 = "  |     |_________ c"
	#row6 = "__|                 "
	#row7 = "  |   ____________ d"
	#row8 = "  |__|              "
	#row9 = "     |____________ e"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell(' |')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('__')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[4])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def balanced_tree_5_leaves_type_2_html(values, distances=None):
	# values = ['a','b','c', 'd', 'e']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4,5]
	#row1 = "                 ____ a"
	#row2 = "         _______|     "
	#row3 = "        |       |____ b"
	#row4 = "   _____|              "
	#row5 = "  |     |____________ c"
	#row6 = "__|                    "
	#row7 = "  |          ________ d"
	#row8 = "  |_________|          "
	#row9 = "            |________ e"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('__')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('  ')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('  ')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('__')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[4])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def balanced_tree_5_leaves_type_3_html(values, distances=None):
	# values = ['a','b','c', 'd', 'e']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4,5]
	#row1 = "                 ____ a"
	#row2 = "   _____________|     "
	#row3 = "  |             |____ b"
	#row4 = "  |                    "
	#row5 = "__|          ________ c"
	#row6 = "  |      ___|          "
	#row7 = "  |     |   |________ d"
	#row8 = "  |_____|              "
	#row9 = "        |____________ e"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('__')+letter_cell(values[0])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('__')+td_cell('__')+td_cell('_|')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('  ')+td_cell(' |')+td_cell('__')+letter_cell(values[1])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('__')+td_cell('__')+letter_cell(values[2])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('  ')+td_cell('_|')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell(' |')+td_cell(' |')+td_cell('__')+td_cell('__')+letter_cell(values[3])
	table += '</tr><tr>'
	table += td_cell(' |')+td_cell('_|')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell(' |')+td_cell('__')+td_cell('__')+td_cell('__')+letter_cell(values[4])
	table += '</tr><tr>'
	table += td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')+td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table


if __name__ == '__main__':
	#comb_tree_4_leaves_html(['a','b','c','d'], distances=[6,10,12])
	#balanced_tree_4_leaves_html(['a','b','c','d'], distances=[6,10,12])

	#giraffe_tree_5_leaves_html(['a','b','c','d','e'], distances=[6,6,12,14])
	#comb_tree_5_leaves_html(['a','b','c','d','e'], distances=[6,10,12,14])
	#balanced_tree_5_leaves_type_1_html(['a','b','c','d','e'], distances=[3,6,9,12])
	#balanced_tree_5_leaves_type_2_html(['a','b','c','d','e'], distances=[3,6,9,12])
	#balanced_tree_5_leaves_type_3_html(['a','b','c','d','e'], distances=[3,6,9,12])

	comb_tree_3_leaves_html(['Asian elephant', 'African elephant', 'Woolly mammoth'])
	print('')
	comb_tree_3_leaves_type_2_html(['African elephant', 'Asian elephant', 'Woolly mammoth'])
	print('')
	comb_tree_3_leaves_type_2_html(['Asian elephant', 'African elephant', 'Woolly mammoth'])
	print('')
	balanced_tree_3_leaves_html(['Asian elephant', 'African elephant', 'Woolly mammoth'])


#THE END
