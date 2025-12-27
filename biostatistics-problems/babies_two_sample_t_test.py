#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Standard Library
import math
import random
import statistics

# local repo modules
import bptools


#============================================
def student_t_pdf(x: float, df: float) -> float:
	"""
	PDF of Student's t with df degrees of freedom.

	Args:
		x (float): t value.
		df (float): degrees of freedom (Welch df allowed, non-integer).

	Returns:
		float: pdf value.
	"""
	c = math.gamma((df + 1.0) / 2.0) / (math.sqrt(df * math.pi) * math.gamma(df / 2.0))
	pdf = c * (1.0 + (x * x) / df) ** (-(df + 1.0) / 2.0)
	return pdf

#============================================
def student_t_cdf(x: float, df: float) -> float:
	"""
	CDF of Student's t via Simpson integration. Accurate for df >= 10.

	Args:
		x (float): t value.
		df (float): degrees of freedom (Welch df allowed).

	Returns:
		float: P(T <= x).
	"""
	if x == 0.0:
		return 0.5
	if x < 0.0:
		return 1.0 - student_t_cdf(-x, df)

	n = 2000  # even number for Simpson's rule
	h = x / n
	s = student_t_pdf(0.0, df) + student_t_pdf(x, df)
	odd = 0.0
	even = 0.0
	i = 1
	while i < n:
		val = student_t_pdf(i * h, df)
		if i % 2 == 0:
			even += val
		else:
			odd += val
		i += 1
	area = (h / 3.0) * (s + 4.0 * odd + 2.0 * even)
	cdf = 0.5 + area
	return cdf

# simple assertion for symmetry at 0
assert 0.499 <= student_t_cdf(0.0, 30.0) <= 0.501


#============================================
def generate_group(n: int, base_mu: float, sigma: float, delta_range: tuple[float, float]) -> list[float]:
	"""
	Synthesize n baby weights with one decimal place around base_mu + delta.
	Ensures at least two distinct values (nonzero variance).
	"""
	delta = round(random.uniform(delta_range[0], delta_range[1]), 2)
	target_mu = base_mu + delta

	values = []
	i = 0
	while i < n:
		v = random.gauss(target_mu, sigma)
		v = max(4.0, min(12.0, v))
		values.append(round(v, 1))
		i += 1

	# if rounding collapsed variance, nudge one element by 0.1 within bounds
	if len(set(values)) == 1:
		j = random.randrange(n)
		step = 0.1 if values[j] <= 11.9 else -0.1
		values[j] = round(values[j] + step, 1)

	assert len(values) == n
	assert 4.0 <= min(values) <= max(values) <= 12.0
	# extra safety: guarantee variance > 0
	assert len(set(values)) > 1
	assert statistics.stdev(values) > 1e-6
	return values

#============================================
def welch_t_one_tailed(group1: list[float], group2: list[float], tails: int = 1) -> tuple[float, float, float]:
	"""
	Welch's two-sample t-test for H1: mean1 > mean2 (one-tailed by default).

	Args:
		group1 (list[float]): sample from group 1 (e.g., Joe's).
		group2 (list[float]): sample from group 2 (e.g., Veggies).
		tails (int): 1 for one-tailed, 2 for two-tailed.

	Returns:
		tuple[float, float, float]: (t_stat, df_welch, p_value)
	"""
	n1, n2 = len(group1), len(group2)
	x1, x2 = statistics.fmean(group1), statistics.fmean(group2)
	s1, s2 = statistics.stdev(group1), statistics.stdev(group2)
	assert s1 > 1e-6
	assert s2 > 1e-6

	se2 = (s1 * s1) / n1 + (s2 * s2) / n2
	se = math.sqrt(se2)
	t_stat = (x1 - x2) / se

	num = se2 * se2
	den = ((s1 * s1) / n1) ** 2 / (n1 - 1) + ((s2 * s2) / n2) ** 2 / (n2 - 1)
	df = num / den

	if tails == 1:
		p = 1.0 - student_t_cdf(t_stat, df)
	else:
		abs_t = abs(t_stat)
		p = 2.0 * (1.0 - student_t_cdf(abs_t, df))

	assert 0.0 <= p <= 1.0
	return t_stat, df, p

#============================================
def format_question_html(group1: list[float], group2: list[float], tails: int) -> str:
	"""
	Build the Blackboard NUM question stem for a two-sample t-test.

	Args:
		group1 (list[float]): Joe's Hospital weights.
		group2 (list[float]): Green Veggies weights.
		tails (int): 1 or 2.

	Returns:
		str: HTML-formatted question stem with a single numeric blank.
	"""
	rows1 = "<br/>".join(f"{w:.1f}" for w in group1)
	rows2 = "<br/>".join(f"{w:.1f}" for w in group2)
	tutorial_link = (
		"https://docs.google.com/document/d/1k5UzUlpu-5wCMyWpop0bFlXBgAWivwTwd020Jgo1EIk/edit"
	)

	q = ""
	q += ("<p><b>Two-Sample T-Test Scenario</b><br/>"
		"Previously, you compared newborn weights at Joe's Hospital of Fried "
		"Foods to the national average (7.5 lbs) using a one-sample t-test. "
		"Now, Joe faces a challenge from Alex, CEO of Green Veggies Health "
		"Center, who believes her babies are just as heavy as Joe's fried-food "
		"babies.</p>")

	n1 = len(group1)
	n2 = len(group2)
	q += (f"<p>Joe's Hospital of Fried Foods (n={n1}) and Green Veggies Health "
		f"Center (n={n2}) each recorded the weights of newborns this month. "
		"Joe believes his hospital's babies weigh more on average than those "
		"from Green Veggies.</p>")

	if tails == 1:
		q += ("<p>Use a one tailed two sample t test for "
			"H1: &mu;<sub>Joe</sub> &gt; &mu;<sub>Veggies</sub>.</p>")
	else:
		q += ("<p>Use a two tailed two sample t test for "
			"H1: &mu;<sub>Joe</sub> &ne; &mu;<sub>Veggies</sub>.</p>")
	q += "<p>Assume unequal variances (Welch's t test).</p>"
	q += "<table style='border-collapse:collapse;'><tr>"
	q += "<td style='vertical-align:top; padding-right:20px;'>"
	q += "<b>Joe's Hospital (lbs):</b><br/>"
	q += f"<span style='font-family:monospace; background-color:#eee; white-space:pre;'>{rows1}</span>"
	q += "</td>"
	q += "<td style='vertical-align:top;'>"
	q += "<b>Green Veggies (lbs):</b><br/>"
	q += f"<span style='font-family:monospace; background-color:#eee; white-space:pre;'>{rows2}</span>"
	q += "</td>"
	q += "</tr></table>"
	q += "<p>Compute the p value in Google Sheets using the tutorial:"
	q += f" <a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>.</p>"
	q += "<p>Enter your result as a decimal between 0 and 1 "
	q += "(for example, 0.084, not 8.4%).</p>"
	return q


#============================================
def write_question(N: int, args) -> str:
	"""
	Create one Blackboard numeric question row for a two-sample t-test.

	Args:
		N (int): question number.
		tails (int): 1 for one-tailed, 2 for two-tailed.

	Returns:
		str: formatted Blackboard NUM question row.
	"""
	base_mu = 7.5
	sigma = 1.5

	tails = args.tails
	n1 = random.randint(25, 39)
	n2 = random.randint(25, 39)
	#bring numbers closer together
	half_diff = abs(n1 - n2) // 4

	if n1 > n2:
		n1 -= half_diff
		n2 += half_diff
	elif n1 < n2:
		n1 += half_diff
		n2 -= half_diff
	if n1 == n2:
		n1 += 1

	min_p, max_p = 0.05, 0.95
	max_tries = 200

	p_value = 1.0
	tries = 0
	group1 = []
	group2 = []

	while not (min_p < p_value < max_p) and tries < max_tries:
		# Joe's shifted higher; Veggies shifted lower
		group1 = generate_group(n1, base_mu, sigma, (0.10, 0.60))
		group2 = generate_group(n2, base_mu, sigma, (-0.60, -0.10))

		mean1 = statistics.fmean(group1)
		mean2 = statistics.fmean(group2)
		if mean1 <= mean2:
			tries += 1
			continue

		t_stat, df, p_value = welch_t_one_tailed(group1, group2, tails)
		tries += 1

	assert min_p <= p_value <= max_p
	assert len(group1) == n1 and len(group2) == n2
	assert statistics.fmean(group1) > statistics.fmean(group2)

	question_text = format_question_html(group1, group2, tails)

	answer_float = p_value
	tolerance_float = round(max(0.001, 0.01 * answer_float), 4)

	complete_question = bptools.formatBB_NUM_Question(
		N, question_text, answer_float, tolerance_float, tol_message=False
	)
	return complete_question


#============================================
def parse_arguments():
	"""
	Parse command-line arguments.

	Returns:
		argparse.Namespace: args with duplicates, max_questions, tails.
	"""
	parser = bptools.make_arg_parser(description="Generate two-sample t-test questions.")
	parser.add_argument(
		'-q', '--tails', type=int, dest='tails',
		choices=(1, 2), default=1, help='1 for one-tailed, 2 for two-tailed.'
	)
	args = parser.parse_args()
	return args


#============================================
def main():
	"""
	Generate and save a bank of two-sample t-test numeric questions.

	Workflow:
	1. Parse CLI args.
	2. Build filename with script name and tails.
	3. Generate formatted questions.
	4. Shuffle and trim if needed.
	5. Write to output file and report.
	"""
	args = parse_arguments()

	outfile = bptools.make_outfile(None, f"tails{args.tails}")
	bptools.collect_and_write_questions(write_question, args, outfile)


#============================================
if __name__ == '__main__':
	main()
