#!/usr/bin/env python

import os
import sys
import random
import argparse
import colorsys

import bptools

#==========================
#==========================
def getGenePartSizes(num_exons):
	total_gene_parts = num_exons * 2 + 1
	#5' UTR - exon 1 - intron 1 - exon 2 - ... - intron N-1 - exon N - 3' UTR
	part_sizes = []
	for i in range(total_gene_parts):
		part_size = random.randint(2, 99) * 10
		part_sizes.append(part_size)
	return part_sizes

#==========================
#==========================
def make_color_wheel(r, g, b, degree_step=40): # Assumption: r, g, b in [0, 255]
	r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
	#print(r, g, b)
	hue, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
	#print(hue, l, s)
	wheel = []
	for deg in range(0, 359, degree_step):
		hue_i = (hue*360. + float(deg))/360.
		#print(hue_i, l, s)
		ryb_percent_color = colorsys.hls_to_rgb(hue_i, l, s)
		#print(ryb_percent_color)
		rgb_percent_color = ryb_to_rgb(*ryb_percent_color)
		rgb_color = tuple(map(lambda x: int(round(x*255)), rgb_percent_color))
		hexcolor = '%02x%02x%02x' % rgb_color
		wheel.append(hexcolor)
	return wheel

#==========================
#==========================
def _cubic(t, a, b):
	weight = t * t * (3 - 2*t)
	return a + weight * (b - a)

#==========================
#==========================
def ryb_to_rgb(r, y, b): # Assumption: r, y, b in [0, 1]
	# red
	x0, x1 = _cubic(b, 1.0, 0.163), _cubic(b, 1.0, 0.0)
	x2, x3 = _cubic(b, 1.0, 0.5), _cubic(b, 1.0, 0.2)
	y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
	red = _cubic(r, y0, y1)
	# green
	x0, x1 = _cubic(b, 1.0, 0.373), _cubic(b, 1.0, 0.66)
	x2, x3 = _cubic(b, 0., 0.), _cubic(b, 0.5, 0.094)
	y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
	green = _cubic(r, y0, y1)
	# blue
	x0, x1 = _cubic(b, 1.0, 0.6), _cubic(b, 0.0, 0.2)
	x2, x3 = _cubic(b, 0.0, 0.5), _cubic(b, 0.0, 0.0)
	y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
	blue = _cubic(r, y0, y1)
	# return
	return (red, green, blue)


#==========================
#==========================
def makeHtmlTable(part_sizes):
	color_wheel = make_color_wheel(128, 128, 0, 22)
	table = ''
	table += '<table style="border-collapse: collapse; border: 2px solid black; table-layout: fixed;'
	table += '<colgroup width="{0}"></colgroup>'.format(10)
	for size in part_sizes:
		table += '<colgroup width="{0}"></colgroup>'.format(size)
	table += '<colgroup width="{0}px"></colgroup>'.format(10)
	table += '<tr>'
	part_type_tuple = ('exon', 'intron')
	for i, size in enumerate(part_sizes):
		shift = (i%2) * len(color_wheel)//2
		color = color_wheel[(i)%len(color_wheel)]
		part_type = part_type_tuple[(i+1)%2]
		if i == 0:
			table += '<td bgcolor="#{0}">5&prime; UTR &mdash; {1} bp</td>'.format(color, size)
		elif i == len(part_sizes) - 1:
			table += '<td bgcolor="#{0}">3&prime; UTR &mdash; {1} bp</td>'.format(color, size)
		else:
			table += '<td bgcolor="#{0}">{1} &mdash; {2} bp</td>'.format(color, part_type, size)
	table += '</tr>'
	table += '</table>'
	print(table)
	return table


#==========================
#==========================
def makeCompleteQuestion(N, num_exons):
	part_sizes = getGenePartSizes(num_exons)
	table = makeHtmlTable(part_sizes)
	f = open("temp.html", "w")
	f.write(table)
	f.close()

	sys.exit(1)
	bbformat = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbformat




#==========================
#==========================
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num-exons', type=int, dest='num_exons',
		help='number of exons in the gene', default=5)
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
