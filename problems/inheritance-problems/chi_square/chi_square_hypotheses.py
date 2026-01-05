#!/usr/bin/env python3

import math
import random

import bptools
import chisquarelib


SCENARIOS = [
	{
		"id": "monohybrid_31",
		"title": "Monohybrid cross (3:1)",
		"ratio": "3:1",
		"wrong_ratio": "1:1",
		"labels": [
			"Dominant phenotype (A&ndash;)",
			"Recessive phenotype (aa)",
		],
		"context": (
			"<p>You cross two heterozygous individuals (Aa &times; Aa) and score the "
			"offspring phenotypes.</p>"
		),
	},
	{
		"id": "incomplete_dominance_121",
		"title": "Incomplete dominance (1:2:1)",
		"ratio": "1:2:1",
		"wrong_ratio": "1:1:1",
		"labels": [
			"Red flowers (RR)",
			"Pink flowers (Rr)",
			"White flowers (rr)",
		],
		"context": (
			"<p>In a plant species with incomplete dominance, you cross two pink "
			"individuals (Rr &times; Rr) and score flower color.</p>"
		),
	},
	{
		"id": "dihybrid_9311",
		"title": "Dihybrid cross (9:3:3:1)",
		"ratio": "9:3:3:1",
		"wrong_ratio": "8:2:4:2",
		"labels": [
			"Yellow Round (Y&ndash;R&ndash;)",
			"Yellow Wrinkled (Y&ndash;rr)",
			"Green Round (yyR&ndash;)",
			"Green Wrinkled (yyrr)",
		],
		"context": (
			"<p>You perform a standard dihybrid cross and count the F<sub>2</sub> "
			"offspring phenotypes.</p>"
		),
	},
	{
		"id": "testcross_1111",
		"title": "Dihybrid testcross (1:1:1:1)",
		"ratio": "1:1:1:1",
		"wrong_ratio": "9:3:3:1",
		"labels": [
			"A&ndash;B&ndash;",
			"A&ndash;bb",
			"aaB&ndash;",
			"aabb",
		],
		"context": (
			"<p>You perform a dihybrid testcross (AaBb &times; aabb) and count the "
			"offspring phenotypes.</p>"
		),
	},
]


#===========================
def _parse_ratio(ratio: str) -> list:
	bins = ratio.split(":")
	return [float(b) for b in bins]


#===========================
def _make_expected_counts(N: int, ratio: str) -> list:
	weights = _parse_ratio(ratio)
	total = sum(weights)
	expected = []
	for w in weights:
		expected.append(float(N) * w / total)
	return expected


#===========================
def _lcm(a: int, b: int) -> int:
	return abs(a * b) // math.gcd(a, b)


#===========================
def _pick_total_count(ratio: str) -> int:
	num_bins = len(ratio.split(":"))
	if num_bins == 2:
		min_N, max_N = 80, 160
	elif num_bins == 3:
		min_N, max_N = 120, 240
	else:
		min_N, max_N = 160, 320

	ratio_sum = int(sum(_parse_ratio(ratio)))
	multiple = _lcm(4, ratio_sum)
	k_min = (min_N + multiple - 1) // multiple
	k_max = max_N // multiple
	if k_max < k_min:
		k_min = max(1, k_min)
		k_max = k_min + 10
	return random.randint(k_min, k_max) * multiple


#===========================
def _format_expected(value: float) -> str:
	rounded = int(round(value))
	if abs(value - rounded) < 1e-9:
		return str(rounded)
	return f"{value:.1f}"


#===========================
def _make_counts(ratio: str) -> tuple:
	N = _pick_total_count(ratio)
	observed = chisquarelib.create_observed_progeny(N=N, ratio=ratio)
	expected = _make_expected_counts(N, ratio)
	return N, observed, expected


#===========================
def _make_counts_table(labels: list, ratio: str, observed: list, expected: list) -> str:
	table = '<table style="border: 1px solid black; border-collapse: collapse;">'
	table += '<colgroup width="220"></colgroup>'
	table += '<colgroup width="80"></colgroup>'
	table += '<colgroup width="90"></colgroup>'
	table += '<colgroup width="90"></colgroup>'
	table += "<tr>"
	table += " <th align='center' colspan='4' style='background-color: silver'>Observed data</th> "
	table += "</tr>"
	table += "<tr>"
	table += " <th align='center' style='background-color: lightgray'>Category</th> "
	table += " <th align='center' style='background-color: lightgray'>Ratio</th> "
	table += " <th align='center' style='background-color: lightgray'>Expected</th> "
	table += " <th align='center' style='background-color: lightgray'>Observed</th> "
	table += "</tr>"

	ratio_bins = ratio.split(":")
	for i, label in enumerate(labels):
		table += "<tr>"
		table += f" <td>&nbsp;{label}</td>"
		table += f" <td align='center'>{ratio_bins[i]}</td>"
		table += f" <td align='center'>{_format_expected(expected[i])}</td>"
		table += f" <td align='center'>{observed[i]}</td>"
		table += "</tr>"

	table += "</table>"
	return table


#===========================
def _choice_pair(h0: str, ha: str) -> str:
	choice = ""
	choice += "<p>"
	choice += f"<b>H<sub>0</sub></b>: {h0}<br/>"
	choice += f"<b>H<sub>A</sub></b>: {ha}"
	choice += "</p>"
	return choice


#===========================
def _make_pair_choices(ratio: str, wrong_ratio: str) -> tuple:
	h0_correct = (
		f"The offspring proportions are consistent with the expected {ratio} ratio "
		"(any differences from the expected ratio are due to chance)."
	)
	ha_correct = (
		f"The offspring proportions are not consistent with the expected {ratio} ratio "
		"(the differences are too large to explain by chance alone)."
	)

	h0_swapped = (
		f"The offspring proportions are not consistent with the expected {ratio} ratio "
		"(the differences are too large to explain by chance alone)."
	)
	ha_swapped = (
		f"The offspring proportions are consistent with the expected {ratio} ratio "
		"(any differences from the expected ratio are due to chance)."
	)

	h0_exact = f"The observed counts are exactly in a {ratio} ratio."
	ha_exact = f"The observed counts are not exactly in a {ratio} ratio."

	h0_wrong_ratio = (
		f"The offspring proportions are consistent with the expected {wrong_ratio} ratio "
		"(any differences from the expected ratio are due to chance)."
	)
	ha_wrong_ratio = (
		f"The offspring proportions are not consistent with the expected {wrong_ratio} ratio "
		"(the differences are too large to explain by chance alone)."
	)

	correct = _choice_pair(h0_correct, ha_correct)
	choices = [
		correct,
		_choice_pair(h0_swapped, ha_swapped),
		_choice_pair(h0_exact, ha_exact),
		_choice_pair(h0_wrong_ratio, ha_wrong_ratio),
	]
	random.shuffle(choices)
	return choices, correct


#===========================
def _make_single_statement_choices(ratio: str, wrong_ratio: str, kind: str) -> tuple:
	if kind not in ("null", "alt"):
		raise ValueError(f"Unknown kind: {kind}")

	h0_consistent = (
		f"The offspring proportions are consistent with the expected {ratio} ratio "
		"(any differences from the expected ratio are due to chance)."
	)
	h0_not_consistent = (
		f"The offspring proportions are not consistent with the expected {ratio} ratio "
		"(the differences are too large to explain by chance alone)."
	)
	h0_exact = f"The observed counts are exactly in a {ratio} ratio."
	h0_wrong_ratio = (
		f"The offspring proportions are consistent with the expected {wrong_ratio} ratio "
		"(any differences from the expected ratio are due to chance)."
	)

	ha_not_consistent = (
		f"The offspring proportions are not consistent with the expected {ratio} ratio "
		"(the differences are too large to explain by chance alone)."
	)
	ha_consistent = (
		f"The offspring proportions are consistent with the expected {ratio} ratio "
		"(any differences from the expected ratio are due to chance)."
	)
	ha_exact = f"The observed counts are not exactly in a {ratio} ratio."
	ha_wrong_ratio = (
		f"The offspring proportions are not consistent with the expected {wrong_ratio} ratio "
		"(the differences are too large to explain by chance alone)."
	)

	if kind == "null":
		correct = f"<b>H<sub>0</sub></b>: {h0_consistent}"
		choices = [
			f"<b>H<sub>0</sub></b>: {h0_consistent}",
			f"<b>H<sub>0</sub></b>: {h0_not_consistent}",
			f"<b>H<sub>0</sub></b>: {h0_exact}",
			f"<b>H<sub>0</sub></b>: {h0_wrong_ratio}",
		]
	else:
		correct = f"<b>H<sub>A</sub></b>: {ha_not_consistent}"
		choices = [
			f"<b>H<sub>A</sub></b>: {ha_not_consistent}",
			f"<b>H<sub>A</sub></b>: {ha_consistent}",
			f"<b>H<sub>A</sub></b>: {ha_exact}",
			f"<b>H<sub>A</sub></b>: {ha_wrong_ratio}",
		]

	random.shuffle(choices)
	return choices, correct


#===========================
def make_question(kind: str, scenario_id: str = None) -> tuple:
	if scenario_id is None:
		scenario = random.choice(SCENARIOS)
	else:
		matches = [s for s in SCENARIOS if s["id"] == scenario_id]
		if len(matches) != 1:
			raise ValueError(f"Unknown scenario_id: {scenario_id}")
		scenario = matches[0]

	ratio = scenario["ratio"]
	wrong_ratio = scenario["wrong_ratio"]
	labels = scenario["labels"]
	N, observed, expected = _make_counts(ratio)

	question = ""
	question += scenario["context"]
	question += f"<p>Total offspring scored: <span style='font-family: monospace;'>{N}</span></p>"
	question += _make_counts_table(labels, ratio, observed, expected)
	question += "<hr/> "

	if kind == "pair":
		question += (
			"<p>For a chi-squared (&chi;<sup>2</sup>) goodness-of-fit test, which option correctly "
			"states the null hypothesis (H<sub>0</sub>) and the alternative hypothesis (H<sub>A</sub>)?</p>"
		)
		choices, answer = _make_pair_choices(ratio, wrong_ratio)
	elif kind == "null":
		question += (
			"<p>For a chi-squared (&chi;<sup>2</sup>) goodness-of-fit test, which statement is the "
			"<b>null hypothesis</b> (H<sub>0</sub>)?</p>"
		)
		choices, answer = _make_single_statement_choices(ratio, wrong_ratio, "null")
	elif kind == "alt":
		question += (
			"<p>For a chi-squared (&chi;<sup>2</sup>) goodness-of-fit test, which statement is the "
			"<b>alternative hypothesis</b> (H<sub>A</sub>)?</p>"
		)
		choices, answer = _make_single_statement_choices(ratio, wrong_ratio, "alt")
	else:
		raise ValueError(f"Unknown kind: {kind}")

	return question, choices, answer


#===========================
def write_question(N: int, args) -> str:
	question_text, choices_list, answer_text = make_question(args.kind, args.scenario)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


#===========================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Chi-square hypotheses (null vs alternative).")
	parser.add_argument(
		"-k", "--kind", dest="kind", type=str, choices=("pair", "null", "alt"),
		help="Question kind: (pair) choose correct H0/HA pair, (null) H0 only, (alt) HA only.",
		default="pair",
	)
	parser.add_argument(
		"-s", "--scenario", dest="scenario", type=str,
		help="Optional fixed scenario id (e.g., dihybrid_9311).",
		default=None,
	)
	args = parser.parse_args()
	return args


#===========================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None, args.kind)
	if args.scenario is not None:
		outfile = bptools.make_outfile(None, args.kind, args.scenario)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
