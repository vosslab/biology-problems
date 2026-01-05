#!/usr/bin/env python3

import sys
import copy
import random
import seqlib
import bptools

dna = ['A', 'C', 'G', 'T',]

"""
num_sequence = 3 #fixed for easy
num_diff_sequence = 1 #fixed for easy / max 3
random_diff_sequence = False
sequence_length = 6
separate = 3
"""

"""
num_sequence = 5 #fixed for easy
num_diff_sequence = 3 #fixed for easy / max 3
random_diff_sequence = True
sequence_length = 12
separate = 3
"""

num_sequence = 9 #fixed for easy
num_diff_sequence = 3 #fixed for easy / max 3
random_diff_sequence = False
sequence_length = 9
separate = 3


#==========================
def makeSequences():
	sequence_list = []
	for j in range(num_sequence):
		sequence_list.append('')
	consensus = ''
	
	for i in range(sequence_length):
		other_dna = copy.copy(dna)
		random.shuffle(other_dna)
		letter = other_dna.pop()
		consensus += letter
		indices = list(range(num_sequence))
		random.shuffle(indices)
		if random_diff_sequence is True:
			diff_sequence_indices = indices[:random.randint(0,num_diff_sequence)]
		else:
			diff_sequence_indices = indices[:num_diff_sequence]
		for j in range(num_sequence):
			if j in diff_sequence_indices:
				sequence_list[j] += other_dna.pop()
			else:
				sequence_list[j] += letter

	return consensus, sequence_list

#==========================
def makeSequencesSafe():
	not_good = True
	i = 0
	while not_good is True:
		i += 1
		#print("trying sequences {0}".format(i))
		consensus, sequence_list = makeSequences()
		not_good = False
		for s in sequence_list:
			if s == consensus:
				not_good = True
	return consensus, sequence_list

#==========================
def printSequence(seq, consensus=None):
	if consensus is not None:
		score = seqlib.sequenceSimilarityScore(seq, consensus)
		sys.stderr.write('{0:02d} '.format(score))
	for i in range(len(seq)):
		if i > 0 and i % separate == 0:
			sys.stderr.write(', ')
		sys.stderr.write(seq[i] + " ")
	sys.stderr.write('\n')

#==========================
def insertCommas(my_str):
	new_str = ''
	for i in range(0, len(my_str), separate):
		new_str += my_str[i:i+separate] + ','
	return new_str[:-1]

# FIB TAB question text TAB answer text TAB answer two text

#==========================
#==========================
def makeCompleteQuestion():
	consensus, sequence_list = makeSequencesSafe()

	#for j in range(num_sequence):
	#	printSequence(sequence_list[j], consensus)
	#printSequence(consensus, consensus)

	table = seqlib.makeHtmlTable(sequence_list)
	question = "What is the consensus sequence for the table above? "
	question += "<br/> <i> you may include a comma every {0} letters, but ".format(separate)
	question += "do not include any extra commas or spaces in your answer. </i>"

	bbquestion = 'FIB\t'
	bbquestion += table + ' <br/> '
	bbquestion += question + '\t'
	bbquestion += consensus + '\t'	
	bbquestion += insertCommas(consensus)

	#============================
	print("blank 1. "+question)
	print("A. {0}".format(consensus))
	print("B. {0}".format(insertCommas(consensus)))
	print('')
	return bbquestion

#==========================
def write_question(N, args):
	return makeCompleteQuestion()


#==========================
#==========================
if __name__ == '__main__':
	parser = bptools.make_arg_parser(description="Generate consensus sequence FIB questions.")
	args = parser.parse_args()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)
	
#==========================
#==========================
#==========================
#==========================
