#!/usr/bin/env python

import sys
import copy
import random

def complement(seq):
	newseq = copy.copy(seq)
	newseq = newseq.replace('A', 'x')
	newseq = newseq.replace('T', 'A')
	newseq = newseq.replace('x', 'T')
	newseq = newseq.replace('G', 'x')
	newseq = newseq.replace('C', 'G')
	newseq = newseq.replace('x', 'C')
	return newseq

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 7

	answers = []
	seq = ""
	for i in range(seqlen):
		seq += random.choice('AGCT')
	answers.append(seq)
	answers.append(seq[::-1])

	print(("source: 5'-%s-3'"%(seq)))
	compl = complement(seq)
	answers.append(compl)
	half = int(seqlen//2)
	answers.append(compl[::-1])
	#print compl
	if seq == compl:
		print("oops")
		sys.exit(1)

	nube = seq[:half] + compl[half:]
	answers.append(nube)

	random.shuffle(answers)
	charlist = "ABCDE"
	for i in range(len(answers)):
		a = answers[i]
		c = charlist[i]
		print(("%s. 5'-%s-3'"%(c, a)))
		
		