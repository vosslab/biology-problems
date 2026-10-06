"""Exact inheritance probabilities and presentation shared by fictional plant questions."""

# Standard Library
import sys
import random
import argparse
import fractions
import itertools
import collections

GENOTYPES = tuple(itertools.product(range(3), repeat=2))
CELL_STYLE = "border: 1px solid #737373; padding: 7px 10px; color: #202020;"
GENE_COLORS = ("#753b71", "#245b88")


#=====================
def locus_counts(first: int, second: int) -> dict:
	"""Count first-allele copies among the four equally likely gamete pairings."""
	gametes = ((0, 0), (0, 1), (1, 1))
	counts = collections.Counter(a + b for a in gametes[first] for b in gametes[second])
	return dict(counts)


#=====================
def cross_distribution(first: tuple, second: tuple) -> dict:
	a_counts = locus_counts(first[0], second[0])
	b_counts = locus_counts(first[1], second[1])
	distribution = {
		(a, b): fractions.Fraction(a_count * b_count, 16)
		for a, a_count in a_counts.items() for b, b_count in b_counts.items()
	}
	return distribution


#=====================
def locus_text(copies: int, gene: str) -> str:
	"""Use italic gene symbols and numbered subscripts without implying dominance.

	Follows Introduction to Molecular Genetics and Genomics, chapters 2 and 3:
	alleles share a gene letter; heterozygotes list the smaller subscript first.
	"""
	alleles = ((2, 2), (1, 2), (1, 1))[copies]
	text = "".join(f"<i>{gene}</i><sub>{allele}</sub>" for allele in alleles)
	text = "<span style='font-family: monospace; font-size: 1em; white-space: nowrap;'>" + text
	text += "</span>"
	return text


#=====================
def genotype_text(genotype: tuple) -> str:
	parts = []
	for index, gene in enumerate(("A", "B")):
		parts.append(f"<strong style='color: {GENE_COLORS[index]};'>"
			f"{locus_text(genotype[index], gene)}</strong>")
	text = "<span style='white-space: nowrap;'>" + " ".join(parts) + "</span>"
	return text


#=====================
def table_start(caption: str) -> str:
	text = "<table style='border-collapse: collapse; margin: 12px 0;'>"
	text += f"<caption><strong>{caption}</strong></caption>"
	return text


#=====================
def calculation_value(terms: tuple) -> fractions.Fraction:
	value = sum((left * right for left, right in terms), fractions.Fraction())
	return value


#=====================
def calculation_text(terms: tuple) -> str:
	parts = [f"({left} &times; {right})" for left, right in terms]
	text = " + ".join(parts) + f" = {calculation_value(terms)}"
	return text


#=====================
def make_choices(terms: tuple, errors: list) -> tuple:
	"""Sample named genetic errors, then sort the worked answers numerically."""
	correct = calculation_value(terms)
	wrong = {}
	for error, candidate in errors:
		value = calculation_value(candidate)
		# Equal-length setups avoid making a multi-route key the only long choice.
		if len(candidate) == len(terms) and 0 <= value <= 1 and value != correct:
			wrong.setdefault(value, []).append(candidate)
	if len(wrong) < 2:
		raise ValueError("Not enough distinct named-error distractors")
	answer = calculation_text(terms)
	values = random.sample(sorted(wrong), min(3, len(wrong)))
	selected = {value: calculation_text(random.choice(wrong[value])) for value in values}
	selected[correct] = answer
	choices = [selected[value] for value in sorted(selected)]
	return choices, answer


#=====================
def cap_questions(args: argparse.Namespace, capacity: int) -> None:
	requested = args.duplicates
	if args.max_questions is not None:
		requested = min(requested, args.max_questions)
	if requested > capacity:
		print(f"Requested {requested} questions; only {capacity} unique scenarios are available. "
			f"Writing {capacity} questions without repeats.", file=sys.stderr)
	args.max_questions = min(requested, capacity)
