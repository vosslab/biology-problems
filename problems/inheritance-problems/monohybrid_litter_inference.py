#!/usr/bin/env python3

import sys
import math
import random
import argparse

import bptools


# MC inference from exact Mendelian ratios; shared BBQ/export and anti-cheat helpers.
# Shuffle scenarios once per run; random clear letters keep the natural genotype choice order.
# Example: Aa x unknown, 18 round : 6 wrinkled (3:1), identifies Aa.
TRAITS = [
	{
		"organism": "cat",
		"phenotype_verb": "is",
		"dominant": "short hair",
		"recessive": "long hair",
		"trait": "hair length",
	},
	{
		"organism": "person",
		"phenotype_verb": "is",
		"dominant": "a widow's peak",
		"recessive": "a straight hairline",
		"trait": "hairline shape",
	},
	{
		"organism": "pea plant",
		"phenotype_verb": "are",
		"dominant": "round seeds",
		"recessive": "wrinkled seeds",
		"trait": "seed shape",
	},
	{
		"organism": "mouse",
		"phenotype_verb": "is",
		"dominant": "black fur",
		"recessive": "brown fur",
		"trait": "fur color",
	},
]

GENOTYPES = {
	"AA": "homozygous dominant",
	"Aa": "heterozygous",
	"aa": "homozygous recessive",
}

# Built and shuffled once per run; each question uses one scenario without cycling.
SCENARIOS: list[tuple] = []


#=====================
def genotype_text(genotype: str, gene_letter: str) -> str:
	# Keep allele letters at the surrounding text size in browser previews.
	display_genotype = genotype.replace("A", gene_letter.upper()).replace("a", gene_letter)
	text = '<span style="font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 1em;">'
	text += f"{display_genotype}</span>"
	return text


#=====================
def choice_text(genotype: str, gene_letter: str) -> str:
	text = f"{genotype_text(genotype, gene_letter)} ({GENOTYPES[genotype]})"
	return text


#=====================
def gametes_for_genotype(genotype: str) -> tuple:
	if genotype == "AA":
		return ("A", "A")
	if genotype == "aa":
		return ("a", "a")
	return ("A", "a")


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
def offspring_table(
		trait: dict, dominant_count: int, recessive_count: int, gene_letter: str) -> str:
	cell_style = "padding: 4px 10px; text-align: left; color: #202020;"
	text = '<table style="border-collapse: collapse; border: 1px solid #b8b8b8; '
	text += 'margin: 0 0 12px; max-width: 100%;">'
	text += f'<tr><th scope="col" style="{cell_style}">Offspring phenotype</th>'
	text += f'<th scope="col" style="{cell_style}">Genotype</th>'
	text += f'<th scope="col" style="{cell_style}">Observed</th></tr>'
	rows = (
		(trait["dominant"], "A_", dominant_count, "#f4f8fb", "#245b88", "&#9679;"),
		(trait["recessive"], "aa", recessive_count, "#fdf8ef", "#805000", "&#9632;"),
	)
	for phenotype, genotype, count, background, color, symbol in rows:
		style = f"{cell_style} background-color: {background};"
		text += f'<tr><th scope="row" style="{style} font-weight: normal;">{phenotype}</th>'
		text += f'<td style="{style}">{genotype_text(genotype, gene_letter)}</td>'
		text += f'<td style="{style}">'
		# Shapes and written counts preserve the observation without color.
		if count:
			symbols = " ".join([symbol] * count)
			text += f'<span aria-hidden="true" style="color: {color}; font-size: 14px;">'
			text += f"{symbols}</span> &nbsp; "
		text += f"<strong>{count}</strong></td></tr>"
	text += "</table>"
	return text


#=====================
def write_question(N: int, args: argparse.Namespace) -> object | None:
	if N > len(SCENARIOS):
		return None
	trait, known_genotype, unknown_genotype, ratio, litter_size = SCENARIOS[N - 1]
	dominant_count = litter_size * ratio[0] // 4
	recessive_count = litter_size * ratio[1] // 4

	# These pairs have distinct case shapes; avoid lookalikes such as C/c and X/x.
	gene_letter = random.choice("bdefhnrt")
	known_parent = genotype_text(known_genotype, gene_letter)
	dominant_allele = genotype_text("A", gene_letter)
	recessive_allele = genotype_text("a", gene_letter)
	dominant_genotype = genotype_text("A_", gene_letter)
	recessive_genotype = genotype_text("aa", gene_letter)
	question_text = offspring_table(trait, dominant_count, recessive_count, gene_letter)
	# Each sentence has one job: setup, experiment, result, conclusion.
	verb = trait["phenotype_verb"]
	question_text += '<p style="margin: 0 0 1.5em;">'
	question_text += f"{dominant_allele} is dominant to {recessive_allele}, so "
	question_text += f"{trait['dominant']} {verb} {dominant_genotype} and "
	question_text += f"{trait['recessive']} {verb} {recessive_genotype}.</p>"
	# Group the experiment, result, and conclusion on consecutive lines.
	question_text += '<p style="margin: 0;">'
	question_text += f"A {trait['organism']} (<strong>Parent 1</strong>) with genotype "
	question_text += f"{known_parent} is crossed with a second {trait['organism']} "
	question_text += "(<strong>Parent 2</strong>) of unknown genotype.<br/>"
	if dominant_count == 0:
		question_text += f"The offspring above all have {trait['recessive']}.<br/>"
	elif recessive_count == 0:
		question_text += f"The offspring above all have {trait['dominant']}.<br/>"
	else:
		divisor = math.gcd(*ratio)
		ratio_text = f"{ratio[0] // divisor}:{ratio[1] // divisor}"
		question_text += f"The offspring above show a <strong>{ratio_text}</strong> "
		question_text += "phenotypic ratio.<br/>"
	question_text += "Which genotype for <strong>Parent 2</strong> would produce "
	question_text += "this offspring ratio given that <strong>Parent 1</strong> is "
	question_text += f"{known_parent}?</p>"

	choices_list = [choice_text(genotype, gene_letter) for genotype in GENOTYPES]
	answer_text = choice_text(unknown_genotype, gene_letter)
	bb_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	return bb_question


#===========================================================
def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(description="Infer a parent's genotype from offspring ratios.")
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
