#!/usr/bin/env python3

import os
import sys
import time
import random
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
def writeQuestion(N=1, length=10, num_sites=2, dna_type='fragment', max_fragment_size=7):

	enzymes = restrictlib.get_enzyme_list()
	enzyme_class1 = restrictlib.random_enzyme_one_end(enzymes)
	enzyme_name1 = enzyme_class1.__name__
	enzyme_class2 = restrictlib.random_enzyme_one_end(enzymes, badletter=enzyme_name1[0])
	enzyme_name2 = enzyme_class2.__name__

	if dna_type == 'strand' and num_sites < 3:
		print("Strand mode requires at least 3 sites")
		sys.exit(1)
	elif dna_type == 'fragment' and num_sites < 2:
		print("Fragment mode requires at least 2 sites")
		sys.exit(1)

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
	if dna_type == 'fragment':
		header = "<p>Below is a short fragment of DNA that is {0:d} kb in length.</p> ".format(length)
	elif dna_type == 'strand':
		header = "<p>Below is a long strand of DNA, a close up of particular section is shown.</p> "
	details  = "<p>There are two (2) different types of restriction sites: "
	details += "<i>{0}</i> and <i>{1}</i> labeled at the top of the DNA strand.</p>".format(enzyme_name1, enzyme_name2)
	if dna_type == 'strand':
		details += "<p>Note: The dashes at the left and right indicate that the next restriction site is"
		details += "very far away and will not be appear in a gel; it will likely be stuck in the well.</p>"
	question = "<h6>Determine the sizes of bands that would appear on a gel "
	question += "after restriction enzyme digestion with only <i>{0}</i>.</h6>".format(enzyme_name1)
	#print(header+details+question)
	#print(header+table+details+question)

	max_answer = max(answers)
	last_answer = max(max_answer+1, 5)
	choices_list = []
	answers_list = []
	for i in range(1, last_answer+1):
		choice_str = "{0:d} kb".format(i)
		choices_list.append(choice_str)
		if i in answers:
			answers_list.append(choice_str)
	#sys.exit(1)
	question_text = header+table+details+question
	bb_question = bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)
	return bb_question

#============================================
#============================================
#============================================
if __name__ == '__main__':
	num_questions = 10
	length=18
	num_sites=4
	#dna_type='fragment' # short piece of DNA
	dna_type='strand' # long strand of DNA
	max_fragment_size = 7
	print("num_questions=", num_questions)
	print("length=", length)
	print("num_sites=", num_sites)
	print("dna_type=", dna_type)



	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	N = 0
	for i in range(num_questions):
		bb_question = writeQuestion(N, length, num_sites, dna_type, max_fragment_size)
		if bb_question is not None:
			N += 1
			f.write(bb_question)
	f.close()
	bptools.print_histogram()
	print("Wrote", N, "of", num_questions, "questions")
