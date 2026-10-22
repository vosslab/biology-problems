#!/usr/bin/env python3
"""Six-face dice practice with one chi-square skill per question.

The Bozeman video uses 36 rolls: 2, 4, 8, 9, 3, 10. The exact statistic is
58/6, not its spoken 9.6. Questions use the lecture's 0.05 cutoff and distinguish
a hypothesis from a conclusion. No decision proves that a die is fair.
"""

import fractions
import random

import bptools
import chisquarelib


FORMATS = {"expected": "MC", "df": "MC", "calculate": "MC",
	"interpret": "MC"}


def dice_data(expected: int, deviations: list) -> dict:
	"""Compute all displayed quantities from the same six observed counts."""
	observed = [expected + difference for difference in deviations]
	if len(observed) != 6 or sum(deviations) != 0 or min(observed) < 0 or expected < 5:
		raise ValueError("Dice data require six counts, a fixed total, and expected counts >= 5.")
	terms = [fractions.Fraction((value - expected) ** 2, expected) for value in observed]
	statistic = sum(terms)
	critical = chisquarelib.get_critical_value(0.05, 5)
	data = {"total": 6 * expected, "expected": expected, "observed": observed,
		"terms": terms, "statistic": statistic, "critical": critical,
		"reject": float(statistic) > critical}
	return data


def random_data() -> dict:
	expected = random.choice((5, 6, 8, 10, 12, 15, 20))
	# Low, moderate (video), and high deviations cover both sides of the cutoff.
	deviations = random.choice(([-1, 0, 1, -2, 0, 2], [-4, -2, 2, 3, -3, 4],
		[-expected, 0, 0, 0, 0, expected]))
	deviations = random.sample(deviations, len(deviations))
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


def get_question_text(data: dict, show_expected: bool = True, show_calculation: bool = False) -> str:
	headers = ["Face", "Observed"]
	if show_expected:
		headers.append("Expected")
	labels = [die_face(index) for index in range(1, 7)]
	if show_calculation:
		text = chisquarelib.create_worked_table(labels, data["observed"], [data["expected"]] * 6)
	else:
		rows = []
		for label, value in zip(labels, data["observed"]):
			row = [label, value]
			if show_expected:
				row.append(data["expected"])
			rows.append(row)
		text = chisquarelib.render_table(headers, rows)
	text += f'<p>You roll a six-sided die {data["total"]} times. '
	text += 'The null hypothesis is that each face has probability 1/6 on every roll.</p>'
	return text


def arithmetic_question(N: int, text: str, options: list):
	"""Show evaluated arithmetic so MC questions assess the setup, not mental math.

	The first option is correct. Remove numerically equivalent distractors before
	sorting by the supplied result, so rounding never produces two correct choices.
	"""
	choices_by_value = {}
	for expression, value in options:
		expression = expression.replace(" / ", "/").replace(" + ", "+").replace(" &minus; ", "&minus;")
		result = f"{float(value):.2f}".rstrip("0").rstrip(".")
		if result not in choices_by_value:
			relation = "=" if fractions.Fraction(result) == value else "&asymp;"
			choices_by_value[result] = (f"<span style='font-size:85%;'>{expression} {relation}</span> "
				f"<strong>{result}</strong>")
	answer_value = f"{float(options[0][1]):.2f}".rstrip("0").rstrip(".")
	answer = choices_by_value[answer_value]
	choices = [choices_by_value[value] for value in sorted(choices_by_value, key=float)]
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def expected_question(N: int, data: dict):
	text = get_question_text(data, show_expected=False)
	face = random.randint(1, 6)
	text += f"<p>Which calculation gives the expected number of rolls showing face {face} "
	text += "under the null hypothesis? The arithmetic is shown; no calculator is needed.</p>"
	total = data["total"]
	# Errors: divide by df, assume two outcomes, use the total, or use face count.
	options = [(f"{total} / 6", fractions.Fraction(total, 6)),
		(f"{total} / 5", fractions.Fraction(total, 5)),
		(f"{total} / 2", fractions.Fraction(total, 2)),
		(f"{total} / 1", total), ("6 / 1", 6)]
	item = arithmetic_question(N, text, options)
	return item


def df_question(N: int, data: dict):
	text = get_question_text(data)
	text += "<p>Which calculation gives the degrees of freedom for this chi-square test? "
	text += "The arithmetic is shown; no calculator is needed.</p>"
	# Errors: subtract twice, count every face, or count rolls instead of categories.
	options = [("6 &minus; 1", 5), ("6 &minus; 2", 4), ("6 &minus; 0", 6),
		(f"{data['total']} &minus; 1", data["total"] - 1)]
	item = arithmetic_question(N, text, options)
	return item


def calculation_question(N: int, data: dict):
	index = random.choice([i for i, value in enumerate(data["observed"])
		if value != data["expected"]])
	observed = data["observed"][index]
	expected = data["expected"]
	difference = observed - expected
	text = get_question_text(data)
	text += "<p>Each face contributes (observed &minus; expected)<sup>2</sup> / expected "
	text += "to &chi;<sup>2</sup>. The arithmetic is shown in each choice; "
	text += "no calculator is needed.</p>"
	if random.choice((True, False)):
		text += f"<p>Which calculation gives the contribution from face {index + 1}?</p>"
		base = f"({observed} &minus; {expected})"
		# Errors: omit the square, omit division, or divide by faces instead of expected.
		options = [(f"{base}<sup>2</sup> / {expected}", data["terms"][index]),
			(f"{base} / {expected}", fractions.Fraction(difference, expected)),
			(f"{base}<sup>2</sup>", difference ** 2),
			(f"{base}<sup>2</sup> / 6", fractions.Fraction(difference ** 2, 6))]
		# Error: divide by observed count; omit when that denominator is zero.
		if observed:
			options.append((f"{base}<sup>2</sup> / {observed}",
				fractions.Fraction(difference ** 2, observed)))
	else:
		# Use the displayed numbers throughout, including the wrong calculations.
		part = fractions.Fraction(f"{float(data['terms'][index]):.2f}")
		others = fractions.Fraction(f"{float(data['statistic'] - data['terms'][index]):.2f}")
		a, b = f"{float(part):.2f}", f"{float(others):.2f}"
		text += f'<p>The contribution from face {index + 1} is {a}. '
		text += f"The other faces contribute {b} in total. "
		text += "Which calculation combines them to give &chi;<sup>2</sup>?</p>"
		# Errors: omit a term, subtract instead of add, or average the contributions.
		high, low = max(part, others), min(part, others)
		options = [(f"{a} + {b}", part + others), (f"{b} + 0", others),
			(f"{float(high):.2f} &minus; {float(low):.2f}", high - low),
			(f"({a} + {b}) / 6", (part + others) / 6)]
	item = arithmetic_question(N, text, options)
	return item



def result_text(data: dict) -> str:
	text = get_question_text(data, show_calculation=True)
	text += "<p>Subtract expected from observed, square the difference, and divide by expected. "
	text += "Add the six contributions to get &chi;<sup>2</sup>. "
	text += "The total uses unrounded contributions.</p>"
	text += chisquarelib.make_chi_square_table(degrees_of_freedom=(4, 5, 6), p_values=(0.05,))
	text += f'<p>Calculated &chi;<sup>2</sup> = {float(data["statistic"]):.2f}.</p>'
	return text


def interpretation_question(N: int, data: dict):
	text = result_text(data)
	text += "<p>Which one of the following conclusions is supported at &alpha; = 0.05?</p>"
	reject = "Reject the null hypothesis; there is enough evidence that face probabilities differ from 1/6."
	keep = "Fail to reject the null hypothesis; there is not enough evidence that face probabilities differ from 1/6."
	# Errors: reverse the decision; claim proof of equal chances; demand exact counts.
	choices = [reject, keep,
		"The null hypothesis is proven; every face has exactly the same chance on each roll.",
		"The null hypothesis is disproven; a fair die must give exactly equal counts of all faces."]
	answer = reject if data["reject"] else keep
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def write_question(N: int, args):
	data = random_data()
	writers = {"expected": expected_question, "df": df_question,
		"calculate": calculation_question, "interpret": interpretation_question}
	item = writers[args.kind](N, data)
	return item


def parse_arguments():
	parser = bptools.make_arg_parser(description="Dice chi-square practice with small calculations.")
	parser.add_argument("-k", "--kind", choices=tuple(FORMATS), default="expected",
		help="Skill to practice; each kind has a fixed quiz format.")
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(args.kind, FORMATS[args.kind])
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
