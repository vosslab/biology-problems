#!/usr/bin/env python

import copy
import random

gene_types = [
	'incomplete dominance',
	'codominance',
	'complete dominance',
]
random.shuffle(gene_types)

color_translate = {
	'tomato': 'red',
	'darkturquoise': 'blue',
	'chartreuse': 'green',
	'royalblue': 'blue',
	'sienna': 'dark brown',
	'peru': 'light brown',
	'goldenrod': 'light brown',
	'snow': 'white',
	'#e6f2ff': 'white',
	'#ff9999': 'red',
	'#99c2ff': 'light blue',
	'#dd99ff': 'purple' ,
	'#99ccff': 'blue',
	'palegreen': 'green',
	'#4d94ff': 'blue',
	'#4dffc3': 'blue-green'
}

color_sets = [
	['tomato', 'orange', 'yellow',],
	['#4d94ff', 'palegreen', 'yellow'],
	['sienna', 'goldenrod', 'yellow'],
	['tomato', 'pink', 'snow',],
	['#4d94ff', '#99c2ff', '#e6f2ff',],
	['#ff9999', '#dd99ff', '#4d94ff'],
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
def createDataTable(gene_type, letter, color_set, title=None):
	table = '<table border=1 style="border: 1px solid black; border-collapse: collapse; ">'
	table += '<colgroup width="60"></colgroup> '
	table += '<colgroup width="60"></colgroup> '
	table += '<colgroup width="80"></colgroup> '
	table += '<colgroup width="80"></colgroup> '

	table += "<tr>"
	if title is not None:
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray'>{0}</th> ".format(title)
	else:
		table += " <th align='center' colspan='2' rowspan='2' style='background-color: lightgray'>Genotypes</th> ".format(title)
	table += " <th align='center' colspan='2'>Female &female;</th> "
	table += "</tr>"

	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}</td>".format(letter.upper())
	table += " <td align='center' style='background-color: lightgray'>{0}</td>".format(letter.lower())
	table += "</tr>"

	table += "<tr>"
	table += " <th align='center' rowspan='2'><br/>Male<br/>&male;<br/><br/></th> "
	table += " <td align='center' style='background-color: lightgray;'>{0}</td>".format(letter.upper())
	#always dominant color
	table += " <td align='center' style='background-color: {0};'>{1}{1}</td>".format(color_set[0], letter.upper())
	table += formatHeterozygoes(gene_type, letter, color_set)
	table += "</tr>"

	table += "<tr>"
	table += " <td align='center' style='background-color: lightgray'>{0}</td>".format(letter.lower())
	table += formatHeterozygoes(gene_type, letter, color_set)
	#always recessive color
	table += " <td align='center' style='background-color: {0};'>{1}{1}</td>".format(color_set[2], letter.lower())
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
	#gene_letters = list('A')
	f = open("bbq-monohybird_cross_dominance.txt", "w")
	for letter in gene_letters:
		for gene_type in gene_types:
			for color_set in color_sets:
				complete_question = makeQuestion(gene_type, color_set, letter)
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
