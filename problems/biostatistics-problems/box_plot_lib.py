
import math
import random


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


def render_boxplot_html(
	summary: dict, axis_padding: int = 1, axis_bounds: tuple | None = None,
	mean: float | None = None,
) -> str:
	"""Draw independent, precisely positioned marks inside an exportable HTML table.

	An optional multiplication sign marks the actual mean. Coincident edges and fractional
	values retain their positions instead of overwriting neighboring grid cells.
	"""
	if not is_nondecreasing(summary):
		raise ValueError("Expected a nondecreasing five-number summary")
	if axis_bounds is None:
		axis_start = math.floor(summary["min"] - axis_padding)
		axis_end = math.ceil(summary["max"] + axis_padding)
	else:
		axis_start, axis_end = axis_bounds
	if not axis_start <= summary["min"] <= summary["max"] <= axis_end:
		raise ValueError("The axis must contain the five-number summary")
	if axis_start >= axis_end:
		raise ValueError("Expected an axis with positive width")

	span = axis_end - axis_start
	positions = {key: 100 * (value - axis_start) / span for key, value in summary.items()}
	# A table wrapper lets Blackboard image export capture the entire figure.
	html = '<table role="presentation" style="border-collapse: collapse; width: 480px; '
	html += 'max-width: 100%; background-color: white; color: #172333; margin: 4px 0;">'
	html += '<tr><td style="padding: 4px 24px;">'
	html += '<div style="position: relative; height: 76px; width: 100%;">'
	# Draw caps over the gray box edges so zero-length whiskers remain visible.
	html += _plot_mark(positions["q1"], positions["q3"] - positions["q1"], 6, 32,
		"background-color: #dceaf5; border: 2px solid #777777;")
	for start, end in (("min", "q1"), ("q3", "max")):
		html += _plot_mark(positions[start], positions[end] - positions[start], 22, 0,
			"border-top: 2px solid #000000;")
	for key in ("min", "max"):
		html += _plot_mark(positions[key], 0, 14, 16,
			"border-left: 3px solid #000000; margin-left: -1px;")
	html += _plot_mark(positions["median"], 0, 6, 32, "border-left: 3px solid #172333;")
	if mean is not None:
		if not axis_start <= mean <= axis_end:
			raise ValueError("The axis must contain the mean")
		mean_position = 100 * (mean - axis_start) / span
		background = "#dceaf5" if summary["q1"] <= mean <= summary["q3"] else "white"
		html += f'<span style="position: absolute; left: {mean_position:.8f}%; top: 14px; '
		html += 'width: 16px; height: 16px; margin-left: -8px; text-align: center; '
		html += f'color: black; background-color: {background}; '
		html += 'font: normal 18px/16px Arial, sans-serif;">&times;</span>'
	html += _plot_mark(0, 100, 50, 0, "border-top: 1px solid #172333;")
	# Label a manageable number of ticks without changing the plotted scale.
	step = max(1, math.ceil(span / 12))
	first_tick = math.ceil(axis_start / step) * step
	for value in range(first_tick, math.floor(axis_end) + 1, step):
		position = 100 * (value - axis_start) / span
		html += _plot_mark(position, 0, 50, 5, "border-left: 1px solid #172333;")
		html += f'<span style="position: absolute; left: {position:.8f}%; top: 60px; '
		html += 'width: 40px; margin-left: -20px; text-align: center; '
		html += f'font: 13px Arial, sans-serif;">{value}</span>'
	html += '</div></td></tr></table>'
	return html


def _plot_mark(left: float, width: float, top: int, height: int, style: str) -> str:
	"""Position a mark by its center line, including zero-width tied boxes."""
	html = f'<div style="position: absolute; left: {left:.8f}%; width: {width:.8f}%; '
	# Nonempty divs survive the exporter's XML serialization without self-closing.
	html += f'top: {top}px; height: {height}px; box-sizing: border-box; '
	html += f'font-size: 0; line-height: 0; {style}">&#160;</div>'
	return html


def render_boxplot_choices(
	correct: dict, distractors: list, num_choices: int, mean: float | None = None,
) -> tuple:
	"""Render unique alternatives with identical axis bounds and dimensions."""
	summaries = [correct]
	for summary in distractors:
		if summary not in summaries:
			summaries.append(summary)
	if len(summaries) < num_choices:
		raise ValueError("Not enough unique box plots")
	summaries = summaries[:num_choices]
	axis_bounds = (
		math.floor(min(summary["min"] for summary in summaries) - 1),
		math.ceil(max(summary["max"] for summary in summaries) + 1),
	)
	if mean is not None:
		axis_bounds = (min(axis_bounds[0], math.floor(mean - 1)),
			max(axis_bounds[1], math.ceil(mean + 1)))
	choices = [render_boxplot_html(summary, axis_bounds=axis_bounds, mean=mean)
		for summary in summaries]
	answer = choices[0]
	random.shuffle(choices)
	return choices, answer
