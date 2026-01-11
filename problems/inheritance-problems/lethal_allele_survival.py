#!/usr/bin/env python3

import random
from fractions import Fraction

import bptools


TRAITS = [
	{
		"organism": "fruit flies",
		"trait": "curly wings",
		"symbol": "C",
	},
	{
		"organism": "cattle",
		"trait": "dwarf legs",
		"symbol": "D",
	},
	{
		"organism": "cats",
		"trait": "tailless",
		"symbol": "T",
	},
	{
		"organism": "mice",
		"trait": "yellow coat",
		"symbol": "Y",
	},
]

QUESTION_TYPES = ("lethal_fraction", "survival_fraction", "survival_count", "lethal_count", "living_ratio")

FRACTION_LABELS = {
	Fraction(0, 1): "None, 0%",
	Fraction(1, 4): "1/4, 25%",
	Fraction(1, 3): "1/3, 33.3%",
	Fraction(1, 2): "1/2, 50%",
	Fraction(2, 3): "2/3, 66.7%",
	Fraction(3, 4): "3/4, 75%",
	Fraction(1, 1): "All, 100%",
}


#=====================
def make_fraction_choices(correct):
	distractors = [Fraction(1, 4), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)]
	distractors = [frac for frac in distractors if frac != correct]
	choices = [correct] + random.sample(distractors, 3)
	random.shuffle(choices)
	return [FRACTION_LABELS[frac] for frac in choices], FRACTION_LABELS[correct]


#=====================
def make_ratio_choices(correct):
	choices = ["1:1", "2:1", "3:1", "1:2", "3:2"]
	random.shuffle(choices)
	if correct not in choices:
		choices[0] = correct
	return choices, correct


#=====================
def make_count_choices(correct, total):
	choices = {correct}
	for frac in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 1)):
		choices.add(int(total * frac))
	choices = list(choices)
	if len(choices) < 5:
		choices.extend([correct + 4, max(0, correct - 4)])
	choices = sorted(set(choices))
	random.shuffle(choices)
	return [str(value) for value in choices[:5]], str(correct)


#=====================
def write_question(N, args):
	trait = random.choice(TRAITS)
	question_type = random.choice(QUESTION_TYPES)
	allele = trait["symbol"]

	question_text = (
		f"<p>In {trait['organism']}, allele {allele} causes {trait['trait']} in heterozygotes "
		f"({allele}{allele.lower()}) but is lethal in homozygotes ({allele}{allele}). "
		f"Two heterozygous individuals are crossed.</p>"
	)

	if question_type == "lethal_fraction":
		question_text += "<p>What fraction of all conceptions are expected to be lethal?</p>"
		choices_list, answer_text = make_fraction_choices(Fraction(1, 4))
	elif question_type == "survival_fraction":
		question_text += "<p>What fraction of all conceptions are expected to survive?</p>"
		choices_list, answer_text = make_fraction_choices(Fraction(3, 4))
	elif question_type == "living_ratio":
		question_text += "<p>Among surviving offspring, what is the ratio of "
		question_text += f"{trait['trait']} to normal phenotype?</p>"
		choices_list, answer_text = make_ratio_choices("2:1")
	elif question_type == "lethal_count":
		total = random.choice((40, 80, 120, 160))
		question_text += f"<p>If {total} conceptions occur, how many are expected to be lethal?</p>"
		choices_list, answer_text = make_count_choices(total // 4, total)
	else:
		total = random.choice((40, 80, 120, 160))
		question_text += f"<p>If {total} conceptions occur, how many are expected to survive?</p>"
		choices_list, answer_text = make_count_choices(3 * total // 4, total)

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
