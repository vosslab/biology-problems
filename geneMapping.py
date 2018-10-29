#!/usr/bin/env python

import os
import copy
import numpy
import random
from fractions import gcd

def invertType(genotype):
	basetype = 'abc'
	newtype = ''
	for i in range(3):
		if genotype[i] == '+':
			newtype += basetype[i]
		else:
			newtype += '+'
	return newtype

def flipGene(genotype, gene):
	basetype = 'abc'
	newlist = list(genotype)
	for i in range(3):
		if basetype[i] == gene:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'
	newtype = ""
	for i in newlist:
		newtype += i
	return newtype

afile = "gene_order_answers.txt"
qfile = "gene_order_questions.txt"
if not os.path.exists(afile):
	open(afile, 'a').close()
f = open(afile, "r")
qcount = len(f.readlines()) + 1
f.close()

#gene order
print "selecting gene order"
geneorder = random.choice(['abc', 'acb', 'bac'])
print geneorder

print "determine gene distances"
a = numpy.random.poisson(lam=12, size=7)
a.sort()
distances = [a[0], a[-1]]
random.shuffle(distances)
print distances

print "------------"
answerString = ("%d. %s - %d - %s - %d - %s"
	%(qcount, geneorder[0],distances[0],geneorder[1],distances[1],geneorder[2]))
print answerString
print "------------"

print "determine double crossovers"
doublecross = distances[0]*distances[1]/100.
print "doublecross", doublecross*10, 'per 1000'

print "determine progeny size"
gcd1 = gcd(distances[0], 100)
gcd2 = gcd(distances[1], 100)
gcdfinal = gcd(gcd1, gcd2)
print "Final GCD", gcdfinal
progenybase = 100/gcdfinal
progs = numpy.arange(1, 41, 1, dtype=numpy.float64)*progenybase
numpy.random.shuffle(progs)
bases = progs * distances[0] * distances[1] / 1e4
devs = (bases - numpy.around(bases, 0))**2
argmin = numpy.argmin(devs)
progeny = int(progs[argmin])
print progeny

print "determine parental type"
types = ['+++', '++c', '+b+', '+bc']
parental = random.choice(types)
print parental, invertType(parental)

typemap1 = {}
print "determine double type"
doubletype = flipGene(parental, geneorder[1])
doublecount = int(round(doublecross*progeny/100.))
print doubletype, invertType(doubletype), doublecount
typemap1[doubletype] = doublecount

print "determine first flip"
firsttype = flipGene(parental, geneorder[0])
firstcount = int(round(distances[0]*progeny/100.)) - doublecount
print firsttype, invertType(firsttype), firstcount
typemap1[firsttype] = firstcount

print "determine second flip"
secondtype = flipGene(parental, geneorder[2])
secondcount = int(round(distances[1]*progeny/100.)) - doublecount
print secondtype, invertType(secondtype), secondcount
typemap1[secondtype] = secondcount

print "determine parental type count"
parentcount = progeny - doublecount - firstcount - secondcount
print parental, invertType(parental), parentcount
typemap1[parental] = parentcount

print "\n\ngenerate table"
typemap = {}
for t in types:
	n = invertType(t)
	rand = random.gauss(0.5, 0.07)
	try:
		count = typemap1[t]
	except KeyError:
		count = typemap1[n]
	typemap[t] = int(rand * count)
	typemap[n] = count - typemap[t]
alltypes = typemap.keys()
alltypes.sort()

questionString = "\nQuestion %d:\n"%(qcount)
for t in alltypes:
	questionString += ("%s %d\n"%(t, typemap[t]))
questionString +=  "--- ---\n"
questionString +=  "TOT %d\n\n"%(progeny)
print questionString


f = open(afile, "a")
f.write(answerString+"\n")
f.close()
f = open(qfile, "a")
f.write(questionString)
f.close()

