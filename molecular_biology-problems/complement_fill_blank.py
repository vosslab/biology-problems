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
