#!/usr/bin/env python

import os
import sys
import random
import itertools

colors = ('violet (410 nm)', 'indigo (430 nm)', 'blue (460 nm)', 'green (530 nm)', 'yellow (580 nm)', 'orange (600 nm)', 'red (700 nm)')
html_colors = ('#9d159d', '#4a0080', '#000080', '#006600', '#b3b300', '#e63900', '#990000')
options = ('donor_absorb', 'fret_color', 'acceptor_emit')

#TYPE 1, the correct order of the colors
#TYPE 2, the correct overlap of donor/acceptor C1 -> C2 and C3 -> C4; C2=C3, not C1=C4 or C1=C3 or C2=C4

#==================================
def colorHtml(color_id):
	html_text = '<span style="color: {0}"><strong>{1}</strong></span>'.format(html_colors[color_id], colors[color_id])
	return html_text

#==================================
def writeChoice(donor_absorb_id, fret_color_id, acceptor_emit_id):
	choice = ""
	choice += "The donor protein absorbs {0} and emits {1}; ".format(colorHtml(donor_absorb_id), colorHtml(fret_color_id))
	choice += "the acceptor protein absorbs {0} and emits {1}. ".format(colorHtml(fret_color_id), colorHtml(acceptor_emit_id))
	return choice

#==================================
#==================================
if __name__ == '__main__':
	answer_hist = {}
	num_duplicates = 2
	#==================================
	indices = list(range(7))
	set_indices = list(itertools.combinations(indices, 3))
	filtered_set_indices = []
	for color_set in set_indices:
		if color_set[1] - color_set[0] == 1 or color_set[2] - color_set[1] == 1:
			#make sure the colors are not next to one another
			continue
		filtered_set_indices.append(color_set)
	print("There are {0} possible color combinations after filtering".format(len(filtered_set_indices)))
	#print(set_indices)

	#==================================
	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
		
	for color_set in filtered_set_indices:
		if color_set[1] - color_set[0] == 1 or color_set[2] - color_set[1] == 1:
			#make sure the colors are not next to one another
			continue
		donor_absorb = colors[color_set[0]]
		fret_color = colors[color_set[1]]
		acceptor_emit = colors[color_set[2]]
		print(donor_absorb, fret_color, acceptor_emit)
		N += 1
		number = "{0}. ".format(N)
		question = ""
		question += "F&ouml;rster resonance energy transfer (FRET) requires both an acceptor fluorescent protein and a donor fluorescent protein. "
		question += "Which one of the following color combinations would be an effective FRET setup? "

		letters = "ABCDEF"

		permuations = list(itertools.permutations(color_set))
		random.shuffle(permuations)
		#print(permuations)
		
		for d in range(num_duplicates):
			random.shuffle(permuations)
			f.write("MC\t{0}\t".format(question))
			print("{0}. {1}".format(N, question))
			for i, color_permute in enumerate(permuations):
				choice = writeChoice(color_permute[0], color_permute[1], color_permute[2])
				f.write(choice+'\t')
				if color_permute == color_set:
					prefix = 'x'
					f.write('Correct\t')
					answer_hist[letters[i]] = answer_hist.get(letters[i], 0) + 1
				else:
					prefix = ' '
					f.write('Incorrect\t')
				print('- [{0}] {1}. {2}'.format(prefix, letters[i], choice))
			print("")
			f.write('\n')
	f.close()
	print(answer_hist)


