#!/usr/bin/env python

import os
import sys
import copy
import random
from scipy.stats.distributions import chi2

### types of errors
# show 3 tables of chi square calculations
# - table 1 the real answer
# - table 2 divide by the observed
# - table 3 random choice of
# - - divide by observed squared
# - - forget to square the top divide by observed squared
# - - forget to square the top divide by observed
# student chooses which one is correct, and decides whether or not to reject the null.

error_types = {
	0: 'divide by observed squared',
	1: 'forget to square the top divide by observed squared',
	2: 'forget to square the top divide by observed',
}

choices = [
	'table 1 is correct and we <b>reject</b> the null hypothesis',
	'table 2 is correct and we <b>reject</b> the null hypothesis',
	'table 3 is correct and we <b>reject</b> the null hypothesis',

	'table 1 is correct and we <b>accept</b> the null hypothesis',
	'table 2 is correct and we <b>accept</b> the null hypothesis',
	'table 3 is correct and we <b>accept</b> the null hypothesis',
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
		calc = "<sup>({0}-{1})<sup>2</sup></sup>&frasl;&nbsp;<sub>{2}</sub>".format(obs, exp, obs)
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
		calc = "<sup>({0}-{1})<sup>2</sup></sup>&frasl;&nbsp;<sub>{2}<sup>2</sup></sub>".format(obs, exp, obs)
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
		calc = "<sup>({0}-{1})<sup>2</sup></sup>&frasl;&nbsp;<sub>{2}</sub>".format(obs, exp, exp)
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
	table += " <td colspan='{0}' align='right' style='background-color: lightgray'>(sum) &chi;<sup>2</sup>&nbsp;=&nbsp;</td>".format(numcol)
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
	table += " <th align='center' colspan='{0}' style='background-color: gainsboro'>Table of Chi-Squared (&chi;<sup>2</sup>) Critical Values</th>".format(len(p_values)+1)
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
	question += "<p>Your lab partner is trying again (eye roll) and did another a chi-squared (&chi;<sup>2</sup>) test "
	question += "on the F<sub>2</sub> generation in a dihybid cross based on your lab data (above). "
	question += "They wanted to know if the results confirm the expected phenotype ratios.</p>"

	question += "<p>You helped them set up the null hypothesis, so you know that part is correct, "
	question += "but they got confused and were unsure about how to calculate the "
	question += "chi-squared (&chi;<sup>2</sup>) value. So much so that "
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

#===================
#===================
def makeQuestion(error_type, desired_result):
	"""
	error type to NOT include

	0: 'divide by observed squared',
	1: 'forget to square the top divide by observed squared',
	2: 'forget to square the top divide by observed',
	"""

	if desired_result == 'reject':
		ratio = '8:2:4:2'
	elif desired_result == 'accept':
		ratio = '9:3:3:1'

	observed = [90, 30, 30, 10]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11 or observed[3] > 19:
		observed = createObservedProgeny(ratio=ratio)

	chi_square_table = make_chi_square_table()

	answer_stats = normalGoodStats(ratio, observed)

	number_stats = []
	i = -1
	#print(error_type)
	for method in (divideByObservedError, divideByObservedAndSquareError, noSquareError):
		i += 1
		#print(i)
		if i == error_type:
			continue
		wrong_stats_list = method(ratio, observed)
		number_stats.append(wrong_stats_list)

	#tabke the tables and shuffle them
	number_stats.append(answer_stats)
	shuffle_map = list(range(len(number_stats)))
	random.shuffle(shuffle_map)
	#print(shuffle_map)
	shuffled_tables = []
	for i,index in enumerate(shuffle_map):
		stats_list = number_stats[index]
		numbers_table = createDataTable(stats_list, "Table {0}".format(i+1))
		shuffled_tables.append(numbers_table)

	#use the real values
	final_chisq = float(answer_stats[-1])
	df = 3
	alpha = 0.05
	result = getChiSquareResult(final_chisq, df, alpha)
	print(result)
	answer_num = shuffle_map[2]
	if result == 'accept_null':
		answer_num += 3

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
	duplicates = 15
	letters = "ABCDEFGHI"
	f = open("bbq-chi_square_choices.txt", "w")
	for i in range(duplicates):
		for error_type in error_types:
			for desired_result in ('accept', 'reject'):
				print("")
				print(desired_result)
				complete_question, answer_num = makeQuestion(error_type, desired_result)
				f.write("MC\t{0}".format(complete_question))
				answer = choices[answer_num]
				choices_copy = copy.copy(choices)
				#random.shuffle(choices_copy)
				for k, c in enumerate(choices_copy):
					if c == answer:
						prefix = "*"
						status = "Correct"
					else:
						prefix = ""
						status = "Incorrect"
					f.write("\t{0}\t{1}".format(c, status))
					print("{0}{1}. {2}".format(prefix, letters[k], c))
				f.write("\n")
