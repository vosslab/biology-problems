#!/usr/bin/env python3

import bptools
import chisquarelib

#===================
#===================
def normalGoodStats(ratio, observed=None):
	if observed is None:
		observed = [90]
		while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11:
			observed = chisquarelib.create_observed_progeny(ratio=ratio)
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
	table = '<table style="border: 1px solid black; border-collapse: collapse; ">'
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
	question += "reject or fail to reject the null hypothesis</i></p> "

	return question

#===================
#===================
def makeQuestion( desired_result):

	if desired_result == 'reject':
		ratio = '8:2:4:2'
	elif desired_result == 'accept':
		ratio = '9:3:3:1'

	observed = [90, 30, 30, 10]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11 or observed[3] > 19:
		observed = chisquarelib.create_observed_progeny(ratio=ratio)

	answer_stat_list = normalGoodStats(ratio, observed)

	#take the tables and shuffle them
	numbers_table = createDataTableWithMissing(answer_stat_list, "Data Table")

	#use the real values
	final_chisq = float(answer_stat_list[-1])
	df = 3
	alpha = 0.05
	result = chisquarelib.get_chi_square_result(final_chisq, df, alpha)
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
#===================
#===================
def write_question(N, args):
	complete_question, final_chisq = makeQuestion(args.desired_result)
	if complete_question is None:
		return None
	tolerance = round(max(final_chisq * 0.02, 0.01), 2)
	bbq_content = bptools.formatBB_NUM_Question(N, complete_question, final_chisq, tolerance)
	return bbq_content

#===================
def parse_arguments():
	parser = bptools.make_arg_parser(description='Chi Square Question')
	question_group = parser.add_mutually_exclusive_group(required=False)
	question_group.add_argument('--desired_result', dest='desired_result', type=str,
		choices=('accept', 'reject'), help='Set the question type: accept or reject')
	question_group.add_argument('-a', '--accept', dest='desired_result', action='store_const',
		const='accept',)
	question_group.add_argument('-r', '--reject', dest='desired_result', action='store_const',
		const='reject',)
	parser.set_defaults(desired_result='accept')
	args = parser.parse_args()
	return args

#===================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None, args.desired_result.upper())
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
