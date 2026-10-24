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
	blank_rows = [[row[0], row[1], "__", "__"] for row in stats_list[:-1]]
	blank_rows.append("__")
	table = chisquarelib.create_data_table(blank_rows, title, labels=chisquarelib.PEA_PHENOTYPES)
	return table

#===================
#===================
def questionContent():
	question = ''
	question += "<p>Complete the table and calculate the <span style='color: #935d00;'>chi-square statistic (&chi;<sup>2</sup>)</span>.</p> "
	question += "<p><i>Even though not part of the question, ask yourself whether you would "
	question += "reject or fail to reject the <span style='color: #0247fe;'>null hypothesis (H<sub>0</sub>)</span></i></p> "

	return question

#===================
#===================
def makeQuestion( desired_result):

	if desired_result == 'reject':
		ratio = '8:2:4:2'
	elif desired_result == 'support':
		ratio = '9:3:3:1'

	observed = [90, 30, 30, 10]
	while 88 <= observed[0] <= 92 or 9 <= observed[3] <= 11 or observed[3] > 19:
		observed = chisquarelib.create_observed_progeny(ratio=ratio)

	answer_stat_list = normalGoodStats(ratio, observed)

	#take the tables and shuffle them
	numbers_table = createDataTableWithMissing(answer_stat_list)

	#use the real values
	final_chisq = float(answer_stat_list[-1])
	df = 3
	alpha = 0.05
	result = chisquarelib.get_chi_square_result(final_chisq, df, alpha)
	if not result.startswith("accept" if desired_result == "support" else "reject"):
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
		choices=('support', 'reject'), help='Set the question type: support or reject')
	question_group.add_argument('-s', '--support', dest='desired_result', action='store_const',
		const='support',)
	question_group.add_argument('-r', '--reject', dest='desired_result', action='store_const',
		const='reject',)
	parser.set_defaults(desired_result='support')
	args = parser.parse_args()
	return args

#===================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(args.desired_result.upper())
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
