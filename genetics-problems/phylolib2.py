#!/usr/bin/env python

import re
import copy
import numpy

class ascii_tree(object):
	def __init__(self):
		self.code = None
		self.leaves = None
		self.char_array = None

	def code_to_number_of_leaves(self, code):
		return len(self.code_to_char_list(code))

	def create_empty_array(self, leaves=None):
		if leaves is None:
			leaves = self.leaves
		#rows: 3->5, 4->7, 5->9 => rows = 2*leaves - 1
		rows = 2*leaves - 1
		#cols =
		cols = 3*leaves + 3
		char_array = numpy.empty((rows, cols), dtype='str')
		char_array[:] = ' '
		return char_array

	def print_array(self):
		lines = []
		shape = self.char_array.shape
		for rownum in range(shape[0]):
			line = ''.join(self.char_array[rownum]) + ' '
			print(line)
		print("")

	def code_to_char_list(self, code):
		#print(code)
		re_list = re.split("[^a-zA-Z]*", code)
		#re_list has extra spaces
		#char_str = ''.join(re_list)
		#char_list = list(char_str)
		char_list = list(filter(None, re_list))
		return char_list

	def get_edge_number_for_string(self, my_str, code):
		if len(my_str) == self.leaves:
			return None
		index = code.find(my_str)
		digit1 = code[index-1]
		try:
			digit2 = code[index+len(my_str)]
		except IndexError:
			digit2 = 'None'
		if digit1.isdigit():
			if digit2.isdigit():
				print("character {0} has two edge numbers {1} and {2}".format(my_str, digit1, digit2))
				raise
			edge_number = int(digit1)
		elif digit2.isdigit():
			edge_number = int(digit2)
		else:
			print("character {0} has no edge number".format(my_str))
			return None
		return edge_number

	def edge_number_to_line_length(self, edge_number):
		#line_length = 3*edge_number + 1
		#self.edge_number_to_line_length = {1:4, 2:7, 3:10, 4:13, 5:16, 6:19, 7:22}
		line_length = 3*edge_number + 1
		return line_length

	def make_tree(self, code=None):
		if code is None:
			code = '(((a3b)4((c1d)2e))5f)'
			code = '(((a1b)4((c2d)3e))5f)'
			code = '(((a3b)5((c1d)4e))6(f2g))'
		self.code = code
		self.leaves = self.code_to_number_of_leaves(self.code)
		self.char_array = self.create_empty_array(self.leaves)

		char_list = self.code_to_char_list(code)
		#print(char_list)
		char_edge_number = {}
		char_row_number = {}
		edge_number_char_list = {}
		for i,character in enumerate(char_list):
			row = i*2
			char_row_number[character] = row
			self.char_array[row, -1] = character
			edge_number = self.get_edge_number_for_string(character, code)
			char_edge_number[character] = edge_number
			edge_number_char_list[edge_number] = edge_number_char_list.get(edge_number, []) + [character]
			line_length = self.edge_number_to_line_length(edge_number)
			self.char_array[row, -line_length-2:-2] = '_'
		#print(char_edge_number)
		#print(edge_number_char_list)

		newcode = copy.copy(code)
		for edge_number in range(1, self.leaves):
			#print("===========\nedge_number {0} of {1} for code: '{2}'".format(edge_number,self.leaves-1,newcode))
			index = newcode.find(str(edge_number))
			#char1 = newcode[index-1]
			#char2 = newcode[index+1]
			#if char1 in '()' or char2 in '()':
			#	continue
			char1 = edge_number_char_list[edge_number][0]
			char2 = edge_number_char_list[edge_number][1]
			subcode = "({0}{1}{2})".format(char1,edge_number,char2)
			if not subcode in newcode:
				#swap order
				char2, char1 = char1, char2
				subcode = "({0}{1}{2})".format(char1,edge_number,char2)
			if not subcode in newcode:
				print('{0} not found in {1}'.format(subcode, newcode))
				raise
			#print(char1, char2)

			row1 = char_row_number[char1]
			row2 = char_row_number[char2]
			midrow = (row1 + row2 + 1)//2

			combined = "{0}{2}".format(char1,edge_number,char2)
			#print("{0} -> {1},".format(subcode, combined))
			newcode = newcode.replace(subcode, combined)
			#print("{0} -> {1},".format(code, newcode))
			new_edge_number = self.get_edge_number_for_string(combined, newcode)
			if new_edge_number is not None:
				edge_number_char_list[new_edge_number] = edge_number_char_list.get(new_edge_number, []) + [combined]
			char_row_number[combined] = midrow
			#print(char_row_number)


			#print(row1, row2, midrow)
			line_length = self.edge_number_to_line_length(edge_number)
			if new_edge_number is not None:
				next_line_length = self.edge_number_to_line_length(new_edge_number)
				#print(line_length, next_line_length)
				gap = next_line_length - line_length - 1
			else:
				gap = 2
			#self.char_array[row1, -line_length-2:-2] = '_'
			#self.char_array[row2, -line_length-2:-2] = '_'
			self.char_array[midrow, -line_length-3-gap:-line_length-3] = '_'
			self.char_array[row1+1:row2+1, -line_length-3] = '|'

		return

code_library = {
	### Number of types for number of leaves:
	# Wedderburn-Etherington numbers
	# https://oeis.org/A001190
	# unlabeled binary rooted trees (every node has out-degree 0 or 2) with n endpoints (and 2n-1 nodes in all)
	# 1, 1, 2, 3,  6, 11,  23,   46,   98,   207,   451, ...
	### Number of edge-labeled for number of leaves:
	# https://oeis.org/A000111
	# 1, 1, 2, 5, 16, 61, 272, 1385, 7936, 50521, ...

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

	## 2 leaves -- 1 type / 1 edge-labeled
	'pair':		'(a1b)',

	## 3 leaves -- 1 type / 1 edge-labeled
	'3comb':	'((a1b)2c)',
	#'3comb*':	'(a2(b1c))',

	## 4 leaves -- 2 type / 2 edge-labeled
	'4comb':		'(((a1b)2c)3d)', #type 1
	#'4comb*':		'(a3(b2(c1d)))',
	'4balanced':	'((a1b)3(c2d))', #type 2
	#'4balanced*':	'((a2b)3(c1d))',

	## 5 leaves	 -- 3 type / 5 edge-labeled
	'5comb':		'((((a1b)2c)3d)4e)', #type 1
	'5giraffe':		'(((a1b)3(c2d))4e)', #type 2
	#'5giraffe*':	'(((a2b)3(c1d))4e)',
	'3comb+pair1':	'(((a1b)2c)4(d3e))', #type 3 / 3 edge-labels
	'3comb+pair2':	'(((a1b)3c)4(d2e))',
	'3comb+pair3':	'(((a2b)3c)4(d1e))',

	###================================================
	## 6 leaves  -- 6 type / 16 edge-labeled
	'6comb':		'(((((a1b)2c)3d)4e)5f)', #type 1
	'5giraffe+1':	'((((a1b)3(c2d))4e)5f)', #type 2
	#'5giraffe*+1':	'((((a2b)3(c1d))4e)5f)',

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
	## 7 leaves  -- 11 type / 61 edge-labeled
	'7comb':			'((((((a1b)2c)3d)4e)5f)6g)', #type 1 / 1 edge-labels
	'5giraffe+1+1':		'(((((a1b)3(c2d))4e)5f)6g)', #type 2 / 1 edge-labels
	'3comb+pair1+1+1':	'(((((a1b)2c)4(d3e))5f)6g)', #type 3 / 3 edge-labels
	'4comb+pair1+1':	'(((((a1b)2c)3d)5(e4f))6g)', #type 4 / 4 edge-labels
	'6twohead1+1':		'((((a1b)3(c2d))5(e4f))6g)', #type 5 / 4 edge-labels
	'6balanced1+1':		'((((a1b)2c)5((d3e)4f))6g)', #type 6 / 3 edge-labels

	'5comb+pair':		'(((((a1b)2c)3d)4e)6(f5g))', #type 7 / 5 edge-labels
	'5giraffe+pair':	'((((a1b)3(c2d))4e)6(f5g))', #type 8 / 5 edge-labels
	'3comb+pair1+pair':	'((((a1b)2c)4(d3e))6(f5g))', #type 9 / 5x3 = 15 edge-labels

	'4comb+3comb':		'((((a1b)2c)3d)6((e4f)5g))', #type 10 / (4+3+2+1) = 10 edge-labels
	'4balanced+3comb':	'(((a1b)3(c2d))6((e4f)5g))', #type 11 / (4+3+2+1) = 10 edge-labels

	###================================================
	## 8 leaves  -- 24 type / 272 edge-labeled
	# 11 from 7 leaves
	'8comb':				'(((((((a1b)2c)3d)4e)5f)6g)7h)', #type  1 /  1 edge-labels
	'5giraffe+1+1+1':		'((((((a1b)3(c2d))4e)5f)6g)7h)', #type  2 /  1 edge-labels
	'3comb+pair1+1+1+1':	'((((((a1b)2c)4(d3e))5f)6g)7h)', #type  3 /  3 edge-labels
	'4comb+pair1+1+1':		'((((((a1b)2c)3d)5(e4f))6g)7h)', #type  4 /  4 edge-labels
	'6twohead1+1+1':		'(((((a1b)3(c2d))5(e4f))6g)7h)', #type  5 /  4 edge-labels
	'6balanced1+1+1':		'(((((a1b)2c)5((d3e)4f))6g)7h)', #type  6 /  3 edge-labels
	'5comb+pair+1':			'((((((a1b)2c)3d)4e)6(f5g))7h)', #type  7 /  5 edge-labels
	'5giraffe+pair+1':		'(((((a1b)3(c2d))4e)6(f5g))7h)', #type  8 /  5 edge-labels
	'3comb+pair1+pair+1':	'(((((a1b)2c)4(d3e))6(f5g))7h)', #type  9 / 15 edge-labels
	'4comb+3comb+1':		'(((((a1b)2c)3d)6((e4f)5g))7h)', #type 10 / 10 edge-labels
	'4balanced+3comb+1':	'((((a1b)3(c2d))6((e4f)5g))7h)', #type 11 / 10 edge-labels

	# 6 from 6 leaves
	'6comb+pair':			'((((((a1b)2c)3d)4e)5f)7(g6h))', #type 12 /  6 edge-labels
	'5giraffe+1+pair':		'(((((a1b)3(c2d))4e)5f)7(g6h))', #type 13 /  6 edge-labels
	'3comb+pair1+1+pair':	'(((((a1b)2c)4(d3e))5f)7(g6h))', #type 14 / 18 edge-labels
	'4comb+pair1+pair':		'(((((a1b)2c)3d)5(e4f))7(g6h))', #type 15 / 24 edge-labels
	'6twohead1+pair':		'((((a1b)3(c2d))5(e4f))7(g6h))', #type 16 / 24 edge-labels
	'6balanced1+pair':		'((((a1b)2c)5((d3e)4f))7(g6h))', #type 17 / 18 edge-labels

	# 3 from 5 leaves
	'5comb+3comb':			'(((((a1b)2c)3d)4e)7((f5g)6h))', #type 18 / 15 edge-labels
	'5giraffe+3comb':		'((((a1b)3(c2d))4e)7((f5g)6h))', #type 19 / 15 edge-labels
	'3comb+pair1+3comb':	'((((a1b)2c)4(d3e))7((f5g)6h))', #type 20 / 45 edge-labels

	# 2x2 from 4 leaves
	'8hanukkah':			'((((a1b)3c)5d)7(e6(f4(g2h))))', #type 21 / 10 edge-labels
	'8balanced':			'(((a1b)5(c3d))7((e4f)6(g2h)))', #type 22 / 10 edge-labels
	#'4balanced+4comb':		'(((a1b)3(c2d))7(((e4f)5g)6h))', #duplicate
	'4comb+4balanced':		'((((a1b)2c)3d)7((e4f)6(g5h)))', #type 23 / 20 edge-labels

	###================================================
	## 9 leaves  -- 24 type / 272 edge-labeled
	# 23 from 8 leaves
	'9comb':				'((((((((a1b)2c)3d)4e)5f)6g)7h)8i)', #type  1 /  1 edge-labels
	'5giraffe+1+1+1+1':		'(((((((a1b)3(c2d))4e)5f)6g)7h)8i)', #type  2 /  1 edge-labels
	'3comb+pair1+1+1+1+1':	'(((((((a1b)2c)4(d3e))5f)6g)7h)8i)', #type  3 /  3 edge-labels
	'4comb+pair1+1+1+1':	'(((((((a1b)2c)3d)5(e4f))6g)7h)8i)', #type  4 /  4 edge-labels
	'6twohead1+1+1+1':		'((((((a1b)3(c2d))5(e4f))6g)7h)8i)', #type  5 /  4 edge-labels
	'6balanced1+1+1+1':		'((((((a1b)2c)5((d3e)4f))6g)7h)8i)', #type  6 /  3 edge-labels
	'5comb+pair+1+1':		'(((((((a1b)2c)3d)4e)6(f5g))7h)8i)', #type  7 /  5 edge-labels
	'5giraffe+pair+1+1':	'((((((a1b)3(c2d))4e)6(f5g))7h)8i)', #type  8 /  5 edge-labels
	'3comb+pair1+pair+1+1':	'((((((a1b)2c)4(d3e))6(f5g))7h)8i)', #type  9 / 15 edge-labels
	'4comb+3comb+1+1':		'((((((a1b)2c)3d)6((e4f)5g))7h)8i)', #type 10 / 10 edge-labels
	'4balanced+3comb+1+1':	'(((((a1b)3(c2d))6((e4f)5g))7h)8i)', #type 11 / 10 edge-labels
	'6comb+pair+1':			'(((((((a1b)2c)3d)4e)5f)7(g6h))8i)', #type 12 /  6 edge-labels
	'5giraffe+1+pair+1':	'((((((a1b)3(c2d))4e)5f)7(g6h))8i)', #type 13 /  6 edge-labels
	'3comb+pair1+1+pair+1':	'((((((a1b)2c)4(d3e))5f)7(g6h))8i)', #type 14 / 18 edge-labels
	'4comb+pair1+pair+1':	'((((((a1b)2c)3d)5(e4f))7(g6h))8i)', #type 15 / 24 edge-labels
	'6twohead1+pair+1':		'(((((a1b)3(c2d))5(e4f))7(g6h))8i)', #type 16 / 24 edge-labels
	'6balanced1+pair+1':	'(((((a1b)2c)5((d3e)4f))7(g6h))8i)', #type 17 / 18 edge-labels
	'5comb+3comb+1':		'((((((a1b)2c)3d)4e)7((f5g)6h))8i)', #type 18 / 15 edge-labels
	'5giraffe+3comb+1':		'(((((a1b)3(c2d))4e)7((f5g)6h))8i)', #type 19 / 15 edge-labels
	'3comb+pair1+3comb+1':	'(((((a1b)2c)4(d3e))7((f5g)6h))8i)', #type 20 / 45 edge-labels
	'8hanukkah+1':			'(((((a1b)3c)5d)7(e6(f4(g2h))))8i)', #type 21 / 10 edge-labels
	'8balanced+1':			'((((a1b)5(c3d))7((e4f)6(g2h)))8i)', #type 22 / 10 edge-labels
	'4comb+4balanced+1':	'(((((a1b)2c)3d)7((e4f)6(g5h)))8i)', #type 23 / 10 edge-labels

	# 11 from 7 leaves
	'7comb+pair':				'(((((((a1b)2c)3d)4e)5f)6g)8(h7i))', #type 24 /  7 edge-labels
	'5giraffe+1+1+pair':		'((((((a1b)3(c2d))4e)5f)6g)8(h7i))', #type 25 /  7 edge-labels
	'3comb+pair1+1+1+pair':		'((((((a1b)2c)4(d3e))5f)6g)8(h7i))', #type 26 / 21 edge-labels
	'4comb+pair1+1+pair':		'((((((a1b)2c)3d)5(e4f))6g)8(h7i))', #type 27 / 28 edge-labels
	'6twohead1+1+pair':			'(((((a1b)3(c2d))5(e4f))6g)8(h7i))', #type 28 / 28 edge-labels
	'6balanced1+1+pair':		'(((((a1b)2c)5((d3e)4f))6g)8(h7i))', #type 29 / 21 edge-labels
	'5comb+pair+pair':			'((((((a1b)2c)3d)4e)6(f5g))8(h7i))', #type 30 / 35 edge-labels
	'5giraffe+pair+pair':		'(((((a1b)3(c2d))4e)6(f5g))8(h7i))', #type 31 / 35 edge-labels
	'3comb+pair1+pair+pair':	'(((((a1b)2c)4(d3e))6(f5g))8(h7i))', #type 32 /105 edge-labels
	'4comb+3comb+pair':			'(((((a1b)2c)3d)6((e4f)5g))8(h7i))', #type 33 / 70 edge-labels
	'4balanced+3comb+pair':		'((((a1b)3(c2d))6((e4f)5g))8(h7i))', #type 34 / 70 edge-labels

	# 6 from 6 leaves
	'6comb+3comb':			'((((((a1b)2c)3d)4e)5f)8((g6h)7i))', #type 35 / 21 edge-labels
	'5giraffe+1+3comb':		'(((((a1b)3(c2d))4e)5f)8((g6h)7i))', #type 36 / 21 edge-labels
	'3comb+pair1+1+3comb':	'(((((a1b)2c)4(d3e))5f)8((g6h)7i))', #type 37 / 63 edge-labels
	'4comb+pair1+3comb':	'(((((a1b)2c)3d)5(e4f))8((g6h)7i))', #type 38 / 84 edge-labels
	'6twohead1+3comb':		'((((a1b)3(c2d))5(e4f))8((g6h)7i))', #type 39 / 84 edge-labels
	'6balanced1+3comb':		'((((a1b)2c)5((d3e)4f))8((g6h)7i))', #type 40 / 63 edge-labels

	# 2x3 from 5 leaves
	'5comb+4comb':				'(((((a1b)2c)3d)4e)8(((f5g)6h)7i))', #type 41 / 15 edge-labels
	'5giraffe+4comb':			'((((a1b)3(c2d))4e)8(((f5g)6h)7i))', #type 42 / 15 edge-labels
	'3comb+pair1+4comb':		'((((a1b)2c)4(d3e))8(((f5g)6h)7i))', #type 43 / 45 edge-labels
	'5comb+4balanced':			'(((((a1b)2c)3d)4e)8(((f5g)6h)7i))', #type 44 / 15 edge-labels
	'5giraffe+4balanced':		'((((a1b)3(c2d))4e)8(((f5g)6h)7i))', #type 45 / 15 edge-labels
	'3comb+pair1+4balanced':	'((((a1b)2c)4(d3e))8(((f5g)6h)7i))', #type 46 / 45 edge-labels
}


if __name__ == '__main__':
	a = ascii_tree()
	for name in code_library:
		code = code_library[name]
		if a.code_to_number_of_leaves(code) < 9:
			continue
		print('=====\n{0}'.format(name))
		a.make_tree(code)
		a.print_array()