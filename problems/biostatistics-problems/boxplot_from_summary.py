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


def generate_summary() -> dict:
	min_v = random.randint(2, 8)
	q1_v = min_v + random.randint(2, 4)
	median_v = q1_v + random.randint(2, 4)
	q3_v = median_v + random.randint(2, 4)
	max_v = q3_v + random.randint(2, 4)

	return {"min": min_v, "q1": q1_v, "median": median_v, "q3": q3_v, "max": max_v}


def get_question_text(s: dict) -> str:
	html = ""
	html += "A variable was summarized using the five number summary below.<br/>\n"
	html += f"Minimum = <span style='font-family: monospace;'>{s['min']}</span><br/>\n"
	html += f"Q1 = <span style='font-family: monospace;'>{s['q1']}</span><br/>\n"
	html += f"Median = <span style='font-family: monospace;'>{s['median']}</span><br/>\n"
	html += f"Q3 = <span style='font-family: monospace;'>{s['q3']}</span><br/>\n"
	html += f"Maximum = <span style='font-family: monospace;'>{s['max']}</span><br/>\n"
	html += "Which box plot matches these summary statistics?"
	return html


def make_distractors(correct: dict) -> list:
	out = []

	d1 = dict(correct)
	d1["q1"] = correct["q1"] + 1
	if is_strict(d1):
		out.append(d1)

	d2 = dict(correct)
	d2["q3"] = correct["q3"] - 1
	if is_strict(d2):
		out.append(d2)

	d3 = dict(correct)
	d3["min"] = correct["min"] + 1
	if is_strict(d3):
		out.append(d3)

	d4 = dict(correct)
	d4["max"] = correct["max"] - 1
	if is_strict(d4):
		out.append(d4)

	return out


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


def generate_choices(correct: dict, num_choices: int) -> (list, str):
	correct_html = render_boxplot_html(correct)

	distractors = make_distractors(correct)
	distractors = pad_distractors(distractors, correct, num_choices - 1)

	choices = [correct_html]
	for ds in distractors:
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
	correct = generate_summary()
	question_text = get_question_text(correct)
	choices_list, answer_text = generate_choices(correct, args.num_choices)
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)


def main() -> None:
	parser = bptools.make_arg_parser("Box plot MC: select the correct plot from a five number summary")
	parser = bptools.add_choice_args(parser)
	args = parser.parse_args()

	outfile = bptools.make_outfile(__file__, "MC", "boxplot_from_summary", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == "__main__":
	main()
