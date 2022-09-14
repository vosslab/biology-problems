import sys
import random

#https://www.engineeringtoolbox.com/pKa-inorganic-acid-base-hydrated-metal-ion-monoprotic-diprotic-triprotic-tetraprotic-d_1950.html

buffers = {
	'butyrate':
	{	'acid_name':	'butyric acid',
		'base_name':	'butyrate',
		'pKa_list':		[4.82, ],
		'state_list':	['CH_3CH_2CH_2CO_2H', 'CH_3CH_2CH_2CO_2-1'],
	},

	'carbonate':
	{	'acid_name':	'carbonic acid',
		'base_name':	'carbonate',
		'pKa_list':		[6.35, 10.33],
		'state_list':	['H_2CO_3', 'HCO_3-1', 'CO_3-2',],
	},
	'sulfite':
	{	'acid_name':	'sulfurous acid',
		'base_name':	'sulfite',
		'pKa_list':		[1.81, 6.97],
		'state_list':	['H_2SO_3', 'HSO_3