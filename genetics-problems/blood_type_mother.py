#!/usr/bin/env python

import os
import random

phenotypes = ['O', 'A', 'B', 'AB',]
alleles = ['O', 'A', 'B',]
genotypes = ['OO', 'AO', 'BO', 'AB',]
pmap = {
	'O': 'OO',
	'A': 'AO',
	'B': 'BO',
	'AB': 'AB',
}
pmaplist = {
	'O': ['OO'],
	'A': ['AO', 'AA'],
	'B': ['BO', 'BB'],
	'AB': ['AB'],
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


def getPossibleMomTypes(dad_geno, kid_geno):
	answers = set()
	geno_set = set()
	kid_list = list(kid_geno)
	for dad_allele in dad_geno:
		if not dad_allele in kid_list:
			continue
		kid_list.remove(dad_allele)
	#print("Dad removed"+str(kid_list))
	if len(kid_list) == 2:
		return set()
	elif len(kid_list) == 1:
		#mom must have this allele
		required = kid_list[0]
	else:
		required = None
	#print(required)
	for dad_allele in dad_geno:
		#print(dad_allele)
		kid_list = list(kid_geno)
		if not dad_allele in kid_list:
			continue
		kid_list.remove(dad_allele)
		if required is not None and kid_list[0] != required:
			continue
		#print(kid_list)
		kid_allele = kid_list[0]
		for mom_allele in alleles:
			if kid_allele < mom_allele:
				geno = kid_allele+mom_allele
			else:
				geno = mom_allele+kid_allele
			pheno = gmap[geno]
			simple_geno = pmap[pheno]
			geno_set.add(geno)
			answers.add(pheno)
	#print('{0} + X -> {1} ... {2}'.format(dad_geno, kid_geno, geno_set))
	return geno_set

if __name__ == '__main__':
	#print(getPossibleMomTypes('AO', 'AO'))
	#sys.exit(1)

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
	for dad_pheno in phenotypes:
		for kid_pheno in phenotypes:

			N += 1
			number = "{0}. ".format(N)
			question = '<span style="font-family: times new roman, times; font-size: large;">'
			question += 'For the ABO blood group in humans, the i<sup>A</sup> and i<sup>B</sup> alleles are codominant and the i allele is recessive. '
			offspring = random.choice(('daughter &female;', 'son &male;'))
			question += 'A father &male; who has <u>blood type {0}</u> has a {1} who has <u>blood type {2}</u>, '.format(dad_pheno, offspring, kid_pheno)
			question += "which of the following blood types could the mother &female; possibly have? "
			question += "Check all that apply.</span>"

			answers = set()
			dad_genos = pmaplist[dad_pheno]
			kid_genos = pmaplist[kid_pheno]
			for dad_geno in dad_genos:
				for kid_geno in kid_genos:
					new_answers = getPossibleMomTypes(dad_geno, kid_geno)
					answers = answers.union(new_answers)


			#print(answers)
			#print('Summary {0} + X -> {1} ... {2}'.format(dad_pheno, kid_pheno, answers))
			answer_pheno_dict = {}
			for genotype in answers:
				pheno = gmap[genotype]
				answer_pheno_dict[pheno] = True




			print(number+question)
			f.write("MA\t"+question+"\t")
			answermap = {}
			i = 0
			choices = []
			for pheno in phenotypes:
				choice = "Type {0} blood".format(pheno)
				choices.append(choice)
				f.write(choice+"\t")
				if answer_pheno_dict.get(pheno) is True:
					answermap[choice] = True
					f.write("Correct\t")
					prefix = '*'
				else:
					answermap[choice] = False
					prefix = ''
					f.write("Incorrect\t")
				print("{0}{1}. {2}".format(prefix, letters[i], choice))
				i += 1
			choice = "None of the above are possible; the father &male; is not related to his {0}".format(offspring)
			f.write(choice+"\t")
			if len(answers) == 0:
				answermap[choice] = True
				f.write("Correct\t")
				prefix = '*'
			else:
				answermap[choice] = False
				prefix = ''
				f.write("Incorrect\t")
			print("{0}{1}. {2}".format(prefix, letters[i], choice))
			print("\n")
			f.write("\n")
	f.close()
