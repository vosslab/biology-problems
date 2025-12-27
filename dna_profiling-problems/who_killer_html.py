#!/usr/bin/env python3

import sys
import math
import random

import bptools
import gellib

debug = None

# Define complexity styles
COMPLEXITY_STYLES = {
	'easy': {'num_suspects': 4, 'num_bands': 13},
	'medium': {'num_suspects': 5, 'num_bands': 24,},
	'hard': {'num_suspects': 9, 'num_bands': 36,}
}

#================
def init_gel_params(style):
	if style not in COMPLEXITY_STYLES:
		print(f"Error: Style '{style}' not recognized. Available styles are {', '.join(COMPLEXITY_STYLES.keys())}.")
		sys.exit(1)
	return COMPLEXITY_STYLES[style]

class RFLPClass:
	#=====================================
	"""Initialize RFLPClass"""
	def __init__(self, num_bands):
		self.num_bands = num_bands
		self.allbands = frozenset(range(self.num_bands))
		self.people = {}
		self.debug = True
		self.fail = {}

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
		killer.remove(min(killer))
		killer = frozenset(killer)

		# Generate 'blood' using the 'have_baby' function
		blood = set()
		blood.update(victim)
		blood.update(killer)
		blood = frozenset(blood)

		# Calculate derived sets
		canthave = frozenset(self.allbands - blood)
		central_canthave = set(canthave)
		max_central_canthave = max(9, math.sqrt(self.num_bands))
		central_canthave.remove(min(central_canthave))
		central_canthave.remove(max(central_canthave))
		while len(central_canthave) >= max_central_canthave:
			central_canthave.remove(min(central_canthave))
			central_canthave.remove(max(central_canthave))
		central_canthave = frozenset(central_canthave)
		neverhave = frozenset(canthave - central_canthave)
		self.validbands = set(self.allbands - neverhave)

		musthave = frozenset(blood - victim)
		ignore = frozenset(victim.intersection(blood))
		crime_diffs = frozenset(killer - victim)

		minimum_musthave = math.sqrt(len(victim))/2.0
		self.fail['minimum musthave'] = f"{minimum_musthave:.03f}"
		minimum_crime_diffs = math.sqrt(len(victim))
		self.fail['minimum crime_diffs'] = f"{minimum_crime_diffs:.03f}"


		# Check criteria
		if len(musthave) <= minimum_musthave:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. blood=", len(blood), blood)
				print(".. musthave=", len(musthave), musthave)
				print("The blood and victim are too similar.")
			self.fail['musthave'] = self.fail.get('musthave', 0) + 1
			return None

		if len(ignore) <= 2:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. blood=", len(blood), blood)
				print(".. ignore=", len(ignore), ignore)
				print("The blood and victim are too disimilar.")
			self.fail['ignore'] = self.fail.get('ignore', 0) + 1
			return None

		if len(canthave) >= len(blood)+2:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. blood=", len(blood), blood)
				print(".. canthave=", len(canthave), canthave)
				print("The number of cant have bands is too big.")
			self.fail['canthave-blood'] = self.fail.get('canthave-blood', 0) + 1
			return None

		if len(canthave) <= 2:
			if self.debug is True:
				print(".. suspect=", len(suspect), suspect)
				print(".. blood=", len(blood), blood)
				print(".. ignore=", len(ignore), ignore)
				print("The blood and suspect are too similar.")
			self.fail['canthave'] = self.fail.get('canthave', 0) + 1
			return None

		if len(crime_diffs) <= minimum_crime_diffs:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. killer=", len(killer), killer)
				print(".. crime_diffs=", len(crime_diffs), crime_diffs)
				print("The victim and killer are too similar.")
			self.fail['crime_diffs'] = self.fail.get('crime_diffs', 0) + 1
			return None

		if abs(len(victim) - len(killer)) / len(victim) >= 0.25:
			if self.debug is True:
				print(".. victim=", len(victim), victim)
				print(".. killer=", len(killer), killer)
				print("The victim and killer sets have lengths that differ by more than 25%.")
			self.fail['victim-killer'] = self.fail.get('victim-killer', 0) + 1
			return None

		if self.debug is True:
			print(".. self.validbands=", len(self.validbands), self.validbands)
			print(".. victim=", len(victim), victim)
			print(".. killer=", len(killer), killer)
			print(".. blood=", len(blood), blood)
			print(".. musthave=", len(musthave), musthave)
			print(".. canthave=", len(canthave), canthave)
			print(".. central_canthave=", len(central_canthave), central_canthave)
			print(".. neverhave", len(central_canthave), central_canthave)
			print(".. ignore=", len(ignore), ignore)

		self.people['victim'] = victim
		self.people['killer'] = killer
		self.people['blood'] = blood
		self.people['musthave'] = musthave
		self.people['canthave'] = canthave
		self.people['central_canthave'] = central_canthave
		self.people['ignore'] = ignore

		return victim, killer, blood

	#====================================
	def create_suspects(self, num_suspects=7):
		# Generate additional male DNA bands
		suspects_set = set()
		suspects_set.add(self.people.get('killer'))

		while len(suspects_set) < num_suspects:
			suspect_type_1 = self.create_suspect_type_1()
			suspect_type_2 = self.create_suspect_type_2()
			suspect_type_3 = self.create_suspect_type_3()
			suspects_set.add(suspect_type_1)
			suspects_set.add(suspect_type_2)
			suspects_set.add(suspect_type_3)

		if len(suspects_set) > num_suspects:
			suspects_set.remove(self.people.get('killer'))
			num_to_remove = len(suspects_set) - num_suspects + 1
			suspects_set -= set(random.sample(list(suspects_set), num_to_remove))
			suspects_set.add(self.people.get('killer'))

		suspects_list = list(suspects_set)
		random.shuffle(suspects_list)
		random.shuffle(suspects_list)
		if self.check_suspects(suspects_list) is False:
			return None
		self.people['suspects_list'] = suspects_list
		return suspects_list

	def create_suspect_type_1(self):
		"""
		type 1 suspects have:
			not killer: some missing musthave bands
			not killer: some extra central_canthave bands
		"""
		# Retrieve the 'canthave' and 'musthave' band sets from the 'people' attribute
		canthave = self.people.get('central_canthave')
		musthave = self.people.get('musthave')
		# Calculate the size of the suspect set based on a random percentage (between 30% and 40%) of total bands
		suspect_size = int(self.num_bands * random.uniform(0.3, 0.4))
		# Initialize 'suspect' as a random subset of 'validbands' with size 'suspect_size'
		suspect = set(random.sample(list(self.validbands), suspect_size))

		# Add bands to suspect that the actual killer cannot have from 'canthave'
		current_canthave = len(suspect.intersection(canthave))
		num_to_add_canthave = max(int(math.sqrt(len(canthave)))//2, 1)
		# Sample 'num_to_add_canthave' bands from 'canthave'
		add_canthave = random.sample(list(canthave), num_to_add_canthave)
		# Add these innocence proving bands to 'suspect'
		suspect.update(add_canthave)

		# Add most bands that the actual killer must have from 'musthave'
		# We will remove some of them in the next step to introduce uncertainty
		suspect.update(musthave)
		num_to_remove_musthave = max(int(math.sqrt(len(musthave))), 1)
		# Randomly sample 'num_to_remove_musthave' bands from 'musthave' and remove them from 'suspect'
		suspect -= set(random.sample(list(musthave), num_to_remove_musthave))
		# Now suspect is missing musthave bands, further proving their innocence
		# Return the finalized 'suspect' set as an immutable frozenset
		return frozenset(suspect)

	#====================================
	def create_suspect_type_2(self):
		"""
		type 2 suspects have:
			yes killer: all of the musthave bands
			not killer: some extra central_canthave bands
		"""
		# Retrieve the 'canthave' and 'musthave' band sets from the 'people' attribute
		canthave = self.people.get('central_canthave')
		musthave = self.people.get('musthave')
		# Calculate the size of the suspect set based on a random percentage (between 30% and 40%) of total bands
		suspect_size = int(self.num_bands * random.uniform(0.3, 0.4))
		# Initialize 'suspect' as a random subset of 'validbands' with size 'suspect_size'
		suspect = set(random.sample(list(self.validbands), suspect_size - len(musthave)))

		# Add bands to suspect that the actual killer cannot have from 'canthave'
		num_to_add_canthave = max(int(math.sqrt(len(canthave)))//2, 1)
		# Sample 'num_to_add_canthave' bands from 'canthave'
		add_canthave = random.sample(list(canthave), num_to_add_canthave)
		# Add these innocence proving bands to 'suspect'
		suspect.update(add_canthave)

		# Add all bands that the actual killer must have from 'musthave'
		suspect.update(musthave)
		# Return the finalized 'suspect' set as an immutable frozenset
		return frozenset(suspect)

	#====================================
	def create_suspect_type_3(self):
		"""
		type 3 suspects have:
			not killer: some missing musthave bands
			yes killer: none of the canthave bands
		"""
		# Retrieve the 'canthave' and 'musthave' band sets from the 'people' attribute
		canthave = self.people.get('canthave')
		musthave = self.people.get('musthave')
		# Calculate the size of the suspect set based on a random percentage (between 30% and 40%) of total bands
		suspect_size = int(self.num_bands * random.uniform(0.3, 0.4))
		# Initialize 'suspect' as a random subset of 'validbands' with size 'suspect_size'
		suspect = set(random.sample(list(self.validbands), suspect_size))

		# Find the overlap of canthave bands and the suspect
		overlap_canthave = suspect.intersection(canthave)
		# Remove all overlapping canthave bands 'suspect'
		suspect -= overlap_canthave

		# Add most bands that the actual killer must have from 'musthave'
		# We will remove some of them in the next step to introduce uncertainty
		suspect.update(musthave)
		# Calculate the number of 'musthave' bands to remove as the square root of the size of 'musthave', incremented by 1
		num_to_remove_musthave = max(int(math.sqrt(len(musthave))), 1)
		# Randomly sample 'num_to_remove_musthave' bands from 'musthave' and remove them from 'suspect'
		suspect -= set(random.sample(list(musthave), num_to_remove_musthave))
		# Now suspect is missing musthave bands, further proving their innocence

		# Return the finalized 'suspect' set as an immutable frozenset
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
		gel_class.createBandTree(self.num_bands)

		gel_class.blankLane()
		if self.debug is True:
			gel_class.drawLane(self.allbands, "allbands")
			gel_class.drawLane(self.validbands, "validbands")
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
			gel_class.drawLane(self.people.get('killer'), "killer")
			gel_class.drawLane(self.people.get('canthave'), "canthave")
			gel_class.drawLane(self.people.get('central_canthave'), "canthave*")
			gel_class.drawLane(self.people.get('musthave'), "musthave")
			gel_class.drawLane(self.people.get('ignore'), "ignore")
			gel_class.blankLane()
		gel_class.saveImage(f"suspects_{N:04d}.png")
		print("open suspects.png")
		return killer_index

	#================
	def make_suspects_HTML_table(self):
		gel_class = gellib.GelClassHtml()
		gel_class.createBandTree(self.num_bands)

		table = ""
		table += gel_class.tableWidths()
		table += gel_class.blankLane()
		if self.debug is True:
			table += gel_class.drawLane(self.allbands, "All Bands")
			table += gel_class.drawLane(self.validbands, "Valid Bands")
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
			table += gel_class.drawLane(self.people.get('killer'), "killer")
			table += gel_class.drawLane(self.people.get('canthave'), "canthave")
			table += gel_class.drawLane(self.people.get('central_canthave'), "canthave*")
			table += gel_class.drawLane(self.people.get('musthave'), "musthave")
			table += gel_class.drawLane(self.people.get('ignore'), "ignore")
			table += gel_class.blankLane()
		table += "</table> "
		return table, killer_index

#================
#================
def write_question(N, params, debug):
	# Initialization
	rflp_class = RFLPClass(params['num_bands'])
	rflp_class.debug = debug
	results = None
	attempts = 0
	while results is None:
		attempts += 1
		if attempts % 100 == 0:
			print(f"Still working on creating the crime scene, so far {attempts} attempts")
		if attempts > 10000:
			print(rflp_class.fail)
			print("too many attempts")
			sys.exit(1)
		results = rflp_class.create_crime_scene()
	print(f"Created Crime Scene in {attempts} attempts")
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
def write_question_wrapper(N, args):
	"""
	Wrapper for collect_and_write_questions that uses precomputed params.
	"""
	return write_question(N, args.params, args.debug)

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser(description="Generate DNA gel questions.")

	parser.add_argument('-D', '--debug', dest='debug', action='store_true',
		help='Enable debug mode, which changes the question output.')
	parser.set_defaults(debug=False)

	# Add an argument to specify the number of answer choices for each question
	parser = bptools.add_choice_args(parser, default=None)

	# Create a mutually exclusive group for style selection
	# This group allows only one complexity style to be specified at a time
	style_group = parser.add_mutually_exclusive_group()

	# Add an option to manually set the style
	style_group.add_argument(
		'-s', '--style', dest='style', type=str,
		choices=('easy', 'medium', 'hard'),
		help='Set the complexity style for generating questions: easy, medium, or hard'
	)

	# Add a shortcut option to set style to easy
	style_group.add_argument(
		'-E', '--easy', dest='style', action='store_const', const='easy',
		help='Set question style to easy'
	)

	# Add a shortcut option to set style to medium
	style_group.add_argument(
		'-M', '--medium', dest='style', action='store_const', const='medium',
		help='Set question style to medium'
	)

	# Add a shortcut option to set style to hard
	style_group.add_argument(
		'-H', '--hard', dest='style', action='store_const', const='hard',
		help='Set question style to hard'
	)

	parser.set_defaults(style='medium')
	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	params = init_gel_params(args.style)
	if args.num_choices is not None:
		params['num_suspects'] = args.num_choices
	args.params = params

	outfile = bptools.make_outfile(
		None,
		args.style.upper(),
		f"{params['num_suspects']}_suspects"
	)
	bptools.collect_and_write_questions(write_question_wrapper, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
