#!/usr/bin/env python

import sys
import string
import random

uppercase = "ABCDEFGHJKMPQRSTVWXYZ"
lowercase = "abcdefghjkmpqrstvwxyz"


def createGenotype(num_genes):
	genestr = ""
	gamete_count = 1
	for i in range(num_genes):
		val = random.random()
		if val < 0.25:
			genestr += uppercase[i] + uppercase[i]
		elif val < 0.75:
			genestr += uppercase[i] + lowercase[i]
			gamete_count *= 2
		else:
			genestr += lowercase[i] + lowercase[i]
		genestr += " "
	return genestr, gamete_count

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_genes = int(sys.argv[1])
	else:
		num_genes = 3

	genestr, gamete_count = createGenotype(num_genes)
	print(gamete_count)
	print(genestr)
	print(genestr.replace(' ', '\t'))

