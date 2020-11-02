#!/usr/bin/env python

import sys
import copy
import random
import crossinglib

red_x = '<span style="color: red;"><b>&#10005;</b></span>'

#===================
#===================
def digenic_inheritance(color_set):
	#0: '9:3:3:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	table += '<tr>'
	table += ' <td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 1 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw, aB_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 2 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Genes 1&plus;2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Both Genes Dominant</b>'

	table += '</td></tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(0, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'digenic inheritance'))

	description = table+'</br>'
	description += 'Gene 1 when dominant expresses an enzyme that creates a {0} pigment from a {1} precursor. '.format(Ab_color, ab_color)
	description += 'Gene 2 when dominant expresses an enzyme that creates a {0} pigment from a {1} precursor. '.format(aB_color, ab_color)
	description += 'When both genes are dominant, the two pigments combine to form a {0} color. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and only the {0} pigment remains. '.format(ab_color)
	return description


#===================
#===================
def recessive_epistasis(color_set):
	#1: '9:3:4',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(5):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 1</td>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(1, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'recessive epistasis'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that converts the {0} pigment into a {1} pigment. '.format(ab_color, Ab_color)
	description += 'When gene 1 is homozygous recessive, it remains {0} in color. '.format(ab_color)
	description += 'Gene 2 only has an effect on the pigment when gene 1 is dominant. '
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into a {1} pigment. '.format(Ab_color, AB_color)
	return description

#===================
#===================
def dominant_epistasis(color_set):
	#2: '12:3:1',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(5):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td rowspan="2"></td><td align="center">Gene 1</td><td rowspan="2"></td></tr>'
	table += '<tr>'
	table += ' <td align="center">{0}&darr;{0}</td> '.format(red_x)
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw, aB_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(2, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'dominant epistasis'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that inhibits another enzyme that converts {0} pigment into {1} pigment. '.format(AB_color, ab_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into a {1} pigment. '.format(ab_color, aB_color)
	description += 'When both genes are dominant, the dominant allele of gene 1 inhibits the production of the {0} color, so it will remain the {1} color. '.format(ab_color, AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and only the {0} color remains. '.format(ab_color)
	return description

#===================
#===================
def duplicate_recessive_epistasis(color_set):
	#3: '9:7',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(5):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 1</td>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(3, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate recessive epistasis'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that converts a {0} pigment into a a second molecule with the same {0} color. '.format(ab_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the second {0} colored molecule from gene 1 into a {1} pigment. '.format(ab_color, AB_color)
	description += 'The {0} color forms only when both genes are dominant, if either gene is homozygous recessive, the {1} color remains. '.format(AB_color, ab_color)
	return description

#===================
#===================
def duplicate_interaction_epistasis(color_set):
	#4: '9:6:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	table += '<tr>'
	table += ' <td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 1 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 2 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Genes 1&plus;2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Both Genes Dominant</b>'

	table += '</td></tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(4, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate interaction epistasis'))

	#Complete dominance at both gene pairs; however, when either gene is dominant, it hides the effects of the other gene
	#Certain phenotypic traits depend on the dominant alleles of two gene loci. When dominant is present it will show its phenotype. The ratio will be 9: 6: 1.

	description = table+'</br>'
	description += 'Both Gene 1 and Gene 2 when dominant express an enzyme that creates a {0} pigment from a {1} precursor. '.format(Ab_color, ab_color)
	description += 'When both genes are dominant, the two enzymes combine to form a {0} color. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and only the {0} color remains. '.format(ab_color)
	return description

#===================
#===================
def duplicate_dominant_epistasis(color_set):
	#5: '15:1',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td><td></td></tr>'
	#table += '<tr><td></td><td align="center">&darr;</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += '</tr>'
	#table += '<tr><td></td><td align="center">&uarr;</td><<td rowspan="2"></td></tr>'
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(5, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate dominant epistasis'))

	description = table+'</br>'
	description += 'When either gene 1 or gene 2 is dominant, they express an enzyme that converts a precursor {0} pigment into a {1} pigment. '.format(ab_color, AB_color)
	description += 'If both gene 1 and gene 2 are homozygous recessive, then only the {0} pigment is present'.format(ab_color)
	return description

#===================
#===================
def dominant_and_recessive_epistasis(color_set):
	#6: '13:3',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	aB_color_raw = color_set[2]
	#ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	#ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td rowspan="3"></td><td align="center">Gene 1</td></tr>'
	table += '<tr><td align="center">{0}&darr;{0}</td></tr>'.format(red_x)
	table += '<tr><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw,aB_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = crossinglib.dihybridAssignColors(6, color_set)
	#print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'dominant and recessive epistasis'))

	description = table+'</br>'
	description += 'When gene 2 is dominant and gene 1 is homozygous recessive, gene 2 expresses an enzyme that converts a {0} pigment into a {1} pigment. '.format(AB_color, aB_color)
	description += 'Whenever gene 1 is dominant, then gene 1 expresses a protein that completely suppresses the activity of gene 2. '
	description += 'When both genes are dominant, the inhibited gene 2 is unable to produce the {0} pigment, so it remains {1} in color. '.format(aB_color, AB_color)
	description += 'If neither of the genes are dominant, then there is no active enzyme and only the {0} pigment remains. '.format(AB_color)

	return description

#===================
#===================
#===================
#===================
def questionContent(gene_id):
	question = '<br/>'
	question += '<p>The diagram and description above that explain the interaction of two genes. '
	question += ' <b>Determine the dihybird cross phenotypic ratio.</b></p>'
	#print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	#assigned_colors = crossinglib.dihybridAssignColors(gene_id, color_set)
	#dihybrid_table = crossinglib.createDiHybridTable(letter1, letter2, assigned_colors)
	#testcross_table = crossinglib.createTestCrossTable(letter1, letter2, assigned_colors)

	method = method_list[gene_id]
	header = method(color_set)

	# write the question content
	question = questionContent(gene_id)

	complete_question = header
	complete_question += " <br/> "
	complete_question += question

	print(complete_question)
	return complete_question


#===================
#===================
def writeQuestion(gene_id, color_set, file_handle):
	# make the question

	letter_pool = copy.copy(crossinglib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = [letter_pool.pop(), letter_pool.pop()]
	two_letters.sort()
	letter1 = two_letters[0]
	letter2 = two_letters[1]
	complete_question = makeQuestion(gene_id, color_set, letter1, letter2)

	# write the question
	choice_letters = "ABCDEFGHI"
	file_handle.write("MC\t{0}".format(complete_question))
	answer = gene_id
	mixed_gene_ids = list(crossinglib.gene_interaction_names.keys())
	random.shuffle(mixed_gene_ids)
	for k, sub_gene_id in enumerate(mixed_gene_ids):
		if sub_gene_id == answer:
			prefix = "*"
			status = "Correct"
		else:
			prefix = ""
			status = "Incorrect"
		ratio = crossinglib.gene_type_ratios[sub_gene_id]
		name = crossinglib.gene_interaction_names[sub_gene_id]
		description = crossinglib.gene_type_description[sub_gene_id]
		assigned_colors = crossinglib.dihybridAssignColors(sub_gene_id, color_set)
		data_table = crossinglib.createDiHybridTable('A', 'B', assigned_colors, name)
		choice_text = "<p>These two genes would show {0} and a <b>{1} ratio</b>.</p> {2}".format(name, ratio, data_table)
		file_handle.write("\t{0}\t{1}".format(choice_text, status))
		print("<p>{0}{1}. {2}</p>".format(prefix, choice_letters[k], ratio))
	file_handle.write("\n")


#===================
method_list = [
	digenic_inheritance,
	recessive_epistasis,
	dominant_epistasis,
	duplicate_recessive_epistasis,
	duplicate_interaction_epistasis,
	duplicate_dominant_epistasis,
	dominant_and_recessive_epistasis,
]

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	duplicates = 1
	file_handle = open("bbq-dihybrid_cross_gene_metabolics.txt", "w")
	for i in range(duplicates):
		for color_set in crossinglib.get_four_color_sets():
			for gene_id in crossinglib.gene_interaction_names:
				writeQuestion(gene_id, color_set, file_handle)
			#sys.exit(1)
	file_handle.close()
