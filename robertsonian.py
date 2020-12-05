#!/usr/bin/env python

import os
import sys
import copy
import math
import numpy
import random

debug = False

#Mbp
chromosome_lengths = {
	13: (18,97),
	14: (17,90),
	15: (19,84),
	21: (13,35),
	22: (15,37),
}
centromere_length = 20

def drawChromosome(chromosome1, color='coral'):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance = chromosome_lengths[chromosome1]
	table += '<colgroup width="{0}"></colgroup>'.format(distance[0]*3-12)
	table += '<colgroup width="{0}"></colgroup>'.format(24)
	table += '<colgroup width="{0}"></colgroup>'.format(distance[1]*3-12)
	table += '<tr>'
	table += '<td bgcolor="{1}"  style="border: 2px solid black;" align="center"><span style="font-size: small">{0}p</span></td>'.format(chromosome1, color)
	table += '<td bgcolor="SlateGray" style="border: 4px solid black;"></td>'
	table += '<td bgcolor="{1}"   style="border: 2px solid black;" align="center"><span style="font-size: small">{0}q</span></td>'.format(chromosome1, color)
	table += '</tr>'
	table += '</table>'
	return table

def drawRobertChromosome(chromosome1, chromosome2, color1='coral', color2='deepskyblue'):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance1 = chromosome_lengths[chromosome1]
	distance2 = chromosome_lengths[chromosome2]
	table += '<colgroup width="{0}"></colgroup>'.format(distance1[1]*3-12)
	table += '<colgroup width="{0}"></colgroup>'.format(24)
	table += '<colgroup width="{0}"></colgroup>'.format(distance2[1]*3-12)
	table += '<tr>'
	table += '<td bgcolor="{1}"  style="border: 2px solid black;" align="center"><span style="font-size: small">{0}q</span></td>'.format(chromosome1, color1)
	table += '<td bgcolor="SlateGray" style="border: 4px solid black;"></td>'
	table += '<td bgcolor="{1}"   style="border: 2px solid black;" align="center"><span style="font-size: small">{0}q</span></td>'.format(chromosome2, color2)
	table += '</tr>'
	table += '</table>'
	return table

def questionText(chromosome1, chromosome2):
	question = ''
	question += '<p>An individual has a Robertsonian translocation involving chromosomes '
	question += '{0} and {1}.</p>'.format(chromosome1, chromosome2)
	question += '<h5>Which one of the following gametes was formed by alternate segregation in this individual?</h5>'
	return question

def blackboardFormat(chromosome1, chromosome2):
	question_string = questionText(chromosome1, chromosome2)
	table1 = ''
	#A. rob(14; 21)
	#B. rob(14; 21), +14
	#C. rob(14; 21), +21
	#D. -14
	#E. -21

	if random.random() < 0.5:
		color1 = 'deepskyblue'
		color2 = 'coral'
	else:
		color1 = 'coral'
		color2 = 'deepskyblue'

	table1  = drawChromosome(chromosome1, color1)
	table2  = drawChromosome(chromosome2, color2)
	table12 = drawRobertChromosome(chromosome1, chromosome2, color1, color2)

	choices = []

	smtab = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	trtd = '<tr><td style="border: 0px solid white;">'

	answer = '{2}{3}rob({0}; {1})</td></tr>'.format(chromosome1, chromosome2, smtab, trtd)
	answer += trtd + table12 + '</td></tr>'
	answer += '</table><p></p><p></p>'
	choices.append(answer)

	wrong = '{2}{3}rob({0}; {1}), +{0}</td></tr>'.format(chromosome1, chromosome2, smtab, trtd)
	wrong += trtd + table12 + '</td></tr>'
	wrong += trtd + table1 + '</td></tr>'
	wrong += '</table><p></p><p></p>'
	choices.append(wrong)

	wrong = '{2}{3}rob({0}; {1}), +{1}</td></tr>'.format(chromosome1, chromosome2, smtab, trtd)
	wrong += trtd + table12 + '</td></tr>'
	wrong += trtd + table2 + '</td></tr>'
	wrong += '</table><p></p><p></p>'
	choices.append(wrong)

	wrong = '{2}{3}&ndash;{0}</td></tr>'.format(chromosome1, chromosome2, smtab, trtd)
	wrong += trtd + table2 + '</td></tr>'
	wrong += '</table><p></p><p></p>'
	choices.append(wrong)

	wrong = '{2}{3}&ndash;{1}</td></tr>'.format(chromosome1, chromosome2, smtab, trtd)
	wrong += trtd + table1 + '</td></tr>'
	wrong += '</table><p></p><p></p>'
	choices.append(wrong)

	blackboard = "MC\t"
	blackboard += question_string
	#print(question)

	random.shuffle(choices)
	for c in choices:
		blackboard += "\t" + c
		if c == answer:
			blackboard += '\tCorrect'
		else:
			blackboard += '\tIncorrect'

	print(question_string)
	return blackboard

if __name__ == "__main__":
	filename = "bbq-robertsonian.txt"
	f = open(filename, "w")
	acrocentric_chromosomes = [13, 14, 15, 21, 22]
	duplicates = 2
	for i in range(duplicates):
		for chromosome1 in acrocentric_chromosomes:
			for chromosome2 in acrocentric_chromosomes:
				if chromosome1 >= chromosome2:
					continue
				final_question = blackboardFormat(chromosome1, chromosome2)
				print(chromosome1, chromosome2)
				f.write(final_question+'\n')
	f.close()
