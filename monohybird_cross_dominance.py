#!/usr/bin/env python

import copy
import random
import crossinglib

#===================
#===================
def questionContent(gene_type, color_set):
	question = ''
	question += '<p>Above are the phenotypic results from a monohybrid cross. '
	question += 'The phenotypes were '

	color1 = crossinglib.color_translate.get(color_set[0], color_set[0])
	color2 = crossinglib.color_translate.get(color_set[1], color_set[1])
	color3 = crossinglib.color_translate.get(color_set[2], color_set[2])

	if gene_type == 'complete dominance':
		question += 'three {0} and one {1}. '.format(color1, color3)
	else:
		truebreeds = [color1, color3,]
		random.shuffle(truebreeds)
		for color in truebreeds:
			question += '{0}, '.format(color)
		if gene_type == 'incomplete dominance':
			question += ' and {0}. '.format(color2)
		elif gene_type == 'codominance':
			question += ' and speckled {0} and {1}. '.format(truebreeds[0],truebreeds[1])
	question += '</p><p><strong>What type of dominance is being shown?</strong></p>'
	print(question)
	return question

#===================
#===================
def makeQuestion(gene_type, color_set, letter):
	"""
	gene types

	0: 'complete dominance',
	1: 'incomplete dominance',
	2: 'codominance',
	"""

	gene_table = crossinglib.createSingleGeneTable(gene_type, letter, color_set, 'Gene 1')
	print(gene_table)

	# write the question content
	question = questionContent(gene_type, color_set)

	complete_question = ''
	complete_question += gene_table
	complete_question += " <br/> "
	complete_question += question

	return complete_question

#===================
#===================
def writeQuestion(letter, gene_type, color_set, file_handle):
	complete_question = makeQuestion(gene_type, color_set, letter)
	answer = gene_type
	gene_types_copy = copy.copy(crossinglib.single_gene_types)
	gene_types_copy.append('epistasis')
	gene_types_copy.append('X-linked recessive')
	random.shuffle(gene_types_copy)

	choice_letters = "ABCDEFGHI"
	file_handle.write("MC\t{0}".format(complete_question))
	for k, sub_gene_type in enumerate(gene_types_copy):
		if sub_gene_type == answer:
			prefix = "*"
			status = "Correct"
		else:
			prefix = ""
			status = "Incorrect"
		choice_text = "The gene shows {0}".format(sub_gene_type)
		file_handle.write("\t{0}\t{1}".format(choice_text, status))
		print("{0}{1}. {2}".format(prefix, choice_letters[k], choice_text))
	file_handle.write("\n")
	return

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	duplicates = 1
	#gene_letters = list('A')
	file_handle = open("bbq-monohybird_cross_dominance.txt", "w")
	for letter in crossinglib.gene_letters:
		for gene_type in crossinglib.single_gene_types:
			for color_set in crossinglib.three_color_sets:
				writeQuestion(letter, gene_type, color_set, file_handle)
	file_handle.close()
