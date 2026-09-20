#!/usr/bin/env python3

"""Generate circular-DNA restriction-digest gel-band questions.

Cut-placement rules: CUT_PLACEMENT.md.
"""

import math
import random

import bptools
import digest_lib
import dna_render_lib


MAP_LEFT = 80
MAP_TOP = 56
MAP_WIDTH = 360
MAP_HEIGHT = 240
MAP_RADIUS = 40
DNA_STROKE = 7
CANVAS_WIDTH = 520
CANVAS_HEIGHT = 336
LABEL_PAD = 4
COORD_LABEL_HALF_WIDTH = 24
ENZYME_LABEL_HALF_WIDTH = 28
LABEL_HALF_HEIGHT = 9
ENZYME_CORNER_PAD = 20
STRAIGHT_REGIONS = ('top', 'right', 'bottom', 'left')


#============================================
def get_circular_fragment_sizes(length: int, cut_sites: list[int]) -> list[int]:
	"""Return distinct gel-band sizes from cuts in a circular DNA molecule."""
	if length < 3:
		raise ValueError("Circular DNA must be at least 3 kb long.")
	if len(cut_sites) < 2:
		raise ValueError("A circular digest needs at least two cut sites.")
	if len(set(cut_sites)) != len(cut_sites):
		raise ValueError("Cut sites must be unique.")
	if any(site < 0 or site >= length for site in cut_sites):
		raise ValueError("Cut sites must be between 0 kb and the plasmid length.")

	fragment_sizes = digest_lib.circular_fragment_list(length, cut_sites)
	distinct_sizes = sorted(set(fragment_sizes))
	return distinct_sizes


#============================================
def _centerline_box() -> tuple[float, float, float, float, float]:
	"""Return left, top, width, height, and corner radius of the stroke centerline."""
	half_stroke = DNA_STROKE / 2
	left = MAP_LEFT + half_stroke
	top = MAP_TOP + half_stroke
	width = MAP_WIDTH - DNA_STROKE
	height = MAP_HEIGHT - DNA_STROKE
	radius = MAP_RADIUS - half_stroke
	return left, top, width, height, radius


#============================================
def perimeter_length() -> float:
	"""Return the stroke-centerline length of the rounded rectangle."""
	straight_h = MAP_WIDTH - 2 * MAP_RADIUS
	straight_v = MAP_HEIGHT - 2 * MAP_RADIUS
	radius = MAP_RADIUS - DNA_STROKE / 2
	length = 2 * straight_h + 2 * straight_v + 2 * math.pi * radius
	return length


#============================================
def _arc_point(center_x: float, center_y: float, radius: float, start_deg: float,
		span_deg: float, distance: float, region: str) -> tuple[float, float, float, str]:
	"""Place a point on a clockwise quarter-circle; angles are screen degrees."""
	theta = start_deg + span_deg * (distance / (math.pi / 2 * radius))
	theta = theta % 360
	rad = math.radians(theta)
	x_position = center_x + radius * math.cos(rad)
	y_position = center_y + radius * math.sin(rad)
	return x_position, y_position, theta, region


#============================================
def point_at_distance(distance: float) -> tuple[float, float, float, str]:
	"""Map a clockwise distance from top-center onto the stroke centerline."""
	left, top, width, height, radius = _centerline_box()
	right = left + width
	bottom = top + height
	center_x = left + width / 2
	straight_h = MAP_WIDTH - 2 * MAP_RADIUS
	straight_v = MAP_HEIGHT - 2 * MAP_RADIUS
	half_top = straight_h / 2
	arc = math.pi / 2 * radius
	# 0 kb is the midpoint of the top straight; wrap finishes on the left half.
	if distance <= half_top:
		return center_x + distance, top, 270.0, 'top'
	distance -= half_top
	if distance <= arc:
		return _arc_point(right - radius, top + radius, radius, 270.0, 90.0, distance, 'top-right')
	distance -= arc
	if distance <= straight_v:
		return right, top + radius + distance, 0.0, 'right'
	distance -= straight_v
	if distance <= arc:
		return _arc_point(right - radius, bottom - radius, radius, 0.0, 90.0, distance, 'bottom-right')
	distance -= arc
	if distance <= straight_h:
		return right - radius - distance, bottom, 90.0, 'bottom'
	distance -= straight_h
	if distance <= arc:
		return _arc_point(left + radius, bottom - radius, radius, 90.0, 90.0, distance, 'bottom-left')
	distance -= arc
	if distance <= straight_v:
		return left, bottom - radius - distance, 180.0, 'left'
	distance -= straight_v
	if distance <= arc:
		return _arc_point(left + radius, top + radius, radius, 180.0, 90.0, distance, 'top-left')
	distance -= arc
	return center_x - half_top + distance, top, 270.0, 'top'


#============================================
def get_perimeter_point(coordinate: int, length: int) -> tuple[float, float, float, str]:
	"""Map an integer kb onto the complete rounded-rectangle perimeter."""
	distance = coordinate / length * perimeter_length()
	return point_at_distance(distance)


#============================================
def is_enzyme_eligible(coordinate: int, length: int) -> bool:
	"""Return True when a site is on a straight with room for an inside enzyme label."""
	x_position, y_position, _angle_deg, region = get_perimeter_point(coordinate, length)
	if region not in STRAIGHT_REGIONS:
		return False
	left, top, width, height, radius = _centerline_box()
	right = left + width
	bottom = top + height
	if region in ('top', 'bottom'):
		return (
			x_position >= left + radius + ENZYME_CORNER_PAD
			and x_position <= right - radius - ENZYME_CORNER_PAD
		)
	return (
		y_position >= top + radius + ENZYME_CORNER_PAD
		and y_position <= bottom - radius - ENZYME_CORNER_PAD
	)


#============================================
def _outward_unit(angle_deg: float) -> tuple[float, float]:
	"""Return the screen-space outward unit vector (0 deg points right)."""
	rad = math.radians(angle_deg)
	return math.cos(rad), math.sin(rad)


#============================================
def _label_center(x_position: float, y_position: float, angle_deg: float, inward: bool,
		tick_length: int, half_width: int) -> tuple[int, int]:
	"""Place a horizontal label just beyond the tick along the local normal."""
	out_x, out_y = _outward_unit(angle_deg)
	half_along = abs(out_x) * half_width + abs(out_y) * LABEL_HALF_HEIGHT
	distance = tick_length / 2 + LABEL_PAD + half_along
	if inward:
		distance = -distance
	label_x = x_position + out_x * distance
	label_y = y_position + out_y * distance
	return round(label_x), round(label_y)


#============================================
def add_coordinate_marker(parts: list[str], coordinate: int, x_position: float,
		y_position: float, angle_deg: float, color: str, tick_length: int) -> None:
	"""Draw one perimeter tick and its outside horizontal kb label."""
	css_angle = angle_deg - 270.0
	out_x, out_y = _outward_unit(angle_deg)
	tick_x = x_position
	tick_y = y_position
	# Extra enzyme length grows inward; keep the outward end on the ordinary tick.
	if tick_length > dna_render_lib.TICK_LENGTH:
		extra = tick_length - dna_render_lib.TICK_LENGTH
		tick_x -= out_x * extra / 2
		tick_y -= out_y * extra / 2
	parts.append(dna_render_lib.make_positioned(
		dna_render_lib.make_rotated_tick(color, css_angle, tick_length),
		round(tick_x), round(tick_y), anchor='middle'
	))
	label_x, label_y = _label_center(
		x_position, y_position, angle_deg, False, dna_render_lib.TICK_LENGTH,
		COORD_LABEL_HALF_WIDTH
	)
	parts.append(dna_render_lib.make_positioned(
		dna_render_lib.make_coordinate_label(coordinate), label_x, label_y, anchor='middle'
	))


#============================================
def add_enzyme_label(parts: list[str], enzyme_name: str, color: str, x_position: float,
		y_position: float, angle_deg: float) -> None:
	"""Draw a horizontal enzyme name just inside the DNA at a straight-edge site."""
	tick_length = dna_render_lib.TICK_LENGTH + dna_render_lib.TICK_LABEL_EXTRA
	label_x, label_y = _label_center(
		x_position, y_position, angle_deg, True, tick_length, ENZYME_LABEL_HALF_WIDTH
	)
	parts.append(dna_render_lib.make_positioned(
		dna_render_lib.make_enzyme_label(enzyme_name, color), label_x, label_y, anchor='middle'
	))


#============================================
def make_circular_map(length: int, site_to_enzyme: dict[int, str]) -> str:
	"""Draw a rounded-rectangle plasmid map using shared inline-CSS primitives."""
	color_map = dna_render_lib.enzyme_color_map(list(site_to_enzyme.values()))
	parts = [
		f'<span style="border: {DNA_STROKE}px solid {dna_render_lib.DNA_ORANGE}; '
		f'border-radius: {MAP_RADIUS}px; box-sizing: border-box; height: {MAP_HEIGHT}px; '
		f'left: {MAP_LEFT}px; position: absolute; top: {MAP_TOP}px; '
		f'width: {MAP_WIDTH}px;">&nbsp;</span>'
	]
	for coordinate in range(length):
		x_position, y_position, angle_deg, _region = get_perimeter_point(coordinate, length)
		tick_color = dna_render_lib.COORDINATE_BLACK
		tick_length = dna_render_lib.TICK_LENGTH
		if coordinate in site_to_enzyme:
			enzyme_name = site_to_enzyme[coordinate]
			tick_color = color_map[enzyme_name]
			tick_length += dna_render_lib.TICK_LABEL_EXTRA
			add_enzyme_label(parts, enzyme_name, tick_color, x_position, y_position, angle_deg)
		add_coordinate_marker(
			parts, coordinate, x_position, y_position, angle_deg, tick_color, tick_length
		)
	map_html = dna_render_lib.make_canvas(
		CANVAS_WIDTH, CANVAS_HEIGHT, ''.join(parts), 'Circular restriction-digest DNA map.'
	)
	return map_html


#============================================
def _sample_sites(possible_sites: list[int], count: int) -> list[int]:
	"""Return a sorted random subset, matching linear get_rand_list()."""
	sites = list(possible_sites)
	random.shuffle(sites)
	while len(sites) > count:
		sites.pop()
	sites.sort()
	return sites


#============================================
def _assign_circular_enzymes(nonzero_sites: list[int], selected_count: int
		) -> tuple[list[int], list[int]]:
	"""Keep 0 kb as B and mix remaining sites; 2+2 is B A B A."""
	# extra B sites besides the origin
	extra_b_count = len(nonzero_sites) - selected_count
	interior_indices = list(range(1, len(nonzero_sites) - 1))
	if extra_b_count <= len(interior_indices):
		extra_indices = set(random.sample(interior_indices, extra_b_count))
	else:
		extra_indices = set(random.sample(range(len(nonzero_sites)), extra_b_count))
	selected_sites = []
	distractor_sites = [0]
	for index, site in enumerate(nonzero_sites):
		if index in extra_indices:
			distractor_sites.append(site)
		else:
			selected_sites.append(site)
	return selected_sites, distractor_sites


#============================================
def choose_sites(length: int, selected_count: int, difficulty: str,
		distractor_count: int = 2) -> tuple[list[int], list[int]]:
	"""Choose mixed sites with the distractor at 0 kb until evaluation accepts."""
	if selected_count < 2:
		raise ValueError("The selected enzyme needs at least two sites.")
	if distractor_count < 2:
		raise ValueError("The distractor enzyme needs at least two sites.")
	# Corners stay enzyme-free; 0 kb is always a distractor site on the top straight.
	possible_sites = [
		site for site in range(1, length) if is_enzyme_eligible(site, length)
	]
	required_nonzero = selected_count + (distractor_count - 1)
	if required_nonzero > len(possible_sites):
		raise ValueError("DNA length is too short for the requested number of sites.")
	for _ in range(100):
		picked = _sample_sites(possible_sites, required_nonzero)
		selected_sites, distractor_sites = _assign_circular_enzymes(picked, selected_count)
		if digest_lib.map_is_acceptable(
				'circular', length, selected_sites, distractor_sites, difficulty
				) is True:
			return selected_sites, distractor_sites
	raise ValueError("Could not place restriction sites that meet the digest rules.")


#============================================
def write_question(N: int, args):
	"""Create one circular restriction-digest gel-band question."""
	enzyme_name, distractor_enzyme_name = digest_lib.choose_distinct_enzyme_names()
	cut_sites, distractor_sites = choose_sites(
		args.length, args.sites_per_enzyme, args.difficulty
	)
	band_sizes = get_circular_fragment_sizes(args.length, cut_sites)
	if len(band_sizes) < 2:
		return None

	site_to_enzyme = {}
	for site in cut_sites:
		site_to_enzyme[site] = enzyme_name
	for site in distractor_sites:
		site_to_enzyme[site] = distractor_enzyme_name

	plasmid_map = make_circular_map(args.length, site_to_enzyme)
	color_map = dna_render_lib.enzyme_color_map((enzyme_name, distractor_enzyme_name))
	enzyme_html = dna_render_lib.colored_enzyme_name(enzyme_name, color_map[enzyme_name])
	distractor_html = dna_render_lib.colored_enzyme_name(
		distractor_enzyme_name, color_map[distractor_enzyme_name]
	)
	context_html = digest_lib.enzyme_context_paragraph(
		enzyme_html, enzyme_name, distractor_html, distractor_enzyme_name
	)
	question_text = (
		f'{context_html}'
		f'<p>The map shows an intact <strong>{args.length} kb circular DNA molecule</strong>. '
		'Each enzyme name marks a restriction site. The 0 kb coordinate is the map origin; '
		'it is not necessarily cut by the enzyme in the question.</p>'
		f'{plasmid_map}'
		f'<p>After digesting the DNA with {enzyme_html} <strong>only</strong>, which '
		'<strong>distinct DNA band sizes</strong> will you see on an agarose gel? Select all '
		'that apply.</p>'
	)
	max_choice = max(max(band_sizes), 5)
	choices_list = [f'{size} kb' for size in range(1, max_choice + 1)]
	answers_list = [f'{size} kb' for size in band_sizes]
	return bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)


#============================================
def parse_arguments():
	parser = digest_lib.make_digest_parser("Generate circular restriction digest questions.")
	parser.add_argument(
		'-s', '--sites-per-enzyme', '--sites_per_enzyme', type=int, default=None,
		dest='sites_per_enzyme', help='Number of selected-enzyme restriction sites.'
	)
	args = parser.parse_args()
	# Easy uses two selected sites; medium and rigorous use three.
	presets = {'easy': (10, 2), 'medium': (12, 3), 'rigorous': (16, 3)}
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
def main():
	args = parse_arguments()
	bptools.apply_anticheat_args(args)
	outfile = bptools.make_outfile(
		f'length_{args.length}', f'sites_{args.sites_per_enzyme}_selected'
	)
	bptools.collect_and_write_questions(write_question, args, outfile)


#============================================
if __name__ == '__main__':
	main()
