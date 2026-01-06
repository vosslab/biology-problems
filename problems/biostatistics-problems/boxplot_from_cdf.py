#!/usr/bin/env python3

import random

import bptools
import make_html_box_plot


def render_boxplot_html(summary: dict) -> str:
	axis_start = max(0, summary["min"] - 1)
	axis_end = summary["max"] + 1

	box_plot = make_html_box_plot.BoxPlot(
		axis_start=axis_start,
		whisker_start=summary["min"],
		box_start=summary["q1"],
		median=summary["median"],
		box_end=summary["q3"],
		whisker_end=summary["max"],
		axis_end=axis_end,
		mean=summary["median"],
	)

	grid = make_html_box_plot.create_grid(box_plot.axis_start, box_plot.axis_end)
	grid = make_html_box_plot.assign_elements(grid, box_plot)
	return make_html_box_plot.generate_html(grid, box_plot.axis_start, box_plot.axis_end)


def is_strict(summary: dict) -> bool:
	return summary["min"] < summary["q1"] < summary["median"] < summary["q3"] < summary["max"]


def make_cdf_table_from_breaks(breaks: list, counts: list) -> list:
	"""
	breaks: increasing x values
	counts: frequencies at each break, same length as breaks
	Returns rows of (x, cumulative_count).
	"""
	cum = 0
	rows = []
	for x, f in zip(breaks, counts):
		cum += f
		rows.append((x, cum))
	return rows


def quantile_from_cdf(rows: list, rank_k: int) -> int:
	for x, cum in rows:
		if cum >= rank_k:
			return x
	return rows[-1][0]


def rows_to_html_table(rows: list) -> str:
	html = "<table style='border-collapse: collapse; font-family: monospace;'>\n"
	html += "<tr><th style='border: 1px solid black; padding: 4px;'>Value</th>"
	html += "<th style='border: 1px solid black; padding: 4px;'>Cumulative count</th></tr>\n"
	for x, cum in rows:
		html += "<tr>"
		html += f"<td style='border: 1px solid black; padding: 4px; text-align: right;'>{x}</td>"
		html += f"<td style='border: 1px solid black; padding: 4px; text-align: right;'>{cum}</td>"
		html += "</tr>\n"
	html += "</table>\n"
	return html


def generate_cdf_problem() -> (list, dict):
	"""
	Construct a simple step CDF with N=40, then compute the implied five number summary:
	- min is first break
	- max is last break
	- Q1 is rank 10
	- median is rank 20
	- Q3 is rank 30
	"""
	N = 40

	min_v = random.randint(2, 6)
	step1 = random.randint(2, 4)
	step2 = random.randint(2, 4)
	step3 = random.randint(2, 4)
	step4 = random.randint(2, 4)

	breaks = [min_v, min_v + step1, min_v + step1 + step2, min_v + step1 + step2 + step3, min_v + step1 + step2 + step3 + step4]

	# Five bins that sum to 40, keep them chunky so quartiles fall cleanly on steps
	c1 = random.randint(6, 10)
	c2 = random.randint(6, 10)
	c3 = random.randint(6, 10)
	remaining = N - (c1 + c2 + c3)
	c4 = random.randint(4, remaining - 4)
	c5 = remaining - c4
	counts = [c1, c2, c3, c4, c5]

	rows = make_cdf_table_from_breaks(breaks, counts)

	q1 = quantile_from_cdf(rows, 10)
	med = quantile_from_cdf(rows, 20)
	q3 = quantile_from_cdf(rows, 30)

	summary = {"min": breaks[0], "q1": q1, "median": med, "q3": q3, "max": breaks[-1]}
	if not is_strict(summary):
		return generate_cdf_problem()

	return rows, summary


def get_question_text(rows: list) -> str:
	table_html = rows_to_html_table(rows)

	html = ""
	html += "A sample of N = 40 observations is summarized by the cumulative frequency table below.<br/>\n"
	html += table_html
	html += "Use the rule: for rank k, pick the smallest value whose cumulative count is at least k.<br/>\n"
	html += "Ranks: Q1 is k = 10, median is k = 20, Q3 is k = 30.<br/>\n"
	html += "Which box plot matches this cumulative frequency table?"
	return html


def make_distractors_from_summary(correct: dict) -> list:
	out = []

	# Wrong ranks (off by one bin direction)
	d1 = dict(correct)
	d1["q1"] = correct["q1"] + 1
	if is_strict(d1):
		out.append(d1)

	d2 = dict(correct)
	d2["median"] = correct["median"] + 1
	if is_strict(d2):
		out.append(d2)

	d3 = dict(correct)
	d3["q3"] = correct["q3"] - 1
	if is_strict(d3):
		out.append(d3)

	# Swap Q1 and Q3 (classic)
	d4 = dict(correct)
	d4["q1"] = correct["q3"]
	d4["q3"] = correct["q1"]
	if is_strict(d4):
		out.append(d4)

	return out


def pad_distractors(distractors: list, correct: dict, target: int) -> list:
	out = list(distractors)
	tries = 0
	while len(out) < target and tries < 60:
		tries += 1
		ds = dict(correct)
		key = random.choice(["q1", "median", "q3"])
		ds[key] = ds[key] + random.choice([-2, -1, 1, 2])
		if is_strict(ds):
			out.append(ds)
	return out[:target]


def generate_choices(correct: dict, num_choices: int) -> (list, str):
	correct_html = render_boxplot_html(correct)

	distractors = make_distractors_from_summary(correct)
	distractors = pad_distractors(distractors, correct, num_choices - 1)

	choices = [correct_html]
	for ds in distractors:
		choices.append(render_boxplot_html(ds))

	choices = list(dict.fromkeys(choices))
	while len(choices) < num_choices:
		ds = dict(correct)
		ds["q1"] = ds["q1"] - 1
		if is_strict(ds):
			choices.append(render_boxplot_html(ds))
			choices = list(dict.fromkeys(choices))

	choices = choices[:num_choices]
	random.shuffle(choices)
	return choices, correct_html


def write_question(N: int, args) -> str:
	rows, correct = generate_cdf_problem()
	question_text = get_question_text(rows)
	choices_list, answer_text = generate_choices(correct, args.num_choices)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from a cumulative frequency table")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile(__file__, "MC", "boxplot_from_cdf", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
