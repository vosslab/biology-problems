#!/usr/bin/env python

import sys
import copy
import random

used_markers = {}

def createMarker(num_markers):
	charlist = "ABCDEFG"
	markers = []
	for i in range(num_markers):
		letter = charlist[i]
		num = random.choice(list(range(1,10)))
		marker = "%s%d"%(letter, num)
		while used_markers.get(marker) is not None:
			num = random.choice(list(range(1,10)))
			marker = "%s%d"%(letter, num)
		used_markers[marker] = True
		markers.append(marker)
	return set(markers)

def markersToString(markers):
	mystr = ""
	markerlist = list(markers)
	markerlist.sort()
	for marker in markerlist:
		mystr += "%s,"%(marker)
	return mystr[:-1]

def splitMarkers(markers1, markers2):
	markerlist1 = list(markers1)
	markerlist1.sort()
	markerlist2 = list(markers2)
	markerlist2.sort()
	markerselect = []
	while len(set(markerselect)) <= 1:
		markerselect = []
		for i in range(len(markerlist1)):
			markerselect.append(random.choice((1,2)))
	newmarkers = []
	for i in range(len(markerselect)):
		ms = markerselect[i]
		if ms == 1:
			newmarkers.append(markerlist1[i])
		else:
			newmarkers.append(markerlist2[i])
	return set(newmarkers)


if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_markers = int(sys.argv[1])
	else:
		num_markers = 2
	if num_markers > 7:
		num_markers = 7
		
	mom1 = createMarker(num_markers)
	mom2 = createMarker(num_markers)
	dad1 = createMarker(num_markers)
	dad2 = createMarker(num_markers)
	print(mom1, mom2, dad1, dad2)
	print("")

	#question = "XXX. "
	question = ""
	question += ('A mother has a HLA genotype of <span style="color:FireBrick">{0}</span> on one chromosome and <span style="color:DarkGoldenRod">{1}</span> on the other. '
			.format(markersToString(mom1), markersToString(mom2)))
	question += ('The father has a HLA genotype of <span style="color:DarkViolet">{0}</span> on one chromosome and <span style="color:DarkBlue">{1}</span> on the other. '
			.format(markersToString(dad1), markersToString(dad2)))
	question += 'Which one of the following is a possible genotype for one of their offspring?'
	print(question)

#A father has a HLA genotype of A2,B1 on one chromosome and A7,B6 on the other.
#The mother has an HLA genotype of A4,B3 on one chromosome and A5,B9 on the other.
#Which one of the following is a possible genotype for one of their offspring?

	answers = []

	#wrong two moms
	answer = copy.copy(mom1)
	answer = answer.union(mom2)
	answers.append(answer)
	
	#wrong two dads
	answer = copy.copy(dad1)
	answer = answer.union(dad2)
	answers.append(answer)

	#real correct answer
	answer = copy.copy(random.choice((dad1, dad2)))
	answer = answer.union(random.choice((mom1, mom2)))
	answers.append(answer)
	correct = answer

	#jumbled 1
	answer = splitMarkers(mom1, mom2)
	answer = answer.union(splitMarkers(dad1, dad2))
	answers.append(answer)

	#jumbled 2
	answer = splitMarkers(mom1, mom2)
	answer = answer.union(splitMarkers(dad1, dad2))
	answers.append(answer)

	stringanswers = []
	for a in answers:
		stringanswers.append(markersToString(a))
	stringanswers = list(set(stringanswers))
	correct_str = markersToString(correct)


	random.shuffle(stringanswers)
	charlist = "ABCDE"
	answer_str = ""
	for i in range(len(stringanswers)):
		c = charlist[i]
		a = stringanswers[i]
		prefix = ''
		answer_str += "{0}\t".format(a)
		if a == correct_str:
			answer_str += "Correct\t"
			prefix = '*'
		else:
			answer_str += "Incorrect\t"
		print(("{0}{1}. {2}".format(prefix,c,a)))

	
	f = open("bbq-hla_genotypes.txt", "a")
	f.write("MC\t")
	f.write(question+"\t")
	f.write(answer_str)
	f.write('\n')
	f.close()


