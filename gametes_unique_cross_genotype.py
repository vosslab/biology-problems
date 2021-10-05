#!/usr/bin/env python

import os
import random
import genotype



if __name__ == '__main__':
	num_genes = 6
	num_questions = 299
	max_choices = 5
	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
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

		#print("total_genotypes=", total_genotypes)
		power2, power3 = genotype.deconstructPowerOfNumber(total_genotypes)
		choice_text = genotype.formatChoice(power2, power3)
		answer = (total_genotypes, choice_text)
		
		f.write("MC\t{0}\t".format(question))
		print("{0}. {1}".format(N, question))

		letters = "ABCDEF"
		choices = []
		for diff_power2 in range(-2, 3):
			for diff_power3 in range(-2, 3):
				if diff_power2 == 0 and diff_power3 == 0:
					continue
				npow2 = power2 + diff_power2
				npow3 = power3 + diff_power3
				if npow2 < 0 or npow3 < 0:
					continue
				if npow2 + npow3 > num_genes:
					continue
				if npow2 + npow3 < 2:
					continue
				num = 2**npow2 * 3**npow3
				choice_text = genotype.formatChoice(npow2, npow3)
				choices.append((num, choice_text))

		#limit choices
		random.shuffle(choices)
		choices = choices[:max_choices-1]
		choices.append(answer)
		choices.sort()
		
		for i, choice in enumerate(choices):
			value, choice_text = choice
			f.write(choice_text+'\t')
			if value == total_genotypes:
				prefix = 'x'
				f.write('Correct\t')
			else:
				prefix = ' '
				f.write('Incorrect\t')
			print('- [{0}] {1}. {2}'.format(prefix, letters[i], choice_text))
		print("")
		f.write('\n')
	f.close()

