#==================================
#==================================
#==================================

# Definitions for tree structure terminology:
#
# Nodes: The fundamental units of a tree, representing points where branches meet.
#    Nodes can be internal (intermediate points where branches join) or terminal (leaves).
#
# Internal Nodes: Points within the tree where two branches converge. Internal nodes
#    represent hypothetical common ancestors or groupings of taxa. In the code, they
#    are labeled by numbers (e.g., '1', '2', '3') to denote the order or hierarchy
#    of branching events.
#
# Leaves: Terminal nodes of the tree, representing the taxa or observed entities
#    being compared. Leaves (e.g., 'a', 'b', 'c') are the endpoints of branches
#    and do not have child nodes.
#
# Taxa: The entities represented by the leaves of the tree, which can refer to
#    biological classifications such as species, genera, or families. In broader
#    contexts, taxa can also refer to operational units like populations, genetic
#    sequences, or other entities being compared in the analysis. Note: Individual
#    genes or organisms are not themselves taxa but may be grouped within taxa.
#
# Branches: The connections between nodes in the tree. Branches represent the
#    relationships between taxa and internal nodes, such as evolutionary connections
#    or shared traits. In the code, branches are implied by the structure of parentheses.
#
# Example Explanation for '((((a1b)3(c2d))6((e4f)5g))7h)':
#    - 'a' and 'b' are leaves connected at internal node '1'.
#    - 'c' and 'd' are leaves connected at internal node '2'.
#    - '(a1b)' and '(c2d)' are connected at internal node '3'.
#    - 'e' and 'f' are leaves connected at internal node '4'.
#    - '(e4f)' and 'g' are connected at internal node '5'.
#    - '(a1b)3(c2d)' and '((e4f)5g)' are connected at internal node '6'.
#    - The entire subtree then connects to 'h' at internal node '7'.

code_library = {
	### Number of types for number of leaves:
	# Wedderburn-Etherington numbers
	# https://oeis.org/A001190
	# unlabeled binary rooted trees (every node has out-degree 0 or 2) with n endpoints (and 2n-1 nodes in all)
	# 1, 1, 2, 3,  6, 11,  23,   46,   98,   207,   451, ...
	### Number of edge-labeled for number of leaves:
	# https://oeis.org/A000111
	# 1, 1, 2, 5, 16, 61, 272, 1385, 7936, 50521, ...

	# 2:  1 / 1
	# 3:  1 / 1
	# 4:  2 / 2
	# 5:  3 / 5
	# 6:  6 / 16
	# 7: 11 / #61
	# 8: 23 / #272
	# 9: 46 / #1385
	# 10: 98
	#   9+1: 46, 8+2: 23, 7+3: 11, 6+4: 6*2, 5+5: 3*3 - 3
	#   46 + 23 + 11 + 6*2 + 3*3 - 3 = 98
	# subtraction is (n*n - n)//2; n = 3
	# 11: 207
	#   10+1: 98, 9+2: 46, 8+3: 23, 7+4: 2*11, 6+5: 3*6
	#   98 + 46 + 23+ 2*11 + 3*6 = 207
	# 12: 451
	#   11+1: 207, 10+2: 98, 9+3: 46, 8+4: 2*23, 7+5: 3*11, 6+6: 6*6 - 15
	#   207 + 98 + 46 + 2*23+ 3*11 + 6*6 - 15 = 451
	# subtraction is (n*n - n)//2; n = 6
	# 13: 983
	#   12+1: 451, 11+2: 207, 10+3: 98, 9+4: 2*46, 8+5: 3*23, 7+6: 6*11
	#   451 + 207 + 98 + 2*46 + 3*23 + 6*11 = 983
	# 14: 2179
	#   13+1: 983, 12+2: 451, 11+3: 207, 10+4: 2*98, 9+5: 3*46, 8+6: 6*23, 7+7: 11*11 - 55
	#   983 + 451 + 207 + 2*98 + 3*46 + 6*23 + 11*11 - 55 = 2179
	# subtraction is (n*n - n)//2; n = 11

	###================================================
	## 2 leaves -- 1 type / 1 edge-labeled
	'pair':		'(a1b)',

	###================================================
	## 3 leaves -- 1 type / 1 edge-labeled
	'3comb':	'((a1b)2c)',
	#'3comb*':	'(a2(b1c))',

	###================================================
	## 4 leaves -- 2 type / 2 edge-labeled
	'4comb':		'(((a1b)2c)3d)', #type 1
	#'4comb*':		'(a3(b2(c1d)))',
	'4balanced':	'((a1b)3(c2d))', #type 2
	#'4balanced*':	'((a2b)3(c1d))',

	###================================================
	## 5 leaves	 -- 3 type / 5 edge-labeled
	'5comb':		'((((a1b)2c)3d)4e)', #type 1
	'5giraffe':		'(((a1b)3(c2d))4e)', #type 2
	#'5giraffe*':	'(((a2b)3(c1d))4e)', #type 2 alternate (extra)
	'3comb+pair1':	'(((a1b)2c)4(d3e))', #type 3 / 3 edge-labels
	'3comb+pair2':	'(((a1b)3c)4(d2e))',
	'3comb+pair3':	'(((a2b)3c)4(d1e))',

	###================================================
	###================================================
	## 6 leaves  -- 6 type / 16 edge-labeled
	'6comb':		'(((((a1b)2c)3d)4e)5f)', #type 1
	'5giraffe+1':	'((((a1b)3(c2d))4e)5f)', #type 2
	#'5giraffe*+1': 	'((((c2d)3(a1b))4e)5f)', #type 2 alternate (extra)
	#'5giraffe|+1': 	'(f5(e4((c2d)3(a1b))))', #type 2 mirror (extra)
	#'5giraffe|*+1':	'(f5(e4((a1b)3(c2d))))', #type 2 mirror/alternate (extra)
	#'5giraffe?+1': 	'((e4((a1b)3(c2d)))5f)', #type 2 e-flop (extra)
	#'5giraffe?*+1':	'((e4((c2d)3(a1b)))5f)', #type 2 e-flop/alternate (extra)
	#'5giraffe|?+1':	'(f5(((a1b)3(c2d))4e))', #type 2 mirror/e-flop (extra)
	#'5giraffe|?*+1':	'(f5(((c2d)3(a1b))4e))', #type 2 mirror/e-flop/alternate (extra)

	'3comb+pair1+1':	'((((a1b)2c)4(d3e))5f)', #type 3 / 3 edge-labels
	'3comb+pair2+1':	'((((a1b)3c)4(d2e))5f)',
	'3comb+pair3+1':	'((((a2b)3c)4(d1e))5f)',

	'4comb+pair1':	'((((a1b)2c)3d)5(e4f))', #type 4 / 4 edge-labels
	'4comb+pair2':	'((((a1b)2c)4d)5(e3f))',
	'4comb+pair3':	'((((a1b)3c)4d)5(e2f))',
	'4comb+pair4':	'((((a2b)3c)4d)5(e1f))',

	'6twohead1':	'(((a1b)3(c2d))5(e4f))', #type 5 / 4 edge-labels
	'6twohead2':	'(((a1b)4(c2d))5(e3f))',
	'6twohead3':	'(((a1b)4(c3d))5(e2f))',
	'6twohead4':	'(((a2b)4(c3d))5(e1f))',
	#'6twohead*1':	'(((a2b)3(c1d))5(e4f))',
	#'6twohead*2':	'(((a2b)4(c1d))5(e3f))',
	#'6twohead*3':	'(((a3b)4(c1d))5(e2f))',
	#'6twohead*4':	'(((a3b)4(c2d))5(e1f))',

	'6balanced1':	'(((a1b)2c)5((d3e)4f))', #type 6 / 3 edge-labels
	'6balanced2':	'(((a1b)3c)5((d2e)4f))',
	'6balanced3':	'(((a2b)3c)5((d1e)4f))',
	#'6balanced3*':	'(((a1b)4c)5((d2e)3f))',
	#'6balanced2*':	'(((a2b)4c)5((d1e)3f))',
	#'6balanced1*':	'(((a3b)4c)5((d1e)2f))',

	###================================================
	###================================================
	## 7 leaves  -- 11 type / 61 edge-labeled
	'7comb':			'((((((a1b)2c)3d)4e)5f)6g)', #type 1 / 1 edge-labels
	'5giraffe+1+1':		'(((((a1b)3(c2d))4e)5f)6g)', #type 2 / 1 edge-labels
	'3comb+pair+1+1':	'(((((a1b)2c)4(d3e))5f)6g)', #type 3 / 3 edge-labels
	'4comb+pair+1':		'(((((a1b)2c)3d)5(e4f))6g)', #type 4 / 4 edge-labels
	'6twohead1+1':		'((((a1b)3(c2d))5(e4f))6g)', #type 5 / 4 edge-labels
	'6balanced1+1':		'((((a1b)2c)5((d3e)4f))6g)', #type 6 / 3 edge-labels

	'5comb+pair':		'(((((a1b)2c)3d)4e)6(f5g))', #type 7 / 5 edge-labels
	'5giraffe+pair':	'((((a1b)3(c2d))4e)6(f5g))', #type 8 / 5 edge-labels
	'3comb+pair+pair':	'((((a1b)2c)4(d3e))6(f5g))', #type 9 / 5x3 = 15 edge-labels

	'4comb+3comb':		'((((a1b)2c)3d)6((e4f)5g))', #type 10 / (4+3+2+1) = 10 edge-labels
	'4balanced+3comb':	'(((a1b)3(c2d))6((e4f)5g))', #type 11 / (4+3+2+1) = 10 edge-labels

	###================================================
	###================================================
	## 8 leaves  -- 23 type / 272 edge-labeled
	# previous: 11 from 7 leaves
	'8comb':				'(((((((a1b)2c)3d)4e)5f)6g)7h)', #type  1 /  1 edge-labels
	'5giraffe+1+1+1':		'((((((a1b)3(c2d))4e)5f)6g)7h)', #type  2 /  1 edge-labels
	'3comb+pair+1+1+1':		'((((((a1b)2c)4(d3e))5f)6g)7h)', #type  3 /  3 edge-labels
	'4comb+pair+1+1':		'((((((a1b)2c)3d)5(e4f))6g)7h)', #type  4 /  4 edge-labels
	'6twohead1+1+1':		'(((((a1b)3(c2d))5(e4f))6g)7h)', #type  5 /  4 edge-labels
	'6balanced1+1+1':		'(((((a1b)2c)5((d3e)4f))6g)7h)', #type  6 /  3 edge-labels
	'5comb+pair+1':			'((((((a1b)2c)3d)4e)6(f5g))7h)', #type  7 /  5 edge-labels
	'5giraffe+pair+1':		'(((((a1b)3(c2d))4e)6(f5g))7h)', #type  8 /  5 edge-labels
	'3comb+pair+pair+1':	'(((((a1b)2c)4(d3e))6(f5g))7h)', #type  9 / 15 edge-labels
	'4comb+3comb+1':		'(((((a1b)2c)3d)6((e4f)5g))7h)', #type 10 / 10 edge-labels
	'4balanced+3comb+1':	'((((a1b)3(c2d))6((e4f)5g))7h)', #type 11 / 10 edge-labels

	# 6 from 6 leaves
	'6comb+pair':			'((((((a1b)2c)3d)4e)5f)7(g6h))', #type 12 /  6 edge-labels
	'5giraffe+1+pair':		'(((((a1b)3(c2d))4e)5f)7(g6h))', #type 13 /  6 edge-labels
	'3comb+pair+1+pair':	'(((((a1b)2c)4(d3e))5f)7(g6h))', #type 14 / 18 edge-labels
	'4comb+pair+pair':		'(((((a1b)2c)3d)5(e4f))7(g6h))', #type 15 / 24 edge-labels
	'6twohead1+pair':		'((((a1b)3(c2d))5(e4f))7(g6h))', #type 16 / 24 edge-labels
	'6balanced1+pair':		'((((a1b)2c)5((d3e)4f))7(g6h))', #type 17 / 18 edge-labels

	# 3 from 5 leaves
	'5comb+3comb':			'(((((a1b)2c)3d)4e)7((f5g)6h))', #type 18 / 15 edge-labels
	'5giraffe+3comb':		'((((a1b)3(c2d))4e)7((f5g)6h))', #type 19 / 15 edge-labels
	'3comb+pair+3comb':		'((((a1b)2c)4(d3e))7((f5g)6h))', #type 20 / 45 edge-labels

	# 2x2 from 4 leaves
	'8hanukkah':			'((((a1b)3c)5d)7(e6(f4(g2h))))', #type 21 / 10 edge-labels
	'8balanced':			'(((a1b)5(c3d))7((e4f)6(g2h)))', #type 22 / 10 edge-labels
	#'4balanced+4comb':		'(((a1b)3(c2d))7(((e4f)5g)6h))', #duplicate to below
	'4comb+4balanced':		'((((a1b)2c)3d)7((e4f)6(g5h)))', #type 23 / 20 edge-labels

	###================================================
	###================================================
	## 9 leaves  -- 46 type / 1385 edge-labeled
	# previous: 23 from 8 leaves
	'9comb':				'((((((((a1b)2c)3d)4e)5f)6g)7h)8i)', #type  1 /  1 edge-labels
	'5giraffe+1+1+1+1':		'(((((((a1b)3(c2d))4e)5f)6g)7h)8i)', #type  2 /  1 edge-labels
	'3comb+pair+1+1+1+1':	'(((((((a1b)2c)4(d3e))5f)6g)7h)8i)', #type  3 /  3 edge-labels
	'4comb+pair+1+1+1':		'(((((((a1b)2c)3d)5(e4f))6g)7h)8i)', #type  4 /  4 edge-labels
	'6twohead1+1+1+1':		'((((((a1b)3(c2d))5(e4f))6g)7h)8i)', #type  5 /  4 edge-labels
	'6balanced1+1+1+1':		'((((((a1b)2c)5((d3e)4f))6g)7h)8i)', #type  6 /  3 edge-labels
	'5comb+pair+1+1':		'(((((((a1b)2c)3d)4e)6(f5g))7h)8i)', #type  7 /  5 edge-labels
	'5giraffe+pair+1+1':	'((((((a1b)3(c2d))4e)6(f5g))7h)8i)', #type  8 /  5 edge-labels
	'3comb+pair+pair+1+1':	'((((((a1b)2c)4(d3e))6(f5g))7h)8i)', #type  9 / 15 edge-labels
	'4comb+3comb+1+1':		'((((((a1b)2c)3d)6((e4f)5g))7h)8i)', #type 10 / 10 edge-labels
	'4balanced+3comb+1+1':	'(((((a1b)3(c2d))6((e4f)5g))7h)8i)', #type 11 / 10 edge-labels
	'6comb+pair+1':			'(((((((a1b)2c)3d)4e)5f)7(g6h))8i)', #type 12 /  6 edge-labels
	'5giraffe+1+pair+1':	'((((((a1b)3(c2d))4e)5f)7(g6h))8i)', #type 13 /  6 edge-labels
	'3comb+pair+1+pair+1':	'((((((a1b)2c)4(d3e))5f)7(g6h))8i)', #type 14 / 18 edge-labels
	'4comb+pair+pair+1':	'((((((a1b)2c)3d)5(e4f))7(g6h))8i)', #type 15 / 24 edge-labels
	'6twohead1+pair+1':		'(((((a1b)3(c2d))5(e4f))7(g6h))8i)', #type 16 / 24 edge-labels
	'6balanced1+pair+1':	'(((((a1b)2c)5((d3e)4f))7(g6h))8i)', #type 17 / 18 edge-labels
	'5comb+3comb+1':		'((((((a1b)2c)3d)4e)7((f5g)6h))8i)', #type 18 / 15 edge-labels
	'5giraffe+3comb+1':		'(((((a1b)3(c2d))4e)7((f5g)6h))8i)', #type 19 / 15 edge-labels
	'3comb+pair+3comb+1':	'(((((a1b)2c)4(d3e))7((f5g)6h))8i)', #type 20 / 45 edge-labels
	'8hanukkah+1':			'(((((a1b)3c)5d)7(e6(f4(g2h))))8i)', #type 21 / 10 edge-labels
	'8balanced+1':			'((((a1b)5(c3d))7((e4f)6(g2h)))8i)', #type 22 / 10 edge-labels
	'4comb+4balanced+1':	'(((((a1b)2c)3d)7((e4f)6(g5h)))8i)', #type 23 / 10 edge-labels

	# 11 from 7 leaves
	'7comb+pair':			'(((((((a1b)2c)3d)4e)5f)6g)8(h7i))', #type 24 /  7 edge-labels
	'5giraffe+1+1+pair':	'((((((a1b)3(c2d))4e)5f)6g)8(h7i))', #type 25 /  7 edge-labels
	'3comb+pair+1+1+pair':	'((((((a1b)2c)4(d3e))5f)6g)8(h7i))', #type 26 / 21 edge-labels
	'4comb+pair+1+pair':	'((((((a1b)2c)3d)5(e4f))6g)8(h7i))', #type 27 / 28 edge-labels
	'6twohead1+1+pair':		'(((((a1b)3(c2d))5(e4f))6g)8(h7i))', #type 28 / 28 edge-labels
	'6balanced1+1+pair':	'(((((a1b)2c)5((d3e)4f))6g)8(h7i))', #type 29 / 21 edge-labels
	'5comb+pair+pair':		'((((((a1b)2c)3d)4e)6(f5g))8(h7i))', #type 30 / 35 edge-labels
	'5giraffe+pair+pair':	'(((((a1b)3(c2d))4e)6(f5g))8(h7i))', #type 31 / 35 edge-labels
	'3comb+pair+pair+pair':	'(((((a1b)2c)4(d3e))6(f5g))8(h7i))', #type 32 /105 edge-labels
	'4comb+3comb+pair':		'(((((a1b)2c)3d)6((e4f)5g))8(h7i))', #type 33 / 70 edge-labels
	'4balanced+3comb+pair':	'((((a1b)3(c2d))6((e4f)5g))8(h7i))', #type 34 / 70 edge-labels

	# 6 from 6 leaves
	'6comb+3comb':			'((((((a1b)2c)3d)4e)5f)8((g6h)7i))', #type 35 / 21 edge-labels
	'5giraffe+1+3comb':		'(((((a1b)3(c2d))4e)5f)8((g6h)7i))', #type 36 / 21 edge-labels
	'3comb+pair+1+3comb':	'(((((a1b)2c)4(d3e))5f)8((g6h)7i))', #type 37 / 63 edge-labels
	'4comb+pair+3comb':		'(((((a1b)2c)3d)5(e4f))8((g6h)7i))', #type 38 / 84 edge-labels
	'6twohead1+3comb':		'((((a1b)3(c2d))5(e4f))8((g6h)7i))', #type 39 / 84 edge-labels
	'6balanced1+3comb':		'((((a1b)2c)5((d3e)4f))8((g6h)7i))', #type 40 / 63 edge-labels

	# 2x3 from 5 leaves
	'5comb+4comb':			'(((((a1b)2c)3d)4e)8(((f5g)6h)7i))', #type 41 / 15 edge-labels
	'5giraffe+4comb':		'((((a1b)3(c2d))4e)8(((f5g)6h)7i))', #type 42 / 15 edge-labels
	'3comb+pair+4comb':		'((((a1b)2c)4(d3e))8(((f5g)6h)7i))', #type 43 / 45 edge-labels
	'5comb+4balanced':		'(((((a1b)2c)3d)4e)8(((f5g)6h)7i))', #type 44 / 15 edge-labels
	'5giraffe+4balanced':	'((((a1b)3(c2d))4e)8(((f5g)6h)7i))', #type 45 / 15 edge-labels
	'3comb+pair+4balanced':	'((((a1b)2c)4(d3e))8(((f5g)6h)7i))', #type 46 / 45 edge-labels

	###================================================
	###================================================
	## 10 leaves  -- 98 type / 7936 edge-labeled
	# previous: 46 types from 9 leaves

	### Number of types for number of leaves:
	# Wedderburn-Etherington numbers
	# https://oeis.org/A001190
	# unlabeled binary rooted trees (every node has out-degree 0 or 2) with n endpoints (and 2n-1 nodes in all)
	# 1, 1, 2, 3,  6, 11,  23,   46,   98,   207,   451, ...
	### Number of edge-labeled for number of leaves:
	# https://oeis.org/A000111
	# 1, 1, 2, 5, 16, 61, 272, 1385, 7936, 50521, ...

	###================================================
	###================================================
}

if __name__ == '__main__':
	import random
	all_codes = list(code_library.values())
	tree_code = random.choice(all_codes)
	print(f"tree_code = {tree_code}")
