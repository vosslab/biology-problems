#!/usr/bin/env python3

import itertools
import random

import bptools

colors = (
	"violet (410 nm)",
	"indigo (430 nm)",
	"blue (460 nm)",
	"green (530 nm)",
	"yellow (580 nm)",
	"orange (600 nm)",
	"red (700 nm)",
)
html_colors = ("#9d159d", "#4a0080", "#000080", "#006600", "#b3b300", "#e63900", "#990000")

#==========================
def color_html(color_id):
	return f'<span style="color: {html_colors[color_id]}"><strong>{colors[color_id]}</strong></span>'

#==========================
def write_choice(color_seq):
	choice = ""
	choice += f"The donor protein absorbs {color_html(color_seq[0])} and emits {color_html(color_seq[1])}; "
	choice += f"the acceptor protein absorbs {color_html(color_seq[2])} and emits {color_html(color_seq[3])}. "
	return choice

#==========================
def get_filtered_color_sets():
	indices = list(range(len(colors)))
	set_indices = list(itertools.combinations(indices, 3))
	filtered_set_indices = []
	for color_set in set_indices:
		if color_set[1] - color_set[0] == 1 or color_set[2] - color_set[1] == 1:
			continue
		filtered_set_indices.append(color_set)
	return filtered_set_indices

FILTERED_COLOR_SETS = get_filtered_color_sets()

#==========================
def build_color_sequences(color_set, num_choices):
	correct_seq = (color_set[0], color_set[1], color_set[1], color_set[2])

	wrong_sequences = [
		(color_set[0], color_set[1], color_set[2], color_set[0]),
		(color_set[0], color_set[1], color_set[0], color_set[2]),
		(color_set[0], color_set[1], color_set[2], color_set[1]),
		(color_set[2], color_set[1], color_set[1], color_set[0]),
		(color_set[2], color_set[1], color_set[0], color_set[2]),
		(color_set[2], color_set[1], color_set[2], color_set[0]),
		(color_set[2], color_set[1], color_set[0], color_set[1]),
	]
	random.shuffle(wrong_sequences)
	choices = wrong_sequences[: max(1, num_choices - 1)]
	choices.append(correct_seq)
	random.shuffle(choices)
	return choices, correct_seq

#==========================
def write_question(N, args):
	color_set = random.choice(FILTERED_COLOR_SETS)
	question = ""
	question += "F&ouml;rster resonance energy transfer (FRET) requires both an acceptor fluorescent protein "
	question += "and a donor fluorescent protein. "
	question += "Which one of the following color combinations would be an effective FRET setup? "

	color_sequences, correct_seq = build_color_sequences(color_set, args.num_choices)
	choices_list = [write_choice(color_seq) for color_seq in color_sequences]
	answer_text = write_choice(correct_seq)

	return bptools.formatBB_MC_Question(N, question, choices_list, answer_text)

#==========================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate FRET overlap color questions.")
	parser = bptools.add_choice_args(parser, default=5)
	args = parser.parse_args()
	return args

#==========================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#==========================
if __name__ == "__main__":
	main()

