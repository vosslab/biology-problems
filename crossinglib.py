
import sys
import copy
import random

gene_letters = list('ADEGRT')

gene_interaction_names = {
	0: 'digenic inheritance',
	1: 'recessive epistasis',
	2: 'dominant epistasis',
	3: 'duplicate recessive epistasis',
	4: 'duplicate interaction',
	5: 'duplicate dominant epistasis',
	6: 'dominant and recessive epistasis',
}

single_gene_types = [
	'incomplete dominance',
	'codominance',
	'complete dominance',
]
random.shuffle(single_gene_types)

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
	'cornflowerblue': 'blue',
	'royalblue': 'blue',
	'sienna': 'dark brown',
	'tomato': 'red',

	'chartreuse': 'green',
	'peru': 'light brown',
	'goldenrod': 'light brown',
	'lightgreen': 'light green',
	'salmon': 'pink',
	'lightsalmon': 'pink',
	'lightcoral': 'pink',
	'plum': 'purple',
	'palegreen': 'green',
	'lightskyblue': 'light blue',

	'snow': 'white',
	'azure': 'white',
	'ivory': 'white',
}

three_color_sets = [
	['tomato', 'orange', 'yellow',],
	['cornflowerblue', 'palegreen', 'yellow'],
	['sienna', 'goldenrod', 'yellow'],
	['tomato', 'pink', 'snow',],
	['cornflowerblue', 'lightskyblue ', 'azure',],
	['lightsalmon ', 'plum', 'cornflowerblue'],
]
random.shuffle(three_color_sets)

four_color_sets = [
	['tomato', 'goldenrod', 'yellow', 'snow'],
	['cornflowerblue', 'palegreen', 'yellow', 'ivory'],
	['sienna', 'tomato', 'goldenrod', 'yellow'],
	['tomato', 'goldenrod', 'pink', 'snow',],
	['cornflowerblue ', 'lime', 'aquamarine', 'azure',],
	['tomato', 'plum', 'lightsalmon', 'snow'],
	['cornflowerblue', 'tan', 'powderblue', 'ivory'],
	['cornflowerblue', 'salmon', 'yellow', 'gainsboro'],
]
random.shuffle(four_color_sets)

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
def createSingleGeneTable(gene_type, letter, color_set, title=None):
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
def dihybridAssignColors(gene_id, color_set):
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
