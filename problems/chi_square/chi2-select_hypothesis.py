#!/usr/bin/env python3
"""Identify one chi-square hypothesis from a cross and observed offspring.

Apply the predicted ratio to all four retained cross types. Distractors use
the opposite hypothesis, the observed ratio, exact counts, or another cross's
ratio. Imitate the data-first and statement-swap question exemplars.
"""

import math
import random
import argparse

import bptools
import chisquarelib


SCENARIOS = [
	{
		"id": "monohybrid_31",
		"title": "Monohybrid cross (3:1)",
		"ratio": "3:1",
		"wrong_ratio": "1:1",
		"labels": ["Dominant phenotype (A&ndash;)", "Recessive phenotype (aa)"],
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
		"labels": ["Red flowers (RR)", "Pink flowers (Rr)", "White flowers (rr)"],
		"context": (
			"<p>In a plant species with incomplete dominance, you cross two <span style='color: #ad246f; background-color: #ffffff;'>pink</span> "
			"individuals (Rr &times; Rr) and score flower color.</p>"
		),
	},
	{
		"id": "dihybrid_9311",
		"title": "Dihybrid cross (9:3:3:1)",
		"ratio": "9:3:3:1",
		"wrong_ratio": "1:1:1:1",
		"labels": ["A&ndash;B&ndash;", "A&ndash;bb", "aaB&ndash;", "aabb"],
		"context": (
			"<p>You perform a dihybrid cross (AaBb &times; AaBb) and count the F<sub>2</sub> "
			"offspring phenotypes. Assume independent assortment and complete dominance.</p>"
		),
	},
	{
		"id": "testcross_1111",
		"title": "Dihybrid testcross (1:1:1:1)",
		"ratio": "1:1:1:1",
		"wrong_ratio": "9:3:3:1",
		"labels": ["A&ndash;B&ndash;", "A&ndash;bb", "aaB&ndash;", "aabb"],
		"context": (
			"<p>You perform a dihybrid testcross (AaBb &times; aabb) and count the "
			"offspring phenotypes. Assume independent assortment and complete dominance.</p>"
		),
	},
]


#===========================
def _make_single_statement_choices(scenario: dict, kind: str,
		observed: list, expected: list, num_choices: int) -> tuple:
	if kind not in ("null", "alt"):
		raise ValueError(f"Unknown kind: {kind}")

	ratio = scenario["ratio"]
	divisor = math.gcd(*observed)
	observed_ratio = ":".join(str(count // divisor) for count in observed)
	# Apply the same wording to correct and wrong ratios, so chance is not a key cue.
	null_frame = random.choice((
		"The offspring proportions follow {ratio}; observed differences are due to chance.",
		"The cross produces a {ratio} ratio, allowing for differences due to chance.",
	))
	alt_frame = random.choice((
		"The offspring proportions differ from {ratio}.",
		"The cross produces an offspring ratio different from {ratio}.",
	))
	null = null_frame.format(ratio=ratio)
	alternative = alt_frame.format(ratio=ratio)
	counts = ":".join(str(count) for count in expected)
	if kind == "null":
		correct = null
		opposite = alternative
		pool = [
			# Error: substitute the observed ratio for the cross's prediction.
			null_frame.format(ratio=observed_ratio),
			# Error: require the particular sample to match the predicted counts exactly.
			f"The observed counts must be exactly {counts}, in the table's category order.",
			# Error: use the ratio for a different genetic model.
			null_frame.format(ratio=scenario["wrong_ratio"]),
		]
	else:
		correct = alternative
		opposite = null
		pool = [
			# Error: test against the observed ratio instead of the predicted ratio.
			alt_frame.format(ratio=observed_ratio),
			# Error: describe a sample mismatch rather than the cross's proportions.
			f"The observed counts are not exactly {counts}, in the table's category order.",
		]

	# Error: sample size changes predicted counts, not the cross's predicted ratio.
	pool.append("The cross's predicted offspring ratio changes with the sample size.")
	# Observed counts can occasionally simplify to the other model's ratio.
	pool = list(dict.fromkeys(pool))
	choices = [correct, opposite] + random.sample(pool, num_choices - 2)
	random.shuffle(choices)
	return choices, correct


#===========================
def make_question(kind: str, num_choices: int = 4) -> tuple:
	scenario = random.choice(SCENARIOS)
	ratio = scenario["ratio"]
	weights = [int(part) for part in ratio.split(":")]
	minimum, maximum = {2: (80, 160), 3: (120, 240), 4: (160, 320)}[len(weights)]
	total = random.randint(minimum // sum(weights), maximum // sum(weights)) * sum(weights)
	expected = [total * weight // sum(weights) for weight in weights]
	observed = expected
	# Exact matches would make the observed-ratio distractor another correct answer.
	while observed == expected:
		observed = chisquarelib.create_observed_progeny(N=total, ratio=ratio)
	rows = [[label, part, count]
		for label, part, count in zip(scenario["labels"], weights, observed)]
	question = chisquarelib.render_table(["Offspring phenotype", "Predicted ratio", "Observed"], rows)
	question += scenario["context"]
	hypothesis = {"null": ("null", "0", "#0247fe"), "alt": ("alternative", "a", "#b74300")}[kind]
	name, symbol, color = hypothesis
	question += f"<p>Which statement is the <span style='color: {color};'>{name} hypothesis "
	question += f"(H<sub>{symbol}</sub>)</span> for this chi-square test?</p>"
	choices, answer = _make_single_statement_choices(scenario, kind, observed, expected, num_choices)

	return question, choices, answer


#===========================
def write_question(N: int, args: argparse.Namespace) -> object:
	kind = random.choice(("null", "alt")) if args.kind == "mix" else args.kind
	question_text, choices_list, answer_text = make_question(kind, args.num_choices)
	item = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return item


#===========================
def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(description="Chi-square hypotheses (null vs alternative).")
	bptools.add_choice_args(parser, default=4)
	kind_group = parser.add_mutually_exclusive_group()
	kind_group.add_argument(
		"-k", "--kind", dest="kind", choices=("null", "alt", "mix"),
		help="Choose null, alternative, or a random equal-chance mix (default).",
	)
	kind_group.add_argument("--null", dest="kind", action="store_const", const="null",
		help="Ask only for the null hypothesis.")
	kind_group.add_argument("--alt", dest="kind", action="store_const", const="alt",
		help="Ask only for the alternative hypothesis.")
	kind_group.add_argument("--mix", dest="kind", action="store_const", const="mix",
		help="Choose the null or alternative hypothesis randomly with equal probability.")
	parser.set_defaults(kind="mix")
	args = parser.parse_args()
	if args.num_choices not in (4, 5):
		parser.error("--num-choices must be 4 or 5")
	return args


#===========================
def main() -> None:
	args = parse_arguments()
	outfile = bptools.make_outfile(args.kind)
	if args.num_choices == 5:
		outfile = bptools.make_outfile(args.kind, "5_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
