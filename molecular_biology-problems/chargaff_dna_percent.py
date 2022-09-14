#!/usr/bin/env python3

import os
import sys
import random

import seqlib
import bptools

#========================================
nt2name = {
	'A':	'adenine',
	'C':	'cytosine',
	'G':	'guanine',
	'T':	'thymine',
	'U':	'uracil',
	'Ade':	'adenine',
	'Cyt':	'cytosine',
	'Gua':	'guanine',
	'Thy':	'thymine',
	'Ura':	'uracil',
}

#========================================
canonical = {
	'A':	'Ade',
	'C':	'Cyt',
	'G':	'Gua',
	'T':	'Thy',
	'U':	'Ura',
	'Ade':	'Ade',
	'Cyt':	'Cyt',
	'Gua':	'Gua',
	'Thy':	'Thy',
	'Ura':	'Ura',
	'adenine':	'Ade',
	'cytosine':	'Cyt',
	'guanine':	'Gua',
	'thymine':	'Thy',
	'uracil':	'Ura',
}

#========================================
complement = {
	'A': 'T',
	'T': 'A',
	'G': 'C',
	'C': 'G',
	'Ade': 'Thy',
	'Thy': 'Ade',
	'Gua': 'Cyt',
	'Cyt': 'Gua',
}

#========================================
def getAnswer(nt1, percent):
	#nt2 = complement(nt1)
	offperc = 50 - percent
	if nt1.startswith("A"):
		#CGT
		answer = [offperc, offperc, percent]
	elif nt1.startswith("C"):
		#AGT
		answer = [offperc, percent, offperc]
	elif nt1.startswith("G"):
		#ACT
		answer = [offperc, percent, offperc]
	elif nt1.startswith("T"):
		#ACG
		answer = [percent, offperc, offperc]
	return answer

#========================================
colormap = {
	'A': '#004d00', #A is green
	'C': '#003566', #C is blue
	'T': '#6e1212', #T is red
	'G': '#2a2000', #G is black
	'U': '#420080', #U is purple
}

#========================================
def printChoice(nts, valuelist):
	global colormap
	mystr = ''
	#seqlib.colorNucleotideForeground()
	for i in range(3):
		nt = nts[i][0]
		color = colormap[nt]
		mystr += "<span style='color: {0};'>{1}:{2:02d}%</span>, ".format(color, nts[i], valuelist[i])
	return mystr

#========================================
#========================================
def makeQuestion(N):
	global colormap
	if random.random() < 0.5:
		percent = random.randint(1,23)
	else:
		percent = random.randint(27,49)

	nt1 = None
	if len(sys.argv) > 2:
		text = sys.argv[2].strip()
		keys = list(canonical.keys())
		if text in keys:
			nt1 = canonical[text]

	nts = ['Ade', 'Cyt', 'Thy', 'Gua']
	random.shuffle(nts)
	if nt1 is None:
		nt1 = nts.pop()
	else:
		nts.remove(nt1)
	nts.sort()

	question = "<p>According to Chargraff's experimental data "
	question += "and a sample of double stranded DNA where "
	nt = nt1[0].upper()
	color = colormap[nt]
	question += "<strong><span style='color: {0};'>{1:02d}% is {2}</strong>.</p>".format(color, percent, nt2name[nt1])
	question += "<p>What are the percentages of the other three (3) bases?</p>"

	answer = getAnswer(nt1, percent)

	#print(question)
	choices = []
	offperc = 50 - percent
	avgperc = 25
	choices.append([offperc, offperc, percent])
	choices.append([offperc, percent, offperc])
	choices.append([percent, offperc, offperc])
	offchoices = []
	offchoices.append([offperc, 25, 25])
	offchoices.append([25, offperc, 25])
	offchoices.append([25, 25, offperc])
	random.shuffle(offchoices)
	choices.append(offchoices[0])
	choices.append(offchoices[1])
	random.shuffle(choices)
	
	choices_list = []
	for valuelist in choices:
		choice_text = printChoice(nts, valuelist)
		choices_list.append(choice_text)
		if valuelist == answer:
			answer_text = choice_text
	
	complete_question = bptools.formatBB_MC_Question(N, question, choices_list, answer_text)
	return complete_question

#========================================
#========================================
if __name__ == '__main__':
	num_questions = 199
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_questions):
		complete_question = makeQuestion(i+1)
		f.write(complete_question)
	f.close()

	
