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
	"incomplete": ("white", "pink", "red"),
	"codominant": ("white", "red and white patches", "red"),
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
	text = "<div>"
	for index, (gene, title, descriptions) in enumerate((
		("A", "Petal color", PETALS[model[0]]),
		("B", "Flower markings", MARKINGS[model[1]]),
	)):
		# Keep each key intact when tables become images in Blackboard exports.
		text += "<div style='display: inline-block; vertical-align: top; margin-right: 16px;'>"
		text += plantprobabilitylib.table_start(f"{title} (gene <i>{gene}</i>)")
		style = plantprobabilitylib.CELL_STYLE
		text += f"<tr><th scope='col' style='{style}'>Genotype</th>"
		text += f"<th scope='col' style='{style}'>Appearance</th></tr>"
		for copies in (2, 1, 0):
			background = ("#f6e5f4", "#e2eef9")[index]
			text += f"<tr><th scope='row' style='{style} background-color: {background};'>"
			text += f"<span style='color: {plantprobabilitylib.GENE_COLORS[index]};'>"
			text += plantprobabilitylib.locus_text(copies, gene) + "</span></th>"
			text += f"<td style='{style}'>{descriptions[copies]}</td></tr>"
		text += "</table></div> "
	text += "</div>"
	return text


#=====================
def parent_table(model: tuple, first: tuple, second: tuple) -> str:
	style = plantprobabilitylib.CELL_STYLE
	text = plantprobabilitylib.table_start("Parent cross")
	text += f"<tr><th scope='col' style='{style}'>Plant</th>"
	text += f"<th scope='col' style='{style}'>Petal color</th>"
	text += f"<th scope='col' style='{style}'>Markings</th></tr>"
	for number, genotype in enumerate((first, second), 1):
		text += f"<tr><th scope='row' style='{style}'>Parent {number}</th>"
		text += f"<td style='{style}'>{PETALS[model[0]][genotype[0]]}</td>"
		text += f"<td style='{style}'>{MARKINGS[model[1]][genotype[1]]}</td></tr>"
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
		colors = " <strong>OR</strong> ".join(
			PETALS[model[0]][genotype[0]] for genotype in targets)
		text = f"<p>Petal color: {colors}<br/>"
		text += f"Markings: {MARKINGS[model[1]][targets[0][1]]}</p>"
		text += "<p>What fraction of the offspring will have this combination?</p>"
		return text
	else:
		text = f"<p>Petal color: {PETALS[model[0]][targets[0][0]]}<br/>"
		text += f"Markings: {MARKINGS[model[1]][targets[0][1]]}</p>"
		text += "<p>What fraction of the offspring will have this combination?</p>"
		return text
	text = f"<p>What fraction of the offspring will have {outcome}?</p>"
	return text


#=====================
def answer_terms(first: tuple, second: tuple, targets: tuple) -> tuple:
	a_counts = plantprobabilitylib.locus_counts(first[0], second[0])
	b_counts = plantprobabilitylib.locus_counts(first[1], second[1])
	terms = tuple((fractions.Fraction(a_counts[a], 4), fractions.Fraction(b_counts[b], 4))
		for a, b in targets)
	return terms


#=====================
def distractor_terms(first: tuple, second: tuple, targets: tuple) -> list:
	"""Recompute the requested event under named mistakes, not arbitrary fractions."""
	counts = [plantprobabilitylib.locus_counts(a, b) for a, b in zip(first, second)]
	correct = answer_terms(first, second, targets)
	errors = []
	for locus, gene in enumerate(("A", "B")):
		for mistake in ("ignore_gene", "miss_heterozygote_route", "equal_genotypes",
				"complete_dominance", "assume_heterozygous_parents", "wrong_genotype_row",
				"other_homozygote_row"):
			terms = []
			for genotype, pair in zip(targets, correct):
				copies = genotype[locus]
				count = counts[locus][copies]
				if mistake == "ignore_gene":
					# Error: assume every offspring has the requested trait at this gene.
					factor = fractions.Fraction(1)
				elif mistake == "miss_heterozygote_route":
					# Error: count only one parental route to a heterozygote.
					misses_route = copies == 1 and first[locus] == second[locus] == 1
					factor = fractions.Fraction(count, 8 if misses_route else 4)
				elif mistake == "equal_genotypes":
					# Error: count distinct genotypes rather than equally likely gamete pairs.
					factor = fractions.Fraction(1, len(counts[locus]))
				elif mistake == "complete_dominance":
					# Error: merge the heterozygote and allele-1 homozygote phenotypes.
					count = sum(n for g, n in counts[locus].items() if (g > 0) == (copies > 0))
					factor = fractions.Fraction(count, 4)
				elif mistake == "assume_heterozygous_parents":
					# Error: use a memorized heterozygote x heterozygote cross at this gene.
					factor = fractions.Fraction(2 if copies == 1 else 1, 4)
				elif mistake == "wrong_genotype_row":
					# Error: use a heterozygote row for a homozygote, or the reverse.
					wrong_row = 2 if copies == 1 else 1
					count = sum(n for g, n in counts[locus].items() if g == wrong_row)
					factor = fractions.Fraction(count, 4)
				else:
					# Error: choose the other homozygote row, including the other side of a blend.
					wrong_row = 0 if copies == 1 else 2 - copies
					count = sum(n for g, n in counts[locus].items() if g == wrong_row)
					factor = fractions.Fraction(count, 4)
				changed = list(pair)
				changed[locus] = factor
				terms.append(tuple(changed))
			errors.append((f"{mistake}_{gene}", tuple(terms)))
	# Error: count just one gamete route to each two-gene genotype.
	missed_routes = tuple((a / 2 if g[0] == first[0] == second[0] == 1 else a,
		b / 2 if g[1] == first[1] == second[1] == 1 else b)
		for g, (a, b) in zip(targets, correct))
	errors.append(("miss_heterozygote_routes_both_genes", missed_routes))
	# Error: replace the actual cross with a memorized double-heterozygote cross.
	terms = answer_terms((1, 1), (1, 1), targets)
	errors.append(("assume_double_heterozygous_parents", terms))
	return errors


#=====================
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	model, first, second, kind, targets = SCENARIOS[N - 1]
	text = phenotype_tables(model)
	text += "<p>In mosaic plants, genes <i>A</i> and <i>B</i> assort "
	text += "independently. The parents below are crossed.</p>"
	text += parent_table(model, first, second)
	text += request_text(model, kind, targets)
	choices, answer = plantprobabilitylib.make_choices(answer_terms(first, second, targets),
		distractor_terms(first, second, targets))
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
