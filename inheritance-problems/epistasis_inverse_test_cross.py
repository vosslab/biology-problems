#!/usr/bin/env python3

import os
import copy
import math
import random
import argparse

import bptools

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


def firstDigit(key):
	bits = key.split(':')
	number = float(bits[0])
	number += float(bits[1])/100.
	return number


if __name__ == '__main__':
	# Initialize argparse for command line arguments
	parser = argparse.ArgumentParser(description='Generate blackboard questions.')
	# Add command line options for number of genes and number of questions
	parser.add_argument('-x', '--num_repeats', dest='num_repeats', type=int, default=11, help='Number of question generation runs')
	# Parse the command line arguments
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	#random.shuffle(keys)
	N = 0
	question_list = []
	for i in range(args.num_repeats):
		for dihybrid_ratio in list(epistasis_ratios.keys()):
			N += 1
			test_ratio = epistasis_ratios[dihybrid_ratio]
			question_txt = ''
			question_txt += f'The progeny from the test-cross exhibited a modified <b>ratio of {test_ratio}</b>'
			question_txt += ', different from the expected 1:1:1:1 ratio. '
			question_txt += 'What would be the expected phenotypic ratio in the F<sub>2</sub> generation if the original dihybrid cross is continued?'

			answer_txt = dihybrid_ratio
			colon_count = answer_txt.split(' ')[0].count(':')
			if colon_count == 2:
				choice_set = set(copy.copy(two_colon_choices))
			elif colon_count == 1:
				choice_set = set(copy.copy(one_colon_choices))
			#print(choice_set)
			#print(answer_txt)
			possible_answers = set(inverse_ratios[test_ratio])
			#print(possible_answers)
			choices_list = list(choice_set.difference(possible_answers))

			#print(choices_list)

			#possibilities = math.comb(len(choices_list), 4)
			#print("There are {0} possibilities\n".format(possibilities))

			random.shuffle(choices_list)
			choices_list = choices_list[:4]
			choices_list.append(answer_txt)
			choices_list = sorted(choices_list, key=firstDigit)
			choices_list.reverse()

			bbformat = bptools.formatBB_MC_Question(N, question_txt, choices_list, answer_txt)
			f.write(bbformat)


