#!/usr/bin/env python3

import os
import random
import seqlib

"""
give the user four different primers and have them choose which one has the lowest/highest melting temp
"""

#=====================
#=====================
def getATcontent(seq):
	at_content = 0
	at_content += seq.count('A')
	at_content += seq.count('T')

#=====================
#=====================
def getCGcontent(seq):
	at_content = 0
	at_content += seq.count('C')
	at_content += seq.count('G')

#=====================
#=====================
def makeSequence(sequence_len, num_at_bases):
	sequence = []
	for i in range(sequence_len - num_at_bases):
		sequence.append(random.choice(('G', 'C')))
	for i in range(num_at_bases):
		sequence.append(random.choice(('A', 'T')))
	seq_text = ''.join(sequence)
	loop_count = 0
	while 'CCC' in seq_text or 'GGG' in seq_text or 'AAA' in seq_text or 'TTT' in seq_text:
		loop_count += 1
		random.shuffle(sequence)
		seq_text = ''.join(sequence)
		if loop_count > 20:
			break
	seq_text = ''.join(sequence)
	return seq_text

#=====================
#=====================
def makeChoices(sequence_len, answer_num_at_bases):
	answer = makeSequence(sequence_len, answer_num_at_bases + random.randint(-1,1))
	wrong_num_at_bases = sequence_len - answer_num_at_bases
	wrong1 = makeSequence(sequence_len, wrong_num_at_bases)
	wrong2 = makeSequence(sequence_len, wrong_num_at_bases+1)
	wrong3 = makeSequence(sequence_len, wrong_num_at_bases-1)
	choices_list = [answer, wrong1, wrong2, wrong3]
	random.shuffle(choices_list)
	return choices_list, answer

#=====================
#=====================
#=====================
#=====================
if __name__ == '__main__':
	sequence_len = 12
	num_off_bases = 3
	num_questions = 199

	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_questions//2):
		for question_type in ('highest', 'lowest'):
			N += 1
			number = "{0}. ".format(N)
			#header = "{0} primer design".format(N)
			question = ("Which one of the following DNA sequences below will have the "
				+"<strong>{0}</strong> melting point (T<sub>m</sub>).</p>".format(
				question_type.upper()
			))
			question += '<p><i>Hint: I tried to make this question pretty easy and it does not require a calculator.</i></p>'

			if question_type == 'highest':
				answer_num_at_bases = num_off_bases
			elif question_type == 'lowest':
				answer_num_at_bases = sequence_len - num_off_bases

			choices_list, answer = makeChoices(sequence_len, answer_num_at_bases)

			f.write("MC\t<p>{0}\t".format(number + question))
			print("{0}. {1}".format(N, question))

			letters = "ABCDEF"
			for i, choice_seq in enumerate(choices_list):
				f.write('{0}\t'.format(seqlib.DNA_Table(choice_seq)))
				if choice_seq == answer:
					prefix = 'x'
					f.write('Correct\t')
				else:
					prefix = ' '
					f.write('Incorrect\t')
				bottom_sequence = seqlib.complement(choice_seq)
				print("- [{0}] {1}. 5'-{2}-3'".format(prefix, letters[i], choice_seq))
				print("-        3'-{0}-5'".format(bottom_sequence))
				print("")
			print("")
			f.write('\n')
	f.close()

