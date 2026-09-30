#!/usr/bin/env python3
"""One-cross probabilities with incomplete dominance and codominance at two genes."""

# Standard Library
import random
import argparse
import fractions
import itertools

# Local modules
import bptools
import plantprobabilitylib

# Each row lists second-allele homozygote, heterozygote, first-allele homozygote.
PETALS = {
	"incomplete": ("white petals", "pink petals", "red petals"),
	"codominant": ("white petals", "red and white patches on petals", "red petals"),
}
MARKINGS = {
	"incomplete": ("thin stripes", "medium-width stripes", "wide stripes"),
	"codominant": ("dots", "dots and stripes", "stripes"),
}
MODELS = (
	("incomplete", "incomplete"),
	("codominant", "codominant"),
	("codominant", "incomplete"),
)
SCENARIOS: list[tuple] = []


#=====================
def phenotype_text(model: tuple, genotype: tuple) -> str:
	text = f"{PETALS[model[0]][genotype[0]]} with {MARKINGS[model[1]][genotype[1]]}"
	return text


#=====================
def possible_requests(first: tuple, second: tuple, offspring: set) -> list:
	"""Offer relational prompts first; equivalent direct targets are removed by the pool."""
	requests = [
		("parent_one", frozenset((first,))),
		("parent_two", frozenset((second,))),
		("either_parent", frozenset((first, second))),
		("new_combination", frozenset(((first[0], second[1]),))),
		("different", frozenset(offspring - {first, second})),
	]
	requests.extend(("specific", frozenset((genotype,))) for genotype in sorted(offspring))
	for a_values in itertools.combinations(range(3), 2):
		for b in range(3):
			requests.append(("either_color", frozenset((a, b) for a in a_values)))
	return requests


#=====================
def build_scenarios() -> list[tuple]:
	scenarios = []
	for model in MODELS:
		for first, second in itertools.combinations_with_replacement(
				plantprobabilitylib.GENOTYPES, 2):
			# Require segregation at both genes so neither gene is irrelevant to the cross.
			if any(len(plantprobabilitylib.locus_counts(a, b)) < 2
					for a, b in zip(first, second)):
				continue
			distribution = plantprobabilitylib.cross_distribution(first, second)
			offspring = set(distribution)
			seen_targets = set()
			for kind, targets in possible_requests(first, second, offspring):
				# No impossible targets, cosmetic rewrites, or long sums of many outcomes.
				if not targets or not targets <= offspring or len(targets) > 3:
					continue
				if targets in seen_targets or targets == offspring:
					continue
				seen_targets.add(targets)
				scenarios.append((model, first, second, kind, tuple(sorted(targets))))
	return scenarios


#=====================
def phenotype_tables(model: tuple) -> str:
	text = ""
	for index, (gene, title, descriptions) in enumerate((
		("A", "Petal color", PETALS[model[0]]),
		("B", "Flower markings", MARKINGS[model[1]]),
	)):
		text += plantprobabilitylib.table_start(title)
		style = plantprobabilitylib.CELL_STYLE
		text += f"<tr><th scope='col' style='{style}'>Genotype</th>"
		text += f"<th scope='col' style='{style}'>Appearance</th></tr>"
		for copies in (2, 1, 0):
			background = ("#f6e5f4", "#e2eef9")[index]
			text += f"<tr><th scope='row' style='{style} background-color: {background};'>"
			text += f"<span style='color: {plantprobabilitylib.GENE_COLORS[index]};'>"
			text += plantprobabilitylib.locus_text(copies, gene) + "</span></th>"
			text += f"<td style='{style}'>{descriptions[copies]}</td></tr>"
		text += "</table>"
	return text


#=====================
def request_text(model: tuple, kind: str, targets: tuple) -> str:
	if kind == "parent_one":
		outcome = "the same petal color and markings as Parent 1"
	elif kind == "parent_two":
		outcome = "the same petal color and markings as Parent 2"
	elif kind == "either_parent":
		outcome = "the same petal color and markings as either parent"
	elif kind == "new_combination":
		outcome = "Parent 1's petal color and Parent 2's markings"
	elif kind == "different":
		outcome = "a combination of petal color and markings that neither parent has"
	elif kind == "either_color":
		colors = " or ".join(PETALS[model[0]][genotype[0]] for genotype in targets)
		markings = MARKINGS[model[1]][targets[0][1]]
		outcome = f"{colors}, together with {markings}"
	else:
		outcome = phenotype_text(model, targets[0])
	text = f"<p>What is the probability that an offspring will have <strong>{outcome}</strong>?</p>"
	return text


#=====================
def answer_terms(first: tuple, second: tuple, targets: tuple) -> tuple:
	a_counts = plantprobabilitylib.locus_counts(first[0], second[0])
	b_counts = plantprobabilitylib.locus_counts(first[1], second[1])
	terms = tuple((fractions.Fraction(a_counts[a], 4), fractions.Fraction(b_counts[b], 4))
		for a, b in targets)
	return terms


#=====================
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	model, first, second, kind, targets = SCENARIOS[N - 1]
	text = "<p>In fictional mosaic plants, gene A affects petal color and gene B affects "
	text += "flower markings. The genes assort independently. The tables show each genotype's "
	text += "appearance.</p>"
	text += phenotype_tables(model)
	text += "<p>Two plants are crossed:<br/>"
	text += f"<strong>Parent 1:</strong> {phenotype_text(model, first)}<br/>"
	text += f"<strong>Parent 2:</strong> {phenotype_text(model, second)}</p>"
	text += request_text(model, kind, targets)
	choices, answer = plantprobabilitylib.make_choices(answer_terms(first, second, targets))
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


#=====================
def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(
		description="Two-gene phenotype probabilities in fictional plants.")
	args = parser.parse_args()
	return args


#=====================
def main() -> None:
	args = parse_arguments()
	global SCENARIOS
	SCENARIOS = build_scenarios()
	random.shuffle(SCENARIOS)
	plantprobabilitylib.cap_questions(args, len(SCENARIOS))
	bptools.collect_and_write_questions(write_question, args, bptools.make_outfile())


if __name__ == "__main__":
	main()
