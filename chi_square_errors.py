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

choices = [
	'the wrong number was used for division',
	'the numbers were not squared',
	'the wrong rejection criteria was used',
	'the null hypothesis is incorrect',
]

def createDataTable(stats_list):
	index = 0
	table = '<table cellpading=5 cellspacing=5 border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="180"></colgroup> '
	w = 90
	for j in range(4):
		table += '<colgroup width="{0}"></colgroup> '.format(w)
	table += "<tr>"
	table += " <th>Phenotype</th> "
	table += " <th align='center'>Expected</th> <th align='center'>Observed</th> "
	table += " <th align='center'>Deviation</th> <th align='center'>Statistic</th> "
	table += "</tr>"
	table += "<tr>"
	table += " <td>Yellow Round (Y&mdash;R&mdash;)</td>"
	for j in range(4):
		stat = stats_list[0][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>Yellow Wrinkled (Y&mdash;rr)</td>"
	for j in range(4):
		stat = stats_list[1][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>Green Round (yyR&mdash;)</td>"
	for j in range(4):
		stat = stats_list[2][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td>Green Wrinkled (yyrr)</td>"
	for j in range(4):
		stat = stats_list[3][j]
		table += " <td align='center'>{0}</td>".format(stat)
	table += "</tr>"
	table += "<tr>"
	table += " <td colspan='4' align='right'>&chi;<sup>2</sup>&nbsp;=&nbsp;</td>"
	stat = stats_list[4]
	table += " <td align='right'>{0}</td>".format(stat)
	table += "</tr>"
	table += "</table>"
	return table

if __name__ == '__main__':
	N = 0
	question = ""
	question += "Your lab partner has done a chi-squared (&chi;<sup>2</sup>) test for your lab data (abovE), "
	question += "but as usual they did something wrong. What did they do wrong? "

	stats_list = [[900, 900, 0, 0,], [300, 300, 0, 0,], [300, 300, 0, '0.002',], [100, 100, 0, 0,], '1.0']
	table = createDataTable(stats_list)
	print(table)

