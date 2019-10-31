#!/usr/bin/env python

import os
import sys
import copy
import math
import numpy
import random
from fractions import gcd

basetype = 'def'
if len(sys.argv) > 1:
	basetype = sys.argv[1].strip()

def tetradSetToString(tetradSet):
	mystr = ("%s\t%s\t%s\t%s\t"
		%(tetradSet[0],tetradSet[1],tetradSet[2],tetradSet[3],))
	return mystr

def invertType(genotype):
	newtype = ''
	for i in range(3):
		if genotype[i] == '+':
			newtype += basetype[i]
		else:
			newtype += '+'
	return newtype

def flipGene(genotype, gene):
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

#gene order
print "selecting gene order"
possible_orders = []
possible_orders.append(basetype)
order1 = basetype[0]+basetype[2]+basetype[1]
possible_orders.append(order1)
order2 = basetype[1]+basetype[0]+basetype[2]
possible_orders.append(order2)
print possible_orders

geneorder = random.choice(possible_orders)
print geneorder

print "determine gene distances"
a = numpy.random.poisson(lam=12, size=7)
a.sort()
distances = [a[0], a[-1]]
random.shuffle(distances)
print distances

print geneorder[0], '-', distances[0], '-', geneorder[1], '-', distances[1], '-', geneorder[2],

print "determine double crossovers"
doublecross = distances[0]*distances[1]/200.
doublecross += distances[0]*distances[0]/200.
doublecross += distances[1]*distances[1]/200.
#doublecross /= 2.0
print "doublecross %.1f per 1000"%(doublecross*10)

print "determine progeny size"
gcd1 = gcd(distances[0], 100)
gcd2 = gcd(distances[1], 100)
gcdfinal = gcd(gcd1, gcd2)
print "Final GCD", gcdfinal
progenybase = 100/gcdfinal
progs = numpy.arange(2, 41, 1, dtype=numpy.float64)*progenybase
numpy.random.shuffle(progs)
bases = progs * distances[0] * distances[1] / 1e4
devs = (bases - numpy.around(bases, 0))**2
argmin = numpy.argmin(devs)
progeny = int(progs[argmin])
print progeny

print "determine parental type"
types = ['+++', '++'+basetype[2], '+'+basetype[1]+'+', '+'+basetype[1]+basetype[2]]
parental = random.choice(types)
print parental, invertType(parental)

### START CHANGING HERE

doublecount = int(round(doublecross*progeny/100.))+2
if doublecount <= 4:
	doublecount = 5

#simulate the numbers
#probably could be faster with Poisson random numbers, but this is more fun
d00 = distances[0]*distances[0]
d01 = distances[0]*distances[1]
d11 = distances[1]*distances[1]
totalcross = float(d00 + d11 + d01)
r00 = d00/totalcross
r11 = d11/totalcross
dcount1 = 0
dcount2 = 0
dcount3 = 0
for i in range(doublecount):
	r = random.random()
	if r < r00:
		dcount1 += 1
	elif r < r00 + r11:
		dcount2 += 1
	else:
		dcount3 += 1
"""
dcount = doublecount
avgrand = (random.random() + random.random() + random.random())/3.
dcount1 = int(round(dcount * avgrand/1.5))
dcount -= dcount1
avgrand = (random.random() + random.random() + random.random())/3.
dcount2 = int(round(dcount * avgrand))
dcount3 = dcount - dcount2
"""
print dcount1, dcount2, dcount3

firstcount = 2*(int(round(distances[0]*progeny/100.)) - 3*(dcount1 + dcount3))
secondcount = 2*(int(round(distances[1]*progeny/100.)) - 3*(dcount2 + dcount3))
if firstcount <= 0 or secondcount <= 0:
	print "two many double cross-overs"
	sys.exit(1)
parentcount = progeny - doublecount - firstcount - secondcount

# Create Six Genotypes
sixTetradSets = []
tetradCount = {}

tetradSet = [parental, parental, invertType(parental), invertType(parental),]
tetradSet.sort()
tetradName = tetradSetToString(tetradSet)
sixTetradSets.append(tetradName)
tetradCount[tetradName] = parentcount

#first flip
firsttype = flipGene(parental, geneorder[0])

#usually TT
tetradSet = [firsttype, invertType(firsttype), parental, invertType(parental),]
tetradSet.sort()
tetradName = tetradSetToString(tetradSet)
sixTetradSets.append(tetradName)
tetradCount[tetradName] = firstcount

#usually NPD
tetradSet = [firsttype, invertType(firsttype), firsttype, invertType(firsttype), ]
tetradSet.sort()
tetradName = tetradSetToString(tetradSet)
sixTetradSets.append(tetradName)
tetradCount[tetradName] = dcount1

#second flip
secondtype = flipGene(parental, geneorder[2])

#usually TT
tetradSet = [secondtype, invertType(secondtype), parental, invertType(parental),]
tetradSet.sort()
tetradName = tetradSetToString(tetradSet)
sixTetradSets.append(tetradName)
tetradCount[tetradName] = secondcount

#usually NPD
tetradSet = [secondtype, invertType(secondtype), secondtype, invertType(secondtype),]
tetradSet.sort()
tetradName = tetradSetToString(tetradSet)
sixTetradSets.append(tetradName)
tetradCount[tetradName] = dcount2

#both flips
thirdtype = flipGene(flipGene(parental, geneorder[2]), geneorder[0])

#usually NPD
tetradSet = [thirdtype, invertType(thirdtype), thirdtype, invertType(thirdtype),]
tetradSet.sort()
tetradName = tetradSetToString(tetradSet)
sixTetradSets.append(tetradName)
tetradCount[tetradName] = dcount3

sixTetradSets.sort()
print "------------------------------------------"
for i,tetradName in enumerate(sixTetradSets):
	print "%d\t%s%d"%(i+1,tetradName, tetradCount[tetradName])
print "\t\t\t\tTOTAL\t%d"%(progeny)
