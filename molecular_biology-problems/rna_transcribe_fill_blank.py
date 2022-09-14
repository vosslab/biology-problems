#!/usr/bin/env python3

import os
import sys

import seqlib
import bptools

def addTextPrimes(my_str):
	return "5'-" + my_str + "-3'"

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 9
	if len(sys.argv) >= 3:
		num_questions = int(sys.argv[1])
	else:
		num_questions = 24

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	
	question_base = ''
	question_base += '<p>Enter the sequence for the mRNA product in the 5&prime; to 3&prime; direction '
	question_base += 'produced from transcription of the DNA template strand above.</p>'	
	question_base += "<p><i> you may include a comma every 3 letters, but "
	question_base += "do NOT include any extra commas or spaces in your answer. </i>"
	question_base += "<br/> <i> also do NOT include the 5' and 3' in your answer. </i></p>"
	for i in range(num_questions):
		#============================
		question_seq = seqlib.makeSequence(seqlen)
		question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=False)

		answer_seq = seqlib.transcribe(seqlib.complement(question_seq))
		#flip_seq = seqlib.flip(answer_seq)
		comma_seq = seqlib.insertCommas(answer_seq)
		answers_list = [answer_seq, addTextPrimes(answer_seq), ]
		answers_list += [comma_seq, addTextPrimes(comma_seq), ]
		
		question_text = question_table + question_base		
		N = i+1
		bbformat = bptools.formatBB_FIB_Question(N, question_text, answers_list)
		f.write(bbformat)
	f.close()
