

import os
import re
import sys
import copy
import math
import numpy
import string
import random
import crcmod.predefined

#====================================
def invertGenotype(genotype, basetype):
	newtype = ''
	for i in range(len(basetype)):
		if genotype[i] == '+':
			newtype += basetype[i]
		else:
			newtype += '+'
	return newtype

#====================================
def flipGeneByLetter(genotype, gene, basetype):
	newlist = list(genotype)
	for i in range(len(basetype)):
		if basetype[i] == gene:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'
	newtype = ""
	for i in newlist:
		newtype += i
	return newtype

#====================================
def flipGeneByIndex(genotype, gene_index, basetype):
	newlist = list(genotype)
	for i in range(len(basetype)):
		if basetype[i] == gene:
			if genotype[i] == '+':
				newlist[i] = basetype[i]
			else:
				newlist[i] = '+'
	newtype = ""
	for i in newlist:
		newtype += i
	return newtype
