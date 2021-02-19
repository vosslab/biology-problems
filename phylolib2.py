#!/usr/bin/env python

import re
import sys
import copy
import numpy

class ascii_tree(object):
	def __init__(self, leaves):
		self.leaves = leaves
		self.char_array = self.create_empty_array(self.leaves)

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
			line = ''.join(self.char_array[rownum]) + ' .'
			print(line)

	def code_to_char_list(self, code):
		char_str = ''.join(re.split("[^a-zA-Z]*", code))
		char_list = list(char_str)
		return char_list

	def get_edge_number_for_string(self, my_str, code):
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

	def edge_number_to_line_length(edge_number):
		#line_length = 3*edge_number + 1
		#self.edge_number_to_line_length = {1:4, 2:7, 3:10, 4:13, 5:16, 6:19, 7:22}
		line_length = 3*edge_number + 1
		return line_length

	def make_tree(self, code=None):
		if code is None:
			code = '(((a3b)4((c1d)2e))5f)'
			code = '(((a1b)4((c2d)3e))5f)'
			code = '(((a3b)5((c1d)4e))6(f2g))'
		char_list = self.code_to_char_list(code)
		print(char_list)
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
		print(char_edge_number)
		print(edge_number_char_list)
		
		newcode = copy.copy(code)
		for edge_number in range(1, self.leaves):
			print("===========\nedge_number {0} of {1} for code: '{2}'".format(edge_number,self.leaves-1,newcode))
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
			print(char1, char2)

			row1 = char_row_number[char1]
			row2 = char_row_number[char2]
			midrow = (row1 + row2 + 1)//2

			combined = "{0}{2}".format(char1,edge_number,char2)
			print("{0} -> {1},".format(subcode, combined))
			newcode = newcode.replace(subcode, combined)
			print("{0} -> {1},".format(code, newcode))
			new_edge_number = self.get_edge_number_for_string(combined, newcode)
			if new_edge_number is not None:
				edge_number_char_list[new_edge_number] = edge_number_char_list.get(new_edge_number, []) + [combined]
			char_row_number[combined] = midrow
			print(char_row_number)


			print(row1, row2, midrow)
			line_length = self.edge_number_to_line_length(edge_number)
			if new_edge_number is not None:
				next_line_length = self.edge_number_to_line_length(new_edge_number)
				print(line_length, next_line_length)
				gap = next_line_length - line_length - 1
			else:
				gap = 2
			#self.char_array[row1, -line_length-2:-2] = '_'
			#self.char_array[row2, -line_length-2:-2] = '_'
			self.char_array[midrow, -line_length-3-gap:-line_length-3] = '_'
			self.char_array[row1+1:row2+1, -line_length-3] = '|'



		
		return
			


			
if __name__ == '__main__':
	a = ascii_tree(7)
	a.make_tree()
	a.print_array()