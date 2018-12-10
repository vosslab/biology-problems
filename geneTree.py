#!/usr/bin/env python

import re
import sys
import copy
import random
import pprint
#from skbio.tree import nj

### TODO
# 1. more alphabetical order of genes in tree
# 2. add deviations to distance matrix to require averaging
# 3. better tree construction, works with #1

#====================
def item2letters(item):
	letters = []
	for letter in list(item):
		if re.match("^[A-Z]$", letter):
			letters.append(letter)
	return letters

#====================
def addDistances(item1, item2, distmatrix):
	letters1 = item2letters(item1)
	letters2 = item2letters(item2)
	for l1 in letters1:
		for l2 in letters2:
			key1 = l1+"-"+l2
			key2 = l2+"-"+l1
			distmatrix[key1] = dist
			distmatrix[key2] = dist
	return

#====================
def printTree(origlist, distmatrix):
	prevDist = None
	prevLetter = None
	for i,letter in enumerate(origlist):
		sys.stderr.write(letter+" ")
		if i < len(origlist)-1:
			nextLetter = origlist[i+1]
			key = letter+"-"+nextLetter
			dist = distmatrix[key]*2
		else:
			dist = 10000

		if prevDist is None or dist < prevDist:
			for j in range(dist):
				sys.stderr.write("_")
			sys.stderr.write("\n  ")
			for j in range(dist):
				sys.stderr.write(" ")
			sys.stderr.write("|")
			if prevDist is not None:
				for j in range(prevDist-dist-1):
					sys.stderr.write("_")
			sys.stderr.write("\n")
		else:
			for j in range(prevDist):
				sys.stderr.write("_")
			sys.stderr.write("|")
			if dist < 100:
				for j in range(dist-prevDist-1):
					sys.stderr.write("_")
			sys.stderr.write("\n  ")
			for j in range(prevDist):
				sys.stderr.write(" ")
			sys.stderr.write("\n")
		prevDist = dist
		prevLetter = letter
	return

#====================
def printTree2(origlist, distmatrix):
	for i,l1 in enumerate(origlist):
		sys.stderr.write(l1+" ")
		if i > 0:
			l2 = origlist[i-1]
			key = l1+"-"+l2
			d1 = distmatrix[key]
		else:
			d1 = 100

		if i < len(origlist)-1:
			l2 = origlist[i+1]
			key = l1+"-"+l2
			d2 = distmatrix[key]
		else:
			d2 = 100

		d = min(d1, d2)*2
		for j in range(d):
			sys.stderr.write("_")

		if d2 > d1:
			sys.stderr.write("|")
		else:
			sys.stderr.write(" ")
		sys.stderr.write("\n  ")
		if i < len(origlist)-1:
			for j in range(d2*2):
				sys.stderr.write(" ")
			sys.stderr.write("|_")
		sys.stderr.write("\n")

#====================
def printMatrix(origlist, distmatrix):
	letters = copy.copy(origlist)
	letters.sort()
	for l in letters:
		sys.stderr.write("\t%s"%(l))
	sys.stderr.write("\n")
	for l1 in letters:
		sys.stderr.write(l1)
		for l2 in letters:
			key = l1+"-"+l2
			d = distmatrix[key]*2
			sys.stderr.write("\t%d"%(d))
		sys.stderr.write("\n")
	sys.stderr.write("\n")

def addItemsToBetterList(item1, item2, betterlist):
	if item1< item2:
		if len(item1) == 1:
			betterlist.append(item1)
		if len(item2) == 1:
			betterlist.append(item2)
	else:
		if len(item2) == 1:
			betterlist.append(item2)
		if len(item1) == 1:
			betterlist.append(item1)
	return

#====================
if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_items = int(sys.argv[1])
	else:
		num_items = 4

	charlist = list("ABCDEFGHJKMPQRSTWXYZ")

	itemlist = charlist[:num_items]
	random.shuffle(itemlist)
	if itemlist[0] > itemlist[-1]:
		itemlist.reverse()
	origlist = copy.copy(itemlist)
	print itemlist
	dist = 2
	distmatrix = {}
	for letter in itemlist:
		key = letter+"-"+letter
		distmatrix[key] = 0

	betterlist = []
	while len(itemlist) > 1:
		merge = random.randint(1,len(itemlist)-1)
		addDistances(itemlist[merge-1], itemlist[merge], distmatrix)
		addItemsToBetterList(itemlist[merge-1], itemlist[merge], betterlist)
		itemlist[merge-1] = "("+itemlist[merge-1]+str(dist)+itemlist[merge]+")"
		itemlist.pop(merge)
		dist += random.randint(1,3)
		print itemlist
	print("\n")
	pprint.pprint(origlist)
	pprint.pprint(betterlist)

	print("\n")
	printMatrix(origlist, distmatrix)

	#print("\n")
	#printTree(betterlist, distmatrix)

	print("\n")
	printTree2(betterlist, distmatrix)
