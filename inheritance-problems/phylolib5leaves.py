#cannot be run on its own, requires phylolib

#NOTE: phylolib2 is much better, use that when you can


import sys
import random
import phylolib_common as phc

space = " "
dash = '_'
bar = '|'

distance_multiplier = 15

#====================================================================================
#====================================================================================
#====================================================================================

def random_tree_5_leaves_html(values, distances=None):
	r = random.randint(1,5)
	if r == 1:
		return giraffe_tree_5_leaves_html(values, distances)
	elif r == 2:
		return comb_tree_5_leaves_html(values, distances)
	elif r == 3:
		return balanced_tree_5_leaves_type_1_html(values, distances)
	elif r == 4:
		return balanced_tree_5_leaves_type_2_html(values, distances)
	elif r == 5:
		return balanced_tree_5_leaves_type_3_html(values, distances)

def random_comb_tree_5_leaves_html(values, distances=None):
	sys.exit(1)
	r = random.randint(1,2)
	if r == 1:
		return comb_tree_5_leaves_html(values, distances)
	elif r == 2:
		return comb_tree_5_leaves_html(values, distances)

def random_balanced_tree_5_leaves_type_1_html(values, distances=None):
	r = random.randint(1,2)
	if r == 1:
		return balanced_tree_5_leaves_type_1_html(values, distances)
	elif r == 2:
		return balanced_tree_5_leaves_type_1_alternate_html(values, distances)


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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[4])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[4])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[4])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def balanced_tree_5_leaves_type_1_alternate_html(values, distances=None):
	# values = ['a','b','c', 'd', 'e']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4,5]
	#row5 = "         _________ c"
	#row4 = "   _____|          "
	#row1 = "  |     |     ____ a"
	#row2 = "  |     |____|     "
	#row3 = "  |          |____ b"
	#row6 = "__|                 "
	#row7 = "  |   ____________ d"
	#row8 = "  |__|              "
	#row9 = "     |____________ e"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[4])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[4])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[4])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

#====================================================================================
#====================================================================================
#====================================================================================
#THE END
