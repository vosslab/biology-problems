#!/usr/bin/env python3

import random
from pathlib import Path

import bptools


PARENT_GENOTYPES = {
	"N/O; N/LP": (("N", "O"), ("N", "LP")),
	"N/O; N/N": (("N", "O"), ("N", "N")),
	"N/O; LP/LP": (("N", "O"), ("LP", "LP")),
	"N/N; N/LP": (("N", "N"), ("N", "LP")),
	"N/N; LP/LP": (("N", "N"), ("LP", "LP")),
	"N/N; N/N": (("N", "N"), ("N", "N")),
}

SCENARIOS = (
	("N/O; N/LP", "N/O; N/LP"),
	("N/O; N/LP", "N/O; N/N"),
	("N/O; N/LP", "N/O; LP/LP"),
	("N/O; N/LP", "N/N; N/LP"),
	("N/O; N/LP", "N/N; LP/LP"),
	("N/O; LP/LP", "N/N; N/LP"),
)

OUTCOME_LABELS = (
	("lethal", "O/O: lethal white; nonviable"),
	("fewspot", "Fewspot class"),
	("both", "Frame-overo and leopard-complex patterns"),
	("frame", "Frame-overo pattern only"),
	("leopard", "Leopard-complex pattern only"),
	("solid", "Neither modeled pattern"),
)


#========================================================
def format_genotype(alleles: tuple, allele_order: tuple) -> str:
	ordered_alleles = sorted(alleles, key=allele_order.index)
	return "/".join(ordered_alleles)


#========================================================
def label_parent_genotype(genotype: str) -> str:
	frame_genotype, leopard_genotype = genotype.split("; ")
	return (
		f"Frame-overo: {frame_genotype}; "
		f"Leopard complex: {leopard_genotype}"
	)


#========================================================
def make_gametes(genotype: tuple) -> list:
	frame_alleles, lp_alleles = genotype
	gametes = []
	for frame_allele in frame_alleles:
		for lp_allele in lp_alleles:
			gametes.append((frame_allele, lp_allele))
	return gametes


#========================================================
def classify_offspring(frame_genotype: str, lp_genotype: str) -> str:
	if frame_genotype == "O/O":
		return "lethal"
	if lp_genotype == "LP/LP":
		return "fewspot"
	if frame_genotype == "N/O" and lp_genotype == "N/LP":
		return "both"
	if frame_genotype == "N/O":
		return "frame"
	if lp_genotype == "N/LP":
		return "leopard"
	return "solid"


#========================================================
def offspring_profile(known_parent: str, unknown_parent: str) -> dict:
	known_gametes = make_gametes(PARENT_GENOTYPES[known_parent])
	unknown_gametes = make_gametes(PARENT_GENOTYPES[unknown_parent])
	profile = {outcome: 0 for outcome, _label in OUTCOME_LABELS}
	for known_gamete in known_gametes:
		for unknown_gamete in unknown_gametes:
			frame_genotype = format_genotype(
				(known_gamete[0], unknown_gamete[0]), ("N", "O")
			)
			lp_genotype = format_genotype(
				(known_gamete[1], unknown_gamete[1]), ("N", "LP")
			)
			outcome = classify_offspring(frame_genotype, lp_genotype)
			profile[outcome] += 1
	return profile


#========================================================
def make_offspring_table(profile: dict) -> str:
	rows = []
	cell_style = "border: 1px solid #666; padding: 6px 10px; text-align: left;"
	count_style = f"{cell_style} white-space: nowrap;"
	for outcome, label in OUTCOME_LABELS:
		rows.append(
			"<tr>"
			f"<td style='{cell_style}'>{label}</td>"
			f"<td style='{count_style}'>{profile[outcome]} of 16</td>"
			"</tr>"
		)
	return (
		"<table style='border-collapse: collapse;'>"
		"<thead><tr>"
		f"<th scope='col' style='{cell_style}'>Offspring class</th>"
		f"<th scope='col' style='{count_style}'>Count</th>"
		"</tr></thead>"
		"<tbody>"
		+ "".join(rows)
		+ "</tbody></table>"
	)


#========================================================
def make_question_text(scenario: tuple) -> str:
	known_parent, unknown_parent = scenario
	profile = offspring_profile(known_parent, unknown_parent)
	known_parent_labels = label_parent_genotype(known_parent)
	image_path = Path(__file__).resolve().with_name("horse_coat_patterns.png")
	image_src = image_path.relative_to(Path.cwd().resolve()).as_posix()

	question_text = (
		"<p>A Pintaloosa is a horse from a Pinto (or Paint) x Appaloosa cross. It may show "
		"either pattern system, both, or neither. These drawings show the five coats "
		"used in the table: neither modeled pattern, frame-overo, leopard-complex, "
		"fewspot, and Pintaloosa (both patterns). They do not diagnose a horse's genotype.</p>"
	)
	image_alt = (
		"Five representative horse coats: neither modeled pattern, frame-overo, "
		"leopard-complex, fewspot, and Pintaloosa with both patterns."
	)
	question_text += (
		f'<p><img src="{image_src}" width="1100" '
		f'style="max-width: 100%; height: auto;" alt="{image_alt}" /></p>'
	)
	question_text += (
		"<p>Use this two-locus teaching model. N is the non-pattern allele at both loci. "
		"At <em>EDNRB</em>, N/O produces a frame-overo pattern, while O/O causes "
		"lethal white syndrome and is nonviable.</p>"
	)
	question_text += (
		"<p>At <em>TRPM1</em>, N/N has no modeled leopard-complex spotting, N/LP is "
		"the leopard class, and this model treats LP/LP as the fewspot class. A living "
		"N/O; N/LP foal "
		"shows both modeled patterns. Assume independent assortment. Actual coat-pattern "
		"expression is more variable; LP/LP is associated with congenital stationary "
		"night blindness.</p>"
	)
	question_text += (
		f"<p>The mare's test results are <strong>{known_parent_labels}.</strong> "
		"The stallion's results are missing. The table gives expected outcomes from 16 conceptions, "
		"including any nonviable O/O foals.</p>"
	)
	question_text += make_offspring_table(profile)
	question_text += (
		"<p><strong>Hint:</strong> Start with the lethal-white count to see whether the stallion "
		"can pass an O allele. Then use the fewspot count, remembering that O/O foals are "
		"counted as lethal white.</p>"
	)
	question_text += (
		"<p><strong>Case question:</strong> Which stallion genotype can produce all "
		"six expected offspring counts?</p>"
	)
	question_text += (
		"<p>Sources: <a href='https://vgl.ucdavis.edu/test/lethal-white-overo'>"
		"UC Davis VGL frame-overo/LWO</a>; <a href='https://vgl.ucdavis.edu/test/leopard-complex'>"
		"UC Davis VGL Leopard Complex</a>; <a href='https://apha.com/registration/the-breed/'>"
		"American Paint Horse Association coat-pattern guide</a>.</p>"
	)
	return question_text


#========================================================
def make_choices(answer: str, num_choices: int) -> list:
	other_genotypes = [genotype for genotype in PARENT_GENOTYPES if genotype != answer]
	choices = [answer] + random.sample(other_genotypes, num_choices - 1)
	random.shuffle(choices)
	return choices


#========================================================
def write_question(N: int, args, scenario: tuple = None):
	if scenario is None:
		scenario = random.choice(SCENARIOS)
	unknown_parent = scenario[1]
	question_text = make_question_text(scenario)
	genotype_choices = make_choices(unknown_parent, args.num_choices)
	choices = [label_parent_genotype(genotype) for genotype in genotype_choices]
	answer_text = label_parent_genotype(unknown_parent)
	return bptools.formatBB_MC_Question(N, question_text, choices, answer_text)


#========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate horse coat-pattern genotype-inference questions."
	)
	parser = bptools.add_choice_args(parser, default=5)
	args = parser.parse_args()
	if args.num_choices < 2 or args.num_choices > len(PARENT_GENOTYPES):
		parser.error(f"--num-choices must be between 2 and {len(PARENT_GENOTYPES)}.")
	return args


#========================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#========================================================
if __name__ == '__main__':
	main()
