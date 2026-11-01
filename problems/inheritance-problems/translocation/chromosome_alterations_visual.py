#!/usr/bin/env python3
"""Analyze gene order to identify deletion, duplication, inversion, and translocation.

One randomized pair of schematic chromosomes supplies matching and both MC directions.
Distractors confuse loss, extra copies, reversed order, exchange, or an unchanged sequence.
Letter order carries the answer; texture is decorative.
Imitate the data-first, shared-figure question pattern in QUESTION_EXEMPLARS.md.
Standard bptools export and anti-cheat defaults apply.
"""

import argparse
import dataclasses
import random
import string

import bptools
import translocationlib


@dataclasses.dataclass(frozen=True)
class Chromosome:
	"""Retain ordered regions, source colors, and rearrangement joins."""
	p: str
	color: str
	q: tuple[tuple[str, str], ...]
	junctions: tuple[int, ...] = ()


ChromosomePair = tuple[Chromosome, Chromosome]
ALTERATIONS = {
	'del': ('Deletion', '#CC0066'),
	'dup': ('Duplication', '#007A00'),
	'inv': ('Inversion', '#935D00'),
	't': ('Translocation', '#0067CC'),
}


def make_alterations(originals: ChromosomePair, start: int, stop: int,
		exchange1: int, exchange2: int) -> dict[str, ChromosomePair]:
	"""Make four distinct events while retaining centromeres and original end regions."""
	first, second = originals
	prefix, block, suffix = first.q[:start], first.q[start:stop], first.q[stop:]
	# Keep tandem copies short while deletions and inversions affect larger blocks.
	duplicated = first.q[start:start + 2]
	outcomes = {
		'del': (dataclasses.replace(first, q=prefix + suffix, junctions=(start,)), second),
		'dup': (dataclasses.replace(first, q=prefix + duplicated + first.q[start:],
			junctions=(start + 2,)), second),
		'inv': (dataclasses.replace(first, q=prefix + block[::-1] + suffix,
			junctions=(start, stop)), second),
		't': (
			dataclasses.replace(first, q=first.q[:exchange1] + second.q[exchange2:],
				junctions=(exchange1,)),
			dataclasses.replace(second, q=second.q[:exchange2] + first.q[exchange1:],
				junctions=(exchange2,)),
		),
	}
	return outcomes


def generate_scenario() -> tuple[ChromosomePair, dict[str, ChromosomePair]]:
	"""Use consecutive source letters and randomized affected regions and light colors."""
	arm_sizes = [(p, q) for p in range(2, 6) for q in range(max(4, p + 1), 12)]
	# Three affected genes need one retained region on each side of the event.
	first_sizes = random.choice([sizes for sizes in arm_sizes if sizes[1] >= 5])
	# Keep distinct A-Z labels across the two originals.
	second_sizes = random.choice([sizes for sizes in arm_sizes
		if sum(first_sizes) + sum(sizes) <= len(string.ascii_uppercase)])
	lengths = (first_sizes, second_sizes)
	total_genes = sum(p_length + q_length for p_length, q_length in lengths)
	first_letter = random.randrange(len(string.ascii_uppercase) - total_genes + 1)
	letters = string.ascii_uppercase[first_letter:first_letter + total_genes]
	colors = bptools.default_color_wheel(2, my_color_wheel=bptools.light_color_wheel)
	random.shuffle(colors)
	chromosomes = []
	offset = 0
	for (p_length, q_length), color in zip(lengths, colors):
		sequence = letters[offset:offset + p_length + q_length]
		fill = f'#{color}'
		q_genes = tuple((gene, fill) for gene in sequence[p_length:])
		chromosomes.append(Chromosome(sequence[:p_length], fill, q_genes))
		offset += len(sequence)
	originals = (chromosomes[0], chromosomes[1])
	block_length = random.randint(3, len(originals[0].q) - 2)
	start = random.randint(1, len(originals[0].q) - block_length - 1)
	stop = start + block_length
	outcomes = make_alterations(originals, start, stop,
		len(originals[0].q) - random.choice((2, 3)),
		len(originals[1].q) - random.choice((2, 3)))
	return originals, outcomes


def draw_chromosomes(chromosomes: tuple[Chromosome, ...], label: str = '') -> str:
	"""Keep the displayed chromosomes inside the existing rounded answer frame."""
	diagrams = [translocationlib.draw_labeled_chromosome(
		chromosome.p, chromosome.color, chromosome.q, chromosome.junctions)
		for chromosome in chromosomes]
	# Separate chromosome tables export as images with their own text alternatives.
	markup = '<div style="display: inline-block; border: 1px solid #adb5bd; '
	markup += 'border-radius: 8px; color: #000; background-color: #fff;">'
	contents = [label, *diagrams] if label else diagrams
	markup += ''.join(f'<div style="padding: 8px;">{content}</div>' for content in contents)
	markup += '</div>'
	return markup


def format_alteration(code: str) -> str:
	"""Use full names with the instructor's fixed text colors."""
	name, color = ALTERATIONS[code]
	markup = '<span style="font-size: 14px; font-weight: bold; white-space: nowrap; '
	markup += f'color: {color}; background-color: #fff;">{name}</span>'
	return markup


def write_question(N: int, args: argparse.Namespace) -> object:
	originals, outcomes = generate_scenario()
	terms = {code: format_alteration(code) for code in ALTERATIONS}
	target = random.choice(tuple(ALTERATIONS)) if args.question_type == 'mc' else None
	show_both = args.always_two or target in (None, 't')
	visible_originals = originals if show_both else originals[:1]
	label = 'Original chromosomes' if show_both else 'Original chromosome'
	question = draw_chromosomes(visible_originals, label)
	question += '<p>Letters mark ordered regions on schematic chromosomes; '
	question += 'collars mark centromeres. White zigzags mark rearrangement junctions.</p>'
	if args.question_type == 'matching':
		question += '<p>Match each chromosome alteration with its corresponding arrangement. '
		question += 'Each choice is used exactly once.</p>'
		codes = list(ALTERATIONS)
		random.shuffle(codes)
		diagrams = [draw_chromosomes(outcomes[code]) for code in codes]
		item = bptools.formatBB_MAT_Question(N, question,
			[terms[code] for code in codes], diagrams)
	else:
		if args.flip:
			question += '<p>Which one of the following arrangements represents '
			question += f'{terms[target]}?</p>'
			possibilities = dict(outcomes)
			if not show_both:
				# With one source chromosome, use its unchanged sequence as the fourth option.
				possibilities.pop('t')
				possibilities['unchanged'] = originals
			codes = list(possibilities)
			random.shuffle(codes)
			diagrams = {code: draw_chromosomes(pair if show_both else pair[:1])
				for code, pair in possibilities.items()}
			choices = [diagrams[code] for code in codes]
			answer = diagrams[target]
		else:
			altered = outcomes[target] if show_both else outcomes[target][:1]
			question += draw_chromosomes(altered, 'After rearrangement')
			question += '<p>Which one of the following chromosome alterations describes '
			question += 'this rearrangement?</p>'
			choices = [terms[code] for code in ALTERATIONS]
			answer = terms[target]
		item = bptools.formatBB_MC_Question(N, question, choices, answer)
	return item


def parse_arguments() -> argparse.Namespace:
	parser = bptools.make_arg_parser(description='Identify chromosome alterations from diagrams.')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--matching', dest='question_type', action='store_const',
		const='matching', help='Match all four alteration names to diagrams (default).')
	group.add_argument('--mc', dest='question_type', action='store_const',
		const='mc', help='Name the alteration in a rearranged chromosome diagram.')
	parser.set_defaults(question_type='matching')
	parser.add_argument('--flip', action='store_true',
		help='With --mc, choose a diagram for the named alteration.')
	parser.add_argument('--always-two', action='store_true',
		help='With --mc, keep both chromosomes visible for every alteration.')
	args = parser.parse_args()
	if args.flip and args.question_type != 'mc':
		parser.error('--flip requires --mc')
	return args


def main() -> None:
	args = parse_arguments()
	mode = 'matching' if args.question_type == 'matching' else 'which_one'
	outfile = bptools.make_outfile(mode, 'flipped' if args.flip else None,
		'two_chromosomes' if args.always_two and args.question_type == 'mc' else None)
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
