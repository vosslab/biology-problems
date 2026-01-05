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
def f_pdf(x: float, d1: int, d2: int) -> float:
	"""
	PDF of F(d1, d2).
	"""
	if x <= 0.0:
		return 0.0
	a = d1 / 2.0
	b = d2 / 2.0
	beta = math.gamma(a) * math.gamma(b) / math.gamma(a + b)
	num = (d1 ** a) * (d2 ** b) * (x ** (a - 1.0))
	den = beta * ((d1 * x + d2) ** (a + b))
	return num / den

#============================================
def f_cdf(x: float, d1: int, d2: int) -> float:
	"""
	CDF of F(d1, d2) via Simpson integration. Accurate for typical df.
	"""
	if x <= 0.0:
		return 0.0
	n = 2000  # even
	h = x / n
	s = f_pdf(0.0, d1, d2) + f_pdf(x, d1, d2)
	odd = 0.0
	even = 0.0
	i = 1
	while i < n:
		val = f_pdf(i * h, d1, d2)
		if i % 2 == 0:
			even += val
		else:
			odd += val
		i += 1
	area = (h / 3.0) * (s + 4.0 * odd + 2.0 * even)
	return area

#============================================
def f_test_variances(group2014: list[float], group2024: list[float], tails: int = 2) -> tuple[float, int, int, float]:
	"""
	Two-sample F-test on variances.
	One-tailed H1 (tails=1): var_2024 < var_2014.
	Two-tailed H1 (tails=2): var_2024 != var_2014.
	Returns (F, df1, df2, p).
	"""
	n1, n2 = len(group2014), len(group2024)
	s1 = statistics.stdev(group2014)
	s2 = statistics.stdev(group2024)
	assert s1 > 1e-9 and s2 > 1e-9

	# Ratio set so H1: var_2024 < var_2014 corresponds to F large
	F = (s1 * s1) / (s2 * s2)
	df1 = n1 - 1
	df2 = n2 - 1

	if tails == 1:
		p = 1.0 - f_cdf(F, df1, df2)
	else:
		# Two-tailed: 2 * min( P(F<=f), P(F>=f) )
		p_lower = f_cdf(F, df1, df2)
		p_upper = 1.0 - p_lower
		p = 2.0 * min(p_lower, p_upper)

	assert 0.0 <= p <= 1.0
	return F, df1, df2, p

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
def format_question_html(
	years_2014: list[float],
	years_2024: list[float],
	tails: int,
	selected_sites: list[str]
) -> str:
	"""
	Build the Blackboard NUM question stem for a two-sample F-test of variances.
	"""
	pairs = sorted(zip(selected_sites, years_2014, years_2024), key=lambda x: x[0])

	table_html = (
		"<table border='1' cellpadding='3' style='border-collapse:collapse;'>"
		"<tr>"
		"<th style='text-align:center;'>Sample<br/>Location</th>"
		"<th style='text-align:center;'>2014<br/>Shannon<br/>Index</th>"
		"<th style='text-align:center;'>2024<br/>Shannon<br/>Index</th>"
		"</tr>"
	)
	for site, v14, v24 in pairs:
		table_html += (
			f"<tr><td>{site}</td>"
			f"<td style='text-align:right;'>{v14:.2f}</td>"
			f"<td style='text-align:right;'>{v24:.2f}</td></tr>"
		)
	table_html += "</table>"

	csv_rows = "Sample Location,2014 Shannon Index,2024 Shannon Index<br/>"
	for site, v14, v24 in pairs:
		csv_rows += f"{site},{v14:.2f},{v24:.2f}<br/>"

	tutorial_link = "https://docs.google.com/document/d/1tQE36lOQ_HJ2LsZdpqBnQl98xdz8G6YE7JRa6c9Mi9o/edit"

	q = "<p><b>F-Test of Variances: 2014 vs 2024</b></p>"
	if tails == 1:
		q += "<p>Use a one tailed F test for H1: variance_2024 &lt; variance_2014.</p>"
	else:
		q += "<p>Use a two tailed F test for H1: variance_2024 != variance_2014.</p>"

	q += "<p>Sample Data Table:<br/>"
	q += "<em>Copy the table rows and use regular paste (Ctrl-V or &#8984;-V) into Google Sheets.</em></p>"
	q += table_html

	q += "<p>Alternate Copyable Format:<br/>"
	q += "<em>Copy this text and use <strong>Data &rarr; Split text to columns &rarr; Comma</strong> in Google Sheets.</em></p>"
	q += f"<p><span style='font-family: monospace; background-color:#eee;'>{csv_rows}</span></p>"

	q += "<p>Enter the p value as a decimal between 0 and 1.</p>"
	q += f"<p>Workflow: <a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>.</p>"
	return q

#============================================
def _write_one_question(N: int, tails: int) -> str:
	"""
	Create one Blackboard numeric question row for an F-test of variances.
	"""
	# Keep means near the same; change dispersion between years
	mu_center = 4.0
	base_sigma = 0.55

	n = random.randint(12, 24)
	sites = random.sample(DIVERSITY_SITES, n)

	min_p, max_p = 0.05, 0.95
	max_tries = 200

	p_value = 1.0
	tries = 0
	y2014: list[float] = []
	y2024: list[float] = []

	while not (min_p < p_value < max_p) and tries < max_tries:
		# Make 2014 variance larger than 2024 for one-tailed H1
		shift = round(random.uniform(0.10, 0.40), 2)
		sig14 = base_sigma * (1.0 + shift)
		sig24 = base_sigma * (1.0 - shift)

		y2014 = generate_shannon_group(n, mu_center, sig14)
		y2024 = generate_shannon_group(n, mu_center, sig24)

		# Enforce one-tailed direction if requested
		if tails == 1:
			if statistics.variance(y2024) >= statistics.variance(y2014):
				tries += 1
				continue

		F, df1, df2, p_value = f_test_variances(y2014, y2024, tails)
		tries += 1

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
def write_question(N: int, args) -> str:
	return _write_one_question(N, args.tails)

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
	outfile = bptools.make_outfile(None, f"tails{args.tails}")
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
if __name__ == '__main__':
	main()
