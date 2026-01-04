
import math
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
def make_chi_square_table() -> str:
	"""
	Create a Chi-Squared table with critical values.

	Returns
	-------
	str
		A string containing the HTML representation of the Chi-Squared table.
	"""

	# Initialize the maximum degree of freedom for the table
	max_df = 4

	# Initialize the probability values that will be used in the table
	p_values = [0.95, 0.90, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01]

	# Start building the HTML table with added CSS styles for better readability and design
	table = '<table style="border-collapse: collapse; border: 2px solid gray;">'

	# Set column widths for the table
	table += '<colgroup width="100"></colgroup>'
	for p in p_values:
		table += '<colgroup width="60"></colgroup>'

	# Add table title
	table += f"<tr><th align='center' colspan='{len(p_values)+1}' "
	table += "style='background-color: gainsboro; border: 1px solid gray; padding: 5px;'>"
	table += "Table of Chi-Squared (&chi;&sup2;) Critical Values</th></tr>"


	# Add row for Degrees of Freedom and Probability headers, bold font and different background color
	table += "<tr><th rowspan='2' align='center' style='background-color: #D3D3D3; "
	table += "font-weight: bold; border: 1px solid gray; padding: 5px;'>Degrees of Freedom</th> "
	table += f"<th align='center' colspan='{len(p_values)}' style='background-color: #D3D3D3; "
	table += "font-weight: bold; border: 1px solid gray; padding: 5px;'>Probability</th></tr>"

	# Add row for actual probability values, bold font and different background color
	table += "<tr>"
	for p in p_values:
		table += "<th align='center' style='background-color: #F0F0F0; font-weight: bold; "
		table += f"border: 1px solid gray; padding: 5px;'>{p:.2f}</th>"

	table += "</tr>"

	# Populate the table with chi-squared values
	for df in range(1, max_df + 1):
		# Alternate row colors between white and light tan
		if df % 2 == 1:
			color = "#FAFAD2"
		else:
			color = "#FFFFFF"

		table += f"<tr style='background-color: {color};'>"

		# Add degree of freedom value with bold font
		table += "<th align='center' style='background-color: #D3D3D3; font-weight: bold; "
		table += f"border: 1px solid gray; padding: 5px;'>{df}</th>"

		# Loop through each probability value to fill in chi-squared values
		for p in p_values:
			chisq = get_critical_value(p, df)
			table += "<td align='center' style='border: 1px solid gray; padding: 5px;'>"
			table += f"{chisq:.2f}</td>"

		table += "</tr>"

	# Finalize the table
	table += "</table>"

	# Return the HTML string
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
def create_data_table(stats_list: list, title: str = None) -> str:
	"""
	Create an HTML table from a list of statistics.

	Parameters
	----------
	stats_list : list
		List of lists containing the statistics for each phenotype.
	title : str, optional
		Title for the table.

	Returns
	-------
	str
		The HTML string representing the table.
	"""
	# Initialize the number of columns based on the length of the first element in stats_list.
	numcol = len(stats_list[0])

	# Initialize HTML table structure with border and styles.
	table = '<table style="border: 1px solid black; border-collapse: collapse; ">'

	# Add column widths.
	table += '<colgroup width="160"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
	table += '<colgroup width="80"></colgroup> '

	# Add title to the table if provided.
	if title is not None:
		table += f"<tr><th align='center' colspan='5' style='background-color: silver'>{title}</th></tr>"

	# Add headers for the table.
	table += "<tr>"
	table += "<th align='center' style='background-color: lightgray'>Phenotype</th> "
	table += "<th align='center' style='background-color: lightgray'>Expected</th> "
	table += "<th align='center' style='background-color: lightgray'>Observed</th> "
	table += "<th align='center' style='background-color: lightgray'>Calculation</th> "
	table += "<th align='center' style='background-color: lightgray'>Statistic</th> "
	table += "</tr>"

	# Loop through stats_list to populate table rows for each phenotype.
	phenotypes = ["Yellow Round (Y&ndash;R&ndash;)", "Yellow Wrinkled (Y&ndash;rr)", "Green Round (yyR&ndash;)", "Green Wrinkled (yyrr)"]
	for i, phenotype in enumerate(phenotypes):
		table += f"<tr><td>&nbsp;{phenotype}</td>"
		for j in range(numcol):
			stat = stats_list[i][j]
			table += f" <td align='center'>{stat}</td>"
		table += "</tr>"

	# Add the sum chi-squared statistic to the last row.
	table += f"<tr><td colspan='{numcol}' align='right' style='background-color: lightgray'>(sum) &chi;&sup2;&nbsp;=&nbsp;</td>"
	stat = stats_list[-1]
	table += f" <td align='center'>{stat}</td></tr>"

	# Close the HTML table tag.
	table += "</table>"

	# Return the finalized HTML table as a string.
	return table
