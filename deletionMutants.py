#!/usr/bin/env python

import re
import sys
import math
import copy
import random
import pprint

def list2string(mylist):
	mystring = ""
	for letter in mylist:
		mystring += letter
	return mystring

def list2text(mylist):
	mystring = ""
	if len(mylist) > 2:
		sublist = mylist[:-1]
		for letter in sublist:
			mystring += letter+", "
		mystring += "and "+mylist[-1]
	elif len(mylist) == 2:
		mystring = mylist[0]+" and "+mylist[1]
	return mystring

num2word = {
	1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 
	6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 
	11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 
	15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'
}


#====================
if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_items = int(sys.argv[1])
	else:
		num_items = 4

	charlist = list("ABCDEFGHJKMPQRSTWXYZ")

	itemlist = charlist[:num_items]
	random.shuffle(itemlist)

	# complicated step to get version of list that is most alphabetical
	if itemlist[0] > itemlist[-1]:
		itemlist.reverse()
	origlist = copy.copy(itemlist)
	sortedlist = copy.copy(itemlist)
	sortedlist.sort()
	print itemlist

	num_deletions = 5
	min_deletion_size = 2
	max_deletion_size = min(len(itemlist) - 1,5)

	N = len(itemlist)
	# N permutations 2, P(N, 2) minus three
	num_sub_sets = N - 1
	#print("Expect %d del pairs"%(num_sub_sets))

	i = 0
	iters = 0
	del_set = []
	split_gene_pairs = {}
	used_end_genes = {}
	while len(split_gene_pairs) < num_sub_sets or len(used_end_genes) < 2:
		iters += 1
		#print("%d of %d gene pairs"%(len(split_gene_pairs), num_sub_sets))
		delsize = random.randint(min_deletion_size, max_deletion_size)
		delstart = random.randint(0, len(itemlist)-delsize)
		deletion = itemlist[delstart:delstart+delsize]
		new_split = 0
		if delstart > 0:
			key = itemlist[delstart-1]+itemlist[delstart]
			#print key
			if split_gene_pairs.get(key) is None:
				split_gene_pairs[key] =True
				new_split += 1
		if delstart+delsize < len(itemlist):
			key = itemlist[delstart+delsize-1]+itemlist[delstart+delsize]
			#print key
			if split_gene_pairs.get(key) is None:
				split_gene_pairs[key] =True
				new_split += 1
		## need to make sure we include both of the end genes in at least one deletion
		if deletion[0] == itemlist[0]:
			gene = deletion[0]
			if used_end_genes.get(gene) is None:
				used_end_genes[gene] = True
				new_split += 1
		if deletion[-1] == itemlist[-1]:
			gene = deletion[-1]
			if used_end_genes.get(gene) is None:
				used_end_genes[gene] = True
				new_split += 1
		deletion.sort()
		if new_split > 0 and not deletion in del_set:
			i+=1
			del_set.append(deletion)
			print("Del %d: %s"%(i, str(deletion)))
			#print(split_gene_pairs)
			#print i, len(used_genes), delsize, delstart, deletion

	print("\n##########\n")

	### write question
	#Genes a, b, c, d, e, and f are closely linked in a chromosome, but their order is unknown.
	#Four deletions in the region are found to uncover recessive alleles of the genes as follows:
	#Deletion?1 uncovers a, d, and f; Deletion?2 uncovers d, e, and f; Deletion?3 uncovers c, d, and e;
	#Deletion?4 uncovers b and c. Which one of the following is the correct order for the genes?

	random.shuffle(del_set)

	sys.stdout.write(("A total of %s genes "%(num2word[len(origlist)]))
		+list2text(sortedlist)+" are closely linked in a single chromosome, but "
		+"their order is unknown. ")
	sys.stdout.write(("A total of %s deletions in the region are found "%(num2word[len(del_set)]))
		+"to uncover recessive alleles of the genes as follows: ")
	for i,deletion in enumerate(del_set):
		sys.stdout.write("Deletion #%d uncovers the %s genes %s; "%(i+1, num2word[len(deletion)], list2text(deletion)))
	sys.stdout.write("What the correct order for the %s genes? "%(num2word[len(origlist)]))
	sys.stdout.write("Hint: the first gene on the end is gene %s."%(origlist[0]))

	#sys.stdout.write("Which one of the following is the correct order for the genes?")
	
	
	print("\n\n##########\n")

