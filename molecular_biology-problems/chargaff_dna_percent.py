#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#========================================
nt2name = {
	'A':	'adenine',
	'C':	'cytosine',
	'G':	'guanine',
	'T':	'thymine',
	'U':	'uracil',
	'Ade':	'adenine',
	'Cyt':	'cytosine',
	'Gua':	'guanine',
	'Thy':	'thymine',
	'Ura':	'uracil',
}

#========================================
canonical = {
	'a':	'Ade',
	'c':	'Cyt',
	'g':	'Gua',
	't':	'Thy',
	'u':	'Ura',
	'ade':	'Ade',
	'cyt':	'Cyt',
	'gua':	'Gua',
	'thy':	'Thy',
	'ura':	'Ura',
	'adenine':	'Ade',
	'cytosine':	'Cyt',
	'guanine':	'Gua',
	'thymine':	'Thy',
	'uracil':	'Ura',
}

#========================================
complement = {
	'A': 'T',
	'T': 'A',
	'G': 'C',
	'C': 'G',
	'Ade': 'Thy',
	'Thy': 'Ade',
	'Gua': 'Cyt',
	'Cyt': 'Gua',
}

#========================================
def getAnswer(nt1, percent):
	#nt2 = complement(nt1)
	offperc = 50 - percent
	if nt1.startswith("A"):
		#CGT
		answer = [offperc, offperc, percent]
	elif nt1.startswith("C"):
		#AGT
		answer = [offperc, percent, offperc]
	elif nt1.startswith("G"):
		#ACT
		answer = [offperc, percent, offperc]
	elif nt1.startswith("T"):
		#ACG
		answer = [percent, offperc, offperc]
	return answer

#========================================
colormap = {
	'A': '#004d00', #A is green
	'C': '#003566', #C is blue
	'T': '#6e1212', #T is red
	'G': '#2a2000', #G is black
	'U': '#420080', #U is purple
}

#========================================
def printChoice(nts, valuelist):
	global colormap
	mystr = ''
	# Iterate through the three nucleotides
	for i in range(3):
		# Get the first letter of the nucleotide to use as a key for the colormap
		nt = nts[i][0]
		# Fetch the corresponding color
		color = colormap[nt]
		# Append the formatted string, color-coded and with full nucleotide names, abbreviations, and perhaps an em dash as a separator
		mystr += "<span style='color: {0};'>{1} ({2}): {3:2d}%</span> &mdash; ".format(color, nt2name[nts[i]], nt, valuelist[i])
	# Remove the trailing em dash and space
	return mystr[:-9]

#========================================
#========================================
def write_question(N, num_choices, override_nt):
	global colormap
	if random.random() < 0.5:
		percent = random.randint(1,23)
	else:
		percent = random.randint(27,49)

	nt1 = None
	if override_nt is not None:
		nt1 = canonical.get(override_nt.lower())
		if nt1 is None:
			raise ValueError(f"Invalid nucleotide override: {override_nt}")

	nts = ['Ade', 'Cyt', 'Thy', 'Gua']
	random.shuffle(nts)
	if nt1 is None:
		nt1 = nts.pop()
	else:
		nts.remove(nt1)
	nts.sort()

	# Ensure the nucleotide is uppercase to match the colormap keys
	nt = nt1[0].upper()
	# Assign the appropriate color for the nucleotide based on the colormap
	color = colormap[nt]

	# Initialize the question string with a precise introductory phrase
	question = "<p>According to Chargaff's rules concerning the base pairing composition in double-stranded DNA, "
	# Eliminate redundancy and improve formality by replacing 'Given' with 'consider'
	question += "consider a sample where the percentage composition of "

	# Utilize HTML to emphasize and color-code the percentage and nucleotide type
	# Here, I retained your existing format and just tweaked the wording
	question += "<strong><span style='color: {0};'>{1:2d}% is {2}</span></strong>.</p>".format(color, percent, nt2name[nt])
	# Formulate the follow-up query in a separate paragraph for clarity
	question += "<p>What are the percentages of the other three bases?</p>"

	answer = getAnswer(nt1, percent)

	#print(question)
	choices = []
	offperc = 50 - percent
	choices.append([offperc, offperc, percent])
	choices.append([offperc, percent, offperc])
	choices.append([percent, offperc, offperc])
	offchoices = []
	offchoices.append([offperc, 25, 25])
	offchoices.append([25, offperc, 25])
	offchoices.append([25, 25, offperc])
	random.shuffle(offchoices)
	choices.append(offchoices[0])
	choices.append(offchoices[1])
	random.shuffle(choices)
	
	choices_list = []
	for valuelist in choices:
		choice_text = printChoice(nts, valuelist)
		choices_list.append(choice_text)
		if valuelist == answer:
			answer_text = choice_text
	
	complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer_text)
	return complete_question

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

	# Add an argument to specify the number of answer choices for each question
	parser.add_argument(
		'-c', '--num_choices', type=int, default=5, dest='num_choices',
		help="Number of choices to create."
	)

	# Mutually exclusive group for nucleotide override methods
	nt_group = parser.add_mutually_exclusive_group()
	nt_group.add_argument('--A', action='store_const', const='A', dest='override_nt',
		help='Force nucleotide A (Adenine)')
	nt_group.add_argument('--T', action='store_const', const='T', dest='override_nt',
		help='Force nucleotide T (Thymine)')
	nt_group.add_argument('--C', action='store_const', const='C', dest='override_nt',
		help='Force nucleotide C (Cytosine)')
	nt_group.add_argument('--G', action='store_const', const='G', dest='override_nt',
		help='Force nucleotide G (Guanine)')
	nt_group.add_argument('--U', action='store_const', const='U', dest='override_nt',
		help='Force nucleotide U (Uracil)')
	nt_group.add_argument('--override-nt', type=str, dest='override_nt',
		help='Specify nucleotide by name or letter (e.g., A, adenine, guanine, Gua)')


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
		f'-{args.num_choices}_choices'
		'-questions.txt'  # Add the file extension
	)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for _ in range(args.duplicates):
			# Generate the complete formatted question
			complete_question = write_question(N+1, args.num_choices, args.override_nt)

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
