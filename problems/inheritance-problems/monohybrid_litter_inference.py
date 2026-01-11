#!/usr/bin/env python3

import random

import bptools


TRAITS = [
	{
		"organism": "cat",
		"dominant": "short hair",
		"recessive": "long hair",
		"trait": "hair length",
	},
	{
		"organism": "person",
		"dominant": "widow's peak",
		"recessive": "straight hairline",
		"trait": "hairline shape",
	},
	{
		"organism": "pea plant",
		"dominant": "round seeds",
		"recessive": "wrinkled seeds",
		"trait": "seed shape",
	},
	{
		"organism": "mouse",
		"dominant": "black fur",
		"recessive": "brown fur",
		"trait": "fur color",
	},
]

GENOTYPES = ("AA", "Aa", "aa")


#=====================
def gametes_for_genotype(genotype):
	if genotype == "AA":
		return ("A", "A")
	if genotype == "aa":
		return ("a", "a")
	return ("A", "a")


#=====================
def phenotype_for_genotype(genotype, trait):
	if "A" in genotype:
		return trait["dominant"]
	return trait["recessive"]


#=====================
def offspring_ratio(parent_one, parent_two):
	offspring = []
	for g1 in gametes_for_genotype(parent_one):
		for g2 in gametes_for_genotype(parent_two):
			offspring.append("".join(sorted([g1, g2], reverse=True)))
	dominant = sum(1 for g in offspring if "A" in g)
	recessive = len(offspring) - dominant
	return dominant, recessive


#=====================
def choose_informative_cross():
	for _ in range(200):
		known_genotype = random.choice(("Aa", "aa"))
		unknown_genotype = random.choice(GENOTYPES)
		dominant, recessive = offspring_ratio(known_genotype, unknown_genotype)
		if known_genotype == "Aa":
			candidates = {
				"AA": offspring_ratio("Aa", "AA"),
				"Aa": offspring_ratio("Aa", "Aa"),
				"aa": offspring_ratio("Aa", "aa"),
			}
		else:
			candidates = {
				"AA": offspring_ratio("aa", "AA"),
				"Aa": offspring_ratio("aa", "Aa"),
				"aa": offspring_ratio("aa", "aa"),
			}
		matching = [g for g, ratio in candidates.items() if ratio == (dominant, recessive)]
		if len(matching) == 1:
			return known_genotype, unknown_genotype, (dominant, recessive)
	return "Aa", "aa", (2, 2)


#=====================
def choose_litter_size(ratio):
	dominant, recessive = ratio
	if dominant == 4 and recessive == 0:
		return random.choice((8, 10, 12))
	if dominant == 0 and recessive == 4:
		return random.choice((8, 10, 12))
	if dominant == 2 and recessive == 2:
		return random.choice((8, 10, 12))
	if dominant == 3 and recessive == 1:
		return random.choice((8, 12, 16))
	return 8


#=====================
def parent_description(genotype, trait, role):
	phenotype = phenotype_for_genotype(genotype, trait)
	if genotype == "AA":
		return f"A true-breeding {role} with {phenotype}"
	if genotype == "aa":
		return f"A true-breeding {role} with {phenotype}"
	return f"A {role} with {phenotype} known to be heterozygous"


#=====================
def write_question(N, args):
	trait = random.choice(TRAITS)
	known_genotype, unknown_genotype, ratio = choose_informative_cross()
	litter_size = choose_litter_size(ratio)
	dominant_count = litter_size * ratio[0] // 4
	recessive_count = litter_size * ratio[1] // 4

	known_parent = parent_description(known_genotype, trait, trait["organism"])
	question_text = (
		f"<p>{known_parent} is crossed with an individual of unknown genotype. "
		f"In a large litter of {litter_size} offspring, "
		f"{dominant_count} show {trait['dominant']} and {recessive_count} show "
		f"{trait['recessive']}.</p>"
	)
	question_text += (
		"<p>Assume a single gene with A dominant to a. "
		"What is the most likely genotype of the unknown parent?</p>"
	)

	choices_list = [
		bptools.html_monospace("AA"),
		bptools.html_monospace("Aa"),
		bptools.html_monospace("aa"),
		"Cannot be determined from the data given",
	]
	answer_text = bptools.html_monospace(unknown_genotype)
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
