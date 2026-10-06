#!/usr/bin/env python3
"""Bonus: condition on an offspring's brightness, then predict a second cross."""

# Standard Library
import random
import argparse
import fractions
import itertools

# Local modules
import bptools
import plantprobabilitylib

BRIGHTNESS = ("no glow", "low brightness", "medium brightness", "high brightness",
	"very high brightness")
BACKGROUNDS = ("#303030", "#665078", "#9a79b5", "#d5bfe6", "#f7ecff")
FOREGROUNDS = ("#ffffff", "#ffffff", "#171717", "#202020", "#202020")
SCENARIOS: list[tuple] = []


#=====================
def selected_distribution(first: tuple, second: tuple, brightness: int) -> dict:
	distribution = plantprobabilitylib.cross_distribution(first, second)
	selected = {genotype: probability for genotype, probability in distribution.items()
		if sum(genotype) == brightness}
	total = sum(selected.values(), fractions.Fraction())
	conditional = {genotype: probability / total for genotype, probability in selected.items()}
	return conditional


#=====================
def target_probability(parent: tuple, mate: tuple, brightness: int) -> fractions.Fraction:
	distribution = plantprobabilitylib.cross_distribution(parent, mate)
	probability = sum((p for genotype, p in distribution.items() if sum(genotype) == brightness),
		fractions.Fraction())
	return probability


#=====================
def build_scenarios() -> list[tuple]:
	scenarios = []
	seen = set()
	# Precompute the small cross space instead of repeating it for every selected group.
	probabilities = {(parent, mate, target): target_probability(parent, mate, target)
		for parent in plantprobabilitylib.GENOTYPES for mate in plantprobabilitylib.GENOTYPES
		for target in range(5)}
	for first, second in itertools.combinations_with_replacement(
			plantprobabilitylib.GENOTYPES, 2):
		for selected in range(1, 4):
			conditional = selected_distribution(first, second, selected)
			if len(conditional) < 2:
				continue
			for mate in plantprobabilitylib.GENOTYPES:
				for target in range(5):
					outcomes = {g: probabilities[g, mate, target] for g in conditional}
					# The unknown genotype must change the answer to the second cross.
					if len(set(outcomes.values())) < 2:
						continue
					answer = sum(conditional[g] * outcomes[g] for g in conditional)
					if not 0 < answer < 1:
						continue
					key = (first, second, selected, mate, target)
					swapped_parents = sorted((first[::-1], second[::-1]))
					swapped = (*swapped_parents, selected, mate[::-1], target)
					canonical = min(key, swapped)
					if canonical in seen:
						continue
					seen.add(canonical)
					scenarios.append(canonical)
	return scenarios


#=====================
def brightness_table() -> str:
	style = plantprobabilitylib.CELL_STYLE
	text = plantprobabilitylib.table_start("Flower brightness")
	text += f"<tr><th scope='col' style='{style}'><i>A</i> / <i>B</i></th>"
	for b in (2, 1, 0):
		text += f"<th scope='col' style='{style} color: #245b88;'>"
		text += plantprobabilitylib.locus_text(b, "B") + "</th>"
	text += "</tr>"
	for a in (2, 1, 0):
		text += f"<tr><th scope='row' style='{style} color: #753b71;'>"
		text += plantprobabilitylib.locus_text(a, "A") + "</th>"
		for b in (2, 1, 0):
			text += f"<td style='{style} background-color: {BACKGROUNDS[a + b]}; "
			text += f"color: {FOREGROUNDS[a + b]};'>"
			text += BRIGHTNESS[a + b].removesuffix(" brightness") + "</td>"
		text += "</tr>"
	text += "</table>"
	return text


#=====================
def answer_terms(first: tuple, second: tuple, selected: int, mate: tuple, target: int) -> tuple:
	conditional = selected_distribution(first, second, selected)
	# Omit zero routes from the displayed sum, but retain all routes in conditioning.
	terms = tuple((weight, target_probability(genotype, mate, target))
		for genotype, weight in sorted(conditional.items())
		if target_probability(genotype, mate, target) > 0)
	return terms


#=====================
def distractor_terms(first: tuple, second: tuple, selected: int, mate: tuple, target: int) -> list:
	conditional = selected_distribution(first, second, selected)
	original = plantprobabilitylib.cross_distribution(first, second)
	contributing = [g for g in sorted(conditional) if target_probability(g, mate, target) > 0]
	errors = []
	# Error: use the original cross frequencies without conditioning on the selected phenotype.
	terms = tuple((original[g], target_probability(g, mate, target)) for g in contributing)
	errors.append(("ignore_phenotype_selection", terms))
	# Error: assume compatible genotypes have equal frequencies.
	terms = tuple((fractions.Fraction(1, len(conditional)), target_probability(g, mate, target))
		for g in contributing)
	errors.append(("equal_compatible_genotypes", terms))
	# Error: assume one compatible genotype is certain, retaining the same displayed routes.
	for assumed in conditional:
		terms = tuple((fractions.Fraction(g == assumed), target_probability(g, mate, target))
			for g in contributing)
		errors.append((f"assume_genotype_{assumed}", terms))
	for locus, gene in enumerate(("A", "B")):
		terms = []
		for parent in contributing:
			outcomes = plantprobabilitylib.cross_distribution(parent, mate)
			# Error: count only one parental route to a heterozygote in the second cross.
			probability = sum((p / 2 if g[locus] == parent[locus] == mate[locus] == 1 else p)
				for g, p in outcomes.items() if sum(g) == target)
			terms.append((conditional[parent], probability))
		errors.append((f"miss_heterozygote_route_{gene}", tuple(terms)))
	# Error: condition only on genotypes that can produce the requested second-cross result.
	weight = sum(conditional[g] for g in contributing)
	terms = tuple((conditional[g] / weight, target_probability(g, mate, target))
		for g in contributing)
	errors.append(("exclude_nonproducing_selected_genotypes", terms))
	return errors


#=====================
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	first, second, selected, mate, target = SCENARIOS[N - 1]
	text = brightness_table()
	text += "<p>In lantern plants, genes <i>A</i> and <i>B</i> assort "
	text += "independently.</p>"
	text += f"<p>First cross:<br/>{plantprobabilitylib.genotype_text(first)} &times; "
	text += f"{plantprobabilitylib.genotype_text(second)}</p>"
	text += f"<p>One offspring with <strong>{BRIGHTNESS[selected]}</strong> is chosen at random.</p>"
	text += "<p>Second cross:<br/>Selected plant &times; "
	text += f"{plantprobabilitylib.genotype_text(mate)}</p>"
	text += "<p>What is the probability that an offspring from the second cross will have "
	text += f"<strong>{BRIGHTNESS[target]}</strong>?</p>"
	choices, answer = plantprobabilitylib.make_choices(
		answer_terms(first, second, selected, mate, target),
		distractor_terms(first, second, selected, mate, target))
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


#=====================
def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(description="Bonus: predict a cross after selecting a phenotype.")
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
