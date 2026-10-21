#!/usr/bin/env python3
"""Small-family probability puzzles: outcomes before binomial notation.

Lectures 07B/07C: independence, ordered outcomes, and surviving offspring.
Exemplars: Rule, case, question; Note that hands over arithmetic.
The authoring contract is in docs/active_plans/active/GENETICS_PROBABILITY_CHI_SQUARE.md.
"""

import fractions
import itertools
import math
import random

import bptools


FORMATS = {"independence": "MC", "outcomes": "MA", "tables": "MATCH", "calculate": "MC"}
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


def count_text(number: int) -> str:
	words = ("zero", "one", "two", "three", "four")
	text = f"{words[number]} ({number})" if 2 <= number <= 4 else words[number]
	return text


def probability_label(value: fractions.Fraction) -> str:
	text = f"{value}, {float(value):.1%}"
	return text


def distribution(number: int, probability: fractions.Fraction) -> list:
	"""Exact probabilities by number of offspring with the selected phenotype."""
	values = [math.comb(number, count) * probability ** count
		* (1 - probability) ** (number - count) for count in range(number + 1)]
	return values


def context_table(scenario: tuple) -> str:
	context, target, other, probability = scenario
	text = data_table(["Offspring phenotype", "Probability for one offspring"],
		[(target.capitalize(), str(probability)), (other.capitalize(), str(1 - probability))])
	text += context + "<p>Offspring outcomes are independent.</p>"
	return text


def independence_question(N: int, scenario: tuple):
	_, target, other, probability = scenario
	previous = random.randint(2, 4)
	previous_trait = random.choice((target, other))
	text = context_table(scenario)
	text += f"<p>The first {count_text(previous)} offspring are {previous_trait}. "
	text += f"What is the probability that the <u>next</u> offspring is {target}?</p>"
	# Errors: a run guarantees repetition, a run forces a switch, or the two outcomes
	# are assumed equally likely. The fixed quarters ladder also contains complements.
	values = [fractions.Fraction(i, 4) for i in range(5)]
	choices = [probability_label(value) for value in values]
	item = bptools.formatBB_MC_Question(N, text, choices, probability_label(probability))
	return item


def outcome_question(N: int, scenario: tuple):
	_, target, other, _ = scenario
	number = random.randint(2, 4)
	condition = random.choice(("exactly", "at least"))
	count = random.randint(1, number - 1)
	sequences = list(itertools.product((target, other), repeat=number))
	correct = []
	wrong = []
	for sequence in sequences:
		matches = sequence.count(target) >= count if condition == "at least" else sequence.count(target) == count
		(correct if matches else wrong).append(sequence)
	# Wrong sequences confuse exactly/at least or count the other phenotype.
	selected = random.sample(correct, min(3, len(correct)))
	selected += random.sample(wrong, min(3, len(wrong)))
	selected.sort()
	choices = [" &rarr; ".join(sequence) for sequence in selected]
	answers = [" &rarr; ".join(sequence) for sequence in selected if sequence in correct]
	text = context_table(scenario)
	text += f"<p>Read each sequence from first to last for {count_text(number)} offspring. "
	text += f"Which sequences have <u>{condition} {count_text(count)}</u> {target} offspring? "
	text += "Select all that apply.</p>"
	item = bptools.formatBB_MA_Question(N, text, choices, answers)
	return item


def table_question(N: int, scenario: tuple):
	context, target, _, probability = scenario
	number = random.randint(2, 4)
	values = distribution(number, probability)
	rows = [(str(count), str(value)) for count, value in enumerate(values)]
	text = data_table([f"Number of {target} offspring", "Probability"], rows)
	text += context
	surviving = " surviving" if scenario == SURVIVORS else ""
	text += f"<p>The table gives probabilities for {count_text(number)}{surviving} offspring. "
	text += "Offspring outcomes are independent. Match each outcome with its probability. "
	text += "Each choice will be used exactly once.</p>"
	# Combine rows to distinguish at least, at most, and none without factorials.
	events = [(f"No {target} offspring", values[0]),
		(f"All {count_text(number)} offspring are {target}", values[-1])]
	for count in range(1, number):
		events.append((f"Exactly {count_text(count)} {target} offspring", values[count]))
		events.append((f"At least {count_text(count)} {target} offspring", sum(values[count:])))
		events.append((f"At most {count_text(count)} {target} offspring", sum(values[:count + 1])))
	random.shuffle(events)
	selected = []
	used = set()
	for event, value in events:
		if value not in used:
			selected.append((event, value))
			used.add(value)
		if len(selected) == 3:
			break
	prompts = [f'<span style="color: inherit;">{event}</span>' for event, _ in selected]
	answers = [probability_label(value) for _, value in selected]
	item = bptools.formatBB_MAT_Question(N, text, prompts, answers)
	return item


def calculation_question(N: int, scenario: tuple):
	_, target, other, probability = scenario
	number = random.randint(2, 4)
	count = random.randint(0, number - 1)
	one_order = probability ** count * (1 - probability) ** (number - count)
	answer = math.comb(number, count) * one_order
	text = context_table(scenario)
	if probability != fractions.Fraction(1, 2):
		sequence = " &rarr; ".join([target] * count + [other] * (number - count))
		text += f"<p>Note: the probability of {sequence} in that order is {one_order}. "
		text += "Every order with these same numbers of each phenotype has that probability.</p>"
	text += f"<p>For {count_text(number)} offspring, what is the probability of "
	text += f"<u>exactly {count_text(count)}</u> {target} offspring, in any order?</p>"
	wrong = [one_order, fractions.Fraction(count, number), probability]
	# Errors: omit the other phenotype; treat all sequences as equally likely;
	# count one extra arrangement. Duplicates and accidental keys are removed.
	wrong += [probability ** count, fractions.Fraction(math.comb(number, count), 2 ** number),
		(math.comb(number, count) + 1) * one_order]
	values = sorted(set([answer] + [value for value in wrong if 0 <= value <= 1]))
	choices = [probability_label(value) for value in values]
	item = bptools.formatBB_MC_Question(N, text, choices, probability_label(answer))
	return item


def write_question(N: int, args):
	scenarios = SCENARIOS + (SURVIVORS,) if args.kind == "tables" else SCENARIOS
	scenario = random.choice(scenarios)
	writers = {"independence": independence_question, "outcomes": outcome_question,
		"tables": table_question, "calculate": calculation_question}
	item = writers[args.kind](N, scenario)
	return item


def parse_arguments():
	parser = bptools.make_arg_parser(description="Accessible offspring probability quizzes.")
	parser.add_argument("-k", "--kind", choices=tuple(FORMATS), default="independence",
		help="Skill to practice; each kind has a fixed quiz format.")
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(args.kind, FORMATS[args.kind])
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
