#!/usr/bin/env python3

import random

import bptools

def make_choices_for_cycle(cycle_num: int, num_choices: int):
	if cycle_num < 2:
		amplicon_copies = 0
	else:
		amplicon_copies = 2**(cycle_num - 2)

	orig = int(cycle_num - num_choices + 1)
	for shift in range(5):
		start = orig + shift
		if start < -1:
			continue
		stop = start + num_choices
		if start > -1 and 2**start > amplicon_copies:
			continue

		choices_list = []
		answer_text = None
		for power in range(start, stop):
			value = 2**power
			if value < 1:
				value = 0
			if power >= 2:
				choice = "2<sup>{0:d}</sup> = {1:,d} complete copies".format(power, value)
			elif power == 1:
				choice = "two complete copies"
			elif power == 0:
				choice = "just one complete copy"
			elif power == -1:
				choice = "no copies are complete"
			choices_list.append(choice)
			if value == amplicon_copies:
				answer_text = choice
		return choices_list, answer_text
	return None, None

def write_question_batch(start_num: int, args) -> list:
	questions = []
	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return questions
	N = start_num
	for cycle_num in range(1, args.num_cycles + 1):
		question = ""
		question += "Starting with genomic DNA, how many copies of the double-stranded "
		question += f"amplicon of the exact length are there after {cycle_num} rounds of PCR?"
		choices_list, answer_text = make_choices_for_cycle(cycle_num, args.num_choices)
		if choices_list is None or answer_text is None:
			continue
		bb_question = bptools.formatBB_MC_Question(N, question, choices_list, answer_text)
		questions.append(bb_question)
		N += 1
		if remaining is not None and len(questions) >= remaining:
			return questions
	return questions

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate PCR amplicon copy count questions.",
		batch=True
	)
	parser = bptools.add_choice_args(parser, default=5)
	parser.add_argument(
		'-n', '--num-cycles', dest='num_cycles', type=int,
		default=30, help='Number of PCR cycles to include.'
	)
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)
