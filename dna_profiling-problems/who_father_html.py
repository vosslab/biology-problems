#!/usr/bin/env python3

import os
import sys
import copy
import math
import random
import argparse

import bptools
import gellib

debug = None

# Define complexity styles
COMPLEXITY_STYLES = {
	'easy': {'num_males': 3, 'num_bands': 14,},
	'medium': {'num_males': 5, 'num_bands': 24,},
	'hard': {'num_males': 9, 'num_bands': 36,}
}


class RFLPClass:
	#=====================================
	"""Initialize RFLPClass"""
	def __init__(self, num_bands):
		self.num_bands = num_bands
		self.allbands = set(range(self.num_bands))
		self.people = {}
		self.debug = True
		self.fail = {}

	#=====================================
	def create_family(self):
		"""
		This function aims to create unique DNA bands for a family consisting of a mother, a father, and a child.
		The function should adhere to specific criteria to ensure variability and similarity where required.

		Variables:
		- mother: set, DNA bands for the mother
		- father: set, DNA bands for the father
		- child: set, DNA bands for the child
		- allbands: set, all possible DNA bands
		- bothparents: set, intersection of bands between mother and father

		Derived Sets:
		- musthave: set, bands present in child but not in mother
		- ignore: set, bands common between mother and child
		- parent_diffs: set, bands unique to the father when compared to the mother

		Returns:
		- Tuple (mother, father, child) if all criteria are met
		- None otherwise
		"""
		# Sample sizes for mother and father sets. The child set will be derived from these.
		mother_size = int(self.num_bands * random.uniform(0.3, 0.4))
		father_size = int(mother_size * random.uniform(0.9, 1.1))

		# Populate 'mother' and 'father'
		mother = set(random.sample(list(self.allbands), mother_size))
		#always good to give first band to mom, otherwise makes problem a little too easy
		mother.add(0)
		mother = frozenset(mother)
		father = set(random.sample(list(mother), mother_size//2))
		father.update(random.sample(list(self.allbands - mother), father_size - len(father)))
		father = frozenset(father)
		parent_diffs = father - mother
		forced_unique = max(len(parent_diffs)//2, 1)

		# Generate 'child' using the 'have_baby' function
		child = self.have_baby(mother, father, forced_unique)

		# Calculate derived sets
		musthave = child - mother
		ignore = mother.intersection(child)

		minimum_musthave = math.sqrt(len(mother))/2.0
		self.fail['minimum musthave'] = f"{minimum_musthave:.03f}"
		minimum_parent_diffs = math.sqrt(len(mother))
		self.fail['minimum parent_diffs'] = f"{minimum_parent_diffs:.03f}"


		# Check criteria
		if len(musthave) < minimum_musthave:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. child=", len(child), child)
				print(".. musthave=", len(musthave), musthave)
				print("The child and mother are too similar.")
			self.fail['musthave'] = self.fail.get('musthave', 0) + 1
			return None

		if len(ignore) < 2:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. child=", len(child), child)
				print(".. ignore=", len(ignore), ignore)
				print("The child and mother are too disimilar.")
			self.fail['ignore'] = self.fail.get('ignore', 0) + 1
			return None

		if len(parent_diffs) <= minimum_parent_diffs:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. father=", len(father), father)
				print(".. parent_diffs=", len(parent_diffs), parent_diffs)
				print("The mother and father are too similar.")
			self.fail['parent_diffs'] = self.fail.get('parent_diffs', 0) + 1
			return None

		if abs(len(mother) - len(father)) / len(mother) >= 0.25:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. father=", len(father), father)
				print("The mother and father sets have lengths that differ by more than 25%.")
			self.fail['mother-father'] = self.fail.get('mother-father', 0) + 1
			return None

		if abs(len(mother) - len(child)) / len(mother) >= 0.25:
			if self.debug is True:
				print(".. mother=", len(mother), mother)
				print(".. child=", len(child), child)
				print("The mother and child sets have lengths that differ by more than 25%.")
			self.fail['mother-child'] = self.fail.get('mother-child', 0) + 1
			return None

		if self.debug is True:
			print(".. mother=", len(mother), mother)
			print(".. father=", len(father), father)
			print(".. child=", len(child), child)

		self.people['mother'] = mother
		self.people['father'] = father
		self.people['child'] = child
		self.people['musthave'] = musthave
		self.people['ignore'] = ignore

		return mother, father, child

	#====================================
	def have_baby(self, mother, father, forced_unique=2):
		child = set()
		# Adding bands from mother and father with 0.5 probability
		child.update(random.sample(list(mother), len(mother)//2))
		child.update(random.sample(list(father), len(father)//2))
		# Removing random bands from child
		removal_count = forced_unique*2
		child -= set(random.sample(list(child), min(removal_count, len(child)-1)))

		# Adding extra unique bands from both parents
		unique_from_mother = random.sample(list(mother - father), forced_unique)
		unique_from_father = random.sample(list(father - mother), forced_unique)
		child.update(unique_from_mother)
		child.update(unique_from_father)
		return frozenset(child)

	#====================================
	def create_additional_males(self, num_males=7):
		# Generate additional male DNA bands
		males_set = set()
		males_set.add(self.people.get('father'))
		musthave = self.people.get('musthave')
		for i, exclude_band in enumerate(list(musthave)):
			male_type_1 = self.create_male_type_1(exclude_band)
			if male_type_1 is not None:
				males_set.add(male_type_1)
				if self.debug is True:
					print(".. exclude_band=", exclude_band)
					print(f".. type 1 male {i+1}=", len(male_type_1), male_type_1)
		print(f"Created {len(males_set)} type 1 males")

		# Generate additional males with random changes in DNA bands
		while len(males_set) < num_males:
			male_type_2 = self.create_male_type_2()
			if male_type_2 is not None:
				males_set.add(male_type_2)
				if self.debug is True:
					print(f".. type 2 male {len(males_set)+1}=", len(male_type_2), male_type_2)
		if len(males_set) > num_males:
			males_set.remove(self.people.get('father'))
			num_to_remove = len(males_set) - num_males + 1
			males_set -= set(random.sample(list(males_set), num_to_remove))
			males_set.add(self.people.get('father'))
		print(f"Created {len(males_set)} total males")
		males_list = list(males_set)
		random.shuffle(males_list)
		random.shuffle(males_list)
		if self.check_males(males_list) is False:
			return None
		self.people['males_list'] = males_list
		return males_list

	#====================================
	def check_males(self, males_list):
		dadcount = 0
		for i, male in enumerate(males_list):
			if self.is_father(male) is True:
				dadcount += 1
		if dadcount == 0:
			print("no fathers in list")
			return False
		elif dadcount > 1:
			print(f"too many fathers in list: {dadcount}")
			return False
		return True

	#====================================
	def create_male_type_1(self, exclude_band):
		# contains all but one of the must have bands
		musthave = self.people.get('musthave')
		child = self.people.get('child')
		male_type_1 = set(copy.copy(musthave))
		male_type_1.update(random.sample(list(child), len(child)//2+1))
		male_type_1.update(random.sample(list(self.allbands), len(child)//2+1))
		male_type_1.remove(exclude_band)
		if self.is_father(male_type_1) is True:
			return None
		return frozenset(male_type_1)

	#====================================
	def create_male_type_2(self):
		musthave = self.people.get('musthave')
		male_type_2 = set(copy.copy(musthave))
		for i in range(len(self.people.get('child'))+1):
			male_type_2.add(random.choice(list(self.allbands)))
		male_type_2.remove(random.choice(list(musthave)))
		if self.is_father(male_type_2) is True:
			return None
		return frozenset(male_type_2)

	#================
	def make_unknown_males_PNG_image(self, N=1):
		# Initialization
		gel_class = gellib.GelClassImage()
		gel_class.createBandTree(self.num_bands)
		gel_class.setTextColumn("Must Have")
		if self.debug is True:
			gel_class.drawLane(self.allbands, "allbands")
			gel_class.blankLane()
		gel_class.drawLane(self.people.get('mother'), "Mother")
		gel_class.drawLane(self.people.get('child'), "Child")
		males_list = self.people.get('males_list')
		gel_class.blankLane()
		dadcount = 0
		for i, male in enumerate(males_list):
			if self.is_father(male) is True:
				dadcount += 1
				answer_index = i
			gel_class.drawLane(male, "Male %d"%(i+1))
		if dadcount != 1:
			print("wrong number of fathers")
			sys.exit(1)
		gel_class.blankLane()
		if self.debug is True:
			gel_class.drawLane(self.people.get('father'), "Father")
			gel_class.drawLane(self.people.get('musthave'), "Must Have")
			gel_class.drawLane(self.people.get('ignore'), "Ignore")
			gel_class.blankLane()
		gel_class.blankLane()
		gel_class.saveImage(f"males_{N:04d}.png")
		print("open males.png")
		return answer_index

	#================
	def make_unknown_males_HTML_table(self):
		# Initialization
		gel_class = gellib.GelClassHtml()
		gel_class.createBandTree(self.num_bands)

		mother = self.people.get('mother')
		child = self.people.get('child')
		table = ""
		table += gel_class.tableWidths()
		#table += gel_class.drawLane(list(allbands), "allbands")
		table += gel_class.blankLane()
		table += gel_class.drawLane(sorted(mother), "Mother")
		table += gel_class.drawLane(sorted(child), "Child")
		males_list = self.people.get('males_list')
		dadcount = 0
		for i, male in enumerate(males_list):
			if self.is_father(male) is True:
				dadcount += 1
				answer_index = i
			#print(("Male #%d: %s -- %s"%(i+1, str(sorted(male)), isfather)))
			table += gel_class.drawLane(male, "Male %d"%(i+1))
		if dadcount != 1:
			print("wrong number of fathers")
			return None
		table += gel_class.blankLane()
		if self.debug is True:
			table += gel_class.drawLane(self.people.get('father'), "Father")
			table += gel_class.drawLane(self.people.get('musthave'), "musthave")
			table += gel_class.drawLane(self.people.get('ignore'), "ignore")
			table += gel_class.blankLane()
		table += "</table>"
		return table, answer_index

	#====================================
	def is_father(self, male):
		#1. Everyone of the child's bands must come from a parent; Account for each band in the child
		#2. Only some bands from each parent are present in the child; A parent's band presence doesn't guarantee it's in the child
		#3. If the child has a band that the mother is missing, it must come from the father
		# Check if the male is the father based on the set difference
		if len(self.people.get('musthave') - male) == 0:
			return True
		return False


#================
def init_gel_params(style):
	if style not in COMPLEXITY_STYLES:
		print(f"Error: Style '{style}' not recognized. Available styles are {', '.join(COMPLEXITY_STYLES.keys())}.")
		sys.exit(1)
	return COMPLEXITY_STYLES[style]

#================
#================
def writeQuestion(N, params, debug):
	# Initialization
	rflp_class = RFLPClass(params['num_bands'])
	rflp_class.debug = debug
	results = None
	attempts = 0
	while results is None:
		attempts += 1
		if attempts % 100 == 0:
			print(f"Still working on creating the Family, so far {attempts} attempts")
		if attempts > 10000:
			print(rflp_class.fail)
			print("too many attempts")
			sys.exit(1)
		results = rflp_class.create_family()
	print(f"Created Family in {attempts} attempts")
	mother, father, child = results
	# Create additional males
	males = rflp_class.create_additional_males(params['num_males'])

	# Generate the HTML table
	table, answer_index = rflp_class.make_unknown_males_HTML_table()
	rflp_class.make_unknown_males_PNG_image(N)

	# Define the sub-headings and questions as HTML
	the_question = "<h6>The Question</h6><p>Who is the father of the child?</p>"
	background = "<h6>Background</h6><p>Restriction Fragment Length Polymorphism (RFLP) is a molecular biology technique used to distinguish between closely related DNA samples. It's commonly employed in paternity tests, among other applications.</p>"
	instructions = "<h6>Instructions</h6><p>Use the provided DNA gel profile to determine paternity. Each band in the gel corresponds to a DNA fragment. Fragments are inherited; thus, the child's DNA will have overlapping fragments with the true father.</p>"
	# Add a disclaimer
	legal_disclaimer = "<h6>Disclaimer</h6><p>In actual diagnostic processes, the results of RFLP for confirming paternity are often cited to provide a 99.9% accuracy level or higher. However, no test is foolproof. Legal confirmation may involve additional procedures and evaluations to ensure the integrity and admissibility of the test.</p>"

	# Combine all elements to form the full question
	full_question = "{0} {1} {2} {3} {4}".format(the_question, table, background, legal_disclaimer, instructions)

	print(params)

	choices_list = []
	for i, male in enumerate(males):
		choice = "Male &num;{0:d}".format(i+1)
		choices_list.append(choice)
		if i == answer_index:
			answer_string = choice
	bb_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_string)
	return bb_question

#================
#================
if __name__ == '__main__':
	# Command-line argument parsing moved here
	parser = argparse.ArgumentParser(description="Generate DNA gel questions.")
	parser.add_argument('-s', '--style', type=str, default='medium',
		help='The complexity style for generating questions (easy, medium, hard)')
	parser.add_argument('-d', '--debug', dest='debug', action='store_true',
		help='Enable debug mode, which changes the question output.')
	parser.add_argument('-x', '--max_questions', dest='max_questions', type=int, default=3,
		help='Number of questions to write')
	parser.set_defaults(debug=False)

	args = parser.parse_args()
	params = init_gel_params(args.style)

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')
	with open(outfile, 'w') as f:
		for i in range(args.max_questions):
			N = i + 1
			print(f"\nQuestion {N} of {args.max_questions}")
			bb_question = writeQuestion(N, params, args.debug)
			if bb_question is None:
				continue
			f.write(bb_question)
		f.write("\n")
	bptools.print_histogram()
