#!/usr/bin/env python

import os
import sys
import random

### types of errors
# * divide by the observed instead of expected
# * forget to square the numbers before division
# * use chi-sq value being less than 0.05 to reject
# * take a p > 0.05 as reject
# * use the wrong null hypothesis
# * wrong degrees of freedom

choices = [
	'the wrong number was used for division',
	'the numbers were not squared',
	'the wrong rejection criteria was used',
	'the null hypothesis is incorrect',
	'the degrees of freedom is wrong',
]

#===================
#===================
def createObservedProgeny(N=160, ratio="9:3:3:1"):
	#female lay 100 eggs per day
	bins = ratio.split(':')
	floats = []
	for b in bins:
		floats.append(float(b))
	total = sum(floats)
	print(floats)
	probs = []
	sumprob = 0
	for f in floats:
		sumprob += f/total
		probs.append(sumprob)
	print(probs)
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
	while 88 <= observed[0] <= 92:
		observed = createObservedProgeny()
	expected = [90,30,30,10]
	stats_list = []
	chisq = 0.0
	for j in range(len(observed)):
		row = []
		row.append(expected[j])
		row.append(observed[j])
		diff = observed[j] - expected[j]
		row.append(diff)
		chirow = diff**2/float(observed[j])
		calc = "<sup>({0})<sup>2</sup></sup>&frasl;&nbsp;<sub>{1}</sub>".format(diff, observed[j])
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
	numcol = 5
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="160"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += "<tr>"
	table += " <th align='center' style='background-color: lightgray'>Phenotype</th> "
	table += " <th align='center' style='background-color: lightgray'>Expected</th> "
	table += " <th align='center' style='background-color: lightgray'>Observed</th> "
	table += " <th align='center' style='background-color: lightgray'>Deviation</th> "
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
	table += " <td colspan='5' align='right' style='background-color: lightgray'>(sum) &chi;<sup>2</sup>&nbsp;=&nbsp;</td>"
	stat = stats_list[4]
	table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "</table>"
	return table

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	N = 0
	question = ""
	question += "Your lab partner has done a chi-squared (&chi;<sup>2</sup>) test for your lab data (abovE), "
	question += "but as usual they did something wrong. What did they do wrong? "
	print(createObservedProgeny())

	#stats_list = [[900, 900, 0, 0,], [300, 300, 0, 0,], [300, 300, 0, '0.002',], [100, 100, 0, 0,], '1.0']
	stats_list = divideByObservedError()
	table = createDataTable(stats_list)
	print(table)

