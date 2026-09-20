#!/usr/bin/env python3

"""Generate linear-DNA restriction-digest gel-band questions.

Cut-placement rules: CUT_PLACEMENT.md.
"""

import math
import random

import bptools
import digest_lib
import dna_render_lib


debug = False


#============================================
def _dotted_dna_segment(left: int, top: int, width: int) -> str:
	"""Return a dashed orange DNA continuation aligned with the solid 6 px strand."""
	dash_width = 6
	gap_width = 4
	parts = []
	position = left
	while position + dash_width <= left + width:
		parts.append(
			f'<span style="background-color: {dna_render_lib.DNA_ORANGE}; height: 6px; '
			f'left: {position}px; position: absolute; top: {top}px; '
			f'width: {dash_width}px;">&nbsp;</span>'
		)
		position += dash_width + gap_width
	segment_html = ''.join(parts)
	return segment_html


#============================================
def make_linear_map(length: int, label_dict: dict[int, str], dna_type: str) -> str:
	"""Draw a linear DNA map with centered labels and uniformly sized cut ticks."""
	space_width = 60
	# Strand maps need room past both ends so the continuation reads as more DNA.
	continuation_width = 0
	if dna_type == 'strand':
		continuation_width = space_width
	side_pad = 20
	baseline_left = side_pad + continuation_width
	baseline_width = length * space_width
	baseline_top = 68
	canvas_width = baseline_left + baseline_width + side_pad + continuation_width
	color_map = dna_render_lib.enzyme_color_map(list(label_dict.values()))
	parts = []

	# The finite orange segment is the molecule under restriction analysis.
	parts.append(
		f'<span style="background-color: {dna_render_lib.DNA_ORANGE}; height: 6px; '
		f'left: {baseline_left}px; position: absolute; top: {baseline_top}px; '
		f'width: {baseline_width}px;">&nbsp;</span>'
	)
	if dna_type == 'strand':
		# Dashes continue the DNA line past both visible ends.
		parts.append(_dotted_dna_segment(side_pad, baseline_top, continuation_width - 4))
		parts.append(_dotted_dna_segment(
			baseline_left + baseline_width + 4, baseline_top, continuation_width - 4
		))

	for coordinate in range(length + 1):
		position = baseline_left + coordinate * space_width
		enzyme_name = label_dict.get(coordinate)
		tick_color = dna_render_lib.COORDINATE_BLACK
		if enzyme_name is not None:
			tick_color = color_map[enzyme_name]
			parts.append(dna_render_lib.make_positioned(
				dna_render_lib.make_enzyme_label(enzyme_name, tick_color), position, 20
			))
		tick_left = position - dna_render_lib.TICK_THICKNESS // 2
		tick_length = dna_render_lib.TICK_LENGTH
		tick_top = baseline_top + 6 // 2 - dna_render_lib.TICK_LENGTH // 2
		if enzyme_name is not None:
			# Extra length points up toward the enzyme label.
			tick_length += dna_render_lib.TICK_LABEL_EXTRA
			tick_top -= dna_render_lib.TICK_LABEL_EXTRA
		parts.append(dna_render_lib.make_positioned(
			dna_render_lib.make_vertical_tick(tick_color, tick_length), tick_left, tick_top,
			anchor='left'
		))
		parts.append(dna_render_lib.make_positioned(
			dna_render_lib.make_coordinate_label(coordinate, include_unit=False), position, 90
		))

	parts.append(dna_render_lib.make_positioned('Scale in kb', canvas_width // 2, 114))
	map_html = dna_render_lib.make_canvas(
		canvas_width, 136, ''.join(parts), 'Linear restriction-digest DNA map.'
	)
	return map_html


#============================================
def get_rand_list(size, total_length, include_ends=False):
	if include_ends is True:
		sites = list(range(total_length + 1))
	else:
		sites = list(range(1, total_length))
	random.shuffle(sites)
	while len(sites) > size:
		sites.pop()
	sites.sort()
	return sites


#============================================
def split_interleaved_sites(sites: list[int]) -> tuple[list[int], list[int]]:
	"""Assign sorted coordinates as selected, distractor, selected, ..."""
	selected_sites = []
	distractor_sites = []
	for index, site in enumerate(sites):
		if index % 2 == 0:
			selected_sites.append(site)
		else:
			distractor_sites.append(site)
	return selected_sites, distractor_sites


#============================================
def write_question(N, args):
	length = args.length
	num_sites = args.num_sites
	dna_type = args.dna_type
	max_fragment_size = args.max_fragment_size
	enzyme_name1, enzyme_name2 = digest_lib.choose_distinct_enzyme_names()

	complete_sites = num_sites + (num_sites - 1)
	if complete_sites * 2 > length:
		print(complete_sites, "too many sites for length", length)
		return None

	sites = None
	selected_sites = None
	for _ in range(100):
		candidate_sites = get_rand_list(complete_sites, length, include_ends=False)
		candidate_selected, candidate_distractor = split_interleaved_sites(candidate_sites)
		if digest_lib.map_is_acceptable(
				dna_type, length, candidate_selected, candidate_distractor, args.difficulty
				) is False:
			continue
		correct_fragments = digest_lib.digest_fragments(dna_type, length, candidate_selected)
		if max(correct_fragments) > max_fragment_size:
			continue
		sites = candidate_sites
		selected_sites = candidate_selected
		break
	if sites is None:
		return None

	label_dict = {}
	for index, site in enumerate(sites):
		if index % 2 == 0:
			label_dict[site] = enzyme_name1
		else:
			label_dict[site] = enzyme_name2
		if debug is True:
			print(site, label_dict[site])
	if debug is True:
		print("end", length)

	answers = sorted(set(digest_lib.digest_fragments(dna_type, length, selected_sites)))
	rigorous_mode = args.difficulty == 'rigorous'

	map_html = make_linear_map(length, label_dict, dna_type)
	if dna_type == 'fragment':
		header = (
			f"<p><strong>DNA Fragment Question:</strong> "
			f"Shown below is a short DNA fragment that is only {length} kb in length. "
			f"This fragment has been isolated for restriction enzyme analysis.</p>"
		)
	elif dna_type == 'strand':
		header = (
			"<p><strong>DNA Strand Question:</strong></p>"
			"<p>Examine the DNA strand shown below. The table highlights a specific portion "
			"of a much longer DNA molecule to focus on the region containing restriction sites.</p>"
		)

	color_map = dna_render_lib.enzyme_color_map((enzyme_name1, enzyme_name2))
	enzyme1_html = dna_render_lib.colored_enzyme_name(enzyme_name1, color_map[enzyme_name1])
	enzyme2_html = dna_render_lib.colored_enzyme_name(enzyme_name2, color_map[enzyme_name2])
	opening = digest_lib.enzyme_context_paragraph(
		enzyme1_html, enzyme_name1, enzyme2_html, enzyme_name2
	)
	details = ''
	if dna_type == 'strand':
		details += (
			"<p><strong>Note:</strong> The dashes at both ends of the strand indicate that the next restriction site is far away "
			"and outside the visible region. Because this segment is part of a much larger molecule, any uncut or very large fragments "
			"will not travel into the gel and will appear to be stuck in the well.</p>"
		)
	if rigorous_mode:
		details += (
			"<p><strong>Gel interpretation:</strong> This is a complete digest. DNA fragments of the same length "
			"co-migrate and appear as a single band. Select all distinct band lengths.</p>"
		)
	question = (
		f"<h6><strong>Determine the sizes of the DNA bands</strong> that would appear on an agarose gel "
		f"after digestion with {enzyme1_html} only.</h6>"
	)
	question_text = opening + header + map_html + details + question

	last_answer = max(max(answers) + 1, 5)
	choices_list = []
	answers_list = []
	for answer_size in range(1, last_answer + 1):
		choice_str = f"{answer_size:d} kb"
		choices_list.append(choice_str)
		if answer_size in answers:
			answers_list.append(choice_str)
	bb_question = bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)
	return bb_question


#============================================
def apply_difficulty_defaults(args):
	presets = {
		'easy': {'length': 10, 'num_sites': 2, 'dna_type': 'fragment'},
		'medium': {'length': 12, 'num_sites': 3, 'dna_type': 'fragment'},
		'rigorous': {'length': 16, 'num_sites': 4, 'dna_type': 'strand'},
	}
	preset = presets[args.difficulty]
	if args.length is None:
		args.length = preset['length']
	if args.dna_type is None:
		args.dna_type = preset['dna_type']
	if args.num_sites is None:
		args.num_sites = preset['num_sites']
		if args.dna_type == 'strand':
			args.num_sites = max(args.num_sites, 3)
			if args.difficulty == 'rigorous':
				args.num_sites = 4
	return args


#============================================
def parse_arguments():
	parser = digest_lib.make_digest_parser("Generate restriction digest questions.")
	parser.add_argument(
		'-s', '--num-sites', '--num_sites', type=int, default=None, dest='num_sites',
		help='Number of sites in the DNA sequence.'
	)
	parser.add_argument(
		'--max-fragment-size', '--max_fragment_size', type=int,
		default=None, dest='max_fragment_size',
		help='Maximum size of the DNA fragment.'
	)
	dna_group = parser.add_mutually_exclusive_group()
	dna_group.add_argument(
		'-T', '--dna-type', '--dna_type', dest='dna_type',
		choices=['fragment', 'strand'], type=str,
		help='Type of DNA sequence to use. Choices: fragment or strand.'
	)
	dna_group.add_argument(
		'-F', '--fragment', dest='dna_type', action='store_const', const='fragment',
		help='Use DNA fragments'
	)
	dna_group.add_argument(
		'-S', '--strand', dest='dna_type', action='store_const', const='strand',
		help='Use full DNA strands'
	)
	args = parser.parse_args()
	args = apply_difficulty_defaults(args)
	if args.max_fragment_size is None:
		args.max_fragment_size = math.ceil(args.length // 2 + 1)
	if args.dna_type == 'strand' and args.num_sites < 3:
		raise ValueError("Strand mode requires at least 3 restriction sites.")
	if args.dna_type == 'fragment' and args.num_sites < 2:
		raise ValueError("Fragment mode requires at least 2 restriction sites.")
	return args


#============================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(f"len_{args.length}", f"sites_{args.num_sites}", args.dna_type)
	bptools.collect_and_write_questions(write_question, args, outfile)


#============================================
if __name__ == '__main__':
	main()
