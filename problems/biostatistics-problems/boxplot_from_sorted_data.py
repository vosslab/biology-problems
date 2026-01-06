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


def build_sorted_dataset_11(min_v: int, q1_v: int, med_v: int, q3_v: int, max_v: int) -> list:
	"""
	Build a sorted size-11 dataset with anchors around typical quartile positions.
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
	q1_v = min_v + random.randint(0, 3)
	med_v = q1_v + random.randint(0, 3)
	q3_v = med_v + random.randint(0, 3)
	max_v = q3_v + random.randint(0, 3)

	data = build_sorted_dataset_11(min_v, q1_v, med_v, q3_v, max_v)
	s = five_number_summary_tukey_hinges(data)

	if not is_nondecreasing(s) or not has_tie(s):
		return generate_dataset_11()

	return data


def make_distractor_summaries(data_sorted: list, correct: dict) -> list:
	"""
	Common mistakes for odd n=11 (Tukey hinges):
	- Wrong median index (5th or 7th instead of 6th)
	- Exclusive halves for quartiles (software-default trap)
	- Wrong quartile positions (off-by-one)
	"""
	x = data_sorted
	distractors = []

	d1 = dict(correct)
	d1["median"] = x[4]
	if is_nondecreasing(d1):
		distractors.append(d1)

	d2 = dict(correct)
	d2["median"] = x[6]
	if is_nondecreasing(d2):
		distractors.append(d2)

	d3 = dict(correct)
	lower_excl = x[:len(x) // 2]
	upper_excl = x[len(x) // 2 + 1:]
	d3["q1"] = median_of_sorted(lower_excl)
	d3["q3"] = median_of_sorted(upper_excl)
	if is_nondecreasing(d3):
		distractors.append(d3)

	d4 = dict(correct)
	d4["q1"] = (x[1] + x[2]) / 2
	d4["q3"] = (x[8] + x[9]) / 2
	if is_nondecreasing(d4):
		distractors.append(d4)

	d5 = dict(correct)
	d5["q1"] = (x[3] + x[4]) / 2
	d5["q3"] = (x[6] + x[7]) / 2
	if is_nondecreasing(d5):
		distractors.append(d5)

	return distractors


def get_question_text(data_sorted: list) -> str:
	data_text = ", ".join([str(v) for v in data_sorted])
	html = ""
	html += "A sample of 11 measurements (already sorted) is shown below.<br/>\n"
	html += f"<span style='font-family: monospace;'>{data_text}</span><br/>\n"
	html += "Which box plot correctly represents this data set?<br/>\n"
	html += "Quartiles use Tukey hinges (median of halves); ties are allowed and keep the summary nondecreasing."
	return html


def generate_choices(data_sorted: list, num_choices: int) -> (list, str):
	correct = five_number_summary_tukey_hinges(data_sorted)
	correct_html = render_boxplot_html(correct)

	distractor_summaries = make_distractor_summaries(data_sorted, correct)

	choices = [correct_html]
	for ds in distractor_summaries:
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
		data_sorted = generate_dataset_11()
		try:
			choices_list, answer_text = generate_choices(data_sorted, args.num_choices)
			break
		except ValueError:
			continue
	question_text = get_question_text(data_sorted)

	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from sorted data (n=11)")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile(__file__, "MC", "boxplot_from_sorted_data", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
