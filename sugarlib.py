### Library for crateing HTML tables of Sugar molecules

import copy

### nomenclature for sugar code
# A or M - aldose (A) or ketose (M) with a hydroxymethyl group
# L, R, or K - left, right, or carboxyl
# L, D - L sugar or D sugar
# M - nonstereo symmetric carbon, M = Hydroxymethyl group

#unless specified the following are all D sugars

class SugarCodes(object):
	def __init__(self):
		self.sugar_code_to_name = {
			'ADM': 'glyceraldehyde',
			'MKM': 'dihydroxacetone',
		
			'ARDM': 'erythrose',
			'ALDM': 'threose',
			'MKDM': 'erythrulose',

			'ARRDM': 'ribose',
			'ALRDM': 'arabinaose',
			'ARLDM': 'xylose',
			'ALLDM': 'lyxose',
			'MKRDM': 'ribulose',
			'MKLDM': 'xylulose',
			'MRKDM': 'meso 3-ketopentose',
			'MLKDM': 'D-3-ketopentose',
			'MRKLM': 'L-3-ketopentose',

			'ARRRDM': 'allose',
			'ALRRDM': 'altrose',
			'ARLRDM': 'glucose',
			'ALLRDM': 'mannose',
			'ARRLDM': 'gulose',
			'ALRLDM': 'idose',
			'ARLLDM': 'galactose',
			'ALLLDM': 'talose',
			'MKLLDM': 'psicose',
			'MKLRDM': 'fructose',
			'MKRLDM': 'sorbose',
			'MKRRDM': 'tagatose',
		}
		self.get_names_from_codes()

	#============================
	def get_names_from_codes(self):
		self.sugar_name_to_code = {}
		for code in self.sugar_code_to_name:
			name = self.sugar_code_to_name[code]
			self.sugar_name_to_code[name] = code

	#============================
	def get_D_hexoses(self):
		D_hexose_names = []
		for code in self.sugar_code_to_name:
			if len(code) == 6:
				name = self.sugar_code_to_name[code]
				D_hexose_names.append(name)
		return D_hexose_names

	#============================
	def get_D_aldohexoses(self):
		D_aldohexose_names = []
		for code in self.sugar_code_to_name:
			if len(code) == 6 and code[0] == 'A':
				name = self.sugar_code_to_name[code]
				D_aldohexose_names.append(name)
		return D_aldohexose_names

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
		return get_enantiomer_code_from_code(sugar_code)

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
	sugar_code = sugarcodes.sugar_name_to_code['glucose']
	sugar_struct = SugarStructure(sugar_code)
	sugar_struct.sugar_summary()
	return sugar_struct

#============================
def galactose():
	sugarcodes = SugarCodes()
	sugar_code = sugarcodes.sugar_name_to_code['galactose']
	sugar_struct = SugarStructure(sugar_code)
	sugar_struct.sugar_summary()
	return sugar_struct

#============================
def fructose():
	sugarcodes = SugarCodes()
	sugar_code = sugarcodes.sugar_name_to_code['fructose']
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
	def _aldose_html_header(self):
		aldose_header = ''
		aldose_header += '<tr>'
		aldose_header += ' <td colspan="2" style="text-align: right;">H&nbsp;</td>'
		aldose_header += ' <td colspan="2"></td>'
		aldose_header += ' <td colspan="2" style="text-align: left;">&nbsp;O</td>'
		aldose_header += '</tr><tr>'
		aldose_header += ' <td></td>'
		aldose_header += ' <td colspan="2" style="text-align: right;">\&nbsp;</td>'
		aldose_header += ' <td colspan="2" style="text-align: left;">&nbsp;//</td>'
		aldose_header += ' <td></td>'
		aldose_header += '</tr><tr>'
		aldose_header += ' <td></td>'
		aldose_header += ' <td></td>'
		aldose_header += ' <td colspan="2" style="text-align: center;">C</td>'
		aldose_header += ' <td></td>'
		aldose_header += ' <td></td>'
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
		hydrogen_cap += ' <td></td>'
		hydrogen_cap += ' <td></td>'
		hydrogen_cap += ' <td colspan="2" style="text-align: center;">H</td>'
		hydrogen_cap += ' <td></td>'
		hydrogen_cap += ' <td></td>'
		hydrogen_cap += '</tr>'
		return hydrogen_cap

	#============================
	def _hydroxymethyl_html_cap(self):
		hydroxymethyl_cap = ''
		hydroxymethyl_cap += '<tr>'
		hydroxymethyl_cap += ' <td></td>'
		hydroxymethyl_cap += ' <td></td>'
		hydroxymethyl_cap += ' <td colspan="4" style="text-align: left;">CH<sub>2</sub>OH</td>'
		hydroxymethyl_cap += '</tr>'
		return hydroxymethyl_cap

	#============================
	def _html_top_connector(self, extra_columns=False):
		top_connector = ''
		top_connector += '<tr>'
		if extra_columns is True:
			top_connector += ' <td></td>'
		top_connector += ' <td style="border-top: solid black 1px;"></td>'
		top_connector += ' <td style="border-right: solid black 1px; border-top: solid black 1px;"></td>'
		top_connector += ' <td style="border-left: solid black 1px; border-top: solid black 1px;"></td>'
		top_connector += ' <td style="border-top: solid black 1px;"></td>'
		if extra_columns is True:
			top_connector += ' <td></td>'
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
		bottom_content += ' <td rowspan="2" style="text-align: right;">{0}</td>'.format(content[0])
		bottom_content += ' <td style="border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border-right: solid black 1px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border-left: solid black 1px; border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td style="border-bottom: solid black 1px;"></td>'
		bottom_content += ' <td rowspan="2" style="text-align: left;">{0}</td>'.format(content[1])
		bottom_content += '</tr>'
		return bottom_content

	#============================
	def _html_carboxyl(self):
		bottom_content = ''
		bottom_content += '<tr>'
		bottom_content += ' <td style="border-right: solid black 1px;" colspan="3"></td>'
		bottom_content += ' <td style="border-left: solid black 1px;" colspan="3">'
		bottom_content += '  <span style="font-size: medium;">==</span>O<span style="font-size: x-large;">&nbsp;</span></td>'
		bottom_content += '</tr>'
		return bottom_content

	#============================
	def Fischer_projection_html(self):
		table = ''
		table += '<table border="1" style="border-collapse: collapse; border: white solid 0px;">'
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

