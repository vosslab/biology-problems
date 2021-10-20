#!/usr/bin/env python

import sys
import seqlib
import random

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		seqlen = int(sys.argv[1])
	else:
		seqlen = 10

	#============================
	seq = seqlib.makeSequence(seqlen)
	answer = seqlib.complement(seq)

	#============================
	print("1. Which one of the following DNA sequences is complimentary to the direction-less DNA sequence {0} ?".format(seqlib.html_monospace(seq)))

	#============================
	choices = []
	half = int(seqlen//2)

	#choice 1
	choices.append(answer)
	#choice 2
	choices.append(seqlib.flip(seq))

	extra_choices = []
	extra_choices.append(answer[:half] + seq[half:])
	extra_choices.append(seq[:half] + answer[half:])
	extra_choices.append(seqlib.flip(seq[:half]) + seq[half:])
	extra_choices.append(seq[:half] + seqlib.flip(seq[half:]))
	extra_choices.append(seqlib.flip(answer[:half]) + answer[half:])
	extra_choices.append(answer[:half] + seqlib.flip(answer[half:]))
	extra_choices.append(answer[:half] + seqlib.flip(seq[half:]))
	random.shuffle(extra_choices)
	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)

	for i in range(3):
		choices.append(extra_choices.pop())

	random.shuffle(choices)
	charlist = "ABCDEF"
	for i in range(len(choices)):
		choice_msg = choices[i]
		letter = charlist[i]
		prefix = ""
		if choice_msg == answer:
			prefix = "*"
		print("%s%s. <span style='font-family: monospace;'>%s</span>"%(prefix, letter, choice_msg))
		
		
