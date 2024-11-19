#!/usr/bin/env python3

# Standard Library
import os
import random
import argparse

# Local repo modules
import bptools
import tetradlib
import genemaplib as gml
import phenotypes_for_yeast

debug = True



#===========================================================
#===========================================================
def get_question_header():
	"""
	Returns the introductory context of the problem for unordered tetrad three-gene mapping.
	"""
	header = '<h5>Unordered Tetrad Two Gene Mapping</h5>'
	header += '<p>In this problem, you will use unordered tetrads to determine the between a single pair of genes '
	header += 'and calculate the distances between them. The yeast <i>Saccharomyces cerevisiae</i> is used in this study. '
	header += 'A cross has been performed to study the linkage relationships among two genes, '
	header += 'and the resulting genotypes are summarized in the table below.</p>'
	if gml.is_valid_html(header) is False:
		print(header)
		raise ValueError
	return header

#===========================================================
#===========================================================
def get_important_tips():
	"""
	Returns the HTML formatted hints for solving the problem.

	Returns:
		str: HTML formatted string with hints.
	"""
	tips = '<h6>Important Answer Guidelines</h6>'
	tips += '<p><ul>'
	tips += '<li><i>Important Tip 1:</i> '
	tips += '  Your calculated distance between the pair of genes should be a whole number. '
	tips += '  Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
	tips += '  Please provide your answer as a complete number without fractions or decimals.</li>'
	tips += '<li><i>Important Tip 2:</i> '
	tips += '  Your answer should be written as a numerical value only, '
	tips += '  with no spaces, commas, or units such as "cM" or "map units". '
	tips += '  For example, if the distance is fifty one centimorgans, simply write "51".</li>'
	tips += '</ul></p>'
	if gml.is_valid_html(tips) is False:
		print(tips)
		raise ValueError
	return tips

#===========================================================
#===========================================================
def get_question_footer_steps():
	"""
	Returns the HTML formatted step-by-step instructions for solving the problem.

	Returns:
		str: HTML formatted string with step-by-step instructions.
	"""
	steps = '<h6>Step-by-Step Instructions</h6>'
	steps += '<ul>'
	steps += ' <li>Step 1: Find the row for the Parental Type for all three genes.</li>'
	steps += ' <li>Step 2: Looking at only your two genes, assign PD, NPD, TT.</li>'
	steps += ' <li>Step 3: Determine if the two genes are linked.</li>'
	steps += '   <ul><li>PD &gt;&gt; NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	steps += ' <li>Step 4: Determine the map distance between the two genes.</li>'
	steps += '   <ul><li>D = &half; (TT + 6 NPD) / total = (3 NPD + &half; TT) / total</li></ul>'
	steps += '</ul>'
	if gml.is_valid_html(steps) is False:
		print(steps)
		raise ValueError
	return steps

#====================================
def construct_progeny_counts(distance: int, progeny_size_int: int) -> dict:
	"""
	Constructs a dictionary with counts of different progeny types (Parental Ditype, Tetratype,
	and Non-Parental Ditype) based on the given genetic distance.

	Args:
		distance (float): The genetic distance between genes or to the centromere (in centiMorgans).
		progeny_size_int (int): Total number of progeny (tetrads) to simulate.

	Returns:
		dict: A dictionary with counts for 'pd' (Parental Ditype), 'tt' (Tetratype), and 'npd' (Non-Parental Ditype).

	Raises:
		ValueError: If the criteria for gene distances are not met.
	"""
	# For "linked" questions, it represents the distance between two genes.

	# For linked genes, Tetratype (TT) and Non-Parental Ditype (NPD) counts are calculated based on single (SCO)
	# and double crossovers (DCO).
	# SCO (Single Crossover) count is proportional to the distance between genes.
	sco_count = int(distance * progeny_size_int) // 100

	# DCO (Double Crossover) count is based on the square of the distance (distance^2) to capture rare events.
	dco_count = int(distance ** 2 * progeny_size_int) // 10000

	# Calculate Non-Parental Ditype (NPD) and Tetratype (TT) counts using SCO and DCO values.
	non_parental_ditype_count = int(round(dco_count / 4))
	# distance*prog = TT/2 + 3*NPD
	# TT = 2 * (distance*prog - 3*NPD)
	# TT = 2 * (sco_count - 3*NPD)
	#tetratype_count = sco_count + dco_count // 2
	tetratype_count = 2 * (sco_count - 3 * non_parental_ditype_count)
	parental_ditype_count = progeny_size_int - non_parental_ditype_count - tetratype_count


	#double check the distance value
	distance_calc = (tetratype_count/2 + 3*non_parental_ditype_count)*100/progeny_size_int
	print(f'distance_calc = {distance_calc:.4f} and {distance:.4f}')
	if abs(distance_calc - distance) > 0.04:
		print("ROUNDING ERROR")
		return None

	if tetratype_count > parental_ditype_count:
		raise ValueError(f"tetratype_count > parental_ditype_count: {tetratype_count} > {parental_ditype_count}")
		return None

	# Return a dictionary with counts for each progeny type.
	progeny_type_count_dict = {
		'pd': parental_ditype_count,
		'tt': tetratype_count,
		'npd': non_parental_ditype_count,
	}
	if debug:
		import pprint
		pprint.pprint(progeny_type_count_dict)

	return progeny_type_count_dict

#====================================
def assign_tetrads(progeny_type_count_dict: dict, gene_letters_str: str) -> dict:
	"""
	Assigns specific tetrad types to progeny type counts (PD, TT, NPD) based on gene letters.

	This function randomly assigns ditype (PD and NPD) and tetratype (TT) configurations for the given genes.

	Args:
		progeny_type_count_dict (dict): Dictionary with counts for 'pd' (Parental Ditype), 'tt' (Tetratype),
			and 'npd' (Non-Parental Ditype).
		gene_letters_str (str): Gene symbols (e.g., "ab" or "xy").

	Returns:
		dict: A dictionary mapping specific tetrad configurations to their counts.
	"""

	# Get two possible ditype tetrads for the given two gene letters (PD and NPD configurations).
	ditype_tetrads = tetradlib.get_all_ditype_tetrads(gene_letters_str)
	# Shuffle to randomize which ditype is PD and which is NPD
	random.shuffle(ditype_tetrads)
	parental_ditype = ditype_tetrads[0]
	non_parental_ditype = ditype_tetrads[1]

	# Get the single tetratype configuration (TT) for the given two gene letters.
	tetratype_tetrads = tetradlib.get_all_tetratype_tetrads(gene_letters_str)
	tetratype = tetratype_tetrads[0]

	# Map each specific tetrad type to its count from progeny_type_count_dict.
	progeny_tetrads_count_dict = {
		parental_ditype: progeny_type_count_dict['pd'],
		tetratype: progeny_type_count_dict['tt'],
		non_parental_ditype: progeny_type_count_dict['npd'],
	}
	return progeny_tetrads_count_dict

#=====================
#=====================
def make_choices(progeny_type_count_dict, distance_int, num_choices):
	"""
	Generates a list of answer choices describing the genetic distance between two genes.

	This function calculates the correct answer and generates a list of plausible wrong answers
	based on different combinations of Tetratype (TT) and Non-Parental Ditype (NPD) values.
	The goal is to produce enough diverse choices to populate a multiple-choice question.

	Args:
		progeny_type_count_dict (dict): A dictionary with counts for Parental Ditype ('pd'), Tetratype ('tt'),
			and Non-Parental Ditype ('npd').
		distance_int (int): The correct genetic distance, used to verify the generated answer.
		num_choices (int): The total number of answer choices to generate.

	Returns:
		tuple: A list of formatted answer choices and the correct answer text.
	"""

	# Extract progeny counts for each tetrad type
	parent_count = progeny_type_count_dict['pd']
	tetratype_count = progeny_type_count_dict['tt']
	npd_count = progeny_type_count_dict['npd']
	total_progeny_count = parent_count + tetratype_count + npd_count

	# Generate the correct answer based on given TT and NPD values
	answer_text, correct_distance = tetradlib.tetrad_calculation_string(
		[tetratype_count], [npd_count], total_progeny_count
	)
	if abs(correct_distance * 100 - distance_int) > 0.04:
		raise ValueError("The correct answer calculation does not match the expected distance.")

	choices_list = []

	# Helper function to add a choice if it's unique and plausible
	def add_choice(tt_values, npd_values):
		"""
		Calculates the genetic distance for given TT and NPD counts, and adds the choice
		to the list if it meets certain criteria.

		Args:
			tt_values (list): List of TT counts used for this choice.
			npd_values (list): List of NPD counts used for this choice.
		"""
		choice_text, distance = tetradlib.tetrad_calculation_string(tt_values, npd_values, total_progeny_count)
		if distance < 0.7:
			choices_list.append(choice_text)


	# Add the wrong choices based on different PD, TT, and NPD combinations
	# These choices are constructed based on common mistakes or misinterpretations students might make.

	# Choices that include only NPD
	add_choice([0], [npd_count])            # Only NPD, no TT or PD
	add_choice([npd_count], [npd_count])    # Full NPD in both TT and NPD fields
	add_choice([npd_count], [0])

	# Choices that include PD to test if the student incorrectly assumes it should be included
	add_choice([parent_count], [0])         # Only PD, no TT or NPD
	add_choice([parent_count], [npd_count]) # PD and NPD, no TT

	# Choices that include only TT, testing the student assumption around TT-only scenarios
	add_choice([tetratype_count], [0])      # Only TT, no NPD or PD

	# Final catch-all: add combinations with mixed TT and NPD counts, even if unlikely
	add_choice([tetratype_count, parent_count], [npd_count]) # Combination that is likely to fail 0.6 max

	#likely to fail the 0.6 max
	add_choice([npd_count], [tetratype_count]) # NPD in TT field, and TT in NPD field
	add_choice([0], [tetratype_count])

	# Limit the list to the specified number of choices (num_choices - 1 for wrong choices)
	if len(choices_list) > num_choices - 1:
		choices_list = random.sample(choices_list, num_choices - 1)
	# Add the correct answer to the list and shuffle the order
	choices_list.append(answer_text)
	random.shuffle(choices_list)

	return choices_list, answer_text


#===========================
def generate_question(N: int, question_type, num_choices) -> str:
	"""
	Generates a formatted multiple-choice question on gene linkage and genetic distance.

	This function generates a question that asks whether two genes are linked or unlinked
	based on genetic distance. It also constructs an HTML-formatted table showing progeny counts,
	and provides multiple answer choices with one correct answer.

	Args:
		N (int): Question number, used to determine the type of question (linked or unlinked) and for formatting.
		question_type (str)

	Returns:
		str: The fully formatted HTML question string, ready to be written to a file.

	Raises:
		ValueError: If something goes wrong with generating answer choices.
	"""
	if question_type == 'mc':
		#small distances make the answer too obvious
		distance = round(random.uniform(20, 32),2)
	else:
		#large distances can make the PD assignment hard
		distance = random.randint(2, 32)
	if debug: print(f"Distance: {distance}")

	# Retrieve the instructions and hints for the question footer
	question_header = get_question_header()
	footer_steps = get_question_footer_steps()
	fib_important_tips = get_important_tips()

	# Get two random gene letters (e.g., 'A' and 'B') and fetch phenotype descriptions for each gene
	gene_letters_str = gml.get_gene_letters(2)
	phenotype_dict = phenotypes_for_yeast.phenotype_dict
	phenotype_info_str = gml.get_phenotype_info(gene_letters_str, phenotype_dict)

	# Determine an appropriate progeny size based on the genetic distance
	progeny_size_int = gml.get_progeny_size(distance)
	print(f'progeny_size_int = {progeny_size_int}')
	print(f'ratio = {progeny_size_int * distance**2 / 40000}')
	while progeny_size_int * distance**2 < 80000:
		print("INCREASE PROGENY SIZE x 2")
		progeny_size_int *= 2

	# Construct counts of different tetrad types (Parental Ditype, Non-Parental Ditype, and Tetratype)
	# This is based on whether the genes are linked or unlinked, the genetic distance, and progeny size
	progeny_type_count_dict = construct_progeny_counts(distance, progeny_size_int)
	if progeny_type_count_dict is None:
		return None

	# Assign specific tetrads (genotype combinations) to each count type (PD, NPD, TT) for display in the table
	progeny_tetrads_count_dict = assign_tetrads(progeny_type_count_dict, gene_letters_str)

	#Check if progeny_tetrads_count_dict are valid
	if tetradlib.check_if_progeny_counts_are_valid(progeny_tetrads_count_dict) is False:
		return None

	# Generate a text-based table (ASCII) for debugging and console output
	ascii_table = tetradlib.get_progeny_ascii_table(2, progeny_tetrads_count_dict, progeny_size_int)
	print(ascii_table)

	# Generate an HTML-formatted table of the progeny tetrads to be included in the question
	html_table = tetradlib.make_progeny_html_table(progeny_tetrads_count_dict, progeny_size_int)

	# Combine all parts of the question into a single HTML string
	# This includes the phenotype descriptions, the HTML table, the question setup, and any instructional steps
	full_question = question_header + phenotype_info_str + html_table + footer_steps
	statement = f"<h5>Determine the distance between the two genes {gene_letters_str[0].upper()} and {gene_letters_str[1].upper()}</h5>"

	# Format question based on type
	if question_type == 'mc':
		full_question = full_question + statement
		choices_list, answer_text = make_choices(progeny_type_count_dict, distance, num_choices)
		if choices_list is None:
			return None
		final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
	else:
		full_question = full_question + fib_important_tips + statement
		print(f"gene_pair_distance = {distance}")
		final_question = bptools.formatBB_NUM_Question(N, full_question, distance, 0.1, tol_message=False)

	return final_question

#=====================
def parse_arguments():
	"""Parses command-line arguments for the script."""
	parser = argparse.ArgumentParser(description="Generate genetics mapping questions.")
	question_group = parser.add_mutually_exclusive_group(required=True)

	# Add question type argument with choices
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str, choices=('num', 'mc'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)
	question_group.add_argument(
		'-m', '--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice'
	)
	question_group.add_argument(
		'-n', '--num', dest='question_type', action='store_const', const='num',
		help='Set question type to numeric'
	)

	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of choices to choose from in the question', default=6)

	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do', default=1
	)

	args = parser.parse_args()

	return args

#=====================
#=====================
def main():
	args = parse_arguments()

	# Generate output filename based on script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	# Define output file name
	outfile = (
		'bbq-' +
		script_name +
		'-' +
		args.question_type.upper() +
		'-questions.txt'
		)
	print(f'Writing to file: {outfile}')

	# Open file and write questions
	N = 0
	with open(outfile, 'w') as f:
		for _ in range(args.duplicates):
			final_question = generate_question(N, args.question_type, args.num_choices)
			if final_question is not None:
				N += 1
				f.write(final_question)
			else:
				print("Question generation failed")
	f.close()

	# Display histogram if question type is multiple choice
	if args.question_type == "mc":
		bptools.print_histogram()

if __name__ == "__main__":
	main()
