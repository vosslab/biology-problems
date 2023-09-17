#!/usr/bin/env python3

import os
import sys
import math
import random
import argparse

import bptools
import gellib

debug = None

# Define complexity styles
COMPLEXITY_STYLES = {
	'easy': {'num_suspects': 3, 'num_bands': 27,},
	'medium': {'num_suspects': 5, 'num_bands': 24,},
	'hard': {'num_suspects': 9, 'num_bands': 32,}
}

class RFLPClass:
	#=====================================
	"""Initialize RFLPClass"""
	def __init__(self, num_bands):
		self.num_bands = num_bands
		self.allbands = frozenset(range(self.num_bands))
		self.people = {}
		self.debug = True

	#=====================================
	def create_crime_scene(self):
		"""
		This function aims to create unique DNA bands for a family consisting of a victim, a killer, and a blood.
		The function should adhere to specific criteria to ensure variability and similarity where required.

		Variables:
		- victim: set, DNA bands for the victim
		- killer: set, DNA bands for the killer
		- blood: set, DNA bands for the blood
		- allbands: set, all possible DNA bands
		- bothparents: set, intersection of bands between victim and killer

		Derived Sets:
		- musthave: set, bands present in blood but not in victim
		- ignore: set, bands common between victim and blood
		- parent_diffs: set, bands unique to the killer when compared to the victim

		Returns:
		- Tuple (victim, killer, blood) if all criteria are met
		- None otherwise
		"""
		# Sample sizes for victim and killer sets. The blood set will be derived from these.
		victim_size = int(self.num_bands * random.uniform(0.3, 0.4))
		killer_size = int(victim_size * random.uniform(0.9, 1.1))

		# Populate 'victim' and 'killer'
		victim = frozenset(random.sample(list(self.allbands), victim_size))
		killer = set(random.sample(list(victim), victim_size//2))
		killer.update(random.sample(list(self.allbands - victim), killer_size - len(killer)))
		killer = frozenset(killer)

		# Generate 'blood' using the 'have_baby' function
		blood = set()
		blood.update(victim)
		blood.update(killer)
		blood = frozenset(blood)

		# Calculate derived sets
		canthave = frozenset(self.allbands - blood)
		musthave = frozenset(blood - victim)
		ignore = frozenset(victim.intersection(killer))
		crime_diffs = frozenset(killer - victim)

		# Check criteria
		if len(musthave) <= 2:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. blood=", len(blood), blood)
				print(".. musthave=", len(musthave), musthave)
				print("The blood and victim are too similar.")
			return None

		if len(ignore) <= 2:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. blood=", len(blood), blood)
				print(".. ignore=", len(ignore), ignore)
				print("The blood and victim are too disimilar.")
			return None

		if len(canthave) <= 2:
			if self.debug is True:
				print(".. suspect=", len(suspect), suspect)
				print(".. blood=", len(blood), blood)
				print(".. ignore=", len(ignore), ignore)
				print("The blood and suspect are too similar.")
			return None

		if len(crime_diffs) <= 4:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. killer=", len(killer), killer)
				print(".. crime_diffs=", len(crime_diffs), crime_diffs)
				print("The victim and killer are too similar.")
			return None

		if abs(len(victim) - len(killer)) / len(victim) >= 0.25:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. killer=", len(killer), killer)
				print("The victim and killer sets have lengths that differ by more than 25%.")
			return None

		if self.debug is True:
			print(".. victim=", len(victim), victim)
			print(".. killer=", len(killer), killer)
			print(".. blood=", len(blood), blood)

		self.people['victim'] = victim
		self.people['killer'] = killer
		self.people['blood'] = blood
		self.people['musthave'] = musthave
		self.people['canthave'] = canthave
		self.people['ignore'] = ignore

		return victim, killer, blood

	#====================================
	def create_suspects(self, num_suspects=7):
		# Generate additional male DNA bands
		suspects_set = set()
		suspects_set.add(self.people.get('killer'))

		while len(suspects_set) < num_suspects:
			# add a suspect with 1 band extra
			suspect = self.create_suspect_type_1()
			suspects_set.add(suspect)

		suspects_list = list(suspects_set)
		random.shuffle(suspects_list)
		random.shuffle(suspects_list)
		if self.check_suspects(suspects_list) is False:
			return None
		self.people['suspects_list'] = suspects_list
		return suspects_list

	#====================================
	def create_suspect_type_1(self):
		canthave = self.people.get('canthave')
		musthave = self.people.get('musthave')
		suspect_size = int(self.num_bands * random.uniform(0.3, 0.4))
		suspect = set(random.sample(list(self.allbands), suspect_size))
		# add a suspect with 1 band extra
		## add all musthaves
		suspect.update(musthave)
		remove_canthave = int(math.sqrt(len(canthave)))+1
		suspect.update(random.sample(list(canthave), remove_canthave))
		remove_musthave = int(math.sqrt(len(musthave)))+1
		suspect -= set(random.sample(list(musthave), remove_musthave))
		return frozenset(suspect)

	#====================================
	def check_suspects(self, suspects_list):
		killer_count = 0
		for i, suspect in enumerate(suspects_list):
			if self.is_killer(suspect) is True:
				killer_count += 1
		if killer_count == 0:
			print("no killers in list")
			return False
		elif killer_count > 1:
			print(f"too many killers in list: {killer_count}")
			return False
		return True

	#====================================
	def is_killer(self, suspect):
		#1. All bands in the crime scene sample must come from the victim or the criminal; Account for each band in the blood sample
		#2. All bands from both the criminal and victim are present in the crime scene sample; Suspect is innocent if their band is absent in the sample
		#3. If a band from the crime scene isn't present in the victim, the criminal must have that band
		#killer must have all bands
		victim = self.people.get('victim')
		blood = self.people.get('blood')
		if (blood - victim) == (suspect - victim):
			return True
		return False

	#================
	def make_suspects_PNG_image(self, N=1):
		gel_class = gellib.GelClassImage()
		gel_class.setTextColumn("Suspect #5")
		gel_class.createBandTree(params['num_bands'])

		gel_class.blankLane()
		if self.debug is True:
			gel_class.drawLane(self.allbands, "allbands")
			gel_class.blankLane()
		gel_class.drawLane(self.people.get('victim'), "Victim")
		gel_class.drawLane(self.people.get('blood'), "Blood")
		killer_count = 0
		suspects_list = self.people.get('suspects_list')
		for i, suspect in enumerate(suspects_list):
			gel_class.drawLane(suspect, "Suspect #{0:d}".format(i+1))
			if self.is_killer(suspect):
				killer_index = i
				killer_count += 1
		if killer_count != 1:
			"wrong number of killers"
			return None
		gel_class.blankLane()
		if self.debug is True:
			gel_class.drawLane(self.people.get('canthave'), "canthave")
			gel_class.drawLane(self.people.get('musthave'), "musthave")
			gel_class.drawLane(self.people.get('ignore'), "ignore")
			gel_class.blankLane()
		gel_class.saveImage(f"suspects_{N:04d}.png")
		print("open suspects.png")
		return killer_index

	#================
	def make_suspects_HTML_table(self):
		gel_class = gellib.GelClassHtml()
		gel_class.createBandTree(params['num_bands'])

		table = ""
		table += gel_class.tableWidths()
		table += gel_class.blankLane()
		if self.debug is True:
			table += gel_class.drawLane(self.allbands, "All Bands")
			table += gel_class.blankLane()
		table += gel_class.drawLane(self.people.get('victim'), "Victim")
		table += gel_class.drawLane(self.people.get('blood'), "Blood")

		killer_count = 0
		suspects_list = self.people.get('suspects_list')
		for i, suspect in enumerate(suspects_list):
			table += gel_class.drawLane(suspect, "Suspect &num;{0:d}".format(i+1))
			if self.is_killer(suspect):
				killer_index = i
				killer_count += 1
		if killer_count != 1:
			"wrong number of killers"
			return None
		table += gel_class.blankLane()
		if self.debug is True:
			table += gel_class.drawLane(self.people.get('canthave'), "canthave")
			table += gel_class.drawLane(self.people.get('musthave'), "musthave")
			table += gel_class.drawLane(self.people.get('ignore'), "ignore")
			table += gel_class.blankLane()
		table += "</table> "
		return table, killer_index

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
	while results is None:
		results = rflp_class.create_crime_scene()
	victim, killer, blood = results
	# Create additional males
	rflp_class.create_suspects(params['num_suspects'])

	# Generate the HTML table
	table, killer_index = rflp_class.make_suspects_HTML_table()
	rflp_class.make_suspects_PNG_image(N)

	# Define the sub-headings and questions as HTML
	the_question = "<h6>The Question</h6><p>Based on the DNA gel profile, which suspect left blood at the crime scene?</p>"
	background = "<h6>Background</h6><p>Restriction Fragment Length Polymorphism (RFLP) is a molecular biology technique employed to differentiate between closely related DNA samples. This technique is frequently used in forensic investigations to identify individuals.</p>"
	instructions = "<h6>Instructions</h6><p>Utilize the provided DNA gel profile to identify the perpetrator. Each band in the gel represents a DNA fragment. The perpetrator's DNA will display overlapping fragments with the blood sample found at the crime scene.</p>"

	# Define the sub-headings and questions as HTML
	background = "<h6>Background</h6><p>Restriction Fragment Length Polymorphism (RFLP) is a molecular biology method used to differentiate between closely related DNA samples. It is often used in forensic investigations.</p>"
	the_question = "<h6>The Question</h6><p>Which suspect left blood at the crime scene?</p>"
	legal_disclaimer = "<h6>Disclaimer</h6><p>In adherence to the principles of due process, all individuals in this exercise shall be presumed innocent until proven guilty beyond a reasonable doubt in a court of law.</p>"
	instructions = "<h6>Instructions</h6><p>Examine the provided DNA gel profile to identify which suspect is responsible for leaving the blood sample. Each band in the gel signifies a DNA fragment. The killer's DNA will match with the blood sample found at the crime scene.</p>"

	# Combine all elements to form the full question
	full_question = "{0} {1} {2} {3} {4}".format(the_question, table, background, legal_disclaimer, instructions)


	choices_list = []
	answer_string = ''
	suspects_list = rflp_class.people.get('suspects_list')
	for i, suspect in enumerate(suspects_list):
		choice = "Suspect &num;{0}".format(i+1)
		choices_list.append(choice)
		if i == killer_index:
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
			bb_question = writeQuestion(N, params, args.debug)
			if bb_question is None:
				continue
			f.write(bb_question)
		f.write("\n")
	bptools.print_histogram()
