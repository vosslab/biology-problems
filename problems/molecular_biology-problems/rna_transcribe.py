#!/usr/bin/env python3
"""Generate MC or FIB RNA transcription questions with optional prime labels.

Questions use fresh random scenarios and the standard bptools BBQ/export pipeline.
Shared anti-cheat defaults apply; fixed random seeds are for verification only.
"""

# Standard Library
import argparse

# local repo modules
import bptools
import rna_transcribe_lib


#============================================
def write_question(N: int, args: argparse.Namespace) -> object:
	"""Delegate one question to the shared transcription generator."""
	question = rna_transcribe_lib.generate_question(
		N, args.sequence_len, args.question_type, args.direction_mode, args.num_choices)
	return question


#============================================
def parse_arguments() -> argparse.Namespace:
	"""Parse question format, direction mode, and standard generator options."""
	parser = bptools.make_arg_parser(description=__doc__)
	format_group = parser.add_mutually_exclusive_group(required=True)
	format_group.add_argument('-m', '--mc', dest='question_type',
		action='store_const', const='mc', help='Generate multiple-choice questions.')
	format_group.add_argument('-f', '--fib', dest='question_type',
		action='store_const', const='fib', help='Generate fill-in-the-blank questions.')
	bptools.add_choice_args(parser, default=5)
	direction_group = parser.add_mutually_exclusive_group(required=True)
	direction_group.add_argument('-D', '--directionless', dest='direction_mode',
		action='store_const', const='directionless', help='Omit prime labels; align left-to-right.')
	direction_group.add_argument('-p', '--prime', dest='direction_mode',
		action='store_const', const='prime', help="Include 5' and 3' direction labels.")
	parser.add_argument('-s', '--sequence-length', '--seqlen', dest='sequence_len',
		type=int, default=9, help='Length of the DNA sequence (at least 2; default: 9).')
	args = parser.parse_args()
	# ASVS 2.2.1: validate sequence length and the supported MC choice count.
	if args.sequence_len < 2:
		parser.error('--sequence-length must be at least 2')
	if args.question_type == 'mc' and not 2 <= args.num_choices <= 5:
		parser.error('--num-choices must be between 2 and 5 for MC questions')
	return args


#============================================
def main() -> None:
	"""Generate and save a bank named for its format, direction, and length."""
	args = parse_arguments()
	outfile = bptools.make_outfile(
		args.question_type.upper(), args.direction_mode, f'len_{args.sequence_len}')
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
