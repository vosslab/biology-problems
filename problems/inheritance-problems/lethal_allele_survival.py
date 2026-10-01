#!/usr/bin/env python3

import sys
import random
import argparse
from fractions import Fraction

import bptools
import gene_mapping.phenotypes_for_flies
import gene_mapping.phenotypes_for_yeast


OFFSPRING_TOTALS = (48, 72, 96, 120)

ORGANISM_ICONS = {
	"fruit fly": "&#129712;",
	"budding yeast": "&#129440;",
}

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

THIRDS = (Fraction(1, 3), Fraction(2, 3))

GENOTYPE_COLORS = {
	"lethal": "#8a3b20",
	"heterozygous": "#245b88",
	"wildtype": "#326430",
}

# Built and shuffled once per run; each question uses one scenario without cycling.
SCENARIOS: list[tuple] = []


#=====================
def build_scenarios() -> list[tuple]:
	templates = []
	weights = []
	for cross in CROSSES:
		probabilities = probabilities_for_cross(cross)
		for question_type in QUESTION_TYPES:
			probability_key = question_type.replace("_survivor_fraction", "_survivors")
			probability_key = probability_key.removesuffix("_fraction").removesuffix("_count")
			# Favor survivor-denominator questions with thirds as the correct probability.
			weight = 1
			if probability_key in probabilities and probabilities[probability_key] in THIRDS:
				weight = 8
			totals = OFFSPRING_TOTALS if question_type.endswith("_count") else (None,)
			for total in totals:
				templates.append((cross, question_type, total))
				weights.append(weight)
	scenarios = []
	for phenotype_dict in (
			gene_mapping.phenotypes_for_flies.phenotype_dict,
			gene_mapping.phenotypes_for_yeast.phenotype_dict):
		# Single-letter aliases identify phenotype labels, excluding dictionary metadata.
		phenotypes = [phenotype_dict[key] for key in sorted(phenotype_dict) if len(key) == 1]
		for affected in phenotypes:
			for wildtype in phenotypes:
				if affected == wildtype:
					continue
				# Shuffling the combined pool chooses an organism and pair for each question.
				cross, question_type, total = random.choices(templates, weights=weights, k=1)[0]
				named_trait = {
					"organism": phenotype_dict["common name"],
					"symbol": "C", "trait": affected, "wildtype": wildtype,
				}
				scenarios.append((named_trait, cross, question_type, total))
	return scenarios


#=====================
def genotype_text(genotype: str, kind: str) -> str:
	text = f"<strong style='color: {GENOTYPE_COLORS[kind]}; "
	text += "font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 1em;'>"
	text += f"{genotype}</strong>"
	return text


#=====================
def cross_setup(trait: dict, cross: dict) -> str:
	allele = trait["symbol"]
	heterozygote = genotype_text(f"{allele}{allele.lower()}", "heterozygous")
	if cross["parents"] == "heterozygote_x_heterozygote":
		second_parent = heterozygote
	else:
		second_parent = genotype_text(allele.lower() * 2, "wildtype")
	text = f"<strong>Parent 1:</strong> {heterozygote} &times; "
	text += f"<strong>Parent 2:</strong> {second_parent}"
	return text


#=====================
def select_fractions(correct: Fraction) -> list[Fraction]:
	# Include both thirds, then vary the remaining choices and sort by percentage.
	selected = {correct, *THIRDS}
	distractors = [frac for frac in FRACTION_LABELS if frac not in selected]
	selected.update(random.sample(distractors, 5 - len(selected)))
	choices = sorted(selected)
	return choices


#=====================
def make_fraction_choices(correct: Fraction) -> tuple:
	choices = select_fractions(correct)
	return [FRACTION_LABELS[frac] for frac in choices], FRACTION_LABELS[correct]


#=====================

def make_ratio_choices(correct: str) -> tuple:
	choices = ["1 to 2", "1 to 1", "3 to 2", "2 to 1", "3 to 1"]
	if correct not in choices:
		raise ValueError(f"unsupported living phenotype ratio: {correct}")
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
	choices = select_fractions(correct)
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
	cell_style = "padding: 4px 10px; text-align: left; color: #202020;"
	text = "<table style='border-collapse: collapse; "
	text += "margin: 0 0 12px; max-width: 100%;'>"
	text += "<tr style='border-bottom: 1px solid #b8b8b8;'>"
	text += f"<th scope='col' style='{cell_style}'>Genotype</th>"
	text += f"<th scope='col' style='{cell_style}'>Outcome</th></tr>"
	affected_outcome = trait['trait'].capitalize()
	wildtype_outcome = trait['wildtype'].capitalize()
	rows = (
		(f"{allele}{allele}", "<span aria-hidden='true'>&#10060;</span> Lethal, does not survive",
			"lethal"),
		(f"{allele}{recessive}", affected_outcome, "heterozygous"),
		(f"{recessive}{recessive}", wildtype_outcome, "wildtype"),
	)
	for genotype, description, kind in rows:
		text += "<tr style='border-bottom: 1px solid #b8b8b8;'>"
		text += f"<th scope='row' style='{cell_style}'>{genotype_text(genotype, kind)}</th>"
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
	dominant_allele = genotype_text(allele, "heterozygous")
	recessive_allele = genotype_text(allele.lower(), "wildtype")
	dominant = genotype_text(f"{allele}_", "heterozygous")
	wildtype = genotype_text(allele.lower() * 2, "wildtype")
	lethal = genotype_text(allele * 2, "lethal")
	question_text = cross_reference(trait)
	question_text += '<p style="margin: 0 0 1.5em;">'
	question_text += f'<span aria-hidden="true">{ORGANISM_ICONS[trait["organism"]]}</span> '
	question_text += f"For a hypothetical {trait['organism']} trait, "
	question_text += f"{dominant_allele} is dominant to {recessive_allele}, "
	question_text += f"so {dominant} produces the {trait['trait']} phenotype "
	question_text += f"and {wildtype} produces the {trait['wildtype']} phenotype. "
	question_text += f"However, {lethal} is lethal and those offspring do not survive.</p>"
	setup = cross_setup(trait, cross)
	question_text += f'<p style="margin: 0;">{setup}.<br/>'

	fraction_prompts = {
		"lethal_fraction": (
			"lethal", f"What fraction of all offspring would have the lethal {lethal} genotype?",
		),
		"survival_fraction": ("survival", "What fraction of all offspring will survive?"),
		"affected_fraction": (
			"affected",
			f"What fraction of all offspring will survive with the {trait['trait']} phenotype?",
		),
		"wildtype_fraction": (
			"wildtype",
			f"What fraction of all offspring will survive with the {trait['wildtype']} phenotype?",
		),
		"affected_survivor_fraction": (
			"affected_survivors",
			f"Of the offspring that survive, what fraction will have the {trait['trait']} phenotype?",
		),
		"wildtype_survivor_fraction": (
			"wildtype_survivors",
			f"Of the offspring that survive, what fraction will have the {trait['wildtype']} phenotype?",
		),
	}
	if question_type in fraction_prompts:
		probability_key, prompt = fraction_prompts[question_type]
		question_text += f"{prompt}</p>"
		choices_list, answer_text = make_fraction_choices(probabilities[probability_key])
	elif question_type.endswith("_count"):
		outcome = question_type.removesuffix("_count")
		outcome_text = {
			"lethal": f"have the lethal {lethal} genotype",
			"survival": "survive",
			"affected": f"survive with the {trait['trait']} phenotype",
			"wildtype": f"survive with the {trait['wildtype']} phenotype",
			"affected_survivors": f"have the {trait['trait']} phenotype",
			"wildtype_survivors": f"have the {trait['wildtype']} phenotype",
		}[outcome]
		if outcome.endswith("_survivors"):
			question_text += f"The cross produces {total} surviving offspring.<br/>"
			question_text += f"How many of the surviving offspring do you expect to {outcome_text}?</p>"
		else:
			question_text += f"Before considering survival, assume the cross produces {total} offspring.<br/>"
			question_text += f"How many would you expect to {outcome_text}?</p>"
		correct = probabilities[outcome]
		choices_list, answer_text = make_count_choices(correct, total)
	else:
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
