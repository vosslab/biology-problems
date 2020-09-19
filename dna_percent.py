#!/usr/bin/env python

import sys
import random

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

def printChoice(letter, nts, valuelist, prefix):
	mystr = ("%s%s. %s:%d, %s:%d, %s:%d"
		%(prefix, letter, nts[0], valuelist[0], nts[1], valuelist[1], nts[2], valuelist[2]))
	return mystr

if __name__ == '__main__':
	if len(sys.argv) > 1:
		percent = int(sys.argv[1])
	else:
		#percent = random.choice((10, 15, 20, 30, 35, 40))
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

	question = "2. In a sample of double stranded DNA, %d%s is %s. "%(percent, '%', nt2name[nt1])
	question += "What are the percentages of the other three (3) bases?"

	answer = getAnswer(nt1, percent)

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
		prefix = ""
		if valuelist == answer:
			prefix = "*"
		mystr += printChoice(letter, nts, valuelist, prefix)
		mystr += "\n"
	print(mystr)
	
