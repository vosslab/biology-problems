#!/usr/bin/env python

import os
import sys
import copy
import math
import random

N = 0

epistasis_ratios = {
	'15:1':	'3:1',
	'13:3':	'3:1',
	'12:4':	'2:2 or 1:1',
	'12:3:1':	'2:1:1',
	'10:6':	'2:2 or 1:1',
	'10:3:3':	'2:1:1',
	'9:7':	'1:3',
	'9:6:1':	'1:2:1 or 1:1:2',
	'9:4:3':	'1:2:1 or 1:1:2',
}

one_colon_choices = [
	'4:1', '3:2', '3:1', '2:3', '2:2 or 1:1', '2:1', '1:4', '1:3', '1:2',
]

two_colon_choices = [
	'3:1:1', '2:2:1', '2:1:2', '2:1:1', '1:3:1', '1:2:2', '1:2:1 or 1:1:2', '1:1:3', '1:1:1',
]


def write_question(question, choices):
	global N
	N += 1
	f = open('bbq-epistasis_test_cross.txt', 'a')
	print('{0}. {1}'.format(N, question))

	letters = 'ABCDEF'

	f.write('MC\t{0}\t'.format(question))
	for i,choice in enumerate(choices):
		f.write(choice+'\t')
		if choice == answer:
			prefix = 'x'
			f.write('Correct\t')
		else:
			prefix = ' '
			f.write('Incorrect\t')
		print('- [{0}] {1}. {2}'.format(prefix, letters[i], choice))
	print('')
	f.write('\n')
	f.close()

if __name__ == '__main__':
	keys = list(epistasis_ratios.keys())
	num_repeats = 11
	#random.shuffle(keys)
	for ratio in keys:

		number = '{0}. '.format(N)
		question = ''
		question += 'In a specific cross, F<sub>2</sub> progeny exhibit a modified dihybrid ratio of <b>{0}</b> (instead of 9:3:3:1 ). '.format(ratio)
		question += 'What phenotypic ratio would be expected from a test-cross with an individual from the F<sub>1</sub> progeny? '

		answer = epistasis_ratios[ratio]
		colon_count = answer.split(' ')[0].count(':')
		if colon_count == 2:
			choices = copy.copy(two_colon_choices)
		elif colon_count == 1:
			choices = copy.copy(one_colon_choices)
		print(choices)
		print(answer)
		choices.remove(answer)

		possibilities = math.comb(len(choices), 5)
		#print("There are {0} possibilities".format(possibilities))

		### BREAK
		original_choices = choices
		try:
			os.remove('bbq-epistasis_test_cross.txt')
		except FileNotFoundError:
			pass
		for i in range(num_repeats):
			choices = copy.copy(original_choices)
			random.shuffle(choices)
			random.shuffle(choices)
			choices = choices[0:5]
			choices.append(answer)
			random.shuffle(choices)
			random.shuffle(choices)

			write_question(question, choices)


