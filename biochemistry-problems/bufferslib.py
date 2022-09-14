import sys
import random

#https://www.engineeringtoolbox.com/pKa-inorganic-acid-base-hydrated-metal-ion-monoprotic-diprotic-triprotic-tetraprotic-d_1950.html

monoprotic = {
	'acetate':
	{	'acid_name':	'acetic acid',
		'base_name':	'acetate',
		'pKa_list':		[4.76, ],
		'state_list':	['CH3COOH', 'CH3COO-1'],
	},
	'butyrate':
	{	'acid_name':	'butyric acid',
		'base_name':	'butyrate',
		'pKa_list':		[4.82, ],
		'state_list':	['CH_3CH_2CH_2CO_2H', 'CH_3CH_2CH_2CO_2-1'],
	},
}

diprotic = {
	'carbonate':
	{	'acid_name':	'carbonic acid',
		'base_name':	'carbonate',
		'pKa_list':		[6.35, 10.33],
		'state_list':	['H_2CO_3', 'HCO_3-1', 'CO_3-2',],
	},
	'lactate':
	{	'acid_name':	'lactic acid',
		'base_name':	'lactate',
		'pKa_list':		[3.86, 15.1],
		'state_list':	['CH3CH(OH)COOH', 'CH3CH(OH)COO-1', 'CH3CH(O)COO-2',],
	},
	'malate':
	{	'acid_name':	'malic acid',
		'base_name':	'malate',
		'pKa_list':		[3,40, 5.20,],
		'state_list':	['(COOH)CH2CH(OH)COOH', '(COOH)CH2CH(OH)COO-1', '(COO)CH2CH(OH)COO-2',],
	},
	'sulfite':
	{	'acid_name':	'sulfurous acid',
		'base_name':	'sulfite',
		'pKa_list':		[1.81, 6.97],
		'state_list':	['H_2SO_3', 'HSO_3-1', 'SO_3-2',],
	},
}


triprotic = {
	'arsenate':
	{	'acid_name':	'arsenic acid',
		'base_name':	'arsenate',
		'pKa_list':		[2.19, 6.94, 11.5,],
		'state_list':	['H3AsO4', 'H2AsO4-1', 'HAsO4-2', 'AsO4-3',]
	},
	'citrate':
	{	'acid_name':	'citric acid',
		'base_name':	'citrate',
		'pKa_list':		[3.13, 4.76, 6.39,],
		'state_list':	['HOC3H4(COOH)3', 'HOC3H4(COOH)2(COO)-1',
			'HOC3H4(COOH)(COO)2-2', 'HOC3H4(COO)3-3',],
	},
	'malate':
	{	'acid_name':	'malic acid',
		'base_name':	'malate',
		'pKa_list':		[3,40, 5.20, 14.5],
		'state_list':	['COOHCH2CH(OH)COOH', 'COOHCH2CH(OH)COO-1',
			'COOCH2CH(OH)COO-2', 'COOCH2CH(O)COO-3'],
	},
	'phosphate':
	{	'acid_name':	'phosphoric acid',
		'base_name':	'phosphate',
		'pKa_list':		[2.16, 7.21, 12.32,],
		'state_list':	['H3PO4', 'H2PO4-1', 'HPO4-2', 'PO4-3',]
	},
}

tetraprotic = {
	'citrate':
	{	'acid_name':	'citric acid',
		'base_name':	'citrate',
		'pKa_list':		[3.13, 4.76, 6.39, 14.4,],
		'state_list':	['HOC3H4(COOH)3', 'HOC3H4(COOH)2(COO)-1',
			'HOC3H4(COOH)(COO)2-2', 'HOC3H4(COO)3-3', 'OC3H4(COO)3-4',],
	},
	'pyrophosphate':
	{	'acid_name':	'pyrophosphoric acid',
		'base_name':	'pyrophosphate',
		'pKa_list':		[0.91, 2.1, 6.7, 9.32,],
		'state_list':	['H4P2O7', 'H3P2O7-1', 'H2P2O7-2', 'HP2O7-3', 'P2O7-4',]
	},
}
