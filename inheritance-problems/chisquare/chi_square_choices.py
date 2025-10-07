#!/usr/bin/env python3

import os
import sys
import random
import argparse

import bptools
import chisquarelib


### types of errors
# show 3 tables of chi square calculations
# - table 1 the real answer
# - table 2 divide by the observed
# - table 3 random choice of
# - - divide by observed squared
# - - forget to square the top divide by observed squared
# - - forget to square the top divide by observed
# student chooses which one is correct, and decides whether or not to reject the null.

#the table numbering answer choice is off

#print("There is a problem with table numbering")
#sys.exit(1)

error_types = {
	0: 'divide by observed squared',
	1: 'forget to square the top divide by observed squared',
	2: 'forget to square the top divide by observed',
}

accept_str = '<span style="color: #009900;"><strong>FAIL to REJECT</strong></span>' #GREEN
reject_str = '<span style="color: #e60000;"><strong>REJECT</strong></span>' #RED
tables_list = [
		'<span style="color: #e69100;"><strong>Table 1</strong></span>', #LIGHT ORANGE
		'<span style="color: #004d99;"><strong>Table 2</strong></span>', #NAVY BLUE
		'<span style="color: #b30077;"><strong>Table 3</strong></span>', #MAGENTA
	]


choices_list = [
	f'{tables_list[0]} with &chi;&sup2; = XXXX is correct and we {reject_str} the null hypothesis',
	f'{tables_list[1]} with &chi;&sup2; = XXXX is correct and we {reject_str} the null hypothesis',
	f'{tables_list[2]} with &chi;&sup2; = XXXX is correct and we {reject_str} the null hypothesis',

	f'{tables_list[0]} with &chi;&sup2; = XXXX is correct and we {accept_str} the null hypothesis',
	f'{tables_list[1]} with &chi;&sup2; = XXXX is correct and we {accept_str} the null hypothesis',
	f'{tables_list[2]} with &chi;&sup2; = XXXX is correct and we {accept_str} the null hypothesis',
]



#===================
#===================
def createObservedProgeny(N=160, ratio="9:2:4:1"):
	#female lay 100 eggs per day
	bins = ratio.split(':')
	floats = []
	for b in bins:
		floats.append(float(b))
	total = sum(floats)
	#print(floats)
	probs = []
	sumprob = 0
	for f in floats:
		sumprob += f/total
		probs.append(sumprob)
	#print(probs)
	count_dict = {}
	for i in range(N):
		r = random.random()
		for j in range(len(probs)):
			if r < probs[j]:
				count_dict[j] = count_dict.get(j, 0) + 1
				break
	#print(count_dict)
	count_list = []
	for j in range(len(probs)):
		count_list.append(count_dict.get(j, 0))
	#print(count_list)
	return count_list

#===================
#===================
def divideByObservedError(ratio, observed=None):
	if observed is None:
		observed = [90]
		while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
			observed = createObservedProgeny(ratio=ratio)
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
def divideByObservedAndSquareError(ratio, observed=None):
	if observed is None:
		observed = [90]
		while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
			observed = createObservedProgeny(ratio=ratio)
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
def noSquareError(ratio, observed=None):
	if observed is None:
		observed = [90]
		while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
			observed = createObservedProgeny(ratio=ratio)
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
def normalGoodStats(ratio, observed=None):
	if observed is None:
		observed = [90]
		while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
			observed = createObservedProgeny(ratio=ratio)
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
def questionContent():
	question = ''
	question += "<p>Your lab partner is trying again (eye roll) and did another a chi-squared (&chi;&sup2;) test "
	question += "on the F<sub>2</sub> generation in a dihybid cross based on your lab data (above). "
	question += "They wanted to know if the results confirm the expected phenotype ratios.</p>"

	question += "<p>You helped them set up the null hypothesis, so you know that part is correct, "
	question += "but they got confused and were unsure about how to calculate the "
	question += "chi-squared (&chi;&sup2;) value. So much so that "
	question += "they did it three (3) different ways.</p> "

	question += "<p>Before you ask your instructor for a new lab partner, "
	question += "<b>tell them which table is correct AND whether they can reject or fail to reject "
	question += "the null hypothesis</b> using the information provided.</p> "
	return question

"""bad_ratios = [
	'8:2:4:2',
	'10:3:2:1',
	'9:5:1:1',
	'7:3:3:3',
	'4:4:4:4',
	]"""

bad_ratios = [
	'8:2:4:2',
	]
#===================
#===================
#===================
def makeQuestion(error_type: int, desired_result: str) -> tuple:
	"""
	Numpydoc Style:
	Create a chi-square question with specific error types and results.

	Parameters
	----------
	error_type : int
		Specifies the type of error to exclude from the wrong answers.
		0: 'divide by observed squared',
		1: 'forget to square the top divide by observed squared',
		2: 'forget to square the top divide by observed',
	desired_result : str
		Desired result for the chi-square question, either 'reject' or 'accept'.

	Returns
	-------
	tuple
		Complete question string and the answer number.
	"""
	# Define ratio based on desired_result
	if desired_result == 'reject':
		ratio = random.choice(bad_ratios)
	elif desired_result == 'accept':
		ratio = '9:3:3:1'

	# Create observed data
	observed = [90, 30, 30, 10]
	while (min(observed) < 2
		or 88 <= observed[0] <= 92
		or 9 <= observed[3] <= 11
		or observed[3] > 19):
		observed = createObservedProgeny(ratio=ratio)

	# Create chi-square table (not defined in this code)
	chi_square_table =chisquarelib.make_chi_square_table()

	# Generate correct answer stats
	answer_stat_list = normalGoodStats(ratio, observed)
	answer_chi_sq = float(answer_stat_list[-1])

	# Initialize variables
	number_stats = []
	i = -1
	# Generate wrong stats, skipping the one specified by error_type
	for method in (divideByObservedError, divideByObservedAndSquareError, noSquareError):
		i += 1
		if i == error_type:
			continue
		wrong_stats_list = method(ratio, observed)
		number_stats.append(wrong_stats_list)

	# Error check
	if len(number_stats) > 2:
		sys.exit(1)

	# Shuffle tables
	number_stats.append(answer_stat_list)
	shuffle_map = list(range(len(number_stats)))
	random.shuffle(shuffle_map)
	shuffled_tables = []
	new_number_stats = []

	# Shuffle and prepare tables for the question
	for i, index in enumerate(shuffle_map):
		stats_list = number_stats[index]
		new_number_stats.append(stats_list)
		numbers_table = chisquarelib.create_data_table(stats_list, tables_list[i])
		shuffled_tables.append(numbers_table)

	# Calculate chi-square result
	df = 3
	alpha = 0.05
	result = chisquarelib.get_chi_square_result(answer_chi_sq, df, alpha)

	# Error check: unexpected result
	if not result.startswith(desired_result):
		print("Woah! Unexpected result, it's okay though.")
		print(f"Debug: desired_result = {desired_result}, result = {result}")  # Debugging line
		print(answer_chi_sq)
		return None,None,None

	# Identify the correct answer
	answer_num = shuffle_map.index(2)
	if answer_chi_sq != float(new_number_stats[answer_num][-1]):
		print("Woah! Unexpected result, it's okay though.")
		print(answer_chi_sq, float(new_number_stats[answer_num][-1]))
		sys.exit(1)

	# Shift answer_num if the result is 'accept_null'
	if result == 'accept_null':
		answer_num += 3

	# Write the question content
	question = questionContent()
	complete_question = f"{chi_square_table} <br/> "
	for number_table in shuffled_tables:
		complete_question += f"{number_table} <br/> "
	complete_question += " <hr/> "
	complete_question += question

	edit_choices_list = []
	for i, choice in enumerate(choices_list):
		chi2value = float(new_number_stats[i%3][-1])
		edit_choice = choice.replace('XXXX' , f'{chi2value:.3f}')
		edit_choices_list.append(edit_choice)

	return complete_question, answer_num, edit_choices_list

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	parser = argparse.ArgumentParser(description='Chi Square Question')
	parser.add_argument('-d', '--duplicate-runs', type=int, dest='duplicate_runs',
		help='number of questions to create', default=199)
	args = parser.parse_args()

	letters = "ABCDEFGHI"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	while N < args.duplicate_runs:
		# three (3) types
		error_type = random.choice(list(error_types.keys()))
		# two (2) outcomes
		desired_result = random.choice(('accept', 'reject'))
		print(f"desired_result={desired_result} error_type={error_type}")
		complete_question, answer_num, edit_choices_list = makeQuestion(error_type, desired_result)
		if complete_question is None:
			continue
		answer_str = edit_choices_list[answer_num]
		N += 1
		bbformat = bptools.formatBB_MC_Question(N, complete_question, edit_choices_list, answer_str)
		f.write(bbformat)
	f.close()
	bptools.print_histogram()


#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
