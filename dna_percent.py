#!/usr/bin/env python

import sys
import copy
import random


nt2name = {
	'A':	'adenine',
	'C':	'cytosine',
	'G':	'guanine',
	'T':	'thymine',
	'U':	'uracil',
}

complement = {
	'A': 'T',
	'T': 'A',
	'G': 'C',
	'C': 'G',
}

def printChoice(letter, nts, valuelist):
	mystr = ("%s. %s:%d, %s:%d, %s:%d"
		%(letter, nts[0], valuelist[0], nts[1], valuelist[1], nts[2], valuelist[2]))
	return mystr

if __name__ == '__main__':

	percent = random.choice((10, 15, 20, 30, 35, 40))

	nts = ['A', 'C', 'T', 'G']
	random.shuffle(nts)
	nt1 = nts.pop()

	question = "XXX. In a sample of double stranded DNA, %d%s is %s. "%(percent, '%', nt2name[nt1])
	question += "What are the percentages of the other three (3) bases?"

	print(question)
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
	
	letters = ('A', 'B', 'C', 'D', 'E')
	mystr = ""
	for i in range(len(choices)):
		valuelist = choices[i]
		letter = letters[i]
		mystr += printChoice(letter, nts, valuelist)
		mystr += "\t"
	print(mystr)
	
