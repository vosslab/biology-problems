#!/usr/bin/env python3

import os
import sys
import random
import itertools

colors = ('violet (410 nm)', 'indigo (430 nm)', 'blue (460 nm)', 'green (530 nm)', 'yellow (580 nm)', 'orange (600 nm)', 'red (700 nm)')
html_colors = ('#9d159d', '#4a0080', '#000080', '#006600', '#b3b300', '#e63900', '#990000')
options = ('donor_absorb', 'fret_color', 'acceptor_emit')

# THIS IS TYPE 2...
#TYPE 1, the correct order of the colors
#TYPE 2, the correct overlap of donor/acceptor C1 -> C2 and C3 -> C4; C2=C3, not C1=C4 or C1=C3 or C2=C4

#==================================
def colorHtml(color_id):
	html_text = '<span style="color: {0}"><strong>{1}</strong></span>'.format(html_colors[color_id], colors[color_id])
	return html_text

#==================================
def writeChoice(color_seq):
	choice = ""
	choice += "The donor protein absorbs {0} and emits {1}; ".format(colorHtml(color_seq[0]), colorHtml(color_seq[1]))
	choice += "the acceptor protein absorbs {0} and emits {1}. ".format(colorHtml(color_seq[2]), colorHtml(color_seq[3]))
	return choice

#==================================
#==================================
if __name__ == '__main__':
	answer_hist = {}
	num_duplicates = 5
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
			#double check to make sure the colors are not next to one another
			print("colors were not filtered")
			sys.exit(1)
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

		#TYPE 2, the correct overlap of donor/acceptor C1 -> C2 and C3 -> C4; C2=C3, not C1=C4 or C1=C3 or C2=C4
		correct_seq = (color_set[0], color_set[1], color_set[1], color_set[2])

		wrong1a_seq = (color_set[0], color_set[1], color_set[2], color_set[0])
		wrong2a_seq = (color_set[0], color_set[1], color_set[0], color_set[2])
		wrong3a_seq = (color_set[0], color_set[1], color_set[2], color_set[1])

		wrong0b_seq = (color_set[2], color_set[1], color_set[1], color_set[0])
		wrong1b_seq = (color_set[2], color_set[1], color_set[0], color_set[2])
		wrong2b_seq = (color_set[2], color_set[1], color_set[2], color_set[0])
		wrong3b_seq = (color_set[2], color_set[1], color_set[0], color_set[1])

		color_sequences = [wrong1a_seq, wrong2a_seq, wrong3a_seq, wrong0b_seq, wrong1b_seq, wrong2b_seq, wrong3b_seq]
		random.shuffle(color_sequences)
		color_sequences.pop()
		random.shuffle(color_sequences)
		color_sequences.pop()
		random.shuffle(color_sequences)
		color_sequences.pop()
		random.shuffle(color_sequences)
		color_sequences.append(correct_seq)
		random.shuffle(color_sequences)
		
		for d in range(num_duplicates):
			random.shuffle(color_sequences)
			f.write("MC\t{0}\t".format(question))
			print("{0}. {1}".format(N, question))
			for i, color_seq in enumerate(color_sequences):
				choice = writeChoice(color_seq)
				f.write(choice+'\t')
				if color_seq == correct_seq:
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


