#!/usr/bin/env python3
"""Offspring probability puzzles, factorials, and binomial reasoning.

Lectures 07B/07C: independence, ordered outcomes, and surviving offspring.
Exemplars: Rule, case, question; Note that hands over arithmetic.
The factorial/coefficient/binomial/explain modes follow Lecture 07B/07C:
apply factorials, count phenotype orders, set up probabilities, and explain repeated labels.
Distractors omit arrangements, swap probabilities, or count repeated labels as distinct.
No calculator is needed; choices use binomial coefficients, factorials, and powers.
"""

import fractions
import math
import random

import bptools
import binomiallib


FORMATS = {"factorial": "MC", "coefficient": "MC", "binomial": "MC", "explain": "MC"}
SCENARIOS = (
	("<p>You cross a purple-flowered pea plant (Pp) with a white-flowered plant (pp).</p>",
		"purple", "white", fractions.Fraction(1, 2)),
	("<p>You cross two (2) purple-flowered pea plants (Pp &times; Pp).</p>",
		"purple", "white", fractions.Fraction(3, 4)),
	("<p>You cross two (2) heterozygous mice (Bb &times; Bb). "
		"Black fur is dominant to brown fur.</p>", "brown", "black", fractions.Fraction(1, 4)),
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
		[(target.capitalize(), str(probability)), (other.capitalize(), str(1 - probability))])
	text += context + "<p>Offspring outcomes are independent.</p>"
	return text


def factorial_question(N: int, scenario: tuple):
	"""Apply factorial notation to distinct biological samples, not phenotype counts."""
	number = random.randint(3, 6)
	sample = random.choice(("pea seeds", "bean seedlings", "fruit-fly sample tubes", "mouse DNA samples"))
	text = (f"<p>You label {number} {sample} so that each can be identified. "
		"You place them all in a row, one in each position.</p>"
		"<p>Which expression counts the different orders of these individually labeled items? "
		"Leave your answer as an expression; no calculator is needed.</p>")
	answer = f"{number}! = " + " &times; ".join(str(i) for i in range(number, 0, -1))
	# Errors: factorial as addition, number squared, or two categories per position.
	choices = [answer, f"{number}! = " + " + ".join(str(i) for i in range(number, 0, -1)),
		f"{number}<sup>2</sup> = {number} &times; {number}",
		f"2<sup>{number}</sup> = " + " &times; ".join(["2"] * number)]
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def factorial_coefficient(number: int, count: int) -> str:
	"""Display the factorial ratio without requiring large-number arithmetic."""
	text = binomiallib.fraction(f"{number}!", f"{count}! &times; {number - count}!")
	return text


def coefficient_question(N: int, scenario: tuple):
	"""Connect binomial notation to factorial counts, including the zero-factorial case."""
	_, target, other, _ = scenario
	number = random.randint(5, 9)
	count = random.choice([0, number] + list(range(2, number - 1)))
	text = context_table(scenario)
	text += (f"<p>Consider {number} offspring: exactly {count} are {target} and "
		f"{number - count} are {other}. Count different phenotype sequences from first "
		"offspring to last, treating offspring with the same phenotype as interchangeable.</p>"
		"<p>Which factorial expression counts these sequences?</p>")
	answer = factorial_coefficient(number, count)
	# Errors: count individually labeled offspring; ignore one repeated category;
	# add the denominator factorials instead of multiplying them.
	candidates = [(binomiallib.fraction(f"{number}!", "1! &times; 1!"), math.factorial(number)),
		(binomiallib.fraction(f"{number}!", f"{count}! &times; 1!"),
			fractions.Fraction(math.factorial(number), math.factorial(count))),
		(binomiallib.fraction(f"{number}!", f"1! &times; {number - count}!"),
			fractions.Fraction(math.factorial(number), math.factorial(number - count))),
		(binomiallib.fraction(f"{number}!", f"{count}! + {number - count}!"),
			fractions.Fraction(math.factorial(number), math.factorial(count) + math.factorial(number - count))),
		(f"{count}! &times; {number - count}!", math.factorial(count) * math.factorial(number - count)),
		(f"2<sup>{number}</sup>", 2 ** number)]
	choices = [answer]
	used = {fractions.Fraction(math.comb(number, count))}
	for label, value in candidates:
		if value not in used:
			choices.append(label)
			used.add(value)
		if len(choices) == 4:
			break
	# Connect the same coefficient notation to each proposed factorial expansion.
	coefficient = binomiallib.binomial_coefficient(number, count)
	choices = [binomiallib.format_expression([coefficient, "=", label]) for label in choices]
	answer = binomiallib.format_expression([coefficient, "=", answer])
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def binomial_expression(number: int, count: int, probability: fractions.Fraction) -> str:
	"""Show arrangement count times the probability of one phenotype order."""
	text = binomiallib.binomial_probability(
		number, count, 1 - probability, probability, worked=False)
	return text


def binomial_question(N: int, scenario: tuple):
	"""Set up an exact-count probability; students need not evaluate powers."""
	_, target, other, probability = scenario
	number, count = random.choice([(5, 2), (6, 2), (7, 3), (8, 3), (9, 4)])
	text = context_table(scenario)
	surviving = " surviving" if scenario == SURVIVORS else ""
	text += (f"<p>For {number}{surviving} offspring, which expression gives the probability "
		f"of <strong>exactly {count} {target}</strong> and {number - count} {other}, "
		"in any order? Leave the answer as an expression; no calculator is needed.</p>")
	answer = binomial_expression(number, count, probability)
	one_order = binomiallib.format_expression([
		f"({probability})<sup>{count}</sup> &times; ({1 - probability})<sup>{number - count}</sup>"])
	# Errors: omit arrangements, swap phenotype probabilities, omit the other phenotype.
	choices = [answer, one_order, binomial_expression(number, count, 1 - probability),
		binomiallib.format_expression([binomiallib.binomial_coefficient(number, count),
			"&times;", f"({probability})<sup>{count}</sup>"])]
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def explanation_question(N: int, scenario: tuple):
	"""Explain why repeated phenotype labels require a factorial denominator."""
	_, target, other, _ = scenario
	number, count = random.choice([(5, 2), (6, 2), (7, 3), (8, 3)])
	text = context_table(scenario)
	text += (f"<p>To count phenotype sequences with {count} {target} and {number - count} "
		f"{other} offspring, you use the binomial coefficient:</p>")
	text += binomiallib.format_expression([binomiallib.binomial_coefficient(number, count),
		"=", factorial_coefficient(number, count)])
	text += f"<p>Why divide {number}! by {count}! &times; {number - count}!?</p>"
	answer = "Swapping offspring with the same phenotype leaves the phenotype sequence unchanged."
	choices = [answer,
		"Swapping offspring with different phenotypes leaves the phenotype sequence unchanged.",
		"The division changes the probability of each phenotype to one half.",
		"The division makes each offspring outcome depend on the preceding offspring."]
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def write_question(N: int, args):
	scenarios = SCENARIOS
	if args.kind == "binomial":
		# Unequal probabilities make swapping exponents a distinct misconception.
		scenarios = SCENARIOS[1:] + (SURVIVORS,)
	scenario = random.choice(scenarios)
	writers = {"factorial": factorial_question, "coefficient": coefficient_question,
		"binomial": binomial_question, "explain": explanation_question}
	item = writers[args.kind](N, scenario)
	return item


def parse_arguments():
	parser = bptools.make_arg_parser(description="Factorial and binomial reasoning in genetics.")
	parser.add_argument("-k", "--kind", choices=tuple(FORMATS), default="binomial",
		help="Skill to practice; each kind has a fixed quiz format.")
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(args.kind, FORMATS[args.kind])
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
