#!/usr/bin/env python3
"""Generate an ordered-list question for an environmental 16S rDNA survey.

Authoring contract:
- Family: ordered list (ORD) or multiple choice (MC); output: Blackboard BBQ.
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
	if args.mc:
		return write_mc_question(N, ordered_answers_list)
	complete_question = bptools.formatBB_ORD_Question(
		N,
		question_text,
		ordered_answers_list,
	)
	return complete_question


def write_mc_question(N: int, ordered_steps: list[str]):
	"""Ask for the same workflow using numbered steps and four sequences."""
	displayed_steps = random.sample(ordered_steps, len(ordered_steps))
	correct_order = [displayed_steps.index(step) + 1 for step in ordered_steps]
	wrong_orders = []
	# Error: two neighboring stages are done in the wrong order.
	for index in range(len(correct_order) - 1):
		wrong_order = correct_order.copy()
		wrong_order[index:index + 2] = reversed(wrong_order[index:index + 2])
		wrong_orders.append(wrong_order)
	# Error: the workflow is read from last to first; also supports three-step items.
	wrong_orders.append(list(reversed(correct_order)))
	format_order = lambda order: " &rarr; ".join(str(number) for number in order)
	answer = format_order(correct_order)
	choices = [answer] + [format_order(order) for order in random.sample(wrong_orders, 3)]
	random.shuffle(choices)
	step_list = "".join(f"<li>{step}</li>" for step in displayed_steps)
	question = (
		"<p>The steps of an environmental 16S rDNA survey are listed below.</p>"
		f"<ol>{step_list}</ol><p>Which sequence puts the steps in order from first to last?</p>"
	)
	return bptools.formatBB_MC_Question(N, question, choices, answer)


def parse_arguments():
	"""Parse the standard bptools options for ordering questions."""
	parser = bptools.make_arg_parser(
		description="Generate environmental 16S rDNA survey ordering questions."
	)
	parser = bptools.add_choice_args(parser, default=MAX_CHOICES)
	parser.add_argument(
		"-m", "--mc", action="store_true",
		help="Use four multiple-choice sequences; -c still sets the number of steps.",
	)
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
	if args.mc:
		outfile = bptools.make_outfile("MC", f"{args.num_choices}_steps")
	else:
		outfile = bptools.make_outfile("ORD", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
