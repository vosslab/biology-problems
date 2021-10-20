#!/usr/bin/env python

import os
import random

def geno2pheno(genotype):
	if genotype.startswith('+'):
		phenotype = "red"
	else:
		phenotype = "white"
	if '-' in genotype:
		phenotype += " male"
	else:
		phenotype += " female"
	return phenotype

def get_answer(female_genotype, male_genotype):
	if female_genotype == "++":
		return 0
	elif female_genotype == "+w":
		if male_genotype == "+-":
			return 1
		elif male_genotype == "w-":
			return 2
	elif female_genotype == "ww":
		if male_genotype == "+-":
			return 3
		elif male_genotype == "w-":
			return 4

def cross_experiment(female_genotype, male_genotype, progeny_size=400):
	distribution = {}
	for i in range(progeny_size):
		a = random.choice(list(female_genotype))
		b = random.choice(list(male_genotype))
		offspring = [a,b]
		offspring.sort()
		offspring_str = offspring[0]+offspring[1]
		distribution[offspring_str] = distribution.get(offspring_str, 0) + 1
	#sys.exit(1)
	return distribution

def print_distribution_string(distribution):
	keys = list(distribution.keys())
	keys.sort()
	pcount = {}
	for key in keys:
		phenotype = geno2pheno(key)
		pcount[phenotype] = pcount.get(phenotype,0) + distribution[key]

	pkeys = list(pcount.keys())
	pkeys.sort()
	mystr = ""
	for pkey in pkeys:
		mystr += "{0}: {1:d}, ".format(pkey, pcount[pkey])
	print(mystr)

def print_distribution_table(distribution):
	keys = list(distribution.keys())
	keys.sort()
	pcount = {}
	for key in keys:
		phenotype = geno2pheno(key)
		pcount[phenotype] = pcount.get(phenotype,0) + distribution[key]

	pkeys = list(pcount.keys())
	pkeys.sort()
	mystr = '<table cellpadding="2" cellspacing="2" style="border-collapse: collapse; text-align:center; border: 1px solid black; font-size: 14px;">'
	mystr += "<tr><th>phenotype</th><th>female &female;</th><th>male &male;</th></tr> "
	mystr += "<tr><td>red-eyed (wildtype)</td><td align='center'>{0}</td><td align='center'>{1}</td></tr> ".format(pcount.get('red female', 0), pcount.get('red male', 0))
	mystr += "<tr><td>white-eyed (mutant)</td><td align='center'>{0}</td><td align='center'>{1}</td></tr> ".format(pcount.get('white female', 0), pcount.get('white male', 0))
	mystr += "</table><br/>"
	return mystr


if __name__ == '__main__':
	#for female_genotype in ("++", "+w", "ww"):
	#	for male_genotype in ("+-", "w-"):
	duplicates = 4
	choices = [
		'homozygous wildtype female (++) and male of unknown genotype',
		'heterozygous female (+w) and wildtype male (+&ndash;)',
		'heterozygous female (+w) and mutant male (w&ndash;)',
		'homozygous mutant female (ww) and wildtype male (+&ndash;)',
		'homozygous mutant female (ww) and mutant male (w&ndash;)',
	]
	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	post_question = "<p><strong>What are the genotypes of the parents in this cross?</strong></p>"
	female_genotype = random.choice(("++", "+w", "ww"))
	male_genotype = random.choice(("+-", "w-"))
	letters = "ABCDEFG"
	progeny_size_selection = (160, 200, 400, 600,)
	for i in range(duplicates):
		for progeny_size in progeny_size_selection:
			for female_genotype in ("++", "+w", "ww"):
				for male_genotype in ("+-", "w-"):
					if female_genotype == "++" and male_genotype == "+-":
						continue
					pre_question = "<p>The white-eyed phenotype is an X-linked recessive disorder in fruit flies. The red allele, +, is dominant to the white allele, w. The offspring of size {0} from the mating of a single female and a single male are shown in the table below:</p>".format(progeny_size)
					N += 1
					print(female_genotype)
					print(male_genotype)
					distribution = cross_experiment(female_genotype, male_genotype, progeny_size)
					answer_id = get_answer(female_genotype, male_genotype)

					bad_cross = False
					for key in distribution:
						if distribution[key] % 5 == 0:
							bad_cross = True
					if bad_cross is True:
						continue
					print_distribution_string(distribution)
					print(pre_question)
					table = print_distribution_table(distribution)
					print(table)
					print(post_question)
					choice_txt = ""
					for j, choice in enumerate(choices):
						if j == answer_id:
							prefix = "*"
							status = "Correct"
						else:
							prefix = ""
							status = "Incorrect"
						print('{0}{1}. {2}'.format(prefix, letters[j], choice))
						choice_txt += "\t{0}\t{1}".format(choice, status)
					f.write("MC\t{0}{1}{2}{3}\n".format(pre_question, table, post_question, choice_txt))
					print("")
	f.close()

