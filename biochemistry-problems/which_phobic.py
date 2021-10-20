#!/usr/bin/env python

import random

phobic = [
'benzene, C<sub>6</sub>H<sub>6</sub>',
'ethylene, CH<sub>2</sub>CH<sub>2</sub>',
'butane, CH<sub>3</sub>CH<sub>2</sub>CH<sub>2</sub>CH<sub>3</sub>',
]

phillic = [
'acetate, C<sub>2</sub>H<sub>3</sub>O<sub>2</sub>',
'erythrose, C<sub>4</sub>H<sub>8</sub>O<sub>4</sub>',
'glycine, NH<sub>2</sub>CH<sub>2</sub>COOH',
'ethanol, CH<sub>3</sub>CH<sub>2</sub>OH',
'methanol, CH<sub>3</sub>OH',
'ammonia, NH<sub>3</sub>',
'phosphoric acid, H<sub>3</sub>PO<sub>4</sub>',
'urea, CO(NH<sub>2</sub>)<sub>2</sub>',
]

if __name__ == '__main__':
	
	#============================
	print("1. Based on their molecular formula, which one of the following compounds is most likely hydrophobic")
	letters = "ABCDEFG"

	answer_number = random.randint(1,4)-1
	random.shuffle(phobic)
	random.shuffle(phillic)

	for i in range(4):
		if i == answer_number:
			choice = phobic.pop()
			prefix = '*'
		else:
			choice = phillic.pop()
			prefix = ''
		print("{0}{1}. {2}".format(prefix, letters[i], choice))
	print("")

