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
	text += 'The null hypothesis (H<sub>0</sub>) is that each face has probability 1/6 on every roll.</p>'
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
	text += "under the null hypothesis (H<sub>0</sub>)? The arithmetic is shown; no calculator is needed.</p>"
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
	"""Identify one consistently applied error in a partner's complete table."""
	choices_by_error = {
		"observed": "They divided by the observed count instead of the expected count.",
		"no_square": "They did not square the difference between observed and expected counts.",
		"square_expected": "They divided by the square of the expected count instead of the expected count.",
		"faces": "They divided by the number of faces instead of the expected count.",
	}
	errors = list(choices_by_error)
	if 0 in data["observed"]:
		errors.remove("observed")
	if data["expected"] == 6:
		errors.remove("faces")
	error = random.choice(errors)
	expected = data["expected"]
	rows = []
	terms = []
	for face, observed in enumerate(data["observed"], 1):
		difference = observed - expected
		if error == "no_square":
			numerator, denominator = difference, expected
			calculation = f"({observed} &minus; {expected}) / {expected}"
		else:
			numerator = difference ** 2
			if error == "observed":
				denominator = observed
				divisor = str(observed)
			elif error == "square_expected":
				denominator = expected ** 2
				divisor = f"{expected}<sup>2</sup>"
			else:
				denominator = 6
				divisor = "6"
			calculation = f"({observed} &minus; {expected})<sup>2</sup> / {divisor}"
		term = fractions.Fraction(numerator, denominator)
		terms.append(term)
		calculation += f" = {numerator} / {denominator}"
		rows.append([die_face(face), expected, observed, calculation, f"{float(term):.3f}"])
	text = f'<p>You roll a six-sided die {data["total"]} times. '
	text += 'The null hypothesis (H<sub>0</sub>) is that each face has probability 1/6 on every roll.</p>'
	text += '<p>Your lab partner completed the chi-square table below.</p>'
	text += chisquarelib.render_table(chisquarelib.CALCULATION_HEADERS, rows,
		"Lab partner's chi-square calculation", footer=(data["total"], sum(terms)))
	text += '<p><strong>Which mistake did your lab partner make in the calculation?</strong></p>'
	choices = list(choices_by_error.values())
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, choices_by_error[error])
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
	reject = "Reject the null hypothesis (H<sub>0</sub>); there is enough evidence that face probabilities differ from 1/6."
	keep = "Fail to reject the null hypothesis (H<sub>0</sub>); there is not enough evidence that face probabilities differ from 1/6."
	# Errors: reverse the decision; claim proof of equal chances; demand exact counts.
	choices = [reject, keep,
		"The null hypothesis (H<sub>0</sub>) is proven; every face has exactly the same chance on each roll.",
		"The null hypothesis (H<sub>0</sub>) is disproven; a fair die must give exactly equal counts of all faces."]
	answer = reject if data["reject"] else keep
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def write_question(N: int, args):
	data = random_data()
	# Keep every row informative when students inspect a calculation error.
	if args.kind == "calculate":
		while data["expected"] in data["observed"]:
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
