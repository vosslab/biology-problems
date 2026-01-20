#!/usr/bin/env python3

import math
import random

import bptools

class GelMigration(object):
	def __init__(self):
		self.debug = False

		self.slope = 0.8 * self.random_average(10)
		self.min_mw = 100
		self.max_mw = 10000
		self.intercept = math.log(self.max_mw) * self.random_average(10)
		#f(max) = 0.0
		#f(min) = 5.0
		#f(x) = b - m*log(x)
		# 0 = log(max) - m*log(max)
		# 0 = m + 1
		# m = -1s


	#==================================================
	def random_average(self, count):
		x = 0
		for i in range(count):
			x += random.random()
		x /= float(count)
		return x

	#==================================================
	def molecular_weight_to_distance(self, mw):
		dist = self.intercept - math.log(mw)*self.slope
		if dist <= 0:
			raise ValueError("Distance less than zero.")
		return dist

	#==================================================
	def distance_to_molecular_weight(self, dist):
		mw = math.exp( (self.intercept - dist)/self.slope )
		return mw

	#==================================================
	def sort_by_molecular_weight(self, a, b):
		if a['MW'] > b['MW']:
			return True
		return False

	#==================================================
	def getNearestValidDNA_Size(self, num_base_pairs):
		num_zeros = math.floor(math.log10(num_base_pairs + 1))
		two_divisor = 10**(num_zeros - 1)

		first_two_digits = int(math.ceil(num_base_pairs / two_divisor))
		first_digit = first_two_digits // 10
		second_digit = first_two_digits % 10
		#if 2 < second_digit < 8:
		#	second_digit = 5
		#else:
		#	second_digit = 0
		first_two_digits = first_digit * 10 + second_digit
		new_num_base_pairs = first_two_digits * two_divisor
		#print(num_base_pairs, "-->", new_num_base_pairs)

		return new_num_base_pairs

	#==================================================
	def get_marker_set_for_gel(self):

		gel_set = []
		gel_set.append( {'MW': 500, 'fullname': '500 base pairs', 'abbr': '500 bp',} )
		gel_set.append( {'MW': 1000, 'fullname': '1,000 base pairs', 'abbr': '1000 bp',} )
		gel_set.append( {'MW': 2000, 'fullname': '2,000 base pairs', 'abbr': '2000 bp',} )
		gel_set.append( {'MW': 3000, 'fullname': '3,000 base pairs', 'abbr': '3000 bp',} )
		gel_set.append( {'MW': 5000, 'fullname': '5,000 base pairs', 'abbr': '5000 bp',} )
		gel_set.append( {'MW': 10000, 'fullname': '10,000 base pairs', 'abbr': '10000 bp',} )


		gel_set = sorted(gel_set, key=lambda k: k['MW'])

		if self.debug is True:
			print("")
			import pprint
			pprint.pprint(gel_set)

		return gel_set

	#==================================================
	def get_unknown(self, gel_set, gap=None):
		if gap is None:
			gap = random.randint(1,4)

		low_mw = gel_set[gap-1]['MW']
		high_mw = gel_set[gap]['MW']
		mw_range = (high_mw - low_mw)/4.0

		low_dist = self.molecular_weight_to_distance(low_mw)
		high_dist = self.molecular_weight_to_distance(high_mw)
		#30-70%
		adj_rand = random.random()*0.4 + 0.3

		unknown_dist = adj_rand*(high_dist - low_dist) + low_dist
		if unknown_dist < 0:
			raise ValueError("Distance less than zero.")
		unknown_mw = self.distance_to_molecular_weight(unknown_dist)
		#just clean up the numbers
		unknown_mw = self.getNearestValidDNA_Size(unknown_mw)
		unknown_dist = self.molecular_weight_to_distance(unknown_mw)

		dist_range = (high_dist - low_dist)/2.0
		#mw_range = (high_unknown_mw - low_unknown_mw)/4.0

		if self.debug is True:
			print(f"Unknown: MW = {unknown_mw:.1f} +/- {mw_range:.1f}; Dist = {unknown_dist:.2f} +/- {dist_range:.2f}")
		return unknown_mw, unknown_dist, mw_range, gap


	#==================================================
	def writeProblem(self, N=44, question_type='num', num_choices=5):

		gel_set = self.get_marker_set_for_gel()
		max_gap = min(len(gel_set) - 1, num_choices)
		unknown_gap = random.randint(1, max_gap)
		unknown_mw, unknown_dist, mw_range, gap = self.get_unknown(gel_set, unknown_gap)

		question = ''
		question += " <h6>Gel Migration Problem</h6> "
		question += '<p><table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">'
		question += (
			"<tr><th align='center' style='vertical-align: bottom;'>DNA Marker</th>"
			"<th align='center'>&num; of<br/>Base Pairs<br/>(bp)</th>"
			"<th align='center'>Migration<br/>Distance<br/>(cm)</th></tr>"
		)
		for marker_dict in gel_set:
			dist = self.molecular_weight_to_distance(marker_dict['MW'])
			question += (
				f"<tr><td align='right'>{marker_dict['fullname']}</td>"
				f"<td align='right'>{marker_dict['MW']:d}</td>"
				f"<td align='right'>{dist:.2f}</td></tr>"
			)
		question += (
			f"<tr><td align='right'>Unknown</td>"
			f"<td align='center'>?&nbsp;?</td>"
			f"<td align='right'>{unknown_dist:.2f}</td></tr>"
		)
		question += "</table></p>"
		question += '<p>The standard DNA ladder and unknown DNA strand listed in the table were separated using an agarose gel</p>'
		question += '<p><b>Estimate the number of base pairs of the unknown DNA strand.</b></p>'

		if question_type == 'mc':
			choices_list = []
			answer = f'{unknown_mw} base pairs (bp)'
			choice_count = min(num_choices, len(gel_set) - 1)
			for i in range(choice_count):
				j = i+1
				if j == gap:
					choices_list.append(answer)
					continue
				mw, _dist, _range, _gap = self.get_unknown(gel_set, j)
				new_num_base_pairs = self.getNearestValidDNA_Size(mw)
				choices_list.append(f'{new_num_base_pairs} base pairs (bp)')
			bb_format = bptools.formatBB_MC_Question(N, question, choices_list, answer)
		else:
			bb_format = bptools.formatBB_NUM_Question(N, question, unknown_mw, mw_range)

		return bb_format

def write_question(N, args):
	return args.gelm.writeProblem(N, args.question_type, args.num_choices)


#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate gel migration questions.")
	parser = bptools.add_choice_args(parser, default=5)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc', 'num'],
		required=False,
		default='num'
	)
	args = parser.parse_args()
	return args


#==================================================
def main():
	args = parse_arguments()
	args.gelm = GelMigration()
	outfile = bptools.make_outfile(args.question_type)
	bptools.collect_and_write_questions(write_question, args, outfile)


#==================================================
if __name__ == '__main__':
	main()
