#!/usr/bin/env python

import sys
import copy
import random

def html_print(ordered, metabolites, classes):
	htmltext = ""

	tdopen = '<td align="center" valign="middle">'
	width = 60 * (len(ordered) +1)
	htmltext += ('<table width={0:d}px cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">'.format(width))
	htmltext += ('<tr><td></td>')
	for molecule in ordered:
		htmltext += ('{0}{1}</td>'.format(tdopen, molecule))
	htmltext += ('</tr>')
	for i in range(len(classes)):
		htmltext += ('<tr>')
		alive = False
		htmltext += ('{0}Class {1:d}</td>'.format(tdopen, i+1))
		happylist = {}
		happymeta = classes[i]
		for m in metabolites:
			if m == happymeta:
				alive = True
			happylist[m] = alive
		for m in ordered:
			if happylist[m] is True:
				htmltext += ('{0}+</td>'.format(tdopen))
			else:
				htmltext += ('{0}&ndash;</td>'.format(tdopen))
		htmltext += ('</tr>')
	htmltext += ('</table>')
	return htmltext



if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_metabolites = int(sys.argv[1])
	else:
		num_metabolites = 4
	question_type = 1

	charlist = "ABCDEGHJKMPQRSTWXYZ"
	ordered = list(charlist[-num_metabolites:])
	old_question = ""

	metabolites = copy.copy(ordered)
	random.shuffle(metabolites)
	for i in range(len(metabolites)-1):
		old_question += (metabolites[i]+" -> ")
	old_question += (metabolites[-1])
	#print("")

	classes = copy.copy(ordered)
	random.shuffle(classes)
	#print(classes)
	#print(metabolites)
	#print(ordered)
	#print("")

	class_count = {}

	for m in ordered:
		old_question += ("\t"+m)
	old_question += ('\n')
	for i in range(len(classes)):
		alive = False
		old_question += ("Class %d\t"%(i+1))
		happylist = {}
		happymeta = classes[i]
		for m in metabolites:
			if m == happymeta:
				alive = True
			happylist[m] = alive
		for m in ordered:
			if happylist[m] is True:
				old_question += ('+\t')
				class_count[i+1] = class_count.get(i+1, 0) + 1
			else:
				old_question += ('-\t')
		old_question += ('\n')
	print("")

	#print(old_question)
	#print(class_count)

	answer = "".join(metabolites)
	metabolic_text = "&nbsp;({0}-{1})".format(ordered[0], ordered[-1])
	
	if question_type == 1:
		question = "blank 1. "
	elif question_type == 2:
		question = "1. "

	question += "<p>A mutant screen was carried out to produce the diagram below. "
	question += "The diagram shows different classes&nbsp;(1-{0}) of mutants for metabolic precursors{0} of a metabolic pathway to produce a product were characterized to either grow&nbsp;(+) or not grow&nbsp;(&ndash;) in minimal media.".format(len(ordered), metabolic_text)
	question += ('</p>')
	question += html_print(ordered, metabolites, classes)


	if question_type == 1:
		question += "<h6>Write the metabolic precursors{0} in their correct order for the pathway without spaces or dashes. ".format(metabolic_text)
		example_text = answer
		while example_text == answer:
			example = copy.copy(ordered)
			random.shuffle(example)
			example_text = "".join(example)
		question += "For example, {0}.</h6>".format(example_text)
		answer = "".join(metabolites)
		print(question)
		print("A. {0}".format(answer))
	elif question_type == 2:
		question += "<h6>Which one of the following classes is the <i>wild-type</i> organism?</h6>"
		print(question)
		for i in range(len(classes)):
			ltr = charlist[i]
			prefix = ""
			if class_count[i+1] == len(classes):
				prefix = "*"
			print("{0}{1}. Class {2:d}".format(prefix, ltr, i+1))



