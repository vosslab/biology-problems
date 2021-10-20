#!/usr/bin/env python

import os
import sys
import copy
import random


num_sequence = 10 #fixed for easy
sequence_length = 9
separate = 3

dna = ['A', 'C', 'G', 'T',]
codes = {
	'A': ('A'),
	'B': ('C', 'G', 'T',), # not A
	'C': ('C'),
	'D': ('A', 'G', 'T',), # not C
	'G': ('G'),
	'H': ('A', 'C', 'T',), # not G
	'K': ('G', 'T',),
	'M': ('A', 'C',),
	'N': ('A', 'C', 'G', 'T',),
	'R': ('A', 'G',), # purine
	'S': ('C', 'G',), # strong
	'T': ('T'),
	'V': ('A', 'C', 'G',), # not T
	'W': ('A', 'T',), # weak
	'Y': ('C', 'T',), # pyrimidine
}
invcodes = {
	('A',): 'A',
	('C', 'G', 'T'): 'B',
	('C',): 'C',
	('A', 'G', 'T'): 'D',
	('G',): 'G',
	('A', 'C', 'T'): 'H',
	('G', 'T'): 'K',
	('A', 'C'): 'M',
	('A', 'C', 'G', 'T'): 'N',
	('A', 'G'): 'R',
	('C', 'G'): 'S',
	('T',): 'T',
	('A', 'C', 'G'): 'V',
	('A', 'T'): 'W',
	('C', 'T'): 'Y'
}


#==========================
def colorNucleotide(nt):
	adenine = ' bgcolor="#e6ffe6"' #green
	cytosine = ' bgcolor="#e6f3ff"' #blue
	thymine = ' bgcolor="#ffe6e6"' #red
	guanine = ' bgcolor="#f2f2f2"' #black
	uracil = ' bgcolor="#f3e6ff"' #purple
	if nt == 'A':
		return adenine
	elif nt == 'C':
		return cytosine
	elif nt == 'G':
		return guanine
	elif nt == 'T':
		return thymine
	elif nt == 'U':
		return thymine
	return ''


#==========================
def histogramList(seq_list):
	histogram = {}
	for nt in dna:
		histogram[nt] = seq_list.count(nt)
	return histogram

#==========================
def getConsensus(histogram):
	max_value = -1
	key_list = []
	for k,v in histogram.items():
		if v > max_value:
			max_value = v
	for k,v in histogram.items():
		if v == max_value:
			key_list.append(k)
	return key_list

#==========================
def makeSequenceColumn():
	seq_list = []
	keys = list(codes.keys())
	random.shuffle(keys)
	seq_key = random.choice(keys)
	seq_set = list(codes[seq_key])
	for j in range(num_sequence):
		seq_list.append(random.choice(seq_set))
	histogram = histogramList(seq_list)
	invlist = []
	print(histogram)
	for k,v in histogram.items():
		if v > 0:
			invlist.append(k)
	invkey = tuple(invlist)
	inv_seq_key = invcodes[invkey]
	if inv_seq_key != seq_key:
		print("ERROR key was supposed to be {0} but was only {1}.".format(seq_key, inv_seq_key))
	return seq_list, inv_seq_key

#==========================
def makeSequences():
	sequence_list = []
	for j in range(num_sequence):
		sequence_list.append('')
	consensus = ''
	
	for i in range(sequence_length):
		seq_list, consensus_nt = makeSequenceColumn()
		consensus += consensus_nt
		for j, nt in enumerate(seq_list):
			sequence_list[j] += nt

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
def scoreSequences(seq1, seq2):
	min_length = min(len(seq1), len(seq2))
	score = 0
	for i in range(min_length):
		if seq1[i] == seq2[i]:
			score += 1
	return score

#==========================
def makeHtmlRow(seq):
	htmlrow = ""
	htmlrow += "<tr>"
	for i in range(len(seq)):
		if i > 0 and i % separate == 0:
			htmlrow += "<td>&nbsp;,&nbsp;</td> "
		nt = seq[i]
		htmlrow += "<td {1}>&nbsp;{0}&nbsp;</td> ".format(nt, colorNucleotide(nt))
	return htmlrow

#==========================
def makeHtmlTable(sequence_list):
	table = ""
	table += '<table style="border-collapse: collapse; border: 1px solid silver;"> '
	table += "<tr> "
	for j in range(num_sequence):
		table += makeHtmlRow(sequence_list[j])
	table += '</tr></table> '
	return table

#==========================
def printSequence(seq, consensus=None):
	if consensus is not None:
		score = scoreSequences(seq, consensus)
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

	table = makeHtmlTable(sequence_list)
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
#==========================
if __name__ == '__main__':
	duplicates = 199
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(duplicates):
		complete_question = makeCompleteQuestion()
		f.write(complete_question)
		f.write('\n')
	f.close()

#==========================
#==========================
#==========================
#==========================
