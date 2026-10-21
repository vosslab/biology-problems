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
	"interpret": "MC", "conclusions": "MA", "connect": "MATCH"}


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


def data_table(headers: list, rows: list) -> str:
	style = "padding: 4px 8px; border-bottom: 1px solid #b8b8b8; text-align: right;"
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


def get_question_text(data: dict, show_expected: bool = True) -> str:
	headers = ["Face", "Observed"]
	if show_expected:
		headers.append("Expected")
	rows = []
	for index, value in enumerate(data["observed"], start=1):
		row = [index, value]
		if show_expected:
			row.append(data["expected"])
		rows.append(row)
	text = data_table(headers, rows)
	text += f'<p>You roll a six-sided die {data["total"]} times. '
	text += 'The null hypothesis is that each face has probability 1/6 on every roll.</p>'
	return text


def numeric_question(N: int, text: str, answer, wrong: list):
	values = sorted(set([answer] + wrong))
	choices = [f"{float(value):g}" for value in values]
	item = bptools.formatBB_MC_Question(N, text, choices, f"{float(answer):g}")
	return item


def expected_question(N: int, data: dict):
	text = get_question_text(data, show_expected=False)
	face = random.randint(1, 6)
	text += f"<p>How many rolls showing face {face} are expected under the null hypothesis?</p>"
	# Errors: divide by df, divide into two outcomes, use the total, or use the
	# number of faces as a count. Integer totals keep the intended calculation easy.
	wrong = [data["total"] / 5, data["total"] / 2, data["total"], 6]
	item = numeric_question(N, text, data["expected"], wrong)
	return item


def df_question(N: int, data: dict):
	text = get_question_text(data)
	text += "<p>How many degrees of freedom are used for this chi-square test?</p>"
	# Errors: count every face, subtract twice, or count rolls instead of categories.
	item = numeric_question(N, text, 5, [4, 6, data["total"] - 1])
	return item


def calculation_question(N: int, data: dict):
	index = random.choice([i for i, value in enumerate(data["observed"])
		if value != data["expected"]])
	observed = data["observed"][index]
	expected = data["expected"]
	difference = observed - expected
	text = get_question_text(data)
	text += "<p>Each face contributes (observed &minus; expected)<sup>2</sup> / expected "
	text += "to &chi;<sup>2</sup>.</p>"
	if random.choice((True, False)):
		text += f"<p>What is the contribution from face {index + 1}? "
		text += "Round to two decimal places.</p>"
		answer = data["terms"][index]
		# Errors: omit the square, omit division, or divide by number of faces.
		wrong = [fractions.Fraction(difference, expected), difference ** 2,
			fractions.Fraction(difference ** 2, 6)]
		# Error: divide by the observed count instead of the expected count.
		if observed:
			wrong.append(fractions.Fraction(difference ** 2, observed))
	else:
		others = data["statistic"] - data["terms"][index]
		text += f'<p>The contribution from face {index + 1} is {float(data["terms"][index]):.2f}. '
		text += f"The other faces contribute {float(others):.2f} in total. "
		text += "What is &chi;<sup>2</sup>? Round to two decimal places.</p>"
		# Sum the displayed numbers so rounding cannot contradict the supplied work.
		answer = round(float(others), 2) + round(float(data["terms"][index]), 2)
		# Errors: omit a term, subtract instead of adding, average instead of summing.
		wrong = [others, abs(others - data["terms"][index]), data["statistic"] / 6]
	values = sorted(set(round(float(value), 2) for value in [answer] + wrong))
	choices = [f"{value:.2f}" for value in values]
	item = bptools.formatBB_MC_Question(N, text, choices, f"{float(answer):.2f}")
	return item


def result_text(data: dict) -> str:
	text = get_question_text(data)
	text += data_table(["Degrees of freedom", "Critical value at &alpha; = 0.05"],
		[(4, "9.49"), (5, "11.07"), (6, "12.59")])
	text += f'<p>Calculated &chi;<sup>2</sup> = {float(data["statistic"]):.2f}.</p>'
	return text


def interpretation_question(N: int, data: dict):
	text = result_text(data)
	text += "<p>Which one of the following conclusions is supported at &alpha; = 0.05?</p>"
	reject = "Reject the null hypothesis; there is enough evidence that face probabilities differ from 1/6."
	keep = "Do not reject the null hypothesis; there is not enough evidence that face probabilities differ from 1/6."
	# Errors: reverse the decision; claim proof of equal chances; demand exact counts.
	choices = [reject, keep,
		"The null hypothesis is proven; every face has exactly the same chance on each roll.",
		"The null hypothesis is disproven; a fair die must give exactly equal counts of all faces."]
	answer = reject if data["reject"] else keep
	random.shuffle(choices)
	item = bptools.formatBB_MC_Question(N, text, choices, answer)
	return item


def conclusions_question(N: int, data: dict):
	text = result_text(data)
	text += "<p>Which statements about this test are correct? Select all that apply.</p>"
	decision = "Reject" if data["reject"] else "Do not reject"
	opposite = "Do not reject" if data["reject"] else "Reject"
	answers = [f'Each face has an expected count of {data["expected"]}.',
		"The test has five (5) degrees of freedom.",
		f"{decision} the null hypothesis at &alpha; = 0.05."]
	# Errors: divide by df instead of faces, count faces without subtracting one,
	# and reverse the comparison with the critical value.
	wrong = [f'Each face has an expected count of {data["total"] / 5:g}.',
		"The test has six (6) degrees of freedom.",
		f"{opposite} the null hypothesis at &alpha; = 0.05."]
	choices = answers + wrong
	random.shuffle(choices)
	item = bptools.formatBB_MA_Question(N, text, choices, answers)
	return item


def matching_question(N: int, data: dict):
	text = get_question_text(data, show_expected=False)
	text += "<p>Match each quantity with its value for this experiment. "
	text += "Each choice will be used exactly once.</p>"
	pairs = [("Total number of rolls", str(data["total"])),
		("Number of possible faces", "6"), ("Degrees of freedom", "5")]
	# Include expected count only when it is distinct from df and face count.
	if data["expected"] not in (5, 6):
		pairs.append(("Expected count for each face", str(data["expected"])))
	random.shuffle(pairs)
	prompts = [f'<span style="color: inherit;">{prompt}</span>' for prompt, _ in pairs]
	answers = [value for _, value in pairs]
	item = bptools.formatBB_MAT_Question(N, text, prompts, answers)
	return item


def write_question(N: int, args):
	data = random_data()
	writers = {"expected": expected_question, "df": df_question,
		"calculate": calculation_question, "interpret": interpretation_question,
		"conclusions": conclusions_question, "connect": matching_question}
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
