#!/usr/bin/env python

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

gene_type_description = {
	0: 'interaction of two genes affect the phenotypic expression of a single trait',
	1: 'when one gene is homozygous recessive, it hides the phenotype of the other gene',
	2: 'when one gene is dominant, it hides the phenotype of the other gene',
	3: 'when either gene is homozygous recessive, it hides the effect of the other gene',
	4: 'when either gene is dominant, it hides the effects of the other gene',
	5: 'when either gene is dominant, it shows the same phenotype',
	6: 'when one gene is dominant and another gene is homozygous recessive, it creates a new phenotype',
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
	'yellowgreen': 'light green',

	'palegreen': 'green',
	'snow': 'white',
	'azure': 'white',
	'ivory': 'white',
}

color_sets = [
	['tomato', 'orange', 'yellow', 'snow'],
	['cornflowerblue', 'palegreen', 'yellow', 'ivory'],
	['tomato', 'sienna', 'goldenrod', 'yellow'],
	['tomato', 'orange', 'pink', 'snow',],
	['cornflowerblue ', 'yellowgreen', 'aquamarine', 'azure',],
	['tomato', 'orchid', 'salmon', 'snow'],
	['cornflowerblue', 'powderblue', 'tan', 'ivory'],
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
def createDataTable(gene_type, letter1, letter2, color_set, title=None):
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
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray'>Genotypes</th> ".format(title)
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
	#always dominant color
	table += " <td align='center' style='background-color: {0};'>{1}{1}{2}{2}</td>".format(color_set[0], letter1.upper(), letter2.upper())


	table += "</tr>"

	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.upper(), letter2.lower())
	table += formatHeterozygoes(gene_type, letter, color_set)
	#always recessive color
	table += " <td align='center' style='background-color: {0};'>{1}{1}</td>".format(color_set[2], letter.lower())
	table += "</tr>"

	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.upper())
	table += "</tr>"


	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}{1}</td>".format(letter1.lower(), letter2.lower())
	table += " <td align='center' style='background-color: {0};'>{1}{1}{2}{2}</td>".format(color_set[0], letter1.lower(), letter2.lower())
	table += "</tr>"


	table += "</table>"
	return table


#===================
#===================
def questionContent(gene_type, color_set):
	question = ''
	question += '<p>Above are the phenotypic results from a monohybrid cross. '
	question += 'The phenotypes were '

	color1 = color_translate.get(color_set[0], color_set[0])
	color2 = color_translate.get(color_set[1], color_set[1])
	color3 = color_translate.get(color_set[2], color_set[2])

	if gene_type == 'complete dominance':
		question += 'three {0} and one {1} '.format(color1, color3)
	else:
		truebreeds = [color1, color3,]
		random.shuffle(truebreeds)
		for color in truebreeds:
			question += '{0}, '.format(color)
		if gene_type == 'incomplete dominance':
			question += ' and {0}'.format(color2)
		elif gene_type == 'codominance':
			question += ' and speckled {0} and {1}'.format(truebreeds[0],truebreeds[1])
	question += '</p><p><strong>What type of dominance is being shown?</strong></p>'
	print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set, letter1, letter2):
	"""
	gene ids

	0: '9:3:3:1',
	1: '9:3:4',
	2: '12:3:1',
	3: '9:7',
	4: '9:6:1',
	5: '15:1',
	6: '13:3',
	"""

	gene_table = createDataTable(gene_type, letter, color_set, 'Gene 1')
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
#===================
#===================
if __name__ == '__main__':
	duplicates = 1
	letters = "ABCDEFGHI"
	gene_letters = list('ADEGRT')
	gene_letters = list('AD')
	f = open("bbq-dihybrid_cross_gene_interactions.txt", "w")
	for i in range(len(gene_letters)):
		for j in range(i+1, len(gene_letters)):
			for gene_id in gene_types:
				for color_set in color_sets:
					letter1 = gene_letters[i]
					letter2 = gene_letters[j]
					complete_question = makeQuestion(gene_id, color_set, letter1, letter2)
					f.write("MC\t{0}".format(complete_question))
					answer = gene_type
					gene_types_copy = copy.copy(gene_types)
					gene_types_copy.append('epistasis')
					gene_types_copy.append('X-linked recessive')
					random.shuffle(gene_types_copy)
					for k, sub_gene_type in enumerate(gene_types_copy):
						if sub_gene_type == answer:
							prefix = "*"
							status = "Correct"
						else:
							prefix = ""
							status = "Incorrect"
						choice_text = "The gene shows {0}".format(sub_gene_type)
						f.write("\t{0}\t{1}".format(choice_text, status))
						print("{0}{1}. {2}".format(prefix, letters[k], choice_text))
					f.write("\n")
	f.close()
