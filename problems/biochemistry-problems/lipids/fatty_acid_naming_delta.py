#!/usr/bin/env python3

"""
Multiple-choice generator: show an unsaturated fatty-acid skeleton (ASCII
art) and ask the student for the correct Delta notation describing the
positions of the cis double bonds.

Mirrors the PGML version `fatty_acid_naming_delta.pgml`. Chain length
16-22, 2 or 3 cis double bonds placed by pool elimination with minimum
spacing of 3 (no conjugated dienes).
"""

# Standard Library
import random

# local repo modules
import bptools
import fatty_acid_lib

#============================================
def build_choices(chain_length: int, omegas: list) -> tuple:
	"""
	Build the list of MC choices and the answer string.

	Distractors mirror the omega variant but with the Delta label:
	- correct: Delta-positions list
	- wrong-end: omega-positions (= chain_length - delta for each)
	- shift-up / shift-down: off-by-one shifts on each list
	- just-count: trivial 1,2,3,... pattern
	"""
	# Convert omegas to deltas (sorted ascending)
	deltas = sorted([chain_length - omega for omega in omegas])
	# Off-by-one shift distractors built from each list
	n_items = len(omegas)
	bad_omegas = [omegas[i] + (n_items - 1 - i) for i in range(n_items)]
	bad_deltas = [deltas[i] + (n_items - 1 - i) for i in range(n_items)]
	just_count = [i + 1 for i in range(n_items)]
	# Build HTML for each choice
	correct = fatty_acid_lib.format_delta_html(deltas)
	wrong_swap = fatty_acid_lib.format_delta_html(omegas)
	wrong_bad_omega = fatty_acid_lib.format_delta_html(bad_omegas)
	wrong_bad_delta = fatty_acid_lib.format_delta_html(bad_deltas)
	wrong_just_count = fatty_acid_lib.format_delta_html(just_count)
	# Deduplicate while preserving the correct answer at the front
	seen = set()
	choices = []
	for choice in (correct, wrong_swap, wrong_bad_omega, wrong_bad_delta, wrong_just_count):
		if choice in seen:
			continue
		seen.add(choice)
		choices.append(choice)
	random.shuffle(choices)
	return choices, correct


#============================================
def write_question(N: int, args) -> str:
	"""
	Generate one Delta-notation MC question.
	"""
	chain_length = random.randint(16, 22)
	num_double_bonds = random.randint(2, 3)
	# Pool-eliminate scattered omega positions; we'll display as Delta
	omegas = fatty_acid_lib.pool_eliminate_positions(chain_length, num_double_bonds)
	if len(omegas) < 2:
		return None
	# Render the chain (rendering uses bond indices, which are the same
	# physical positions regardless of which numbering system labels them)
	bond_indices = fatty_acid_lib.omegas_to_bond_indices(omegas)
	chain_html = fatty_acid_lib.render_fatty_acid_ascii(chain_length, bond_indices)
	# Compose question stem
	question_text = ''
	question_text += '<p>' + chain_html + '</p>'
	question_text += '<p>The skeletal structure above shows an unsaturated fatty acid '
	question_text += f'with {chain_length} carbons. The methyl end is on the left '
	question_text += '(H<sub>3</sub>C) and the carboxyl end (COOH) is on the right. '
	question_text += 'Each vertex and line end represents one carbon atom. '
	question_text += '<b>&Delta; (Delta)</b> notation counts carbons from the COOH end '
	question_text += '(carbon 1).</p>'
	question_text += '<p>What is the correct <b>&Delta; (Delta)</b> notation '
	question_text += 'describing the positions of the double bonds in this '
	question_text += f'{chain_length}-carbon fatty acid?</p>'
	choices, answer = build_choices(chain_length, omegas)
	if len(choices) < 4:
		return None
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices, answer)
	return complete_question


#============================================
def parse_arguments():
	"""
	Parse command-line arguments.
	"""
	parser = bptools.make_arg_parser(
		description='Generate fatty acid Delta-notation MC questions (read structure, pick notation).'
	)
	args = parser.parse_args()
	return args


#============================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
