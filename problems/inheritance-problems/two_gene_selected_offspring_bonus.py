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
BACKGROUNDS = ("#ffffff", "#f3edf8", "#e4d6ef", "#ccb3df", "#ae89c7")
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
	text += f"<tr><th scope='col' style='{style}'>Gene <i>A</i> / Gene <i>B</i></th>"
	for b in (2, 1, 0):
		text += f"<th scope='col' style='{style} color: #245b88;'>"
		text += plantprobabilitylib.locus_text(b, "B") + "</th>"
	text += "</tr>"
	for a in (2, 1, 0):
		text += f"<tr><th scope='row' style='{style} color: #753b71;'>"
		text += plantprobabilitylib.locus_text(a, "A") + "</th>"
		for b in (2, 1, 0):
			text += f"<td style='{style} background-color: {BACKGROUNDS[a + b]};'>"
			text += BRIGHTNESS[a + b] + "</td>"
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
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	first, second, selected, mate, target = SCENARIOS[N - 1]
	text = "<p>In fictional lantern plants, two genes affect how brightly the flowers glow. "
	text += "Both genes show incomplete dominance and assort independently. "
	text += "The table shows flower brightness for each genotype.</p>"
	text += brightness_table()
	text += f"<p>Two plants, {plantprobabilitylib.genotype_text(first)} and "
	text += f"{plantprobabilitylib.genotype_text(second)}, are crossed. "
	text += f"One of their offspring with <strong>{BRIGHTNESS[selected]}</strong> "
	text += "is chosen at random. This plant is crossed with a "
	text += f"{plantprobabilitylib.genotype_text(mate)} plant.</p>"
	text += "<p>What is the probability that an offspring from the second cross will have "
	text += f"<strong>{BRIGHTNESS[target]}</strong>?</p>"
	choices, answer = plantprobabilitylib.make_choices(
		answer_terms(first, second, selected, mate, target))
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
