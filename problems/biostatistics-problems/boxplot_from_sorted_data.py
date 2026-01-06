#!/usr/bin/env python3

import random

import bptools
import make_html_box_plot


def median_of_sorted_odd(sorted_values: list) -> int:
	mid = len(sorted_values) // 2
	return sorted_values[mid]


def five_number_summary_odd_exclusive_median(values: list) -> dict:
	"""
	Quartile rule (odd n):
	- Median is the middle value.
	- Q1 is the median of the lower half (excluding the overall median).
	- Q3 is the median of the upper half (excluding the overall median).
	"""
	x = sorted(values)
	n = len(x)
	if n % 2 == 0:
		raise ValueError("Expected odd n")

	med = median_of_sorted_odd(x)
	lower = x[:n // 2]
	upper = x[n // 2 + 1:]

	q1 = median_of_sorted_odd(lower)
	q3 = median_of_sorted_odd(upper)

	return {"min": x[0], "q1": q1, "median": med, "q3": q3, "max": x[-1]}


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
	html = make_html_box_plot.generate_html(grid, box_plot.axis_start, box_plot.axis_end)
	return html


def is_strict(summary: dict) -> bool:
	return summary["min"] < summary["q1"] < summary["median"] < summary["q3"] < summary["max"]


def build_sorted_dataset_11(min_v: int, q1_v: int, med_v: int, q3_v: int, max_v: int) -> list:
	"""
	Build a sorted size-11 dataset whose:
	3rd term is Q1, 6th term is median, 9th term is Q3.
	"""
	x1 = min_v
	x3 = q1_v
	x6 = med_v
	x9 = q3_v
	x11 = max_v

	x2 = random.randint(x1, x3)
	x4 = random.randint(x3, x6)
	x5 = random.randint(x3, x6)
	x7 = random.randint(x6, x9)
	x8 = random.randint(x6, x9)
	x10 = random.randint(x9, x11)

	data = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11]
	return sorted(data)


def generate_dataset_11() -> list:
	min_v = random.randint(3, 8)
	q1_v = min_v + random.randint(2, 4)
	med_v = q1_v + random.randint(2, 4)
	q3_v = med_v + random.randint(2, 4)
	max_v = q3_v + random.randint(2, 4)

	data = build_sorted_dataset_11(min_v, q1_v, med_v, q3_v, max_v)
	s = five_number_summary_odd_exclusive_median(data)

	if not is_strict(s):
		return generate_dataset_11()

	return data


def make_distractor_summaries(data_sorted: list, correct: dict) -> list:
	"""
	Common mistakes for odd n=11:
	- Wrong median index (5th instead of 6th)
	- Inclusive quartiles (use 4th and 8th as Q1/Q3)
	- Off-by-one quartile index (2nd or 10th)
	"""
	x = data_sorted
	distractors = []

	d1 = dict(correct)
	d1["median"] = x[4]
	if is_strict(d1):
		distractors.append(d1)

	d2 = dict(correct)
	d2["q1"] = x[3]
	d2["q3"] = x[7]
	if is_strict(d2):
		distractors.append(d2)

	d3 = dict(correct)
	d3["q1"] = x[1]
	if is_strict(d3):
		distractors.append(d3)

	d4 = dict(correct)
	d4["q3"] = x[9]
	if is_strict(d4):
		distractors.append(d4)

	return distractors


def pad_distractors(distractors: list, correct: dict, target: int) -> list:
	out = list(distractors)
	tries = 0
	while len(out) < target and tries < 50:
		tries += 1
		ds = dict(correct)
		key = random.choice(["q1", "median", "q3"])
		step = random.choice([-2, -1, 1, 2])
		ds[key] = ds[key] + step
		if is_strict(ds):
			out.append(ds)
	return out[:target]


def get_question_text(data_sorted: list) -> str:
	data_text = ", ".join([str(v) for v in data_sorted])
	html = ""
	html += "A sample of 11 measurements (already sorted) is shown below.<br/>\n"
	html += f"<span style='font-family: monospace;'>{data_text}</span><br/>\n"
	html += "Which box plot correctly represents this data set?<br/>\n"
	html += "Quartile rule: exclude the median when finding Q1 and Q3."
	return html


def generate_choices(data_sorted: list, num_choices: int) -> (list, str):
	correct = five_number_summary_odd_exclusive_median(data_sorted)
	correct_html = render_boxplot_html(correct)

	distractor_summaries = make_distractor_summaries(data_sorted, correct)
	distractor_summaries = pad_distractors(distractor_summaries, correct, num_choices - 1)

	choices = [correct_html]
	for ds in distractor_summaries:
		choices.append(render_boxplot_html(ds))

	choices = list(dict.fromkeys(choices))
	while len(choices) < num_choices:
		ds = dict(correct)
		ds["median"] = ds["median"] + 1
		if is_strict(ds):
			choices.append(render_boxplot_html(ds))
			choices = list(dict.fromkeys(choices))

	choices = choices[:num_choices]
	random.shuffle(choices)
	return choices, correct_html


def write_question(N: int, args) -> str:
	data_sorted = generate_dataset_11()
	question_text = get_question_text(data_sorted)
	choices_list, answer_text = generate_choices(data_sorted, args.num_choices)

	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from sorted data (n=11)")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile(__file__, "MC", "boxplot_from_sorted_data", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
