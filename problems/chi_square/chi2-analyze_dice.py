#!/usr/bin/env python3
"""Apply chi-square setup and row arithmetic to six-outcome dice tables.

Each item asks for degrees of freedom, an expected count, or one row calculation.
Distractors model category-count, data-reading, and formula errors. Select
their numeric ranks randomly, then preserve ascending answer order. Imitate
the show-the-setup exemplar with compact slanted fractions and bold results.
"""

import random
import argparse
import fractions

import bptools
import chisquarelib


FORMATS = {"expected-count": "MC", "degrees-free": "MC", "row-calc": "MC"}


def dice_data(expected: int, deviations: list) -> dict:
	"""Keep six observed counts consistent with their total and expected count."""
	observed = [expected + difference for difference in deviations]
	if len(observed) != 6 or sum(deviations) != 0 or min(observed) < 0 or expected < 5:
		raise ValueError("Dice data require six counts, a fixed total, and expected counts >= 5.")
	data = {"total": 6 * expected, "expected": expected, "observed": observed}
	return data


def random_data() -> dict:
	"""Simulate rolls with whole-number expectations under the fair-die model."""
	# Whole expected counts keep attention on the calculation rather than rounding.
	expected = random.randint(5, 30)
	weights = [1] * 6
	if random.choice((True, False)):
		weights[random.randrange(6)] = random.choice((2, 3))
	# Simulate fair or biased rolls, without prescribing the test's conclusion.
	observed = [expected] * 6
	while len(set(observed)) == 1:
		rolls = random.choices(range(6), weights=weights, k=6 * expected)
		observed = [rolls.count(face) for face in range(6)]
	deviations = [value - expected for value in observed]
	data = dice_data(expected, deviations)
	return data


def die_face(face: int) -> str:
	"""Draw a die with a small layout table; the adjacent number supplies its label."""
	pips = {
		1: (4,),
		2: (0, 8),
		3: (0, 4, 8),
		4: (0, 2, 6, 8),
		5: (0, 2, 4, 6, 8),
		6: (0, 2, 3, 5, 6, 8),
	}[face]
	text = '<table role="presentation" aria-hidden="true" style="display: inline-table; '
	text += 'vertical-align: middle; width: 40px; height: 40px; table-layout: fixed; '
	text += 'box-sizing: border-box; border: 2px solid #202020; border-radius: 5px; '
	text += 'border-collapse: separate; border-spacing: 0; padding: 2px; margin: 0; '
	text += 'color: #202020; background: #ffffff;">'
	for row in range(3):
		text += '<tr>'
		for column in range(3):
			text += '<td style="width: 10px; height: 10px; padding: 0; border: 0; '
			text += 'text-align: center; vertical-align: middle; font-size: 0; '
			text += 'line-height: 0; background: #ffffff;">'
			if row * 3 + column in pips:
				text += '<span style="display: inline-block; width: 6px; height: 6px; '
				text += 'border-radius: 50%; background: #202020;"></span>'
			text += '</td>'
		text += '</tr>'
	text += f'</table> <span style="vertical-align: middle;">{face}</span>'
	return text


def get_question_text(data: dict, show_expected: bool = True) -> str:
	headers = ["Face", "Observed"]
	if show_expected:
		headers.append("Expected")
	labels = [die_face(index) for index in range(1, 7)]
	rows = []
	for label, value in zip(labels, data["observed"]):
		row = [label, value]
		if show_expected:
			row.append(data["expected"])
		rows.append(row)
	text = chisquarelib.render_table(headers, rows)
	text += f'<p>You roll a six-sided die {data["total"]} times. '
	text += 'The <span style="color: #0247fe;">null hypothesis (H<sub>0</sub>)</span> '
	text += f'is that each face has probability {slanted_fraction("1", "6")} on every roll.</p>'
	return text


def slanted_fraction(numerator: str, denominator: str) -> str:
	"""Match the raised numerator and lowered denominator in lab-partner tables."""
	text = '<span style="display: inline-block; white-space: nowrap; line-height: 1.8;">'
	text += f'<sup style="font-size: 90%;">{numerator}</sup>'
	text += '&frasl;'
	text += f'<sub style="font-size: 90%;">{denominator}</sub></span>'
	return text


def select_options(options: list, num_choices: int) -> list:
	"""Deduplicate by displayed result and vary the key's rank among valid choices.

	The first option is correct. Choose a feasible number of smaller distractors
	randomly, rather than allowing a mostly-larger pool to fix the answer's rank.
	"""
	unique = {}
	for expression, value in options:
		result = f"{float(value):.2f}"
		if result not in unique:
			unique[result] = (expression, value)
	correct = options[0]
	lower = [option for option in unique.values() if option[1] < correct[1]]
	upper = [option for option in unique.values() if option[1] > correct[1]]
	needed = num_choices - 1
	minimum = max(0, needed - len(upper))
	maximum = min(needed, len(lower))
	if minimum > maximum:
		raise ValueError("Not enough distinct distractors for the requested choice count.")
	lower_count = random.choice(list(range(minimum, maximum + 1)))
	selected = [correct] + random.sample(lower, lower_count)
	selected += random.sample(upper, needed - lower_count)
	selected.sort(key=lambda option: option[1])
	return selected


def arithmetic_question(N: int, text: str, options: list, *,
		fixed_decimals: bool = False) -> object:
	"""Supply evaluated choices so students judge the setup without a calculator."""
	selected = select_options(options, 5)
	choices = []
	answer = ""
	for expression, value in selected:
		result = f"{float(value):.2f}"
		if not fixed_decimals:
			result = result.rstrip("0").rstrip(".")
		relation = "=" if fractions.Fraction(result) == value else "&asymp;"
		choice = f'{expression} {relation} <strong>{result}</strong>'
		choices.append(choice)
		if value == options[0][1]:
			answer = choice
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def expected_count_question(N: int, data: dict) -> object:
	text = get_question_text(data, show_expected=False)
	face = random.randint(1, 6)
	text += f"<p>Which calculation gives the expected number of rolls showing face {face} "
	text += "under the null hypothesis?</p>"
	total = data["total"]
	options = [(slanted_fraction(str(total), "6"), fractions.Fraction(total, 6))]
	# Errors: use degrees of freedom, carry over four/two categories, or count all rolls.
	for divisor in (5, 4, 2, 1):
		options.append((slanted_fraction(str(total), str(divisor)),
			fractions.Fraction(total, divisor)))
	# Error: report a probability rather than an expected count.
	options.append((slanted_fraction("1", "6"), fractions.Fraction(1, 6)))
	# Error: apply the face probability twice.
	options.append((slanted_fraction(str(total), "6<sup>2</sup>"),
		fractions.Fraction(total, 36)))
	# Error: divide the selected face's observed count instead of the total rolls.
	observed = data["observed"][face - 1]
	options.append((slanted_fraction(str(observed), "6"), fractions.Fraction(observed, 6)))
	# Error: substitute the number of faces for the number of rolls.
	options.append((slanted_fraction("6", "1"), fractions.Fraction(6)))
	item = arithmetic_question(N, text, options)
	return item


def degrees_free_question(N: int, data: dict) -> object:
	text = get_question_text(data)
	text += "<p>How many degrees of freedom does this chi-square test have?</p>"
	# Errors: carry over two/four rows, subtract twice, or forget to subtract one.
	values = [5, 2 - 1, 4 - 1, 6 - 2, 6]
	# Errors: count both data columns, or count rolls instead of categories.
	values.extend([2 * 6, data["total"] - 1])
	options = [(f"{bptools.number_to_cardinal(value)} ({value})", value) for value in values]
	selected = select_options(options, 4)
	choices = [expression for expression, value in selected]
	item = bptools.formatBB_MC_Question(N, text, choices, options[0][0])
	return item


def row_calc_options(data: dict, face: int) -> list:
	"""Build exact worked calculations from the target row and named mistakes."""
	expected = data["expected"]
	observed = data["observed"][face - 1]
	difference = observed - expected
	if observed <= 0 or abs(difference) < 2:
		raise ValueError("The target row needs a positive count differing from expected by at least two.")
	base = f"({observed} &minus; {expected})"
	squared = f"{base}<sup>2</sup>"
	# Correct setup, followed by omitting the square and using observed as divisor.
	calculations = [(squared, str(expected), difference ** 2, expected),
		(base, str(expected), difference, expected),
		(squared, str(observed), difference ** 2, observed)]
	# Errors: square expected, divide by faces, or divide by total rolls.
	calculations.extend([
		(squared, f"{expected}<sup>2</sup>", difference ** 2, expected ** 2),
		(squared, "6", difference ** 2, 6),
		(squared, str(data["total"]), difference ** 2, data["total"])])
	# Error: square the individual counts instead of their difference.
	calculations.append((f"{observed}<sup>2</sup> &minus; {expected}<sup>2</sup>",
		str(expected), observed ** 2 - expected ** 2, expected))
	# Error: read the observed count from another row of the six-outcome table.
	for other_face, other_observed in enumerate(data["observed"], 1):
		if other_face != face:
			calculations.append((f"({other_observed} &minus; {expected})<sup>2</sup>",
				str(expected), (other_observed - expected) ** 2, expected))
	options = []
	for numerator_text, denominator_text, numerator, denominator in calculations:
		expression = slanted_fraction(numerator_text, denominator_text)
		expression += " = " + slanted_fraction(str(numerator), str(denominator))
		options.append((expression, fractions.Fraction(numerator, denominator)))
	return options


def target_faces(data: dict) -> list:
	"""Exclude target rows where zero or a one-count difference collapses errors."""
	faces = [face for face, observed in enumerate(data["observed"], 1)
		if observed > 0 and abs(observed - data["expected"]) >= 2]
	return faces


def row_calc_question(N: int, data: dict) -> object:
	face = random.choice(target_faces(data))
	text = get_question_text(data)
	text += f"<p>Which calculation gives the contribution of face {face} "
	text += "to the <span style='color: #935d00;'>chi-square statistic "
	text += "(&chi;<sup>2</sup>)</span>?</p>"
	item = arithmetic_question(N, text, row_calc_options(data, face), fixed_decimals=True)
	return item


def write_question(N: int, args: argparse.Namespace) -> object:
	data = random_data()
	if args.kind == "row-calc":
		while not target_faces(data):
			data = random_data()
	writers = {"expected-count": expected_count_question, "degrees-free": degrees_free_question,
		"row-calc": row_calc_question}
	item = writers[args.kind](N, data)
	return item


def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(description="Dice chi-square practice with small calculations.")
	kind_group = parser.add_mutually_exclusive_group()
	kind_group.add_argument("-k", "--kind", dest="kind", choices=tuple(FORMATS),
		help="Skill to practice; each kind has a fixed quiz format.")
	kind_group.add_argument("-D", "--degrees-free", dest="kind", action="store_const", const="degrees-free",
		help="Generate degrees-of-freedom questions.")
	kind_group.add_argument("-E", "--expected-count", dest="kind", action="store_const", const="expected-count",
		help="Generate expected-count questions.")
	kind_group.add_argument("-R", "--row-calc", dest="kind", action="store_const", const="row-calc",
		help="Generate worked row-contribution questions.")
	parser.set_defaults(kind="expected-count")
	args = parser.parse_args()
	return args


def main() -> None:
	args = parse_arguments()
	outfile = bptools.make_outfile(args.kind, FORMATS[args.kind])
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
