#!/usr/bin/env python

import sys
import csv
import math
import random
import proteinlib

debug = False

class GelMigration(object):
	def __init__(self):
		self.debug = True
		proteinlib.debug = self.debug
		self.slope = 1
		self.intercept = 1
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
		dist = math.log(mw)*self.slope + self.intercept
		return dist

	#==================================================
	def writeQuestion(self, protein_dict=None, N=44):
		if protein_dict is None:
			protein_dict = self.protein_tree[1]
		question = "\n"
		question += "{0:d}. <h6>Gel Migration Problem</h6> ".format(N)
		question += ('<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">')
		question += ('<tr><th>Protein Name</th><th>molecular<br/>weight (kDa)</th><th>migration<br/>distance (cm)</th></tr>')
		dist = self.molecular_weight_to_distance(protein_dict['MW'],)
		question += ('<tr><td>{0} ({1})</td><td align="center">{2:.1f}</td><td align="center">{3:.1f}</td></tr>'.format(protein_dict['fullname'], protein_dict['abbr'], protein_dict['MW'], dist))
		question += "</table>"
		question += '<p>The protein in the table (above) is placed in a buffer solution with a pH of {0:.1f}.</p> '.format(0)
		#question += '<p>Check all of the answers below that apply. </p> '
		question += '<p>What is the correct net charge on the {0} protein at <b>pH of {1:.1f}</b>? '.format(protein_dict['abbr'], 0)
	
		'<span style="color:darkblue">'
		'<span style="color:darkred">'

		low_pH_answers = []
		high_pH_answers = []
		return question


	#==================================================
	def printQuestion(question, answers, wrongs):
		letters = "ABCDEFGH"
		print(question)

		for i in range(len(answers)):
			item_number = 2*i
			if random.random() < 0.5:
				print("*{0}. {1}".format(letters[2*i], answers[i]))
				print("{0}. {1}".format(letters[2*i+1], wrongs[i]))
			else:
				print("{0}. {1}".format(letters[2*i], wrongs[i]))
				print("*{0}. {1}".format(letters[2*i+1], answers[i]))
		print("{0}. {1}".format(letters[2*i+2], wrongs[-1]))


#==================================================
#==================================================
if __name__ == '__main__':
	question_count = 0
	gelm = GelMigration()
	question = gelm.writeQuestion()
	print(question)

	sys.exit(1)
	protein_tree = parse_protein_file()
	answer_count = {1:0, 2:0, 3:0, 4:0}

	for protein_dict in protein_tree:
		pI = protein_dict['pI']
		low_pH = math.floor(2*pI)/2. - 1
		high_pH = math.ceil(2*pI)/2. + 1

		for pH in (low_pH, high_pH):
			if pH < 2 or pH > 12:
				continue
			question_count += 1
			question, answers, wrongs = writeQuestion(protein_dict, pH, question_count)
			printQuestion(question, answers, wrongs)


