#!/usr/bin/env python

import re
import sys
import copy
import numpy
import random

class GeneTree(object):
	#==================================
	def __init__(self):
		self.code = None
		self.leaves = None
		self.char_array = None
		self.html_array = None
		self.cell_count = 0


		self._load_code_library()
		self._check_tree_count_theory()

	#==================================
	def _load_code_library(self):
		self.num_leaves_to_tree_set = {}
		self.max_leaves = 0
		self.code_to_name = {}
		count = 0
		for name, code in code_library.items():
			count += 1
			self.code_to_name[code] = name
			num_leaves = self.code_to_number_of_leaves(code)
			self.max_leaves = max(self.max_leaves, num_leaves)
			self.num_leaves_to_tree_set[num_leaves] = self.num_leaves_to_tree_set.get(num_leaves, []) + [code,]
		print("Processed {0} codes into {1} different sets with max leaves of {2}".format(
			count, len(self.num_leaves_to_tree_set), self.max_leaves))
		#print(list(self.num_leaves_to_tree_set.keys()))
		return

	#==================================
	def _check_tree_count_theory(self):
		return
		keys = list(self.num_leaves_to_tree_set.keys())
		keys.sort()
		for key in keys:
			print("leaves=", key, ": trees=", len(self.num_leaves_to_tree_set[key]))
		return

	#==================================
	def get_tree_name_from_code(self, code):
		return self.code_to_name[code]

	#==================================
	def get_random_gene_tree_code_for_leaf_count(self, num_leaves):
		if num_leaves > self.max_leaves:
			print("too many leaves requested {0} > max {1}".format(num_leaves, self.max_leaves))
			sys.exit(1)
		good_codes = self.num_leaves_to_tree_set[num_leaves]
		return random.choice(good_codes)

	#==================================
	def get_all_gene_tree_code_for_leaf_count(self, num_leaves):
		return self.num_leaves_to_tree_set[num_leaves]

	#==================================
	def make_flip_code_list(self, code_list):
		flip_list = code_list[::-1]
		flip_code = ''.join(flip_list)
		flip_code = flip_code.replace('(', '@')
		flip_code = flip_code.replace(')', '(')
		flip_code = flip_code.replace('@', ')')
		return list(flip_code)

	#==================================
	def get_left_of_node(self, code, node_number):
		N = str(node_number)
		Nloc = code.find(N)
		left_count = Nloc

		if code[Nloc-1].isalpha():
			return code[Nloc-1]
		if code[Nloc-1] == ')':
			parendiff = 1
			for i in range(2, left_count):
				#print(i, Nloc-i, code[Nloc-i], "parendiff=", parendiff)
				if code[Nloc-i] == ')':
					parendiff += 1
				elif code[Nloc-i] == '(':
					parendiff -= 1
				if parendiff == 0:
					return code[Nloc-i:Nloc]
				#print(i, Nloc-i, code[Nloc-i], "parendiff=", parendiff)

		return code[Nloc-1:Nloc]

	#==================================
	def get_right_of_node(self, code, node_number):
		N = str(node_number)
		Nloc = code.find(N)
		right_count = len(code) - Nloc

		if code[Nloc+1].isalpha():
			return code[Nloc+1]
		if code[Nloc+1] == '(':
			parendiff = 1
			for i in range(2, right_count):
				if code[Nloc+i] == '(':
					parendiff += 1
				elif code[Nloc+i] == ')':
					parendiff -= 1
				if parendiff == 0:
					return code[Nloc+1:Nloc+1+i]
		return code[Nloc+1:Nloc+2]

	#==================================
	def _flip_node_in_code(self, code, node_number):
		N = str(node_number)
		Nloc = code.find(N)
		left_text = self.get_left_of_node(code, node_number)
		right_text = self.get_right_of_node(code, node_number)

		code_list = list(code)
		start = Nloc-len(left_text)
		end = Nloc+len(right_text)+1
		sublist = code_list[start:end]
		flip_sublist = self.make_flip_code_list(sublist)
		code_list[start:end] = flip_sublist
		new_code = ''.join(code_list)

		if new_code[0] != '(' or new_code[-1] != ')':
			print("flipping node=", node_number)
			print(left_text, N, right_text)
			print(''.join(sublist),"<-sublist")
			print(''.join(flip_sublist),"<-flip_sublist")
			print(code,"<-code")
			print(new_code,"<-new_code")
			print("ERROR, see parentheses!!")
			sys.exit(1)

		return new_code

	#==================================
	def permute_code_by_node(self, code, node_number=None):
		#rotates tree about a single node, but preserves connections
		max_nodes = self.code_to_number_of_nodes(code)
		if node_number is None:
			node_number = random.randint(1,max_nodes)
		elif node_number == 0:
			return copy.copy(code)
		elif node_number > max_nodes:
			print("error: node_number {0} > max_nodes {1}".format(node_number, max_nodes))
			sys.exit(1)

		new_code = self._flip_node_in_code(code, node_number)
		return new_code

	#==================================
	def _permute_code_by_node_binary(self, code, node_binary):
		max_nodes = self.code_to_number_of_nodes(code)
		new_code = copy.copy(code)
		for node_number in range(max_nodes+1):
			# power of two, essentually a binary number
			if (node_binary // 2**node_number) % 2 == 1:
				new_code = self.permute_code_by_node(code, node_number)
		return new_code

	#==================================
	def int_to_binary_list(self, num):
		bin_list = []
		if num == 0:
			return [0,]
		import math
		max_nodes = int(math.ceil(math.log(float(num))/math.log(2.0)))
		for j in range(0, max_nodes+1):
			# power of two, essentually a binary number
			bin_list.append((num  // 2**j) % 2)
		print(num, bin_list)

	#==================================
	def get_all_code_permutations(self, code):
		max_nodes = self.code_to_number_of_nodes(code)
		code_permutations = []
		for node_binary in range(2**max_nodes+1):
			new_code = self._permute_code_by_node_binary(code, node_binary)
			code_permutations.append(new_code)
		prelen = len(code_permutations)
		#print(code_permutations)
		code_permutations = list(set(code_permutations))
		postlen = len(code_permutations)
		if prelen != postlen:
			print("count of code permuations are duplicates")
			#print(code_permutations)
			print("prelen=", prelen, "postlen=", postlen)
			#sys.exit(1)
		return code_permutations

	#==================================
	def get_random_code_permutation(self, code):
		max_nodes = self.code_to_number_of_nodes(code)
		node_binary = random.randint(0, 2**max_nodes)
		new_code = self._permute_code_by_node_binary(code, node_binary)
		return new_code

	#==================================
	def code_to_number_of_leaves(self, code):
		return len(self.code_to_char_list(code))

	#==================================
	def code_to_char_list(self, code):
		#print(code)
		re_list = re.split("[^a-zA-Z]*", code)
		#re_list has extra spaces
		#char_str = ''.join(re_list)
		#char_list = list(char_str)
		char_list = list(filter(None, re_list))
		return char_list

	#==================================
	def code_to_number_of_nodes(self, code):
		return len(self.code_to_node_list(code))

	#==================================
	def code_to_node_list(self, code):
		#print(code)
		re_list = re.split("[^0-9]*", code)
		num_list = list(filter(None, re_list))
		#print(num_list)
		return num_list

	#==================================
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

	#==================================
	def print_array_ascii(self):
		shape = self.char_array.shape
		for rownum in range(shape[0]):
			line = ''.join(self.char_array[rownum]) + ' '
			print(line)
		print("")

	#==================================
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

	#==================================
	def edge_number_to_line_length(self, edge_number):
		#line_length = 3*edge_number + 1
		#self.edge_number_to_line_length = {1:4, 2:7, 3:10, 4:13, 5:16, 6:19, 7:22}
		line_length = 3*edge_number + 1
		return line_length

	#==================================
	def make_edge_number_char_list(self, code):
		edge_number_char_list = {}
		char_list = self.code_to_char_list(code)
		for i,character in enumerate(char_list):
			edge_number = self.get_edge_number_for_string(character, code)
			edge_number_char_list[edge_number] = edge_number_char_list.get(edge_number, []) + [character]
		return edge_number_char_list

	#==================================
	def make_char_tree(self, code=None):
		"""
		takes code and writes to self.char_array
		"""
		if code is None:
			print("Code not defined, using an example")
			code = '(((a3b)4((c1d)2e))5f)'
			code = '(((a1b)4((c2d)3e))5f)'
			code = '(((a3b)5((c1d)4e))6(f2g))'
		self.code = code
		self.leaves = self.code_to_number_of_leaves(self.code)
		self.char_array = self.create_empty_array(self.leaves)

		char_list = self.code_to_char_list(code)
		#char_edge_number = {}
		char_row_number = {}
		edge_number_char_list = {}
		for i,character in enumerate(char_list):
			row = i*2
			char_row_number[character] = row
			self.char_array[row, -1] = character
			edge_number = self.get_edge_number_for_string(character, code)
			#char_edge_number[character] = edge_number
			edge_number_char_list[edge_number] = edge_number_char_list.get(edge_number, []) + [character]
			line_length = self.edge_number_to_line_length(edge_number)
			#print(row, edge_number, line_length)
			self.char_array[row, -line_length-2:-2] = '_'

		newcode = copy.copy(code)
		#print(edge_number_char_list)
		for edge_number in range(1, self.leaves):
			char1 = edge_number_char_list[edge_number][0]
			char2 = edge_number_char_list[edge_number][1]
			subcode = "({0}{1}{2})".format(char1,edge_number,char2)
			#print(subcode)
			if not subcode in newcode:
				#swap order
				char2, char1 = char1, char2
				subcode = "({0}{1}{2})".format(char1,edge_number,char2)
			if not subcode in newcode:
				print('{0} not found in {1}'.format(subcode, newcode))
				raise

			row1 = char_row_number[char1]
			row2 = char_row_number[char2]
			midrow = (row1 + row2 + 1)//2

			combined = "{0}{1}".format(char1, char2)
			newcode = newcode.replace(subcode, combined)
			new_edge_number = self.get_edge_number_for_string(combined, newcode)
			if new_edge_number is not None:
				edge_number_char_list[new_edge_number] = edge_number_char_list.get(new_edge_number, []) + [combined]
			char_row_number[combined] = midrow

			line_length = self.edge_number_to_line_length(edge_number)
			if new_edge_number is not None:
				next_line_length = self.edge_number_to_line_length(new_edge_number)
				gap = next_line_length - line_length - 1
			else:
				gap = 2
			self.char_array[midrow, -line_length-3-gap:-line_length-3] = '_'
			self.char_array[row1+1:row2+1, -line_length-3] = '|'
		return

	#==================================
	def get_td_cell(self, cell_code):
		self.cell_count += 1
		content = copy.copy(cell_code)
		content = content.replace(' ', '')
		content = content.replace('|', '')
		content = content.replace('_', '')
		if len(content) > 0:
			return self.get_letter_cell(content)
		#print(cell_code)

		line = ' 3px solid black; '
		td_cell = '<td style="border: 0px solid white; '
		if len(cell_code) > 1 and cell_code[1] == '|':
			td_cell += 'border-right:'+line
		if cell_code[0] == '|':
			td_cell += 'border-left:'+line
		if '_' in cell_code:
			td_cell += 'border-bottom:'+line
		#if self.cell_count % 2 == 1:
		#	td_cell += 'background-color: silver'
		td_cell += '">'
		td_cell += ' '
		td_cell += '</td>' # third line
		return td_cell

	#==================================
	def get_letter_cell(self, text):
		white_border = 'border: 0px solid white; '
		middle = 'vertical-align: middle; '
		alignspan = ' align="left" rowspan="2" '
		letter_cell = ' <td style="'+white_border+middle+'"'+alignspan+'>'
		letter_cell += '&nbsp;<span style="font-size: x-large;">'
		letter_cell += '{0}</span></td>'.format(text) # value
		return letter_cell

	#==================================
	def make_html_tree(self, code=None):
		"""
		this function will translate the char_array into an html_array
		"""
		if code is not None:
			# assume char tree is stale and make it again
			self.make_char_tree(code)
		elif self.char_array is None:
			# make a default code
			self.make_char_tree()
		#else: we're good we have a char_array ready to go
		#print(self.char_array)
		(rows, cols) = self.char_array.shape
		#print((rows, cols))
		self.html_array = numpy.empty((rows+1, cols//2+2), dtype=numpy.chararray)
		self.pair_array = numpy.empty((rows+1, cols//2+2), dtype=numpy.chararray)
		for r in range(rows+1):
			self.html_array[r,0] = '<tr>'
			self.html_array[r,-1] = '</tr>'
			for c in range(0,cols,2):
				if r == rows:
					self.pair_array[r,c//2+1] = '  '
					self.html_array[r,c//2+1] = self.get_td_cell(' ')
				else:
					char_pair = ''.join(self.char_array[r, c:c+2])
					self.pair_array[r,c//2+1] = char_pair
					#sys.stderr.write("'{0}'".format(char_pair))
					td_cell = self.get_td_cell(char_pair)
					#print(td_cell)
					self.html_array[r,c//2+1] = td_cell
			#row_list = list(self.html_array[r,:])
			#print(''.join(row_list))
			#sys.stderr.write('\n')

	#==================================
	def get_html_from_code(self, code):
		self.make_char_tree(code)
		#self.print_array_ascii()
		self.make_html_tree()
		html_table = self.format_array_html()
		return html_table

	#==================================
	def format_array_html(self, code=None):
		if self.html_array is None:
			self.make_html_tree(code)
		(rows, cols) = self.html_array.shape
		html_table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
		for c in range(cols):
			html_table += '<colgroup width="30"></colgroup>'
		"""
		html_table += '<colgroup width="30"></colgroup>'
		html_table += '<colgroup width="{0}"></colgroup>'.format((distances[3]-distances[2])*20)
		html_table += '<colgroup width="{0}"></colgroup>'.format((distances[2]-distances[1])*20)
		html_table += '<colgroup width="{0}"></colgroup>'.format((distances[1]-distances[0])*20)
		html_table += '<colgroup width="{0}"></colgroup>'.format(distances[0]*20)
		html_table += '<colgroup width="30"></colgroup>'
		"""
		for r in range(rows):
			row_list = list(self.html_array[r,:])
			html_table += ''.join(row_list)
		html_table += '</table>'
		return html_table

#==================================
#==================================
#==================================
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
	#'5giraffe*':	'(((a2b)3(c1d))4e)',
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
	###================================================
	## 8 leaves  -- 23 type / 272 edge-labeled
	# previous: 11 from 7 leaves
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
	###================================================
	## 9 leaves  -- 46 type / 1385 edge-labeled
	# previous: 23 from 8 leaves
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


	###================================================
	###================================================
}


#==================================
#==================================
#==================================



#==================================
#==================================
#==================================
if __name__ == '__main__':
	a = GeneTree()
	f = open('html_dump.html', 'w')
	for name in code_library:
		code = code_library[name]
		if a.code_to_number_of_leaves(code) != 9:
			continue
		new_code = a.permute_code(code)
		print('=====\n{0}'.format(name))
		all_codes = a.get_all_code_permutations(code)
		all_codes.sort()
		for c in all_codes:
			if 'b1a' in c:
				continue
			print(c)
			a.make_char_tree(c)
			a.print_array_ascii()
		sys.exit(1)

		a.make_html_tree()
		#print(a.pair_array)
		#print(a.html_array)
		f.write((a.format_array_html()))
	f.close()
