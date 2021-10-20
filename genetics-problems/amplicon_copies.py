#!/usr/bin/env python

import os
import random

if __name__ == '__main__':
	num_cycles = 12
	num_choices = 6
	N = 0
	answer_hist = {}
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_cycles):
		N += 1
		number = "{0}. ".format(N)
		question = ""
		question += "Starting with genomic DNA, how many copies of the double-stranded "
		question += "amplicon of the exact length are there after {0} rounds of PCR?".format(N)
		if N < 2:
			amplicon_copies = 0
		else:
			amplicon_copies = 2**(N-2)
		


		letters = "ABCDEF"
		#orig = int(N - num_choices - 1) #allow answers to be letter E, which means 2^cycles is not a choice
		orig = int(N - num_choices + 1) #make sure 2^cycles is a choice
		for shift in range(5):
			start = orig + shift
			if start < -1:
				continue
			stop = start + num_choices #have 5 choices
			print("amplicon_copies = {0}; 2^start = {1}".format(amplicon_copies, 2**start))
			if start > -1 and 2**start > amplicon_copies:
				continue
			f.write("MC\t{0}\t".format(question))
			print("{0}. {1}".format(N, question))

	
			for i, power in enumerate(range(start, stop)):
				value = 2**power
				if value < 1:
					value = 0
				#print("value = {0}".format(value))
				if power >= 2:
					choice = "2<sup>{0:d}</sup> = {1:,d} complete copies".format(power, value)
				elif power == 1:
					choice = "two complete copies"
				elif power == 0:
					choice = "just one complete copy"
				elif power == -1:
					choice = "no copies are complete"
				f.write(choice+'\t')
				if value == amplicon_copies:
					prefix = 'x'
					f.write('Correct\t')
					answer_hist[letters[i]] = answer_hist.get(letters[i], 0) + 1
				else:
					prefix = ' '
					f.write('Incorrect\t')
				print('- [{0}] {1}. {2}'.format(prefix, letters[i], choice))
			print("")
			f.write('\n')
	f.close()
	print(answer_hist)

