#!/usr/bin/env python

import os
import sys
import random

#local
import seqlib
import bptools

def writeQuestion(N):
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 9

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


if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')

	num_questions = 198
	for i in range(num_questions):
		N = i + 1
		bbformat = writeQuestion(N)
		f.write(bbformat)
	f.close()
	bptools.print_histogram()

