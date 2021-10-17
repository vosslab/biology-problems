#!/usr/bin/env python

import os
import random
import restrictlib

#============================================
#============================================
def tdBlock(vtype="top", htype="middle", fill_color="white", strand_color="black", tick_color="#999999", fragment=True):
	border_str = ""
	if vtype == "top" and not fragment:
		border_str += 'border-bottom: 4px solid {0}; '.format(strand_color)
	elif vtype == "top" and not (htype == "start" or htype == "end"):
		border_str += 'border-bottom: 4px solid {0}; '.format(strand_color)
	else:
		border_str += 'border-bottom: 0px solid {0}; '.format(fill_color)

	if vtype == "bottom" and not fragment:
		border_str += 'border-top: 4px solid {0}; '.format(strand_color)
	elif vtype == "bottom" and not (htype == "start" or htype == "end"):
		border_str += 'border-top: 4px solid {0}; '.format(strand_color)
	else:
		border_str += 'border-top: 0px solid {0}; '.format(fill_color)

	if htype == "start" or htype == "right":
		border_str += 'border-right: 2px solid {0}; '.format(tick_color)
	else:
		border_str += 'border-right: 0px solid {0}; '.format(fill_color)

	if htype == "end" or htype == "left":
		border_str += 'border-left: 2px solid {0}; '.format(tick_color)
	else:
		border_str += 'border-left: 0px solid {0}; '.format(fill_color)

	return '  <td style="{0}" bgcolor="{1}"> </td> '.format(border_str, fill_color)

#============================================
#============================================
def longDNA(vtype="top", fill_color="white", strand_color="gray", tick_color="#999999"):
	border_str = ""
	if vtype == "top":
		border_str += 'border-bottom: 4px dotted {0}; '.format(strand_color)
	else:
		border_str += 'border-bottom: 0px solid {0}; '.format(fill_color)

	if vtype == "bottom":
		border_str += 'border-top: 4px dotted {0}; '.format(strand_color)
	else:
		border_str += 'border-top: 0px solid {0}; '.format(fill_color)

	border_str += 'border-right: 0px solid {0}; '.format(fill_color)
	border_str += 'border-left: 0px solid {0}; '.format(fill_color)

	return '  <td style="{0}" bgcolor="{1}"> </td> '.format(border_str, fill_color)

#============================================
#============================================
def makeTable(length, label_dict=None, fragment=True):
	if label_dict is None:
		label_dict = { 1: "EcoRI", 4: "NheI", }
	table = ""
	space_width = 20
	table = '<table cellpading="0" cellspacing="0" border="0" style="border-collapse: collapse; "> '
	table += '<colgroup width="{0}"></colgroup> '.format(space_width*2)
	for i in range(2*length+2):
		table += '<colgroup width="{0}"></colgroup> '.format(space_width)
	table += '<colgroup width="{0}"></colgroup> '.format(space_width*2)

	table += "<tbody>"

	#Restriction Enzymes
	#DNA number row
	table += "<tr>"
	table += '<td style="border: 0px solid white; "></td>'
	for i in range(length+1):
		msg = label_dict.get(i, "")
		table += '<td align="center" colspan="2" style="border: 0px solid white; "><i>{0}</i></td>'.format(msg)
	table += '<td style="border: 0px solid white; "></td>'
	table += "</tr>"

	#DNA top row
	table += "<tr>"
	if fragment is True:
		table += '<td style="border: 0px solid white; "></td>'
	else:
		table += longDNA("top")
	table += tdBlock("top", "start", fragment=fragment)
	for i in range(length):
		table += tdBlock("top", "left", fragment=fragment)
		table += tdBlock("top", "right", fragment=fragment)
	table += tdBlock("top", "end", fragment=fragment)
	if fragment is True:
		table += '<td style="border: 0px solid white; "></td>'
	else:
		table += longDNA("top")
	table += "</tr>"

	#DNA bottom row
	table += "<tr>"
	if fragment is True:
		table += '<td style="border: 0px solid white; "></td>'
	else:
		table += longDNA("bottom")
	table += tdBlock("bottom", "start", fragment=fragment)
	for i in range(length):
		table += tdBlock("bottom", "left", fragment=fragment)
		table += tdBlock("bottom", "right", fragment=fragment)
	table += tdBlock("bottom", "end", fragment=fragment)
	if fragment is True:
		table += '<td style="border: 0px solid white; "></td>'
	else:
		table += longDNA("bottom")
	table += "</tr>"

	#DNA number row
	table += "<tr>"
	table += '<td style="border: 0px solid white; "></td>'
	for i in range(length+1):
		table += '<td align="center" colspan="2" style="border: 0px solid white; ">{0}</td>'.format(i)
	table += '<td style="border: 0px solid white; "></td>'
	table += "</tr>"

	table += "</tbody>"
	table += "</table>"
	return table

#============================================
#============================================
def getRandList(size, total_length, include_ends=False):
	if include_ends is True:
		a = list(range(total_length+1))
	else:
		a = list(range(1, total_length))
	random.shuffle(a)
	while len(a) > size:
		a.pop()
	a.sort()
	return a

#============================================
#============================================
#============================================
if __name__ == '__main__':
	length = 10
	fragment = True
	enzymes = restrictlib.get_enzyme_list()
	enzyme_class1 = restrictlib.random_enzyme_one_end(enzymes)
	enzyme_name1 = enzyme_class1.__name__
	enzyme_class2 = restrictlib.random_enzyme_one_end(enzymes, badletter=enzyme_name1[0])
	enzyme_name2 = enzyme_class2.__name__

	answers = []
	if fragment is True:
		a = getRandList(3, length, include_ends=False)
		label_dict = {
			a[0]: enzyme_name1,
			a[1]: enzyme_name2,
			a[2]: enzyme_name1,
		}
		answers = [a[0], a[2]-a[0], length-a[2]]
	else:
		a = getRandList(5, length, include_ends=False)
		label_dict = {
			a[0]: enzyme_name1,
			a[1]: enzyme_name2,
			a[2]: enzyme_name1,
			a[3]: enzyme_name2,
			a[4]: enzyme_name1,
		}
		answers = [a[2]-a[0], a[4]-a[2]]
	answers.sort()
	print(answers)

	table = makeTable(length, label_dict, fragment)
	header = "<p>Below is a linear piece of DNA that is {0:d} kb in length.</p> ".format(length)
	details = "<p>There are two (2) different types of restriction sites: {0} and {1} labeled at the top of the DNA strand.</p>".format(enzyme_name1, enzyme_name2)
	if fragment is False:
		details += "<p>The dashes at the left and right indicate that the next restriction site is very far away and will not be present on a gel.</p>"
	question = "<h6>Determine the sizes of bands that would appear on a gel after restriction enzyme digestion with only <i>{0}</i>.</h6>".format(enzyme_name1)
	print(header+details+question)
	#print(header+table+details+question)

	max_answer = max(answers)
	answer_str = ""
	last_answer = max(max_answer+1, 5)
	for i in range(1, last_answer+1):
		answer_str += "{0} kb\t".format(i)
		if i in answers:
			answer_str += "Correct\t"
		else:
			answer_str += "Incorrect\t"
	print(answer_str)
	#sys.exit(1)
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'a')
	f.write("MA\t")
	f.write(header+table+details+question+"\t")
	f.write(answer_str)
	f.write('\n')
	f.close()
