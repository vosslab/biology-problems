### Library for crateing HTML tables of Sugar molecules

### nomenclature for sugar code
# A or M - aldose (A) or ketose (M) with a hydroxymethyl group
# L, R, or K - left, right, or carboxyl
# L, D - L sugar or D sugar
# M - nonstereo symmetric carbon, M = Hydroxymethyl group

sugar_table = {
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
	'MKLDM': 'xylulose'
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



def dextrose():
	return D_glucose()

def D_glucose():
	sugar_code = "ALRLDM"
	sugar = SugarClass(sugar_code)
	print(sugar.molecular_formula_txt())
	sugar.generate_structral_formula()
	print(sugar.structural_parts)
	return sugar

def D_galactose():
	sugar_code = "ARLLDM"
	sugar = SugarClass(sugar_code)
	print(sugar.molecular_formula_txt())
	sugar.generate_structral_formula()
	print(sugar.structural_parts)
	return sugar

def D_fructose():
	sugar_code = "KKLRDM"
	sugar = SugarClass(sugar_code)
	print(sugar.molecular_formula_txt())
	sugar.generate_structral_formula()
	print(sugar.structural_parts)
	return sugar

class SugarClass(object):
	def __init__(self, sugar_code):
		self.sugar_code = sugar_code
		self.molecular_formula_ready = False
		self.structural_formula_ready = False

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

	def molecular_formula_html(self):
		if self.molecular_formula_ready is False:
			self.generate_molecular_formula()
		molecular_formula = ""
		molecular_formula += "C<sub>{0:d}</sub>".format(self.carbons)
		molecular_formula += "H<sub>{0:d}</sub>".format(self.hydrogens)
		molecular_formula += "O<sub>{0:d}</sub>".format(self.oxygens)
		return molecular_formula
	

	def molecular_formula_txt(self):
		if self.molecular_formula_ready is False:
			self.generate_molecular_formula()
		molecular_formula = ""
		molecular_formula += "C{0:d} ".format(self.carbons)
		molecular_formula += "H{0:d} ".format(self.hydrogens)
		molecular_formula += "O{0:d} ".format(self.oxygens)
		return molecular_formula
	


