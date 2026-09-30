#!/usr/bin/env python3

import sys
import random
import argparse

import bptools


TRAITS = [
	{
		"organism": "cats",
		"dominant": "short hair",
		"recessive": "long hair",
		"trait": "hair length",
	},
	{
		"organism": "people",
		"dominant": "a widow's peak",
		"recessive": "a straight hairline",
		"trait": "hairline shape",
	},
	{
		"organism": "pea plants",
		"dominant": "round seeds",
		"recessive": "wrinkled seeds",
		"trait": "seed shape",
	},
	{
		"organism": "mice",
		"dominant": "black fur",
		"recessive": "brown fur",
		"trait": "fur color",
	},
]

GENOTYPES = ("AA", "Aa", "aa")

# Built and shuffled once per run; each question uses one scenario without cycling.
SCENARIOS: list[tuple] = []


#=====================
def gametes_for_genotype(genotype: str) -> tuple:
	if genotype == "AA":
		return ("A", "A")
	if genotype == "aa":
		return ("a", "a")
	return ("A", "a")


#=====================
def phenotype_for_genotype(genotype: str, trait: dict) -> str:
	if "A" in genotype:
		return trait["dominant"]
	return trait["recessive"]


#=====================
def offspring_ratio(parent_one: str, parent_two: str) -> tuple:
	offspring = []
	for g1 in gametes_for_genotype(parent_one):
		for g2 in gametes_for_genotype(parent_two):
			offspring.append("".join(sorted([g1, g2], reverse=True)))
	dominant = sum(1 for g in offspring if "A" in g)
	recessive = len(offspring) - dominant
	return dominant, recessive


#=====================
def build_scenarios() -> list[tuple]:
	scenarios = []
	for trait in TRAITS:
		for known_genotype in ("Aa", "aa"):
			candidates = {
				genotype: offspring_ratio(known_genotype, genotype) for genotype in GENOTYPES
			}
			for unknown_genotype, ratio in candidates.items():
				# The observed ratio must identify exactly one unknown genotype.
				if list(candidates.values()).count(ratio) != 1:
					continue
				for litter_size in (12, 24):
					scenarios.append((trait, known_genotype, unknown_genotype, ratio, litter_size))
	return scenarios


#=====================
def parent_description(genotype: str, trait: dict) -> str:
	phenotype = phenotype_for_genotype(genotype, trait)
	text = f"{phenotype}; genotype <strong>{genotype}</strong>"
	return text


#=====================
def offspring_table(trait: dict, dominant_count: int, recessive_count: int) -> str:
	cell_style = "border: 1px solid #737373; padding: 8px 12px; color: #202020;"
	text = "<table style='border-collapse: collapse; margin: 12px 0;'>"
	text += "<caption><strong>Offspring</strong> (one symbol = one offspring)</caption>"
	text += f"<tr><th scope='col' style='{cell_style}'>Trait</th>"
	text += f"<th scope='col' style='{cell_style}'>Number</th>"
	text += f"<th scope='col' style='{cell_style}'>Offspring shown</th></tr>"
	rows = (
		(trait["dominant"], dominant_count, "#e2eef9", "#245b88", "&#9679;"),
		(trait["recessive"], recessive_count, "#fff0d5", "#805000", "&#9632;"),
	)
	for phenotype, count, background, color, symbol in rows:
		style = f"{cell_style} background-color: {background};"
		text += f"<tr><th scope='row' style='{style}'>{phenotype}</th>"
		text += f"<td style='{style}'>{count}</td>"
		# Shape and written counts preserve the information without color.
		symbols = " ".join([symbol] * count) if count else "None"
		text += f"<td style='{style}'>"
		text += f"<span aria-hidden='true' style='color: {color}; font-size: 22px;'>"
		text += f"{symbols}</span></td></tr>"
	text += "</table>"
	return text


#=====================
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	trait, known_genotype, unknown_genotype, ratio, litter_size = SCENARIOS[N - 1]
	dominant_count = litter_size * ratio[0] // 4
	recessive_count = litter_size * ratio[1] // 4

	known_parent = parent_description(known_genotype, trait)
	question_text = f"<p>Two {trait['organism']} produce {litter_size} offspring.</p>"
	question_text += f"<p>A is dominant to a: AA and Aa have {trait['dominant']}; "
	question_text += f"aa has {trait['recessive']}.</p>"
	question_text += "<p>"
	question_text += f"<strong>Parent 1:</strong> {known_parent}<br/>"
	question_text += "<strong>Parent 2:</strong> genotype unknown</p>"
	question_text += offspring_table(trait, dominant_count, recessive_count)
	question_text += (
		"<p>These counts match the expected ratio for the cross.</p>"
		"<p>What is the genotype of Parent 2?</p>"
	)

	choices_list = [
		bptools.html_monospace("AA"),
		bptools.html_monospace("Aa"),
		bptools.html_monospace("aa"),
		"There is not enough information to tell",
	]
	random.shuffle(choices_list)
	answer_text = bptools.html_monospace(unknown_genotype)
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
