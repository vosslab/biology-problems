#!/usr/bin/env python3

"""
Multiple-choice generator: show an omega notation (e.g., omega-3,12,17)
and ask the student to pick the correct fatty-acid skeletal structure
from four ASCII-art choices.

Mirrors the PGML version `fatty_acid_match_omega.pgml`. Distractors
include a wrong-end misread (counted from COOH instead of methyl), two
off-by-one shifts, and two random-scatter backups so we always end up
with four distinct structures even when palindromic positions cause the
mirror distractor to collide with the correct answer.
"""

# Standard Library
import random

# local repo modules
import bptools
import fatty_acid_lib

#============================================
def build_choice_html(chain_length: int, bond_indices) -> str:
	"""
	Build a single MC choice: the ASCII-art chain wrapped in a bordered
	div so the structure stays visually grouped with its A/B/C/D label.
	"""
	chain = fatty_acid_lib.render_fatty_acid_ascii(chain_length, bond_indices)
	# Bordered card so the SVG-equivalent ASCII chain reads as a single
	# unit attached to its radio-button letter.
	html = ''
	html += '<div style="display:inline-block; padding:6px 10px;'
	html += ' margin:4px 0; border:1px solid #c8c8c8; border-radius:4px;'
	html += ' background:#fafafa;">'
	html += chain
	html += '</div>'
	return html


#============================================
def build_choices(chain_length: int, omegas: list) -> tuple:
	"""
	Return (choices, answer) where choices is a deduplicated list of HTML
	strings (one ASCII-art structure per choice) and answer is the
	correct one.

	Candidate distractors in priority order:
	1. correct: bond indices = omega - 1
	2. wrong-end misread: bond indices = chain_length - omega - 1
	   (student counted from COOH instead of methyl end)
	3. shift +1: bond indices = omega (off by one toward COOH)
	4. shift -1: bond indices = omega - 2 (off by one toward methyl)
	5. scatter A: alternative valid scattered placement
	6. scatter B: second alternative
	The first four unique CSV signatures become the four MC choices.
	"""
	correct_bonds = fatty_acid_lib.omegas_to_bond_indices(omegas)
	# Wrong-end misread: bond indices when counted from the wrong end.
	misread_bonds = [chain_length - omega - 1 for omega in omegas]
	misread_bonds.sort()
	# Off-by-one shifts (return [] if any shifted index is out of range)
	shift_p1_bonds = fatty_acid_lib.shift_bond_indices(correct_bonds, 1, chain_length)
	shift_m1_bonds = fatty_acid_lib.shift_bond_indices(correct_bonds, -1, chain_length)
	# Random alternative scatters (backup distractors)
	scatter_a_omegas = fatty_acid_lib.pool_eliminate_positions(chain_length, len(omegas))
	scatter_b_omegas = fatty_acid_lib.pool_eliminate_positions(chain_length, len(omegas))
	scatter_a_bonds = fatty_acid_lib.omegas_to_bond_indices(scatter_a_omegas)
	scatter_b_bonds = fatty_acid_lib.omegas_to_bond_indices(scatter_b_omegas)
	# Walk candidates in priority order, keep first 4 unique by CSV
	candidates = [
		correct_bonds,
		misread_bonds,
		shift_p1_bonds,
		shift_m1_bonds,
		scatter_a_bonds,
		scatter_b_bonds,
	]
	seen = set()
	chosen = []
	for cand in candidates:
		if not cand:
			continue
		key = ','.join(str(b) for b in cand)
		if key in seen:
			continue
		seen.add(key)
		chosen.append(cand)
		if len(chosen) >= 4:
			break
	# Build the HTML choices
	correct_html = build_choice_html(chain_length, correct_bonds)
	choices = [build_choice_html(chain_length, c) for c in chosen]
	# Shuffle so the correct answer is not always first
	random.shuffle(choices)
	return choices, correct_html


#============================================
def write_question(N: int, args) -> str:
	"""
	Generate one match-omega-to-structure MC question.
	"""
	chain_length = random.randint(16, 22)
	num_double_bonds = random.randint(2, 3)
	omegas = fatty_acid_lib.pool_eliminate_positions(chain_length, num_double_bonds)
	if len(omegas) < 2:
		return None
	# Compose question stem
	omega_html = fatty_acid_lib.format_omega_html(omegas)
	question_text = ''
	question_text += f'<p>A polyunsaturated fatty acid with {chain_length} carbons '
	question_text += f'is described by the notation {omega_html}. Each candidate '
	question_text += 'structure below shows a skeletal zigzag with the methyl end on '
	question_text += 'the left (H<sub>3</sub>C) and the carboxyl end on the right '
	question_text += '(COOH); each vertex and line end represents one carbon atom.</p>'
	question_text += f'<p>Which structure correctly matches the {omega_html} notation?</p>'
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
		description='Generate fatty acid match-omega MC questions (read notation, pick structure).'
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
