#!/usr/bin/env python3

import random

import bptools
from box_plot_lib import has_tie, is_nondecreasing, render_boxplot_choices


def generate_summary() -> dict:
	min_v = random.randint(2, 8)
	q1_v = min_v + random.randint(0, 3)
	median_v = q1_v + random.randint(0, 3)
	q3_v = median_v + random.randint(0, 3)
	max_v = q3_v + random.randint(0, 3)

	summary = {"min": min_v, "q1": q1_v, "median": median_v, "q3": q3_v, "max": max_v}
	if not is_nondecreasing(summary) or not has_tie(summary):
		return generate_summary()
	# These eight observations have exactly the requested Tukey hinges.
	data = [min_v, q1_v, q1_v, median_v, median_v, q3_v, q3_v, max_v]
	summary["mean"] = sum(data) / len(data)
	return summary


def get_question_text(s: dict) -> str:
	html = ""
	html += "A variable was summarized using the five number summary below.<br/>\n"
	html += f"Minimum = <span style='font-family: monospace;'>{s['min']}</span><br/>\n"
	html += f"Q1 = <span style='font-family: monospace;'>{s['q1']}</span><br/>\n"
	html += f"Median = <span style='font-family: monospace;'>{s['median']}</span><br/>\n"
	html += f"Q3 = <span style='font-family: monospace;'>{s['q3']}</span><br/>\n"
	html += f"Maximum = <span style='font-family: monospace;'>{s['max']}</span><br/>\n"
	if "mean" in s:
		html += f"Mean = <span style='font-family: monospace;'>{s['mean']:g}</span><br/>"
		html += "The &times; marks the mean; the vertical line marks the median.<br/>"
	html += "Which box plot matches these summary statistics?<br/>\n"
	html += "Quartiles use Tukey hinges (median of halves); ties are allowed and keep the summary nondecreasing."
	return html


def make_distractors(correct: dict) -> list:
	out = []

	d1 = dict(correct)
	d1["q1"] = correct["q3"]
	d1["q3"] = correct["q1"]
	if is_nondecreasing(d1):
		out.append(d1)

	d2 = dict(correct)
	d2["min"] = correct["q1"]
	d2["max"] = correct["q3"]
	if is_nondecreasing(d2):
		out.append(d2)

	d3 = dict(correct)
	d3["median"] = (correct["q1"] + correct["q3"]) / 2
	if is_nondecreasing(d3):
		out.append(d3)

	d4 = dict(correct)
	d4["q1"] = (correct["min"] + correct["q1"]) / 2
	d4["q3"] = (correct["q3"] + correct["max"]) / 2
	if is_nondecreasing(d4):
		out.append(d4)

	d5 = dict(correct)
	d5["q1"] = correct["min"]
	d5["q3"] = correct["max"]
	if is_nondecreasing(d5):
		out.append(d5)

	return out


def generate_choices(correct: dict, num_choices: int) -> (list, str):
	distractors = make_distractors(correct)
	mean = correct.get("mean")
	choices, answer = render_boxplot_choices(correct, distractors, num_choices, mean=mean)
	return choices, answer


def write_question(N: int, args) -> str:
	while True:
		correct = generate_summary()
		try:
			choices_list, answer_text = generate_choices(correct, args.num_choices)
			break
		except ValueError:
			continue
	question_text = get_question_text(correct)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from a five number summary")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile("MC", "boxplot_from_summary", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
