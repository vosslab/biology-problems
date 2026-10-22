
import math
import fractions
import random
from scipy.stats.distributions import chi2

#===============
#===============
def get_p_value(chisq: float, df: int) -> float:
	"""
	Get the p-value based on a given chi-squared value and degrees of freedom.

	Parameters
	----------
	chisq : float
		The chi-squared value.
	df : int
		The degrees of freedom.

	Returns
	-------
	float
		The p-value associated with the chi-squared value and degrees of freedom.
	"""

	# Calculate the p-value using chi2.sf from scipy.stats
	pvalue = chi2.sf(float(chisq), int(df))

	# Return the p-value as a float
	return float(pvalue)

# Simple assertion test for the function: 'get_p_value'
result = get_p_value(7.81472790325, 3)
#print(f"get_p_value={result}")
assert math.isclose(result, 0.0500, abs_tol=1e-9), f"Expected around 0.05, got {result}"

#===============
#===============
def get_critical_value(alpha_criterion: float, df: int) -> float:
	"""
	Get the chi-squared critical value based on a given alpha criterion and degrees of freedom.

	Parameters
	----------
	alpha_criterion : float
		The alpha criterion value.
	df : int
		The degrees of freedom.

	Returns
	-------
	float
		The chi-squared critical value.
	"""

	# Calculate the critical value using chi2.ppf from scipy.stats
	critical_value = chi2.ppf(1.0 - float(alpha_criterion), int(df))

	# Return the critical value as a float
	return float(critical_value)

# Simple assertion test for the function: 'get_critical_value'
result = get_critical_value(0.05, 3)
#print(f"get_critical_value={result}")
assert math.isclose(result, 7.81472790325, abs_tol=1e-9), f"Expected around 7.8147, got {result}"

def get_chi_square_result(final_chisq: float, df: int, alpha: float) -> str:
	# Fetch the critical value based on the significance level and degrees of freedom
	critical_value = get_critical_value(alpha, df)

	# Compare the final chi-square value to the critical value
	# Reject the null hypothesis if final_chisq is greater than the critical_value
	if final_chisq > critical_value:
		return 'reject_null'
	# Accept the null hypothesis if final_chisq is less than or equal to the critical_value
	elif final_chisq <= critical_value:
		return 'accept_null'

	# Return None if none of the conditions are met (though this is unlikely)
	return None

# Simple assertion test for the function: 'getChiSquareResult'
assert get_chi_square_result(10.0, 2, 0.05) == 'reject_null'
assert get_chi_square_result(3.0, 2, 0.05) == 'accept_null'


#===============
#===============
def make_chi_square_table(degrees_of_freedom: tuple = (1, 2, 3, 4),
		p_values: tuple = (0.95, 0.90, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01)) -> str:
	"""Render critical values for the requested degrees of freedom and tail probabilities."""
	headers = ["Degrees of freedom"] + [f"{p:.2f}" for p in p_values]
	rows = [[df] + [f"{get_critical_value(p, df):.2f}" for p in p_values]
		for df in degrees_of_freedom]
	table = render_table(headers, rows,
		"Chi-square critical values (probability in the right tail)")
	return table


#===================
#===================
def create_observed_progeny(N: int = 160, ratio: str = "9:2:4:1") -> list:
	"""
	create_observed_progeny - Simulates the observed progeny count based on a given genetic ratio.

	Parameters
	----------
	N: int
		Number of progenies to simulate (Default is 160).
	ratio: str
		The genetic ratio in string format separated by colons (Default is "9:2:4:1").

	Returns
	-------
	list
		Returns a list of observed progeny counts.
	"""

	# Split the ratio string by colon to get the individual bin ratios.
	bins = ratio.split(':')
	floats = []
	# Convert string ratios to float for calculations.
	for b in bins:
		floats.append(float(b))
	# Calculate the total sum of ratios.
	total = sum(floats)

	# Calculate the cumulative probabilities for each bin.
	probs = []
	sumprob = 0
	for f in floats:
		sumprob += f / total
		probs.append(sumprob)

	# Initialize a dictionary to store the count of progenies falling into each bin.
	count_dict = {}
	# Generate N random numbers and map them to bins based on calculated probabilities.
	for i in range(N):
		r = random.random()
		for j in range(len(probs)):
			if r < probs[j]:
				count_dict[j] = count_dict.get(j, 0) + 1
				break

	# Create a list of observed counts from the dictionary.
	count_list = []
	for j in range(len(probs)):
		count_list.append(count_dict.get(j, 0))

	return count_list

# Simple assertion test for the function 'createObservedProgeny'.
# Note: The test might vary due to the random nature of the function.
result = create_observed_progeny(160, "9:2:4:1")
assert isinstance(result, list) and len(result) == 4


#===============
#===============
PEA_PHENOTYPES = ["Yellow Round (Y&ndash;R&ndash;)", "Yellow Wrinkled (Y&ndash;rr)",
	"Green Round (yyR&ndash;)", "Green Wrinkled (yyrr)"]


def render_table(headers: list, rows: list, title: str = None) -> str:
	"""Render supplied cells verbatim, including intentional errors and blank work."""
	style = "padding: 6px 8px; border-bottom: 1px solid #b8b8b8; text-align: right;"
	text = '<table style="border-collapse: collapse; color: #202020; background: #ffffff;">'
	if title is not None:
		text += f'<caption style="text-align: left; font-weight: bold; padding: 6px;">{title}</caption>'
	text += '<thead><tr style="background: #e3e8ed;">'
	for index, header in enumerate(headers):
		alignment = "text-align: left;" if index == 0 else ""
		text += f'<th scope="col" style="{style} {alignment}">{header}</th>'
	text += '</tr></thead><tbody>'
	for index, row in enumerate(rows):
		if len(row) != len(headers):
			raise ValueError("Each table row must have one cell per header")
		background = "#ffffff" if index % 2 == 0 else "#f2f5f7"
		text += f'<tr style="background: {background};">'
		text += f'<th scope="row" style="{style} text-align: left; font-weight: normal;">{row[0]}</th>'
		for value in row[1:]:
			text += f'<td style="{style}">{value}</td>'
		text += '</tr>'
	text += '</tbody></table>'
	return text


def create_worked_table(labels: list, observed: list, expected: list) -> str:
	"""Calculate correct chi-square work for any number of labeled categories.

	Use render_table or create_data_table for supplied or intentionally wrong work.
	Fractions retain exact contributions; decimals are rounded only for display.
	"""
	if not labels or len(labels) != len(observed) or len(labels) != len(expected):
		raise ValueError("Labels, observed counts, and expected counts must have equal nonzero lengths")
	rows = []
	terms = []
	observed_total = fractions.Fraction()
	expected_total = fractions.Fraction()
	for label, obs, exp in zip(labels, observed, expected):
		obs = fractions.Fraction(str(obs))
		exp = fractions.Fraction(str(exp))
		if obs < 0 or exp <= 0:
			raise ValueError("Observed counts must be nonnegative and expected counts positive")
		observed_total += obs
		expected_total += exp
		difference = obs - exp
		term = difference ** 2 / exp
		terms.append(term)
		numerator = str(difference ** 2)
		denominator = str(exp)
		if (difference ** 2).denominator != 1:
			numerator = f"({numerator})"
		if exp.denominator != 1:
			denominator = f"({denominator})"
		rows.append([label, str(obs), str(exp), str(difference), str(difference ** 2),
			f"{numerator} / {denominator} &asymp; {float(term):.2f}"])
	total = sum(terms)
	rows.append(["<strong>Total</strong>", str(observed_total), str(expected_total),
		"&mdash;", "&mdash;", f"<strong>&chi;<sup>2</sup> = {total} &asymp; {float(total):.2f}</strong>"])
	headers = ["Category", "Observed", "Expected", "Observed &minus; expected",
		"(Observed &minus; expected)<sup>2</sup>",
		"(Observed &minus; expected)<sup>2</sup> / expected"]
	text = render_table(headers, rows, "Chi-square calculation")
	return text


def create_data_table(stats_list: list, title: str = None, labels: list = None,
		headers: list = None) -> str:
	"""Display precomputed work without changing its values or supplied total.

	stats_list contains category rows followed by the total. Callers supply category
	labels and may override columns for other data types or calculation layouts.
	"""
	category_rows = stats_list[:-1]
	if labels is None:
		labels = [f"Category {index + 1}" for index in range(len(category_rows))]
	if len(labels) != len(category_rows):
		raise ValueError("Each category row needs a label")
	if headers is None:
		headers = ["Category", "Expected", "Observed", "Calculation", "Statistic"]
	rows = [[label] + list(values) for label, values in zip(labels, category_rows)]
	rows.append(["<strong>Total &chi;<sup>2</sup></strong>"]
		+ ["&mdash;"] * (len(headers) - 2) + [stats_list[-1]])
	text = render_table(headers, rows, title)
	return text
