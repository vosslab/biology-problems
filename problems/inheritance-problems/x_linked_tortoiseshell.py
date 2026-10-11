#!/usr/bin/env python3

import random
from fractions import Fraction

import bptools


TEXT_LABELS = {
	"orange": ("orange", "#9b4a00"),
	"black": ("black", "#222222"),
	"female": ("female (&female;)", "#990070"),
	"females": ("females (&female;)", "#990070"),
	"daughters": ("daughters (&female;)", "#990070"),
	"male": ("male (&male;)", "#002499"),
}


#=====================
def color_labels(text):
	"""Give coat phenotypes and sex labels consistent colors and sex symbols."""
	replacements = {
		word: bptools.colorHTMLText(label, color[1:])
		for word, (label, color) in TEXT_LABELS.items()
	}
	# Alternate orange and black letters, keeping the mixed-coat label together.
	coat_colors = (TEXT_LABELS["orange"][1][1:], TEXT_LABELS["black"][1][1:])
	letters = ''.join(
		bptools.colorHTMLText(letter, coat_colors[index % 2])
		for index, letter in enumerate("tortoiseshell")
	)
	replacements["tortoiseshell"] = f'<span style="white-space: nowrap;">{letters}</span>'
	colored_text = bptools.applyReplacementRulesToText(text, replacements)
	return colored_text


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
	# The student-facing group "daughters" corresponds to female outcomes.
	target_sex = "female" if target_group == "daughters" else "offspring"
	answer_fraction = fraction_matching(outcomes, target_sex, "tortoiseshell")
	return female_pheno, male_pheno, target_group, answer_fraction


#=====================
def write_question(N, args):
	female_pheno, male_pheno, target_group, answer_fraction = make_cross()
	female_article = "An" if female_pheno == "orange" else "A"
	male_article = "an" if male_pheno == "orange" else "a"

	question_text = (
		"<p>In these cats, orange versus black coat color is X-linked. "
		"Heterozygous females are tortoiseshell. "
		"Assume equal numbers of female (XX) and male (XY) kittens.</p>"
	)
	question_text += (
		f"<p>{female_article} {female_pheno} female mates with {male_article} {male_pheno} male.</p>"
	)
	if target_group == "offspring":
		question_text += "<p>What fraction of all kittens are expected to be tortoiseshell?</p>"
	else:
		question_text += "<p>What fraction of daughters are expected to be tortoiseshell?</p>"

	question_text = color_labels(question_text)
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
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == "__main__":
	main()
