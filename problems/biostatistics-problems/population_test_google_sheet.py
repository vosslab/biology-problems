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
	if x < 0:
		return 1.0 - student_t_cdf(-x, df)
	# integrate from 0 to x
	n = 2000  # even number for Simpson
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
	return 0.5 + area  # symmetry: integral 0..x plus 0.5 at 0


#============================================
def one_tailed_pvalue(weights: list[float], mu: float, sigma: float | None, test_method: str) -> tuple[float, float]:
	"""
	Compute one-tailed p-value for H1: mean > mu.

	Args:
		weights (list[float]): sample data
		mu (float): population mean
		sigma (float|None): population sd if known (Z); None for T
		test_method (str): method to use one-sample t-test

	Returns:
		tuple[float, float]: (statistic, p_one_tailed)
	"""
	n = len(weights)
	xbar = statistics.fmean(weights)

	if test_method.lower().startswith('t'):
		s = statistics.stdev(weights)  # sample sd with ddof=1
		t = (xbar - mu) / (s / math.sqrt(n))
		df = n - 1
		p = 1.0 - student_t_cdf(t, df)
		return t, p
	elif test_method.lower().startswith('z'):
		assert sigma is not None
		z = (xbar - mu) / (sigma / math.sqrt(n))
		p = 1.0 - normal_cdf(z)
		return z, p
	else:
		raise ValueError(f"unknown method {test_method}")
# Simple assertion test for the function: 'compute_one_tailed_pvalue'
_test = [7.6, 7.7, 7.8, 7.9, 8.0, 7.6, 7.7, 7.8, 7.9, 8.0]
_z, _p = one_tailed_pvalue(_test, 7.5, 1.5, "ttest")
assert 0.0 <= _p <= 1.0

#============================================
def generate_baby_weights(n: int, mu: float = 7.5, sigma: float = 1.5) -> list[float]:
	"""
	Generate n baby weights in pounds with one decimal place, sampled around
	mu plus a small positive shift so xbar > mu.

	Args:
		n (int): Sample size.
		mu (float): Population mean.
		sigma (float): Population standard deviation.

	Returns:
		list[float]: List of n weights rounded to one decimal place.
	"""
	# shift keeps the one tailed direction consistent
	shift = round(random.uniform(0.10, 0.60), 2)
	target_mu = mu + shift

	values = []
	for _ in range(n):
		# Box Muller like sampling via Gaussian from random
		v = random.gauss(target_mu, sigma)
		# keep weights in a reasonable newborn range
		v = max(4.0, min(12.0, v))
		# one decimal place as in typical clinical recording
		values.append(round(v, 1))

	# ensure at least slight elevation of mean
	if statistics.mean(values) <= mu:
		# nudge the largest value up by 0.2 if needed
		i = max(range(n), key=lambda k: values[k])
		values[i] = round(min(12.0, values[i] + 0.2), 1)

	# simple assertion tests
	assert len(values) == n
	assert min(values) >= 4.0 and max(values) <= 12.0

	return values

#============================================
def format_question_html(weights: list[float], mu: float, sigma: float | None, test_method: str) -> str:
	"""
	Build the Blackboard FIB_PLUS stem. Students compute a one tailed p value.

	Args:
		weights (list[float]): Baby weights in pounds.

	Returns:
		str: HTML formatted question stem with a single blank [PVALUE].
	"""
	rows = "<br/>".join(f"{w:.1f}" for w in weights)
	ztest_link = "https://docs.google.com/document/d/1ZOLIw-JlNA6Mry1w0t5I5Ffgi7RMiBCSr7VtyNgsdt0/edit"
	ttest_link = "https://docs.google.com/document/d/1lh3EWl4gnyT0dq0rgYzjzC6J1No4zKP2gi5eY3N5uv0/edit"

	q = ""
	q += "<p><b>Joe's Hospital of Fried Foods vs National Average</b></p>"
	if test_method.lower().startswith('z'):
		q += "<p>Use a one tailed Z test for H1: mu_hospital > mu.</p>"
		q += f"<p>Fixed population values: &mu; = {mu} lbs, &sigma; = {sigma} lbs.</p>"
		tutorial_link = ztest_link
	elif test_method.lower().startswith('t'):
		q += "<p>Use a one tailed one sample t test for H1: mu_hospital > mu.</p>"
		q += f"<p>Fixed population values: &mu; = {mu} lbs, Population sd is unknown.</p>"
		tutorial_link = ttest_link
	q += "<p>Sample weights (lbs), enter into a single column in Google Sheets:</p>"
	q += f"<p><span style='font-family: monospace; background-color:#eee;'>{rows}</span></p>"
	q += "<p>Compute the one-tailed p-value using the tutorial workflow from last week: "
	q += f"<a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>.</p>"
	q += "<p>Enter your result as a decimal between 0 and 1 (for example, 0.084, not 8.4%).</p>"
	return q

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# fixed population values
	mu = 7.5
	sigma = 1.5

	# sample size bounded by sheet capacity
	n = random.randint(25, 39)

	# regenerate weights until p is in target interval
	min_p, max_p = 0.05, 0.95
	max_tries = 200
	test_stat = 0.0
	p_value = 1.0
	tries = 0
	mean = -1

	while (not (min_p < p_value < max_p) or mean <= mu) and tries < max_tries:
		weights = generate_baby_weights(n, mu, sigma)
		mean = statistics.fmean(weights)
		if mean < mu:
			continue
		test_stat, p_value = one_tailed_pvalue(weights, mu, sigma, args.test_method)
		tries += 1

	# simple sanity checks
	assert min_p <= p_value <= max_p
	assert len(weights) == n
	assert statistics.fmean(weights) > mu

	question_text = format_question_html(weights, mu, sigma, args.test_method)

	answer_float = p_value
	#tolerance range of 1%
	tolerance_float = round(max(0.001, 0.01 * answer_float), 4)

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_NUM_Question(N, question_text, answer_float,
										tolerance_float, tol_message=False)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser(description="Generate questions.")
	test_group = parser.add_mutually_exclusive_group(required=False)
	# Add an option to manually set the question format
	test_group.add_argument(
		'-m', '--method', dest='test_method', type=str,
		choices=('ztest', 'ttest'),
		help='Set the question test method: ztest (Z test) or ttest (T test)'
	)
	test_group.add_argument(
		'-z', '--ztest', dest='test_method',
		action='store_const', const='ztest',
		help='Use Z test with known sigma'
	)

	test_group.add_argument(
		'-t', '--ttest', dest='test_method',
		action='store_const', const='ttest',
		help='Use one sample t test (sigma unknown)'
	)
	parser.set_defaults(test_method='ztest')
	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using write_question().
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile(None, args.test_method)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
