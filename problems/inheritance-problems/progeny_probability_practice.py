#!/usr/bin/env python3
"""Worked binomial offspring probabilities for genetic crosses."""

import fractions
import math
import random

import bptools
import binomiallib


SCENARIOS = (
	("<p>You cross two (2) <span style='color: #7030a0; background-color: #ffffff;'>purple</span>-flowered pea plants (Pp &times; Pp).</p>",
		"<span style='color: #7030a0; background-color: #ffffff;'>purple</span>", "<span style='color: #595959; background-color: #ffffff;'>white</span>", fractions.Fraction(3, 4)),
	("<p>You cross two (2) heterozygous mice (Bb &times; Bb). "
		"<span style='color: #202020; background-color: #ffffff;'>Black</span> fur is dominant to <span style='color: #804000; background-color: #ffffff;'>brown</span> fur.</p>", "<span style='color: #804000; background-color: #ffffff;'>brown</span>", "<span style='color: #202020; background-color: #ffffff;'>black</span>", fractions.Fraction(1, 4)),
)
SURVIVORS = (
	"<p>You cross two (2) short-tailed mice (Tt &times; Tt). TT offspring do not survive. "
	"Among surviving offspring, Tt mice have short tails and tt mice have long tails.</p>",
	"short-tailed", "long-tailed", fractions.Fraction(2, 3),
)


def data_table(headers: list, rows: list) -> str:
	"""Render compact data with explicit surfaces for light and dark consumers."""
	style = "padding: 4px 8px; border-bottom: 1px solid #b8b8b8; text-align: left;"
	text = '<table style="border-collapse: collapse; color: #202020; background: #ffffff;">'
	text += '<tr style="background: #e3e8ed;">'
	for header in headers:
		text += f'<th scope="col" style="{style}">{header}</th>'
	text += '</tr>'
	for index, row in enumerate(rows):
		background = "#ffffff" if index % 2 == 0 else "#f2f5f7"
		text += f'<tr style="background: {background};">'
		text += f'<th scope="row" style="{style} font-weight: normal;">{row[0]}</th>'
		for value in row[1:]:
			text += f'<td style="{style}">{value}</td>'
		text += '</tr>'
	text += '</table>'
	return text


def context_table(scenario: tuple) -> str:
	context, target, other, probability = scenario
	text = data_table(["Offspring phenotype", "Probability for one offspring"],
		[(target, str(probability)), (other, str(1 - probability))])
	text += context + "<p>Offspring outcomes are independent.</p>"
	return text


def binomial_expression(number: int, count: int, probability: fractions.Fraction) -> str:
	"""Show arrangement count times the probability of one phenotype order."""
	text = binomiallib.binomial_probability(
		number, count, 1 - probability, probability)
	return text


def binomial_question(N: int, scenario: tuple):
	"""Choose a worked exact-count probability calculation."""
	_, target, other, probability = scenario
	number, count = random.choice([(5, 2), (6, 2), (7, 3), (8, 3), (9, 4)])
	text = context_table(scenario)
	surviving = " surviving" if scenario == SURVIVORS else ""
	text += (f"<p>For {number}{surviving} offspring, which expression gives the probability "
		f"of <strong>exactly {count} {target}</strong> and {number - count} {other}, "
		"in any order?</p>")
	answer = binomial_expression(number, count, probability)
	one_order = binomiallib.format_expression([
		f"({probability})<sup>{count}</sup> &times; ({1 - probability})<sup>{number - count}</sup>",
		"=", binomiallib.probability_result(probability ** count * (1 - probability) ** (number - count))])
	# Keep plausible mistakes, but discard implausible final probabilities.
	correct_value = math.comb(number, count) * probability ** count * (1 - probability) ** (number - count)
	candidates = [
		(probability ** count * (1 - probability) ** (number - count), one_order),
		(math.comb(number, count) * (1 - probability) ** count * probability ** (number - count),
			binomial_expression(number, count, 1 - probability)),
		(math.comb(number, count) * probability ** count,
			binomiallib.format_expression([binomiallib.binomial_coefficient(number, count),
				"&times;", f"({probability})<sup>{count}</sup>", "=",
				binomiallib.probability_result(math.comb(number, count) * probability ** count)]))]
	# Confuse the total with a phenotype count, using only numbers in the stem.
	counts = sorted({number, count, number - count})
	for n in counts:
		for k in counts:
			if k > n:
				continue
			for p in (probability, 1 - probability):
				value = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
				candidates.append((value, binomial_expression(n, k, p)))
	random.shuffle(candidates)
	choices = [answer]
	percentages = {f"{float(correct_value) * 100:.1f}"}
	for value, expression in candidates:
		percentage = f"{float(value) * 100:.1f}"
		if not fractions.Fraction(1, 200) <= value <= fractions.Fraction(3, 5):
			continue
		if percentage in percentages:
			continue
		choices.append(expression)
		percentages.add(percentage)
		if len(choices) == 4:
			break
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def write_question(N: int, args):
	# Unequal probabilities make swapping exponents a distinct misconception.
	scenario = random.choice(SCENARIOS + (SURVIVORS,))
	return binomial_question(N, scenario)


def parse_arguments():
	parser = bptools.make_arg_parser(description="Binomial offspring probabilities.")
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	outfile = bptools.make_outfile("binomial", "MC")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
