#!/usr/bin/env python3
"""Generate an ordered-list question about model-system organization.

Authoring contract:
- Family: ordered list (ORD); output: Blackboard BBQ text upload.
- Each instance samples the requested number of levels and one organism per level.
- Category names are internal; students see only the organism names and question stem.
- An optional --seed reproduces the same selected levels and organisms.
- Blackboard randomizes displayed order; the answer follows the seven-level ladder.
- Shared anti-cheat options are available and applied by the bptools collector.
- Example: lambda phage, E. coli, C. elegans, zebrafish, then mouse. Incorrect
  orders might place E. coli before lambda phage or mouse before zebrafish.
"""

import random

import bptools


MODEL_SYSTEM_LEVELS = {
	# Dictionary order defines the increasing-complexity sequence.
	"Viruses": [
		"Lambda phage (bacteriophage)",
		"Tobacco mosaic virus (plant virus)",
	],
	"Bacteria": [
		"Escherichia coli (bacterium)",
		"Photosynthetic cyanobacteria (bacteria)",
	],
	"Single-celled eukaryotes": [
		"Saccharomyces cerevisiae (yeast)",
		"Tetrahymena thermophila (ciliate)",
		"Chlamydomonas reinhardtii (green alga)",
	],
	"Multicellular organisms without a centralized brain": [
		"Caenorhabditis elegans (nematode)",
	],
	"Animals with simple brains": [
		"Drosophila melanogaster (fruit fly)",
		"Danio rerio (zebrafish)",
	],
	"Non-primate mammals": [
		"Mus musculus (mouse)",
		"Rattus norvegicus (rat)",
		"Oryctolagus cuniculus domesticus (rabbit)",
	],
	"Primates": [
		"Rhesus macaque (primate)",
	],
}
MODEL_SYSTEM_CATEGORIES = list(MODEL_SYSTEM_LEVELS.keys())

MIN_CHOICES = 3
MAX_CHOICES = len(MODEL_SYSTEM_CATEGORIES)


def get_question_text() -> str:
	"""Return the prompt for the ordering question."""
	question_text = "Arrange the following model organisms from least to most complex."
	return question_text


def write_question(N: int, args) -> str:
	"""Create one formatted ordered-list question."""
	question_text = get_question_text()
	available_categories = MODEL_SYSTEM_CATEGORIES.copy()
	selected_categories = []
	for _ in range(args.num_choices):
		category = random.choice(available_categories)
		selected_categories.append(category)
		available_categories.remove(category)
	selected_categories.sort(key=MODEL_SYSTEM_CATEGORIES.index)
	ordered_answers_list = []
	for category in selected_categories:
		organism = random.choice(MODEL_SYSTEM_LEVELS[category])
		ordered_answers_list.append(organism)
	complete_question = bptools.formatBB_ORD_Question(
		N,
		question_text,
		ordered_answers_list,
	)
	return complete_question


def parse_arguments():
	"""Parse the standard bptools options for ordering questions."""
	parser = bptools.make_arg_parser(
		description="Generate model-organism complexity ordering questions."
	)
	parser = bptools.add_choice_args(parser, default=5)
	parser.add_argument(
		"--seed",
		dest="seed",
		type=int,
		default=None,
		help="Seed random organism and level selection for reproducibility.",
	)
	args = parser.parse_args()
	if args.num_choices < MIN_CHOICES or args.num_choices > MAX_CHOICES:
		parser.error(f"--num-choices must be between {MIN_CHOICES} and {MAX_CHOICES}.")
	return args


def main():
	"""Generate the BBQ text file."""
	args = parse_arguments()
	if args.seed is not None:
		random.seed(args.seed)
	outfile = bptools.make_outfile("ORD", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
