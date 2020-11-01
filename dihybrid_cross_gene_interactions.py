#!/usr/bin/env python

import sys
import copy
import random

gene_type_names = {
	0: 'digenic inheritance',
	1: 'recessive epistasis',
	2: 'dominant epistasis',
	3: 'duplicate recessive epistasis',
	4: 'duplicate interaction',
	5: 'duplicate dominant epistasis',
	6: 'dominant and recessive epistasis',
}

num2word = {
	1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
	6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
	11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
	15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
	20: 'twenty',
}

gene_type_description = {
	0: 'Interaction of two genes affect the phenotypic expression of a single trait',
	1: 'When one gene is homozygous recessive, it hides the phenotype of the other gene',
	2: 'When one gene is dominant, it hides the phenotype of the other gene',
	3: 'When either gene is homozygous recessive, it hides the effect of the other gene',
	4: 'When either gene is dominant, it hides the effects of the other gene',
	5: 'When either gene is dominant, it shows the same phenotype',
	6: 'When one gene is dominant and another gene is homozygous recessive, it creates a new phenotype',
}

gene_type_ratios = {
	0: '9:3:3:1',
	1: '9:3:4',
	2: '12:3:1',
	3: '9:7',
	4: '9:6:1',
	5: '15:1',
	6: '13:3',
}


color_translate = {
	'tomato': 'red',
	'cornflowerblue': 'blue',

	'chartreuse': 'green',
	'royalblue': 'blue',
	'sienna': 'dark brown',
	'peru': 'light brown',
	'goldenrod': 'light brown',
	'lightgreen': 'light green',
	'salmon': 'pink',
	'lightsalmon': 'pink',

	'palegreen': 'green',
	'snow': 'white',
	'azure': 'white',
	'ivory': 'white',
}

color_sets = [
	['tomato', 'goldenrod', 'yellow', 'snow'],
	['cornflowerblue', 'palegreen', 'yellow', 'ivory'],
	['sienna', 'tomato', 'goldenrod', 'yellow'],
	['tomato', 'goldenrod', 'pink', 'snow',],
	['cornflowerblue ', 'lime', 'aquamarine', 'azure',],
	['tomato', 'plum', 'lightsalmon', 'snow'],
	['cornflowerblue', 'tan', 'powderblue', 'ivory'],
	['cornflowerblue', 'salmon', 'yellow', 'gainsboro'],
]
random.shuffle(color_sets)

#===================
#===================
#===================
#===================
def formatHeterozygoes(gene_type, letter, color_set):
	table = ''
	if gene_type == 'complete dominance':
		table += " <td align='center' style='background-color: {0};'>{1}{2}</td>".format(color_set[0], letter.upper(), letter.lower())
	elif gene_type == 'incomplete dominance':
		table += " <td align='center' style='background-color: {0};'>{1}{2}</td>".format(color_set[1], letter.upper(), letter.lower())
	elif gene_type == 'codominance':
		symbol = "&#10057;&#10057;"
		table += " <td align='center' style='background-color: {1};'><span style='color: {2};'>{0}{0}{0}<br/>{0}</span> {3}{4} <span style='color: {2};'>{0}<br/>{0}{0}{0}</span></td>".format(symbol, color_set[0], color_set[2], letter.upper(), letter.lower())
	return table

#===================
#===================
def createDiHybridTable(letter1, letter2, assigned_colors, title=None):
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="60"></colgroup> '
	table += '<colgroup width="60"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '

	table += "<tr>"
	if title is not None:
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray'>{0}</th> ".format(title)
	else:
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray; vertical-align: middle;'>Dihybrid<br/>Cross</th> "
	table += " <th align='center' colspan='4'>Female &female;</th> "
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.upper())
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.lower())
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.upper())
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.lower())
	table += "</tr>"

	table += "<tr>"
	table += " <th align='center' rowspan='4' style='vertical-align: middle;'>Male<br/>&male;</th> "
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.upper())
	table += " <td align='center' style='background-color: {0};'>{1}{1}{3}{3}</td>".format(assigned_colors[0][0], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{1}{3}{4}</td>".format(assigned_colors[0][1], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{3}</td>".format(assigned_colors[0][2], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{4}</td>".format(assigned_colors[0][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{1}{3}{4}</td>".format(assigned_colors[1][0], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{1}{4}{4}</td>".format(assigned_colors[1][1], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{4}</td>".format(assigned_colors[1][2], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{4}{4}</td>".format(assigned_colors[1][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.upper())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{3}</td>".format(assigned_colors[2][0], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{4}</td>".format(assigned_colors[2][1], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{2}{2}{3}{3}</td>".format(assigned_colors[2][2], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{2}{2}{3}{4}</td>".format(assigned_colors[2][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{4}</td>".format(assigned_colors[3][0], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{4}{4}</td>".format(assigned_colors[3][1], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{2}{2}{3}{4}</td>".format(assigned_colors[3][2], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{2}{2}{4}{4}</td>".format(assigned_colors[3][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "</table>"
	return table


#===================
#===================
def createTestCrossTable(letter1, letter2, assigned_colors, title=None):
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="60"></colgroup> '
	table += '<colgroup width="60"></colgroup> '
	table += '<colgroup width="80"></colgroup> '

	table += "<tr>"
	if title is not None:
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray'>{0}</th> ".format(title)
	else:
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray; vertical-align: middle;'>Test<br/>Cross</th> "
	table += " <th align='center' colspan='1'>Female &female;</th> "
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.lower())
	table += "</tr>"

	table += "<tr>"
	table += " <th align='center' rowspan='4' style='vertical-align: middle;'>Male<br/>&male;</th> "
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.upper())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{3}{4}</td>".format(assigned_colors[0][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{2}{4}{4}</td>".format(assigned_colors[1][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.upper())
	table += " <td align='center' style='background-color: {0};'>{2}{2}{3}{4}</td>".format(assigned_colors[2][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{2}{2}{4}{4}</td>".format(assigned_colors[3][3], letter1.upper(), letter1.lower(), letter2.upper(), letter2.lower())
	table += "</tr>"


	table += "</table>"
	return table

#===================
#===================
def assignColors(gene_id, color_set):
	assigned_colors = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

	#gene 1 dominant; gene 2 dominant
	color1 = color_set[0]
	assigned_colors[0][0] = color1
	assigned_colors[0][1] = color1
	assigned_colors[0][2] = color1
	assigned_colors[0][3] = color1
	assigned_colors[1][0] = color1
	assigned_colors[1][2] = color1
	assigned_colors[2][0] = color1
	assigned_colors[2][1] = color1
	assigned_colors[3][0] = color1

	#gene 1 dominant; gene 2 recessive
	if gene_id in [2,5,6]:
		color2 = color_set[0]
	elif gene_id in [0,1,4]:
		color2 = color_set[1]
	elif gene_id in [3,]:
		color2 = color_set[3]
	assigned_colors[1][1] = color2
	assigned_colors[1][3] = color2
	assigned_colors[3][1] = color2

	#gene 1 recessive; gene 2 dominant
	if gene_id in [5,]:
		color3 = color_set[0]
	elif gene_id in [4,]:
		color3 = color_set[1]
	elif gene_id in [0,2,6]:
		color3 = color_set[2]
	elif gene_id in [1,3]:
		color3 = color_set[3]
	assigned_colors[2][2] = color3
	assigned_colors[2][3] = color3
	assigned_colors[3][2] = color3

	#gene 1 recessive; gene 2 recessive
	if gene_id in [6,]:
		color4 = color_set[0]
	elif gene_id in [0,1,2,3,4,5,]:
		color4 = color_set[3]
	assigned_colors[3][3] = color4

	return assigned_colors


#===================
#===================
def questionContent(gene_id):
	question = ''
	question += '<p>Above are the phenotypic results from a dihybrid cross and double heterozygote test cross. '
	question += 'The phenotypes were '
	ratio = gene_type_ratios[gene_id]
	counts = ratio.split(':')
	for count in counts:
		question += '{0} to '.format(num2word[int(count)])
	question = question[:-4]
	question += ' ({0}).</p>'.format(ratio)
	question += '<p><strong>What type of gene interaction is being shown?</strong></p>'
	print(question)
	return question


#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	assigned_colors = assignColors(gene_id, color_set)
	dihybrid_table = createDiHybridTable(letter1, letter2, assigned_colors)
	testcross_table = createTestCrossTable(letter1, letter2, assigned_colors)
	#print(gene_table)

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
#===================
#===================
if __name__ == '__main__':
	duplicates = 2
	letters = "ABCDEFGHI"
	gene_letters = list('ADEGRT')
	#gene_letters = list('DGR')
	f = open("bbq-dihybrid_cross_gene_interactions.txt", "w")
	#for i in range(len(gene_letters)):
	#for j in range(i+1, len(gene_letters)):
	for i in range(duplicates):
		for gene_id in gene_type_names:
			for color_set in color_sets:
				letter_pool = copy.copy(gene_letters)
				random.shuffle(letter_pool)
				two_letters = [letter_pool.pop(), letter_pool.pop()]
				two_letters.sort()
				letter1 = two_letters[0]
				letter2 = two_letters[1]
				complete_question = makeQuestion(gene_id, color_set, letter1, letter2)
				f.write("MC\t{0}".format(complete_question))
				answer = gene_id
				gene_ids = list(gene_type_names.keys())
				random.shuffle(gene_ids)
				for k, sub_gene_id in enumerate(gene_ids):
					if sub_gene_id == answer:
						prefix = "*"
						status = "Correct"
					else:
						prefix = ""
						status = "Incorrect"
					name = gene_type_names[sub_gene_id]
					description = gene_type_description[sub_gene_id]
					choice_text = "These two genes show <strong>{0}</strong>. {1}.".format(name, description)
					f.write("\t{0}\t{1}".format(choice_text, status))
					print("{0}{1}. {2}".format(prefix, letters[k], choice_text))
				f.write("\n")
			#sys.exit(1)
	f.close()
