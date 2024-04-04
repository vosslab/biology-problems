#!/usr/bin/env python3

# external python/pip modules
import os
import math
import random
import argparse

import bptools
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
	def sort_by_molecular_weight(self, a, b):
		if a['MW'] > b['MW']:
			return True
		return False

	def get_protein_set_for_gel(self, num_proteins=3):
		"""
		Selects a set of proteins for gel simulation from a pre-filtered list of proteins based on their molecular weight (MW).

		This function first selects a random subset of 24 proteins from the available protein list. It then sorts this subset by MW and
		picks proteins to create a varied set, ensuring a range of MWs that simulate a realistic gel migration pattern.

		Args:
			num_proteins (int): The number of proteins to select for the gel, excluding the smallest and largest proteins
				which are always included to ensure a range. Default is 3.

		Returns:
			list: A list of dictionaries, each representing a selected protein with its properties (including 'MW' for molecular weight).

		The selection process includes:
		- Picking one of the smallest proteins.
		- Picking one of the largest proteins.
		- Evenly spacing the remaining selections between the smallest and largest by logarithmic MW,
		aiming to simulate a realistic distribution of protein sizes in a gel.
		- The selected proteins are returned sorted by their MW to facilitate further processing.
		"""
		# Select a random protein_subset of 24 proteins from the pre-filtered list
		protein_subset = random.sample(self.protein_tree, 24)
		# Sort the selected protein_subset by molecular weight (MW) in ascending order
		protein_subset = sorted(protein_subset, key=lambda k: k['MW'])
		# Determine the number of proteins to pull for the initial selection

		# Initialize an empty list to hold the final set of proteins for the gel
		gel_set = []

		pull_size = 3
		# Remove and collect the first few elements
		first_few_entries = []
		for _ in range(pull_size):
			first_few_entries.append(protein_subset.pop(0))
		first_entry = random.choice(first_few_entries)
		gel_set.append(first_entry)
		min_log_mw = math.log(first_entry['MW'])

		# Remove and collect the last few elements
		last_few_entries = []
		for _ in range(pull_size):
			last_few_entries.append(protein_subset.pop(-1))
		last_entry = random.choice(last_few_entries)
		gel_set.append(last_entry)
		max_log_mw = math.log(last_entry['MW'])

		# Calculate the logarithmic slope between the smallest and largest proteins
		# This is used to evenly distribute the remaining protein selections
		log_slope = (max_log_mw - min_log_mw) / float(num_proteins)

		# Initialize variables for tracking the previous protein's MW and the protein itself
		prev_mw = 0
		prev_prot_dict = None
		# Initialize the index for calculating ideal MW of subsequent proteins
		index = 1
		# Calculate the ideal MW for the next protein selection
		ideal_mw = math.exp(log_slope * index + min_log_mw)
		# Debug print statement for ideal MW calculation
		if self.debug is True:
			print("ideal_mw = {0:.1f}".format(ideal_mw))

		# Iterate over the remaining proteins in the subset
		# proteins are sorted, so should work fine with only one for loop
		for protein_dict in protein_subset:
			current_mw = protein_dict['MW']
			# Continue accumulating proteins closer to the ideal MW
			if current_mw < ideal_mw:
				prev_prot_dict = protein_dict
				prev_mw = current_mw
				continue

			# Select the protein that is closest to the ideal MW
			if abs(ideal_mw - current_mw) < abs(ideal_mw - prev_mw):
				gel_set.append(protein_dict)
			else:
				gel_set.append(prev_prot_dict)

			# Increment the index and calculate the next ideal MW
			index += 1
			ideal_mw = math.exp(log_slope * index + min_log_mw)
			# Debug print statement for each iteration's ideal MW calculation
			if self.debug is True:
				print("ideal_mw = {0:.1f}".format(ideal_mw))
			# Break the loop if the desired number of proteins has been selected
			if index > num_proteins:
				break
			if ideal_mw > last_entry['MW']:
				break

		# Sort the final set of proteins by MW before returning
		gel_set = sorted(gel_set, key=lambda k: k['MW'])

		# Debug print the final set of proteins
		if self.debug is True:
			print("")
			import pprint
			pprint.pprint(gel_set)

		if len(gel_set) < num_proteins or len(gel_set) > num_proteins+1:
			print(f"ERROR: failed to get correct number of proteins {len(gel_set)} != {num_proteins}")
			return None

		return gel_set


	#==================================================
	def get_unknown(self, gel_set, gap=None):
		if gap is None:
			gap = random.randint(1,len(gel_set)-1)

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
		#low_unknown_mw =  self.distance_to_molecular_weight(unknown_dist - dist_range)
		#high_unknown_mw = self.distance_to_molecular_weight(unknown_dist + dist_range)
		#mw_range = (high_unknown_mw - low_unknown_mw)/4.0

		if self.debug is True:
			print("Unknown: MW = {0:.1f} +/- {1:.1f}; Dist = {2:.2f} +/- {3:.2f}".format(unknown_mw, mw_range, unknown_dist, dist_range))
		return unknown_mw, unknown_dist, mw_range, gap


	#==================================================
	def write_question(self, N: int, num_choices: int=4, question_type: str='mc'):
		"""
		49. <p>The standard and unknown proteins listed in the table were run using SDS–PAGE.</p> <p><b>Estimate the molecular weight of the unknown protein.</b></p>
		A. 190 kDa	B. 320 kDa	C. 430 kDa	D. 520 kDa
		"""

		gel_set = self.get_protein_set_for_gel(num_choices+1)
		if gel_set is None:
			return None
		print(len(gel_set))
		unknown_mw, unknown_dist, mw_range, gap = self.get_unknown(gel_set)

		question_text = ''
		question_text += " <h6>Gel Migration Problem</h6> "


		question_text += '<p>In this task, data from an SDS-PAGE experiment, where proteins are separated based on molecular weight, is provided. '
		question_text += 'The gel results table below shows some standard proteins with known molecular weights and one unknown protein.</p>'

		question_text += '<p><table cellpadding="2" cellspacing="2" style="text-align:center; border: 2px solid black; font-size: 14px;">'
		# Modified header row with light gray background and a border
		question_text += '<tr style="background-color: #f2f2f2; border-bottom: 3px solid grey;">'
		question_text += '<th>Protein Name</th><th>Molecular<br/>Weight (kDa)</th><th>Migration<br/>Distance (cm)</th></tr>'

		for protein_dict in gel_set:
			dist = self.molecular_weight_to_distance(protein_dict['MW'])
			question_text += f'<tr><td>{protein_dict["fullname"]} ({protein_dict["abbr"]})</td>'
			question_text += f'<td align="center">{protein_dict["MW"]:.1f}</td>'
			question_text += f'<td align="center">{dist:.2f}</td></tr>'

		# Add a distinctive style for the unknown protein row. Here, we add a thick border line above and a light yellow background color.
		question_text += '<tr style="border-top: 3px double gray; background-color: #fffacd;">'
		question_text += '  <td>Unknown</td>'
		question_text += '  <td align="center"><strong>?</strong></td>'
		question_text += f'  <td align="center">{unknown_dist:.2f}</td></tr>'
		question_text += "</table></p>"

		question_text += '<p>Estimate the molecular weight of the unknown protein by comparing its gel migration distance with those of the standards.</p>'

		if question_type == 'mc':
			choices_list = []
			answer_text = f'{unknown_mw:.0f} kDa'
			for i in range(num_choices):
				j = i+1
				if j == gap:
					continue
				mw, d, r, g = self.get_unknown(gel_set, j)
				choices_list.append(f'{mw:.0f} kDa')
				#choices_list.sort()
			choices_list.append(answer_text)
			choices_list = list(set(choices_list))
			choices_list.sort()
			if len(choices_list) < 3:
				return None
			return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

		return bptools.formatBB_NUM_Question(N, question_text, round(unknown_mw,3), mw_range)


#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-n', '--num_choices', type=int, default=5, help="Number of choices to create.")

	# Create a mutually exclusive group for question types
	question_group = parser.add_mutually_exclusive_group()
	# Add question type argument with choices
	question_group.add_argument('-q', '--question-type', dest='question_type', type=str,
		choices=('mc', 'fib'),
		help='Set the question type: multiple choice (mc) or fill-in-the-blank (fib).')
	# Add flags for multiple-choice and fill-in-the-blank question types
	question_group.add_argument('--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice.')
	question_group.add_argument('--fib', dest='question_type', action='store_const', const='fib',
		help='Set question type to fill-in-the-blank.')
	question_group.set_defaults(question_type='mc')

	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	gelm = GelMigration()

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 1
		for d in range(args.duplicates):
			complete_question = gelm.write_question(N, args.num_choices, args.question_type)
			if complete_question is not None:
				N += 1
				f.write(complete_question)
	bptools.print_histogram()


#======================================
#======================================
if __name__ == '__main__':
	main()

