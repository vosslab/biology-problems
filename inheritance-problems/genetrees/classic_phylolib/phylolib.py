#!/usr/bin/env python3

#NOTE: phylolib2 is much better, use that when you can

import sys
import itertools

sys.path.append('classic_phylolib')
from phylolib3leaves import *
from phylolib4leaves import *
from phylolib5leaves import *

#https://arxiv.org/pdf/1902.03321.pdf

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

#====================================================================================
#====================================================================================
#====================================================================================

if __name__ == '__main__':
	#comb_tree_4_leaves_html(['a','b','c','d'], distances=[6,10,12])
	#balanced_tree_4_leaves_html(['a','b','c','d'], distances=[6,10,12])

	#giraffe_tree_5_leaves_html(['a','b','c','d','e'], distances=[6,6,12,14])
	#comb_tree_5_leaves_html(['a','b','c','d','e'], distances=[6,10,12,14])
	#balanced_tree_5_leaves_type_1_html(['a','b','c','d','e'], distances=[3,6,9,12])
	#balanced_tree_5_leaves_type_2_html(['a','b','c','d','e'], distances=[3,6,9,12])
	#balanced_tree_5_leaves_type_3_html(['a','b','c','d','e'], distances=[3,6,9,12])

	t = comb_tree_3_leaves_ascii(['Asian elephant', 'African elephant', 'Woolly mammoth'])
	print(t)
	print('')
	t = comb_tree_3_leaves_alternate_ascii(['African elephant', 'Asian elephant', 'Woolly mammoth'])
	print(t)
	print('')
	t = comb_tree_3_leaves_alternate_ascii(['Asian elephant', 'African elephant', 'Woolly mammoth'])
	print(t)
	print('')
	t = balanced_tree_3_leaves_ascii(['Asian elephant', 'African elephant', 'Woolly mammoth'])
	print(t)

#THE END
