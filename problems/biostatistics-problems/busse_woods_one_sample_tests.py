#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import math
# Provides functions to generate random numbers and selections
import random
import statistics

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#============================================
# Replace the old DIVERSITY_POOL with names only
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
def generate_diversity_values(k: int, mu: float, sigma: float, method: str) -> list[float]:
	"""
	Generate k Shannon Index values, analogous to baby weights generation.

	Args:
		k (int): Sample size.
		mu (float): Benchmark mean (e.g., 4.0).
		sigma (float): Population sd used for Z generation range control.
		method (str): 'ztest' or 'ttest' to steer mean direction.

	Returns:
		list[float]: k values rounded to two decimals within [1.0, 6.0].
	"""
	k = max(5, min(k, len(DIVERSITY_SITES)))
	shift = round(random.uniform(0.10, 0.60), 2)

	if method.lower().startswith('t'):
		target_mu = mu - shift
	else:
		target_mu = mu + random.choice([-1.0, 1.0]) * 0.6 * shift

	values: list[float] = []
	i = 0
	while i < k:
		v = random.gauss(target_mu, sigma)
		v = max(1.0, min(6.0, v))
		values.append(round(v, 2))
		i += 1

	if method.lower().startswith('t') and statistics.fmean(values) >= mu:
		j = max(range(k), key=lambda idx: values[idx])
		values[j] = round(max(1.0, values[j] - 0.2), 2)

	assert len(values) == k
	return values


#============================================
def normal_cdf(z: float) -> float:
	"""
	Compute Phi(z), the standard normal CDF, using math.erf.

	Args:
		z (float): Z value.

	Returns:
		float: Cumulative probability P(Z <= z).
	"""
	p = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
	return p

# Simple assertion test for the function: 'normal_cdf'
assert 0.499 < normal_cdf(0.0) < 0.501

#============================================
def student_t_pdf(x: float, df: int) -> float:
	"""
	PDF of Student's t with df degrees of freedom.

	Args:
		x (float): t value.
		df (int): degrees of freedom.

	Returns:
		float: pdf value.
	"""
	c = math.gamma((df + 1) / 2) / (math.sqrt(df * math.pi) * math.gamma(df / 2))
	return c * (1 + (x * x) / df) ** (-(df + 1) / 2)

#============================================
def student_t_cdf(x: float, df: int) -> float:
	"""
	CDF of Student's t using numeric integration (Simpson). Accurate for df>=10.

	Args:
		x (float): t value.
		df (int): degrees of freedom.

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
	return 0.5 + area

#============================================
def test_stat_and_p(
	values: list[float],
	mu: float,
	sigma: float | None,
	method: str,
	tail: str
) -> tuple[float, float]:
	"""
	Compute test statistic and p value for one sample tests.

	Args:
		values (list[float]): Sample values.
		mu (float): Benchmark mean.
		sigma (float|None): Population sd for Z test, else None.
		method (str): 'ztest' or 'ttest'.
		tail (str): 'less', 'greater', or 'two'.

	Returns:
		tuple[float, float]: (statistic, p_value).
	"""
	n = len(values)
	xbar = statistics.fmean(values)

	if method.lower().startswith('t'):
		s = statistics.stdev(values)
		t = (xbar - mu) / (s / math.sqrt(n))
		df = n - 1
		if tail == 'greater':
			p = 1.0 - student_t_cdf(t, df)
		elif tail == 'less':
			p = student_t_cdf(t, df)
		else:
			p = 2.0 * min(student_t_cdf(t, df), 1.0 - student_t_cdf(t, df))
		return t, p

	if method.lower().startswith('z'):
		assert sigma is not None
		z = (xbar - mu) / (sigma / math.sqrt(n))
		if tail == 'greater':
			p = 1.0 - normal_cdf(z)
		elif tail == 'less':
			p = normal_cdf(z)
		else:
			p = 2.0 * min(normal_cdf(z), 1.0 - normal_cdf(z))
		return z, p

	raise ValueError(f"unknown method {method}")

# Simple assertion test for 'test_stat_and_p'
_z, _p = test_stat_and_p([3.9, 4.1, 4.2], 4.0, 0.6, "ztest", "two")
assert 0.0 <= _p <= 1.0

#============================================
def format_question_html(values: list, mu: float, sigma: float, method: str, tail: str) -> str:
	"""
	Build the Blackboard FIB_PLUS stem for microbial diversity testing.

	Args:
		values (list[float]): Shannon Index sample values.
		mu (float): Benchmark mean.
		sigma (float|None): Population sd for Z test, else None.
		method (str): 'ztest' or 'ttest'.
		tail (str): 'less', 'greater', or 'two'.

	Returns:
		str: HTML formatted question stem.
	"""
	# Build rows pairing site names with generated values
	# Randomly choose the same number of sites as values
	selected_sites = random.sample(DIVERSITY_SITES, len(values))
	# Pair sites with generated values, then sort alphabetically
	pairs = sorted(zip(selected_sites, values), key=lambda x: x[0])

	# Build an HTML table (for readability)
	table_html = "<table border='1' cellpadding='3' style='border-collapse:collapse;'>"
	table_html += "<tr><th style='text-align:center;'>Sample<br/>Location</th>"
	table_html += "<th style='text-align:center;'>2024<br/>Shannon<br/>Index</th></tr>"
	for site, v in pairs:
		table_html += f"<tr><td>{site}</td>"
		table_html += f"<td style='text-align:right;'>{v:.2f}</td></tr>"

	table_html += "</table>"

	# Format table-like text
	rows = "Sample Location\t2024 Shannon Index<br/>"
	for site, v in pairs:
		rows += f"{site},{v:.2f}<br/>"
	z_link = "https://docs.google.com/document/d/1mWpCqMxqU0O2G7r1P0JdpMOgKyJie8Qcy4vwvXuBVuk/edit"
	t_link = "https://docs.google.com/document/d/1V0dAHscKvN8H_X4AlbDEIaukAsHoKHEKjwz7jdbsR0w/edit"

	q = "<p><b>Busse Woods Microbial Diversity vs Benchmark</b></p>"
	if method.lower().startswith('z'):
		q += "<p style='color:#004d99;'><b>Z-Test Scenario</b></p>"
		q += "<p>Use a Z test. Population sd is known.</p>"
		q += f"<p>Fixed values: mu = {mu:.2f}, sigma = {sigma:.2f}.</p>"
		q += "<p>Alternative H1: diversity is different from the benchmark.</p>"
		q += "<p>Use a two tailed test.</p>"
		tutorial_link = z_link
	else:
		q += "<p style='color:#009900;'><b>T-Test Scenario</b></p>"
		q += "<p>Use a one sample t test. Population sd is unknown.</p>"
		q += f"<p>Fixed value: mu = {mu:.2f}. Estimate sd from the sample.</p>"
		q += "<p>Alternative H1: diversity is lower than the benchmark.</p>"
		q += "<p>Use a one tailed test with H1: mean &lt; mu.</p>"
		tutorial_link = t_link

	q += "<p>Sample Data Table:<br/>"
	q += "<em>Copy the table rows and use regular paste (Ctrl-V or &#8984;-V) into Google Sheets.</em></p>"
	q += table_html
	q += "<p>Alternate Copyable Format:<br/>"
	q += "<em>Copy this text and use "
	q += "<strong>Data &rarr; Split text to columns &rarr; Comma</strong> in Google Sheets.</em></p>"
	q += f"<p><span style='font-family: monospace; background-color:#eee;'>{rows}</span></p>"
	q += f"<p>Follow the workflow in the tutorial: <a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>.</p>"
	q += "<p>Enter the p value as a decimal between 0 and 1.</p>"
	return q

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	"""
	Create a complete formatted question for output.

	Args:
		N (int): Question number.
		method (str): 'ztest' or 'ttest'.

	Returns:
		str: A formatted Blackboard question string.
	"""
	mu = 4.0
	sigma = 0.6

	method = args.test_method
	if method == 'ztest':
		tail = 'two'
	else:
		tail = 'less'

	n = random.randint(12, 20)

	min_p, max_p = 0.05, 0.95
	max_tries = 200
	test_stat = 0.0
	p_value = 1.0
	tries = 0

	while not (min_p < p_value < max_p) and tries < max_tries:
		values = generate_diversity_values(n, mu, sigma, method)
		test_stat, p_value = test_stat_and_p(values, mu, sigma, method, tail)
		tries += 1

	assert min_p <= p_value <= max_p
	assert len(values) == n

	question_text = format_question_html(values, mu, sigma, method, tail)

	answer_float = p_value
	tolerance_float = round(max(0.001, 0.01 * answer_float), 4)

	complete_question = bptools.formatBB_NUM_Question(
		N,
		question_text,
		answer_float,
		tolerance_float,
		tol_message=False
	)

	return complete_question

#===========================================================
#===========================================================
def parse_arguments():
	"""
	Parse command-line arguments.

	Returns:
		argparse.Namespace: Parsed args.
	"""
	parser = bptools.make_arg_parser(
		description="Generate Busse Woods diversity questions."
	)
	test_group = parser.add_mutually_exclusive_group(required=False)
	test_group.add_argument(
		'-m', '--method', dest='test_method', type=str,
		choices=('ztest', 'ttest'),
		help='ztest uses sigma known; ttest uses sample sd'
	)
	test_group.add_argument(
		'-z', '--ztest', dest='test_method',
		action='store_const', const='ztest',
		help='Use Z test with known sigma=0.6 and two tailed H1'
	)
	test_group.add_argument(
		'-t', '--ttest', dest='test_method',
		action='store_const', const='ttest',
		help='Use one sample t test with H1 mean < 4.0'
	)
	parser.set_defaults(test_method='ztest')
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
def main():
	"""
	Generate and save microbial diversity questions.

	Workflow:
	1. Parse args.
	2. Create output filename from script name and args.
	3. Generate questions with write_question().
	4. Shuffle and trim to max_questions.
	5. Write all questions to an output file.
	6. Print status.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(args.test_method)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
if __name__ == '__main__':
	main()
