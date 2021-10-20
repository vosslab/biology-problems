#!/usr/bin/env python

import os
import math
import random

def choose(n, r):
	f = math.factorial
	nint = int(n)
	rint = int(r)
	c =  f(nint) // (f(rint) * f(nint - rint))
	return c

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
	numerator = "{0}!".format(n)
	denominator = "({0}&ndash;{1})!&nbsp;&sdot;&nbsp;{1}!".format(n, r)
	fraction = makeFraction(numerator, denominator)
	return fraction

def makeFraction(numerator, denominator):
	fraction = ""
	fraction += "<table border=1 style='border-collapse: collapse; border: 1px solid white;'>"
	fraction += "<tr>"
	fraction += " <td style='text-align: center; vertical-align: middle; border-bottom: 1px solid black;'>"
	fraction += "&nbsp;"+numerator+"&nbsp;"
	fraction += " </td>"
	fraction += "</tr><tr>"
	fraction += " <td style='text-align: center; vertical-align: middle; border-top: 1px solid black;'>"
	fraction += "&nbsp;"+denominator+"&nbsp;"
	fraction += " </td>"
	fraction += "</tr></table>"
	return fraction

def decimal_to_fraction_parts(p):
	if abs(p - 1/3.) < 1e-4:
		a = 1
		b = 3
	elif abs(p - 2/3.) < 1e-4:
		a = 2
		b = 3
	else:
		a, b = (p).as_integer_ratio()
	return a, b

def combinePowerFractions(p, s, q, t):
	a, b = decimal_to_fraction_parts(p)
	c, d = decimal_to_fraction_parts(q)
	numerator = ""
	if a > 1:
		numerator += "{0}<sup>{1}</sup>".format(a, s)
	if c > 1:
		numerator += "{0}<sup>{1}</sup>".format(c, t)
	if a == 1 and c == 1:
		numerator += "1"
	denominator = ""
	if b > 1:
		denominator += "{0}<sup>{1}</sup>".format(b, s)
	if d > 1:
		denominator += "{0}<sup>{1}</sup>".format(d, t)
	if b == 1 and d == 1:
		denominator += "1"

	fraction = makeFraction(numerator, denominator)
	return fraction

def makeChooseCancelled(n, r):
	numerator = ""
	if n == r:
		numerator += "{0}".format(1)
	elif n == r+1:
		numerator += "{0}".format(n)
	else:
		for i in range(n, r+1, -1):
			numerator += "{0}".format(i)
			numerator += "&sdot;"
		numerator += "{0}".format(r+1)

	denominator = ""
	if n == r:
		denominator += "{0}".format(1)
	elif n == r+1:
		denominator += "{0}".format(1)
	else:
		for i in range(r, 2, -1):
			denominator += "{0}".format(i)
			denominator += "&sdot;"
		denominator += "{0}".format(2)

	fraction = makeFraction(numerator, denominator)
	#fraction += "{0}&ndash;{1}".format(n, r)
	return fraction

def percent_to_fraction(p):
	if abs(p - 0.5) < 1e-4:
		ptxt = "<span style='font-size: large;'>&frac12;</span>"
	elif abs(p - 0.25) < 1e-4:
		ptxt = "<span style='font-size: large;'>&frac14;</span>"
	elif abs(p - 0.75) < 1e-4:
		ptxt = "<span style='font-size: large;'>&frac34;</span>"
	elif abs(p - 1/3.) < 1e-4:
		ptxt = "<span style='font-size: large;'>&#8531;</span>"
	elif abs(p - 2/3.) < 1e-4:
		ptxt = "<span style='font-size: large;'>&#8532;</span>"
	elif abs(p*10.0 - int(p*10)) < 1e-4:
		ptxt = "{0:.1f}".format(p)
	else:
		ptxt = "{0:.2f}".format(p)
	return ptxt

def makeFormula(n, s, t, p, q):
	###
	# n = total
	# s = # of p
	# t = # of q
	# p = prob. of s
	# q = prob. of t
	final_value = choose(n, s) * p**s * q**t
	formula = "<table border=1 style='border-collapse: collapse; border: 1px solid white;'>"
	formula += "<tr>"
	formula += " <td>"
	formula += makeChoose(n, s)
	formula += "</td><td>"
	ptxt = percent_to_fraction(p)
	formula += "({0})<sup>{1}</sup>".format(ptxt, s)
	qtxt = percent_to_fraction(q)
	formula += "&sdot;({0})<sup>{1}</sup>".format(qtxt, t)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseLong(n, s)
	formula += "</td><td>"
	if abs(p - q) < 1e-4:
		formula += "({0})<sup>{1}</sup>".format(ptxt, n)
	else:
		formula += "({0})<sup>{1}</sup>".format(ptxt, s)
		formula += "&sdot;({0})<sup>{1}</sup>".format(qtxt, t)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseCancelled(n, s)
	formula += "</td><td>"
	formula += "&times;"
	formula += "</td><td>"
	if abs(p - q) < 1e-4:
		formula += combinePowerFractions(p, n, 1, 1)
	else:
		formula += combinePowerFractions(p, s, q, t)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	c = choose(n, s)
	#formula += "{0:d}".format(c)
	#formula += "</td><td>"
	a, b = decimal_to_fraction_parts(p**s * q**t)
	if 1 < a < 1000:
		formula += makeFraction(str(c)+"&times;"+str(a), str(b))
	elif a == 1:
		formula += makeFraction(str(c), str(b))
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += "{0:.4f}".format(final_value)
	formula += "</td><td>"
	formula += "<strong>&nbsp;=&nbsp;</strong>"
	formula += "</td><td>"
	formula += "<strong>{0:.1f}%</strong>".format(final_value*100)
	formula += "</td>"
	formula += "</tr></table>"
	#print(formula)
	return formula


def writeQuestion(girls, boys):
	total = girls + boys
	question = ""
	question += 'A women has {0} ({1}) children, '.format(num2txt[total], total)
	question += 'what is the probability that she has exactly '
	question += '{0} ({1}) boys and '.format(num2txt[boys], boys)
	question += '{0} ({1}) girls? '.format(num2txt[girls], girls)
	print(question)
	choices = []
	answer = makeFormula(total, boys, girls, 0.5, 0.5)
	choices.append(answer)
	#print(answer)
	wrong1 = makeFormula(total, boys, girls, 0.75, 0.25)
	#print(wrong1)
	choices.append(wrong1)

	wrong2 = makeFormula(total, boys, girls, 0.25, 0.75)
	#print(wrong2)
	choices.append(wrong2)

	if boys > girls:
		wrong3 = makeFormula(boys, girls, boys, 0.5, 0.5)
		wrong4 = makeFormula(boys, boys, girls, 0.5, 0.5)
	else:
		wrong3 = makeFormula(girls, boys, girls, 0.5, 0.5)
		wrong4 = makeFormula(girls, girls, boys, 0.5, 0.5)
	#print(wrong3)
	choices.append(wrong3)
	#print(wrong4)
	choices.append(wrong4)
	random.shuffle(choices)

	complete_text = ""

	complete_text += "MC\t{0}".format(question)
	for choice in choices:
		if choice == answer:
			status = "Correct"
		else:
			status = "Incorrect"
		complete_text += "\t{0}\t{1}".format(choice, status)
	return complete_text

if __name__ == '__main__':
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')	

	"""
	total = random.randint(5,9)
	boys = girls = 0
	while boys == girls:
		boys = random.randint(2,total-2)
		girls = total - boys
	"""

	count = 0
	for total in range(5, 10):
		for boys in range(2, total-1):
			girls = total - boys
			if boys == girls:
				continue
			count += 1
			complete_text = writeQuestion(girls, boys)
			if total == 9 and boys == 5:
				print(complete_text)
			f.write("{0}\n".format(complete_text))
	print("Wrote {0} quesitons".format(count))
	f.close()







