#!/usr/bin/env python3

import random

import bptools
from box_plot_lib import (
	five_number_summary_tukey_hinges,
	has_tie,
	is_nondecreasing,
	median_of_sorted,
	render_boxplot_html,
)


def build_sorted_dataset_12(min_v: int) -> list:
	"""
	Build a sorted size-12 dataset with possible ties and fractional quartiles.
	"""
	data = [min_v]
	for _ in range(11):
		data.append(data[-1] + random.randint(0, 3))
	return data


def generate_dataset_12_unsorted() -> list:
	min_v = random.randint(2, 7)
	data_sorted = build_sorted_dataset_12(min_v)
	s = five_number_summary_tukey_hinges(data_sorted)
	if not is_nondecreasing(s) or not has_tie(s):
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
	html += "Quartiles use Tukey hinges (median of halves); ties are allowed and keep the summary nondecreasing."
	return html


def summary_assuming_given_order(values: list) -> dict:
	n = len(values)
	if n % 2 != 0:
		raise ValueError("Expected even n")
	med = (values[n // 2 - 1] + values[n // 2]) / 2
	q1 = (values[n // 4 - 1] + values[n // 4]) / 2
	q3 = (values[3 * n // 4 - 1] + values[3 * n // 4]) / 2
	return {"min": min(values), "q1": q1, "median": med, "q3": q3, "max": max(values)}


def quantile_linear_interpolation(sorted_values: list, p: float) -> float:
	n = len(sorted_values)
	if n == 1:
		return sorted_values[0]
	h = (n - 1) * p + 1
	h_floor = int(h)
	frac = h - h_floor
	x0 = sorted_values[h_floor - 1]
	if h_floor >= n:
		return x0
	x1 = sorted_values[h_floor]
	return x0 + frac * (x1 - x0)


def make_distractors_from_correct(data_unsorted: list, correct: dict) -> list:
	distractors = []
	x = sorted(data_unsorted)

	d1 = summary_assuming_given_order(data_unsorted)
	if is_nondecreasing(d1):
		distractors.append(d1)

	d2 = dict(correct)
	d2["median"] = x[len(x) // 2 - 1]
	if is_nondecreasing(d2):
		distractors.append(d2)

	d3 = dict(correct)
	d3["median"] = x[len(x) // 2]
	if is_nondecreasing(d3):
		distractors.append(d3)

	d4 = dict(correct)
	lower_wrong = x[:len(x) // 2 + 1]
	upper_wrong = x[len(x) // 2 - 1:]
	d4["q1"] = median_of_sorted(lower_wrong)
	d4["q3"] = median_of_sorted(upper_wrong)
	if is_nondecreasing(d4):
		distractors.append(d4)

	d5 = dict(correct)
	d5["q1"] = quantile_linear_interpolation(x, 0.25)
	d5["median"] = quantile_linear_interpolation(x, 0.5)
	d5["q3"] = quantile_linear_interpolation(x, 0.75)
	if is_nondecreasing(d5):
		distractors.append(d5)

	return distractors


def generate_choices(data_unsorted: list, num_choices: int) -> (list, str):
	correct = five_number_summary_tukey_hinges(data_unsorted)
	correct_html = render_boxplot_html(correct)

	distractors = make_distractors_from_correct(data_unsorted, correct)

	choices = [correct_html]
	for ds in distractors:
		if ds != correct:
			choices.append(render_boxplot_html(ds))

	choices = list(dict.fromkeys(choices))
	if len(choices) < num_choices:
		raise ValueError("Not enough unique distractors for this dataset.")

	choices = choices[:num_choices]
	random.shuffle(choices)
	return choices, correct_html


def write_question(N: int, args) -> str:
	while True:
		data_unsorted = generate_dataset_12_unsorted()
		try:
			choices_list, answer_text = generate_choices(data_unsorted, args.num_choices)
			break
		except ValueError:
			continue
	question_text = get_question_text(data_unsorted)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from unsorted data (n=12)")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile("MC", "boxplot_from_unsorted_even", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
