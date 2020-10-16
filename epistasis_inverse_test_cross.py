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
	'12:4':	'2:2',
	'12:3:1':	'2:1:1',
	'10:6':	'2:2',
	'10:3:3':	'2:1:1',
	'9:7':	'1:3',
	'9:6:1':	'1:2:1',
	'9:4:3':	'1:2:1',
}

inverse_ratios = {
	'3:1':	['15:1', '13:3'],
	'2:1:1':	['12:3:1', '10:3:3'],
	'1:3':	['9:7'],
	'1:2:1':	['9:6:1', '9:4:3'],
	'2:2':	['12:4', '10:6',]
}

#Fake 16:0, 14:2, 11:5, 8:8
one_colon_choices = [
	'16:0', '15:1', '14:2', '13:3', '12:4', '11:5', '10:6', '9:7', '8:8', '5:11', '2:14', '0:16',
]

#Fake 14, 13, 11, 8, 7, 6
two_colon_choices = [
	'14:1:1', '13:2:1', '12:3:1', '11:3:2', '10:3:3', '9:6:1', '9:4:3', '8:8:0', '8:4:4', '7:5:4', '6:5:5',
]


def write_question(question, choices):
	global N
	N += 1
	f = open('bbq-epistasis_inverse_test_cross.txt', 'a')
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

def firstDigit(key):
	bits = key.split(':')
	number = float(bits[0])
	number += float(bits[1])/100.
	return number


if __name__ == '__main__':
	keys = list(epistasis_ratios.keys())
	random.shuffle(keys)
	num_repeats = 11
	try:
		os.remove('bbq-epistasis_inverse_test_cross.txt')
	except FileNotFoundError:
		pass
	#random.shuffle(keys)
	for dihybrid_ratio in keys:
		test_ratio = epistasis_ratios[dihybrid_ratio]
		number = '{0}. '.format(N)
		question = ''
		question += 'In an F<sub>1</sub> heterozygote individual from dihybrid cross is used for a test-cross. '
		question += 'The progeny from the test-cross exhibited a modified <b>ratio of {0}</b> (instead of 1:1:1:1). '.format(test_ratio)
		question += 'What phenotypic ratio would be expected in the F<sub>2</sub> progeny if the dihybrid cross is continued? '

		answer = dihybrid_ratio
		colon_count = answer.split(' ')[0].count(':')
		if colon_count == 2:
			choice_set = set(copy.copy(two_colon_choices))
		elif colon_count == 1:
			choice_set = set(copy.copy(one_colon_choices))
		#print(choice_set)
		#print(answer)
		possible_answers = set(inverse_ratios[test_ratio])
		#print(possible_answers)
		choices = list(choice_set.difference(possible_answers))

		#print(choices)


		possibilities = math.comb(len(choices), 4)
		#print("There are {0} possibilities\n".format(possibilities))

		### BREAK
		original_choices = choices
		for i in range(num_repeats):
			choices = copy.copy(original_choices)
			random.shuffle(choices)
			random.shuffle(choices)
			choices = choices[0:4]
			choices.append(answer)
			choices = sorted(choices, key=firstDigit)
			choices.reverse()

			write_question(question, choices)
		#sys.exit(1)


