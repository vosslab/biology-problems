#base class, import bare minimum

#NOTE: phylolib2 is much better, use that when you can

import numpy
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

def empty_array():
	char_array3 = numpy.empty((3, 3), dtype='str')
	char_array3[:] = ' '

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

#====================================================================================
#====================================================================================
#====================================================================================
#THE END
