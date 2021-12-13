#!/usr/bin/env python

import os
import sys
import random

#local
import seqlib
import bptools

def write_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=False)

	if random.randint(1,2) == 1:
		choice_fivetothree = True
	else:
		choice_fivetothree = False

	answer_seq = seqlib.complement(question_seq)
	answer_table = seqlib.Single_Strand_Table(answer_seq, choice_fivetothree)

	question_text = ''
	question_text += question_table
	question_text += '<h5>Which one of the following sequences below is complimentary to '
	question_text += 'the DNA sequence above?</h5>'
	question_text += '<p>Hint: pay close attention to the 5&prime; and 3&prime; directions!</p>'

	#============================
	choice_list = []
	half = int(seqlen//2)

	#choice 1
	choice_list.append(question_seq)
	#choice 2
	choice_list.append(seqlib.flip(question_seq))
	#choice 3
	choice_list.append(answer_seq)
	#choice 4
	choice_list.append(seqlib.flip(answer_seq))
	#choice 5
	nube = question_seq[:half] + answer_seq[half:]
	choice_list.append(nube)
	
	choice_table_list = []
	for choice in choice_list:
		choice_table = seqlib.Single_Strand_Table(choice, choice_fivetothree)
		choice_table_list.append(choice_table)

	#============================
	random.shuffle(choice_table_list)
	bbformat = bptools.formatBB_MC_Question(N, question_text, choice_table_list, answer_table)
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
		seqlen = int(sys.argv[2])
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
