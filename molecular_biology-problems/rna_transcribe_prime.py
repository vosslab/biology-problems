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
	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=True)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=False)

	answer_seq = seqlib.complement(question_seq)
	answer_mRNA = seqlib.transcribe(answer_seq)

	if random.randint(1,2) == 1:
		choice_fivetothree = True
		answer_table = seqlib.Single_Strand_Table(seqlib.flip(answer_mRNA), fivetothree=True)
	else:
		choice_fivetothree = False
		answer_table = seqlib.Single_Strand_Table(answer_mRNA, fivetothree=False)

	question_text = ''
	question_text += question_table
	question_text += '<p>Which one of the following sequences below would be the mRNA product '
	question_text += 'produced from transcription of the DNA template strand above?</p>'
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
		mRNA = seqlib.transcribe(choice)
		if choice_fivetothree is True:
			choice_table = seqlib.Single_Strand_Table(seqlib.flip(mRNA), fivetothree=True)
		elif choice_fivetothree is False:
			choice_table = seqlib.Single_Strand_Table(mRNA, fivetothree=False)
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
