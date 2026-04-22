#!/usr/bin/env python3

"""
Multiple-choice generator: show a Delta notation (e.g., Delta-9,12,15)
and ask the student to pick the correct fatty-acid skeletal structure
from four ASCII-art choices.

Mirrors the PGML version `fatty_acid_match_delta.pgml`. Distractors:
wrong-end misread (counted from methyl instead of COOH), two off-by-one
shifts, and two random-scatter backups so we always end up with four
distinct structures even when palindromic positions cause the mirror
distractor to collide with the correct answer.
"""

# Standard Library
import random

# local repo modules
import bptools
import fatty_acid_lib

#============================================
def build_choice_html(chain_length: int, bond_indices) -> str:
	"""
	Build a single MC choice: ASCII-art chain wrapped in a bordered div
	so the structure stays visually grouped with its A/B/C/D label.
	"""
	chain = fatty_acid_lib.render_fatty_acid_ascii(chain_length, bond_indices)
	html = ''
	html += '<div style="display:inline-block; padding:6px 10px;'
	html += ' margin:4px 0; border:1px solid #c8c8c8; border-radius:4px;'
	html += ' background:#fafafa;">'
	html += chain
	html += '</div>'
	return html


#============================================
def build_choices(chain_length: int, deltas: list) -> tuple:
	"""
	Return (choices, answer) for the Delta-match question.

	Candidate distractors in priority order:
	1. correct: bond indices = chain_length - delta - 1
	2. wrong-end misread: bond indices = delta - 1
	   (student counted from methyl instead of COOH end)
	3. shift +1 / shift -1 on the correct bond indices (carbon-vs-bond)
	4. two random-scatter alternative placements
	First four unique CSV signatures become the four MC choices.
	"""
	correct_bonds = fatty_acid_lib.deltas_to_bond_indices(chain_length, deltas)
	# Wrong-end misread: bond indices when student counts from methyl
	misread_bonds = sorted([delta - 1 for delta in deltas])
	# Off-by-one shifts on the correct bond indices
	shift_p1_bonds = fatty_acid_lib.shift_bond_indices(correct_bonds, 1, chain_length)
	shift_m1_bonds = fatty_acid_lib.shift_bond_indices(correct_bonds, -1, chain_length)
	# Random alternative scatters: pick fresh delta positions and convert
	scatter_a_deltas = fatty_acid_lib.pool_eliminate_positions(chain_length, len(deltas))
	scatter_b_deltas = fatty_acid_lib.pool_eliminate_positions(chain_length, len(deltas))
	scatter_a_bonds = fatty_acid_lib.deltas_to_bond_indices(chain_length, scatter_a_deltas)
	scatter_b_bonds = fatty_acid_lib.deltas_to_bond_indices(chain_length, scatter_b_deltas)
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
	correct_html = build_choice_html(chain_length, correct_bonds)
	choices = [build_choice_html(chain_length, c) for c in chosen]
	random.shuffle(choices)
	return choices, correct_html


#============================================
def write_question(N: int, args) -> str:
	"""
	Generate one match-Delta-to-structure MC question.
	"""
	chain_length = random.randint(16, 22)
	num_double_bonds = random.randint(2, 3)
	# Delta positions live in the same valid range as omega positions
	# (3..chain_length-2); pool elimination reuses the same picker.
	deltas = fatty_acid_lib.pool_eliminate_positions(chain_length, num_double_bonds)
	if len(deltas) < 2:
		return None
	delta_html = fatty_acid_lib.format_delta_html(deltas)
	question_text = ''
	question_text += f'<p>A polyunsaturated fatty acid with {chain_length} carbons '
	question_text += f'is described by the notation {delta_html}. Each candidate '
	question_text += 'structure below shows a skeletal zigzag with the methyl end on '
	question_text += 'the left (H<sub>3</sub>C) and the carboxyl end on the right '
	question_text += '(COOH); each vertex and line end represents one carbon atom.</p>'
	question_text += f'<p>Which structure correctly matches the {delta_html} notation?</p>'
	choices, answer = build_choices(chain_length, deltas)
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
		description='Generate fatty acid match-Delta MC questions (read notation, pick structure).'
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
