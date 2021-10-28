#!/usr/bin/env python

import os
import genotype

if __name__ == '__main__':
	num_genes = 7
	num_questions = 199
	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_questions):
		N += 1
		question = ""
		question += '<p>How many unique <span style="color: Green;"><strong>GAMETES</strong></span> '
		question += 'could be produced through independent assortment by '
		question += 'an individual with the following genotype?</p> '
		gamete_count = 1
		while gamete_count < 4 or gamete_count > 32:
			geno, gamete_count = genotype.createGenotype(num_genes)
		question += '<p>{0}</p>'.format(geno)
		
		
		crc16 = genotype.getCrc16_FromString(question)
		f.write("MC\t<p>{0}. {1}</p> {2}\t".format(N, crc16, question))
		print("{0}. {1} - {2}".format(N, crc16, question))

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

