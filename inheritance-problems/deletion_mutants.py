#!/usr/bin/env python3

import os
import sys
import copy
import random
import argparse

num2word = {
	1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
	6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
	11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
	15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
	20: 'twenty',
}

#====================
def makeHtmlTable(origlist, del_set):
	table = ''
	table += '<table style="border-collapse: collapse; border: 2px solid black; '
	width = 60*(len(origlist) + 1)
	height = 25*(len(del_set) + 1)
	table += 'width: {0:d}px; height: {1:d}px;">'.format(width, height)
	table += '<tr><th> </th>'
	for i in range(len(origlist)):
		table += '<th align="center">Gene {0}</th>'.format(i+1)
	table += '</tr>'
	colors = ['DarkRed', 'DarkSlateGray', 'DarkGreen', 'Indigo', 'MidnightBlue', 'DarkOliveGreen', ]
	for i,deletion in enumerate(del_set):
		table += '<tr><th align="center">Del #{0}</th>'.format(i+1)
		for gene in origlist:
			if gene in deletion:
				#black fill
				table += '<td bgcolor="{0}"> </td>'.format(colors[i % len(colors)])
			else:
				table += '<td bgcolor="#EEEEEE"> </td>'
		table += '</tr>'
	table += '</table>'
	return table

#====================
def writeQuestion(origlist, del_set):
	### write question
	#Genes a, b, c, d, e, and f are closely linked in a chromosome, but their order is unknown.
	#Four deletions in the region are found to uncover recessive alleles of the genes as follows:
	#Deletion?1 uncovers a, d, and f; Deletion?2 uncovers d, e, and f; Deletion?3 uncovers c, d, and e;
	#Deletion?4 uncovers b and c. Which one of the following is the correct order for the genes?

	sortedlist = copy.copy(origlist)
	sortedlist.sort()

	question = ''

	sys.stderr.write("\n")
	question += (("<p>A total of %s genes "%(num2word[len(origlist)]))
		+list2text(sortedlist)+" are closely linked in a single chromosome, but "
		+"their order is unknown. ")
	question += (("A total of %s deletions in the region are found "%(num2word[len(del_set)]))
		+"to uncover recessive alleles of the genes as follows:</p><ul>  ")
	for i,deletion in enumerate(del_set):
		question += ("<li>Deletion #%d uncovers the %s genes %s;</li>  "%(i+1, num2word[len(deletion)], list2text(deletion)))
	question += ("</ul> <h5>What the correct order for the %s genes?</h5> "%(num2word[len(origlist)]))
	question += ("<p>Hint 1: the first gene on the end is gene %s.</p> "%(origlist[0]))
	question += ("<p>Hint 2: enter your answer in the blank using only {0} letters or one comma every 3 letters.</p> ".format(num2word[len(origlist)]))

	#sys.stderr.write(question)

	sys.stderr.write("\n")
	sys.stderr.write("Answer: %s\n"%(list2string(origlist)))
	sys.stderr.write("\n")

	#sys.stdout.write("Which one of the following is the correct order for the genes?")

	sys.stderr.write("##########\n")
	return question

#====================
def list2string(mylist):
	mystring = ""
	for letter in mylist:
		mystring += letter
	return mystring

#====================
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

#====================
def makeDeletions(num_genes):
	charlist = list("ABCDEFGHJKMPQRSTWXYZ")
	itemlist = charlist[:num_genes]
	random.shuffle(itemlist)

	# complicated step to get version of list that is most alphabetical
	if itemlist[0] > itemlist[-1]:
		itemlist.reverse()
	origlist = copy.copy(itemlist)
	print("itemlist", itemlist)

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
			print(("Del %d: %s"%(i, str(deletion))))
			#print(split_gene_pairs)
			#print i, len(used_genes), delsize, delstart, deletion
	print("")
	print(("Total used gene pairs: %d"%(len(used_gene_pairs))))
	print(("Total split gene pairs: %d"%(len(split_gene_pairs))))

	print("\n##########\n")
	return origlist, del_set

#==========================
def insertCommas(my_str, separate=3):
	new_str = ''
	for i in range(0, len(my_str), separate):
		new_str += my_str[i:i+separate] + ','
	return new_str[:-1]

#====================
def makeBlackboard(question, table, origlist):
	blackboard = ''
	blackboard += 'FIB\t'
	blackboard += table
	blackboard += question
	blackboard += '\t'
	answer = ''.join(origlist)
	blackboard += answer
	blackboard += '\t'
	blackboard += answer[::-1]
	blackboard += '\t'
	blackboard += insertCommas(answer)
	blackboard += '\t'
	blackboard += insertCommas(answer[::-1])
	blackboard += '\n'
	return blackboard

#====================
#====================
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num-genes', type=int, dest='num_genes',
		help='number of deleted genes on the chromosome', default=5)
	parser.add_argument('-q', '--num-questions', type=int, dest='num_questions',
		help='number of questions to create', default=24)
	parser.add_argument('-T', '--table', dest='table', action='store_true')
	parser.add_argument('-F', '--free', '--no-table', dest='table', action='store_false')
	parser.set_defaults(table=True)
	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of choices to choose from in the question', default=5)
	args = parser.parse_args()

	no_table = not args.table

	if args.num_genes < 4:
		print("Sorry, you must have at least 4 genes for this program")
		sys.exit(1)
	if args.num_genes > 20:
		print("Sorry, you must have less than 20 genes for this program")
		sys.exit(1)

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(args.num_questions):
		origlist, del_set = makeDeletions(args.num_genes)
		random.shuffle(del_set)
		if args.table is True:
			print("Making TABLE")
			table = makeHtmlTable(origlist, del_set)
		else:
			table = ''
		question = writeQuestion(origlist, del_set)
		print(question)
		answer = ''.join(origlist)
		print(answer)
		blackboard = makeBlackboard(question, table, origlist)
		f.write(blackboard)
	f.close()
