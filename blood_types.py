#!/usr/bin/env python

import math
import random


def coagulated_blood():
	table = ''
	table += '<table style="border-collapse: collapse; border: 0px solid white;" cellpading="150" cellspacing="150">'
	table += '<tbody><tr>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">&#x25CF;</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">.</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 20px; color: darkred;">&#x25CF;</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">.</span></td>'
	table += '</tr><tr>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">.</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 30px; color: darkred;">&#x25CF;</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">.</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 15px; color: darkred;">&#x25CF;</span></td>'
	table += '</tr><tr>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 20px; color: darkred;">&#x25CF;</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">.</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">&#x25CF;</span></td>'
	table += '<td style="border: 0px solid white;"><span style="font-size: 25px; color: darkred;">.</span></td>'
	table += '</tr></tbody></table>'
	return table

def normal_blood():
	symbol = '<span style="font-size: 100px; color: red;">&#11054;</span>'
	return symbol


def createHtmlTable(code):
	table = ''
	table += '<table style="border-collapse: collapse; border: 1px; border-color: black;">'
	table += '<tbody>'
	table += '<tr>'
	#blood results row
	count = 0
	data_style = 'style="border: 2px solid gray; align: center;"'
	empty_style = 'style="border: 0px solid white;"'
	for c in list(code):
		count += 1
		table += '<td {0}>'.format(data_style)
		if c == '1':
			table += normal_blood()
		else:
			table += coagulated_blood()
		table += '</td>'
		table += '<td {0}> </td>'.format(empty_style)
	table += '<tr>'
	table += '<td {0}>A antigen</td>'.format(data_style)
	table += '<td {0}> </td>'.format(empty_style)
	table += '<td {0}>B antigen</td>'.format(data_style)
	table += '<td {0}> </td>'.format(empty_style)
	table += '<td {0}>D antigen</td>'.format(data_style)
	table += '<td {0}> </td>'.format(empty_style)
	table += '<td {0}>control</td>'.format(data_style)
	table += '<td {0}> </td>'.format(empty_style)
	table += '</tr></tbody></table>'
	return table

code2type = {
	'111':	'O-',
	'011':	'A-',
	'101':	'B-',
	'001':	'AB-',
	'110':	'O+',
	'010':	'A+',
	'100':	'B+',
	'000':	'AB+',
}

def getInvertCode(bcode):
	invert = bcode
	invert = invert.replace('0', '2')
	invert = invert.replace('1', '0')
	invert = invert.replace('2', '1')
	return invert

def flipPlace(bcode, place=3):
	newcode = bcode[:place-1]
	newcode += getInvertCode(bcode[place-1])
	newcode += bcode[place:]
	return newcode

def getWrongChoices(bcode):
	invert = getInvertCode(bcode)
	choices = []
	choices.append(bcode+'1')
	choices.append(bcode+'0')
	choices.append(invert+'1')
	choices.append(invert+'0')
	extras = []
	for choice in choices:
		extras.append(flipPlace(choice, 3))
	random.shuffle(extras)
	#choices.extend(extras)
	choices.append(extras.pop())
	choices.append(extras.pop())
	random.shuffle(choices)
	return choices

def code2display(bcode):
	display_txt = bcode
	display_txt = display_txt.replace("0", "%")
	display_txt = display_txt.replace("1", "O")
	return display_txt

if __name__ == '__main__':
	bcodes = list(code2type.keys())
	N = 0
	letters = "ABCDEFG"
	f = open("blackboard-blood_types_upload.txt", "a")
	for bcode in bcodes:
		N += 1
		answer = bcode+"1"
		choices = getWrongChoices(bcode)
		question = ''
		#question += "{0}. ".format(N)
		question += "What will the results of a blood test look like for a person "
		question += "with <b>{0} blood type</b>?".format(code2type[bcode])
		print(question)
		f.write("MC\t")
		f.write("{0}\t".format(question))
		i = 0
		for choice in choices:
			prefix = "Incorrect"
			if choice == answer:
				prefix = 'Correct'
			ltr = letters[i]
			table = createHtmlTable(choice)
			display_txt = code2display(choice)
			choice_txt = "<p>{0}</p><p>image of blood type result, looks like {1}</p>".format(table, display_txt)
			print("{0}{1}. {2}".format(prefix, ltr, display_txt))
			f.write("{0}\t".format(choice_txt))
			f.write("{0}\t".format(prefix))
			i += 1
		print("")
		f.write('\n')
	f.close()
