### Library for crateing HTML tables of Sugar molecules

import os
import sys
#import copy
import subprocess

### nomenclature for sugar code
# A or M - aldose (A) or ketose (M) with a hydroxymethyl group
# L, R, or K - left, right, or carboxyl
# L, D - L sugar or D sugar
# M - nonstereo symmetric carbon, M = Hydroxymethyl group
# unless specified the following are all D sugars

#==========================
#==========================
#==========================
def get_git_root(path=None):
	"""Return the absolute path of the repository root."""
	if path is None:
		# Use the path of the script
		path = os.path.dirname(os.path.abspath(__file__))
	try:
		base = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=path, universal_newlines=True).strip()
		return base
	except subprocess.CalledProcessError:
		# Not inside a git repository
		return None


#==========================
# Color definitions for different categories
#==========================
dark_blue = '#0000b3'
dark_green = '#008000'
dark_orange = '#b34700'
dark_magenta = '#b300b3'
dark_brown = '#996633'

#==========================
# Color mappings for choices
#==========================
color_choice_mapping = {
	#dark blue for carbon counts
	'diose (2)': dark_blue,
	'triose (3)': dark_blue,
	'tetrose (4)': dark_blue,
	'pentose (5)': dark_blue,
	'hexose (6)': dark_blue,
	'septose (7)': dark_blue,
	'octose (8)': dark_blue,
	'nonose (9)': dark_blue,
	#dark green for stereo D/L configuration
	'D-configuration': dark_green,
	'L-configuration': dark_green,
	#dark orange for double bond carbon location
	'aldose': dark_orange,
	'ketose': dark_orange,
	'3-ketose': dark_orange,
	#dark_magenta for ring names
	'oxetose': dark_magenta,
	'furanose': dark_magenta,
	'pyranose': dark_magenta,
	'oxepinose': dark_magenta,
	'septanose': dark_magenta,
	'octanose': dark_magenta,
	#dark_brown for anomeric configuration
	'&alpha;-anomer': dark_brown,
	'&beta;-anomer': dark_brown,
}

#==========================
# Helper function to apply colors
#==========================
def color_question_choices(choices_list):
	"""
	Applies color to the question choices using a mapping dictionary.

	Args:
		choices_list (list of str): List of plain text choices.

	Returns:
		list of str: List of HTML-formatted choices with colors applied.
	"""
	colored_choices_list = []
	for choice in choices_list:
		# Check if the choice exists in the color mapping
		if choice in color_choice_mapping:
			if choice in color_choice_mapping:
				colored = f'<span style="color:{color_choice_mapping[choice]};">{choice}</span>'
				colored_choices_list.append(colored)
			else:
				colored_choices_list.append(choice)
		else:
			# Keep uncolored if not found in the mapping
			colored_choices_list.append(choice)
	return colored_choices_list


#==========================
# SugarCodes class
#==========================
class SugarCodes(object):
	def __init__(self):
		self.sugar_code_to_name = {
			'ADM': 'D-glyceraldehyde',
			'ALM': 'L-glyceraldehyde',
			'MKM': 'dihydroxacetone',

			# D-aldotetroses
			'ARDM': 'D-erythrose',
			'ALDM': 'D-threose',
			# L-aldotetroses
			'ARLM': 'L-threose',
			'ALLM': 'L-erythrose',
			# ketotetroses
			'MKDM': 'D-erythrulose',
			'MKLM': 'L-erythrulose',

			# D-aldopentoses
			'ARRDM': 'D-ribose',
			'ALRDM': 'D-arabinaose',
			'ARLDM': 'D-xylose',
			'ALLDM': 'D-lyxose',
			# L-aldopentoses
			'ARRLM': 'L-lyxose',
			'ALRLM': 'L-xylose',
			'ARLLM': 'L-arabinaose',
			'ALLLM': 'L-ribose',
			# ketopentoses
			'MKRDM': 'D-ribulose',
			'MKLDM': 'D-xylulose',
			'MKRLM': 'L-xylulose',
			'MKLLM': 'L-ribulose',
			# 3-ketopentoses
			'MRKRM': 'meso 3-ketopentose',
			'MLKDM': 'D-3-ketopentose',
			'MRKLM': 'L-3-ketopentose',

			# D-aldohexoses
			'ARRRDM': 'D-allose',
			'ARRLDM': 'D-gulose',
			'ARLRDM': 'D-glucose',
			'ARLLDM': 'D-galactose',
			'ALRRDM': 'D-altrose',
			'ALRLDM': 'D-idose',
			'ALLRDM': 'D-mannose',
			'ALLLDM': 'D-talose',
			# L-aldohexoses
			'ARRRLM': 'L-talose',
			'ARRLLM': 'L-mannose',
			'ARLRLM': 'L-idose',
			'ARLLLM': 'L-altrose',
			'ALRRLM': 'L-galactose',
			'ALRLLM': 'L-glucose',
			'ALLRLM': 'L-gulose',
			'ALLLLM': 'L-allose',
			# D-ketohexoses
			'MKRRDM': 'D-tagatose',
			'MKRLDM': 'D-sorbose',
			'MKLRDM': 'D-fructose',
			'MKLLDM': 'D-psicose',
			# L-ketohexoses
			'MKRRLM': 'L-psicose',
			'MKRLLM': 'L-fructose',
			'MKLRLM': 'L-sorbose',
			'MKLLLM': 'L-tagatose',

			# aldoheptoses, add extra D to the name
			'ARRRDDM': 'DD-alloheptose',
			'ARRLDDM': 'DD-guloheptose',
			'ARLRDDM': 'DD-glucoheptose',
			'ARLLDDM': 'DD-galactoheptose',
			'ALRRDDM': 'DD-altroheptose',
			'ALRLDDM': 'DD-idoheptose',
			'ALLRDDM': 'DD-mannoheptose',
			'ALLLDDM': 'DD-taloheptose',
			'ARRRLDM': 'LD-alloheptose',
			'ARRLLDM': 'LD-guloheptose',
			'ARLRLDM': 'LD-glucoheptose',
			'ARLLLDM': 'LD-galactoheptose',
			'ALRRLDM': 'LD-altroheptose',
			'ALRLLDM': 'LD-idoheptose',
			'ALLRLDM': 'LD-mannoheptose',
			'ALLLLDM': 'LD-taloheptose',

			# ketoheptose, i.e., heptuloses from aldohexoses
			'MKRRRDM': 'D-alloheptulose',
			# altroheptulose is commonly called sedoheptulose
			'MKLRRDM': 'D-altroheptulose', #natural
			'MKRLRDM': 'D-glucoheptulose',
			'MKLLRDM': 'D-mannoheptulose', #natural
			'MKRRLDM': 'D-guloheptulose',
			'MKLRLDM': 'D-idoheptulose',
			'MKRLLDM': 'D-galactoheptulose',
			'MKLLLDM': 'D-taloheptulose',

			# ketoheptose, i.e., heptuloses from aldohexoses
			'MKRRRLM': 'L-taloheptulose',
			'MKLRRLM': 'L-galactoheptulose',
			'MKRLRLM': 'L-idoheptulose',
			'MKLLRLM': 'L-guloheptulose',
			'MKRRLLM': 'L-mannoheptulose',
			'MKLRLLM': 'L-glucoheptulose',
			'MKRLLLM': 'L-altroheptulose',
			'MKLLLLM': 'L-alloheptulose',

			# the two natural 3-ketoseptoses
			# two natural heptuloses with K <-> L swapped
			'MLKRRDM': 'D-altro-3-heptulose',
			'MLKLRDM': 'D-manno-3-heptulose',

		}
		self.get_names_from_codes()
		self.carbons_to_sugar = {
			2: 'diose', 3: 'triose', 4: 'tetrose',
			5: 'pentose', 6: 'hexose', 7: 'heptose',
			8: 'octose', 9: 'nonose',
		}
		self.ring_names = {
			'oxetose': 4, 'furanose': 5, 'pyranose': 6,
			'oxepinose': 7, 'septanose': 7, 'octanose': 8,
		}

	#============================
	def get_names_from_codes(self):
		self.sugar_name_to_code = {}
		for code in self.sugar_code_to_name:
			name = self.sugar_code_to_name[code]
			self.sugar_name_to_code[name] = code

	#============================
	def get_D_hexoses(self):
		D_hexose_names = self.get_sugar_names(6, 'D')
		return D_hexose_names

	#============================
	def get_D_aldohexoses(self):
		D_aldohexose_names = self.get_sugar_names(6, 'D', 'aldo')
		return D_aldohexose_names

	#============================
	def get_sugar_names(self, num_carbons=None, configuration=None, types=None):
		# num_carbons = #, e.g. 6 = hexoses
		# type = 'aldo', 'keto', or '3-keto'
		# configuration = 'D' or 'L'
		sugar_names = []
		for code in self.sugar_code_to_name:
			if num_carbons is not None and len(code) != num_carbons:
				continue
			if types is not None:
				if isinstance(types, str):
					type_list = [types,]
				else:
					type_list = types
				if 'aldo' not in type_list and code[0] == 'A':
					continue
				if 'keto' not in type_list and code[1] == 'K':
					continue
				if '3-keto' not in type_list and code[2] == 'K':
					continue
			if configuration is not None and code[-2] != configuration:
				continue
			name = self.sugar_code_to_name[code]
			sugar_names.append(name)
		return sugar_names

	#============================
	def flip_position(self, sugar_code, position):
		#position starts at 1 for the carbon number, not the string index
		flipped_code = list(sugar_code)
		length = len(sugar_code)
		if position == 1 or position == length:
			print("Um, the first and last carbon aren't stereosymmetric")
			return None
		elif position == length-1:
			#configuration carbon
			if sugar_code[position-1] == 'D':
				flipped_code[position-1] = 'L'
			elif sugar_code[position-1] == 'L':
				flipped_code[position-1] = 'D'
		else:
			if sugar_code[position-1] == 'R':
				flipped_code[position-1] = 'L'
			elif sugar_code[position-1] == 'L':
				flipped_code[position-1] = 'R'
		#print("Flipped {0} to {1} at position {2:d}".format(sugar_code[position-1], flipped_code[position-1], position))
		return ''.join(flipped_code)

	#============================
	def get_enantiomer_code_from_name(self, sugar_name):
		sugar_code = self.sugar_name_to_code[sugar_name]
		return self.get_enantiomer_code_from_code(sugar_code)

	#============================
	def get_enantiomer_code_from_code(self, sugar_code):
		code_list = list(sugar_code)
		# first is the same
		enantiomer_code = [code_list.pop(0),]
		# last is the same, but save for later
		last_carbon = code_list.pop(-1)
		# next-to-last carbon is special
		penultimate_carbon = code_list.pop(-1)
		for code in code_list:
			if code == 'L':
				enantiomer_code.append('R')
			elif code == 'R':
				enantiomer_code.append('L')
			elif code == 'K':
				enantiomer_code.append('K')
		if penultimate_carbon == 'L':
			enantiomer_code.append('D')
		elif penultimate_carbon == 'D':
			enantiomer_code.append('L')
		elif penultimate_carbon == 'K':
			enantiomer_code.append('K')
		enantiomer_code.append(last_carbon)
		return ''.join(enantiomer_code)

#============================
#============================
#============================

#============================
def dextrose():
	return glucose()

#============================
def glucose():
	sugarcodes = SugarCodes()
	sugar_code = sugarcodes.sugar_name_to_code['D-glucose']
	sugar_struct = SugarStructure(sugar_code)
	sugar_struct.sugar_summary()
	return sugar_struct

#============================
def galactose():
	sugarcodes = SugarCodes()
	sugar_code = sugarcodes.sugar_name_to_code['D-galactose']
	sugar_struct = SugarStructure(sugar_code)
	sugar_struct.sugar_summary()
	return sugar_struct

#============================
def fructose():
	sugarcodes = SugarCodes()
	sugar_code = sugarcodes.sugar_name_to_code['D-fructose']
	sugar_struct = SugarStructure(sugar_code)
	sugar_struct.sugar_summary()
	return sugar_struct

#============================
#============================
#============================
class SugarStructure(object):
	#============================
	def __init__(self, sugar_code):
		self.sugar_code = sugar_code
		self.molecular_formula_ready = False
		self.structural_parts = []

	#============================
	def sugar_summary(self):
		print(self.molecular_formula_txt())
		print(self.structural_part_txt())
		print(self.Fischer_projection_html())
		print(self.Haworth_pyranose_projection_html())
		print(self.Haworth_furanose_projection_html())

	#============================
	def structural_part_txt(self):
		if len(self.structural_parts) == 0:
			self.generate_structral_formula()
		return "--".join(self.structural_parts)

	#============================
	def generate_structral_formula(self):
		self.structural_parts = []
		self.structural_parts.append("H")
		code_list = list(self.sugar_code)
		#second carbon
		first_carbon = code_list.pop(0)
		if first_carbon == "A":
			self.structural_parts.append("C=O")
		elif first_carbon == "M":
			self.structural_parts.append("CHOH")
		#remove last carbon before loop
		last_carbon = code_list.pop(-1)
		# loop over middle carbons
		for code in code_list:
			if code == "L" or code == "R" or code == "D":
				self.structural_parts.append("CHOH")
			elif code == "K":
				self.structural_parts.append("C=O")
		#last_carbon
		if last_carbon == "M":
			self.structural_parts.append("CHOH")
		self.structural_parts.append("H")

	#============================
	def generate_molecular_formula(self):
		self.carbons = 0
		self.oxygens = 0
		self.hydrogens = 0
		code_list = list(self.sugar_code)
		#second carbon
		first_carbon = code_list.pop(0)
		if first_carbon == "A":
			self.carbons += 1
			self.oxygens += 1
			self.hydrogens += 1
		elif first_carbon == "M":
			self.carbons += 1
			self.oxygens += 1
			self.hydrogens += 3
		#remove last carbon before loop
		last_carbon = code_list.pop(-1)
		# loop over middle carbons
		for code in code_list:
			if code == "L" or code == "R" or code == "D":
				self.carbons += 1
				self.oxygens += 1
				self.hydrogens += 2
			elif code == "K":
				self.carbons += 1
				self.oxygens += 1
		#last_carbon
		if last_carbon == "M":
			self.carbons += 1
			self.oxygens += 1
			self.hydrogens += 3

	#============================
	def molecular_formula_html(self):
		if self.molecular_formula_ready is False:
			self.generate_molecular_formula()
		molecular_formula = ""
		molecular_formula += "C<sub>{0:d}</sub>".format(self.carbons)
		molecular_formula += "H<sub>{0:d}</sub>".format(self.hydrogens)
		molecular_formula += "O<sub>{0:d}</sub>".format(self.oxygens)
		return molecular_formula

	#============================
	def molecular_formula_txt(self):
		if self.molecular_formula_ready is False:
			self.generate_molecular_formula()
		molecular_formula = ""
		molecular_formula += "C{0:d} ".format(self.carbons)
		molecular_formula += "H{0:d} ".format(self.hydrogens)
		molecular_formula += "O{0:d} ".format(self.oxygens)
		return molecular_formula

	#============================
	#=====    Fischer projection
	#============================

	#============================
	def _aldose_html_header(self):
		aldose_header = ''
		aldose_header += '<tr>'
		aldose_header += ' <td colspan="2" style="border: solid white 0px; text-align: right;">H&nbsp;</td>'
		aldose_header += ' <td colspan="2" style="border: solid white 0px;"></td>'
		aldose_header += ' <td colspan="2" style="border: solid white 0px; text-align: left;">&nbsp;O</td>'
		aldose_header += '</tr><tr>'
		aldose_header += ' <td style="border: solid white 0px;"></td>'
		aldose_header += r' <td colspan="2" style="border: solid white 0px; text-align: right;">\&nbsp;</td>'
		aldose_header += ' <td colspan="2" style="border: solid white 0px; text-align: left;">&nbsp;//</td>'
		aldose_header += ' <td style="border: solid white 0px;"></td>'
		aldose_header += '</tr><tr>'
		aldose_header += ' <td style="border: solid white 0px;"></td>'
		aldose_header += ' <td style="border: solid white 0px;"></td>'
		aldose_header += ' <td colspan="2" style="border: solid white 0px; text-align: center;">C</td>'
		aldose_header += ' <td style="border: solid white 0px;"></td>'
		aldose_header += ' <td style="border: solid white 0px;"></td>'
		aldose_header += '</tr>'
		return aldose_header

	#============================
	def _hydroxymethyl_html_header(self):
		hydroxymethyl_header = ''
		hydroxymethyl_header += self._hydroxymethyl_html_cap()
		return hydroxymethyl_header

	#============================
	def _hydrogen_html_cap(self):
		hydrogen_cap = ''
		hydrogen_cap += '<tr>'
		hydrogen_cap += ' <td style="border: solid white 0px;"></td>'
		hydrogen_cap += ' <td style="border: solid white 0px;"></td>'
		hydrogen_cap += ' <td colspan="2" style="border: solid white 0px; text-align: center;">H</td>'
		hydrogen_cap += ' <td style="border: solid white 0px;"></td>'
		hydrogen_cap += ' <td style="border: solid white 0px;"></td>'
		hydrogen_cap += '</tr>'
		return hydrogen_cap

	#============================
	def _hydroxymethyl_html_cap(self):
		hydroxymethyl_cap = ''
		hydroxymethyl_cap += '<tr>'
		hydroxymethyl_cap += ' <td style="border: solid white 0px;"></td>'
		hydroxymethyl_cap += ' <td style="border: solid white 0px;"></td>'
		hydroxymethyl_cap += ' <td colspan="4" style="border: solid white 0px; text-align: left;">CH<sub>2</sub>OH</td>'
		hydroxymethyl_cap += '</tr>'
		return hydroxymethyl_cap

	#============================
	def _html_top_connector(self, extra_columns=False):
		top_connector = ''
		top_connector += '<tr>'
		if extra_columns is True:
			top_connector += ' <td style="border: solid white 0px;"></td>'
		top_connector += ' <td style="border: solid white 0px; border-top: solid black 1px;"></td>'
		top_connector += ' <td style="border: solid white 0px; border-right: solid black 1px; border-top: solid black 1px;"></td>'
		top_connector += ' <td style="border: solid white 0px; border-left: solid black 1px; border-top: solid black 1px;"></td>'
		top_connector += ' <td style="border: solid white 0px; border-top: solid black 1px;"></td>'
		if extra_columns is True:
			top_connector += ' <td style="border: solid white 0px;"></td>'
		top_connector += '</tr>'
		return top_connector

	#============================
	def _html_bottom_content(self, configuration='D'):
		if configuration.upper() == 'D' or configuration.upper() == 'R':
			content = ['H', 'OH']
		elif configuration.upper() == 'L':
			content = ['HO', 'H']
		bottom_content = ''
		bottom_content += '<tr>'
		bottom_content += ' <td rowspan="2" style="border: solid white 0px; text-align: right;">{0}</td>'.format(content[0])
		bottom_content += ' <td style="border: solid white 0px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-right: solid black 1px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-left: solid black 1px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td rowspan="2" style="border: solid white 0px; text-align: left;">{0}</td>'.format(content[1])
		bottom_content += '</tr>'
		return bottom_content

	#============================
	def _html_carboxyl(self):
		bottom_content = ''
		bottom_content += '<tr>'
		bottom_content += ' <td style="border: solid white 0px; border-right: solid black 1px;" colspan="3"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-left: solid black 1px;" colspan="3">'
		bottom_content += '  <span style="font-size: medium;">==</span>O<span style="font-size: x-large;">&nbsp;</span></td>'
		bottom_content += '</tr>'
		return bottom_content

	#============================
	def Fischer_projection_html(self):
		table = ''
		table += '<table border="0" style="border-collapse: collapse; border: white solid 0px;">'
		table += '<tbody>'
		code_list = list(self.sugar_code)
		first_code = code_list.pop(0)
		if first_code == 'A':
			table += self._aldose_html_header()
		elif first_code == 'M':
			table += self._hydroxymethyl_html_header()
		#remove last carbon before loop
		last_carbon = code_list.pop(-1)
		# loop over middle carbons
		for code in code_list:
			if code == "L" or code == "R" or code == "D":
				table += self._html_bottom_content(code)
				table += self._html_top_connector()
			elif code == "K":
				#not sure what to do
				table += self._html_carboxyl()
		#last_carbon
		if last_carbon == "M":
			table += self._hydroxymethyl_html_cap()
		table += '</table>'
		return table

	#============================
	#=====    Haworth projection
	#============================

	#============================
	def Haworth_projection_html(self, ring='pyran', anomeric='alpha'):
		# anormeric = 'alpha' or 'beta'
		# ring = 'pyran' or 'furan'
		if ring.startswith('oxet'):
			# oxtane or 2H-oxete
			print("sorry not implemented")
			sys.exit(1)
		elif ring.startswith('furan'):
			return self.Haworth_furanose_projection_html(anomeric)
		elif ring.startswith('pyran'):
			return self.Haworth_pyranose_projection_html(anomeric)
		elif ring.startswith('oxepin') or ring.startswith('septan'):
			# oxepane or oxepine or oxepin, requires a heptose
			# also called a septanose sugar
			print("sorry not implemented")
			sys.exit(1)

	#============================
	def Haworth_pyranose_projection_html(self, anomeric='alpha'):
		if len(self.sugar_code) < 5:
			# 5 carbons and 1 oxygen
			print("sugar is too small for pyranose")
			return
		if len(self.sugar_code) == 5 and self.sugar_code[0] != 'A':
			print("ketose sugar is too small for pyranose")
			return
		table = self.read_Haworth_pyranose_projection_html()
		code_list = list(self.sugar_code)
		first_carbon = code_list.pop(0)
		penultimate_carbon = self.sugar_code[-2]

		c1_end = 'H'
		if first_carbon == 'M':
			second_carbon = code_list.pop(0)
			if second_carbon == 'K':
				c1_end = 'CH<sub>2</sub>OH'
			else:
				code_list.pop(0) # third_carbon
				print('3-ketose error')
				c1_end = 'CHOH<br/>|<br/>CH<sub>2</sub>OH'

		if ((penultimate_carbon == 'D' and anomeric == 'alpha')
				or (penultimate_carbon == 'L' and anomeric == 'beta')):
			bottom = 'OH'
			top = c1_end
		elif ((penultimate_carbon == 'D' and anomeric == 'beta')
				or (penultimate_carbon == 'L' and anomeric == 'alpha')):
			bottom = c1_end
			top = 'OH'

		table = table.replace('X1U', top)
		table = table.replace('X1D', bottom)
		# loop over middle carbons
		for i in range(3):
			code = code_list.pop(0)
			if code == "L":
				bottom = 'H'
				top = 'OH'
			elif code == "R":
				bottom = 'OH'
				top = 'H'
			if i % 2 == 0:
				top = top[::-1]
				bottom = bottom[::-1]
			carbon_up = "X{0:d}U".format(i+2)
			carbon_down = "X{0:d}D".format(i+2)
			table = table.replace(carbon_up, top)
			table = table.replace(carbon_down, bottom)

		if len(code_list) == 1:
			top = 'H'
			bottom = 'H'
		elif len(code_list) == 2:
			penultimate_carbon = code_list.pop(0)
			if penultimate_carbon == 'D':
				top = 'CH<sub>2</sub>OH'
				bottom = 'H'
			elif penultimate_carbon == 'L':
				top = 'H'
				bottom = 'CH<sub>2</sub>OH'
		elif len(code_list) == 3:
			next_carbon = code_list.pop(0)
			if next_carbon == 'R':
				top = 'CH<sub>2</sub>OH<br/>|<br/>CHOH'
				bottom = 'H'
			elif next_carbon == 'L':
				top = 'H'
				bottom = 'CHOH<br/>|<br/>CH<sub>2</sub>OH'
		table = table.replace('X5U', top)
		table = table.replace('X5D', bottom)
		return table

	#============================
	def read_Haworth_pyranose_projection_html(self):
		git_root = get_git_root()
		data_file_path = os.path.join(git_root, 'data/haworth_pyranose_table.html')
		f = open(data_file_path, 'r')
		table = ''
		for line in f:
			table += line.strip()
		f.close()
		return table

	#============================
	def Haworth_furanose_projection_html(self, anomeric='alpha'):
		# 4 carbons and 1 oxygen
		if len(self.sugar_code) < 4:
			print("sugar is too small for furanose")
			return
		if len(self.sugar_code) == 4 and self.sugar_code[0] != 'A':
			print("ketose sugar is too small for furanose")
			return
		table = self.read_Haworth_furanose_projection_html()
		code_list = list(self.sugar_code)
		first_carbon = code_list.pop(0)
		penultimate_carbon = self.sugar_code[-2]

		c1_end = 'H'
		if first_carbon == 'M':
			second_carbon = code_list.pop(0)
			if second_carbon == 'K':
				c1_end = 'CH<sub>2</sub>OH'
			else:
				code_list.pop(0) # third_carbon
				print('3-ketose error')
				c1_end = 'CHOH<br/>|<br/>CH<sub>2</sub>OH'

		if ((penultimate_carbon == 'D' and anomeric == 'alpha')
				or (penultimate_carbon == 'L' and anomeric == 'beta')):
			bottom = 'OH'
			top = c1_end
		elif ((penultimate_carbon == 'D' and anomeric == 'beta')
				or (penultimate_carbon == 'L' and anomeric == 'alpha')):
			bottom = c1_end
			top = 'OH'

		table = table.replace('X1U', top)
		table = table.replace('X1D', bottom)
		# loop over middle carbons
		for i in range(2):
			code = code_list.pop(0)
			if code == "L":
				bottom = 'H'
				top = 'OH'
			elif code == "R":
				bottom = 'OH'
				top = 'H'
			if i % 2 == 0:
				top = top[::-1]
				bottom = bottom[::-1]
			carbon_up = "X{0:d}U".format(i+2)
			carbon_down = "X{0:d}D".format(i+2)
			table = table.replace(carbon_up, top)
			table = table.replace(carbon_down, bottom)

		#print(code_list)
		if len(code_list) == 1:
			top = 'H'
			bottom = 'H'
		elif len(code_list) == 2:
			penultimate_carbon = code_list.pop(0)
			if penultimate_carbon == 'D':
				top = 'CH<sub>2</sub>OH'
				bottom = 'H'
			elif penultimate_carbon == 'L':
				top = 'H'
				bottom = 'CH<sub>2</sub>OH'
		elif len(code_list) == 3:
			next_carbon = code_list.pop(0)
			if next_carbon == 'R':
				top = 'CH<sub>2</sub>OH<br/>|<br/>CHOH'
				bottom = 'H'
			elif next_carbon == 'L':
				top = 'H'
				bottom = 'CHOH<br/>|<br/>CH<sub>2</sub>OH'
		table = table.replace('X4U', top)
		table = table.replace('X4D', bottom)
		return table

	#============================
	def read_Haworth_furanose_projection_html(self):
		git_root = get_git_root()
		data_file_path = os.path.join(git_root, 'data/haworth_furanose_table.html')
		f = open(data_file_path, 'r')
		table = ''
		for line in f:
			table += line.strip()
		f.close()
		return table
