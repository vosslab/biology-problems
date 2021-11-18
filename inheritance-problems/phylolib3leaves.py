#cannot be run on its own, requires phylolib

import random
import phylolib_common as phc

space = " "
dash = '_'
bar = '|'

#====================================================================================
#====================================================================================
#====================================================================================

def random_tree_3_leaves_html(values, distances=None):
	r = random.randint(1,3)
	if r == 1:
		return comb_tree_3_leaves_html(values, distances)
	elif r == 2:
		return comb_tree_3_leaves_alternate_html(values, distances)
	elif r == 3:
		return balanced_tree_3_leaves_html(values, distances)

def random_comb_tree_3_leaves_html(values, distances=None):
	r = random.randint(1,2)
	if r == 1:
		return comb_tree_3_leaves_html(values, distances)
	elif r == 2:
		return comb_tree_3_leaves_alternate_html(values, distances)

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
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('|_')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

#====================================================================================
#====================================================================================
#====================================================================================
#THE END
