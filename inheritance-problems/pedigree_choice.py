#!/usr/bin/env python

import os
import random
import pedigree_lib
import pedigree_code_strings
import crcmod.predefined


#=======================
def getCrc16_FromString(mystr):
 crc16 = crcmod.predefined.Crc('xmodem')
 crc16.update(mystr.encode('ascii'))
 return crc16.hexdigest().lower()

#=======================
def bbFormatMatchingQuestion(N, question_text, matching_list, answer_list):
	complete_question = question_text
	num_items = min(len(matching_list), len(answer_list))
	for i in range(num_items):
		complete_question += '\t' + matching_list[i] + '\t' + answer_list[i]
	crc16_value = getCrc16_FromString(complete_question)
	#MAT TAB question_text TAB answer_text TAB matching text TAB answer two text TAB matching two text
	bb_output_format = "MAT\t<p>{0:03d}. {1}</p> {2}\n".format(N, crc16_value, complete_question)
	return bb_output_format

#=======================
def matchingQuestionSet():
	auto_dom_code_string = pedigree_lib.translateCode(random.choice(pedigree_code_strings.autosomal_dominant))
	auto_rec_code_string = pedigree_lib.translateCode(random.choice(pedigree_code_strings.autosomal_recessive))
	xlinked_dom_code_string = pedigree_lib.translateCode(random.choice(pedigree_code_strings.x_linked_dominant))
	xlinked_rec_code_string = pedigree_lib.translateCode(random.choice(pedigree_code_strings.x_linked_recessive))
	ylinked_code_string = pedigree_lib.translateCode(random.choice(pedigree_code_strings.y_linked))

	matching_list = [auto_dom_code_string, auto_rec_code_string, xlinked_dom_code_string, xlinked_rec_code_string, ylinked_code_string]
	answer_list = ['autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked']
	question_text = "<p>Match the following pedigrees to their most likely inheritance type.</p> "
	question_text += "<p>Note: <i>each inheritance type will only be used ONCE.</i></p> "
	return question_text, matching_list, answer_list


#===============================
#===============================
#===============================
#===============================
if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 1
	question_text, matching_list, answer_list = matchingQuestionSet()
	bb_output_format = bbFormatMatchingQuestion(N, question_text, matching_list, answer_list)
	f.write(bb_output_format)
	f.close()
	print("Wrote {0} questions to file.".format(N))	


#THE END
