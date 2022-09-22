### Library for crateing HTML tables of Amino Acid molecules

import sys
#import copy

#============================
#============================
#============================
class AminoAcidStructure(object):
	#============================
	def __init__(self, sugar_code):
		self.molecular_formula_ready = False
		self.structural_parts = []

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
