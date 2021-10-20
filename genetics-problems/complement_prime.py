#!/usr/bin/env python

import sys
import seqlib
import random

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 7

	#============================
	seq = seqlib.makeSequence(seqlen)
	answer = seqlib.flip(seqlib.complement(seq))

	#============================
	if random.random() < 0.5:
		print("1. Which one of the following sequences is complimentary to the sequence <span style='font-family: monospace;'>5'-%s-3'</span>? Hint: pay attention to the 5' and 3' directions!"%(seq))
	else:
		print("1. Which one of the following sequences is complimentary to the sequence <span style='font-family: monospace;'>3'-%s-5'</span>? Hint: pay attention to the 5' and 3' directions!"%(seqlib.flip(seq)))

	#============================
	choices = []
	half = int(seqlen//2)

	#choice 1
	choices.append(seq)
	#choice 2
	choices.append(seqlib.flip(seq))
	#choice 3
	choices.append(answer)
	#choice 4
	choices.append(seqlib.flip(answer))
	#choice 5
	nube = seq[:half] + answer[half:]
	choices.append(nube)

	#============================
	random.shuffle(choices)
	charlist = "ABCDE"
	for i in range(len(choices)):
		choice_msg = choices[i]
		letter = charlist[i]
		prefix = ""
		if choice_msg == answer:
			prefix = "*"
		print("%s%s. <span style='font-family: monospace;'>5'-%s-3'</span>"%(prefix, letter, choice_msg))
		
		
