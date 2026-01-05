#!/usr/bin/env python3

import random

import bptools


CHOICE_POOL = [
	"All daughters are red-eyed (carriers) and all sons are white-eyed.",
	"All daughters are red-eyed (carriers) and all sons are red-eyed.",
	"All daughters are white-eyed and all sons are red-eyed.",
	"Half the daughters are white-eyed and half are red-eyed; all sons are white-eyed.",
	"All offspring are white-eyed.",
	"All offspring are red-eyed.",
	"Half the sons are white-eyed and half are red-eyed; all daughters are red-eyed (carriers).",
]


#=====================
def make_cross():
	cross_type = random.choice(("female_affected", "male_affected"))
	if cross_type == "female_affected":
		stem = (
			"<p>In fruit flies, eye color is X-linked with red eyes dominant to white eyes. "
			"A true-breeding white-eyed female is crossed with a true-breeding red-eyed male.</p>"
		)
		answer = "All daughters are red-eyed (carriers) and all sons are white-eyed."
	else:
		stem = (
			"<p>In fruit flies, eye color is X-linked with red eyes dominant to white eyes. "
			"A true-breeding red-eyed female is crossed with a white-eyed male.</p>"
		)
		answer = "All daughters are red-eyed (carriers) and all sons are red-eyed."
	return stem, answer


#=====================
def write_question(N, args):
	question_text, answer_text = make_cross()
	question_text += "<p>Which statement best describes the F<sub>1</sub> offspring?</p>"

	choices = [choice for choice in CHOICE_POOL if choice != answer_text]
	choices_list = random.sample(choices, 4)
	choices_list.append(answer_text)
	random.shuffle(choices_list)

	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_question


#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate questions.")
	args = parser.parse_args()
	return args


#===========================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == "__main__":
	main()
