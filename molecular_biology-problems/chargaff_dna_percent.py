#!/usr/bin/env python3

import os
import sys
import random

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
	# Iterate through the three nucleotides
	for i in range(3):
		# Get the first letter of the nucleotide to use as a key for the colormap
		nt = nts[i][0]
		# Fetch the corresponding color
		color = colormap[nt]
		# Append the formatted string, color-coded and with full nucleotide names, abbreviations, and perhaps an em dash as a separator
		mystr += "<span style='color: {0};'>{1} ({2}): {3:2d}%</span> &mdash; ".format(color, nt2name[nts[i]], nt, valuelist[i])
	# Remove the trailing em dash and space
	return mystr[:-9]

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

	# Ensure the nucleotide is uppercase to match the colormap keys
	nt = nt1[0].upper()
	# Assign the appropriate color for the nucleotide based on the colormap
	color = colormap[nt]

	# Initialize the question string with a precise introductory phrase
	question = "<p>According to Chargaff's rules concerning the base pairing composition in double-stranded DNA, "
	# Eliminate redundancy and improve formality by replacing 'Given' with 'consider'
	question += "consider a sample where the percentage composition of "

	# Utilize HTML to emphasize and color-code the percentage and nucleotide type
	# Here, I retained your existing format and just tweaked the wording
	question += "<strong><span style='color: {0};'>{1:2d}% is {2}</span></strong>.</p>".format(color, percent, nt2name[nt])
	# Formulate the follow-up query in a separate paragraph for clarity
	question += "<p>What are the percentages of the other three bases?</p>"

	answer = getAnswer(nt1, percent)

	#print(question)
	choices = []
	offperc = 50 - percent
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

	
