#!/usr/bin/env python

import sys
import string
import random

uppercase = "ABCDEFGHJKMPQRSTVWXYZ"
lowercase = "abcdefghjkmpqrstvwxyz"


def deconstructPowerOfNumber(num):
	temp_num = num
	power2 = 0
	power3 = 0
	while temp_num % 2 == 0:
		temp_num //= 2
		power2 += 1
	while temp_num % 3 == 0:
		temp_num //= 3
		power3 += 1
	#print(num, power2, power3)
	return power2, power3

def formatChoice(power2, power3):
	num = 2**power2 * 3**power3

	pow2str = ""
	if power2 == 0:
		pow2str = None
	if power2 == 1:
		pow2str = "2"
	if power2 > 1:
		pow2str = "2<sup>{0}</sup>".format(power2)		
	
	pow3str = ""
	if power3 == 0:
		pow3str = None
	if power3 == 1:
		pow3str = "3"
	if power3 > 1:
		pow3str = "3<sup>{0}</sup>".format(power3)
	
	if pow2str is None:
		mystr = pow3str + " &nbsp; = {0}".format(num)
	elif pow3str is None:
		mystr = pow2str + " &nbsp; = {0}".format(num)
	else:
		mystr = "{0} &times; {1} &nbsp; = {2}".format(pow2str, pow3str, num)
	return mystr

def crossGenotypes(geno1, geno2):
	cross = []
	for g1 in geno1:
		for g2 in geno2:
			g = [g1,g2]
			g.sort()
			gstr = g[0]+g[1]
			cross.append(gstr)
	cross.sort()
	result = list(set(cross))
	#print(result)
	return result

def countGenotypesForCross(gene_list1, gene_list2):
	if len(gene_list1) != len(gene_list2):
		print("different sizes of lists")
		sys.exit(1)
	total_genotypes = 1
	for i in range(len(gene_list1)):
		geno1 = gene_list1[i]
		geno2 = gene_list2[i]
		cross = crossGenotypes(geno1, geno2)
		total_genotypes *= len(cross)
	return total_genotypes


def crossPhenotypes(geno1, geno2):
	cross = []
	#print(geno1, geno2)
	for g1 in geno1:
		for g2 in geno2:
			g = [g1,g2]
			g.sort()
			gstr = g[0] #+g[1]
			#print(g[0], g[1], gstr)
			cross.append(gstr)
	cross.sort()
	result = list(set(cross))
	#print(result)
	return result

def countPhenotypesForCross(gene_list1, gene_list2):
	if len(gene_list1) != len(gene_list2):
		print("different sizes of lists")
		sys.exit(1)
	total_genotypes = 1
	for i in range(len(gene_list1)):
		geno1 = gene_list1[i]
		geno2 = gene_list2[i]
		cross = crossPhenotypes(geno1, geno2)
		total_genotypes *= len(cross)
	return total_genotypes


def createGenotypeList(num_genes):
	gene_list = []
	for i in range(num_genes):
		val = random.random()
		if val < 0.25:
			gene_list.append((uppercase[i], uppercase[i]))
		elif val < 0.75:
			gene_list.append((uppercase[i], lowercase[i]))
		else:
			gene_list.append((lowercase[i], lowercase[i]))
	return gene_list

def createGenotypeStringFromList(gene_list):
	genestr = ""
	gamete_count = 1
	for gene_pair in gene_list:
		if gene_pair[0] != gene_pair[1]:
			gamete_count *= 2
		genestr += gene_pair[0] + gene_pair[1] + " "
	return genestr, gamete_count

def createGenotype(num_genes):
	gene_list = createGenotypeList(num_genes)
	genestr, gamete_count = createGenotypeStringFromList(gene_list)
	return genestr, gamete_count

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_genes = int(sys.argv[1])
	else:
		num_genes = 3

	genestr, gamete_count = createGenotype(num_genes)
	print(gamete_count)
	print(genestr)
	print(genestr.replace(' ', '\t'))

