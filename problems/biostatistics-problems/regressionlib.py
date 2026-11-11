"""Shared data and calculations for Dr. Caffeine spreadsheet assignments."""

import random

import numpy


def r_squared(pairs: list[tuple[float, int]], degree: int) -> float:
	"""Return coefficient of determination for a model including an intercept."""
	x, y = numpy.array(pairs, dtype=float).T
	design = numpy.vander(x, degree + 1, increasing=True)
	coefficients, _, rank, _ = numpy.linalg.lstsq(design, y, rcond=None)
	if rank != degree + 1:
		raise ValueError("Regression predictors must have full rank")
	residuals = y - design @ coefficients
	centered = y - y.mean()
	total = float(centered @ centered)
	if total == 0:
		raise ValueError("R-squared requires variation in exam scores")
	result = float(1 - (residuals @ residuals) / total)
	return result


def generate_data(degree: int) -> list[tuple[float, int]]:
	"""Draw 25 paired observations with either direction or curvature sign."""
	# Three distinct values guarantee full rank for either model.
	x_values = [3.0, 7.0, 11.5] + [random.randint(6, 23) / 2 for _ in range(22)]
	random.shuffle(x_values)
	direction = random.choice((-1, 1))
	strength = random.uniform(0.1, 4.0) if degree == 1 else random.uniform(0.03, 1.5)
	center = random.uniform(6.5, 8.0)
	baseline = random.uniform(65, 78)
	noise = random.uniform(3, 12)
	pairs = []
	for x in x_values:
		mean = baseline + direction * strength * (x - center) ** degree
		score = round(random.gauss(mean, noise))
		pairs.append((x, score))
	return pairs


def question_text(pairs: list[tuple[float, int]], degree: int) -> str:
	"""Present paired data and a task using the student's completed spreadsheet."""
	sheet = "Linear Regression" if degree == 1 else "Quadratic Regression"
	q = "<p>Dr. Caffeine collected sleep and exam-score data from 25 new students.</p>"
	q += "<table style='border-collapse:collapse;color:#202020;background-color:#ffffff;'>"
	q += "<tr><th scope='col' style='padding:4px;'>Hours of sleep</th>"
	q += "<th scope='col' style='padding:4px;'>Exam score (%)</th></tr>"
	for index, (x, y) in enumerate(pairs):
		background = "#f2f5f7" if index % 2 else "#ffffff"
		q += f"<tr style='background-color:{background};'>"
		q += f"<td style='padding:4px;text-align:right;'>{x:.1f}</td>"
		q += f"<td style='padding:4px;text-align:right;'>{y}</td></tr>"
	q += "</table>"
	q += "<p>Copyable data (25 rows, no header):<br/>"
	q += "<span style='font-family:monospace;'>"
	q += "<br/>".join(f"{x:.1f},{y}" for x, y in pairs)
	q += "</span></p>"
	q += f"<p>In your completed Dr. Caffeine tutorial spreadsheet, open <b>{sheet}</b>. "
	q += "Replace the old sleep and exam-score data with these pairs and follow the "
	q += "tutorial workflow. For the comma-separated text, use "
	q += "Data &rarr; Split text to columns &rarr; Comma.</p>"
	q += "<p>What is the <strong>R<sup>2</sup> value</strong> for your fitted model?</p>"
	q += "<p>Enter a decimal between 0 and 1, to at least three decimal places "
	q += "(for example, 0.084, not 8.4%). Use your new results rather than the tutorial's "
	q += "example results.</p>"
	return q
