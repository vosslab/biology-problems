#!/usr/bin/env python

import os
import sys
import random

import bptools

debug = False

types = {
	1: 'adjacent-1',
	2: 'adjacent-2',
	3: 'alternate',
	4: 'alternate',
}

#Mbp
chromosome_lengths = {
	1: (125,124),
	2: (93,149),
	3: (91,107),
	4: (50,140),
	5: (48,133),
	6: (61,110),
	7: (60,99),
	8: (46,101),
	9: (49,92),
	10: (40,95),
	11: (54,81),
	12: (36,98),
	13: (18,97),
	14: (17,90),
	15: (19,84),
	16: (37,54),
	17: (24,57),
	18: (17,61),
	19: (27,33),
	20: (28,36),
	21: (13,35),
	22: (15,37),
}
centromere_length = 20

color_scales = {
	'red': ['coral', 'lightsalmon', 'crimson'],
	'blue': ['deepskyblue', 'lightskyblue', 'royalblue'],
}

def drawChromosome(chromosome1, color='red'):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance = chromosome_lengths[chromosome1]
	table += '<colgroup width="{0}"></colgroup>'.format(distance[0]*2.4 - 16)
	table += '<colgroup width="{0}"></colgroup>'.format(32)
	table += '<colgroup width="{0}"></colgroup>'.format(distance[1]*2.4 - 16)
	table += '<tr>'
	table += '<td bgcolor="{1}" style="border: 2px solid black;" align="center"><span style="font-size: small"></span></td>'.format(chromosome1, color_scales[color][2])
	table += '<td bgcolor="{1}" style="border: 4px solid black;" align="center">{0}</td>'.format(chromosome1, color_scales[color][1])
	table += '<td bgcolor="{1}" style="border: 2px solid black;" align="center"><span style="font-size: large"></span></td>'.format(chromosome1, color_scales[color][2])
	table += '</tr>'
	table += '</table>'
	return table

def drawTranslocatedChromosome(chromosome1, chromosome2, color1='red', color2='blue'):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white; height: 30px">'
	distance1 = chromosome_lengths[chromosome1]
	distance2 = chromosome_lengths[chromosome2]
	table += '<colgroup width="{0}"></colgroup>'.format(distance1[0]*2.4 - 16)
	table += '<colgroup width="{0}"></colgroup>'.format(32)
	table += '<colgroup width="{0}"></colgroup>'.format(distance1[1]*1.2 - 8)
	table += '<colgroup width="{0}"></colgroup>'.format(distance2[1]*1.2 - 8)
	table += '<tr>'
	table += '<td bgcolor="{1}" style="border: 2px solid black;" align="center"><span style="font-size: large"></span></td>'.format(chromosome1, color_scales[color1][2])
	table += '<td bgcolor="{1}" style="border: 4px solid black;" align="center">{0}</td>'.format(chromosome1, color_scales[color1][1])
	table += '<td bgcolor="{1}" style="border: 2px solid black; border-right: 1px dashed black" align="center"><span style="font-size: large"></span></td>'.format(chromosome2, color_scales[color1][2])
	table += '<td bgcolor="{1}" style="border: 2px solid black; border-left: 1px dashed black" align="center"><span style="font-size: large"></span></td>'.format(chromosome2, color_scales[color2][2])
	table += '</tr>'
	table += '</table>'
	return table

def questionText(segregation_type, chromosome1, chromosome2):
	question = '<p>{0},{1}: {2}</p>'.format(chromosome1, chromosome2, types[segregation_type])
	question += '<p>A phenotypically normal prospective couple seeks genetic counseling '
	question += 'because the man knows that he has a balanced translocation of a portion of his '
	question += 'chromosome {0} that has been exchanged with a portion of his chromosome {1}.</p>'.format(chromosome1, chromosome2)
	question += '<p>Which two (2) of the following sets of gametes was formed by '
	question += '<strong>{0}</strong> segregation in this individual?</p><p></p> '.format(types[segregation_type])
	return question

def merge_tables(table_list):
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white;">'
	for chromo_table in table_list:
		table += '<tr>'
		table += '  <td align="left">{0}</td>'.format(chromo_table)
		table += '</tr>'
	table += '</table>'
	return table

def blackboardFormat(N, segregation_type, chromosome1, chromosome2):
	question_string = questionText(segregation_type, chromosome1, chromosome2)
	#print(question_string)

	table1 = ''
	#A. rob(14; 21)
	#B. rob(14; 21), +14
	#C. rob(14; 21), +21
	#D. -14
	#E. -21

	table1  = drawChromosome(chromosome1, 'red')
	table2  = drawChromosome(chromosome2, 'blue')
	table12 = drawTranslocatedChromosome(chromosome1, chromosome2, 'red', 'blue')
	table21 = drawTranslocatedChromosome(chromosome2, chromosome1, 'blue', 'red')
	table_merge = merge_tables([table1, table2, table12, table21])
	#print(table1+table2+table12+table21)
	question_string += table_merge
	question_string += '<p>all four of the chromosomes present in a somatic cell are shown above</p><p></p>'
	question_string += '<p>CHECK TWO BOXES!</p>'
	choices = []

	smtab = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	trtd = '<tr><td style="border: 0px solid white;">'

	alternate1 = smtab + trtd + 't({0}; {1}), t({1}; {0})</td></tr>'.format(chromosome1, chromosome2)
	alternate1 += trtd + table12 + '</td></tr>'
	alternate1 += trtd + table21 + '</td></tr>'
	alternate1 += '</table><p></p><hr/><p></p>'
	choices.append(alternate1)

	alternate2 = smtab + trtd + '{0}, {1}</td></tr>'.format(chromosome1, chromosome2)
	alternate2 += trtd + table1 + '</td></tr>'
	alternate2 += trtd + table2 + '</td></tr>'
	alternate2 += '</table><p></p><hr/><p></p>'
	choices.append(alternate2)

	adjacent1a = smtab + trtd + 't({0}; {1}), +{1}</td></tr>'.format(chromosome1, chromosome2)
	adjacent1a += trtd + table12 + '</td></tr>'
	adjacent1a += trtd + table2 + '</td></tr>'
	adjacent1a += '</table><p></p><hr/><p></p>'
	choices.append(adjacent1a)

	adjacent1b = smtab + trtd + 't({1}; {0}), +{0}</td></tr>'.format(chromosome1, chromosome2)
	adjacent1b += trtd + table21 + '</td></tr>'
	adjacent1b += trtd + table1 + '</td></tr>'
	adjacent1b += '</table><p></p><hr/><p></p>'
	choices.append(adjacent1b)

	adjacent2a = smtab + trtd + 't({0}; {1}), +{0}</td></tr>'.format(chromosome1, chromosome2)
	adjacent2a += trtd + table12 + '</td></tr>'
	adjacent2a += trtd + table1 + '</td></tr>'
	adjacent2a += '</table><p></p><hr/><p></p>'
	choices.append(adjacent2a)

	adjacent2b = smtab + trtd + 't({1}; {0}), +{1}</td></tr>'.format(chromosome1, chromosome2)
	adjacent2b += trtd + table21 + '</td></tr>'
	adjacent2b += trtd + table2 + '</td></tr>'
	adjacent2b += '</table><p></p><hr/><p></p>'
	choices.append(adjacent2b)

	answers = []
	if segregation_type == 1:
		answers.append(adjacent1a)
		answers.append(adjacent1b)
	elif segregation_type == 2:
		answers.append(adjacent2a)
		answers.append(adjacent2b)
	elif segregation_type == 3 or segregation_type == 4:
		#happens twice as often
		answers.append(alternate1)
		answers.append(alternate2)
	else:
		sys.exit(1)


	random.shuffle(choices)	
	blackboard = bptools.formatBB_MA_Question(N, question_string, choices, answers)

	return blackboard

if __name__ == "__main__":
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	num_problems = 24
	N = 0
	while N < num_problems:
		segregation_type = random.randint(1,4)
		chromosome1 = random.randint(1, 22-1)
		chromosome2 = random.randint(chromosome1+1, 22)
		if chromosome1 >= chromosome2:
			continue
		print("chromosome pair: {0} and {1}".format(chromosome1, chromosome2))
		N += 1
		final_question = blackboardFormat(N, segregation_type, chromosome1, chromosome2)
		f.write(final_question)
	f.close()
	bptools.print_histogram()
