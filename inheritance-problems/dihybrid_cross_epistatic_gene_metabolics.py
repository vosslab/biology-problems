#!/usr/bin/env python3

import os
import re
import sys
import copy
import random
import hybridcrosslib as dihybridcrosslib
import crcmod.predefined


red_x = '<span style="color: red;"><b>&#10005;</b></span>'

#===================
#===================
def digenic_inheritance(color_set):
	# Four colors
	#0: '9:3:3:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

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

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(0, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'digenic inheritance'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'Gene 1 when dominant expresses an enzyme that creates the {0} pigment from the {1} precursor pigment. '.format(Ab_color, ab_color)
	description += 'Gene 2 when dominant expresses an enzyme that creates the {0} pigment from the {1} precursor pigment. '.format(aB_color, ab_color)
	description += 'When both genes are dominant, the two enzymes pathways combine to form the new {0} pigment. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and the {0} precursor pigment remains. '.format(ab_color)
	return description


#===================
#===================
def recessive_epistasis(color_set):
	# Three colors
	#1: '9:3:4',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

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

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(1, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'recessive epistasis'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that converts the {0} precursor pigment into the {1} pigment. '.format(ab_color, Ab_color)
	description += 'When gene 1 is homozygous recessive, there is no pigment change and the {0} precursor pigment remains. '.format(ab_color)
	description += 'Gene 2 only has an effect on the pigment when gene 1 is dominant. '
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into the {1} pigment. '.format(Ab_color, AB_color)
	return description

#===================
#===================
def dominant_epistasis(color_set):
	# Three colors
	#2: '12:3:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

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
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(2, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'dominant epistasis'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color.<li> '
	description += '<uL>When gene 1 is dominant, the gene expresses an enzyme that inhibits another enzyme '
	description += 'that converts the {0} precursor pigment into the {1} pigment.</ul> '.format(AB_color, ab_color)
	description += '<uL>When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into the {1} pigment.</ul> '.format(ab_color, Ab_color)
	description += '<uL>When both genes are dominant, the dominant allele of gene 1 inhibits '
	description += 'the production of the {0} color, so it will remain the {1} precursor color.</ul> '.format(ab_color, AB_color)
	description += '<uL>When both of the genes are homozygous recessive, then the first enzyme is active (not inhibited) and '
	description += 'the {0} precursor pigment is converted to the {1} pigment and '.format(AB_color, ab_color)
	description += 'it will remain the final pigment, as the second enzyme is inactive.</ul></li> '
	return description

#===================
#===================
def duplicate_recessive_epistasis(color_set):
	# Two colors
	#3: '9:7',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

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

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(3, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate recessive epistasis'))

	description = table+'</br>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that converts the {0} precursor pigment into a a second molecule with the same {0} pigment. '.format(ab_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the second {0} pigment molecule from gene 1 into the {1} pigment. '.format(ab_color, AB_color)
	description += 'The {0} pigment forms only when both genes are dominant, if either gene is homozygous recessive, the {1} pigment will remain. '.format(AB_color, ab_color)
	return description

#===================
#===================
def duplicate_interaction_epistasis(color_set):
	# Three colors
	#4: '9:6:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

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

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(4, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate interaction epistasis'))

	#Complete dominance at both gene pairs; however, when either gene is dominant, it hides the effects of the other gene
	#Certain phenotypic traits depend on the dominant alleles of two gene loci. When dominant is present it will show its phenotype. The ratio will be 9: 6: 1.

	description = table+'</br>'
	description += 'Both Gene 1 and Gene 2 when dominant express an enzyme that convert the {0} precursor pigment into the {1} pigment. '.format(ab_color, Ab_color)
	description += 'When both genes are dominant, the two enzymes combine to form the new {0} pigment. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and only the {0} precursor pigment remains. '.format(ab_color)
	return description



#===================
#===================
def duplicate_dominant_epistasis(color_set):
	# Two colors
	#5: '15:1',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

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

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(5, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate dominant epistasis'))

	description = table+'</br>'
	description += 'When either gene 1 or gene 2 is dominant, they express an enzyme that converts the {0} precursor pigment into the {1} pigment. '.format(ab_color, AB_color)
	description += 'If both gene 1 and gene 2 are homozygous recessive, then only the {0} precursor pigment is present'.format(ab_color)
	return description

#===================
#===================
def dominant_and_recessive_epistasis(color_set):
	# Two colors
	#6: '13:3',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = dihybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = dihybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = dihybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = dihybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td rowspan="3"></td><td align="center">Gene 1</td></tr>'
	table += '<tr><td align="center">{0}&darr;{0}</td></tr>'.format(red_x)
	table += '<tr><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = dihybridcrosslib.dihybridAssignColors(6, color_set)
	#print(dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'dominant and recessive epistasis'))

	description = table+'</br>'
	description += 'When gene 2 is dominant and gene 1 is homozygous recessive, '
	description += 'gene 2 expresses an active enzyme that converts the {0} precursor pigment into the {1} pigment. '.format(AB_color, ab_color)
	description += 'Whenever gene 1 is dominant, then gene 1 expresses a protein that completely suppresses the activity of gene 2. '
	description += 'When both genes are dominant, the inhibited gene 2 is unable to produce the {0} pigment, so the {1} precursor pigment remains. '.format(ab_color, AB_color)
	description += 'If neither of the genes are dominant, then there is no active enzyme and again only the {0} precursor pigment remains. '.format(AB_color)

	return description

#===================
#===================
#===================
#===================
def questionContent(gene_id):
	question = '<br/>'
	question += '<p>The diagram and description above explain the interaction of two genes. '
	question += ' <b>Determine the dihybird cross phenotypic ratio.</b></p>'
	#print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	#assigned_colors = dihybridcrosslib.dihybridAssignColors(gene_id, color_set)
	#dihybrid_table = dihybridcrosslib.createDiHybridTable(letter1, letter2, assigned_colors)
	#testcross_table = dihybridcrosslib.createTestCrossTable(letter1, letter2, assigned_colors)

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

#=======================
def getCrc16_FromString(mystr):
	crc16 = crcmod.predefined.Crc('xmodem')
	crc16.update(mystr.encode('ascii'))
	return crc16.hexdigest().lower()

#=====================
def makeQuestionPretty(question):
	pretty_question = copy.copy(question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<table.+\<\/table\>', '[TABLE]\n', pretty_question)
	#print(len(pretty_question))
	pretty_question = re.sub('\<\/p\>\s*\<p\>', '\n', pretty_question)
	#print(len(pretty_question))
	return pretty_question

#=====================
def formatBB_MC_Question(N, question, choices_list, answer):
	bb_question = ''

	number = "{0}. ".format(N)
	crc16 = getCrc16_FromString(question)
	bb_question += 'MC\t<p>{0}. {1}</p> {2}'.format(N, crc16, question)
	pretty_question = makeQuestionPretty(question)
	print('{0}. {1} -- {2}'.format(N, crc16, pretty_question))

	letters = 'ABCDEFGH'
	for i, choice in enumerate(choices_list):
		bb_question += '\t{0}.  {1}&nbsp; '.format(letters[i], choice)
		if choice == answer:
			prefix = 'x'
			bb_question += '\tCorrect'
		else:
			prefix = ' '
			bb_question += '\tIncorrect'
		print("- [{0}] {1}. {2}".format(prefix, letters[i], makeQuestionPretty(choice)))
	print("")
	return bb_question + '\n'

#===================
#===================
def writeQuestion(N, gene_id, color_set):
	# make the question

	letter_pool = copy.copy(dihybridcrosslib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = [letter_pool.pop(), letter_pool.pop()]
	two_letters.sort()
	letter1 = two_letters[0]
	letter2 = two_letters[1]
	complete_question = makeQuestion(gene_id, color_set, letter1, letter2)

	# write the question
	choice_letters = "ABCDEFGHI"
	answer_gene_id = gene_id
	num_colors = dihybridcrosslib.gene_type_num_colors[answer_gene_id]
	wrong_gene_ids = []
	mixed_gene_ids = list(dihybridcrosslib.gene_interaction_names_plus.keys())
	if answer_gene_id == 1:
		mixed_gene_ids.remove(10)
	for sub_gene_id in mixed_gene_ids:
		if dihybridcrosslib.gene_type_num_colors[sub_gene_id] == num_colors:
			wrong_gene_ids.append(sub_gene_id)
	while len(wrong_gene_ids) < 5:
		wrong_gene_ids.append(random.choice(mixed_gene_ids))
		wrong_gene_ids = list(set(wrong_gene_ids))
	print(answer_gene_id, wrong_gene_ids)
	#sys.exit(1)

	random.shuffle(wrong_gene_ids)
	random.shuffle(wrong_gene_ids)
	choices_list = []
	for k, sub_gene_id in enumerate(wrong_gene_ids):
		ratio = dihybridcrosslib.gene_type_ratios[sub_gene_id]
		name = dihybridcrosslib.gene_interaction_names_plus[sub_gene_id]
		#description = dihybridcrosslib.gene_type_description[sub_gene_id]
		assigned_colors = dihybridcrosslib.dihybridAssignColorsModified(sub_gene_id, color_set)
		data_table = dihybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, name)
		choice_text = "<p>These two genes would show {0} and a <b>{1} ratio</b>.</p> {2}".format(name, ratio, data_table)
		choices_list.append(choice_text)
		if sub_gene_id == answer_gene_id:
			answer_text = choice_text
	complete_bb_question = formatBB_MC_Question(N, complete_question, choices_list, answer_text)
	return complete_bb_question


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
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	file_handle = open(outfile, 'w')
	N = 0
	for i in range(duplicates):
		for color_set in dihybridcrosslib.get_four_color_sets():
			for gene_id in dihybridcrosslib.gene_interaction_names:
				N += 1
				complete_bb_question = writeQuestion(N, gene_id, color_set)
				file_handle.write(complete_bb_question)
	file_handle.close()
