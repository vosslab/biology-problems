#!/usr/bin/env python3

import random

import bptools
import make_html_box_plot


def five_number_summary_even_median_of_halves(values: list) -> dict:
	"""
	Quartile rule (even n):
	- Median is the average of the two middle values.
	- Q1 is the median of the lower half.
	- Q3 is the median of the upper half.

	This generator constructs data so these are all integers.
	"""
	x = sorted(values)
	n = len(x)
	if n % 2 != 0:
		raise ValueError("Expected even n")

	mid1 = x[n // 2 - 1]
	mid2 = x[n // 2]
	med = (mid1 + mid2) // 2

	lower = x[:n // 2]
	upper = x[n // 2:]

	q1 = (lower[len(lower) // 2 - 1] + lower[len(lower) // 2]) // 2
	q3 = (upper[len(upper) // 2 - 1] + upper[len(upper) // 2]) // 2

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
	return make_html_box_plot.generate_html(grid, box_plot.axis_start, box_plot.axis_end)


def is_strict(summary: dict) -> bool:
	return summary["min"] < summary["q1"] < summary["median"] < summary["q3"] < summary["max"]


def build_sorted_dataset_12(min_v: int, q1_v: int, med_v: int, q3_v: int, max_v: int) -> list:
	"""
	Build a sorted size-12 dataset so that:
	- 3rd and 4th terms are Q1
	- 6th and 7th terms are median
	- 9th and 10th terms are Q3
	This forces integer quartiles and median under averaging.
	"""
	x1 = min_v
	x3 = q1_v
	x4 = q1_v
	x6 = med_v
	x7 = med_v
	x9 = q3_v
	x10 = q3_v
	x12 = max_v

	x2 = random.randint(x1, x3)
	x5 = random.randint(x4, x6)
	x8 = random.randint(x7, x9)
	x11 = random.randint(x10, x12)

	data = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12]
	return sorted(data)


def generate_dataset_12_unsorted() -> list:
	min_v = random.randint(2, 7)
	q1_v = min_v + random.randint(2, 4)
	med_v = q1_v + random.randint(2, 4)
	q3_v = med_v + random.randint(2, 4)
	max_v = q3_v + random.randint(2, 4)

	data_sorted = build_sorted_dataset_12(min_v, q1_v, med_v, q3_v, max_v)
	s = five_number_summary_even_median_of_halves(data_sorted)
	if not is_strict(s):
		return generate_dataset_12_unsorted()

	data = list(data_sorted)
	random.shuffle(data)
	return data


def get_question_text(data_unsorted: list) -> str:
	data_text = ", ".join([str(v) for v in data_unsorted])
	html = ""
	html += "A sample of 12 measurements (unsorted) is shown below.<br/>\n"
	html += f"<span style='font-family: monospace;'>{data_text}</span><br/>\n"
	html += "Which box plot correctly represents this data set?<br/>\n"
	html += "Quartile rule: median of halves, using averages for the middle two values."
	return html


def make_distractors_from_correct(correct: dict) -> list:
	distractors = []

	d1 = dict(correct)
	d1["q1"] = correct["q1"] + 1
	if is_strict(d1):
		distractors.append(d1)

	d2 = dict(correct)
	d2["q3"] = correct["q3"] - 1
	if is_strict(d2):
		distractors.append(d2)

	d3 = dict(correct)
	d3["median"] = correct["median"] + 1
	if is_strict(d3):
		distractors.append(d3)

	d4 = dict(correct)
	d4["min"] = correct["min"] + 1
	if is_strict(d4):
		distractors.append(d4)

	return distractors


def pad_distractors(distractors: list, correct: dict, target: int) -> list:
	out = list(distractors)
	tries = 0
	while len(out) < target and tries < 60:
		tries += 1
		ds = dict(correct)
		key = random.choice(["min", "q1", "median", "q3", "max"])
		ds[key] = ds[key] + random.choice([-2, -1, 1, 2])
		if is_strict(ds):
			out.append(ds)
	return out[:target]


def generate_choices(data_unsorted: list, num_choices: int) -> (list, str):
	correct = five_number_summary_even_median_of_halves(data_unsorted)
	correct_html = render_boxplot_html(correct)

	distractors = make_distractors_from_correct(correct)
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
	data_unsorted = generate_dataset_12_unsorted()
	question_text = get_question_text(data_unsorted)
	choices_list, answer_text = generate_choices(data_unsorted, args.num_choices)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from unsorted data (n=12)")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile(__file__, "MC", "boxplot_from_unsorted_even", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
