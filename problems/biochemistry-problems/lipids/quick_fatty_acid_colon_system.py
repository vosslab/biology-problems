#!/usr/bin/env python3

import random

import bptools

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


def _format_question(chain_length, num_double_bonds, question_num):
	cl = chain_length
	ndb = num_double_bonds
	question = f'The notation {cl}:{ndb} indicates '
	question += 'which of the following about a fatty acid?'

	choices = []
	answer = f'There are {cl} carbons in the chain with {ndb} double bond(s).'
	choices.append(answer)
	choice = f'There are {num2cardinal[ndb]} {cl}-carbon chains in this lipid molecule.'
	choices.append(choice)
	choice = f'There are {cl} carbons in the chain and the {num2ordinal[ndb]} carbon has a double bond.'
	choices.append(choice)
	choice = f'The {num2ordinal[cl]} carbon in the fatty acid has {ndb} double bond(s).'
	choices.append(choice)
	choice = f'The {num2ordinal[ndb]} and {num2ordinal[cl]} carbons in the fatty acid chain have double bonds.'
	choices.append(choice)

	random.shuffle(choices)

	complete_question = bptools.formatBB_MC_Question(question_num, question, choices, answer)
	return complete_question

#=========================================
#=========================================
def write_question(N: int, args) -> str:
	possible_chain_lengths = [12, 14, 16, 18, 20, 22, 24]
	possible_num_double_bonds = [1, 2, 3, 4]
	chain_length = random.choice(possible_chain_lengths)
	num_double_bonds = random.choice(possible_num_double_bonds)
	return _format_question(chain_length, num_double_bonds, N)

#=========================================
#=========================================
def parse_arguments():
	parser = bptools.make_arg_parser(description='Generate fatty acid notation questions.')
	args = parser.parse_args()
	return args

#=========================================
#=========================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#=========================================
#=========================================
if __name__ == '__main__':
	main()
