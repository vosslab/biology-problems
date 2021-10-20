#!/usr/bin/env python

import sys
import random
import seqlib

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 10

	#============================
	seq = seqlib.makeSequence(seqlen)
	
	#============================
	question = "blank 1. What is the transcribed RNA sequence to the "
	if random.random() < 0.5:
		dirseq = "5'-{0}-3'".format(seq)
		question += "DNA non-template/coding strand sequence {0} ?".format(seqlib.html_monospace(dirseq))
		answer = seqlib.transcribe(seq)
	else:
		dirseq = "3'-{0}-5'".format(seq)
		question += "DNA template strand sequence {0} ?".format(seqlib.html_monospace(dirseq))
		answer = seqlib.transcribe(seqlib.complement(seq))
	question += " Write your nucleotide sequence only in the 5' -> 3' direction"
	print(question)


	#============================
	print("A. {0}".format(answer))
	print("B. 5'-{0}-3'".format(answer))
