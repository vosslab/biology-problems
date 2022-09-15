### Library for crateing HTML tables of Sugar molecules

import sys
#import copy

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
		aldose_header += ' <td colspan="2" style="border: solid white 0px; text-align: right;">\&nbsp;</td>'
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
		f = open('../data/haworth_pyranose_table.html', 'r')
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
		f = open('../data/haworth_furanose_table.html', 'r')
		table = ''
		for line in f:
			table += line.strip()
		f.close()
		return table
