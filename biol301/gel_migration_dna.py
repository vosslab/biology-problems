#!/usr/bin/env python

import sys
import csv
import math
#import numpy
import random

class GelMigration(object):
	def __init__(self):
		self.debug = False
		self.multiple_choice = True

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
	def get_marker_set_for_gel(self):

		gel_set = []
		gel_set.append( {'MW': 500, 'fullname': '500 base pairs', 'abbr': '500 bp',} )
		gel_set.append( {'MW': 1000, 'fullname': '1,000 base pairs', 'abbr': '1000 bp',} )
		gel_set.append( {'MW': 1500, 'fullname': '1,500 base pairs', 'abbr': '1500 bp',} )
		gel_set.append( {'MW': 2000, 'fullname': '2,000 base pairs', 'abbr': '2000 bp',} )		
		gel_set.append( {'MW': 3000, 'fullname': '3,000 base pairs', 'abbr': '3000 bp',} )
		gel_set.append( {'MW': 4000, 'fullname': '4,000 base pairs', 'abbr': '4000 bp',} )
		gel_set.append( {'MW': 5000, 'fullname': '5,000 base pairs', 'abbr': '5000 bp',} )

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
		unknown_mw = self.distance_to_molecular_weight(unknown_dist)

		dist_range = (high_dist - low_dist)/2.0
		low_unknown_mw = self.distance_to_molecular_weight(unknown_dist-dist_range)
		high_unknown_mw = self.distance_to_molecular_weight(unknown_dist+dist_range)
		#mw_range = (high_unknown_mw - low_unknown_mw)/4.0


		if self.debug is True:
			print("Unknown: MW = {0:.1f} +/- {1:.1f}; Dist = {2:.2f} +/- {3:.2f}".format(unknown_mw, mw_range, unknown_dist, dist_range))
		return unknown_mw, unknown_dist, mw_range, gap


	#==================================================
	def writeProblem(self, N=44):

		gel_set = self.get_marker_set_for_gel()
		unknown_mw, unknown_dist, mw_range, gap = self.get_unknown(gel_set)

		if self.multiple_choice is True:
			question = "{0:d}. ".format(N)
		else:
			question = ""
		question += " <h6>Gel Migration Problem</h6> "
		question += ('<p><table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">')
		question += ('<tr><th>Marker</th><th align="center">&num; of<br/>Base Pairs (bp)</th><th align="center">>Migration<br/>Distance (cm)</th></tr>')
		for marker_dict in gel_set:
			dist = self.molecular_weight_to_distance(marker_dict['MW'])
			question += ('<tr><td>{0}</td><td align="center">{2:d}</td><td align="center">{3:.2f}</td></tr>'.format(marker_dict['fullname'], marker_dict['abbr'], marker_dict['MW'], dist))
		question += ('<tr><td>{0}</td><td align="center">{1}</td><td align="center">{2:.2f}</td></tr>'.format("Unknown", "?", unknown_dist))
		question += "</table></p>"
		question += '<p>The standard DNA ladder and unknown DNA strand listed in the table were separated using an agarose gel</p>'
		question += '<p><b>Estimate the number of base pairs of the unknown DNA strand.</b></p>'

		if self.multiple_choice is True:
			print(question)
			choices = []
			for i in range(4):
				j = i+1
				if j == gap:
					choices.append(unknown_mw)
					continue
				mw, d, r, g = self.get_unknown(gel_set, j)
				choices.append(mw)
			letters = "ABCDEFG"
			for i in range(4):
				prefix = ''
				if abs(choices[i] - unknown_mw) < 0.1:
					prefix = '*'
				print("{0}{1}. {2:.0f} base pairs".format(prefix, letters[i], choices[i]))
			print("")
		else:
			bb_format = self.format_for_blackboard(question, unknown_mw, mw_range)
			print(bb_format)

		return question

	#==================================================
	def format_for_blackboard(self, question, answer, tolerance):
		#https://experts.missouristate.edu/plugins/servlet/mobile?contentId=63486780#content/view/63486780
		#"NUM TAB question text TAB answer TAB [optional]tolerance"
		return ("NUM\t{0}\t{1:.1f}\t{2:.1f}".format(question,answer,tolerance))



#==================================================
#==================================================
if __name__ == '__main__':
	total_problems = 100
	gelm = GelMigration()
	for question_count in range(total_problems):
		problem = gelm.writeProblem(question_count+1)



