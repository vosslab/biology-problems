#!/usr/bin/env python3

import os
import copy
import random
import argparse

import bptools
import chisquarelib

### types of errors
# 0 * divide by the observed instead of expected
# 1 * square the bottom number
# 2 * square the bottom observed number
# 3 * forget to square the numbers before division
# 4 * use the wrong null hypothesis
# 5 * wrong degrees of freedom 3 vs 4
# 6 * use chi-sq value being less critical value -> reject
# 7 * wrong degrees of freedom 3 vs 2
# * use chi-sq value being less than 0.05 to reject
# * take a p > 0.05 as reject

error2choice = {
	0: 0,
	1: 0,
	2: 0,
	3: 1,
	4: 3,
	5: 4,
	6: 2,
	7: 4,
	8: 2,
}

choices = [
	'The wrong numbers in the calculation were used for division, you need to divide by a different number.',
	'The numbers in the calculation have to be squared and they are not squared.',
	'The wrong rejection criteria was used. the significance level, &alpha; is wrong.',
	'The expected progeny for the null hypothesis is incorrect. They did the calculation wrong. ',
	'The degrees of freedom is wrong, it should be a different value.',
]

#===================
#===================
def divideByObservedError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = chisquarelib.create_observed_progeny()
	expected = [90,30,30,10]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		obs = observed[j]
		exp = expected[j]
		row.append(exp)
		row.append(obs)
		chirow = (obs-exp)**2/float(obs)
		calc = "<sup>({0}-{1})&sup2;</sup>&frasl;&nbsp;<sub>{2}</sub>".format(obs, exp, obs)
		row.append(calc)
		chistr = "{0:.3f}".format(chirow)
		row.append(chistr)
		chisq += chirow
		stats_list.append(row)
	chistr = "{0:.3f}".format(chisq)
	stats_list.append(chistr)
	return stats_list

#===================
#===================
def divideByObservedAndSquareError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = chisquarelib.create_observed_progeny()
	expected = [90,30,30,10]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		obs = observed[j]
		exp = expected[j]
		row.append(exp)
		row.append(obs)
		chirow = (obs-exp)**2/float(obs**2)
		calc = "<sup>({0}-{1})&sup2;</sup>&frasl;&nbsp;<sub>{2}&sup2;</sub>".format(obs, exp, obs)
		row.append(calc)
		chistr = "{0:.3f}".format(chirow)
		row.append(chistr)
		chisq += chirow
		stats_list.append(row)
	chistr = "{0:.3f}".format(chisq)
	stats_list.append(chistr)
	return stats_list

#===================
#===================
def divideBySquareError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = chisquarelib.create_observed_progeny()
	expected = [90,30,30,10]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		obs = observed[j]
		exp = expected[j]
		row.append(exp)
		row.append(obs)
		chirow = (obs-exp)**2/float(exp**2)
		calc = "<sup>({0}-{1})&sup2;</sup>&frasl;&nbsp;<sub>{2}&sup2;</sub>".format(obs, exp, exp)
		row.append(calc)
		chistr = "{0:.3f}".format(chirow)
		row.append(chistr)
		chisq += chirow
		stats_list.append(row)
	chistr = "{0:.3f}".format(chisq)
	stats_list.append(chistr)
	return stats_list

#===================
#===================
def noSquareError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = chisquarelib.create_observed_progeny()
	expected = [90,30,30,10]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		obs = observed[j]
		exp = expected[j]
		row.append(exp)
		row.append(obs)
		chirow = (obs-exp)/float(exp)
		calc = "<sup>({0}-{1})</sup>&frasl;&nbsp;<sub>{2}</sub>".format(obs, exp, exp)
		row.append(calc)
		chistr = "{0:.3f}".format(chirow)
		row.append(chistr)
		chisq += chirow
		stats_list.append(row)
	chistr = "{0:.3f}".format(chisq)
	stats_list.append(chistr)
	return stats_list

#===================
#===================
def normalGoodStats():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = chisquarelib.create_observed_progeny()
	expected = [90,30,30,10]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		obs = observed[j]
		exp = expected[j]
		row.append(exp)
		row.append(obs)
		chirow = (obs-exp)**2/float(exp)
		calc = "<sup>({0}-{1})&sup2;</sup>&frasl;&nbsp;<sub>{2}</sub>".format(obs, exp, exp)
		row.append(calc)
		chistr = "{0:.3f}".format(chirow)
		row.append(chistr)
		chisq += chirow
		stats_list.append(row)
	chistr = "{0:.3f}".format(chisq)
	stats_list.append(chistr)
	return stats_list

#===================
#===================
def wrongNullHypothesis():
	observed = [90]
	while observed[0] >= 70 or observed[3] <= 20:
		observed = chisquarelib.create_observed_progeny(ratio="7:5:3:2")
	expected = [40,40,40,40]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		obs = observed[j]
		exp = expected[j]
		row.append(exp)
		row.append(obs)
		chirow = (obs-exp)**2/float(exp)
		calc = "<sup>({0}-{1})&sup2;</sup>&frasl;&nbsp;<sub>{2}</sub>".format(obs, exp, exp)
		row.append(calc)
		chistr = "{0:.3f}".format(chirow)
		row.append(chistr)
		chisq += chirow
		stats_list.append(row)
	chistr = "{0:.3f}".format(chisq)
	stats_list.append(chistr)
	return stats_list

#===================
#===================
def chiSquareResults(chisq, critical_value, flip):
	if flip is False:
		if chisq > critical_value:
			results = ("greater", "been rejected")
		elif chisq <= critical_value:
			results = ("less", "failed to be rejected")
	else:
		# this is WRONG
		if chisq > critical_value:
			results = ("greater", "failed to be rejected")
		elif chisq <= critical_value:
			results = ("less", "been rejected")
	return results

#===================
#===================
def questionContent(chisq: float, df: int=3, alpha: float=0.05, flip: bool=False) -> str:
	"""
	Generate a question based on chi-squared test results.

	Parameters
	----------
	chisq : float
		The chi-squared test value.
	df : int, optional
		The degrees of freedom, by default 3.
	alpha : float, optional
		The level of significance, by default 0.05.
	flip : bool, optional
		Flip the result, by default False.

	Returns
	-------
	str
		A question string containing the chi-squared test results.
	"""

	# pvalue = get_p_value(chisq, df)
	critical_value = chisquarelib.get_critical_value(alpha, df)

	# Initialize the question string
	question = ""

	# Start building the first part of the question string
	# Now using f-strings for string formatting
	question += "<p>The final result gives the chi-squared (&chi;&sup2;) test value of "
	question += f"{chisq:.2f} with {df} degrees of freedom. "

	# Append information about the critical value and significance level
	question += "Consulting the Table of &chi;&sup2; Critical Values and a level of significance &alpha;="
	question += f"{alpha:.2f}, we obtain a critical value of {critical_value:.2f}.</p>"


	#keep in case I want to change question in future
	#question += "They calculated a p-value of {2:.3f} ({3:.1f}%). ".format(chisq, df, pvalue, pvalue*100)
	#question += "Since the p-value was {0} than the level of significance &alpha;=0.05 (5%), the null hypothesis was {1}.</p>".format("less", "rejected")

	# Debugging print statements for the chi-squared and critical values
	print(f"chi_square     = {chisq:.3f}")
	print(f"critical_value = {critical_value:.3f}")

	# Get the result string of the chi-squared test based on the test value and critical value
	results = chiSquareResults(chisq, critical_value, flip)

	# Build the last part of the question string based on the results of the chi-squared test
	# Complete the question string with chi-squared test results
	question += f"<p>Since the chi-squared value of {chisq:.2f} is {results[0]} than the "
	question += f"critical value of {critical_value:.2f}, the null hypothesis has {results[1].upper()}.</p>"

	# Separate different sections of the question
	question += "<hr/> "

	# Add a scenario involving a lab partner
	question += "<p>Your lab partner completed a chi-squared (&chi;&sup2;) test on your lab data (above) "
	question += "for the F<sub>2</sub> generation in a standard dihybrid cross. The goal was to verify if "
	question += "the observed results matched the expected phenotype ratios.</p>"
	question += "<p>However, it appears they made an error. <strong>What did they do wrong?</strong></p>"

	return question


### types of errors
# 0 * divide by the observed instead of expected
# 1 * square the bottom number
# 2 * square the bottom observed number
# 3 * forget to square the numbers before division
# 4 * use the wrong null hypothesis
# 5 * wrong degrees of freedom 3 vs 4
# * use chi-sq value being less than 0.05 to reject
# * take a p > 0.05 as reject

#===================
#===================
def makeQuestion(error_type):

	if error_type == 0:
		stats_list = divideByObservedError()
	elif error_type == 1:
		stats_list = divideBySquareError()
	elif error_type == 2:
		stats_list = divideByObservedAndSquareError()
	elif error_type == 3:
		stats_list = noSquareError()
	elif error_type == 4:
		stats_list = wrongNullHypothesis()
	else:
		stats_list = normalGoodStats()

	if error_type == 5:
		df = 4
	elif error_type == 7:
		df = 2
	else:
		df = 3

	if error_type == 6:
		flip = True
	else:
		flip = False

	if error_type == 8:
		alpha = 0.5
	else:
		alpha = 0.05

	chisq = float(stats_list[-1])
	table1 = chisquarelib.create_data_table(stats_list)
	chi_square_table = chisquarelib.make_chi_square_table()
	question = questionContent(chisq, df, alpha, flip)
	complete_question = chi_square_table+"<br/>"+table1+"<br/>"+question

	return complete_question

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	parser = argparse.ArgumentParser(description='Chi Square Question')
	parser.add_argument('-d', '--duplicate-runs', type=int, dest='duplicate_runs',
		help='number of questions to create', default=199)
	args = parser.parse_args()

	letters = "ABCDEFGHI"
	max_error_types = len(error2choice)
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	while N < args.duplicate_runs:
		error_type = random.randint(0, max_error_types-1)
		complete_question = makeQuestion(error_type)
		answer_index = error2choice[error_type]
		answer = choices[answer_index]
		choices_list_copy = copy.copy(choices)
		random.shuffle(choices_list_copy)
		N += 1
		bbformat = bptools.formatBB_MC_Question(N, complete_question, choices_list_copy, answer)
		f.write(bbformat)
	bptools.print_histogram()


#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
