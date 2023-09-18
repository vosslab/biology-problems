#!/usr/bin/env python3

import os
import sys
import copy
import random
import argparse
import bptools

#===============================
def createMarker(num_markers, used_markers):
	charlist = "ABCDEFG"
	markers = []
	single_digit_numbers = list(range(1,10))
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
	markers_list = []
	for marker_text in marker_set:
		marker_text = bptools.colorHTMLText(marker_text, hex_color)
		markers_list.append(marker_text)
	return set(markers_list)


#===============================
# I'm using Python's built-in join function to concatenate the string.
# It's more efficient than using the "+=" operator repeatedly.
def markersToString(markers):
	markerlist = sorted(list(markers))
	mystr = ",".join(markerlist)
	return mystr

#===============================
def mixMarkers(markers1, markers2):
	"""
	Given two sets of string markers, this function returns a new set of markers.
	The new set is the same length as the input sets, containing elements from both.
	"""
	markerlist1 = sorted(list(markers1))
	markerlist2 = sorted(list(markers2))
	#print("markerlist1=", markerlist1)
	#print("markerlist2=", markerlist2)
	markerselect = []

	# Ensure markerselect has at least two unique elements
	while len(set(markerselect)) <= 1:
		markerselect = [random.choice((1, 2)) for _ in markerlist1]

	#print("markerselect=", markerselect)
	newmarkers = [
		markerlist1[i] if ms == 1 else markerlist2[i]
		for i, ms in enumerate(markerselect)
	]

	#print("newmarkers=", newmarkers)
	return set(newmarkers)

#===============================
def mixMarkers2(markers1, markers2):
	"""
	Given two sets of string markers, this function returns a new set of markers.
	The new set is the same length as the input sets, containing elements from both.
	"""
	markerlist1 = list(markers1)
	markerlist1.sort()
	markerlist2 = list(markers2)
	markerlist2.sort()
	markerselect = []
	while len(set(markerselect)) <= 1:
		markerselect = []
		for i in range(len(markerlist1)):
			markerselect.append(random.choice((1,2)))
	newmarkers = []
	for i in range(len(markerselect)):
		ms = markerselect[i]
		if ms == 1:
			newmarkers.append(markerlist1[i])
		else:
			newmarkers.append(markerlist2[i])
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


	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
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

			formatted_question = bptools.formatBB_MC_Question(N, question_string, choices_list, answer_str)
			# Writing the formatted question to the file
			f.write(formatted_question)
	bptools.print_histogram()

#===============================
#===============================
if __name__ == '__main__':
	main()
