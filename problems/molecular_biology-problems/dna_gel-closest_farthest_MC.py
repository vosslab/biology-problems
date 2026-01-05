#!/usr/bin/env python3

import math
import random

import bptools


"""
6. Which of the following fragments of DNA would migrate closest to the wells during agarose gel electrophoresis?
a. 250 bp
b. 750 bp
c. 2,000 bp
*d. 5,000 bp
"""

#==================================================
def getNearestValidDNA_Size(num_base_pairs):
	num_zeros = math.floor(math.log10(num_base_pairs + 1))
	two_divisor = 10**(num_zeros - 1)

	first_two_digits = int(math.ceil(num_base_pairs / two_divisor))
	first_digit = first_two_digits // 10
	second_digit = first_two_digits % 10
	if 2 < second_digit < 8:
		second_digit = 5
	else:
		second_digit = 0
	first_two_digits = first_digit * 10 + second_digit
	new_num_base_pairs = first_two_digits * two_divisor
	#print(num_base_pairs, "-->", new_num_base_pairs)

	return new_num_base_pairs

#==================================================
def getDNA_Bands():
	bands = []
	bands.append(random.randint(50, 250))
	bands.append(random.randint(300, 950))
	bands.append(random.randint(1000, 4000))
	bands.append(random.randint(5000, 9000))
	good_bands = []
	for band in bands:
		good_band = getNearestValidDNA_Size(band)
		good_bands.append(good_band)
	good_bands.sort()
	return good_bands

#==================================
def writeChoice(band_size):
	choice = "{0:,d} base pairs".format(band_size)
	return choice

#==================================================
def write_question(N, args):
	type1 = "migrate closest to "
	type2 = "travel furthest from "
	chosen_type = random.randint(1, 2)
	if chosen_type == 1:
		type_text = type1
		correct_id = -1
	else:
		type_text = type2
		correct_id = 0
	
	question = (
		"Which one of the following fragments of DNA would "
		+ "{0} the wells during agarose gel electrophoresis?".format(type_text)
	)
	
	bands = getDNA_Bands()
	#print(bands)
	correct_band = bands[correct_id]
	answer_text = writeChoice(correct_band)
	choices_list = [writeChoice(band_size) for band_size in bands]

	bb_question = bptools.formatBB_MC_Question(N, question, choices_list, answer_text)
	return bb_question


#==================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate DNA gel migration questions.")
	args = parser.parse_args()
	return args


#==================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(__file__)
	bptools.collect_and_write_questions(write_question, args, outfile)


#==================================================
if __name__ == '__main__':
	main()
	
