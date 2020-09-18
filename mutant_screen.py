#!/usr/bin/env python

import sys
import copy
import random

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_metabolites = int(sys.argv[1])
	else:
		num_metabolites = 4
	charlist = "ABCDEGHJKMPQRSTWXYZ"
	ordered = list(charlist[-num_metabolites:])

	metabolites = copy.copy(ordered)
	random.shuffle(metabolites)
	for i in range(len(metabolites)-1):
		sys.stderr.write(metabolites[i]+" -> ")
	sys.stderr.write(metabolites[-1])
	print("")

	classes = copy.copy(ordered)
	random.shuffle(classes)
	print(classes)
	print(metabolites)
	print(ordered)
	print("")

	for m in ordered:
		sys.stderr.write("\t"+m)
	sys.stderr.write('\n')
	for i in range(len(classes)):
		alive = False
		sys.stderr.write("Class %d\t"%(i+1))
		happylist = {}
		happymeta = classes[i]
		for m in metabolites:
			if m == happymeta:
				alive = True
			happylist[m] = alive
		for m in ordered:
			if happylist[m] is True:
				sys.stderr.write('+\t')
			else:
				sys.stderr.write('-\t')
		sys.stderr.write('\n')

	print("")






