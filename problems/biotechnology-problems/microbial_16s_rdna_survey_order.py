#!/usr/bin/env python3
"""Generate an ordered-list question for an environmental 16S rDNA survey.

Authoring contract:
- Family: ordered list (ORD); output: Blackboard BBQ text upload.
- The full sequence has six steps, from sample collection through abundance graphs.
- A shorter question keeps a random subset of those steps in the same order.
- Blackboard randomizes the displayed order; the answer list is first to last.
- Shared anti-cheat options are available and applied by the bptools collector.
"""

import random

import bptools


SURVEY_STEPS = [
	"Microbial samples are collected from environment",
	"DNA extraction and quantification",
	"PCR amplification of the 16S rDNA genes",
	"Sequencing of the 16S rDNA genes",
	"Sequence clustering using bioinformatics",
	"Analyze bacterial relative abundance graphs",
]

MIN_CHOICES = 3
MAX_CHOICES = len(SURVEY_STEPS)


def get_question_text() -> str:
	"""Return the prompt for the ordering question."""
	question_text = (
		"Place the following steps of an environmental 16S rDNA survey "
		"in order from first to last."
	)
	return question_text


def write_question(N: int, args) -> str:
	"""Create one formatted ordered-list question."""
	question_text = get_question_text()
	available_indexes = list(range(len(SURVEY_STEPS)))
	selected_indexes = []
	for _ in range(args.num_choices):
		step_index = random.choice(available_indexes)
		selected_indexes.append(step_index)
		available_indexes.remove(step_index)
	selected_indexes.sort()
	ordered_answers_list = []
	for step_index in selected_indexes:
		ordered_answers_list.append(SURVEY_STEPS[step_index])
	complete_question = bptools.formatBB_ORD_Question(
		N,
		question_text,
		ordered_answers_list,
	)
	return complete_question


def parse_arguments():
	"""Parse the standard bptools options for ordering questions."""
	parser = bptools.make_arg_parser(
		description="Generate environmental 16S rDNA survey ordering questions."
	)
	parser = bptools.add_choice_args(parser, default=MAX_CHOICES)
	parser.add_argument(
		"--seed",
		dest="seed",
		type=int,
		default=None,
		help="Seed random step selection for reproducibility.",
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
