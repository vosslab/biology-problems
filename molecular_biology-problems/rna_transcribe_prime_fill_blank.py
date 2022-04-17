#!/usr/bin/env python

import os
import sys
import random
import seqlib
import bptools

def write_question(N, seqlen):
	#============================
	seq = seqlib.makeSequence(seqlen)
	
	#============================
	question = "<p>What is the transcribed RNA sequence to the "
	if random.random() < 0.5:
		table = seqlib.Single_Strand_Table(seq, fivetothree=True)
		dirseq = "5'-{0}-3'".format(seq)
		question += "DNA non-template/coding strand sequence {0} ?</p>".format(seqlib.html_monospace(dirseq))
		answer1 = seqlib.transcribe(seq)
	else:
		table = seqlib.Single_Strand_Table(seq, fivetothree=False)
		dirseq = "3'-{0}-5'".format(seq)
		question += "DNA template strand sequence {0} ?</p>".format(seqlib.html_monospace(dirseq))
		answer1 = seqlib.transcribe(seqlib.complement(seq))
	question = table + question

	question += "<p><i> you may include a comma every 3 letters, but "
	question += "do NOT include any extra commas or spaces in your answer. </i>"

	question += "<p>Write your nucleotide sequence only in the 5&prime; -> 3&prime; direction</p>"

	answer1c = seqlib.insertCommas(answer1)
	answer2 = "5'-{0}-3'".format(answer1)
	answer2c = "5'-{0}-3'".format(answer1c)
	answer3 = "5&prime;-{0}-3&prime;".format(answer1)
	answer3c = "5&prime;-{0}-3&prime;".format(answer1c)
	
	answers_list = [answer1, answer2, answer1c, answer2c]
	
	question = bptools.formatBB_FIB_Question(N, question, answers_list)
	return question


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
		num_sequences = 19

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_sequences):
		N = i + 1
		bbtext = write_question(N, seqlen)
		f.write(bbtext)
	f.close()	
