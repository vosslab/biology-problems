#!/usr/bin/env python3

import sys
import random

#rules:
# pH range is between 0 and 14,
# no negative pH, no pH > 14.1

#https://www.engineeringtoolbox.com/pKa-inorganic-acid-base-hydrated-metal-ion-monoprotic-diprotic-triprotic-tetraprotic-d_1950.html

colors_pyramid = [
 [], #0
 ['#404040',], #1
 ['#00008B', '#8B0000', ], #2
 ['#00008B', '#404040', '#8B0000', ], #3
 ['#00008B', '#202060', '#602020', '#8B0000', ], #4
 ['#00008B', '#202060', '#404040', '#602020', '#8B0000', ], #5
]

#============================
#============================
#============================
monoprotic = {
	'acetate':
	{	'acid_name':	'acetic acid',
		'base_name':	'acetate',
		'description':	'is the main component of vinegar and is involved in the metabolism of carbohydrates and fats',
		'pKa_list':		[4.76,],
		'state_list':	['CH3COOH', 'CH3COO-1'],
	},
	'ammonia':
	{	'acid_name':	'ammonium',
		'base_name':	'ammonia',
		'description':	'is primarily used as fertilizer for corn and wheat and is a precursor to nitrogen-containing compounds',
		'pKa_list':		[9.24, ],
		'state_list':	['NH4+1', 'NH3'],
	},
	'butyrate':
	{	'acid_name':	'butyric acid',
		'base_name':	'butyrate',
		'description':	'is a short-chain fatty acid, produced by microbes in animal colons, and can be metabolized by mitochondria',
		'pKa_list':		[4.82,],
		'state_list':	['CH3CH2CH2COOH', 'CH3CH2CH2COO-1'],
	},
	'glycolate':
	{	'acid_name':	'glycolic acid',
		'base_name':	'glycolate',
		'description':	'is produced by plants during photorespiration, a wasteful side reaction from photosynthesis',
		'pKa_list':		[3.83,],
		'state_list':	['HOCH2COOH', 'HOCH2COO-1',],
	},
	'lactate':
	{	'acid_name':	'lactic acid',
		'base_name':	'lactate',
		'description':	'is produced by anaerobic respiration in animal muscles, which can accumulate in the muscles and produce cramps',
		'pKa_list':		[3.86,],
		'state_list':	['CH3CHOHCOOH', 'CH3CHOHCOO-1',],
	},
	'sulfate':
	{	'acid_name':	'sulfuric acid',
		'base_name':	'sulfate',
		'description':	'is also known as battery acid and is produced from fossil fuel and biomass combustion forming acid rain',
		'pKa_list':		[1.99,],
		'state_list':	['HSO4-1', 'SO4-2',],
	},
}

#============================
#============================
#============================
diprotic = {
	'carbonate':
	{	'acid_name':	'carbonic acid',
		'names_list':	['carbonic acid', 'bicarbonate', 'carbonate',],
		'base_name':	'carbonate',
		'description':	'is also known as respiratory acid as it is the only acid excreted as a gas by the lungs',
		'pKa_list':		[6.35, 10.33,],
		'state_list':	['H2CO3', 'HCO3-1', 'CO3-2',],
	},
	'fumarate':
	{	'acid_name':	'fumaric acid',
		'base_name':	'fumarate',
		'description':	'is produced by human skin when exposed to sunlight and is an intermediate in the citric acid cycle',
		'pKa_list':		[3.03, 4.44,],
		'state_list':	['(COOH)CH=CH(COOH)', '(COOH)CH=CH(COO)-1', '(COO)CH=CH(COO)-2',],
	},
	'malate':
	{	'acid_name':	'malic acid',
		'base_name':	'malate',
		'description':	'is the main acid in many fruits and is an intermediate in the citric acid cycle',
		'pKa_list':		[3.40, 5.20,],
		'state_list':	['(COOH)CH2CH(OH)COOH', '(COOH)CH2CH(OH)COO-1',
			'(COO)CH2CH(OH)COO-2',],
	},
	'oxalate':
	{	'acid_name':	'oxalic acid',
		'base_name':	'oxalate',
		'description':	'is found in many plants and vegetables and is a product of metabolic processes',
		'pKa_list':		[1.27, 4.28,],
		'state_list':	['(COOH)2', 'HOOC-COO-1', 'C2O4-2',],
	},
	'succinate':
	{	'acid_name':	'succinic acid',
		'base_name':	'succinate',
		'description':	'is an intermediate in the citric acid cycle and can act as a signaling molecule reflecting the cellular metabolic state',
		'pKa_list':		[4.2, 5.6,],
		'state_list':	['(CH2)2(COOH)2', '(CH2)2(COOH)(COO)-1', '(CH2)2(COO)2-2',],
	},
	'sulfite':
	{	'acid_name':	'sulfurous acid',
		'base_name':	'sulfite',
		'description':	'occurs naturally in wine, but larger amounts are added to wine to stop fermentation and prevent spoilage',
		'pKa_list':		[1.81, 6.97],
		'state_list':	['H2SO3', 'HSO3-1', 'SO3-2',],
	},
	'urate':
	{	'acid_name':	'uric acid',
		'base_name':	'urate',
		'description':	'is an end product of nucleotide purine metabolism.',
		'pKa_list':		[5.4, 10.3,],
		'state_list':	['C5H4N4O3', 'C5H3N4O3-1', 'C5H2N4O3-2'],
	},
}

#============================
#============================
#============================
triprotic = {
	'arsenate':
	{	'acid_name':	'arsenic acid',
		'base_name':	'arsenate',
		'description':	'is extremely toxic, corrosive, and carcinogenic; it serves as a precursor to a variety of pesticides',
		'pKa_list':		[2.19, 6.94, 11.5,],
		'state_list':	['H3AsO4', 'H2AsO4-1', 'HAsO4-2', 'AsO4-3',]
	},
	'citrate':
	{	'acid_name':	'citric acid',
		'base_name':	'citrate',
		'description':	'is an intermediate in the citric acid cycle',
		'pKa_list':		[3.13, 4.76, 6.39,],
		'state_list':	['HOC3H4(COOH)3', 'HOC3H4(COOH)2(COO)-1',
			'HOC3H4(COOH)(COO)2-2', 'HOC3H4(COO)3-3',],
	},
	'phosphate':
	{	'acid_name':	'phosphoric acid',
		'base_name':	'phosphate',
		'description':	'is abbreviated P<sub>i</sub> and is formed by cells from the hydrolysis of ATP into ADP',
		'pKa_list':		[2.16, 7.21, 12.32,],
		'state_list':	['H3PO4', 'H2PO4-1', 'HPO4-2', 'PO4-3',]
	},
}

#============================
#============================
#============================
tetraprotic = {
	'pyrophosphate':
	{	'acid_name':	'pyrophosphoric acid',
		'base_name':	'pyrophosphate',
		'description':	'is abbreviated PP<sub>i</sub> and is formed by cells from the hydrolysis of ATP into AMP',
		'pKa_list':		[0.91, 2.1, 6.7, 9.32,],
		'state_list':	['H4P2O7', 'H3P2O7-1', 'H2P2O7-2', 'HP2O7-3', 'P2O7-4',]
	},
	'EDTA':
	{	'acid_name':	'ethylenediaminetetraacetic acid',
		'base_name':	'EDTA',
		'description':	'is commonly used in chelation therapy and as a chelating agent in biochemical experiments.',
		'pKa_list':		[2.00, 2.67, 6.16, 10.26,],
		'state_list':	['C10H16N2O8', 'C10H15N2O8-1', 'C10H14N2O8-2', 'C10H13N2O8-3', 'C10H12N2O8-4']
	},
}

#============================
#============================
#============================
all_buffer_dict = {}
all_buffer_dict |= monoprotic
all_buffer_dict |= diprotic
all_buffer_dict |= triprotic
all_buffer_dict |= tetraprotic
all_buffer_list = list(all_buffer_dict.values())

#============================
#============================
#============================
protic_names = {
	1: 'monoprotic',
	2: 'diprotic',
	3: 'triprotic',
	4: 'tetraprotic',
}

#============================
#============================
#============================
def _validate(all_buffer_dict):
	required_keys = ['acid_name', 'base_name', 'description', 'pKa_list', 'state_list']
	for buffer_name, buffer_dict in all_buffer_dict.items():
		print(buffer_name)
		for key in required_keys:
			if buffer_dict.get(key) is None:
				print(key+" is missing for "+buffer_name)
				sys.exit(1)
		# test floats
		for pKa_value in buffer_dict['pKa_list']:
			try:
				pKa_string = 'pKa_value = {0:.2f}'.format(pKa_value)
			except ValueError:
				print(pKa_value, 'is not a float')
				sys.exit(1)
		print('...is valid')

#============================
#============================
#============================
def pKa_list_to_words(pKa_list):
	prefix = 'pK<sub>a</sub> value'
	if len(pKa_list) == 1:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		return prefix+' of '+txt1
	elif len(pKa_list) == 2:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		txt2 = '<strong>{0:.2f}</strong>'.format(pKa_list[1])
		return prefix+'s of '+txt1+' and '+txt2
	elif len(pKa_list) == 3:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		txt2 = '<strong>{0:.2f}</strong>'.format(pKa_list[1])
		txt3 = '<strong>{0:.2f}</strong>'.format(pKa_list[2])
		return prefix+'s of '+txt1+', '+txt2+', and '+txt3
	elif len(pKa_list) == 4:
		txt1 = '<strong>{0:.2f}</strong>'.format(pKa_list[0])
		txt2 = '<strong>{0:.2f}</strong>'.format(pKa_list[1])
		txt3 = '<strong>{0:.2f}</strong>'.format(pKa_list[2])
		txt4 = '<strong>{0:.2f}</strong>'.format(pKa_list[3])
		return prefix+'s of '+txt1+', '+txt2+', '+txt3+', and '+txt4
	sys.exit(1)

#============================
#============================
#============================
def expand_buffer_dict(buffer_dict):
	num_pkas = len(buffer_dict['pKa_list'])
	buffer_dict['protic_name'] = protic_names[num_pkas]
	buffer_dict['formula_list'] = format_list_of_chemical_formula_html(buffer_dict['state_list'])
	return buffer_dict

#============================
#============================
#============================
def get_random_buffer():
	buffer_name = random.choice(list(all_buffer_dict.keys()))
	buffer_dict = all_buffer_dict[buffer_name]
	buffer_dict['name'] = buffer_dict
	buffer_dict = expand_buffer_dict(buffer_dict)
	return buffer_dict

#============================
#============================
#============================
def get_protonation_state(buffer_dict, pH_value):
	pKa_list = buffer_dict['pKa_list']
	state_list = buffer_dict['state_list']
	state_colors = colors_pyramid[len(state_list)]
	state = state_list[-1]
	color = state_colors[-1]
	for i, pKa in enumerate(pKa_list):
		if pH_value < pKa:
			state = state_list[i]
			color = state_colors[i]
			break
	return state, color

#============================
#============================
#============================
def get_protonation_formula(buffer_dict, pH_value):
	state, color = get_protonation_state(buffer_dict, pH_value)
	formula = format_chemical_formula_html(state, color)
	return formula

#============================
#============================
#============================
def format_chemical_formula_html(chem_state, color=None):
	string_list = list(chem_state)
	chem_form = ''
	charge = None
	for character in string_list:
		if charge is not None:
			if character == '1':
				chem_form += '<sup>{0}</sup>'.format(charge)
			else:
				chem_form += '<sup>{0}{1}</sup>'.format(character, charge)
		elif character == '-' or character == '+':
			charge = character
		elif character.isalpha():
			chem_form += character
		elif character.isdigit():
			chem_form += '<sub>{0}</sub>'.format(character)

		else:
			chem_form += character
	if color is not None:
		chem_form = f'<span style="color: {color}">{chem_form}</span>'
	return chem_form

#============================
#============================
#============================
def format_list_of_chemical_formula_html(state_list):
	formula_list = []
	state_colors = colors_pyramid[len(state_list)]
	for i, state in enumerate(state_list):
		color = state_colors[i]
		formula = format_chemical_formula_html(state, color)
		formula_list.append(formula)
	return formula_list


#============================
#============================
#============================
if __name__ == '__main__':
	#global all_buffer_list
	_validate(all_buffer_dict)
