#!/usr/bin/env python3

import random
import itertools

import bptools

colors = ('violet (410 nm)', 'indigo (430 nm)', 'blue (460 nm)', 'green (530 nm)', 'yellow (580 nm)', 'orange (600 nm)', 'red (700 nm)')
html_colors = ('#9d159d', '#4a0080', '#000080', '#006600', '#b3b300', '#e63900', '#990000')
options = ('donor_absorb', 'fret_color', 'acceptor_emit')

#TYPE 1, the correct order of the colors
#TYPE 2, the correct overlap of donor/acceptor C1 -> C2 and C3 -> C4; C2=C3, not C1=C4 or C1=C3 or C2=C4

#==================================
def colorHtml(color_id):
	return f'<span style="color: {html_colors[color_id]}"><strong>{colors[color_id]}</strong></span>'

#==================================
def writeChoice(donor_absorb_id, fret_color_id, acceptor_emit_id):
	choice = ""
	choice += f"The donor protein absorbs {colorHtml(donor_absorb_id)} and emits {colorHtml(fret_color_id)}; "
	choice += f"the acceptor protein absorbs {colorHtml(fret_color_id)} and emits {colorHtml(acceptor_emit_id)}. "
	return choice

#==================================
#==================================
def get_filtered_color_sets() -> list:
	indices = list(range(7))
	set_indices = list(itertools.combinations(indices, 3))
	filtered_set_indices = []
	for color_set in set_indices:
		if color_set[1] - color_set[0] == 1 or color_set[2] - color_set[1] == 1:
			#make sure the colors are not next to one another
			continue
		filtered_set_indices.append(color_set)
	return filtered_set_indices

#==================================
def build_question(color_set):
	question_text = ""
	question_text += "F&ouml;rster resonance energy transfer (FRET) requires both an acceptor fluorescent protein and a donor fluorescent protein. "
	question_text += "Which one of the following color combinations would be an effective FRET setup? "
	permuations = list(itertools.permutations(color_set))
	random.shuffle(permuations)
	choices = []
	answer = None
	for color_permute in permuations:
		choice = writeChoice(color_permute[0], color_permute[1], color_permute[2])
		choices.append(choice)
		if color_permute == color_set:
			answer = choice
	return question_text, choices, answer

#==================================
def write_question(N: int, args) -> str:
	color_sets = get_filtered_color_sets()
	color_set = random.choice(color_sets)
	question_text, choices, answer = build_question(color_set)
	return bptools.formatBB_MC_Question(N, question_text, choices, answer)

#==================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate FRET color permutation questions.")
	args = parser.parse_args()
	return args

#==================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == '__main__':
	main()
