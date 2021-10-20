#!/usr/bin/env python

import os
import sys
import csv
import math
import numpy
import random

class GelMigration(object):
	def __init__(self):
		self.debug = True
		self.multiple_choice = True
		self.slope = 0.8
		self.intercept = 5.5
		self.min_base_pairs = 100
		self.max_base_pairs = 20000
		self.createDNA_Tree()


	#==================================================
	def isValidDNA_Size(self, num_base_pairs):
		num_zeros = math.floor(math.log10(num_base_pairs + 1))
		two_divisor = 10**(num_zeros - 1)

		first_two_digits = num_base_pairs // two_divisor
		second_digit = first_two_digits % 10
		if second_digit != 0 and second_digit != 5:
			return False

		other_digits = num_base_pairs % two_divisor
		if other_digits > 0:
			return False	

		#print(num_base_pairs, 10**num_zeros, first_two_digits, other_digits)
		return True

	#==================================================
	def getNearestValidDNA_Size(self, num_base_pairs):
		num_zeros = math.floor(math.log10(num_base_pairs + 1))
		two_divisor = 10**(num_zeros - 1)

		first_two_digits = int(math.ceil(num_base_pairs / two_divisor))
		first_digit = first_two_digits // 10
		second_digit = first_two_digits % 10
		if 2 < second_digit < 8:
			second_digit = 5
		else:
			second_digit = 0
		first_two_digits = first_digit * 10 + second_digit
		new_num_base_pairs = first_two_digits * two_divisor
		print(num_base_pairs, "-->", new_num_base_pairs)

		return new_num_base_pairs

	#==================================================
	def createDNA_Tree(self):
		self.dna_list = []
		min_value = self.min_base_pairs
		max_value = self.max_base_pairs + 1
		step_value = self.min_base_pairs
		for num_base_pairs in range(min_value, max_value, step_value):
			if self.isValidDNA_Size(num_base_pairs):
				self.dna_list.append(num_base_pairs)
		if self.debug is True:
			print("Created DNA {0:d} bands".format(len(self.dna_list)))
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
		return random.sample(self.dna_list, size)

	#==================================================
	def get_dna_set_for_gel(self):
		subset = self.random_subset(5)
		subset.sort()
		print(subset)
		return subset

	#==================================================
	def get_unknown(self, subset):
		array = numpy.array(subset, dtype=numpy.uint16)
		#print(array)
		logarray = numpy.log10(array)
		#print(logarray)
		diff = numpy.diff(logarray)
		#print(diff)
		arg = numpy.argmax(diff)
		#print(arg)
		#print(diff[arg])
		#print(array[arg], array[arg+1])
		#print(logarray[arg], logarray[arg+1])
		new_log_band = logarray[arg] + diff[arg]/2.0
		#print("new_log_band=", new_log_band)
		new_band = int(math.ceil(10**new_log_band))
		#print("new_band=", new_band)
		new_valid_band = self.getNearestValidDNA_Size(new_band)
		print("new_valid_band=", new_valid_band)
		mw_range = 10**math.floor(new_log_band) // 2
		unknown_dist = 0

		if self.debug is True:
			print("Unknown: MW = {0:.1f} +/- {1:.1f}; Dist = {2:.2f}".format(new_valid_band, mw_range, unknown_dist))
		return new_valid_band, unknown_dist, mw_range


	#==================================================
	def writeProblem(self, N=44):
		"""
		49. <p>The standard and unknown proteins listed in the table were run using SDS–PAGE.</p> <p><b>Estimate the molecular weight of the unknown protein.</b></p>
		A. 190 kDa	B. 320 kDa	C. 430 kDa	D. 520 kDa
		"""

		gel_set = self.get_dna_set_for_gel()
		unknown_mw, unknown_dist, mw_range = self.get_unknown(gel_set)

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



