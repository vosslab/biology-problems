#!/usr/bin/env python3

import random

import bptools


# Match the eye and sex colors used in poisson_flies.py.
TEXT_LABELS = {
	"red-eyed": ("red-eyed", "#8b0000"),
	"red eyes": ("red eyes", "#8b0000"),
	"white-eyed": ("white-eyed", "#595959"),
	"white eyes": ("white eyes", "#595959"),
	"female": ("female (&female;)", "#990070"),
	"daughters": ("daughters (&female;)", "#990070"),
	"male": ("male (&male;)", "#002499"),
	"sons": ("sons (&male;)", "#002499"),
}


#=====================
def color_labels(text):
	"""Apply the same phenotype and sex labels to the stem and every choice."""
	replacements = {
		word: bptools.colorHTMLText(label, color[1:])
		for word, (label, color) in TEXT_LABELS.items()
	}
	colored_text = bptools.applyReplacementRulesToText(text, replacements)
	return colored_text


CHOICE_POOL = [
	"All daughters are red-eyed (carriers) and all sons are white-eyed.",
	"All daughters are red-eyed (carriers) and all sons are red-eyed.",
	"All daughters are white-eyed and all sons are red-eyed.",
	"Half the daughters are white-eyed and half are red-eyed; all sons are white-eyed.",
	"All offspring are white-eyed.",
	"Half the sons are white-eyed and half are red-eyed; all daughters are red-eyed (carriers).",
]


#=====================
def make_cross():
	cross_type = random.choice(("female_affected", "male_affected"))
	if cross_type == "female_affected":
		stem = (
			"<p>In fruit flies, eye color is X-linked with red eyes dominant to white eyes. "
			"A white-eyed female is crossed with a red-eyed male.</p>"
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

	question_text = color_labels(question_text)
	choices_list = [color_labels(choice) for choice in choices_list]
	answer_text = color_labels(answer_text)
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
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == "__main__":
	main()
