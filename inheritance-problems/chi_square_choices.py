#!/usr/bin/env python3

import os
import sys
import copy
import random
import argparse
from scipy.stats.distributions import chi2

import bptools


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

accept_str = '<span style="color: #009900;"><strong>ACCEPT</strong></span>' #GREEN
reject_str = '<span style="color: #e60000;"><strong>REJECT</strong></span>' #RED
tables_list = [
		'<span style="color: #e69100;"><strong>Table 1</strong></span>', #LIGHT ORANGE
		'<span style="color: #004d99;"><strong>Table 2</strong></span>', #NAVY BLUE
		'<span style="color: #b30077;"><strong>Table 3</strong></span>', #MAGENTA
	]


choices_list = [
	f'{tables_list[0]} with &chi;&sup2;=XXXX is correct and we {reject_str} the null hypothesis',
	f'{tables_list[1]} with &chi;&sup2;=XXXX is correct and we {reject_str} the null hypothesis',
	f'{tables_list[2]} with &chi;&sup2;=XXXX is correct and we {reject_str} the null hypothesis',

	f'{tables_list[0]} with &chi;&sup2;=XXXX is correct and we {accept_str} the null hypothesis',
	f'{tables_list[1]} with &chi;&sup2;=XXXX is correct and we {accept_str} the null hypothesis',
	f'{tables_list[2]} with &chi;&sup2;=XXXX is correct and we {accept_str} the null hypothesis',
]

#===================
#===================
def get_p_value(chisq, df):
	#print("chisq={0}, df={1}".format(chisq, df))
	pvalue = chi2.sf(float(chisq), int(df))
	return float(pvalue)

#===================
#===================
def get_critical_value(alpha_criterion, df):
	critical_value = chi2.ppf(1.0 - float(alpha_criterion), int(df))
	#print(chisq)
	return float(critical_value)

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
def createDataTable(stats_list, title=None):
	numcol = len(stats_list[0])
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="160"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	if title is not None:
		table += "<tr>"
		table += " <th align='center' colspan='5' style='background-color: silver'>{0}</th> ".format(title)
		table += "</tr>"
	table += "<tr>"
	table += " <th align='center' style='background-color: lightgray'>Phenotype</th> "
	table += " <th align='center' style='background-color: lightgray'>Expected</th> "
	table += " <th align='center' style='background-color: lightgray'>Observed</th> "
	table += " <th align='center' style='background-color: lightgray'>Calculation</th> "
	table += " <th align='center' style='background-color: lightgray'>Statistic</th> "
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Yellow Round (Y&ndash;R&ndash;)</td>"
	for j in range(numcol):
		stat = stats_list[0][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Yellow Wrinkled (Y&ndash;rr)</td>"
	for j in range(numcol):
		stat = stats_list[1][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Green Round (yyR&ndash;)</td>"
	for j in range(numcol):
		stat = stats_list[2][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Green Wrinkled (yyrr)</td>"
	for j in range(numcol):
		stat = stats_list[3][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td colspan='{0}' align='right' style='background-color: lightgray'>(sum) &chi;&sup2;&nbsp;=&nbsp;</td>".format(numcol)
	stat = stats_list[4]
	table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "</table>"
	return table

#===================
#===================
def make_chi_square_table():
	max_df = 4
	p_values = [0.95, 0.90, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01]
	table = '<table border=1 style="border: 1px solid gray; border-collapse: collapse; ">'
	table += '<colgroup width="100"></colgroup> '
	for p in p_values:
		table += '<colgroup width="60"></colgroup> '
	table += "<tr>"
	table += " <th align='center' colspan='{0}' style='background-color: gainsboro'>Table of Chi-Squared (&chi;&sup2;) Critical Values</th>".format(len(p_values)+1)
	table += "</tr>"

	table += "<tr>"
	table += " <th rowspan='2' align='center' style='background-color: silver'>Degrees of Freedom</th>"
	table += " <th align='center' colspan='{0}' style='background-color: silver'>Probability</th>".format(len(p_values))
	table += "</tr>"
	table += "<tr>"
	for p in p_values:
		table += " <th align='center' style='background-color: gainsboro'>{0:.2f}</th>".format(p)
	table += "</tr>"
	for df in range(1, max_df+1):
		table += "<tr>"
		table += " <th align='center' style='background-color: silver'>{0:d}</th>".format(df)
		for p in p_values:
			chisq = get_critical_value(p, df)
			table += " <td align='center'>{0:.2f}</td>".format(chisq)
		table += "</tr>"

	table += "</table>"
	return table

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
	question += "<b>tell them which table is correct AND whether they can accept or reject "
	question += "the null hypothesis</b> using the information provided.</p> "
	return question

#===================
#===================
def getChiSquareResult(final_chisq, df, alpha):
	critical_value = get_critical_value(alpha, df)
	if final_chisq > critical_value:
		return 'reject_null'
	elif final_chisq <= critical_value:
		return 'accept_null'
	return None

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
def makeQuestion(error_type: int, desired_result: str):
	"""
	error type to NOT include

	0: 'divide by observed squared',
	1: 'forget to square the top divide by observed squared',
	2: 'forget to square the top divide by observed',
	"""
	if desired_result == 'reject':
		ratio = random.choice(bad_ratios)
	elif desired_result == 'accept':
		ratio = '9:3:3:1'

	observed = [90, 30, 30, 10]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11 or observed[3] > 19:
		observed = createObservedProgeny(ratio=ratio)

	chi_square_table = make_chi_square_table()

	answer_stat_list = normalGoodStats(ratio, observed)
	answer_chi_sq = float(answer_stat_list[-1])

	number_stats = []
	i = -1
	#print(f"error_type={error_type}")
	for method in (divideByObservedError, divideByObservedAndSquareError, noSquareError):
		i += 1
		#print(i)
		if i == error_type:
			continue
		wrong_stats_list = method(ratio, observed)
		number_stats.append(wrong_stats_list)
	if len(number_stats) > 2:
		sys.exit(1)

	#take the tables and shuffle them
	number_stats.append(answer_stat_list)
	print(f"answer_chi_sq={answer_chi_sq}")
	shuffle_map = list(range(len(number_stats)))
	random.shuffle(shuffle_map)
	#print(shuffle_map)
	shuffled_tables = []
	new_number_stats = []
	for i, index in enumerate(shuffle_map):
		stats_list = number_stats[index]
		new_number_stats.append(stats_list)
		numbers_table = createDataTable(stats_list, tables_list[i%3])
		shuffled_tables.append(numbers_table)
	#use the real values
	df = 3
	alpha = 0.05
	result = getChiSquareResult(answer_chi_sq, df, alpha)
	if not result.startswith(desired_result):
		print("Woah! Unexpected result, it's okay though.")
		print(desired_result, "!=", result)
		print(answer_chi_sq)
		sys.exit(1)
	#print(desired_result, result)
	# this line below needed fixing for this problem to work!!!
	#print(shuffle_map)
	answer_num = shuffle_map.index(2)
	if answer_chi_sq != float(new_number_stats[answer_num][-1]):
		print("Woah! Unexpected result, it's okay though.")
		print(answer_chi_sq, float(new_number_stats[answer_num][-1]))
		sys.exit(1)
	answer_str = choices_list[answer_num]
	#print(answer_num, answer_str)
	#print("answer_num", answer_num)
	if result == 'accept_null':
		answer_num += 3
	answer_str = choices_list[answer_num]
	print(answer_num, answer_str)

	# write the question content
	question = questionContent()

	complete_question = chi_square_table+" <br/> "
	for number_table in shuffled_tables:
		complete_question += number_table+" <br/> "
	complete_question += " <hr/> "
	complete_question += question

	return complete_question, answer_num

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Chi Square Question')
	parser.add_argument('-d', '--duplicate-runs', type=int, dest='duplicate_runs',
		help='number of questions to create', default=199)
	args = parser.parse_args()

	letters = "ABCDEFGHI"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(args.duplicate_runs):
		# three (3) types
		error_type = random.choice(list(error_types.keys()))
		# two (2) outcomes
		desired_result = random.choice(('accept', 'reject'))
		print(f"desired_result={desired_result} error_type={error_type}")
		complete_question, answer_num = makeQuestion(error_type, desired_result)
		print(answer_num)
		answer_str = choices_list[answer_num]
		print(answer_str)
		choices_list_copy = copy.copy(choices_list)
		N += 1
		bbformat = bptools.formatBB_MC_Question(N, complete_question, choices_list_copy, answer_str)
		f.write(bbformat)
	f.close()
	bptools.print_histogram()
