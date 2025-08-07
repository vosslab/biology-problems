#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
import sys
import copy

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities

import bptools

#===============================
def createMarker(num_markers, used_markers):
	"""
	Creates a set of unique HLA markers using predefined letters and random digits.
	"""
	charlist = "ABCDEFG"
	markers = []
	single_digit_numbers = list(range(1, 10))
	for i in range(num_markers):
		letter = charlist[i]
		num = random.choice(single_digit_numbers)
		marker = f"{letter}{num}"
		# check to make sure we have not used this letter-number combo yet
		while used_markers.get(marker) is not None:
			num = random.choice(single_digit_numbers)
			marker = f"{letter}{num}"
		used_markers[marker] = True
		markers.append(marker)
	return set(markers)

#===============================
def addColorToMarkers(marker_set, hex_color):
	"""
	Applies HTML color formatting to a set of marker strings.
	"""
	markers_list = []
	for marker_text in marker_set:
		marker_text = bptools.colorHTMLText(marker_text, hex_color)
		markers_list.append(marker_text)
	return set(markers_list)

#===============================
def markersToString(markers):
	"""
	Returns a comma-separated, alphabetically sorted string of markers.
	"""
	return ",".join(sorted(list(markers)))


#===============================
def mixMarkers(markers1, markers2):
	"""
	Creates a new marker set by randomly selecting elements from the two input sets.
	Ensures at least two unique values are used.
	"""
	markerlist1 = sorted(list(markers1))
	markerlist2 = sorted(list(markers2))
	markerselect = []
	while len(set(markerselect)) <= 1:
		markerselect = [random.choice((1, 2)) for _ in markerlist1]
	newmarkers = [
		markerlist1[i] if ms == 1 else markerlist2[i]
		for i, ms in enumerate(markerselect)
	]
	return set(newmarkers)

#===============================
def generateChoices(marker_collection):
	choices_list = []
	[mom1, mom2, dad1, dad2] = marker_collection

	# part of mom and part of dad = answer
	choice_set = copy.copy(random.choice([dad1, dad2])).union(random.choice([mom1, mom2]))
	correct_answer_str = markersToString(choice_set)
	choices_list.append(correct_answer_str)

	# part of mom1 and part of mom2
	choice_set = copy.copy(mom1).union(mom2)
	choices_list.append(markersToString(choice_set))

	# part of dad1 and part of dad2
	choice_set = copy.copy(dad1).union(dad2)
	choices_list.append(markersToString(choice_set))

	# first mix of mom1/mom2 and mix of dad1/dad2
	choice_set = mixMarkers(mom1, mom2).union(mixMarkers(dad1, dad2))
	choices_list.append(markersToString(choice_set))

	# second mix of mom1/mom2 and mix of dad1/dad2
	choice_set = mixMarkers(mom1, mom2).union(mixMarkers(dad1, dad2))
	choices_list.append(markersToString(choice_set))

	# Remove duplicates and shuffle
	unique_choices_list = list(set(choices_list))
	random.shuffle(unique_choices_list)

	return correct_answer_str, unique_choices_list

#===============================
def generateQuestion(marker_collection):
	[mom1, mom2, dad1, dad2] = marker_collection
	mom1_text = markersToString(mom1)
	mom2_text = markersToString(mom2)
	dad1_text = markersToString(dad1)
	dad2_text = markersToString(dad2)

	# Revised context on HLA typing emphasizing organ transplantation
	question_string = "<p>HLA genotyping serves as a key component in the field of immunogenetics. "
	question_string += "It is used for understanding individual variations in immune responses. "
	question_string += "This molecular technique identifies unique alleles on paired chromosomes. "
	question_string += "It's particularly vital in organ transplantation for matching donors and recipients. "
	question_string += "Finding a correct match reduces the chance for graft rejection. </p>"

	question_string += f"<p>A mother has a HLA genotype of <strong>{mom1_text}</strong> on one chromosome "
	question_string += f"and <strong>{mom2_text}</strong> on the other chromosome. </p>"
	question_string += f"<p>The father has a HLA genotype of <strong>{dad1_text}</strong> on one chromosome "
	question_string += f"and <strong>{dad2_text}</strong> on the other chromosome. </p>"
	question_string += "<p>Which one of the following combinations is a possible genotype for their offspring?</p>"

	return question_string

#===============================
#===============================
def main():
	parser = argparse.ArgumentParser(description='Generate HLA genotype questions.')
	parser.add_argument('-n', '--num_markers', type=int, default=2, help='Number of markers.')
	parser.add_argument('-x', '--max_questions', type=int, default=25, help='Maximum number of questions to generate.')
	parser.add_argument('-c', '--color', dest='use_color', action='store_true', default=True, help='Add color to choices.')
	parser.add_argument('-b', '--bw', dest='use_color', action='store_false', default=True, help='Black and White (default).')
	args = parser.parse_args()
	num_markers = min(args.num_markers, 7)  # Restricting num_markers to a maximum of 7

	# Generate the output file name based on the script name and parameters
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	color_mode = 'color' if args.use_color else 'black'
	outfile = (
		f'bbq-{script_name}'                  # script name
		f'-{num_markers}_markers'             # number of markers
		f'-{color_mode}'                     # color or bw
		'-questions.txt'                     # file extension
	)

	print(f'writing to file: {outfile}')

	N = 0  # Initialize question counter
	with open(outfile, 'w') as f:  # Using 'with' for better file handling
		for i in range(args.max_questions):
			used_markers = {}
			N += 1  # Increment question counter
			mom1 = createMarker(num_markers, used_markers)
			mom2 = createMarker(num_markers, used_markers)
			dad1 = createMarker(num_markers, used_markers)
			dad2 = createMarker(num_markers, used_markers)
			bw_marker_collection = [mom1, mom2, dad1, dad2]
			colors = bptools.default_color_wheel(num_colors=4)
			mom1c = addColorToMarkers(mom1, colors[0])
			mom2c = addColorToMarkers(mom2, colors[1])
			dad1c = addColorToMarkers(dad1, colors[2])
			dad2c = addColorToMarkers(dad2, colors[3])
			color_marker_collection = [mom1c, mom2c, dad1c, dad2c]

			question_string = generateQuestion(color_marker_collection)
			if args.use_color is True:
				answer_str, choices_list = generateChoices(color_marker_collection)
			else:
				answer_str, choices_list = generateChoices(bw_marker_collection)

			complete_question = bptools.formatBB_MC_Question(N, question_string, choices_list, answer_str)

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
