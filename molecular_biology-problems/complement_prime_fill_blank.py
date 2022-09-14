#!/usr/bin/env python3

import os
import sys
import random

#local
import seqlib
import bptools

def write_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	answer_seq = seqlib.complement(question_seq)
	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=False)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=True)

	question_text = ''
	question_text += question_table
	question_text += "<h5>What is the complimentary DNA sequence to the DNA sequence above?</h5>"
	question_text += '<p>Hint: pay close attention to the 5&prime; and 3&prime; directions!</p>'
	question_text += "<p><i> you may include a comma every 3 letters, but "
	question_text += "do NOT include any extra commas or spaces in your answer. </i></p>"

	question_text += "<p>Write your nucleotide sequence only in the 5&prime; -> 3&prime; direction</p>"

	#============================
	answer1 = answer_seq
	answer1c = seqlib.insertCommas(answer1)
	answer2 = "5'-{0}-3'".format(answer1)
	answer2c = "5'-{0}-3'".format(answer1c)
	answer3 = "5&prime;-{0}-3&prime;".format(answer1)
	answer3c = "5&prime;-{0}-3&prime;".format(answer1c)

	answers_list = [answer1, answer2, answer1c, answer2c, answer3, answer3c]

	bbformat = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	return bbformat

#============================
#============================
#============================
#============================
if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 9
	if len(sys.argv) >= 3:
		num_sequences = int(sys.argv[2])
	else:
		num_sequences = 24

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_sequences):
		N = i + 1
		bbtext = write_question(N, seqlen)
		f.write(bbtext)
	f.close()
	bptools.print_histogram()
