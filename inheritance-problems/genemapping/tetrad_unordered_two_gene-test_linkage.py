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

#===========================
#===========================
def get_question_text() -> str:
	"""
	Generates the question text based on the question type.

	Args:
		question_type (str): Type of question ('num' or 'mc').

	Returns:
		str: The formatted question text for either a standard two-gene problem or a complex tetrad problem.
	"""
	# Background information for both types of questions
	question_string = '<h6>Unordered Tetrad Two Gene Determine Linkage</h6>'
	question_string += '<p>The yeast <i>Saccharomyces cerevisiae</i> has unordered tetrads. '
	question_string += 'A cross is made to study the linkage relationships among two genes.</p> '
	question_string += '<p>Using the table above, determine the linkage between the two genes.</p> '
	if gml.is_valid_html(question_string) is False:
		print(question_string)
		raise ValueError
	return question_string


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
	steps += ' <li>Step 1: Find the row with the Parental Type for both genes.</li>'
	steps += ' <li>Step 2: Assign PD, NPD, TT for the other rows</li>'
	steps += ' <li>Step 3: Determine if the two genes are linked.</li>'
	steps += '   <ul><li>PD &gt;&gt; NPD &rarr; linked; PD &approx; NPD &rarr; unlinked</li></ul>'
	steps += '</ul>'
	if gml.is_valid_html(steps) is False:
		print(steps)
		raise ValueError
	return steps


#====================================
def construct_progeny_counts(question_type_str: str, distance_int: int, progeny_size_int: int) -> dict:
	"""
	Constructs a dictionary with counts of different progeny types (Parental Ditype, Tetratype,
	and Non-Parental Ditype) based on the given genetic distance and question type.

	Args:
		question_type_str (str): Type of question, either 'linked' or 'unlinked'.
		distance_int (int): The genetic distance between genes or to the centromere (in centiMorgans).
		progeny_size_int (int): Total number of progeny (tetrads) to simulate.

	Returns:
		dict: A dictionary with counts for 'pd' (Parental Ditype), 'tt' (Tetratype), and 'npd' (Non-Parental Ditype).

	Raises:
		ValueError: If the criteria for unlinked genes are not met.
	"""

	# The input distance is capped between 2 and 30 cM, representing 2% to 30% recombination frequency.
	# For "unlinked" questions, the genetic distance refers to the distance to the centromere.
	# For "linked" questions, it represents the distance between two genes.

	if question_type_str == "unlinked":
		# For unlinked genes, both the Parental Ditype (PD) and Non-Parental Ditype (NPD) need to be greater than Tetratype count.
		# If the distance is above 16 cM, we reduce it to half to keep counts realistic.
		if distance_int > 16:
			distance_int //= 2

		# Calculate Tetratype (TT) count based on genetic distance.
		tetratype_count = (2 * distance_int * progeny_size_int) // 100

		# Ensure that Non-Parental Ditype (NPD) is greater than Tetratype (TT) count for unlinked genes.
		if tetratype_count >= progeny_size_int // 3:
			raise ValueError("Failed criteria for unlinked genes: NPD should be greater than TT.")

		# Split the remaining progeny counts between Parental Ditype (PD) and Non-Parental Ditype (NPD)
		a, b = gml.split_number_in_two(progeny_size_int - tetratype_count)
		parental_ditype_count, non_parental_ditype_count = max(a, b), min(a, b)

	else:  # question_type_str == "linked"
		# For linked genes, Tetratype (TT) and Non-Parental Ditype (NPD) counts are calculated based on single (SCO)
		# and double crossovers (DCO).
		# SCO (Single Crossover) count is proportional to the distance between genes.
		sco_count = (distance_int * progeny_size_int) // 100

		# DCO (Double Crossover) count is based on the square of the distance (distance_int^2) to capture rare events.
		dco_count = (distance_int ** 2 * progeny_size_int) // 10000

		# Calculate Non-Parental Ditype (NPD) and Tetratype (TT) counts using SCO and DCO values.
		non_parental_ditype_count = dco_count // 4
		tetratype_count = 2 * (sco_count - 3 * non_parental_ditype_count)
		parental_ditype_count = progeny_size_int - non_parental_ditype_count - tetratype_count

	# Return a dictionary with counts for each progeny type.
	progeny_type_count_dict = {
		'pd': parental_ditype_count,
		'tt': tetratype_count,
		'npd': non_parental_ditype_count,
	}
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
def get_choices():
	"""
	Generates a list of answer choices describing the relationship between two genes.

	This function returns both "good" choices (correct descriptions) and "wrong" choices
	(incorrect or nonsensical descriptions). Key differences are emphasized using bold and
	uppercase text with color highlighting to further distinguish choices.

	Returns:
		list: A list of formatted answer choices.
	"""

	# Define color styles for key terms with balanced brightness
	linked_style = 'style="color: #006400;"'          # Dark Green
	unlinked_style = 'style="color: #8B0000;"'        # Brick Red
	same_style = 'style="color: #1E40AF;"'            # Deep Blue
	different_style = 'style="color: #D2691E;"'       # Dark Orange
	neither_style = 'style="color: #5B2C6F;"'         # Dark Purple
	both_style = 'style="color: #7B3F00;"'            # Deep Burgundy

	# Good choices: valid, sensible options
	good_choices_list = [
		f'The two genes are <strong {linked_style}>LINKED</strong> and on the <strong {same_style}>SAME</strong> chromosome.',
		f'The two genes are <strong {unlinked_style}>UNLINKED</strong> but may be on either the <strong {same_style}>SAME</strong> or <strong {different_style}>DIFFERENT</strong> chromosomes.'
	]

	# Wrong choices: nonsensical or logically incorrect options
	wrong_choices_list = [
		f'The two genes are <strong {neither_style}>NEITHER</strong> <strong>linked</strong> NOR <strong>unlinked</strong>.',
		f'The two genes are <strong {both_style}>BOTH</strong> <strong>linked</strong> AND <strong>unlinked</strong>.',
		f'The two genes are <strong {linked_style}>LINKED</strong> but are likely on <strong {different_style}>DIFFERENT</strong> chromosomes.',
	]

	# Combine good and wrong choices into one list
	return good_choices_list + wrong_choices_list

#===========================
def generate_question(N: int) -> str:
	"""
	Generates a formatted multiple-choice question on gene linkage and genetic distance.

	This function generates a question that asks whether two genes are linked or unlinked
	based on genetic distance. It also constructs an HTML-formatted table showing progeny counts,
	and provides multiple answer choices with one correct answer.

	Args:
		N (int): Question number, used to determine the type of question (linked or unlinked) and for formatting.

	Returns:
		str: The fully formatted HTML question string, ready to be written to a file.

	Raises:
		ValueError: If something goes wrong with generating answer choices.
	"""

	# Determine the type of question (linked or unlinked) based on the question number
	# This alternates the question type for each call, so even questions are "linked" and odd questions are "unlinked"
	question_type_str = ('linked', 'unlinked')[N % 2]

	# Randomly generate a genetic distance between 12 and 40 centiMorgans for the question
	if question_type_str == "unlinked":
		distance_int = random.randint(4, 16)
	else:
		distance_int = random.randint(20, 31)
	if debug: print(f"Distance: {distance_int}")

	# Retrieve the instructions and hints for the question footer
	steps = get_question_footer_steps()
	question_setup = get_question_text()

	# Get two random gene letters (e.g., 'A' and 'B') and fetch phenotype descriptions for each gene
	gene_letters_str = gml.get_gene_letters(2)
	phenotype_dict = phenotypes_for_yeast.phenotype_dict
	phenotype_info_str = gml.get_phenotype_info(gene_letters_str, phenotype_dict)

	# Determine an appropriate progeny size based on the genetic distance
	progeny_size_int = gml.get_progeny_size(distance_int)
	print(f'progeny_size_int = {progeny_size_int}')
	print(f'ratio = {progeny_size_int * distance_int**2 / 40000}')
	while progeny_size_int * distance_int**2 < 80000:
		print("INCREASE PROGENY SIZE x 2")
		progeny_size_int *= 2

	# Construct counts of different tetrad types (Parental Ditype, Non-Parental Ditype, and Tetratype)
	# This is based on whether the genes are linked or unlinked, the genetic distance, and progeny size
	progeny_type_count_dict = construct_progeny_counts(question_type_str, distance_int, progeny_size_int)

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
	full_question = phenotype_info_str + html_table + steps + question_setup

	# Generate answer choices for the question and set the correct answer based on the question type
	answer_text = None
	choices_list = get_choices()
	if question_type_str == 'linked':
		# For a linked question, ensure the correct answer choice mentions "LINKED" and "SAME" chromosome
		answer_text = choices_list[0]
		if not 'LINKED' in answer_text or not 'SAME' in answer_text:
			print(question_type_str, answer_text)
			raise ValueError("Something wrong with the choices")
	else:
		# For an unlinked question, ensure the correct answer choice mentions "UNLINKED" and "DIFFERENT" chromosomes
		answer_text = choices_list[1]
		if not 'UNLINKED' in answer_text or not 'DIFFERENT' in answer_text:
			print(question_type_str, answer_text)
			raise ValueError("Something wrong with the choices")

	# Randomly shuffle the answer choices to vary the order in each question
	random.shuffle(choices_list)

	# Format the final question as a Blackboard-compatible multiple-choice question using bptools
	final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)

	return final_question

#=====================
#=====================
def parse_arguments():
	"""Parses command-line arguments for the script."""
	parser = argparse.ArgumentParser(description="Generate genetics questions.")

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
	outfile = f'bbq-{script_name}-questions.txt'
	print(f'Writing to file: {outfile}')

	# Open file and write questions
	N = 0
	with open(outfile, 'w') as f:
		for _ in range(args.duplicates):
			final_question = generate_question(N)
			if final_question is not None:
				N += 1
				f.write(final_question)

	bptools.print_histogram()

if __name__ == "__main__":
	main()
