#!/usr/bin/env python3

import sys
import csv
import math
#import numpy
import random
import proteinlib

class GelMigration(object):
	def __init__(self):
		self.debug = False
		self.multiple_choice = True
		proteinlib.debug = self.debug
		self.slope = 0.8
		self.intercept = 5.5
		self.min_mw = 13
		self.max_mw = 70
		self.protein_tree = proteinlib.parse_protein_file()
		self.filterProteinTree()

	#==================================================
	def filterProteinTree(self):
		new_tree = []
		initial_amount = len(self.protein_tree)
		for protein_dict in self.protein_tree:
			if protein_dict['MW'] < self.min_mw:
				continue
			if protein_dict['MW'] > self.max_mw:
				continue
			new_tree.append(protein_dict)
		self.protein_tree = new_tree
		if self.debug is True:
			print("Filter data for {1:d}/{0:d} proteins".format(initial_amount, len(self.protein_tree)))
		return

	#==================================================
	def molecular_weight_to_distance(self, mw):
		dist = self.intercept - math.log(mw)*self.slope
		return dist

	#==================================================
	def distance_to_molecular_weight(self, dist):
		mw = math.exp( (self.intercept - dist)/self.slope )
		return mw

	#==================================================
	def random_subset(self, size):
		return random.sample(self.protein_tree, size)

	#==================================================
	def sort_by_molecular_weight(self, a, b):
		if a['MW'] > b['MW']:
			return True
		return False

	#==================================================
	def get_protein_set_for_gel(self):
		subset = self.random_subset(24)
		subset = sorted(subset, key=lambda k: k['MW']) 
		pull_size = 3

		gel_set = []
		#get one of the smallest
		gel_set.append(subset[random.randint(1,pull_size)-1])
		min_log_mw = math.log(gel_set[0]['MW'])
		del subset[:pull_size]

		#get one of the biggest
		gel_set.append(subset[random.randint(-pull_size,-1)])
		max_log_mw = math.log(gel_set[1]['MW'])
		del subset[-pull_size:]

		#need three more
		log_slope = (max_log_mw - min_log_mw)/4.

		prev_mw = 0
		prev_prot_dict = None
		index = 1
		ideal_mw = math.exp(log_slope*index + min_log_mw)
		if self.debug is True:
			print("ideal_mw = {0:.1f}".format(ideal_mw))
		for protein_dict in subset:
			mw = protein_dict['MW']
			if mw < ideal_mw:
				prev_prot_dict = protein_dict
				prev_mw = mw
				continue

			if ideal_mw - mw < mw - prev_mw:
				gel_set.append(protein_dict)
			else:
				gel_set.append(prev_prot_dict)
			index += 1
			ideal_mw = math.exp(log_slope*index + min_log_mw)
			if self.debug is True:
				print("ideal_mw = {0:.1f}".format(ideal_mw))
			if index > 3:
				break

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
		"""
		49. <p>The standard and unknown proteins listed in the table were run using SDS–PAGE.</p> <p><b>Estimate the molecular weight of the unknown protein.</b></p>
		A. 190 kDa	B. 320 kDa	C. 430 kDa	D. 520 kDa
		"""

		gel_set = self.get_protein_set_for_gel()
		unknown_mw, unknown_dist, mw_range, gap = self.get_unknown(gel_set)

		if self.multiple_choice is True:
			question = "{0:d}. ".format(N)
		else:
			question = ""
		question += " <h6>Gel Migration Problem</h6> "
		question += ('<p><table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">')
		question += ('<tr><th>Protein Name</th><th>Molecular<br/>Weight (kDa)</th><th>Migration<br/>Distance (cm)</th></tr>')
		for protein_dict in gel_set:
			dist = self.molecular_weight_to_distance(protein_dict['MW'])
			question += ('<tr><td>{0} ({1})</td><td align="center">{2:.1f}</td><td align="center">{3:.2f}</td></tr>'.format(protein_dict['fullname'], protein_dict['abbr'], protein_dict['MW'], dist))
		question += ('<tr><td>{0}</td><td align="center">{1}</td><td align="center">{2:.2f}</td></tr>'.format("Unknown", "?", unknown_dist))
		question += "</table></p>"
		question += '<p>The standard and unknown proteins listed in the table were run using SDS&ndash;PAGE.</p>'
		question += '<p><b>Estimate the molecular weight of the unknown protein.</b></p>'

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
				print("{0}{1}. {2:.0f} kDa".format(prefix, letters[i], choices[i]))
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



