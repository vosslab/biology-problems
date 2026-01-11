#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Standard Library
import math
import random
import statistics

# local repo modules
import bptools

#============================================
# Sites master list
DIVERSITY_SITES: list[str] = [
	"Andrews Park",
	"Beisner Road Entrance",
	"Boat Launch Area",
	"Busse Lake",
	"Debra Park",
	"Elk Pasture",
	"Forest Central Grove",
	"Forest North Grove",
	"Forest South Grove",
	"Forest West Grove",
	"Lake Boating Center",
	"Large Event Area",
	"Main Dam",
	"Main Pool",
	"Marshall Park",
	"Model Airplane Field",
	"Nature Preserve",
	"Ned Brown Meadow",
	"North Pool",
	"Osborn Park",
	"Salt Creek Trail",
	"South Pool",
	"Wildlife Refuge",
	"Woodland Meadow",
]

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

	n = 2000
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
def generate_shannon_group(
	n: int,
	target_mu: float,
	sigma: float,
	bounds: tuple[float, float] = (1.0, 6.5)
) -> list[float]:
	"""
	Generate n Shannon Index values around target_mu.

	Args:
		n (int): sample size.
		target_mu (float): target mean for generation.
		sigma (float): dispersion for generation.
		bounds (tuple[float, float]): clamp range [low, high].

	Returns:
		list[float]: n values rounded to 2 decimals within bounds.
	"""
	low, high = bounds
	values: list[float] = []
	i = 0
	while i < n:
		v = random.gauss(target_mu, sigma)
		v = max(low, min(high, v))
		values.append(round(v, 2))
		i += 1

	# ensure variance survives rounding
	if len(set(values)) == 1:
		j = random.randrange(n)
		step = 0.02 if values[j] <= high - 0.02 else -0.02
		values[j] = round(values[j] + step, 2)

	assert len(values) == n
	assert low <= min(values) <= max(values) <= high
	assert statistics.stdev(values) > 1e-6
	return values

#============================================
def welch_t(group1: list[float], group2: list[float], tails: int = 1) -> tuple[float, float, float]:
	"""
	Welch two sample t-test.

	Args:
		group1 (list[float]): sample 1.
		group2 (list[float]): sample 2.
		tails (int): 1 for one-tailed, 2 for two-tailed.

	Returns:
		tuple[float, float, float]: (t_stat, df_welch, p_value)
	"""
	n1, n2 = len(group1), len(group2)
	x1, x2 = statistics.fmean(group1), statistics.fmean(group2)
	s1, s2 = statistics.stdev(group1), statistics.stdev(group2)
	assert s1 > 1e-6 and s2 > 1e-6

	se2 = (s1 * s1) / n1 + (s2 * s2) / n2
	se = math.sqrt(se2)
	t_stat = (x1 - x2) / se

	num = se2 * se2
	den = ((s1 * s1) / n1) ** 2 / (n1 - 1) + ((s2 * s2) / n2) ** 2 / (n2 - 1)
	df = num / den

	if tails == 1:
		# one tailed in the direction group1 > group2
		p = 1.0 - student_t_cdf(t_stat, df)
	else:
		abs_t = abs(t_stat)
		p = 2.0 * (1.0 - student_t_cdf(abs_t, df))

	assert 0.0 <= p <= 1.0
	return t_stat, df, p

#============================================
def format_question_html(
	years_2014: list[float],
	years_2024: list[float],
	tails: int,
	selected_sites: list[str]
) -> str:
	"""
	Build the Blackboard NUM question stem for two-sample test.

	Args:
		years_2014 (list[float]): Shannon indices for 2014.
		years_2024 (list[float]): Shannon indices for 2024.
		tails (int): 1 or 2.
		selected_sites (list[str]): sites paired with values.

	Returns:
		str: HTML with a single numeric blank.
	"""
	# Pair and sort alphabetically by site
	pairs = sorted(zip(selected_sites, years_2014, years_2024), key=lambda x: x[0])

	# Build HTML table
	table_html = (
		"<table border='1' cellpadding='3' style='border-collapse:collapse;'>"
		"<tr>"
		"<th style='text-align:center;'>Sample<br/>Location</th>"
		"<th style='text-align:center;'>2014<br/>Shannon<br/>Index</th>"
		"<th style='text-align:center;'>2024<br/>Shannon<br/>Index</th>"
		"</tr>"
	)
	for site, v14, v24 in pairs:
		table_html += f"<tr><td>{site}</td><td style='text-align:right;'>{v14:.2f}</td><td style='text-align:right;'>{v24:.2f}</td></tr>"
	table_html += "</table>"

	# Build CSV-style block for copy/paste
	csv_rows = "Sample Location,2014 Shannon Index,2024 Shannon Index<br/>"
	for site, v14, v24 in pairs:
		csv_rows += f"{site},{v14:.2f},{v24:.2f}<br/>"

	tutorial_link = "https://docs.google.com/document/d/1DiSYMwPhs8tmWQMLqQwLGHBssy12o-pYzyUT1qIoXcU/edit"

	q = "<p><b>Two-Sample Test of Shannon Diversity: 2014 vs 2024</b></p>"
	if tails == 1:
		q += "<p>Use a one tailed Welch two sample t test for H1: mean_2024 &lt; mean_2014.</p>"
	else:
		q += "<p>Use a two tailed Welch two sample t test for H1: mean_2024 != mean_2014.</p>"

	q += "<p>Assume unequal variances.</p>"

	# Table format
	q += "<p>Sample Data Table:<br/>"
	q += "<em>Copy the table rows and use regular paste (Ctrl-V or &#8984;-V) into Google Sheets.</em></p>"
	q += table_html

	# CSV format
	q += "<p>Alternate Copyable Format:<br/>"
	q += "<em>Copy this text and use <strong>Data &rarr; Split text to columns &rarr; Comma</strong> in Google Sheets.</em></p>"
	q += f"<p><span style='font-family: monospace; background-color:#eee;'>{csv_rows}</span></p>"

	# Instructions
	q += "<p>Compute the p value in Google Sheets using the tutorial: "
	q += f"<a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>.</p>"
	q += "<p>Enter the p value as a decimal between 0 and 1.</p>"
	return q

#============================================
def write_question(N: int, args) -> str:
	"""
	Create one Blackboard numeric question row for a two-sample test.

	Args:
		N (int): question number.
		tails (int): 1 for one tailed, 2 for two tailed.

	Returns:
		str: formatted Blackboard NUM question row.
	"""
	tails = args.tails
	# Target means: 2014 slightly higher than 2024 to reflect decline
	mu_benchmark = 4.0
	shannon_sigma = 0.55

	# choose a random subset of sites; keep 12 to 24 rows
	n = random.randint(12, 24)
	sites = random.sample(DIVERSITY_SITES, n)

	min_p, max_p = 0.05, 0.95
	max_tries = 200

	p_value = 1.0
	tries = 0
	y2014: list[float] = []
	y2024: list[float] = []

	while not (min_p < p_value < max_p) and tries < max_tries:
		# 2014 a bit above benchmark; 2024 a bit below
		shift = round(random.uniform(0.10, 0.60), 2)
		mu_2014 = mu_benchmark + shift
		mu_2024 = mu_benchmark - shift

		y2014 = generate_shannon_group(n, mu_2014, shannon_sigma)
		y2024 = generate_shannon_group(n, mu_2024, shannon_sigma)

		# enforce direction for one tailed hypothesis if needed
		if tails == 1 and statistics.fmean(y2024) >= statistics.fmean(y2014):
			tries += 1
			continue

		t_stat, df, p_value = welch_t(y2014, y2024, tails)
		tries += 1

	# sanity checks
	assert min_p <= p_value <= max_p
	assert len(y2014) == n and len(y2024) == n

	question_text = format_question_html(y2014, y2024, tails, sites)

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
	parser = bptools.make_arg_parser(description="Generate two-sample Shannon tests.")
	parser.add_argument(
		'-q', '--tails', type=int, dest='tails',
		choices=(1, 2), default=1, help='1 for one tailed, 2 for two tailed.'
	)
	args = parser.parse_args()
	return args

#============================================
def main():
	"""
	Generate and save a bank of two-sample Shannon numeric questions.

	Workflow:
	1. Parse CLI args.
	2. Build filename with script name and tails.
	3. Generate formatted questions.
	4. Shuffle and trim if needed.
	5. Write to output file and report.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(f"tails{args.tails}")
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
if __name__ == '__main__':
	main()
