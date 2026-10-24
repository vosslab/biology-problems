#!/usr/bin/env python3

import random

import bptools


SCENARIOS = [
	{
		"id": "monohybrid_31",
		"ratio": "3:1",
		"context": (
			"<p>You cross two heterozygous individuals (Aa &times; Aa) and score the "
			"offspring phenotypes.</p>"
		),
	},
	{
		"id": "incomplete_dominance_121",
		"ratio": "1:2:1",
		"context": (
			"<p>In a plant species with incomplete dominance, you cross two <span style='color: #ad246f; background-color: #ffffff;'>pink</span> "
			"individuals (Rr &times; Rr) and score flower color.</p>"
		),
	},
	{
		"id": "dihybrid_9311",
		"ratio": "9:3:3:1",
		"context": (
			"<p>You perform a dihybrid cross (AaBb &times; AaBb) and count the F<sub>2</sub> "
			"offspring phenotypes. Assume independent assortment and complete dominance.</p>"
		),
	},
	{
		"id": "testcross_1111",
		"ratio": "1:1:1:1",
		"context": (
			"<p>You perform a dihybrid testcross (AaBb &times; aabb) and count the "
			"offspring phenotypes. Assume independent assortment and complete dominance.</p>"
		),
	},
]


#===========================
def _make_single_statement_choices(ratio: str, kind: str) -> tuple:
	if kind not in ("null", "alt"):
		raise ValueError(f"Unknown kind: {kind}")

	null = f"The cross produces offspring with an expected {ratio} ratio."
	alternative = f"The cross produces offspring with an expected ratio different from {ratio}."
	if kind == "null":
		correct = null
		choices = [
			null,
			# Error: use the alternative hypothesis.
			alternative,
			# Error: require an exact ratio in every finite sample.
			f"The cross produces offspring with an observed {ratio} ratio in every sample.",
			# Error: sample size changes expected counts, not the predicted ratio.
			"The cross produces offspring with an expected ratio that depends on sample size.",
		]
	else:
		correct = alternative
		choices = [
			alternative,
			# Error: use the null hypothesis.
			null,
			# Error: sample size changes expected counts, not the predicted ratio.
			"The cross produces offspring with an expected ratio that depends on sample size.",
			# Error: a prediction about the sample is not the general alternative.
			f"The cross produces offspring with an observed {ratio} ratio in every sample.",
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
	question = ""
	question += scenario["context"]
	if kind == "null":
		question += (
			f"<p>You will test the predicted {ratio} ratio with chi-square. "
			"Which one of the following is the <u>null hypothesis (H<sub>0</sub>)</u>?</p>"
		)
		choices, answer = _make_single_statement_choices(ratio, "null")
	elif kind == "alt":
		question += (
			f"<p>The null hypothesis (H<sub>0</sub>) predicts a {ratio} offspring ratio. "
			"Which one of the following is the <u>alternative hypothesis (H<sub>a</sub>)</u> "
			"for this chi-square test?</p>"
		)
		choices, answer = _make_single_statement_choices(ratio, "alt")
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
		"-k", "--kind", dest="kind", type=str, choices=("null", "alt"),
		help="Question kind: (null) H0 only, (alt) HA only.",
		default="null",
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
	outfile = bptools.make_outfile(args.kind)
	if args.scenario is not None:
		outfile = bptools.make_outfile(args.kind, args.scenario)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
