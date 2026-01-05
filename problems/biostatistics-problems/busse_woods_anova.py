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

YEARS = [1994, 2004, 2009, 2014, 2024]


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
	CDF of F(d1, d2) via Simpson integration.
	Accurate for typical df.
	"""
	if x <= 0.0:
		return 0.0
	n = 2000
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

# simple bounds check
assert 0.0 <= f_cdf(1.0, 4, 50) <= 1.0

#============================================
def generate_shannon_group(
	n: int,
	target_mu: float,
	sigma: float,
	bounds: tuple[float, float] = (1.0, 6.5)
) -> list[float]:
	"""
	Generate n Shannon Index values around target_mu.
	"""
	low, high = bounds
	values: list[float] = []
	i = 0
	while i < n:
		v = random.gauss(target_mu, sigma)
		v = max(low, min(high, v))
		values.append(round(v, 2))
		i += 1
	if len(set(values)) == 1:
		j = random.randrange(n)
		step = 0.02 if values[j] <= high - 0.02 else -0.02
		values[j] = round(values[j] + step, 2)
	assert len(values) == n
	assert low <= min(values) <= max(values) <= high
	assert statistics.stdev(values) > 1e-6
	return values

#============================================
def anova_one_way(groups: list[list[float]]) -> tuple[float, int, int, float]:
	"""
	One way ANOVA across k groups.
	Returns (F, df_between, df_within, p_value).
	"""
	k = len(groups)
	ns = [len(g) for g in groups]
	assert all(n > 1 for n in ns)
	N = sum(ns)

	means = [statistics.fmean(g) for g in groups]
	vars_ = [statistics.variance(g) for g in groups]
	grand_mean = sum(m * n for m, n in zip(means, ns)) / N

	ss_between = sum(n * (m - grand_mean) * (m - grand_mean)
		for m, n in zip(means, ns))
	ss_within = sum((n - 1) * s2 for n, s2 in zip(ns, vars_))

	df_between = k - 1
	df_within = N - k
	assert df_between > 0 and df_within > 0

	ms_between = ss_between / df_between
	ms_within = ss_within / df_within
	F = ms_between / ms_within

	p = 1.0 - f_cdf(F, df_between, df_within)
	assert 0.0 <= p <= 1.0
	return F, df_between, df_within, p

# simple assertion: equal means should give small F on average
_test = [generate_shannon_group(12, 4.0, 0.5) for _ in range(5)]
_F, _dfb, _dfw, _p = anova_one_way(_test)
assert 0.0 <= _p <= 1.0

def format_question_html(
	by_year: dict[int, list[float | None]],
	selected_sites: list[str],
	p_value: float
) -> str:
	"""
	Render a visual table and CSV block. Cells with None print as blanks.
	"""
	max_n = len(selected_sites)
	years = [1994, 2004, 2009, 2014, 2024]

	# visual table
	table_html = (
		"<table border='1' cellpadding='3' style='border-collapse:collapse;'>"
		"<tr>"
		"<th style='text-align:center;'>Sample<br/>Location</th>"
		"<th style='text-align:center;'>1994<br/>Shannon<br/>Index</th>"
		"<th style='text-align:center;'>2004<br/>Shannon<br/>Index</th>"
		"<th style='text-align:center;'>2009<br/>Shannon<br/>Index</th>"
		"<th style='text-align:center;'>2014<br/>Shannon<br/>Index</th>"
		"<th style='text-align:center;'>2024<br/>Shannon<br/>Index</th>"
		"</tr>"
	)
	i = 0
	while i < max_n:
		site = selected_sites[i]
		row_cells = []
		j = 0
		while j < len(years):
			v = by_year[years[j]][i]
			row_cells.append("" if v is None else f"{v:.2f}")
			j += 1
		table_html += (
			f"<tr><td>{site}</td>"
			f"<td style='text-align:right;'>{row_cells[0]}</td>"
			f"<td style='text-align:right;'>{row_cells[1]}</td>"
			f"<td style='text-align:right;'>{row_cells[2]}</td>"
			f"<td style='text-align:right;'>{row_cells[3]}</td>"
			f"<td style='text-align:right;'>{row_cells[4]}</td></tr>"
		)
		i += 1
	table_html += "</table>"

	# CSV block (empty fields preserved)
	csv_rows = ("Sample Location,1994 Shannon Index,2004 Shannon Index,"
		"2009 Shannon Index,2014 Shannon Index,2024 Shannon Index<br/>")
	i = 0
	while i < max_n:
		site = selected_sites[i]
		cells = []
		j = 0
		while j < len(years):
			v = by_year[years[j]][i]
			cells.append("" if v is None else f"{v:.2f}")
			j += 1
		csv_rows += f"{site},{cells[0]},{cells[1]},{cells[2]},{cells[3]},{cells[4]}<br/>"
		i += 1

	q = "<p><b>ANOVA of Shannon Diversity: 1994, 2004, 2009, 2014, 2024</b></p>"
	q += "<p>Compare microbial diversity across five years using one way ANOVA.</p>"

	q += "<p>Sample Data Table:<br/>"
	q += "<em>Copy table rows and use regular paste (Ctrl-V or &#8984;-V) into Google Sheets.</em></p>"
	q += table_html

	q += "<p>Alternate Copyable Format:<br/>"
	q += "<em>Copy this text and use "
	q += "<strong>Data &rarr; Split text to columns &rarr; Comma</strong> in Google Sheets.</em></p>"
	q += f"<p><span style='font-family: monospace; background-color:#eee;'>{csv_rows}</span></p>"

	q += "<p>Enter the ANOVA p value as a decimal between 0 and 1.</p>"

	tutorial_link = "https://docs.google.com/document/d/1xkWsWENaOLRHUk6MO50anhL4DEbjmK8_xBmj22k3tts/edit"
	q += f"<p>Workflow: <a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>.</p>"

	return q

def _write_one_question(N: int) -> str:
	"""
	Create one Blackboard numeric question row for ANOVA across 5 years
	with cumulative sampling: once a site appears, it persists in all later years.
	"""
	# cumulative sample sizes (older years smaller)
	max_size = len(DIVERSITY_SITES)
	n24 = max_size
	n14 = n24 - random.randint(2, 5)
	n09 = n14 - random.randint(2, 5)
	n04 = n09 - random.randint(2, 5)
	n94 = n04 - random.randint(2, 5)
	max_n = n24

	# choose site order, then cohorts grow over time
	order_sites = random.sample(DIVERSITY_SITES, max_n)
	cohort94 = order_sites[:n94]
	cohort04 = order_sites[:n04]  # includes 1994
	cohort09 = order_sites[:n09]  # includes 1994, 2004
	cohort14 = order_sites[:n14]
	cohort24 = order_sites[:n24]

	# trend and variance pattern
	mu_center = 4.0
	amp = random.uniform(0.25, 0.55)
	mus = [
		mu_center + 0.40 * amp,  # 1994
		mu_center + 0.25 * amp,  # 2004
		mu_center + 0.15 * amp,  # 2009
		mu_center + 0.05 * amp,  # 2014
		mu_center - 0.20 * amp,  # 2024
	]
	base_sigma = 0.50
	sigmas = [base_sigma * x for x in (1.10, 1.05, 1.00, 0.95, 0.90)]

	# generate per-year values and map to sites
	map1994 = dict(zip(cohort94, generate_shannon_group(n94, mus[0], sigmas[0])))
	map2004 = dict(zip(cohort04, generate_shannon_group(n04, mus[1], sigmas[1])))
	map2009 = dict(zip(cohort09, generate_shannon_group(n09, mus[2], sigmas[2])))
	map2014 = dict(zip(cohort14, generate_shannon_group(n14, mus[3], sigmas[3])))
	map2024 = dict(zip(cohort24, generate_shannon_group(n24, mus[4], sigmas[4])))

	# ANOVA on actual groups (unequal n)
	F, dfb, dfw, p_value = anova_one_way([
		list(map1994.values()),
		list(map2004.values()),
		list(map2009.values()),
		list(map2014.values()),
		list(map2024.values()),
	])
	min_p, max_p = 0.05, 0.95
	if not (min_p <= p_value <= max_p):
		return None

	# display lists aligned to alphabetical site rows
	selected_sites = sorted(order_sites)

	def col_for_year(map_y: dict[str, float]) -> list[float | None]:
		# blanks only for years BEFORE a site was added
		return [map_y.get(site) for site in selected_sites]

	by_year_display = {
		1994: col_for_year(map1994),
		2004: col_for_year(map2004),
		2009: col_for_year(map2009),
		2014: col_for_year(map2014),
		2024: col_for_year(map2024),
	}

	question_text = format_question_html(by_year_display, selected_sites, p_value)

	answer_float = p_value
	tolerance_float = round(max(0.001, 0.01 * answer_float), 4)

	complete_question = bptools.formatBB_NUM_Question(
		N, question_text, answer_float, tolerance_float, tol_message=False
	)
	return complete_question

#============================================
def write_question(N: int, args) -> str:
	return _write_one_question(N)

#============================================
def parse_arguments():
	"""
	Parse command line arguments.
	"""
	parser = bptools.make_arg_parser(description="Generate ANOVA questions (5 years).")
	args = parser.parse_args()
	return args

#============================================
def main():
	"""
	Generate and save a bank of ANOVA numeric questions.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(None, "anova-5year")
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
if __name__ == '__main__':
	main()
