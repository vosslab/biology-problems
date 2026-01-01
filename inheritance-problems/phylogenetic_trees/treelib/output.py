#!/usr/bin/env python3

import re
import copy
import numpy
from collections import defaultdict

try:
	from treelib import tools
except ImportError:
	import tools

### ONLY ALLOWED TO IMPORT tools NOT OTHER TREELIB FILES

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
	'z': 'Zypher',
}

base_font_colors = {
	'a': '#661a00', # red 20%
	'b': '#001a66', # pure blue 15%
	'c': '#664b00', # golden yellow 20%
	'd': '#803100', # brown 20%
	'e': '#003f66', # sky blue 20%
	'f': '#660000', # pure red 20%
	'g': '#006666', # pure cyan 20%
	'h': '#006600', # pure green 20%
	'i': '#330066', # purple 20%
	'j': '#49361d', # tan 20%
	'k': '#424d57', # slate gray 30%
	'l': '#990033', # pink 30%
	'm': '#408000', # lime
	'n': '#3d3d5c', # dull purple
	'o': '#600080', # pink purple
	'p': '#802200', # redish
	'q': '#0e5850', # turquoise
	'r': '#6c1414', # fire brick
	's': '#875e12', # wheat
	't': '#008040', # sea green
	'u': '#990099', # pure magenta
	'v': '#805300', # orange
	'w': '#4d4d00', # pure yellow 15%
	'x': '#871287', # violet
	'y': '#63341c', # sienna
	'z': '#590099', # indigo
}

base_background_colors = {
	'a': '#ffc6b3', # red 85%
	'b': '#b3c6ff', # pure blue 85%
	'c': '#ffebb3', # golden yellow 85%
	'd': '#ffd0b3', # brown 85%
	'e': '#80cfff', # sky blue 85%
	'f': '#ffb3b3', # pure red 85%
	'g': '#99ffff', # pure cyan 80%
	'h': '#b3ffb3', # pure green 85%
	'i': '#d9b3ff', # purple 85%
	'j': '#e9dbc8', # tan 85%
	'k': '#d3d9de', # slate gray 85%
	'l': '#ffb3cc', # pink 30%
	'm': '#d9ffb3', # lime
	'n': '#d1d1e0', # dull purple
	'o': '#ecb3ff', # pink purple
	'p': '#ffc7b3', # redish
	'q': '#bdf5ef', # turquoise
	'r': '#f3bebe', # fire brick
	's': '#f6e1bc', # wheat
	't': '#b3ffd9', # sea green
	'u': '#ffb3ff', # pure magenta
	'v': '#ffe4b3', # orange
	'w': '#ffffb3', # pure yellow 85%
	'x': '#f6bcf6', # violet
	'y': '#eed1c3', # sienna
	'z': '#dfb3ff', # indigo
}

class GeneTreeOutput(object):
	#==================================
	def __init__(self):
		self.taxa_name_map = copy.copy(fake_animals)
		self.font_colors = copy.copy(base_font_colors)
		self.background_colors = copy.copy(base_background_colors)
		self.replace_names = True
		pass

	#====================================================================
	def create_empty_char_tree_array(self, num_leaves: int) -> numpy.chararray:
		# rows: 3->5, 4->7, 5->9 => rows = 2*leaves - 1
		rows = 2 * num_leaves - 1
		cols = 3 * num_leaves + 3
		# Create a chararray with itemsize=1
		empty_char_tree_array = numpy.empty((rows, cols), dtype='S1')
		if empty_char_tree_array.shape != (rows, cols):
			print(f"(rows, cols) = {(rows, cols)}")
			print(f"empty_char_tree_array.shape = {empty_char_tree_array.shape}")
			raise ValueError
		# Initialize all elements to ' ' (space character)
		empty_char_tree_array[:] = ' '
		return empty_char_tree_array

	#==================================
	#==================================
	def make_char_tree_array(self, tree_code: str) -> numpy.array:
		"""
		Takes a gene tree_code and writes the tree structure to char_tree_array.

		The function:
		1. Converts the tree_code into a visual representation stored in char_tree_array.
		2. Processes each taxon and internal node, associating them with rows in the array.
		3. Handles merging of taxa into combined nodes and updates the array iteratively.

		Args:
			tree_code (str): The gene tree_code.

		Returns:
			char_tree_array (ndarray): A 2D array representing the tree structure.
		"""

		# Determine the number of leaves (taxa) in the tree and create an empty character array.
		num_leaves = tools.code_to_number_of_taxa(tree_code)
		self.num_leaves = num_leaves
		char_tree_array = self.create_empty_char_tree_array(num_leaves)

		# Get the list of taxa (leaves) from the tree_code.
		char_list = tools.code_to_taxa_list(tree_code)

		# Initialize mappings:
		# 1. Taxa to their corresponding row numbers in the array.
		# 2. Internal node numbers to their associated taxa.
		char_row_number = {}
		internal_node_number_char_list = defaultdict(list)

		# Process each taxon to set up initial rows and mappings.
		for i, character in enumerate(char_list):
			row = i * 2  # Rows are spaced by 2 for visual separation.
			char_row_number[character] = row  # Map the taxon to its row.
			char_tree_array[row, -1] = character  # Place the taxon at the rightmost position.

			# Get the internal node number associated with the taxon.
			internal_node_number = self.get_internal_node_for_taxon(character, tree_code)

			# Map the internal node number to the list of associated taxa.
			internal_node_number_char_list[internal_node_number].append(character)

			# Draw the line representing the edge length for the taxon.
			line_length = self.internal_node_number_to_line_length(internal_node_number)
			char_tree_array[row, -line_length-2:-2] = '_'  # Horizontal line representing the edge.

		# Make a copy of the tree_code to simulate merging taxa iteratively.
		new_tree_code = copy.copy(tree_code)

		# Process internal nodes to merge taxa and update the character array.
		for internal_node_number in range(1, num_leaves):
			# Get the two taxa associated with the current internal node.
			char1, char2 = internal_node_number_char_list[internal_node_number]

			# Construct the sub_tree_code for the current node in the form "(char1_node_char2)".
			sub_tree_code = f"({char1}{internal_node_number}{char2})"

			# If the sub_tree_code is not found, swap the order of taxa and try again.
			if sub_tree_code not in new_tree_code:
				char2, char1 = char1, char2
				sub_tree_code = f"({char1}{internal_node_number}{char2})"

			# If the sub_tree_code still isn't found, raise an error.
			if sub_tree_code not in new_tree_code:
				print(f"{sub_tree_code} not found in {new_tree_code}")
				raise ValueError("sub_tree_code not found in the tree_code during processing.")

			# Determine the rows for the two taxa being merged and calculate the middle row.
			row1 = char_row_number[char1]
			row2 = char_row_number[char2]
			midrow = (row1 + row2 + 1) // 2  # The new combined taxon is placed in the middle.

			# Replace the sub_tree_code in the tree_code with the combined taxa.
			combined = char1 + char2
			new_tree_code = new_tree_code.replace(sub_tree_code, combined)

			# Update mappings for the new combined taxa.
			new_internal_node_number = self.get_internal_node_for_taxon(combined, new_tree_code)
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
			char_tree_array[midrow, -line_length-3-gap:-line_length-3] = '_'

			# Draw the vertical connection between the two merged taxa.
			char_tree_array[row1+1:row2+1, -line_length-3] = '|'

		return char_tree_array

	#====================================================================
	def internal_node_number_to_line_length(self, internal_node_number: int) -> int:
		#mapping = {1:4, 2:7, 3:10, 4:13, 5:16, 6:19, 7:22}
		line_length = 3*internal_node_number + 1
		return line_length

	#==================================
	#==================================
	def get_internal_node_for_taxon(self, merged_taxa: str, merged_tree_code: str) -> int:
		#print(f"merged_taxa = {merged_taxa}, merged_tree_code = {merged_tree_code}")
		# Handle the case where all taxa have been merged
		if len(merged_taxa) == self.num_leaves:
			return None

		# Find the index of the taxon in the merged_tree_code
		index = merged_tree_code.find(merged_taxa)
		if index == -1:
			raise ValueError(f"The taxon '{merged_taxa}' was not found in the merged_tree_code {merged_tree_code}.")

		# Get the preceding and following characters
		node1 = merged_tree_code[index - 1]
		node2 = merged_tree_code[index + len(merged_taxa)]

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
	def print_ascii_tree(self, tree_code):
		char_tree_array = self.make_char_tree_array(tree_code)
		shape = char_tree_array.shape
		# Decode array to str
		ascii_tree_array = numpy.char.decode(char_tree_array, 'ascii')
		for rownum in range(shape[0]):
			line = ''.join(ascii_tree_array[rownum][:-1])
			gene_text = ascii_tree_array[rownum][-1]
			if (self.replace_names is True
			and len(gene_text) == 1
			and self.taxa_name_map.get(gene_text.lower()) is not None):
				line += f'{self.taxa_name_map[gene_text.lower()]} '
			else:
				line += f'{gene_text} '
			print(line)
		print("")

	#==================================
	""""
	def utf8_character_improve(self, utf8_tree_array):
		return utf8_tree_array
		find_char_array = numpy.array([['|'],['_'],['|']], dtype=str)
		replace_char_array = numpy.array([['|'],['+'],['|']], dtype=str)
		mask = numpy.all(utf8_tree_array==find_char_array, axis=1)
		#ndimage labels???
		for label in labels:
			utf8_tree_array[label] = replace_char_array
		numpy.where(utf8_tree_array==find_char_array, replace_char_array, utf8_tree_array)
		return

	#==================================
	def print_utf8_tree(self, tree_code):
		# Unicode characters for table borders
		horizontal_line = "\u2500"
		vertical_line = "\u2502"
		top_left_corner = "\u250C"
		top_right_corner = "\u2510"
		bottom_left_corner = "\u2514"
		bottom_right_corner = "\u2518"
		middle_top = "\u252C"
		middle_bottom = "\u2534"
		middle_left = "\u251C"
		middle_right = "\u2524"
		center_cross = "\u253C"

		char_tree_array = self.make_char_tree_array(tree_code)
		shape = char_tree_array.shape
		# Decode array to str
		utf8_tree_array = numpy.char.decode(char_tree_array, 'utf8')
		for rownum in range(shape[0]):
			line = ''.join(utf8_tree_array[rownum][:-1])
			gene_text = utf8_tree_array[rownum][-1]
			if (self.replace_names is True
			and len(gene_text) == 1
			and self.taxa_name_map.get(gene_text.lower()) is not None):
				line += f'{self.taxa_name_map[gene_text.lower()]} '
			else:
				line += f'{gene_text} '
			print(line)
		print("")
	"""

	#====================================================================
	#====================================================================
	#====================================================================
	#====================================================================

	#==================================
	def get_gene_name_td_cell(self, gene_text):
		"""
		Generate an HTML `<td>` cell for displaying a gene name, with styling and formatting.
		"""
		# Define the border style for the table cell
		border = 'border: 1px solid silver; '
		# Vertically align the content to the middle
		middle = 'vertical-align: middle; '
		# Set the background color of the cell
		bg_color = f'bgcolor="{self.background_colors.get(gene_text, "#f0f0f0")}" '
		# Set additional `<td>` attributes, such as alignment and spanning two rows
		td_values = f'{bg_color} align="left" rowspan="2" '
		# Combine all the styles into the `<td>` opening tag
		td_sytle = f'style="{border}{middle}" '
		td_cell_open = f'<td {td_sytle} {td_values}>'
		# Define font color and size for the text within the cell
		font_color = f'color: {self.font_colors.get(gene_text, "black")}; '
		font_size = 'font-size: large; '
		# Combine the font styles into the opening `<span>` tag for the text
		text_span = f'&nbsp;<span style="{font_color}{font_size}">'
		# Determine the text content of the cell:
		if (self.replace_names is True
			and len(gene_text) == 1
			and self.taxa_name_map.get(gene_text.lower()) is not None):
			# Replace the gene_text with its mapped name (case insensitive lookup in `taxa_name_map`).
			cell_text = f'{self.taxa_name_map[gene_text.lower()]}'
		else:
			# Use the original gene_text as the cell content
			cell_text = f'{gene_text}'
		# Combine everything to form the complete HTML for the `<td>` cell
		name_td_cell = f'{td_cell_open}{text_span}<strong>{cell_text}</strong></span>&nbsp;</td>'
		# Return the fully constructed HTML `<td>` cell
		return name_td_cell

	#==================================
	def get_td_cell(self, char_pair):
		content = copy.copy(char_pair)
		content = re.sub(r'[ |_]', '', content)
		if len(re.sub(r'[ |_]', '', content)) > 0:
			return self.get_gene_name_td_cell(content)
		line = ' 4px solid black; '
		td_cell = '<td style="border: 0px solid white; '
		if len(char_pair) > 1 and char_pair[1] == '|':
			td_cell += 'border-right:'+line
		if char_pair[0] == '|':
			td_cell += 'border-left:'+line
		if '_' in char_pair:
			td_cell += 'border-bottom:'+line
		td_cell += '">'
		td_cell += ' '
		td_cell += '</td>' # third line
		return td_cell

	#==================================
	def make_html_tree_array(self, char_tree_array):
		"""
		this function will translate the char_tree_array into an html_tree_array
		"""
		(rows, cols) = char_tree_array.shape
		html_rows, html_cols = rows+1, cols//2+2+cols%2
		html_tree_array = numpy.empty((html_rows, html_cols), dtype=numpy.chararray)
		# Decode array to str
		ascii_tree_array = numpy.char.decode(char_tree_array, 'ascii')
		for row_num in range(rows):
			for html_col_num in range(html_cols):
				col_num = html_col_num*2
				char_pair = ''.join(ascii_tree_array[row_num, col_num:col_num+2])
				if len(char_pair) == 0:
					continue
				td_cell = self.get_td_cell(char_pair)
				html_tree_array[row_num, col_num//2+1] = td_cell
		html_tree_array[-1, :] = self.get_td_cell(' ')
		html_tree_array[1::2, -2] = ' '
		html_tree_array[:,  0] = '<tr style="height: 25;">'
		html_tree_array[:, -1] = '</tr>'
		return html_tree_array

	#==================================
	def format_array_into_html_table(self, html_tree_array, caption_tag: str = None):
		(rows, cols) = html_tree_array.shape
		html_table = '<table style="border-collapse: collapse; border: 1px solid silver;">'
		if (caption_tag
		and len(caption_tag) > 19
		and caption_tag.startswith('<caption')
		and caption_tag.endswith('</caption>')):
			html_table += caption_tag
		#col 1 and -1 are <tr>
		for _ in range(cols - 3):
			html_table += '<colgroup width="30"/>'
		html_table += '<colgroup width="100"/>'
		for r in range(rows):
			row_list = list(html_tree_array[r,:])
			html_table += ''.join(row_list)
		html_table += '</table>'
		return html_table

	#==================================
	def get_html_from_tree_code(self, tree_code, caption_tag: str = None):
		char_tree_array = self.make_char_tree_array(tree_code)
		html_tree_array = self.make_html_tree_array(char_tree_array)
		html_table = self.format_array_into_html_table(html_tree_array, caption_tag)
		if tools.is_valid_html(html_table) is False:
			print(html_table)
			raise ValueError("Generated HTML is not well-formed.")
		return html_table

#====================================================================
#====================================================================
#====================================================================
#====================================================================
if __name__ == '__main__':
	import random
	import definitions
	all_tree_codes = list(definitions.code_library.values())
	tree_code = random.choice(all_tree_codes)
	#while len(tree_code) > 12:
	#	tree_code = random.choice(all_tree_codes)
	print(f"tree_code = {tree_code}")
	gtoutput = GeneTreeOutput()
	gtoutput.print_ascii_tree(tree_code)
	char_tree_array = gtoutput.make_char_tree_array(tree_code)
	ascii_tree_array = numpy.char.decode(char_tree_array, 'ascii')
	#print(repr(ascii_tree_array))
	html_tree = gtoutput.get_html_from_tree_code(tree_code)
	f = open("gene_tree.html", "w")
	f.write(html_tree)
	f.close()
	print("open gene_tree.html")
