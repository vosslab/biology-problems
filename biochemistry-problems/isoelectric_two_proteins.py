#!/usr/bin/env python3

import os
import csv
import math
import random
import argparse

import bptools

debug = False

#===========================================================
#===========================================================
def parse_protein_file():
	git_root = bptools.get_git_root()
	data_file_path = os.path.join(git_root, 'data/protein_isoelectric_points.csv')
	file_handle = open(data_file_path, "r")
	reader = csv.reader(file_handle)
	protein_tree = []
	for row in reader:
		if reader.line_num == 1:
			#header = row
			continue
		try:
			protein_dict = {
				'fullname': row[0],
				'abbr':	row[1],
				'pI':	float(row[2]),
				'MW': float(row[3]),
			}
			protein_tree.append(protein_dict)
		except ValueError:
			pass
	if debug is True:
		print("Read data for {0} proteins".format(len(protein_tree)))
	return protein_tree

#===========================================================
#===========================================================
def random_select_proteins(protein_tree):
	protein1 = random.choice(protein_tree)
	if debug is True:
		print("Selected: pI={0:.1f}, {1}".format(protein1['pI'], protein1['fullname']))
	pI1 = protein1['pI']
	pI2 = protein1['pI']
	while abs(pI1 - pI2) < 1.5:
		protein2 = random.choice(protein_tree)
		while protein1.get('abbr') == protein2.get('abbr'):
			protein2 = random.choice(protein_tree)
		pI2 = protein2['pI']
	if debug is True:
		print("Selected: pI={0:.1f}, {1}".format(protein2['pI'], protein2['fullname']))
	return protein1, protein2

#===========================================================
#===========================================================
def get_midpoint_pH(protein1, protein2):
	pI1 = protein1['pI']
	pI2 = protein2['pI']
	if debug is True:
		print("{0:.1f} / {1:.1f}".format(pI1,pI2))
	average = (pI1 + pI2)/2.0
	if debug is True:
		print("Average  pH: {0:.1f}".format(average))
	midpoint = round( (pI1 + pI2)) / 2.0
	if debug is True:
		print("Midpoint pH: {0:.1f}".format(midpoint))
	return midpoint

#===========================================================
#===========================================================
def get_peak_pH(protein1, protein2):
	pI1 = protein1['pI']
	pI2 = protein2['pI']
	min_pI = min(pI1, pI2)
	max_pI = max(pI1, pI2)
	if debug is True:
		print("{0:.1f} / {1:.1f} ... {2:.1f} / {3:.1f}".format(min_pI, max_pI, abs(min_pI - 7.0), abs(max_pI - 7.0) ))
	if abs(min_pI - 7.0) < abs(max_pI - 7.0):
		if debug is True:
			print("min")
		more_neutral_pI = min_pI
		best_peak_pI = math.floor(2*min_pI)/2. - 1
		other_peak_pI = math.ceil(2*max_pI)/2. + 1
	else:
		if debug is True:
			print("max")
		more_neutral_pI = max_pI
		best_peak_pI = math.ceil(2*max_pI)/2. + 1
		other_peak_pI = math.floor(2*min_pI)/2. - 1
	if debug is True:
		print("More Neutral pH: {0:.1f}".format(more_neutral_pI))
		print("Best Peak pH: {0:.1f}".format(best_peak_pI))
		print("Other Peak pH: {0:.1f}".format(other_peak_pI))
	return best_peak_pI, other_peak_pI

#===========================================================
#===========================================================
def get_random_pH(protein1, protein2) -> float:
	"""
	Generate a random pH from a list of calculated pH values.

	Args:
		protein1: The first protein to evaluate.
		protein2: The second protein to evaluate.

	Returns:
		A randomly selected pH value between 2 and 12.
		If no valid pH is found, returns None.
	"""
	midpoint_pH = get_midpoint_pH(protein1, protein2)
	best_peak_pI, other_peak_pI = get_peak_pH(protein1, protein2)

	# Create list of candidate pH values
	pH_list = [midpoint_pH, best_peak_pI, other_peak_pI, midpoint_pH]

	# Filter out invalid pH values
	valid_pH_list = [pH for pH in pH_list if 2 <= pH <= 12]

	if len(valid_pH_list) == 0:
		return None

	# Return a random valid pH if available
	pH = random.choice(valid_pH_list)
	return pH

#===========================================================
#===========================================================
def generate_isoelectric_point_problem(protein1: dict, protein2: dict, pH: float) -> str:
	"""
	Generate an HTML question for an isoelectric point (pI) problem.

	Args:
		protein1: Dictionary containing 'fullname', 'abbr', 'pI', and 'MW' for the first protein.
		protein2: Dictionary containing 'fullname', 'abbr', 'pI', and 'MW' for the second protein.
		pH: The constant pH of the gel in the experiment.

	Returns:
		An HTML string presenting the question.
	"""
	question = (
		"<h6>Isoelectric Point Problem</h6> "
		"<p>A mixture of two proteins are to be separated by isoelectric focusing.</p> "
		'<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black;">'
		"<tr><th>Protein<br/>Name</th><th>Isoelectric<br/>Point (pI)</th><th>Molecular<br/>Weight</th></tr>"
		f'<tr><td>{protein1["fullname"]} ({protein1["abbr"]})</td>'
		f'<td align="right">{protein1["pI"]:.1f}</td>'
		f'<td align="right">{protein1["MW"]:.1f}</td></tr>'
		f'<tr><td>{protein2["fullname"]} ({protein2["abbr"]})</td>'
		f'<td align="right">{protein2["pI"]:.1f}</td>'
		f'<td align="right">{protein2["MW"]:.1f}</td></tr>'
		"</table>"
		f'<p>Both protein samples are placed into a gel with a constant pH of {pH:.1f}. '
		"The gel is then placed into an electric field.</p> "
		"<p>In which direction will each protein in the table migrate at "
		f"<b>pH {pH:.1f}</b>?</p>"
	)

	return question

#===========================================================
#===========================================================
def generate_choices(protein1: dict, protein2: dict, pH: float) -> tuple[list[str], str]:
	"""
	Determine the direction of migration for two proteins based on the given pH.

	Args:
		protein1: Dictionary containing 'abbr' and 'pI' for the first protein.
		protein2: Dictionary containing 'abbr' and 'pI' for the second protein.
		pH: The constant pH of the gel.

	Returns:
		A tuple containing:
			- choices_list: List of possible migration explanations.
			- answer_text: The correct migration explanation based on pH.
	"""
	ab1 = protein1['abbr']
	ab2 = protein2['abbr']

	# Determine the charge and migration behavior of the proteins
	if pH > protein1['pI'] and pH > protein2['pI']:
		# Both have a negative charge and move towards the positive terminal
		answer_id = 0
	elif pH < protein1['pI'] and pH < protein2['pI']:
		# Both have a positive charge and move towards the negative terminal
		answer_id = 1
	elif protein1['pI'] > pH > protein2['pI']:
		# Protein 1 is negative and protein 2 is positive
		answer_id = 2
	elif protein1['pI'] < pH < protein2['pI']:
		# Protein 1 is positive and protein 2 is negative
		answer_id = 3

	# Generate choices
	choice1 = (
		f'Both {ab1} and {ab2} will have a <span style="color:darkred">negative (&ndash;)</span> charge '
		'and travel towards the <span style="color:darkblue">positive (+)</span> terminal'
	)
	choice2 = (
		f'Both {ab1} and {ab2} will have a <span style="color:darkblue">positive (+)</span> charge '
		'and travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal'
	)
	choice3 = (
		f'{ab1} will have a <span style="color:darkblue">positive (+)</span> charge '
		'and travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal<br/> '
		f'{ab2} will have a <span style="color:darkred">negative (&ndash;)</span> charge '
		'and travel towards the <span style="color:darkblue">positive (+)</span> terminal'
	)
	choice4 = (
		f'{ab1} will have a <span style="color:darkred">negative (&ndash;)</span> charge '
		'and travel towards the <span style="color:darkblue">positive (+)</span> terminal<br/> '
		f'{ab2} will have a <span style="color:darkblue">positive (+)</span> charge '
		'and travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal'
	)

	# Compile choices and select the correct answer
	choices_list = [choice1, choice2, choice3, choice4]
	answer_text = choices_list[answer_id]

	return choices_list, answer_text

#===========================================================
#===========================================================
def write_question(N, protein_tree):
	protein1, protein2 = random_select_proteins(protein_tree)
	pH = get_random_pH(protein1, protein2)
	if pH is None:
		return None

	question = generate_isoelectric_point_problem(protein1, protein2, pH)
	choices_list, answer_text = generate_choices(protein1, protein2, pH)
	bb_format = bptools.formatBB_MC_Question(N, question, choices_list, answer_text)
	return bb_format

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
	parser = argparse.ArgumentParser(description="Generate questions.")

	# Add an argument to specify the number of duplicate questions to generate
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create',
		default=1
	)

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

	# Generate the output file name based on the script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'  # Add the script name to the file name
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	protein_tree = parse_protein_file()

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for _ in range(args.duplicates):
			# Generate the complete formatted question
			complete_question = write_question(N+1, protein_tree)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# If the question type is multiple choice, print a histogram of results
	bptools.print_histogram()

	# Print a message indicating how many questions were saved
	print(f'saved {N} questions to {outfile}')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
