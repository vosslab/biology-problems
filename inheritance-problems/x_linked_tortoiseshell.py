#!/usr/bin/env python3

import random
from fractions import Fraction

import bptools


CHOICES = {
	Fraction(0, 1): "None, 0%",
	Fraction(1, 4): "1/4, 25%",
	Fraction(1, 2): "1/2, 50%",
	Fraction(3, 4): "3/4, 75%",
	Fraction(1, 1): "All, 100%",
}

FEMALE_GENOTYPES = {
	"orange": ("O", "O"),
	"black": ("B", "B"),
	"tortoiseshell": ("O", "B"),
}

MALE_GENOTYPES = {
	"orange": ("O", "Y"),
	"black": ("B", "Y"),
}


#=====================
def female_phenotype(genotype):
	if genotype[0] == genotype[1] == "O":
		return "orange"
	if genotype[0] == genotype[1] == "B":
		return "black"
	return "tortoiseshell"


#=====================
def male_phenotype(genotype):
	return "orange" if genotype[0] == "O" else "black"


#=====================
def offspring_outcomes(female_genotype, male_genotype):
	female_gametes = list(female_genotype)
	male_gametes = list(male_genotype)
	outcomes = []
	for egg in female_gametes:
		for sperm in male_gametes:
			if sperm == "Y":
				offspring = ("male", (egg, "Y"), male_phenotype((egg, "Y")))
			else:
				offspring = ("female", (egg, sperm), female_phenotype((egg, sperm)))
			outcomes.append(offspring)
	return outcomes


#=====================
def fraction_matching(outcomes, target_sex, target_pheno):
	if target_sex == "offspring":
		selected = outcomes
	else:
		selected = [o for o in outcomes if o[0] == target_sex]
	matching = [o for o in selected if o[2] == target_pheno]
	if not selected:
		return Fraction(0, 1)
	return Fraction(len(matching), len(selected))


#=====================
def make_cross():
	female_pheno = random.choice(list(FEMALE_GENOTYPES.keys()))
	male_pheno = random.choice(list(MALE_GENOTYPES.keys()))
	female_genotype = FEMALE_GENOTYPES[female_pheno]
	male_genotype = MALE_GENOTYPES[male_pheno]
	target_group = random.choice(("offspring", "daughters"))

	outcomes = offspring_outcomes(female_genotype, male_genotype)
	answer_fraction = fraction_matching(outcomes, target_group, "tortoiseshell")
	return female_pheno, male_pheno, target_group, answer_fraction


#=====================
def write_question(N, args):
	female_pheno, male_pheno, target_group, answer_fraction = make_cross()

	question_text = (
		"<p>In cats, coat color is X-linked. The orange (O) and black (B) alleles are codominant, "
		"so heterozygous females are tortoiseshell.</p>"
	)
	question_text += (
		f"<p>A {female_pheno} female (&female;) mates with a {male_pheno} male (&male;).</p>"
	)
	if target_group == "offspring":
		question_text += "<p>What fraction of all kittens are expected to be tortoiseshell?</p>"
	else:
		question_text += "<p>What fraction of daughters (&female;) are expected to be tortoiseshell?</p>"

	answer_text = CHOICES[answer_fraction]
	choices_list = list(CHOICES.values())

	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_question


#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate questions.")
	args = parser.parse_args()
	return args


#===========================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == "__main__":
	main()
