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
	15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
	20: 'twenty',
}

#====================
if __name__ == '__main__':
	if len(sys.argv) >= 2:
		num_items = int(sys.argv[1])
	else:
		num_items = 6
	if num_items < 4:
		print("Sorry, you must have at least 4 genes for this program")
		sys.exit(1)
	if num_items > 20:
		print("Sorry, you must have less than 20 genes for this program")
		sys.exit(1)

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
	used_gene_pairs = {}
	while len(split_gene_pairs) < num_sub_sets or len(used_gene_pairs) < num_sub_sets:
		iters += 1
		#print("%d of %d gene pairs"%(len(split_gene_pairs), num_sub_sets))
		if random.random() < 0.1:
			delsize = random.randint(min_deletion_size, max_deletion_size)
		elif len(itemlist) > 4 and random.random() < 0.7:
			delsize = random.randint(min_deletion_size+2, max_deletion_size)
		else:
			delsize = random.randint(min_deletion_size+1, max_deletion_size)
		delstart = random.randint(0, len(itemlist)-delsize)
		deletion = itemlist[delstart:delstart+delsize]
		add_value = 0
		if delstart > 0:
			key = itemlist[delstart-1]+itemlist[delstart]
			#print key
			if split_gene_pairs.get(key) is None:
				split_gene_pairs[key] =True
				add_value += 1
		if delstart+delsize < len(itemlist):
			key = itemlist[delstart+delsize-1]+itemlist[delstart+delsize]
			#print key
			if split_gene_pairs.get(key) is None:
				split_gene_pairs[key] =True
				add_value += 1
		## need to make sure every pair of genes is in a least one deletion
		for j in range(len(deletion)-1):
			key = deletion[j]+deletion[j+1]
			if used_gene_pairs.get(key) is None:
				used_gene_pairs[key] =True
				add_value += 1
		deletion.sort()
		if add_value > 0 and not deletion in del_set:
			i+=1
			del_set.append(deletion)
			print("Del %d: %s"%(i, str(deletion)))
			#print(split_gene_pairs)
			#print i, len(used_genes), delsize, delstart, deletion
	print("")
	print("Total used gene pairs: %d"%(len(used_gene_pairs)))
	print("Total split gene pairs: %d"%(len(split_gene_pairs)))

	print("\n##########\n")

	### write question
	#Genes a, b, c, d, e, and f are closely linked in a chromosome, but their order is unknown.
	#Four deletions in the region are found to uncover recessive alleles of the genes as follows:
	#Deletion?1 uncovers a, d, and f; Deletion?2 uncovers d, e, and f; Deletion?3 uncovers c, d, and e;
	#Deletion?4 uncovers b and c. Which one of the following is the correct order for the genes?

	random.shuffle(del_set)

	sys.stderr.write("\n")
	sys.stderr.write(("A total of %s genes "%(num2word[len(origlist)]))
		+list2text(sortedlist)+" are closely linked in a single chromosome, but "
		+"their order is unknown. ")
	sys.stderr.write(("A total of %s deletions in the region are found "%(num2word[len(del_set)]))
		+"to uncover recessive alleles of the genes as follows: ")
	for i,deletion in enumerate(del_set):
		sys.stderr.write("Deletion #%d uncovers the %s genes %s; "%(i+1, num2word[len(deletion)], list2text(deletion)))
	sys.stderr.write("What the correct order for the %s genes? "%(num2word[len(origlist)]))
	sys.stderr.write("Hint: the first gene on the end is gene %s.\n"%(origlist[0]))

	sys.stderr.write("\n")
	sys.stderr.write("Answer: %s\n"%(list2string(origlist)))
	sys.stderr.write("\n")

	#sys.stdout.write("Which one of the following is the correct order for the genes?")

	sys.stderr.write("##########\n")

