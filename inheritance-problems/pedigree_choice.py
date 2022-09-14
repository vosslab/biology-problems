#!/usr/bin/env python3

import os
import re
import copy
import random
import pedigree_lib
import pedigree_code_strings
import crcmod.predefined

#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=====================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table.+\<\/table\>', '[]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_MC_Question(N, question, choices_list, answer):
	bb_question = ''

	number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'MC\t<p>{0}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	letters = 'ABCDEFGH'
	for i, choice in enumerate(choices_list):
		bb_question += '\t{0}'.format(choice)
		if choice == answer:
			prefix = 'x'
			bb_question += '\tCorrect'
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], choice))
	print("")
	return bb_question + '\n'


#=======================
def multipleChoiceQuestionSet():
	bb_output_format_list = []
	choices_list = ('autosomal dominant', 'autosomal recessive', 'x-linked dominant', 'x-linked recessive', 'y-linked')
	question_text = ("<p>Examine the pedigree above. "
	+"Which one of the following patterns of inheritance is most likely demonstrated in the above pedigree inheritance?</p> "
	)
	N = 0
	for ad in pedigree_code_strings.autosomal_dominant:
		if random.random() < 0.5:
			ad = pedigree_lib.mirrorPedigree(ad)
		adc = pedigree_lib.translateCode(ad)
		answer = 'autosomal dominant'
		N += 1
		bb_output_format = formatBB_MC_Question(N, adc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for ar in pedigree_code_strings.autosomal_recessive:			
		if random.random() < 0.5:
			ar = pedigree_lib.mirrorPedigree(ar)
		arc = pedigree_lib.translateCode(ar)
		answer = 'autosomal recessive'
		N += 1
		bb_output_format = formatBB_MC_Question(N, arc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for xd in pedigree_code_strings.x_linked_dominant:
		if random.random() < 0.5:
			xd = pedigree_lib.mirrorPedigree(xd)
		xdc = pedigree_lib.translateCode(xd)
		answer = 'x-linked dominant'
		N += 1
		bb_output_format = formatBB_MC_Question(N, xdc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for xr in pedigree_code_strings.x_linked_recessive:
		if random.random() < 0.5:
			xr = pedigree_lib.mirrorPedigree(xr)
		xrc = pedigree_lib.translateCode(xr)
		answer = 'x-linked recessive'
		N += 1
		bb_output_format = formatBB_MC_Question(N, xrc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)
	for yl in pedigree_code_strings.y_linked:
		if random.random() < 0.5:
			yl = pedigree_lib.mirrorPedigree(yl)
		ylc = pedigree_lib.translateCode(yl)
		answer = 'y-linked'
		N += 1
		bb_output_format = formatBB_MC_Question(N, ylc+question_text, choices_list, answer)
		bb_output_format_list.append(bb_output_format)

	return bb_output_format_list


#===============================
#===============================
#===============================
#===============================
if __name__ == '__main__':
	max_questions = 199
	max_questions = 17
	bb_output_format_list = multipleChoiceQuestionSet()
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
