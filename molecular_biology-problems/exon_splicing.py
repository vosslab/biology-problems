#!/usr/bin/env python

import os
import sys
import copy
import random
import argparse
import subprocess

import bptools

capcolor = 'lightgray'

#==========================
#==========================
def getGenePartSizes(num_exons):
	total_gene_parts = num_exons * 2 + 1
	#5' UTR - exon 1 - intron 1 - exon 2 - ... - intron N-1 - exon N - 3' UTR
	part_sizes_set = set()
	min_part_size = 7
	max_part_size = 21
	if (1 + max_part_size - min_part_size) <= total_gene_parts:
		print("Part size range is too small!!")
		sys.exit(1)
	while len(part_sizes_set) < total_gene_parts:
		part_size = random.randint(min_part_size, max_part_size) * 10
		part_sizes_set.add(part_size)
	part_sizes_list = list(part_sizes_set)
	random.shuffle(part_sizes_list)
	return part_sizes_list

#==========================
#==========================
def make_color_wheel_from_part_sizes(part_sizes): # Assumption: r, g, b in [0, 255]
	deg_step = int(round(360./len(part_sizes) - 4))
	color_amount = random.randint(80,128)
	color_wheel = bptools.make_color_wheel(color_amount, 0, 0, deg_step)
	return color_wheel

#==========================
#==========================
def makeHtmlTable(pre_mRNA_tree):
	if not isinstance(pre_mRNA_tree, list):
		print(pre_mRNA_tree)
		print("Got wrong type in makeHtmlTable()")
		sys.exit(1)

	table = ''
	table += '<table style="border-collapse: collapse; border: 2px solid black; table-layout: fixed;">'
	for mRNA_part in pre_mRNA_tree:
		table += '<colgroup width="{0}"></colgroup>'.format(mRNA_part['size'])
	table += '<tr>'
	part_type_tuple = ('exon', 'intron')
	for mRNA_part in pre_mRNA_tree:
		html_name = mRNA_part['name'].replace(' ', '&nbsp;')
		table += '<td bgcolor="{0}" align="center">{1}<br/><font size=-2>{2} bp</font></td>'.format(
			mRNA_part['color'], mRNA_part['name'], mRNA_part['size'])
	table += '</tr>'
	table += '</table>'
	#print(table)
	return table

#==================================
def convert_int_to_binary_list(integer, size=6):
	binary_list = [int(x) for x in list('{0:0b}'.format(integer))]
	binary_list.reverse()
	while(len(binary_list) < size):
		binary_list = binary_list + [0,]
	#print(integer, '->', binary_list)
	return binary_list

#==========================
#==========================
def makeAllValid_mRNA(pre_mRNA_tree, num_exons, min_exons=3):
	mRNA_list = []
	for i in range(1, 2**num_exons):
		mRNA_tree = []
		p5_cap = { 'name': '5&prime; cap', 'color': capcolor, 'size': 80, }
		mRNA_tree.append(p5_cap)
		binary_list = convert_int_to_binary_list(i, num_exons)
		if sum(binary_list) < min_exons:
			continue
		for j, b in enumerate(binary_list):
			exon_num = j+1
			exon_index = 2*exon_num-1
			if b == 1:
				mRNA_tree.append(pre_mRNA_tree[exon_index])
				#print(pre_mRNA_tree[exon_index]['name'])
		polyA = { 'name': 'polyA tail', 'color': capcolor, 'size': 120, }
		mRNA_tree.append(polyA)
		mRNA_list.append(mRNA_tree)
	#for mRNA_tree in mRNA_list:
	#	print(mRNA_tree)
	#sys.exit(1)
	return mRNA_list

#==========================
#==========================
def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

def makeINValid_mRNA(pre_mRNA_tree, num_exons, exons_to_use):
	mRNA_tree = []
	p5_cap = { 'name': '5&prime; cap', 'color': capcolor, 'size': 80, }
	mRNA_tree.append(p5_cap)

	exon_list = list(range(1, num_exons+1))
	random.shuffle(exon_list)
	while len(exon_list) > exons_to_use:
		exon_list.pop()
	random.shuffle(exon_list)
	bing = copy.copy(exon_list)
	bing.sort()
	while bing == exon_list:
		#print("list is sorted")
		#print("exon_list", exon_list)
		random.shuffle(exon_list)

	#print("exon_list", exon_list)
	for exon_num in exon_list:
		exon_index = 2*exon_num - 1
		mRNA_tree.append(pre_mRNA_tree[exon_index])
		#print(pre_mRNA_tree[exon_index]['name'])
	polyA = { 'name': 'polyA tail', 'color': capcolor, 'size': 120, }
	mRNA_tree.append(polyA)
	#print(mRNA_tree)
	return mRNA_tree

#==========================
#==========================
def makePre_mRNA_tree(part_sizes):
	pre_mRNA_tree = []
	part_type_tuple = ('exon', 'intron')
	color_wheel = make_color_wheel_from_part_sizes(part_sizes)
	for i, size in enumerate(part_sizes):
		mRNA_part = {}
		num = i // 2 + 1
		if i == 0:
			part_type = '5&prime; UTR'
			part_name = part_type
		elif i == len(part_sizes) - 1:
			part_type = '3&prime; UTR'
			part_name = part_type
		else:
			part_type = part_type_tuple[(i+1)%2]
			part_name = "{0} {1}".format(part_type, num)
		shift = (i%3) * len(color_wheel)//3
		color = color_wheel[(i//3 + shift)%len(color_wheel)]
		mRNA_part['name'] = part_name
		mRNA_part['color'] = '#'+color
		mRNA_part['type'] = part_type
		mRNA_part['size'] = size
		pre_mRNA_tree.append(mRNA_part)
	return pre_mRNA_tree

#==========================
#==========================
def makeCompleteQuestion(N, num_exons):
	part_sizes = getGenePartSizes(num_exons)
	pre_mRNA_tree = makePre_mRNA_tree(part_sizes)
	#print(pre_mRNA_tree)
	table = makeHtmlTable(pre_mRNA_tree)
	valid_mRNA_list = makeAllValid_mRNA(pre_mRNA_tree, num_exons, num_exons-1)
	invalid_mRNA = makeINValid_mRNA(pre_mRNA_tree, num_exons, num_exons-1)
	answer = makeHtmlTable(invalid_mRNA)

	random.shuffle(valid_mRNA_list)
	valid_mRNA_choices = valid_mRNA_list[:4]
	random.shuffle(valid_mRNA_choices)
	choices_list = []
	for mRNA_tree in valid_mRNA_choices:
		mRNA_table = makeHtmlTable(mRNA_tree)
		choices_list.append(mRNA_table)
	choices_list += [answer, ]
	random.shuffle(choices_list)

	f = open("temp.html", "w")
	pre_mRNA_table = makeHtmlTable(pre_mRNA_tree)
	f.write(pre_mRNA_table)
	for choice in choices_list:
		f.write(choice)
	f.close()

	question = ''
	question += '<p>The eukaryotic pre-mRNA shown above can be alternatively spliced in a number of different ways.</p>'
	question += '<h5>Which one of the following is NOT a possible processed mRNA?</h5>'

	#sys.exit(1)
	bbformat = bptools.formatBB_MC_Question(N, pre_mRNA_table+question, choices_list, answer)
	return bbformat

#==========================
#==========================
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num-exons', type=int, dest='num_exons',
		help='number of exons in the gene', default=4)
	parser.add_argument('-q', '--num-questions', type=int, dest='num_questions',
		help='number of questions to create', default=24)
	args = parser.parse_args()

	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(args.num_questions):
		N = i+1
		bbformat = makeCompleteQuestion(N, args.num_exons)
		f.write(bbformat)
		f.write('\n')
	f.close()
	proc = subprocess.Popen("open temp.html", shell=True)
	bptools.print_histogram()
