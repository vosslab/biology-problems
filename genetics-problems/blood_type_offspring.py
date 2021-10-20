#!/usr/bin/env python

import os

phenotypes = ['O', 'A', 'B', 'AB',]
genotypes = ['OO', 'AO', 'BO', 'AB',]
pmap = {
	'O': 'OO',
	'A': 'AO',
	'B': 'BO',
	'AB': 'AB',
}
gmap = {
	'OO': 'O',
	'AO': 'A',
	'OA': 'A',
	'AA': 'A',
	'BO': 'B',
	'OB': 'B',
	'BB': 'B',
	'AB': 'AB',
	'BA': 'AB',
}


if __name__ == '__main__':
	N = 0
	"""
	choices = []
	for pheno in phenotypes:
		choice = "Type {0} blood".format(pheno)
		choices.append(choice)
	print(choices)
	"""
	letters = "ABCDEF"

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for pheno1 in phenotypes:
		for pheno2 in phenotypes:
			answers = set()
			N += 1
			number = "{0}. ".format(N)
			question = '<span style="font-family: times new roman, times; font-size: large;">'
			question += 'For the ABO blood group in humans, the i<sup>A</sup> and i<sup>B</sup> alleles are codominant and the i allele is recessive. '
			question += "If a female &female; with <u>type {0} blood</u> marries a male &male; with <u>type {1} blood</u>, ".format(pheno1, pheno2)
			question += "which of the following blood types could their children possibly have? "
			question += "Check all that apply.</span>"
			print(number+question)
			geno1 = pmap[pheno1]
			geno2 = pmap[pheno2]
			for allele1 in geno1:
				for allele2 in geno2:
					geno = allele1+allele2
					pheno = gmap[geno]
					answers.add(pheno)
			#print(answers)
			f.write("MA\t"+question+"\t")
			answermap = {}
			i = 0
			choices = []
			for pheno in phenotypes:
				choice = "Type {0} blood".format(pheno)
				choices.append(choice)
				f.write(choice+"\t")
				if pheno in answers:
					answermap[choice] = True
					f.write("Correct\t")
					prefix = '*'
				else:
					answermap[choice] = False
					prefix = ''
					f.write("Incorrect\t")
				print("{0}{1}. {2}".format(prefix, letters[i], choice))
				i += 1
			print("\n")
			f.write("\n")
	f.close()
