#!/usr/bin/env python

import random

num2txt = {
	1: 'one',
	2: 'two',
	3: 'three',
	4: 'four',
	5: 'five',
	6: 'six',
	7: 'seven',
	8: 'eight',
	9: 'nine',
}

def makeChoose(n, r):
	choose = ""
	choose += "<table border=1 style='border-collapse: collapse; border: 1px solid white;'>"
	choose += "<tr>"
	choose += " <td rowspan=2 style='text-align: center; vertical-align: middle;'>"
	choose += "  <span style='font-size: x-large;'>&lpar;</span></td>"
	choose += " <td style='text-align: center; vertical-align: middle;'>{0}</td>".format(n)
	choose += " <td rowspan=2 style='text-align: center; vertical-align: middle;'>"
	choose += "  <span style='font-size: x-large;'>&rpar;</span></td>"
	choose += "</tr><tr>"
	choose += " <td style='text-align: center; vertical-align: middle;'>{0}</td>".format(r)
	choose += "</tr></table>"
	return choose

def makeChooseLong(n, r):
	choose = ""
	choose += "<table border=1 style='border-collapse: collapse; border: 1px solid white;'>"
	choose += "<tr>"
	choose += " <td style='text-align: center; vertical-align: middle; border-bottom: 1px solid black;'>"
	choose += "   {0}!</td>".format(n)
	choose += "</tr><tr>"
	choose += " <td style='text-align: center; vertical-align: middle; border-top: 1px solid black;'>"
	choose += "   &nbsp;({0}&ndash;{1})!&nbsp;{1}!&nbsp;</td>".format(n, r)
	choose += "</tr></table>"
	return choose


def makeFormula(n, s, t, p, q):
	###
	# n = total
	# s = # of p
	# t = # of q
	# p = prob. of s
	# q = prob. of t
	formula = "<table border=1 style='border-collapse: collapse; border: 1px solid white;'>"
	formula += "<tr>"
	formula += " <td>"
	formula += makeChoose(n, s)
	formula += "</td><td>"
	if abs(p - 0.5) < 1e-4:
		ptxt = "<span style='font-size: large;'>&half;</span>"
	elif abs(p*10.0 - int(p*10)) < 1e-4:
		ptxt = "{0:.1f}".format(p)
	else:
		ptxt = "{0:.2f}".format(p)
	formula += "&nbsp;({0})<sup>{1}</sup>&nbsp;".format(ptxt, s)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseLong(n, s)
	formula += "</td>"
	formula += "</tr></table>"
	print(formula)



if __name__ == '__main__':
	total = random.randint(5,9)
	boys = random.randint(2,total-2)
	girls = total - boys
	question = ""
	question += 'A women has {0} ({1}) children, '.format(num2txt[total], total)
	question += 'what is the probability that she has exactly '
	question += '{0} ({1}) boys and '.format(num2txt[boys], boys)
	question += '{0} ({1}) girls? '.format(num2txt[girls], girls)
	print(question)
	choices = []
	answer = makeFormula(total, boys, girls, 0.5, 0.5)

