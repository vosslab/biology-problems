#!/usr/bin/env python

import random
import genotype


def deconstructPowerOfNumber(num):
	temp_num = num
	power2 = 0
	power3 = 0
	while temp_num % 2 == 0:
		temp_num //= 2
		power2 += 1
	while temp_num % 3 == 0:
		temp_num //= 3
		power3 += 1
	print(num, power2, power3)


if __name__ == '__main__':
	num_genes = 6
	num_questions = 99
	N = 0
	f = open('bbq-gametes_unique_cross_genotype.txt', 'w')
	for i in range(num_questions):
		N += 1
		number = "{0}. ".format(N)
		question = ""
		question += "How many unique genotypes could be produced through hybrid cross between <ul> "
		gamete_count1 = 1
		while gamete_count1 < 2 or gamete_count1 > 16:
			gene_list1 = genotype.createGenotypeList(num_genes)
			geno1, gamete_count1 = genotype.createGenotypeStringFromList(gene_list1)
		gamete_count2 = 1
		while gamete_count2 < 2 or gamete_count2 > 16:
			gene_list2= genotype.createGenotypeList(num_genes)
			geno2, gamete_count2 = genotype.createGenotypeStringFromList(gene_list2)
		total_genotypes = genotype.countGenotypesForCross(gene_list1, gene_list2)


		question1 = "<li>a male (&male;) individual with the genotype {0}</li>".format(geno1)
		question2 = "<li>a female (&female;) individual with the genotype {0}</li>".format(geno2)
		if random.random() < 0.5:
			question += question1 + question2
		else:
			question += question2 + question1
			
		question += "</ul>"

		print("total_genotypes=", total_genotypes)
		deconstructPowerOfNumber(total_genotypes)
		
		f.write("MC\t{0}\t".format(question))
		print("{0}. {1}".format(N, question))

		letters = "ABCDEF"
		for power in range(2, 7):
			value = 2**power
			choice = "2<sup>{0:d}</sup> = {1:d}".format(power, value)
			f.write(choice+'\t')
			if value == gamete_count1:
				prefix = 'x'
				f.write('Correct\t')
			else:
				prefix = ' '
				f.write('Incorrect\t')
			print('- [{0}] {1}. {2}'.format(prefix, letters[power-2], choice))
		print("")
		f.write('\n')
	f.close()

