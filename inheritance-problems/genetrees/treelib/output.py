#!/usr/bin/env python3

import copy
import numpy
from collections import defaultdict

from treelib import tools

### TODO
# add background colors to gene labels
# add font colors to gene labels

fake_animals = {
	'a': 'Ashen',
	'b': 'Bellen',
	'c': 'Chimera',
	'd': 'Dibblet',
	'e': 'Elwet',
	'f': 'Faylen',
	'g': 'Gorret',
	'h': 'Hydra',
	'i': 'Inktoad',
	'j': 'Jackalope',
	'k': 'Kraken',
	'l': 'Lystra',
	'm': 'Manticore',
	'n': 'Narloc',
	'o': 'Oclora',
	'p': 'Phoenix',
	'q': 'Quokka',
	'r': 'Rynoth',
	's': 'Sphinx',
	't': 'Thorret',
	'u': 'Unicorn',
	'v': 'Vyrax',
	'w': 'Wyvern',
	'x': 'Xeraph',
	'y': 'Yawclor',
	'z': 'Zypher'
}


class GeneTreeOutput(object):
	#==================================
	def __init__(self):
		self.td_cell_count = 0
		self.gene_name_map = copy.copy(fake_animals)
		pass

	#==================================
	#==================================
	def make_char_tree(self, code: str) -> numpy.array:
		"""
		Takes a gene tree code and writes the tree structure to char_array.

		The function:
		1. Converts the tree code into a visual representation stored in char_array.
		2. Processes each taxon and internal node, associating them with rows in the array.
		3. Handles merging of taxa into combined nodes and updates the array iteratively.

		Args:
			code (str): The gene tree code.

		Returns:
			char_array (ndarray): A 2D array representing the tree structure.
		"""

		# Determine the number of leaves (taxa) in the tree and create an empty character array.
		num_leaves = tools.code_to_number_of_taxa(code)
		self.num_leaves = num_leaves
		char_array = self.create_empty_char_array(num_leaves)

		# Get the list of taxa (leaves) from the tree code.
		char_list = tools.code_to_taxa_list(code)

		# Initialize mappings:
		# 1. Taxa to their corresponding row numbers in the array.
		# 2. Internal node numbers to their associated taxa.
		char_row_number = {}
		internal_node_number_char_list = defaultdict(list)

		# Process each taxon to set up initial rows and mappings.
		for i, character in enumerate(char_list):
			row = i * 2  # Rows are spaced by 2 for visual separation.
			char_row_number[character] = row  # Map the taxon to its row.
			char_array[row, -1] = character  # Place the taxon at the rightmost position.

			# Get the internal node number associated with the taxon.
			internal_node_number = self.get_internal_node_for_taxon(character, code)

			# Map the internal node number to the list of associated taxa.
			internal_node_number_char_list[internal_node_number].append(character)

			# Draw the line representing the edge length for the taxon.
			line_length = self.internal_node_number_to_line_length(internal_node_number)
			char_array[row, -line_length-2:-2] = '_'  # Horizontal line representing the edge.

		# Make a copy of the tree code to simulate merging taxa iteratively.
		newcode = copy.copy(code)

		# Process internal nodes to merge taxa and update the character array.
		for internal_node_number in range(1, num_leaves):
			# Get the two taxa associated with the current internal node.
			char1, char2 = internal_node_number_char_list[internal_node_number]

			# Construct the subcode for the current node in the form "(char1node_char2)".
			subcode = f"({char1}{internal_node_number}{char2})"

			# If the subcode is not found, swap the order of taxa and try again.
			if subcode not in newcode:
				char2, char1 = char1, char2
				subcode = f"({char1}{internal_node_number}{char2})"

			# If the subcode still isn't found, raise an error.
			if subcode not in newcode:
				print(f"{subcode} not found in {newcode}")
				raise ValueError("Subcode not found in the code during processing.")

			# Determine the rows for the two taxa being merged and calculate the middle row.
			row1 = char_row_number[char1]
			row2 = char_row_number[char2]
			midrow = (row1 + row2 + 1) // 2  # The new combined taxon is placed in the middle.

			# Replace the subcode in the tree code with the combined taxa.
			combined = char1 + char2
			newcode = newcode.replace(subcode, combined)

			# Update mappings for the new combined taxa.
			new_internal_node_number = self.get_internal_node_for_taxon(combined, newcode)
			if new_internal_node_number is not None:
				internal_node_number_char_list[new_internal_node_number].append(combined)
			char_row_number[combined] = midrow  # Map the combined taxa to the middle row.

			# Draw the horizontal line for the combined taxa and vertical connecting lines.
			line_length = self.internal_node_number_to_line_length(internal_node_number)
			if new_internal_node_number is not None:
				next_line_length = self.internal_node_number_to_line_length(new_internal_node_number)
				gap = next_line_length - line_length - 1  # Determine spacing between lines.
			else:
				gap = 2  # Default gap if no new internal node is present.

			# Draw the horizontal line for the combined taxa.
			char_array[midrow, -line_length-3-gap:-line_length-3] = '_'

			# Draw the vertical connection between the two merged taxa.
			char_array[row1+1:row2+1, -line_length-3] = '|'

		return char_array

	#====================================================================
	def create_empty_char_array(self, num_leaves: int) -> numpy.array:
		#rows: 3->5, 4->7, 5->9 => rows = 2*leaves - 1
		rows = 2*num_leaves - 1
		cols = 3*num_leaves + 3
		empty_char_array = numpy.empty((rows, cols), dtype='str')
		empty_char_array[:] = ' '
		return empty_char_array

	#====================================================================
	def internal_node_number_to_line_length(self, internal_node_number: int) -> int:
		#mapping = {1:4, 2:7, 3:10, 4:13, 5:16, 6:19, 7:22}
		line_length = 3*internal_node_number + 1
		return line_length

	#==================================
	#==================================
	def get_internal_node_for_taxon(self, merged_taxa: str, merged_code: str) -> int:
		#print(f"merged_taxa = {merged_taxa}, merged_code = {merged_code}")
		# Handle the case where all taxa have been merged
		if len(merged_taxa) == self.num_leaves:
			return None

		# Find the index of the taxon in the merged_code
		index = merged_code.find(merged_taxa)
		if index == -1:
			raise ValueError(f"The taxon '{merged_taxa}' was not found in the merged_code.")

		# Get the preceding and following characters
		node1 = merged_code[index - 1]
		node2 = merged_code[index + len(merged_taxa)]

		# Check for internal nodes and determine the result
		if node1.isdigit() and node2.isdigit():
			# Error if both preceding and following characters are digits
			print(f"Taxon '{merged_taxa}' has two internal nodes: {node1} and {node2}")
			raise ValueError(f"Taxon '{merged_taxa}' cannot have two internal nodes.")
		elif node1.isdigit():
			return int(node1)
		elif node2.isdigit():
			return int(node2)
		else:
			# No internal node found
			print(f"Taxon '{merged_taxa}' has no internal node.")
			return None

	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================
	def print_array_ascii(self, code):
		char_array = self.make_char_tree(code)
		shape = char_array.shape
		for rownum in range(shape[0]):
			line = ''.join(char_array[rownum]) + ' '
			print(line)
		print("")

	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================

	def make_html_tree(self, code):
		"""
		this function will translate the char_array into an html_array
		"""
		char_array = self.make_char_tree(code)
		#else: we're good we have a char_array ready to go
		(rows, cols) = char_array.shape
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
					char_pair = ''.join(char_array[r, c:c+2])
					self.pair_array[r,c//2+1] = char_pair
					#sys.stderr.write("'{0}'".format(char_pair))
					td_cell = self.get_td_cell(char_pair)
					#print(td_cell)
					self.html_array[r,c//2+1] = td_cell
			#row_list = list(self.html_array[r,:])
			#print(''.join(row_list))
			#sys.stderr.write('\n')
		return

	#==================================
	def get_td_cell(self, cell_code):
		self.td_cell_count += 1
		content = copy.copy(cell_code)
		content = content.replace(' ', '')
		content = content.replace('|', '')
		content = content.replace('_', '')
		if len(content) > 0:
			return self.get_gene_name_cell(content)
		#print(cell_code)

		line = ' 3px solid black; '
		td_cell = '<td style="border: 0px solid white; '
		if len(cell_code) > 1 and cell_code[1] == '|':
			td_cell += 'border-right:'+line
		if cell_code[0] == '|':
			td_cell += 'border-left:'+line
		if '_' in cell_code:
			td_cell += 'border-bottom:'+line
		#if self.td_cell_count % 2 == 1:
		#	td_cell += 'background-color: silver'
		td_cell += '">'
		td_cell += ' '
		td_cell += '</td>' # third line
		return td_cell

	#==================================
	def get_gene_name_cell(self, gene_text):
		white_border = 'border: 0px solid white; '
		middle = 'vertical-align: middle; '
		alignspan = ' align="left" rowspan="2" '
		letter_cell = ' <td style="'+white_border+middle+'"'+alignspan+'>'
		letter_cell += '&nbsp;<span style="font-size: x-large;">'
		if self.gene_name_map.get(gene_text.lower()) is None:
			letter_cell += f'{gene_text.replace("|", "")}</span></td>'
		else:
			letter_cell += f'{self.gene_name_map[gene_text.lower()]}</span></td>'
		return letter_cell

	#==================================
	def format_array_html(self, code=None):
		if self.html_array is None:
			self.make_html_tree(code)
		(rows, cols) = self.html_array.shape
		html_table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
		for c in range(cols):
			html_table += '<colgroup width="30"></colgroup>'
		for r in range(rows):
			row_list = list(self.html_array[r,:])
			html_table += ''.join(row_list)
		html_table += '</table>'
		return html_table

	#==================================
	def get_html_from_code(self, code):
		self.make_html_tree(code)
		html_table = self.format_array_html()
		return html_table

#====================================================================
#====================================================================
#====================================================================
#====================================================================
if __name__ == '__main__':
	import random
	import treecodes
	all_codes = list(treecodes.code_library.values())
	tree_code = random.choice(all_codes)
	print(f"tree_code = {tree_code}")
	gtoutput = GeneTreeOutput()
	gtoutput.print_array_ascii(tree_code)

	html_tree = gtoutput.get_html_from_code(tree_code)
	f = open("gene_tree.html", "w")
	f.write(html_tree)
	f.close()
	print("open gene_tree.html")
