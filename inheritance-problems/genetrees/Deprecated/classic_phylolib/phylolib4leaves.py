#cannot be run on its own, requires phylolib

#NOTE: phylolib2 is much better, use that when you can
print("\033[93m\033[1mNOTE: classic_phylolib is deprecated and phylolib2 is much better. Use that when you can.\033[0m")

import random
import phylolib_common as phc

space = " "
dash = '_'
bar = '|'

distance_multiplier = 15

#====================================================================================
#====================================================================================
#====================================================================================

def random_tree_4_leaves_html(values, distances=None):
	r = random.randint(1,6)
	if r == 1:
		return comb_tree_4_leaves_html(values, distances)
	elif r == 2:
		#alt_values = (values[3], values[0], values[1], values[2])
		# ^ Don't do this the code already does this!
		return comb_tree_4_leaves_alternate_html(values, distances)
	elif r == 3:
		return comb_tree_4_leaves_invert_html(values, distances)
	elif r == 4:
		return comb_tree_4_leaves_alternate_invert_html(values, distances)
	elif r == 5:
		return balanced_tree_4_leaves_html(values, distances)
	elif r == 6:
		return balanced_tree_4_leaves_invert_html(values, distances)

def random_comb_tree_4_leaves_html(values, distances=None):
	r = random.randint(1,4)
	if r == 1:
		return comb_tree_4_leaves_html(values, distances)
	elif r == 2:
		#alt_values = (values[3], values[0], values[1], values[2])
		# ^ Don't do this the code already does this!
		return comb_tree_4_leaves_alternate_html(values, distances)
	elif r == 3:
		return comb_tree_4_leaves_invert_html(values, distances)
	elif r == 4:
		return comb_tree_4_leaves_alternate_invert_html(values, distances)

def random_balanced_tree_4_leaves_html(values, distances=None):
	r = random.randint(1,2)
	if r == 1:
		return balanced_tree_4_leaves_html(values, distances)
	elif r == 2:
		return balanced_tree_4_leaves_invert_html(values, distances)

def comb_tree_4_leaves_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row1 = "         ____ a"
	#row2 = "      __|      "
	#row3 = "     |  |____ b"
	#row4 = "   __|         "
	#row5 = "  |  |_______ c"
	#row6 = "__|            "
	#row7 = "  |__________ d"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def comb_tree_4_leaves_invert_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row7 = "   __________ d"
	#row6 = "__|            "
	#row5 = "  |   _______ c"
	#row4 = "  |__|         "
	#row1 = "     |   ____ a"
	#row2 = "     |__|      "
	#row3 = "        |____ b"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def comb_tree_4_leaves_alternate_invert_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row5 = "      _________ c"
	#row6 = "     |           "
	#row1 = "   __|     ____ a"
	#row2 = "  |  |____|      "
	#row3 = "__|       |____ b"
	#row4 = "  |             "
	#row6 = "  |____________ d"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
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
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

def balanced_tree_4_leaves_invert_html(values, distances=None):
	# values = ['a','b','c', 'd']
	# distances = [2, 3, 4]; 3 > 2; 4 > 3
	# format = ((a,b),c),d
	# 5 rows are needed
	if distances is None:
		distances = [2,3,4]
	#row5 = "         ______ c"
	#row6 = "      __|        "
	#row6 = "     |  |______ d"
	#row4 = "   __|          "
	#row1 = "     |     ____ a"
	#row2 = "     |____|     "
	#row3 = "          |____ b"
	table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	table += '<colgroup width="30"></colgroup>'
	table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*distance_multiplier)
	table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*distance_multiplier)
	table += '<colgroup width="30"></colgroup>'
	table += '<tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[2])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('__')+phc.letter_cell(values[3])
	table += '</tr><tr>'
	table += phc.td_cell('_|')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('__')+phc.letter_cell(values[0])
	table += '</tr><tr>'
	table += phc.td_cell(' |')+phc.td_cell('__')+phc.td_cell('_|')+phc.td_cell('  ')
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell(' |')+phc.td_cell('__')+phc.letter_cell(values[1])
	table += '</tr><tr>'
	table += phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')+phc.td_cell('  ')
	table += '</tr>'
	table += '</table>'
	return table

#====================================================================================
#====================================================================================
#====================================================================================
#THE END
