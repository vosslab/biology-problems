#!/usr/bin/env python

import os
import copy
import string
import random
from scipy.stats.distributions import chi2

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
	'the wrong numbers in the calculation were used for division',
	'the numbers in the calculation have to be squared',
	'the wrong rejection criteria was used',
	'the expected progeny for the null hypothesis is incorrect',
	'the degrees of freedom is wrong',
]

#===================
#===================
def get_p_value(chisq, df):
	#print("chisq={0}, df={1}".format(chisq, df))
	pvalue = chi2.sf(float(chisq), int(df))
	return float(pvalue)

#===================
#===================
def get_chisq_value(pvalue, df):
	chisq = chi2.ppf(1.0 - float(pvalue), int(df))
	#print(chisq)
	return float(chisq)

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
def divideByObservedError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = createObservedProgeny()
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
def divideByObservedAndSquareError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = createObservedProgeny()
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
def divideBySquareError():
	observed = [90]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
		observed = createObservedProgeny()
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
		calc = "<sup>({0}-{1})<sup>2</sup></sup>&frasl;&nbsp;<sub>{2}<sup>2</sup></sub>".format(obs, exp, exp)
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
		observed = createObservedProgeny()
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
		observed = createObservedProgeny()
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
def wrongNullHypothesis():
	observed = [90]
	while observed[0] >= 70 or observed[3] <= 20:
		observed = createObservedProgeny(ratio="7:5:3:2")
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
def createDataTable(stats_list):
	numcol = len(stats_list[0])
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="160"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += "<tr>"
	table += " <th align='center' style='background-color: lightgray'>Phenotype</th> "
	table += " <th align='center' style='background-color: lightgray'>Expected</th> "
	table += " <th align='center' style='background-color: lightgray'>Observed</th> "
	table += " <th align='center' style='background-color: lightgray'>Calculation</th> "
	table += " <th align='center' style='background-color: lightgray'>Statistic</th> "
	table += "</tr>"
	table += "<tr>"
	table += " <td>Yellow Round (Y&ndash;R&ndash;)</td>"
	for j in range(numcol):
		stat = stats_list[0][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>Yellow Wrinkled (Y&ndash;rr)</td>"
	for j in range(numcol):
		stat = stats_list[1][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>Green Round (yyR&ndash;)</td>"
	for j in range(numcol):
		stat = stats_list[2][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>Green Wrinkled (yyrr)</td>"
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
			chisq = get_chisq_value(p, df)
			table += " <td align='center'>{0:.2f}</td>".format(chisq)
		table += "</tr>"

	table += "</table>"
	return table

#===================
#===================
def chiSquareResults(chisq, critical_value, flip):
	if flip is False:
		if chisq > critical_value:
			results = ("greater", "rejected")
		elif chisq <= critical_value:
			results = ("less", "accepted")
	else:
		# this is WRONG
		if chisq > critical_value:
			results = ("greater", "accepted")
		elif chisq <= critical_value:
			results = ("less", "rejected")
	return results

#===================
#===================
def questionContent(chisq, df, alpha, flip=False):

	pvalue = get_p_value(chisq, df)
	critical_value = get_chisq_value(alpha, df)

	question = ""
	question += "<p>The final result gives the chi-squared (&chi;<sup>2</sup>) test value of {0:.2f} with {1} degrees of freedom. ".format(chisq, df)
	question += "Using the Table of &chi;<sup>2</sup> Critical Values and a level of significance &alpha;={0:.2f}, we get a critical value of {1:.2f}. ".format(alpha, critical_value)
	#question += "They calculated a p-value of {2:.3f} ({3:.1f}%). ".format(chisq, df, pvalue, pvalue*100)
	#question += "Since the p-value was {0} than the level of significance &alpha;=0.05 (5%), the null hypothesis was {1}.</p>".format("less", "rejected")
	print("chi_square     = {0:.3f}".format(chisq))
	print("critical_value = {0:.3f}".format(critical_value))

	results = chiSquareResults(chisq, critical_value, flip)

	question += "Since the chi-squared (&chi;<sup>2</sup>) test value of {0:.2f} is {1} than the critical value of {2:.2f}, the null hypothesis was {3}.</p>".format(chisq, results[0], critical_value, results[1])

	question += "<hr/> "

	question += "<p>Your lab partner has done a chi-squared (&chi;<sup>2</sup>) test for your lab data (above), "
	question += "for the F<sub>2</sub> generation in a standard dihybid cross. They wanted to know if "
	question += "the results confirm the expected phenotype ratios, "
	question += "but as usual they did something wrong. <strong>What did they do wrong?</strong></p>"
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
	table1 = createDataTable(stats_list)
	chi_square_table = make_chi_square_table()
	question = questionContent(chisq, df, alpha, flip)
	complete_question = chi_square_table+"<br/>"+table1+"<br/>"+question

	return complete_question


def getCode():
	source = string.ascii_uppercase + string.digits
	code = ''
	for i in range(5):
		code += random.choice(source)
	code += ' - '
	return code


#===================
#===================
#===================
#===================
if __name__ == '__main__':
	duplicates = 11
	max_error_types = len(error2choice)
	letters = "ABCDEFGHI"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(duplicates):
		for error_type in range(max_error_types):
			print("")
			complete_question = makeQuestion(error_type)

			f.write("MC\t" + getCode() + complete_question)
			choice_index = error2choice[error_type]
			answer = choices[choice_index]
			choices_copy = copy.copy(choices)
			random.shuffle(choices_copy)
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
