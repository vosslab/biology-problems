#!/usr/bin/env python

import sys
import seqlib

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 10

	#============================
	seq = seqlib.makeSequence(seqlen)
	answer = seqlib.complement(seq)
	
	#============================
	print("blank 1. What is the complimentary DNA sequence to the direction-less DNA sequence <span style='font-family: monospace;'>{0}</span>?".format(seq))

	#============================
	print("A. {0}".format(answer))
	print("B. {0}".format(seqlib.flip(answer)))
