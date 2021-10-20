#!/usr/bin/env python

import os
import sys
import random
import string
from scipy.stats.distributions import chi2

### simply calculate the chi square value

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
def createDataTableWithMissing(stats_list, title=None):
	numcol = len(stats_list[0])
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="200"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
	table += '<colgroup width="100"></colgroup> '
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
		if j <= 1:
			table += " <td align='center'>{0}</td>".format(stat)
		else:
			table += " <td align='center'>__</td>"
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Yellow Wrinkled (Y&ndash;rr)</td>"
	for j in range(numcol):
		stat = stats_list[1][j]
		if j <= 1:
			table += " <td align='center'>{0}</td>".format(stat)
		else:
			table += " <td align='center'>__</td>"
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Green Round (yyR&ndash;)</td>"
	for j in range(numcol):
		stat = stats_list[2][j]
		if j <= 1:
			table += " <td align='center'>{0}</td>".format(stat)
		else:
			table += " <td align='center'>__</td>"
	table += "</tr>"
	table += "<tr>"
	table += " <td>&nbsp;Green Wrinkled (yyrr)</td>"
	for j in range(numcol):
		stat = stats_list[3][j]
		if j <= 1:
			table += " <td align='center'>{0}</td>".format(stat)
		else:
			table += " <td align='center'>__</td>"
	table += "</tr>"
	table += "<tr>"
	table += " <td colspan='{0}' align='right' style='background-color: lightgray'>(sum) &chi;<sup>2</sup>&nbsp;=&nbsp;</td>".format(numcol)
	stat = stats_list[4]
	table += " <td align='center'>__</td>"
	table += "</tr>"
	table += "</table>"
	return table


#===================
#===================
def questionContent():
	question = ''
	question += "<p>Complete the table and calculate the chi-squared (&chi;<sup>2</sup>) value.</p> "
	question += "<p><i>Even though not part of the question, ask yourself whether you would "
	question += "reject or accept the null hypothesis</i></p> "
	question += "<p><i>Answers need to be within 10&#37; of the actual value to be correct.</i></p> "

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
def makeQuestion( desired_result):

	if desired_result == 'reject':
		ratio = '8:2:4:2'
	elif desired_result == 'accept':
		ratio = '9:3:3:1'

	observed = [90, 30, 30, 10]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11 or observed[3] > 19:
		observed = createObservedProgeny(ratio=ratio)

	answer_stat_list = normalGoodStats(ratio, observed)

	#take the tables and shuffle them
	numbers_table = createDataTableWithMissing(answer_stat_list, "Data Table")

	#use the real values
	final_chisq = float(answer_stat_list[-1])
	df = 3
	alpha = 0.05
	result = getChiSquareResult(final_chisq, df, alpha)
	if not result.startswith(desired_result):
		print("Woah! Unexpected result, it's okay though.")
		print(desired_result, "!=", result)
		print(final_chisq)
		return None, None
		#sys.exit(1)
	#print(desired_result, result)
	# this line below needed fixing for this problem to work!!!

	# write the question content
	question = questionContent()

	complete_question = ''
	complete_question += numbers_table+" <br/> "
	complete_question += " <hr/> "
	complete_question += question

	return complete_question, final_chisq

#===================
#===================
def getCode():
	source = string.ascii_uppercase + string.digits
	code = ''
	for i in range(5):
		code += random.choice(source)
	code += ' - '
	return code

#==================================================
def format_for_blackboard(question, answer, tolerance):
	#https://experts.missouristate.edu/plugins/servlet/mobile?contentId=63486780#content/view/63486780
	#"NUM TAB question text TAB answer TAB [optional]tolerance"
	return ("NUM\t{0}\t{1:.3f}\t{2:.3f}".format(question,answer,tolerance))

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	duplicates = 250
	letters = "ABCDEFGHI"
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(duplicates):
		#for desired_result in ('accept', 'reject'):
		desired_result = 'accept'
		#print("")
		#print(desired_result)
		sys.stderr.write(".")
		if i % 80 == 0:
			sys.stderr.write("\n")
		complete_question, final_chisq = makeQuestion(desired_result)
		if complete_question is None:
			i -= 1
			continue
		tolerance = final_chisq * 0.10
		bbq_content = format_for_blackboard(complete_question, final_chisq, tolerance)
		f.write(bbq_content)
		f.write("\n")
	sys.stderr.write("\n")
