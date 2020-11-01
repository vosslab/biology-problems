#!/usr/bin/env python

import sys
import copy
import random
import crossinglib

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
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw,Ab_color)
	table += '</tr>'
	table += '<tr><td align="center" colspan="3"><hr/></td></tr>'
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw,aB_color)
	table += '</tr>'
	table += '<tr><td align="center" colspan="3"><hr/></td></tr>'
	table += '<tr><td></td><td align="center">Genes 1&plus;2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += '</tr>'
	table += '</table>'

	assigned_colors = crossinglib.dihybridAssignColors(0, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'digenic inheritance'))

	description = table
	description += 'Gene 1 when dominant expresses an enzyme that creates a {0} pigment from a {1} precursor. '.format(Ab_color, ab_color)
	description += 'Gene 2 when dominant expresses an enzyme that creates a {0} pigment from a {1} precursor. '.format(aB_color, ab_color)
	description += 'When both genes are dominant, the two pigments combine to form a {0} color. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment and only the {0} color remains. '.format(ab_color)
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
	table += '<tr><td rowspan="3"></td><td align="center">gene 1</td><td rowspan="3"></td></tr>'
	table += '<tr><td align="center">&darr;</td></tr>'
	table += '<tr>'
	table += ' <td align="center"><span style="color: red;"><b>&#10005;</b></span></td>'
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw,Ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += '</tr>'
	table += '</table>'

	assigned_colors = crossinglib.dihybridAssignColors(1, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'recessive epistasis'))

	description = table
	description += 'When gene 1 is homozygous recessive, the gene expresses an ezymes that prevents any pigment from being created and it remains a {0} color. '.format(ab_color)
	description += 'Gene 2 only has an effect on the color when gene 1 is dominant. '.format(ab_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into a {1} pigment. '.format(Ab_color, AB_color)
	description += 'When both genes are dominant, it remains {0} in color. '.format(Ab_color)
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
	table += '<tr><td rowspan="3"></td><td align="center">Gene 1</td><td rowspan="3"></td></tr>'
	table += '<tr><td align="center">&darr;</td></tr>'
	table += '<tr>'
	table += ' <td align="center"><span style="color: red;"><b>&#10005;</b></span></td>'
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw,aB_color)
	table += '</tr>'
	table += '</table>'

	assigned_colors = crossinglib.dihybridAssignColors(2, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'dominant epistasis'))

	description = table
	description += 'When gene 1 is dominant, the gene expresses an ezymes that inhibits another enzyme that converts {0} pigment into {1} pigment. '.format(AB_color, ab_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into a {1} pigment. '.format(ab_color, aB_color)
	description += 'When both genes are dominant, because the dominant allele of gene 1 inhibits the production of the {0} color and so it will remain {1} in color. '.format(ab_color, AB_color)
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

	table = ''

	assigned_colors = crossinglib.dihybridAssignColors(3, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate recessive epistasis'))

	description = table
	description += 'A colored pigment is part of a two step metabolic pathway. '
	description += 'When gene 1 is dominant, the gene expresses an ezymes that converts a {0} pigment into a and precursor molecue with the same {0} color. '.format(AB_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} colored precursor molecule from gene 1 into a {1} pigment. '.format(AB_color, ab_color)
	description += 'The {0} color forms only when both genes are dominant, if either gene is homozygous recessive, the {1} color remains. '.format(ab_color, AB_color)
	return description

#===================
#===================
def duplicate_interaction_epistasis(color_set):
	#4: '9:6:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = crossinglib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = crossinglib.color_translate.get(Ab_color_raw, Ab_color_raw)
	aB_color = crossinglib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = crossinglib.color_translate.get(ab_color_raw, ab_color_raw)

	table = ''

	assigned_colors = crossinglib.dihybridAssignColors(4, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate interaction epistasis'))

	description = table
	description += 'When either gene 1 or gene 2 is dominant, they express an ezyme that converts a precursor {0} pigment into the {0} color. '.format(ab_color, AB_color)
	description += 'If both gene 1 and gene 2 are homozygous recessive, then only the {0} pigment is present'.format(ab_color)
	return description


	print("NOT DONE")
	return None

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
	table += '<tr><td rowspan="2"></td><td align="center">Gene 1</td><td rowspan="2"></td></tr>'
	table += '<tr><td align="center">&darr;</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += '</tr>'
	table += '<tr><td rowspan="2"></td><td align="center">&uarr;</td><<td rowspan="2"></td></tr>'
	table += '<tr><td align="center">Gene 2</td></tr>'
	table += '</table>'

	assigned_colors = crossinglib.dihybridAssignColors(5, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate dominant epistasis'))

	description = table
	description += 'A colored pigment is part of a two step metabolic pathway. '
	description += 'When either gene 1 or gene 2 is dominant, they express an ezyme that converts a precursor {0} pigment into the {0} color. '.format(ab_color, AB_color)
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
	table += '<tr><td rowspan="4"></td><td align="center">Gene 2</td></tr>'
	table += '<tr><td align="center">&darr;</td></tr>'
	table += '<tr><td align="center"><span style="color: red;"><b>&#10005;</b></span></td></tr>'
	table += '<tr><td align="center">Gene 1</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw,aB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += '</tr>'
	table += '</table>'

	assigned_colors = crossinglib.dihybridAssignColors(6, color_set)
	print(crossinglib.createDiHybridTable('A', 'B', assigned_colors, 'dominant and recessive epistasis'))

	description = table
	description += 'When gene 1 is dominant, the gene expresses an ezymes that converts a {0} pigment into a {1} pigment. '.format(AB_color, aB_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that completely suppresses the activity of gene 1. '
	description += 'When both genes are dominant, the dominant allele of gene 1 inhibits the production of the {0} color and so it remains {1} in color. '.format(aB_color, AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment and only the {0} color remains. '.format(AB_color)

	description = "WRONG COLOR DATA"

	return description

#===================
#===================
#===================
#===================
def questionContent(gene_id):
	question = ''
	question += '<p>Above are the phenotypic results from a dihybrid cross and double heterozygote test cross. '
	question += 'The phenotypes were '
	ratio = crossinglib.gene_type_ratios[gene_id]
	counts = ratio.split(':')
	for count in counts:
		question += '{0} to '.format(crossinglib.num2word[int(count)])
	question = question[:-4]
	question += ' ({0}).</p>'.format(ratio)
	question += '<p><strong>What type of gene interaction is being shown?</strong></p>'
	print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	assigned_colors = crossinglib.dihybridAssignColors(gene_id, color_set)
	dihybrid_table = crossinglib.createDiHybridTable(letter1, letter2, assigned_colors)
	testcross_table = crossinglib.createTestCrossTable(letter1, letter2, assigned_colors)

	# write the question content
	question = questionContent(gene_id)

	complete_question = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	complete_question += ' <tr><td> '
	complete_question += dihybrid_table
	complete_question += ' </td><td> '
	complete_question += '&nbsp;'
	complete_question += ' </td><td> '
	complete_question += testcross_table
	complete_question += '</td></tr></table> '

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
	gene_ids = list(crossinglib.gene_interaction_names.keys())
	random.shuffle(gene_ids)
	for k, sub_gene_id in enumerate(gene_ids):
		if sub_gene_id == answer:
			prefix = "*"
			status = "Correct"
		else:
			prefix = ""
			status = "Incorrect"
		name = crossinglib.gene_interaction_names[sub_gene_id]
		description = crossinglib.gene_type_description[sub_gene_id]
		choice_text = "These two genes show <strong>{0}</strong>. {1}.".format(name, description)
		file_handle.write("\t{0}\t{1}".format(choice_text, status))
		print("{0}{1}. {2}".format(prefix, choice_letters[k], choice_text))
	file_handle.write("\n")

#===================
#===================
#===================
#===================
if __name__ == '__main__':
	for method in (digenic_inheritance, recessive_epistasis, dominant_epistasis, duplicate_recessive_epistasis, duplicate_interaction_epistasis, duplicate_dominant_epistasis, dominant_and_recessive_epistasis):
		print(method(crossinglib.four_color_sets[0]))
		print('<br/><hr/><br/>')
	sys.exit(1)
	duplicates = 2
	file_handle = open("bbq-dihybrid_cross_gene_interactions.txt", "w")
	for i in range(duplicates):
		for gene_id in crossinglib.gene_interaction_names:
			for color_set in crossinglib.four_color_sets:
				writeQuestion(gene_id, color_set, file_handle)
			#sys.exit(1)
	file_handle.close()
