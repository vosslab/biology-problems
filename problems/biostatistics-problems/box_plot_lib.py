#!/usr/bin/env python3

import make_html_box_plot


def median_of_sorted(values: list) -> float:
	n = len(values)
	mid = n // 2
	if n % 2 == 1:
		return values[mid]
	return (values[mid - 1] + values[mid]) / 2


def five_number_summary_tukey_hinges(values: list) -> dict:
	"""
	Quartile rule (Tukey hinges):
	- Median is the middle value (or average of the two middle values).
	- Q1 is the median of the lower half.
	- Q3 is the median of the upper half.
	For odd n, include the overall median in both halves.
	"""
	x = sorted(values)
	n = len(x)
	if n == 0:
		raise ValueError("Expected at least one value")

	med = median_of_sorted(x)
	if n % 2 == 1:
		lower = x[:n // 2 + 1]
		upper = x[n // 2:]
	else:
		lower = x[:n // 2]
		upper = x[n // 2:]

	q1 = median_of_sorted(lower)
	q3 = median_of_sorted(upper)

	return {"min": x[0], "q1": q1, "median": med, "q3": q3, "max": x[-1]}


def is_nondecreasing(summary: dict) -> bool:
	return summary["min"] <= summary["q1"] <= summary["median"] <= summary["q3"] <= summary["max"]


def has_tie(summary: dict) -> bool:
	return (
		summary["min"] == summary["q1"]
		or summary["q1"] == summary["median"]
		or summary["median"] == summary["q3"]
		or summary["q3"] == summary["max"]
	)


def render_boxplot_html(summary: dict, axis_padding: int = 1) -> str:
	axis_start = max(0, summary["min"] - axis_padding)
	axis_end = summary["max"] + axis_padding

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

	grid = make_html_box_plot.create_grid(box_plot.axis_start, box_plot.axis_end, scale=box_plot.scale)
	grid = make_html_box_plot.assign_elements(grid, box_plot)
	return make_html_box_plot.generate_html(grid, box_plot.axis_start, box_plot.axis_end, scale=box_plot.scale)
