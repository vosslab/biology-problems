#!/usr/bin/env python3

import os
import sys
import math
import time
import random
import argparse

import bptools
import restrictlib

debug = True

#============================================
#============================================
def tdBlock(vtype="top", htype="middle", fill_color="white", strand_color="black", tick_color="#999999", dna_type='fragment'):
	border_str = ""
	if vtype == "top" and dna_type == 'strand':
		border_str += 'border-bottom: 4px solid {0}; '.format(strand_color)
	elif vtype == "top" and not (htype == "start" or htype == "end"):
		border_str += 'border-bottom: 4px solid {0}; '.format(strand_color)
	else:
		border_str += 'border-bottom: 0px solid {0}; '.format(fill_color)

	if vtype == "bottom" and dna_type == 'strand':
		border_str += 'border-top: 4px solid {0}; '.format(strand_color)
	elif vtype == "bottom" and not (htype == "start" or htype == "end"):
		border_str += 'border-top: 4px solid {0}; '.format(strand_color)
	else:
		border_str += 'border-top: 0px solid {0}; '.format(fill_color)

	if htype == "start" or htype == "right":
		border_str += 'border-right: 2px solid {0}; '.format(tick_color)
	else:
		border_str += 'border-right: 0px solid {0}; '.format(fill_color)

	if htype == "end" or htype == "left":
		border_str += 'border-left: 2px solid {0}; '.format(tick_color)
	else:
		border_str += 'border-left: 0px solid {0}; '.format(fill_color)

	return '  <td style="{0}" bgcolor="{1}"> </td> '.format(border_str, fill_color)

#============================================
#============================================
def longDNA(vtype="top", fill_color="white", strand_color="gray", tick_color="#999999"):
	border_str = ""
	if vtype == "top":
		border_str += 'border-bottom: 4px dotted {0}; '.format(strand_color)
	else:
		border_str += 'border-bottom: 0px solid {0}; '.format(fill_color)

	if vtype == "bottom":
		border_str += 'border-top: 4px dotted {0}; '.format(strand_color)
	else:
		border_str += 'border-top: 0px solid {0}; '.format(fill_color)

	border_str += 'border-right: 0px solid {0}; '.format(fill_color)
	border_str += 'border-left: 0px solid {0}; '.format(fill_color)

	return '  <td style="{0}" bgcolor="{1}"> </td> '.format(border_str, fill_color)

#============================================
#============================================
def makeTable(length, label_dict=None, dna_type='fragment'):
	if label_dict is None:
		label_dict = { 1: "EcoRI", 4: "NheI", }
	table = ""
	space_width = 20
	table = '<table cellpading="0" cellspacing="0" border="0" style="border-collapse: collapse; "> '
	table += '<colgroup width="{0}"></colgroup> '.format(space_width*2)
	for i in range(2*length+2):
		table += '<colgroup width="{0}"></colgroup> '.format(space_width)
	table += '<colgroup width="{0}"></colgroup> '.format(space_width*2)

	table += "<tbody>"

	#Restriction Enzymes
	#DNA number row
	table += "<tr>"
	table += '<td style="border: 0px solid white; "></td>'
	for i in range(length+1):
		msg = label_dict.get(i, "")
		table += '<td align="center" colspan="2" style="border: 0px solid white; "><i>{0}</i></td>'.format(msg)
	table += '<td style="border: 0px solid white; "></td>'
	table += "</tr>"

	#DNA top row
	table += "<tr>"
	if dna_type == 'fragment':
		table += '<td style="border: 0px solid white; "></td>'
	elif dna_type == 'strand':
		table += longDNA("top")
	table += tdBlock("top", "start", dna_type=dna_type)
	for i in range(length):
		table += tdBlock("top", "left", dna_type=dna_type)
		table += tdBlock("top", "right", dna_type=dna_type)
	table += tdBlock("top", "end", dna_type=dna_type)
	if dna_type == 'fragment':
		table += '<td style="border: 0px solid white; "></td>'
	elif dna_type == 'strand':
		table += longDNA("top")
	table += "</tr>"

	#DNA bottom row
	table += "<tr>"
	if dna_type == 'fragment':
		table += '<td style="border: 0px solid white; "></td>'
	elif dna_type == 'strand':
		table += longDNA("bottom")
	table += tdBlock("bottom", "start", dna_type=dna_type)
	for i in range(length):
		table += tdBlock("bottom", "left", dna_type=dna_type)
		table += tdBlock("bottom", "right", dna_type=dna_type)
	table += tdBlock("bottom", "end", dna_type=dna_type)
	if dna_type == 'fragment':
		table += '<td style="border: 0px solid white; "></td>'
	elif dna_type == 'strand':
		table += longDNA("bottom")
	table += "</tr>"

	#DNA number row
	table += "<tr>"
	table += '<td style="border: 0px solid white; "></td>'
	for i in range(length+1):
		table += '<td align="center" colspan="2" style="border: 0px solid white; ">{0}</td>'.format(i)
	table += '<td style="border: 0px solid white; "></td>'
	table += "</tr>"

	table += "</tbody>"
	table += "</table>"
	return table

#============================================
#============================================
def getRandList(size, total_length, include_ends=False):
	if include_ends is True:
		a = list(range(total_length+1))
	else:
		a = list(range(1, total_length))
	random.shuffle(a)
	while len(a) > size:
		a.pop()
	a.sort()
	return a

#============================================
#============================================
def write_question(N=1, length=10, num_sites=2, dna_type='fragment', max_fragment_size=7):
	enzymes = restrictlib.get_enzyme_list()
	enzyme_class1 = restrictlib.random_enzyme_one_end(enzymes)
	enzyme_name1 = enzyme_class1.__name__
	enzyme_class2 = restrictlib.random_enzyme_one_end(enzymes, badletter=enzyme_name1[0])
	enzyme_name2 = enzyme_class2.__name__



	answers = []
	#Fragment
	complete_sites = num_sites + (num_sites - 1)
	if complete_sites * 2 > length:
		print(complete_sites, "too many sites for length", length)
		return None
	sites = getRandList(complete_sites, length, include_ends=False)
	label_dict = {}
	for i, site in enumerate(sites):
		if i % 2 == 0:
			label_dict[site] = enzyme_name1
			if debug is True:
				print(site, enzyme_name1)
		else:
			label_dict[site] = enzyme_name2
			if debug is True:
				print(site, enzyme_name2)
	if debug is True:
		print("end", length)


	# GENERATE ANSWERS
	strand_answers = []
	fragment_answers = [sites[0], length-sites[-1]]
	for i in range(0, len(sites)-2, 2):
		answer_length = sites[i+2] - sites[i]
		fragment_answers.append(answer_length)
		strand_answers.append(answer_length)
	if debug is True:
		strand_answers.sort()
		fragment_answers.sort()
		print("RAW fragment_answers=", fragment_answers)
		print("RAW strand_answers=", strand_answers)

	strand_answers = list(set(strand_answers))
	strand_answers.sort()
	fragment_answers = list(set(fragment_answers))
	fragment_answers.sort()
	if fragment_answers == strand_answers:
		print("Fragment answers match strand answers")
		print(fragment_answers, strand_answers)
		time.sleep(0.1)
		return None

	if dna_type == 'fragment':
		answers = fragment_answers
	elif dna_type == 'strand':
		answers = strand_answers
	if len(answers) < 2:
		print("too few fragments")
		print(answers)
		time.sleep(0.1)
		return None

	if debug is True:
		print("TRIM fragment_answers=", fragment_answers)
		print("TRIM strand_answers=", strand_answers)

	if max(answers) > max_fragment_size:
		print("too big of a fragment", max(answers))
		print(answers)
		time.sleep(0.1)
		return None

	table = makeTable(length, label_dict, dna_type)

	#==============================
	# Intro paragraph based on DNA type
	if dna_type == 'fragment':
		header = (
			f"<p><strong>DNA Fragment Question:</strong> "
			f"Shown below is a short DNA fragment that is only {length} kb in length. "
			f"This fragment has been isolated for restriction enzyme analysis.</p>"
		)
	elif dna_type == 'strand':
		header = (
			f"<p><strong>DNA Strand Question:</strong></p>"
			f"<p>Examine the DNA strand shown below. The table highlights a specific portion "
			f"of a much longer DNA molecule to focus on the region containing restriction sites.</p>"
		)

	#==============================
	# Restriction site labeling
	details = (
		f"<p>Two (2) distinct types of restriction enzyme recognition sites, "
		f"<i>{enzyme_name1}</i> and <i>{enzyme_name2}</i>, are labeled at the top of this DNA segment.</p>"
	)

	#==============================
	# Add explanatory note for strand view
	if dna_type == 'strand':
		details += (
			"<p><strong>Note:</strong> The dashes at both ends of the strand indicate that the next restriction site is far away "
			"and outside the visible region. Because this segment is part of a much larger molecule, any uncut or very large fragments "
			"will not travel into the gel and will appear to be stuck in the well.</p>"
		)

	#==============================
	# Final prompt to student
	question = (
		f"<h6><strong>Determine the sizes of the DNA bands</strong> that would appear on an agarose gel "
		f"after digestion with <i>{enzyme_name1}</i> only.</h6>"
	)

	#==============================
	# Compose full question
	question_text = header + table + details + question

	max_answer = max(answers)
	last_answer = max(max_answer+1, 5)
	choices_list = []
	answers_list = []
	for i in range(1, last_answer+1):
		choice_str = f"{i:d} kb"
		choices_list.append(choice_str)
		if i in answers:
			answers_list.append(choice_str)
	bb_question = bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)
	return bb_question

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

	# Argument for the length
	parser.add_argument('-n', '--length', type=int, default=12,
						help='Length of the DNA sequence.')

	# Argument for the number of sites
	parser.add_argument(
		'-s', '--num_sites', type=int, default=None,
		help='Number of sites in the DNA sequence.'
	)

	# Argument for maximum fragment size
	parser.add_argument('--max_fragment_size', type=int, default=None,
						help='Maximum size of the DNA fragment.')

	# Create a mutually exclusive group for DNA type
	dna_group = parser.add_mutually_exclusive_group()

	# Long-form explicit argument
	dna_group.add_argument(
		'-T', '--dna_type', dest='dna_type', choices=['fragment', 'strand'], type=str,
		help='Type of DNA sequence to use. Choices: fragment or strand.'
	)

	# Shortcut: set DNA type to 'fragment'
	dna_group.add_argument(
		'-F', '--fragment', dest='dna_type', action='store_const', const='fragment',
		help='Use DNA fragments'
	)

	# Shortcut: set DNA type to 'strand'
	dna_group.add_argument(
		'-S', '--strand', dest='dna_type', action='store_const', const='strand',
		help='Use full DNA strands'
	)

	# Set default after the group is defined
	parser.set_defaults(dna_type='fragment')

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()

	if args.max_fragment_size is None:
		args.max_fragment_size = math.ceil(args.length // 2 + 1)


	#==========================
	# Validate number of sites based on DNA type
	if args.dna_type == 'strand':
		if args.num_sites is None:
			args.num_sites = 3
		if args.num_sites < 3:
			raise ValueError("Strand mode requires at least 3 restriction sites.")
	elif args.dna_type == 'fragment':
		if args.num_sites is None:
			args.num_sites = 2
		if args.num_sites < 2:
			raise ValueError("Fragment mode requires at least 2 restriction sites.")

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
		f'-length_{args.length}'
		f'-sites_{args.num_sites}'
		f'-{args.dna_type}'
		'-questions.txt'  # Add the file extension
	)

	print(f"Number of questions: {args.duplicates}")
	print(f"Length: {args.length}")
	print(f"Number of sites: {args.num_sites}")
	print(f"DNA type: {args.dna_type}")
	print(f"Maximum fragment size: {args.max_fragment_size}")

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		while N < args.duplicates:

			# Generate the complete formatted question
			complete_question = write_question(N+1, args.length, args.num_sites, args.dna_type, args.max_fragment_size)

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


