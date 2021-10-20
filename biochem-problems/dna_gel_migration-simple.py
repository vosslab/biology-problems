#!/usr/bin/env python

import os
import math
import random


"""
6. Which of the following fragments of DNA would migrate closest to the wells during agarose gel electrophoresis?
a. 250 bp
b. 750 bp
c. 2,000 bp
*d. 5,000 bp
"""

answer_hist = {}

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
def writeQuestion(N):
	type1 = "migrate closest to "
	type2 = "travel furthest from "
	chosen_type = random.randint(1, 2)
	if chosen_type == 1:
		type_text = type1
		correct_id = -1
	else:
		type_text = type2
		correct_id = 0
	
	question = ("Which one of the following fragments of DNA would  "
	  +"{0} the wells during agarose gel electrophoresis?".format(type_text))
	
	bands = getDNA_Bands()
	#print(bands)
	correct_band = bands[correct_id]
	
	letters = "ABCDEF"
	complete_question = "MC\t{0}\t".format(question)
	print("{0}. {1}".format(N, question))
	for i, band_size in enumerate(bands):
		choice = writeChoice(band_size)
		complete_question += choice+'\t'
		if band_size == correct_band:
			prefix = 'x'
			complete_question += 'Correct\t'
			answer_hist[letters[i]] = answer_hist.get(letters[i], 0) + 1
		else:
			prefix = ' '
			complete_question += 'Incorrect\t'
		print('- [{0}] {1}. {2}'.format(prefix, letters[i], choice))
	print("")
	return complete_question


#==================================================



if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	duplicates = 199
	for i in range(duplicates):
		complete_question = writeQuestion(i+1)
		f.write(complete_question)
		f.write('\n')
	f.close()
	print(answer_hist)
	
