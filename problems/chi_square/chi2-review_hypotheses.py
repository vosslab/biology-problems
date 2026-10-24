#!/usr/bin/env python3

import math
import random

import bptools
import chisquarelib


SCENARIOS = [
	{
		"id": "monohybrid_31",
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
		"ratio": "1:2:1",
		"wrong_ratio": "1:1:1",
		"labels": [
			"<span style='color: #b02020; background-color: #ffffff;'>Red</span> flowers (RR)",
			"<span style='color: #ad246f; background-color: #ffffff;'>Pink</span> flowers (Rr)",
			"<span style='color: #595959; background-color: #ffffff;'>White</span> flowers (rr)",
		],
		"context": (
			"<p>In a plant species with incomplete dominance, you cross two <span style='color: #ad246f; background-color: #ffffff;'>pink</span> "
			"individuals (Rr &times; Rr) and score flower color.</p>"
		),
	},
	{
		"id": "dihybrid_9311",
		"ratio": "9:3:3:1",
		"wrong_ratio": "8:2:4:2",
		"labels": [
			"<span style='color: #806000; background-color: #ffffff;'>Yellow</span> Round (Y&ndash;R&ndash;)",
			"<span style='color: #806000; background-color: #ffffff;'>Yellow</span> Wrinkled (Y&ndash;rr)",
			"<span style='color: #246b36; background-color: #ffffff;'>Green</span> Round (yyR&ndash;)",
			"<span style='color: #246b36; background-color: #ffffff;'>Green</span> Wrinkled (yyrr)",
		],
		"context": (
			"<p>You perform a dihybrid cross (AaBb &times; AaBb) and count the F<sub>2</sub> "
			"offspring phenotypes. Assume independent assortment and complete dominance.</p>"
		),
	},
	{
		"id": "testcross_1111",
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
			"offspring phenotypes. Assume independent assortment and complete dominance.</p>"
		),
	},
]


ERROR_CHOICES = [
	"Switch the labels on the null and alternative hypotheses.",
	"Allow observed counts to vary from the predicted ratio.",
	"Use this cross's predicted ratio as the reference in both hypotheses.",
	"Keep both hypotheses as written for this cross.",
]


#===========================
def _parse_ratio(ratio: str) -> list:
	return [float(b) for b in ratio.split(":")]


#===========================
def _lcm(a: int, b: int) -> int:
	return abs(a * b) // math.gcd(a, b)


#===========================
def _pick_total_count_for_ratio(ratio: str) -> int:
	num_bins = len(ratio.split(":"))
	min_N = 80
	max_N = 160
	if num_bins == 3:
		min_N, max_N = 120, 240
	elif num_bins >= 4:
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
def _make_expected_counts(N: int, ratio: str) -> list:
	weights = _parse_ratio(ratio)
	total = sum(weights)
	expected = []
	for w in weights:
		expected.append(float(N) * w / total)
	return expected


#===========================
def _make_counts(ratio: str) -> tuple:
	N = _pick_total_count_for_ratio(ratio)
	observed = chisquarelib.create_observed_progeny(N=N, ratio=ratio)
	expected = _make_expected_counts(N, ratio)
	return N, observed, expected


#===========================
def _make_counts_table(labels: list, ratio: str, observed: list, expected: list) -> str:
	rows = [[label, part, _format_expected(exp), obs]
		for label, part, obs, exp in zip(labels, ratio.split(":"), observed, expected)]
	table = chisquarelib.render_table(["Category", "Ratio", "Expected", "Observed"], rows)
	return table


#===========================
def _hypothesis_text(ratio: str) -> tuple:
	h0 = f"The expected offspring ratio for this cross is {ratio}."
	ha = f"The expected offspring ratio for this cross differs from {ratio}."
	return h0, ha


#===========================
def _hypothesis_exact_text(ratio: str) -> tuple:
	h0 = f"The observed counts are exactly in a {ratio} ratio."
	ha = f"The observed counts are not exactly in a {ratio} ratio."
	return h0, ha


#===========================
def _make_lab_partner_hypotheses(ratio: str, wrong_ratio: str, error_type: str) -> tuple:
	h0, ha = _hypothesis_text(ratio)
	if error_type == "swap":
		return ha, h0, 0
	if error_type == "exact":
		h0e, hae = _hypothesis_exact_text(ratio)
		return h0e, hae, 1
	if error_type == "wrong_ratio":
		h0w, haw = _hypothesis_text(wrong_ratio)
		return h0w, haw, 2
	if error_type == "correct":
		return h0, ha, 3
	raise ValueError(f"Unknown error_type: {error_type}")


#===========================
def make_question(error_type: str, scenario_id: str = None) -> tuple:
	if scenario_id is None:
		scenario = random.choice(SCENARIOS)
	else:
		matches = [s for s in SCENARIOS if s["id"] == scenario_id]
		if len(matches) != 1:
			raise ValueError(f"Unknown scenario_id: {scenario_id}")
		scenario = matches[0]

	ratio = scenario["ratio"]
	wrong_ratio = scenario["wrong_ratio"]
	N, observed, expected = _make_counts(ratio)

	lab_h0, lab_ha, answer_index = _make_lab_partner_hypotheses(ratio, wrong_ratio, error_type)

	question = ""
	question += scenario["context"]
	question += f"<p>Total offspring scored: <span style='font-family: monospace;'>{N}</span></p>"
	question += _make_counts_table(scenario["labels"], ratio, observed, expected)
	question += (
		"<p>Your lab partner writes these hypotheses for a chi-square (&chi;<sup>2</sup>) test:</p>"
	)
	question += "<p>"
	question += f"<strong>The <span style=\"color: #0247fe;\">null hypothesis (H<sub>0</sub>)</span></strong>: {lab_h0}<br/>"
	question += f"<strong>The <span style=\"color: #b74300;\">alternative hypothesis (H<sub>a</sub>)</span></strong>: {lab_ha}"
	question += "</p>"
	question += "<p>What should your lab partner change, if anything?</p>"

	choices_list = list(ERROR_CHOICES)
	answer_text = choices_list[answer_index]
	random.shuffle(choices_list)
	return question, choices_list, answer_text


#===========================
def write_question(N: int, args) -> str:
	if args.error_type == "random":
		error_type = random.choice(("swap", "exact", "wrong_ratio", "correct"))
	else:
		error_type = args.error_type
	question_text, choices_list, answer_text = make_question(error_type, args.scenario)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


#===========================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Review a lab partner's chi-square hypotheses.")
	parser.add_argument(
		"-e", "--error-type", dest="error_type", type=str,
		choices=("random", "swap", "exact", "wrong_ratio", "correct"),
		help="Force a specific error type (default: random mix).",
		default="random",
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
	outfile = bptools.make_outfile("hypotheses_partner")
	if args.error_type != "random":
		outfile = bptools.make_outfile("hypotheses_partner", args.error_type)
	if args.scenario is not None:
		outfile = bptools.make_outfile("hypotheses_partner", args.error_type, args.scenario)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
