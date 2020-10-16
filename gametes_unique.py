#!/usr/bin/env python

import random
import genotype


if __name__ == '__main__':
	num_genes = 7
	num_questions = 99
	N = 0
	f = open('bbq-gametes_unique.txt', 'w')
	for i in range(num_questions):
		N += 1
		number = "{0}. ".format(N)
		question = ""
		question += "How many unique gametes could be produced through independent assortment by "
		gamete_count = 1
		while gamete_count < 4 or gamete_count > 32:
			geno, gamete_count = genotype.createGenotype(num_genes)
		question += "an individual with the genotype {0}?".format(geno)

		
		f.write("MC\t{0}\t".format(question))
		print("{0}. {1}".format(N, question))

		letters = "ABCDEF"
		for power in range(2, 7):
			value = 2**power
			choice = "2<sup>{0:d}</sup> = {1:d}".format(power, value)
			f.write(choice+'\t')
			if value == gamete_count:
				prefix = 'x'
				f.write('Correct\t')
			else:
				prefix = ' '
				f.write('Incorrect\t')
			print('- [{0}] {1}. {2}'.format(prefix, letters[power-2], choice))
		print("")
		f.write('\n')
	f.close()

