### Library for crateing HTML tables of Sugar molecules

import os
import re
import sys
#import copy
import subprocess

from qti_package_maker.common import yaml_tools

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


#============================
def validate_sugar_code(sugar_code: str) -> bool:
	"""
	Validates a sugar code using step-wise checks.

	Rules:
	1. Must start with 'A', 'MK', or 'M[RL]K'
	2. Must end in '[DL]M', unless it's a known meso exception ('MKM', 'MRKRM')
	3. 'D' may not appear anywhere else in the code
	4. All characters must be from the allowed set

	Args:
		sugar_code (str): e.g. 'ARLRRDM'

	Raises:
		ValueError: if the code fails any validation rule

	Returns:
		bool: True if valid
	"""
	# 1. Check valid prefix
	if not re.match(r'^(A|MK|M[RL]K)', sugar_code):
		raise ValueError(f"Invalid prefix in sugar code: {sugar_code}")

	# 2. Pass the meso exceptions without D- or L-
	meso_exceptions = {'MKM', 'MRKRM'}
	if sugar_code in meso_exceptions:
		return True

	# 3. Check valid suffix
	if not re.search(r'[DL]M$', sugar_code):
		raise ValueError(f"Invalid suffix in sugar code: {sugar_code} (must end in 'DM' or 'LM')")

	# 4. 'D' may only appear in the penultimate position
	penultimate_index = len(sugar_code) - 2
	if sugar_code.count('D') > int(sugar_code[penultimate_index] == 'D'):
		raise ValueError(f"'D' can only appear in penultimate position: {sugar_code}")

	if not re.search(r'^(A|MK|M[RL]K)[RL]*[DL]M$', sugar_code):
		raise ValueError(f"Invalid character '{c}' in sugar code: {sugar_code}")

	return True

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
		self.sugar_code_to_name = self.load_sugar_code_dict_from_yaml()
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


	#=======================
	def load_sugar_code_dict_from_yaml(self, yaml_path: str="sugar_codes.yml") -> dict:
		"""
		Reads a grouped sugar code YAML file and returns a flat sugar_code_to_name dictionary.
		Uses a custom YAML loader to detect duplicate keys.

		Args:
			yaml_path (str): Path to the YAML file

		Returns:
			dict: Flattened sugar code dictionary {code: name}
		"""
		grouped_dict = yaml_tools.read_yaml_file(yaml_path, msg=False)
		flat_dict = {}
		for group, group_mapping in grouped_dict.items():
			if not isinstance(group_mapping, dict):
				raise ValueError(f"Group '{group}' must be a mapping, got: {type(group_mapping)}")
			for code, name in group_mapping.items():
				if not validate_sugar_code(code):
					raise ValueError(f"Invalid sugar code {code}")
				if code in flat_dict:
					raise ValueError(f"Duplicate sugar code detected across groups: {code}")
				flat_dict[code] = name
		return flat_dict

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
	def get_sugar_names(self, num_carbons=None, configuration="all", types="all"):
		"""
		Retrieves sugar names based on the specified criteria.

		Args:
			num_carbons (int or None): Number of carbons in the sugar (e.g., 6 for hexoses).
				If None, no filtering on carbon count is applied.
			configuration (str or list): 'D', 'L', or 'all' (default). Can also be a list of configurations.
				'e.g., ['D', 'L'] for both configurations.
			types (str or list): 'aldo', 'keto', '3-keto', or 'all' (default). Can also be a list of types.

		Returns:
			list: List of sugar names matching the criteria.
		"""

		# Handle configuration: "all" means both 'D' and 'L'
		if configuration == "all" or configuration is None:
			configuration_list = ["D", "L"]
		elif isinstance(configuration, str):
			configuration_list = [configuration]
		else:
			configuration_list = configuration  # Assume it's a list

		# Handle types: "all" means 'aldo', 'keto', and '3-keto'
		if types == "all" or types is None:
			type_list = ["aldo", "keto", "3-keto"]
		elif isinstance(types, str):
			type_list = [types]
		else:
			type_list = types  # Assume it's a list

		sugar_names_list = []
		# Iterate over sugar codes and filter based on criteria
		for code in self.sugar_code_to_name:
			if not validate_sugar_code(code):
				continue

			# Filter by number of carbons
			if num_carbons is not None and len(code) != num_carbons:
				continue

			# Filter by types
			if code[0] == "A" and "aldo" not in type_list:
				continue
			elif code[0] == "M":
				if code[1] == "K" and "keto" not in type_list:
					continue
				elif code[2] == "K" and "3-keto" not in type_list:
					continue

			# Filter by configuration
			if code[-2] not in configuration_list:
				continue

			# Add matching sugar name to the result
			name = self.sugar_code_to_name[code]
			sugar_names_list.append(name)

		return sugar_names_list

	#============================
	def flip_position(self, sugar_code: str, position: int) -> str:
		"""
		Flips the stereochemistry at a given carbon position in the sugar code.
		"""
		code_chars = list(sugar_code)
		code_len = len(code_chars)
		# convert carbon number to 0-based index
		index = position - 1
		# First and last positions are not stereocenters
		if position == 1 or position == code_len:
			raise ValueError(f"Position {position} is not stereogenic in sugar_code '{sugar_code}'")
		char = code_chars[index]
		if char not in {'R', 'L', 'D'}:
			raise ValueError(f"Cannot flip non-stereocenter '{char}' at position {position} in '{sugar_code}'")
		# Flip D <-> L (penultimate configuration carbon)
		if position == code_len - 1:
			if char == 'D':
				code_chars[index] = 'L'
			elif char == 'L':
				code_chars[index] = 'D'
		# Flip R <-> L (internal stereocenters)
		elif char == 'R':
			code_chars[index] = 'L'
		elif char == 'L':
			code_chars[index] = 'R'

		return ''.join(code_chars)

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
		self.color_OH = True
		self.sugar_code = sugar_code
		self.molecular_formula_ready = False
		self.structural_parts = []
		if self.color_OH is True:
			# blue-ish
			self.H_text =  '<span style="color: #0052cc;">H</span>'
			# orange-ish
			self.OH_text = '<span style="color: #995c00;">OH</span>'
			self.HO_text = '<span style="color: #995c00;">HO</span>'
			# purple-ish
			self.CH2OH_text = '<span style="color: #8f246b;">CH<sub>2</sub>OH</span>'
		else:
			self.H_text = 'H'
			self.OH_text = 'OH'
			self.HO_text = 'HO'
			self.CH2OH_text = 'CH<sub>2</sub>OH'

	#============================
	def sugar_summary(self):
		print("SUGAR SUMMARY")
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
		hydrogen_cap += f' <td colspan="2" style="border: solid white 0px; text-align: center;">{self.H_text}</td>'
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
		hydroxymethyl_cap += f' <td colspan="4" style="border: solid white 0px; text-align: left;">{self.CH2OH_text}</td>'
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
			content = [self.H_text, self.OH_text]
		elif configuration.upper() == 'L':
			content = [self.HO_text, self.H_text]
		bottom_content = ''
		bottom_content += '<tr>'
		bottom_content += f' <td rowspan="2" style="border: solid white 0px; text-align: right;">{content[0]}</td>'
		bottom_content += ' <td style="border: solid white 0px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-right: solid black 1px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-left: solid black 1px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border: solid white 0px; border-bottom: solid black 1px;"></td>'
		bottom_content += f' <td rowspan="2" style="border: solid white 0px; text-align: left;">{content[1]}</td>'
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
		table += '</tbody>'
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
	def flip_direction(self, text: str) -> str:
		"""
		Flips HTML strings like HO <-> OH while preserving HTML tags and styling.
		"""
		if text == self.H_text:
			return self.H_text
		elif text == self.HO_text:
			return self.OH_text
		elif text == self.OH_text:
			return self.HO_text
		return text

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

		c1_end = self.H_text
		if first_carbon == 'M':
			second_carbon = code_list.pop(0)
			if second_carbon == 'K':
				c1_end = self.CH2OH_text
			else:
				code_list.pop(0) # third_carbon
				print('3-ketose error')
				c1_end = f'CHOH<br/>|<br/>{self.CH2OH_text}'

		if ((penultimate_carbon == 'D' and anomeric == 'alpha')
				or (penultimate_carbon == 'L' and anomeric == 'beta')):
			bottom = self.OH_text
			top = c1_end
		elif ((penultimate_carbon == 'D' and anomeric == 'beta')
				or (penultimate_carbon == 'L' and anomeric == 'alpha')):
			bottom = c1_end
			top = self.OH_text

		table = table.replace('X1U', top)
		table = table.replace('X1D', bottom)
		# loop over middle carbons
		for i in range(3):
			code = code_list.pop(0)
			if code == "L":
				bottom = self.H_text
				top = self.OH_text
			elif code == "R":
				bottom = self.OH_text
				top = self.H_text
			if i % 2 == 0:
				top = self.flip_direction(top)
				bottom = self.flip_direction(bottom)
			carbon_up = "X{0:d}U".format(i+2)
			carbon_down = "X{0:d}D".format(i+2)
			table = table.replace(carbon_up, top)
			table = table.replace(carbon_down, bottom)

		if len(code_list) == 1:
			top = self.H_text
			bottom = self.H_text
		elif len(code_list) == 2:
			penultimate_carbon = code_list.pop(0)
			if penultimate_carbon == 'D':
				top = self.CH2OH_text
				bottom = self.H_text
			elif penultimate_carbon == 'L':
				top = self.H_text
				bottom = self.CH2OH_text
		elif len(code_list) == 3:
			next_carbon = code_list.pop(0)
			if next_carbon == 'R':
				top = f'{self.CH2OH_text}<br/>|<br/>CHOH'
				bottom = self.H_text
			elif next_carbon == 'L':
				top = self.H_text
				bottom = f'CHOH<br/>|<br/>{self.CH2OH_text}'
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

		c1_end = self.H_text
		if first_carbon == 'M':
			second_carbon = code_list.pop(0)
			if second_carbon == 'K':
				c1_end = self.CH2OH_text
			else:
				code_list.pop(0) # third_carbon
				print('3-ketose error')
				c1_end = f'CHOH<br/>|<br/>{self.CH2OH_text}'

		if ((penultimate_carbon == 'D' and anomeric == 'alpha')
				or (penultimate_carbon == 'L' and anomeric == 'beta')):
			bottom = self.OH_text
			top = c1_end
		elif ((penultimate_carbon == 'D' and anomeric == 'beta')
				or (penultimate_carbon == 'L' and anomeric == 'alpha')):
			bottom = c1_end
			top = self.OH_text

		table = table.replace('X1U', top)
		table = table.replace('X1D', bottom)
		# loop over middle carbons
		for i in range(2):
			code = code_list.pop(0)
			if code == "L":
				bottom = self.H_text
				top = self.OH_text
			elif code == "R":
				bottom = self.OH_text
				top = self.H_text
			if i % 2 == 0:
				top = self.flip_direction(top)
				bottom = self.flip_direction(bottom)
			carbon_up = "X{0:d}U".format(i+2)
			carbon_down = "X{0:d}D".format(i+2)
			table = table.replace(carbon_up, top)
			table = table.replace(carbon_down, bottom)

		#print(code_list)
		if len(code_list) == 1:
			top = self.H_text
			bottom = self.H_text
		elif len(code_list) == 2:
			penultimate_carbon = code_list.pop(0)
			if penultimate_carbon == 'D':
				top = self.CH2OH_text
				bottom = self.H_text
			elif penultimate_carbon == 'L':
				top = self.H_text
				bottom = self.CH2OH_text
		elif len(code_list) == 3:
			next_carbon = code_list.pop(0)
			if next_carbon == 'R':
				top = f'{self.CH2OH_text}<br/>|<br/>CHOH'
				bottom = self.H_text
			elif next_carbon == 'L':
				top = self.H_text
				bottom = f'CHOH<br/>|<br/>{self.CH2OH_text}'
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
