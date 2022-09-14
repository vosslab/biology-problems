#!/usr/bin/env python3

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
def bbFormatMatchingQuestion(N, question_text, matching_list, answer_list, max_choices=5):
	complete_question = question_text
	num_items = min(len(matching_list), len(answer_list))
	indices = list(range(num_items))
	random.shuffle(indices)
	indices = indices[:max_choices]
	indices.sort()
	for i in indices:
		complete_question += '\t' + matching_list[i] + '\t' + answer_list[i]
	crc16_value = getCrc16_FromString(complete_question)
	#MAT TAB question_text TAB answer_text TAB matching text TAB answer two text TAB matching two text
	bb_output_format = "MAT\t<p>{0:03d}. {1}</p> {2}\n".format(N, crc16_value, complete_question)
	return bb_output_format

#=======================
def matchingQuestionSet():
	bb_output_format_list = []
	question_text = "<p>Match the following pedigrees to their most likely inheritance type.</p> "
	question_text += "<p>Note: <i>each inheritance type will only be used ONCE.</i></p> "
	answer_list = ['autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked']
	N = 0
	for ad in pedigree_code_strings.autosomal_dominant:
		for ar in pedigree_code_strings.autosomal_recessive:			
			for xd in pedigree_code_strings.x_linked_dominant:
				for xr in pedigree_code_strings.x_linked_recessive:
					for yl in pedigree_code_strings.y_linked:
						if random.random() < 0.5:
							ad = pedigree_lib.mirrorPedigree(ad)
						adc = pedigree_lib.translateCode(ad)
						if random.random() < 0.5:
							ar = pedigree_lib.mirrorPedigree(ar)
						arc = pedigree_lib.translateCode(ar)
						if random.random() < 0.5:
							xd = pedigree_lib.mirrorPedigree(xd)
						xdc = pedigree_lib.translateCode(xd)
						if random.random() < 0.5:
							xr = pedigree_lib.mirrorPedigree(xr)
						xrc = pedigree_lib.translateCode(xr)
						if random.random() < 0.5:
							yl = pedigree_lib.mirrorPedigree(yl)
						ylc = pedigree_lib.translateCode(yl)

						matching_list = [adc, arc, xdc, xrc, ylc]
						N += 1
						bb_output_format = bbFormatMatchingQuestion(N, question_text, matching_list, answer_list, max_choices=4)
						bb_output_format_list.append(bb_output_format)

	return bb_output_format_list


#===============================
#===============================
#===============================
#===============================
if __name__ == '__main__':
	max_questions = 199
	max_questions = 17
	bb_output_format_list = matchingQuestionSet()
	if len(bb_output_format_list) > max_questions:
		random.shuffle(bb_output_format_list)
		bb_output_format_list = bb_output_format_list[:max_questions]
		bb_output_format_list.sort()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for bb_output_format in bb_output_format_list:
		N += 1
		f.write(bb_output_format)
	f.close()
	print("Wrote {0} questions to file.".format(N))	


#THE END
