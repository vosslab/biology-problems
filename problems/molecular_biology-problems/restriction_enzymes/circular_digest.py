#!/usr/bin/env python3

"""
Authoring contract
------------------
Question family: multiple answer (MA), asking students to identify gel bands.
Output: Blackboard BBQ text, with optional shared Blackboard pool export.
Randomization: each run selects a fresh enzyme pair and nonzero sites.
Sanitization: shared anti-cheat flags are enabled through bptools.make_arg_parser.
Example: a 12 kb plasmid cut by one enzyme at 2 kb and 7 kb produces 5 kb and 7 kb bands.
"""

import random

import bptools
import restrictlib

PLASMID_ORANGE = "#b74300"
CUT_NAVY = "#0067cc"


#============================================
#============================================
def get_circular_fragment_sizes(length: int, cut_sites: list[int]) -> list[int]:
	"""Return distinct gel-band sizes from cuts in a circular DNA molecule."""
	if length < 3:
		raise ValueError("Circular DNA must be at least 3 kb long.")
	if len(cut_sites) < 2:
		raise ValueError("A circular digest needs at least two cut sites.")
	if len(set(cut_sites)) != len(cut_sites):
		raise ValueError("Cut sites must be unique.")
	if any(site <= 0 or site >= length for site in cut_sites):
		raise ValueError("Cut sites must be between 0 kb and the plasmid length.")

	sorted_sites = sorted(cut_sites)
	fragment_sizes = [
		sorted_sites[index + 1] - sorted_sites[index]
		for index in range(len(sorted_sites) - 1)
	]
	fragment_sizes.append(length - sorted_sites[-1] + sorted_sites[0])
	return sorted(set(fragment_sizes))


#============================================
#============================================
def get_site_side(site: int, length: int) -> str:
	"""Place a coordinate label around the rounded plasmid map."""
	progress = site / length
	if progress < 0.25:
		return "top"
	if progress < 0.50:
		return "right"
	if progress < 0.75:
		return "bottom"
	return "left"


#============================================
#============================================
def make_tick_mark(side: str, color: str, width: int) -> str:
	"""Return a cardinal-direction tick: vertical on long edges, horizontal on short edges."""
	if side in ("top", "bottom"):
		return (
			f'<span style="display: inline-block; height: 24px; border-left: {width}px solid '
			f'{color}; vertical-align: middle;"></span>'
		)
	return (
		f'<span style="display: inline-block; width: 24px; border-top: {width}px solid '
		f'{color}; vertical-align: middle;"></span>'
	)


#============================================
#============================================
def make_coordinate_label(site: int, side: str, enzyme_name: str | None = None) -> str:
	"""Return a cardinal tick with an actual site label or the neutral 0 kb marker."""
	if enzyme_name is None:
		tick_mark = make_tick_mark(side, "#666666", 3)
		return (
			'<span style="display: inline-block; padding: 3px 8px; white-space: nowrap; '
			f'color: #444444;">{tick_mark} <strong>0 kb</strong></span>'
		)
	tick_mark = make_tick_mark(side, CUT_NAVY, 6)
	return (
		'<span style="display: inline-block; padding: 3px 8px; white-space: nowrap; '
		f'color: #202020;">{tick_mark} <i>{enzyme_name}</i><br/>'
		f'<span style="font-family: monospace;">{site} kb</span></span>'
	)


#============================================
#============================================
def make_circular_map(length: int, site_to_enzyme: dict[int, str]) -> str:
	"""Draw a rounded-rectangle plasmid map using inline table border styling."""
	side_labels = {"top": [make_coordinate_label(0, "top")], "right": [], "bottom": [], "left": []}
	for site in sorted(site_to_enzyme):
		side = get_site_side(site, length)
		side_labels[side].append(make_coordinate_label(site, side, site_to_enzyme[site]))

	def join_labels(side: str) -> str:
		return " ".join(side_labels[side]) or "&nbsp;"

	plasmid = (
		'<table cellpadding="0" cellspacing="0" border="0" align="center" '
		f'style="width: 480px; height: 190px; border: 6px solid {PLASMID_ORANGE}; '
		'border-radius: 72px; border-collapse: separate; border-spacing: 0; '
		'background-color: #fffdf9;"><tbody><tr><td>&nbsp;</td></tr></tbody></table>'
	)
	return (
		'<table cellpadding="0" cellspacing="0" border="0" align="center" '
		'style="border-collapse: collapse; text-align: center;"><tbody>'
		f'<tr><td colspan="3">{join_labels("top")}</td></tr>'
		f'<tr><td style="width: 130px; text-align: right;">{join_labels("left")}</td>'
		f'<td style="background-color: #fffdf9;">{plasmid}</td>'
		f'<td style="width: 130px; text-align: left;">{join_labels("right")}</td></tr>'
		f'<tr><td colspan="3">{join_labels("bottom")}</td></tr>'
		'</tbody></table>'
	)


#============================================
#============================================
def choose_enzyme_names() -> tuple[str, str]:
	"""Select readily distinguishable restriction-enzyme labels for a map."""
	enzymes = restrictlib.get_enzyme_list()
	first_enzyme = restrictlib.random_enzyme_one_end(enzymes)
	second_enzyme = restrictlib.random_enzyme_one_end(enzymes, badletter=first_enzyme.__name__[0])
	return first_enzyme.__name__, second_enzyme.__name__


#============================================
#============================================
def choose_sites(length: int, sites_per_enzyme: int) -> tuple[list[int], list[int]]:
	"""Choose nonzero sites so 0 kb remains only a coordinate distractor."""
	if sites_per_enzyme < 2:
		raise ValueError("Each enzyme needs at least two sites.")
	possible_sites = list(range(1, length))
	required_sites = sites_per_enzyme * 2
	if required_sites > len(possible_sites):
		raise ValueError("DNA length is too short for the requested number of sites.")
	random.shuffle(possible_sites)
	first_sites = sorted(possible_sites[:sites_per_enzyme])
	second_sites = sorted(possible_sites[sites_per_enzyme:required_sites])
	return first_sites, second_sites


#============================================
#============================================
def write_question(N: int, args):
	"""Create one circular restriction-digest gel-band question."""
	enzyme_name, distractor_enzyme_name = choose_enzyme_names()
	cut_sites, distractor_sites = choose_sites(args.length, args.sites_per_enzyme)
	band_sizes = get_circular_fragment_sizes(args.length, cut_sites)
	if len(band_sizes) < 2:
		return None

	site_to_enzyme = {}
	for site in cut_sites:
		site_to_enzyme[site] = enzyme_name
	for site in distractor_sites:
		site_to_enzyme[site] = distractor_enzyme_name

	plasmid_map = make_circular_map(args.length, site_to_enzyme)
	question_text = (
		f'<p>The map shows an intact <strong>{args.length} kb circular DNA molecule</strong>. '
		'Each enzyme name marks a restriction site. The gray 0 kb marker establishes the '
		'coordinate system.</p>'
		f'{plasmid_map}'
		f'<p>After digesting the DNA with <i>{enzyme_name}</i> <strong>only</strong>, which '
		'<strong>distinct DNA band sizes</strong> will you see on an agarose gel? Select all '
		'that apply.</p>'
	)
	max_choice = max(max(band_sizes), 5)
	choices_list = [f'{size} kb' for size in range(1, max_choice + 1)]
	answers_list = [f'{size} kb' for size in band_sizes]
	return bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)


#============================================
#============================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate circular restriction digest questions.")
	parser = bptools.add_difficulty_args(parser)
	parser.add_argument(
		'-n', '--length', type=int, default=None,
		help='Length of the circular DNA molecule in kb.'
	)
	parser.add_argument(
		'-s', '--sites-per-enzyme', '--sites_per_enzyme', type=int, default=None,
		dest='sites_per_enzyme', help='Number of sites for each enzyme.'
	)
	args = parser.parse_args()
	presets = {
		'easy': (10, 2),
		'medium': (12, 3),
		'rigorous': (16, 3),
	}
	default_length, default_sites = presets[args.difficulty]
	if args.length is None:
		args.length = default_length
	if args.sites_per_enzyme is None:
		args.sites_per_enzyme = default_sites
	if args.length < 5:
		raise ValueError("Circular DNA length must be at least 5 kb.")
	if args.sites_per_enzyme < 2:
		raise ValueError("Each enzyme needs at least two restriction sites.")
	if args.sites_per_enzyme * 2 >= args.length:
		raise ValueError("DNA length needs open nonzero coordinates after placing all sites.")
	return args


#============================================
#============================================
def main():
	args = parse_arguments()
	bptools.apply_anticheat_args(args)
	outfile = bptools.make_outfile(
		f'length_{args.length}',
		f'sites_{args.sites_per_enzyme}_per_enzyme',
	)
	bptools.collect_and_write_questions(write_question, args, outfile)


#============================================
#============================================
if __name__ == '__main__':
	main()
