#!/usr/bin/env python

import sys
import string
import random

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_genes = int(sys.argv[1])
	else:
		num_genes = 3

	genestr = ""
	for i in range(num_genes):
		val = random.random()
		if val < 0.25:
			genestr += string.uppercase[i] + string.uppercase[i]
		elif val < 0.75:
			genestr += string.uppercase[i] + string.lowercase[i]
		else:
			genestr += string.lowercase[i] + string.lowercase[i]
		genestr += "\t"
	print genestr
	print genestr.replace('\t', ' ')
