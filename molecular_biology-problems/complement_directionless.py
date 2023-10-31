#!/usr/bin/env python3

import os
import sys
import random
import argparse

#local
import seqlib
import bptools

def write_question(N, seqlen=9):

	#============================
	question_seq = seqlib.makeSequence(seqlen)
	answer_seq = seqlib.complement(question_seq)
	question_table = seqlib.Single_Strand_Table_No_Primes(question_seq)
	#============================

	question_text = ''
	question_text += question_table
	question_text += "<h5>Which one of the following DNA sequences is complimentary to the direction-less DNA sequence above?</h5>"

	#============================
	choice_list = []
	half = int(seqlen//2)

	#choice 1
	choice_list.append(answer_seq)
	answer_table = seqlib.Single_Strand_Table_No_Primes(answer_seq)
	#choice 2
	choice_list.append(seqlib.flip(question_seq))

	extra_choices = []
	extra_choices.append(answer_seq[:half] + question_seq[half:])
	extra_choices.append(question_seq[:half] + answer_seq[half:])
	extra_choices.append(seqlib.flip(question_seq[:half]) + question_seq[half:])
	extra_choices.append(question_seq[:half] + seqlib.flip(question_seq[half:]))
	extra_choices.append(seqlib.flip(answer_seq[:half]) + answer_seq[half:])
	extra_choices.append(answer_seq[:half] + seqlib.flip(answer_seq[half:]))
	extra_choices.append(answer_seq[:half] + seqlib.flip(question_seq[half:]))
	random.shuffle(extra_choices)
	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)

	while(len(choice_list) < 5 and len(extra_choices) > 0):
		random.shuffle(extra_choices)
		test_seq = extra_choices.pop()
		if not test_seq in choice_list:
			choice_list.append(test_seq)

	choice_table_list = []
	for choice in choice_list:
		choice_table = seqlib.Single_Strand_Table_No_Primes(choice)
		choice_table_list.append(choice_table)

	#============================
	random.shuffle(choice_table_list)
	bbformat = bptools.formatBB_MC_Question(N, question_text, choice_table_list, answer_table)
	return bbformat


#============================
#============================
#============================
if __name__ == '__main__':
	# Initialize the argparse object
	parser = argparse.ArgumentParser(
		description="A script to set sequence length and number of sequences.")

	# Add arguments to the parser
	parser.add_argument('-s', '--seqlen', dest='seqlen', type=int, default=9,
		help='Set the length of the sequence. Default is 9.')
	parser.add_argument('-n', '--num-sequences', dest='num_sequences', type=int, default=24,
		help='Set the number of sequences. Default is 24.')

	# Parse the command-line arguments
	args = parser.parse_args()

	if args.seqlen > 18:
		print('sequence length too long', args.seqlen)
		sys.exit(1)

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(args.num_sequences):
		N = i + 1
		bbformat = write_question(N, args.seqlen)
		f.write(bbformat)
	f.close()
	bptools.print_histogram()
