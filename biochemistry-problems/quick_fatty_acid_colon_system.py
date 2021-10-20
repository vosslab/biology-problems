#!/usr/bin/env python

import os
import random

num2cardinal = {
	1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
	6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
	11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
	15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
	19: 'nineteen', 20: 'twenty', 22: 'twenty-two', 24: 'twenty-four',
}

num2ordinal = {
	1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th',
	6: '6th', 7: '7th', 8: '8th', 9: '9th', 10: '10th',
	11: '11th', 12: '12th', 13: '13th', 14: '14th', 15: '15th',
	16: '16th', 17: '17th', 18: '18th', 19: '19th', 20: '20th',
	22: '22nd', 24: '24th',
}


def wrtieQuestion(chain_length, num_double_bonds):
	cl = chain_length
	ndb = num_double_bonds
	question = 'The notation {0}:{1} indicates '.format(cl, ndb)
	question += 'which of the following about a fatty acid?'

	choices = []
	answer = 'There are {0} carbons in the chain with {1} double bond(s).'.format(cl, ndb)
	choices.append(answer)
	choice = 'There are {0} {1}-carbon chains in this lipid molecule.'.format(num2cardinal[ndb], cl)
	choices.append(choice)
	choice = 'There are {0} carbons in the chain and the {1} carbon has a double bond.'.format(cl, num2ordinal[ndb])
	choices.append(choice)
	choice = 'The {0} carbon in the fatty acid has {1} double bond(s).'.format(num2ordinal[cl], ndb)
	choices.append(choice)
	choice = 'The {0} and {1} carbons in the fatty acid chain have double bonds.'.format(num2ordinal[ndb], num2ordinal[cl],)
	choices.append(choice)

	random.shuffle(choices)

	complete_question = 'MC\t'
	complete_question += question
	for c in choices:
		complete_question += '\t'+c
		if c == answer:
			complete_question += '\tCorrect'
		else:
			complete_question += '\tIncorrect'
	complete_question += '\n'
	print(complete_question)
	return complete_question


if __name__ == '__main__':
	possible_chain_lengths = [12,14,16,18,20,22,24]
	possible_num_double_bonds = [1,2,3,4]

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')

	for chain_length in possible_chain_lengths:
		for num_double_bonds in possible_num_double_bonds:
			complete_question = wrtieQuestion(chain_length, num_double_bonds)
			f.write(complete_question)
	f.close()
