#!/usr/bin/env python

import re
import sys
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
	# https://oeis.org/A000992
	# 1, 1, 2, 3,  6, 11,  24,   47,  103,   214, ...
	### Number of edge-labeled for number of leaves:
	# https://oeis.org/A000111
	# 1, 1, 2, 5, 16, 61, 272, 1385, 7936, 50521, ...
	
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
}



			
if __name__ == '__main__':
	a = ascii_tree()
	for name in code_library:
		code = code_library[name]
		print('=====\n{0}'.format(name))
		a.make_tree(code)
		a.print_array()