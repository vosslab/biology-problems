#!/usr/bin/env python3
"""Generate Joe's babies versus national average one-sample t-test questions."""

# Authoring contract: one numeric BBQ answer (the p-value) from a one-sample t-test.
# Random samples vary per question; --seed reproduces a complete bank for review.
# The bptools parser supplies anti-cheat flags, applied before question collection.
# Example: weights above 7.5 lb give a positive t statistic; a two-tailed p-value
# uses both tails, while the one-tailed answer uses the greater-than tail.

import math
import random
import statistics

import scipy.stats

import bptools


NATIONAL_MEAN_LB = 7.5
TUTORIAL_URL = (
	"https://docs.google.com/document/d/1lh3EWl4gnyT0dq0rgYzjzC6J1No4zKP2gi5eY3N5uv0/edit"
)


def generate_weights(n: int) -> list[float]:
	"""Draw realistic one-decimal birth weights for Joe's hospital."""
	target_mean = NATIONAL_MEAN_LB + random.uniform(0.2, 0.9)
	weights = []
	for _ in range(n):
		weight = random.gauss(target_mean, 1.3)
		weight = min(12.0, max(4.0, weight))
		weights.append(round(weight, 1))
	return weights


def one_sample_t_pvalue(weights: list[float], tails: int) -> tuple[float, float]:
	"""Return t and the greater-than or two-tailed p-value using sample SD."""
	sample_mean = statistics.fmean(weights)
	sample_sd = statistics.stdev(weights)
	t_stat = (sample_mean - NATIONAL_MEAN_LB) / (sample_sd / math.sqrt(len(weights)))
	degrees_of_freedom = len(weights) - 1
	if tails == 1:
		p_value = scipy.stats.t.sf(t_stat, degrees_of_freedom)
	else:
		p_value = 2 * scipy.stats.t.sf(abs(t_stat), degrees_of_freedom)
	return t_stat, p_value


def format_question_html(weights: list[float], tails: int) -> str:
	"""Present setup, data, procedure, and the result students must report."""
	rows = "<br/>".join(f"{weight:.1f}" for weight in weights)
	if tails == 1:
		direction = "greater than"
		hypothesis = "&gt;"
		test_description = "one-tailed"
		sheet_function = "T.DIST.RT"
		answer_cell = "E13"
	else:
		direction = "different from"
		hypothesis = "&ne;"
		test_description = "two-tailed"
		sheet_function = "T.DIST.2T"
		answer_cell = "E12"

	question = "<p><b>One-Sample t-Test: Joe's Hospital vs. National Average</b></p>"
	question += "<p><b>Setup</b></p>"
	question += (
		"<p>Joe wants to know whether the mean birth weight at Joe's Hospital of "
		f"Fried Foods is {direction} the national average of 7.5 lb. The population "
		"standard deviation is unknown, so use a one-sample t-test with the sample "
		"standard deviation.</p>"
	)
	question += f"<p>H<sub>1</sub>: &mu;<sub>Joe</sub> {hypothesis} 7.5 lb</p>"
	question += "<p><b>Sample data</b></p>"
	question += (
		f"<p>The sample contains {len(weights)} newborn birth weights (lb):</p>"
		"<p><span style='font-family:monospace; background-color:#eee; "
		f"white-space:pre;'>{rows}</span></p>"
	)
	question += "<p><b>Procedure</b></p>"
	question += (
		"<p>In the 'Part 2: National T-Test' sheet from the "
		f"<a href='{TUTORIAL_URL}' target='_blank' rel='noopener'>one-sample t-test "
		"tutorial</a>, clear the old weights in column B and "
		f"paste these {len(weights)} values starting at B2. Complete the tutorial. "
		f"For this {test_description} test, use {sheet_function}.</p>"
	)
	question += "<p><b>Result to report</b></p>"
	question += (
		f"<p>Enter the p-value shown in cell {answer_cell} as a decimal between 0 and 1 "
		"(for example, 0.084).</p>"
	)
	return question


def write_question(N: int, args):
	"""Create one Blackboard numeric question with a positive sample t statistic."""
	n = random.randint(18, 29)
	for _ in range(200):
		weights = generate_weights(n)
		if statistics.fmean(weights) <= NATIONAL_MEAN_LB:
			continue
		if statistics.stdev(weights) == 0:
			continue
		_, p_value = one_sample_t_pvalue(weights, args.tails)
		if 0.005 < p_value < 0.95:
			break
	else:
		raise RuntimeError("Could not generate a suitable one-sample t-test question")

	question_text = format_question_html(weights, args.tails)
	tolerance = round(max(0.001, 0.01 * p_value), 4)
	question = bptools.formatBB_NUM_Question(
		N, question_text, p_value, tolerance, tol_message=False
	)
	return question


def parse_arguments():
	"""Accept bank size, test direction, optional seed, and bptools options."""
	parser = bptools.make_arg_parser(description="Generate one-sample baby weight t-tests.")
	parser.add_argument(
		"-q", "--tails", type=int, choices=(1, 2), default=1,
		help="1 for greater-than (default), 2 for two-tailed",
	)
	parser.add_argument("-s", "--seed", type=int, help="Reproduce a question bank")
	args = parser.parse_args()
	return args


def main():
	"""Generate a one-sample t-test bank in Blackboard text format."""
	args = parse_arguments()
	if args.seed is not None:
		random.seed(args.seed)
	bptools.apply_anticheat_args(args)
	outfile = bptools.make_outfile(f"tails{args.tails}")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
