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
	question_text += "<h5>What is the complimentary DNA sequence to the direction-less DNA sequence above?</h5>"

	question_text += "<p> <i> Note: you may include a comma every 3 letters, but "
	question_text += "do not include any extra commas or spaces in your answer. </i></p>"
	#============================

	answers_list = []
	answers_list.append(answer_seq)
	answers_list.append(seqlib.flip(answer_seq))
	answers_list.append(seqlib.insertCommas(answer_seq))
	answers_list.append(seqlib.insertCommas(seqlib.flip(answer_seq)))

	#============================
	bbformat = bptools.formatBB_FIB_Question(N, question_text, answers_list)
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
