#!/usr/bin/env python3
"""Analyze fragment orientation in a visual, five-choice translocation puzzle.

Four options join broken ends correctly; the keyed option reverses a fragment.
Scenarios and choices are randomized with the standard bptools anti-cheat defaults.
"""

import argparse
import random

import bptools
import letter_translocation_problem_color as letter_model
import translocationlib


def draw_chromosome(chromosome: letter_model.Chromosome, *, source: bool = False) -> str:
	"""Render the model's actual fragment orientations and color identities."""
	left = chromosome.fragment1.text_formatted(
		telomere_first=not chromosome.telomere1_improper)
	right = chromosome.fragment2.text_formatted(
		telomere_first=chromosome.telomere2_improper)
	telomeres = ('right' if chromosome.telomere1_improper else 'left',
		'left' if chromosome.telomere2_improper else 'right')
	diagram = translocationlib.draw_sequence_chromosome(
		left, right, chromosome.fragment1.rgb_color, chromosome.fragment2.rgb_color,
		source=source, telomeres=telomeres)
	return diagram


def generate_choices(chromosome1: letter_model.Chromosome,
		chromosome2: letter_model.Chromosome) -> tuple[list[letter_model.Chromosome],
		letter_model.Chromosome]:
	"""Choose four valid derivatives and one orientation error using both chromosomes."""
	choices = letter_model.make_all_possible_translocations(chromosome1, chromosome2)
	first_fragments = (chromosome1.fragment1, chromosome1.fragment2)
	second_fragments = (chromosome2.fragment1, chromosome2.fragment2)
	# Keep both source chromosomes in the error so color alone cannot identify the key.
	improper = [candidate for candidate in
		letter_model.make_all_improper_translocations(chromosome1, chromosome2)
		if candidate.fragment1 in first_fragments and candidate.fragment2 in second_fragments]
	answer = random.choice(improper)
	choices.append(answer)
	random.shuffle(choices)
	return choices, answer


def get_question_text(chromosome1: letter_model.Chromosome,
		chromosome2: letter_model.Chromosome) -> str:
	"""Present the source chromosomes and the rule for reconnecting their broken ends."""
	question = ''
	for number, chromosome in enumerate((chromosome1, chromosome2), start=1):
		question += '<div style="color: #000; background-color: #fff; margin: 0 0 8px;">'
		question += f'<div style="font-size: 14px;">Chromosome {number}</div>'
		question += draw_chromosome(chromosome, source=True) + '</div>'
	question += '<p>Arrows mark the breaks; gray end caps mark the original telomeres. '
	question += 'The two nonhomologous chromosomes undergo a reciprocal translocation. '
	question += 'Only the broken ends reconnect, preserving gene order within each fragment.</p>'
	question += '<p>Which one of the following chromosome arrangements is '
	question += '<strong>NOT</strong> a possible product of this translocation?</p>'
	return question


def write_question(N: int, args: argparse.Namespace) -> object:
	chromosome1, chromosome2 = letter_model.make_chromosomes(
		args.min_chromosome_size, args.min_fragment_size)
	colors = bptools.default_color_wheel(4, my_color_wheel=bptools.light_color_wheel)
	random.shuffle(colors)
	fragments = (chromosome1.fragment1, chromosome1.fragment2,
		chromosome2.fragment1, chromosome2.fragment2)
	for fragment, color in zip(fragments, colors):
		fragment.rgb_color = f'#{color}'
	candidates, answer = generate_choices(chromosome1, chromosome2)
	choices = [translocationlib.format_gamete_choice('', [draw_chromosome(candidate)])
		for candidate in candidates]
	answer_text = choices[candidates.index(answer)]
	question = bptools.formatBB_MC_Question(
		N, get_question_text(chromosome1, chromosome2), choices, answer_text)
	return question


def parse_arguments() -> argparse.Namespace:
	args = letter_model.parse_arguments()
	# The shared Fragment model requires three genes, despite the older CLI's lower bound.
	if args.min_fragment_size < 3:
		raise ValueError('Use at least 3 genes per fragment for the visual translocation question.')
	return args


def main() -> None:
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
