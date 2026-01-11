#!/usr/bin/env python3

import random

import bptools
from box_plot_lib import has_tie, is_nondecreasing, render_boxplot_html


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


def quantile_from_cdf_left_step(rows: list, rank_k: int) -> int:
	prev_x = rows[0][0]
	for x, cum in rows:
		if cum >= rank_k:
			return prev_x
		prev_x = x
	return rows[-1][0]


def quantile_from_cdf_linear(rows: list, rank_k: int) -> float:
	prev_x = rows[0][0]
	prev_cum = 0
	for x, cum in rows:
		if rank_k <= cum:
			if cum == prev_cum:
				return x
			frac = (rank_k - prev_cum) / (cum - prev_cum)
			return prev_x + frac * (x - prev_x)
		prev_x = x
		prev_cum = cum
	return rows[-1][0]


def average_rank_value(rows: list, k1: int, k2: int, fn) -> float:
	return (fn(rows, k1) + fn(rows, k2)) / 2


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
	- Q1 is the average of ranks 10 and 11
	- median is the average of ranks 20 and 21
	- Q3 is the average of ranks 30 and 31
	"""
	N = 40

	min_v = random.randint(2, 6)
	step1 = random.randint(2, 4)
	step2 = random.randint(2, 4)
	step3 = random.randint(2, 4)
	step4 = random.randint(2, 4)

	breaks = [min_v, min_v + step1, min_v + step1 + step2, min_v + step1 + step2 + step3, min_v + step1 + step2 + step3 + step4]

	# Five bins that sum to 40, keep them chunky so quartiles fall cleanly on steps
	c1 = random.randint(6, 12)
	c2 = random.randint(6, 12)
	c3 = random.randint(6, 12)
	remaining = N - (c1 + c2 + c3)
	c4 = random.randint(2, remaining - 2)
	c5 = remaining - c4
	counts = [c1, c2, c3, c4, c5]

	rows = make_cdf_table_from_breaks(breaks, counts)

	q1 = average_rank_value(rows, 10, 11, quantile_from_cdf)
	med = average_rank_value(rows, 20, 21, quantile_from_cdf)
	q3 = average_rank_value(rows, 30, 31, quantile_from_cdf)

	summary = {"min": breaks[0], "q1": q1, "median": med, "q3": q3, "max": breaks[-1]}
	if not is_nondecreasing(summary) or not has_tie(summary):
		return generate_cdf_problem()

	return rows, summary


def get_question_text(rows: list) -> str:
	table_html = rows_to_html_table(rows)

	html = ""
	html += "A sample of N = 40 observations is summarized by the cumulative frequency table below.<br/>\n"
	html += table_html
	html += "Quartiles use Tukey hinges: for rank k, choose the smallest value whose cumulative count is at least k; for even N, average the two middle ranks in each half (Q1: k=10,11; median: k=20,21; Q3: k=30,31), and ties are allowed.<br/>\n"
	html += "Which box plot matches this cumulative frequency table?"
	return html


def make_distractors_from_summary(rows: list, correct: dict) -> list:
	out = []
	breaks = [x for x, _ in rows]
	counts = [rows[0][1]] + [rows[i][1] - rows[i - 1][1] for i in range(1, len(rows))]

	d1 = dict(correct)
	d1["q1"] = average_rank_value(rows, 10, 11, quantile_from_cdf_left_step)
	d1["median"] = average_rank_value(rows, 20, 21, quantile_from_cdf_left_step)
	d1["q3"] = average_rank_value(rows, 30, 31, quantile_from_cdf_left_step)
	if is_nondecreasing(d1):
		out.append(d1)

	d2 = dict(correct)
	freq_rows = list(zip(breaks, counts))
	d2["q1"] = average_rank_value(freq_rows, 10, 11, quantile_from_cdf)
	d2["median"] = average_rank_value(freq_rows, 20, 21, quantile_from_cdf)
	d2["q3"] = average_rank_value(freq_rows, 30, 31, quantile_from_cdf)
	if is_nondecreasing(d2):
		out.append(d2)

	d3 = dict(correct)
	d3["q1"] = average_rank_value(rows, 10, 11, quantile_from_cdf_linear)
	d3["median"] = average_rank_value(rows, 20, 21, quantile_from_cdf_linear)
	d3["q3"] = average_rank_value(rows, 30, 31, quantile_from_cdf_linear)
	if is_nondecreasing(d3):
		out.append(d3)

	d4 = dict(correct)
	d4["q1"] = average_rank_value(rows, 9, 10, quantile_from_cdf)
	d4["median"] = average_rank_value(rows, 19, 20, quantile_from_cdf)
	d4["q3"] = average_rank_value(rows, 29, 30, quantile_from_cdf)
	if is_nondecreasing(d4):
		out.append(d4)

	d5 = dict(correct)
	d5["q1"] = average_rank_value(rows, 11, 12, quantile_from_cdf)
	d5["median"] = average_rank_value(rows, 21, 22, quantile_from_cdf)
	d5["q3"] = average_rank_value(rows, 31, 32, quantile_from_cdf)
	if is_nondecreasing(d5):
		out.append(d5)

	return out


def generate_choices(rows: list, correct: dict, num_choices: int) -> (list, str):
	correct_html = render_boxplot_html(correct)

	distractors = make_distractors_from_summary(rows, correct)

	choices = [correct_html]
	for ds in distractors:
		if ds != correct:
			choices.append(render_boxplot_html(ds))

	choices = list(dict.fromkeys(choices))
	if len(choices) < num_choices:
		raise ValueError("Not enough unique distractors for this table.")

	choices = choices[:num_choices]
	random.shuffle(choices)
	return choices, correct_html


def write_question(N: int, args) -> str:
	while True:
		rows, correct = generate_cdf_problem()
		try:
			choices_list, answer_text = generate_choices(rows, correct, args.num_choices)
			break
		except ValueError:
			continue
	question_text = get_question_text(rows)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from a cumulative frequency table")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile("MC", "boxplot_from_cdf", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
