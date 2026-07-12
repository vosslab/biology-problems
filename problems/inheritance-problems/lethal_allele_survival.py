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

QUESTION_TYPES = (
	"lethal_fraction",
	"survival_fraction",
	"affected_fraction",
	"normal_fraction",
	"affected_survivor_fraction",
	"normal_survivor_fraction",
	"lethal_count",
	"survival_count",
	"affected_count",
	"normal_count",
	"affected_to_normal_ratio",
	"normal_to_affected_ratio",
)

CROSSES = [
	{
		"parents": "heterozygote_x_heterozygote",
		"lethal_fraction": Fraction(1, 4),
		"affected_fraction": Fraction(1, 2),
		"normal_fraction": Fraction(1, 4),
	},
	{
		"parents": "heterozygote_x_normal",
		"lethal_fraction": Fraction(0, 1),
		"affected_fraction": Fraction(1, 2),
		"normal_fraction": Fraction(1, 2),
	},
]

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
	distractors = list(FRACTION_LABELS)
	distractors = [frac for frac in distractors if frac != correct]
	choices = [correct] + random.sample(distractors, 4)
	random.shuffle(choices)
	return [FRACTION_LABELS[frac] for frac in choices], FRACTION_LABELS[correct]


#=====================

def make_ratio_choices(correct):
	choices = ["1 to 1", "2 to 1", "3 to 1", "1 to 2", "3 to 2"]
	if correct not in choices:
		raise ValueError(f"unsupported living phenotype ratio: {correct}")
	random.shuffle(choices)
	return choices, correct


#=====================
def probabilities_for_cross(cross):
	lethal = cross["lethal_fraction"]
	affected = cross["affected_fraction"]
	normal = cross["normal_fraction"]
	survival = affected + normal
	if lethal + survival != 1:
		raise ValueError("cross probabilities must sum to one")
	return {
		"lethal": lethal,
		"survival": survival,
		"affected": affected,
		"normal": normal,
		"affected_survivors": affected / survival,
		"normal_survivors": normal / survival,
	}


#=====================
def ratio_text(numerator, denominator):
	if numerator == denominator:
		return "1 to 1"
	ratio = numerator / denominator
	if ratio.denominator == 1:
		return f"{ratio.numerator} to 1"
	return f"1 to {ratio.denominator}"


#=====================
def make_count_choices(correct, total):
	distractors = set()
	for frac in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 1)):
		distractors.add(int(total * frac))
	distractors.update((correct + 4, max(0, correct - 4)))
	distractors.discard(correct)
	if len(distractors) < 4:
		raise ValueError("could not generate four unique count distractors")
	choices = random.sample(sorted(distractors), 4)
	choices.append(correct)
	random.shuffle(choices)
	return [str(value) for value in choices], str(correct)


#=====================
def write_question(N, args):
	trait = random.choice(TRAITS)
	cross = random.choice(CROSSES)
	question_type = random.choice(QUESTION_TYPES)
	allele = trait["symbol"]
	probabilities = probabilities_for_cross(cross)

	question_text = (
		f"<p>In {trait['organism']}, allele {allele} causes {trait['trait']} in heterozygotes "
		f"({allele}{allele.lower()}) but is lethal in homozygotes ({allele}{allele}). "
	)
	if cross["parents"] == "heterozygote_x_heterozygote":
		cross_text = random.choice((
			"Two heterozygous individuals are crossed.",
			f"The parental cross is {allele}{allele.lower()} x {allele}{allele.lower()}.",
		))
	else:
		cross_text = random.choice((
			"A heterozygous individual is crossed with a normal homozygous recessive individual.",
			f"The parental cross is {allele}{allele.lower()} x "
			f"{allele.lower()}{allele.lower()}.",
		))
	question_text += cross_text + "</p>"

	fraction_prompts = {
		"lethal_fraction": ("lethal", "What fraction of all conceptions are expected to be lethal?"),
		"survival_fraction": ("survival", "What fraction of all conceptions are expected to survive?"),
		"affected_fraction": (
			"affected",
			f"What fraction of all conceptions are expected to show {trait['trait']}?",
		),
		"normal_fraction": (
			"normal",
			"What fraction of all conceptions are expected to have the normal phenotype?",
		),
		"affected_survivor_fraction": (
			"affected_survivors",
			f"Among surviving offspring, what fraction are expected to show {trait['trait']}?",
		),
		"normal_survivor_fraction": (
			"normal_survivors",
			"Among surviving offspring, what fraction are expected to have the normal phenotype?",
		),
	}
	if question_type in fraction_prompts:
		probability_key, prompt = fraction_prompts[question_type]
		question_text += f"<p>{prompt}</p>"
		choices_list, answer_text = make_fraction_choices(probabilities[probability_key])
	elif question_type.endswith("_count"):
		total = random.choice((40, 80, 120, 160))
		outcome = question_type.removesuffix("_count")
		outcome_text = {
			"lethal": "be lethal",
			"survival": "survive",
			"affected": f"show {trait['trait']}",
			"normal": "have the normal phenotype",
		}[outcome]
		question_text += (
			f"<p>If {total} conceptions occur, how many are expected to {outcome_text}?</p>"
		)
		correct = int(total * probabilities[outcome])
		choices_list, answer_text = make_count_choices(correct, total)
	else:
		if question_type == "affected_to_normal_ratio":
			question_text += "<p>Among surviving offspring, what is the ratio of "
			question_text += f"{trait['trait']} to normal phenotype?</p>"
			correct = ratio_text(probabilities["affected"], probabilities["normal"])
		else:
			question_text += "<p>Among surviving offspring, what is the ratio of normal phenotype to "
			question_text += f"{trait['trait']}?</p>"
			correct = ratio_text(probabilities["normal"], probabilities["affected"])
		choices_list, answer_text = make_ratio_choices(correct)

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
