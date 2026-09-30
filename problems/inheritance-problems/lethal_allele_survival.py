#!/usr/bin/env python3

import sys
import random
import argparse
from fractions import Fraction

import bptools


TRAITS = [
	{
		"organism": "fruit flies",
		"trait": "curly wings",
		"wildtype": "straight wings (wildtype)",
		"symbol": "C",
		"totals": (48, 72, 96, 120),
	},
	{
		"organism": "cattle",
		"trait": "dwarf legs",
		"wildtype": "typical leg length (wildtype)",
		"symbol": "D",
		"totals": (12, 24),
	},
	{
		"organism": "cats",
		"trait": "no tail",
		"wildtype": "a tail (wildtype)",
		"symbol": "T",
		"totals": (12,),
	},
	{
		"organism": "mice",
		"trait": "a yellow coat",
		"wildtype": "a non-yellow coat (wildtype)",
		"symbol": "Y",
		"totals": (12, 24),
	},
]

QUESTION_TYPES = (
	"lethal_fraction",
	"survival_fraction",
	"affected_fraction",
	"wildtype_fraction",
	"affected_survivor_fraction",
	"wildtype_survivor_fraction",
	"lethal_count",
	"survival_count",
	"affected_count",
	"wildtype_count",
	"affected_survivors_count",
	"wildtype_survivors_count",
	"affected_to_wildtype_ratio",
	"wildtype_to_affected_ratio",
)

CROSSES = [
	{
		"parents": "heterozygote_x_heterozygote",
		"lethal_fraction": Fraction(1, 4),
		"affected_fraction": Fraction(1, 2),
		"wildtype_fraction": Fraction(1, 4),
	},
	{
		"parents": "heterozygote_x_wildtype",
		"lethal_fraction": Fraction(0, 1),
		"affected_fraction": Fraction(1, 2),
		"wildtype_fraction": Fraction(1, 2),
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

GENOTYPE_COLORS = {
	"lethal": "#8a3b20",
	"heterozygous": "#245b88",
	"wildtype": "#326430",
}

# Built and shuffled once per run; each question uses one scenario without cycling.
SCENARIOS: list[tuple] = []


#=====================
def build_scenarios() -> list[tuple]:
	scenarios = []
	for trait in TRAITS:
		for cross in CROSSES:
			for question_type in QUESTION_TYPES:
				totals = trait["totals"] if question_type.endswith("_count") else (None,)
				for total in totals:
					scenarios.append((trait, cross, question_type, total))
	return scenarios


#=====================
def genotype_text(genotype: str, kind: str) -> str:
	text = f"<strong style='color: {GENOTYPE_COLORS[kind]};'>{genotype}</strong>"
	return text


#=====================
def cross_setup(trait: dict, cross: dict) -> str:
	allele = trait["symbol"]
	heterozygote = genotype_text(f"{allele}{allele.lower()}", "heterozygous")
	if cross["parents"] == "heterozygote_x_heterozygote":
		text = f"Two heterozygous individuals ({heterozygote}) are crossed"
	else:
		wildtype = genotype_text(allele.lower() * 2, "wildtype")
		text = f"A heterozygous parent ({heterozygote}) is crossed with a wildtype parent ({wildtype})"
	return text


#=====================
def make_fraction_choices(correct: Fraction) -> tuple:
	distractors = list(FRACTION_LABELS)
	distractors = [frac for frac in distractors if frac != correct]
	choices = [correct] + random.sample(distractors, 4)
	random.shuffle(choices)
	return [FRACTION_LABELS[frac] for frac in choices], FRACTION_LABELS[correct]


#=====================

def make_ratio_choices(correct: str) -> tuple:
	choices = ["1 to 1", "2 to 1", "3 to 1", "1 to 2", "3 to 2"]
	if correct not in choices:
		raise ValueError(f"unsupported living phenotype ratio: {correct}")
	random.shuffle(choices)
	return choices, correct


#=====================
def probabilities_for_cross(cross: dict) -> dict:
	lethal = cross["lethal_fraction"]
	affected = cross["affected_fraction"]
	wildtype = cross["wildtype_fraction"]
	survival = affected + wildtype
	if lethal + survival != 1:
		raise ValueError("cross probabilities must sum to one")
	return {
		"lethal": lethal,
		"survival": survival,
		"affected": affected,
		"wildtype": wildtype,
		"affected_survivors": affected / survival,
		"wildtype_survivors": wildtype / survival,
	}


#=====================
def ratio_text(numerator: Fraction, denominator: Fraction) -> str:
	if numerator == denominator:
		return "1 to 1"
	ratio = numerator / denominator
	if ratio.denominator == 1:
		return f"{ratio.numerator} to 1"
	return f"1 to {ratio.denominator}"


#=====================
def make_count_choices(correct: Fraction, total: int) -> tuple:
	# Each choice supplies the arithmetic; students choose the inheritance fraction.
	if total % 12 != 0:
		raise ValueError("offspring totals must be divisible by both 3 and 4")
	distractors = [frac for frac in FRACTION_LABELS if frac != correct]
	choices = [correct] + random.sample(distractors, 4)
	random.shuffle(choices)
	labels = {}
	for frac in choices:
		fraction_text = str(frac)
		count = total * frac
		labels[frac] = f"{fraction_text} &times; {total} = {count.numerator} offspring"
	return [labels[frac] for frac in choices], labels[correct]


#=====================
def cross_reference(trait: dict) -> str:
	allele = trait["symbol"]
	recessive = allele.lower()
	cell_style = "border: 1px solid #737373; padding: 8px 12px; color: #202020;"
	text = "<table style='border-collapse: collapse; margin: 12px 0;'>"
	text += "<caption><strong>Genotype key</strong></caption>"
	text += f"<tr><th scope='col' style='{cell_style}'>Genotype</th>"
	text += f"<th scope='col' style='{cell_style}'>What happens</th></tr>"
	rows = (
		(f"{allele}{allele}", "Does not survive (lethal)", "#fce4d6", "lethal"),
		(f"{allele}{recessive}", f"Survives with {trait['trait']}", "#e2eef9", "heterozygous"),
		(f"{recessive}{recessive}", f"Survives with {trait['wildtype']}", "#e4f1df", "wildtype"),
	)
	for genotype, description, background, kind in rows:
		style = f"{cell_style} background-color: {background};"
		text += f"<tr><th scope='row' style='{style}'>{genotype_text(genotype, kind)}</th>"
		text += f"<td style='{cell_style}'>{description}</td></tr>"
	text += "</table>"
	return text


#=====================
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	trait, cross, question_type, total = SCENARIOS[N - 1]
	probabilities = probabilities_for_cross(cross)

	allele = trait["symbol"]
	heterozygote = genotype_text(f"{allele}{allele.lower()}", "heterozygous")
	lethal = genotype_text(allele * 2, "lethal")
	question_text = f"<p>In {trait['organism']}, heterozygous offspring "
	question_text += f"({heterozygote}) have {trait['trait']}. "
	question_text += f"Offspring with two copies of {allele} ({lethal}) do not survive. "
	question_text += "The table shows what happens with each genotype.</p>"
	question_text += cross_reference(trait)
	setup = cross_setup(trait, cross)

	fraction_prompts = {
		"lethal_fraction": ("lethal", "What fraction of all offspring will not survive?"),
		"survival_fraction": ("survival", "What fraction of all offspring will survive?"),
		"affected_fraction": (
			"affected",
			f"What fraction of all offspring will survive with {trait['trait']}?",
		),
		"wildtype_fraction": (
			"wildtype",
			f"What fraction of all offspring will survive with {trait['wildtype']}?",
		),
		"affected_survivor_fraction": (
			"affected_survivors",
			f"Of the offspring that survive, what fraction will have {trait['trait']}?",
		),
		"wildtype_survivor_fraction": (
			"wildtype_survivors",
			f"Of the offspring that survive, what fraction will have {trait['wildtype']}?",
		),
	}
	if question_type in fraction_prompts:
		probability_key, prompt = fraction_prompts[question_type]
		question_text += f"<p>{setup}. {prompt}</p>"
		choices_list, answer_text = make_fraction_choices(probabilities[probability_key])
	elif question_type.endswith("_count"):
		outcome = question_type.removesuffix("_count")
		outcome_text = {
			"lethal": "not survive",
			"survival": "survive",
			"affected": f"survive with {trait['trait']}",
			"wildtype": f"survive with {trait['wildtype']}",
			"affected_survivors": f"have {trait['trait']}",
			"wildtype_survivors": f"have {trait['wildtype']}",
		}[outcome]
		if outcome.endswith("_survivors"):
			if trait["organism"] == "cattle":
				question_text += f"<p>{setup}. Across several matings, {total} offspring survive. "
			else:
				question_text += f"<p>{setup} and produce {total} surviving offspring. "
			question_text += f"How many of the surviving offspring do you expect to {outcome_text}?</p>"
		else:
			if trait["organism"] == "cattle":
				question_text += f"<p>{setup}. Across several matings, they produce {total} offspring. "
			elif trait["organism"] in ("cats", "mice"):
				question_text += f"<p>{setup} and produce a litter of {total} offspring. "
			else:
				question_text += f"<p>{setup} and produce {total} offspring. "
			question_text += "This total includes offspring that do not survive. "
			question_text += f"How many do you expect to {outcome_text}?</p>"
		correct = probabilities[outcome]
		choices_list, answer_text = make_count_choices(correct, total)
	else:
		question_text += f"<p>{setup}. "
		question_text += "What ratio do you expect among the offspring that survive?<br/>"
		if question_type == "affected_to_wildtype_ratio":
			question_text += f"<strong>{trait['trait']} : {trait['wildtype']}</strong></p>"
			correct = ratio_text(probabilities["affected"], probabilities["wildtype"])
		else:
			question_text += f"<strong>{trait['wildtype']} : {trait['trait']}</strong></p>"
			correct = ratio_text(probabilities["wildtype"], probabilities["affected"])
		choices_list, answer_text = make_ratio_choices(correct)

	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_question


#===========================================================
def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(description="Generate questions.")
	args = parser.parse_args()
	return args


#===========================================================
def main() -> None:
	args = parse_arguments()
	global SCENARIOS
	SCENARIOS = build_scenarios()
	random.shuffle(SCENARIOS)
	requested = args.duplicates
	if args.max_questions is not None:
		requested = min(requested, args.max_questions)
	if requested > len(SCENARIOS):
		print(
			f"Requested {requested} questions; only {len(SCENARIOS)} unique scenarios are available. "
			f"Writing {len(SCENARIOS)} questions without repeats.", file=sys.stderr,
		)
	args.max_questions = min(requested, len(SCENARIOS))
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == "__main__":
	main()
