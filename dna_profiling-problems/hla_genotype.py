#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
import copy
import random

# Import local modules from the project
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
def write_question(N, args):
	used_markers = {}
	mom1 = createMarker(args.num_markers, used_markers)
	mom2 = createMarker(args.num_markers, used_markers)
	dad1 = createMarker(args.num_markers, used_markers)
	dad2 = createMarker(args.num_markers, used_markers)
	bw_marker_collection = [mom1, mom2, dad1, dad2]

	if args.use_color:
		colors = bptools.default_color_wheel(num_colors=4)
		mom1c = addColorToMarkers(mom1, colors[0])
		mom2c = addColorToMarkers(mom2, colors[1])
		dad1c = addColorToMarkers(dad1, colors[2])
		dad2c = addColorToMarkers(dad2, colors[3])
		marker_collection = [mom1c, mom2c, dad1c, dad2c]
	else:
		marker_collection = bw_marker_collection

	question_string = generateQuestion(marker_collection)
	answer_str, choices_list = generateChoices(marker_collection)

	complete_question = bptools.formatBB_MC_Question(
		N,
		question_string,
		choices_list,
		answer_str
	)
	return complete_question

#===============================
#===============================
def parse_arguments():
	parser = bptools.make_arg_parser(description='Generate HLA genotype questions.')
	parser.add_argument('-n', '--num-markers', type=int, dest='num_markers',
		default=2, help='Number of markers.')
	parser.add_argument('-c', '--color', dest='use_color', action='store_true',
		help='Use colored markers in the question and choices.')
	parser.add_argument('-b', '--bw', '--black-white', dest='use_color', action='store_false',
		help='Use black and white marker text.')
	parser.set_defaults(use_color=True)
	args = parser.parse_args()
	return args

#===============================
#===============================
def main():
	args = parse_arguments()
	args.num_markers = min(args.num_markers, 7)

	color_mode = 'color' if args.use_color else 'black'
	outfile = bptools.make_outfile(f"{args.num_markers}_markers", color_mode)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
